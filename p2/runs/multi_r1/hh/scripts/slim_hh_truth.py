#!/usr/bin/env python3
"""hh replacement of lib slim_gentruth.py (patches/005). In-job post-processing of a Delphes (slim_hh_v1 card) file.
1) From the generator record (Particle branch) build the truth needed for truth-tag weighting and object validation:
   event level : last-copy Higgs bosons (up to 2, pT-ordered): pt/eta/phi/m, their b-quark daughters; m_HH; last-copy tops, Z, W.
   per FatJet (same order as Delphes 'FatJet' branch): nB (B hadrons, 'last in chain' = first daughter not a B hadron) and nC (C hadrons) inside dR<0.8,
       nHb (b quarks from H->bb inside dR<0.8), nVq (quarks from W/Z not from top inside), nWq (quarks from W from top inside), ntb (b quarks from top inside).
2) Write <out>_gen.root (TTree 'GenTruth', same entry order as 'Delphes').
3) Write <out>.root = Delphes tree cloned WITHOUT the Particle branch.
Usage: python3 -P slim_hh_truth.py <full_delphes.root> <out_prefix>"""
import sys, numpy as np, awkward as ak, uproot
fin, pre = sys.argv[1], sys.argv[2]
t = uproot.open(fin)["Delphes"]
A = lambda k: t[k].array()
pid, st = A("Particle/Particle.PID"), A("Particle/Particle.Status")
m1, d1, d2 = A("Particle/Particle.M1"), A("Particle/Particle.D1"), A("Particle/Particle.D2")
pt, eta, phi, mass = A("Particle/Particle.PT"), A("Particle/Particle.Eta"), A("Particle/Particle.Phi"), A("Particle/Particle.Mass")
apid = abs(pid); idx = ak.local_index(pid)
def dphi(a, b): return (a - b + np.pi) % (2 * np.pi) - np.pi
def has_flavor(a, d):   # hadron containing a quark of digit d (4=c,5=b): meson digit hundreds, baryon digit thousands
    return ((apid // 100) % 10 == d) | ((apid // 1000) % 10 == d)
hadron = (apid > 100) & (apid != 2212) & ~((apid > 1000) & ((apid // 10) % 10 == 0))
isB, isC = hadron & has_flavor(apid, 5), hadron & ~has_flavor(apid, 5) & has_flavor(apid, 4)
safe_d1 = ak.where(d1 >= 0, d1, 0)
d1_isB = ak.where(d1 >= 0, isB[safe_d1], False); d1_isC = ak.where(d1 >= 0, isC[safe_d1], False)
Blast = isB & ~d1_isB; Clast = isC & ~d1_isC
mo = ak.where(m1 >= 0, m1, 0); mpid = ak.where(m1 >= 0, apid[mo], 0)
mm = ak.where(m1 >= 0, m1[mo], 0); mmpid = ak.where(m1 >= 0, apid[mm], 0)        # grand-mother
quark = (apid <= 5) & (apid >= 1)
# H->bb daughters: b quarks whose mother is a Higgs
bH = (apid == 5) & (mpid == 25)
qV = quark & ((mpid == 23) | (mpid == 24)); qW_top = quark & (mpid == 24) & (mmpid == 6); qV_notop = qV & ~qW_top
btop = (apid == 5) & (mpid == 6)
# last-copy Higgs: pid 25 whose first daughter is not 25
d1pid = ak.where(d1 >= 0, apid[safe_d1], 0)
Hlast = (apid == 25) & (d1pid != 25)
def top_n(code):
    m = (apid == code) & (d1pid != code)
    order = ak.argsort(-pt[m], axis=1)
    return ak.zip({"pt": pt[m][order], "eta": eta[m][order], "phi": phi[m][order], "m": mass[m][order], "idx": idx[m][order]})
H = top_n(25); Tq = top_n(6)
def nth(a, n, f, fill=-999.0): return ak.values_astype(ak.fill_none(ak.pad_none(a[f], n, axis=1)[:, n - 1], fill), np.float32)
out = {}
for n in (1, 2):
    for f in ("pt", "eta", "phi", "m"): out[f"gH{n}_{f}"] = nth(H, n, f)
out["gnH"] = ak.values_astype(ak.num(H.pt), np.int32)
# m_HH of the two leading last-copy Higgs bosons
h1 = ak.zip({"pt": nth(H, 1, "pt"), "eta": nth(H, 1, "eta"), "phi": nth(H, 1, "phi"), "m": nth(H, 1, "m")})
h2 = ak.zip({"pt": nth(H, 2, "pt"), "eta": nth(H, 2, "eta"), "phi": nth(H, 2, "phi"), "m": nth(H, 2, "m")})
def p4(h): return (h.pt * np.cosh(h.eta), h.pt * np.cos(h.phi), h.pt * np.sin(h.phi), h.pt * np.sinh(h.eta), h.m)
def minv(a, b):
    ea = np.sqrt(a.m**2 + (a.pt * np.cosh(a.eta))**2); eb = np.sqrt(b.m**2 + (b.pt * np.cosh(b.eta))**2)
    px = a.pt * np.cos(a.phi) + b.pt * np.cos(b.phi); py = a.pt * np.sin(a.phi) + b.pt * np.sin(b.phi); pz = a.pt * np.sinh(a.eta) + b.pt * np.sinh(b.eta)
    return np.sqrt(np.maximum((ea + eb)**2 - px**2 - py**2 - pz**2, 0.0))
out["gmHH"] = ak.values_astype(ak.where((out["gH1_pt"] > 0) & (out["gH2_pt"] > 0), minv(h1, h2), -999.0), np.float32)
out["gntop"] = ak.values_astype(ak.num(Tq.pt), np.int32)
for n in (1, 2):
    for f in ("pt", "eta", "phi", "m"): out[f"gt{n}_{f}"] = nth(Tq, n, f)
# per-FatJet truth
fpt, feta, fphi = A("FatJet/FatJet.PT"), A("FatJet/FatJet.Eta"), A("FatJet/FatJet.Phi")
def count_in(sel, R=0.8):
    ps = ak.zip({"eta": eta[sel], "phi": phi[sel]})
    a, b = ak.unzip(ak.cartesian([ak.zip({"eta": feta, "phi": fphi}), ps], axis=1, nested=True))
    dr = np.hypot(a.eta - b.eta, dphi(a.phi, b.phi))
    return ak.values_astype(ak.sum(dr < R, axis=2), np.int32)
for name, sel in (("nB", Blast & (pt > 5)), ("nC", Clast & (pt > 5)), ("nHb", bH), ("nVq", qV_notop), ("nWq", qW_top), ("ntb", btop)):
    out["fj_" + name] = count_in(sel)
st23 = st == 23
out["g_nhard_b"] = ak.values_astype(ak.sum(st23 & (pid == 5), axis=1), np.int32); out["g_nhard_bbar"] = ak.values_astype(ak.sum(st23 & (pid == -5), axis=1), np.int32)
out["g_nhard_c"] = ak.values_astype(ak.sum(st23 & (apid == 4), axis=1), np.int32)
out["fj_pt"] = fpt
with uproot.recreate(pre + "_gen.root") as f:
    f["GenTruth"] = out
import ROOT
ROOT.gROOT.SetBatch(True)
fi = ROOT.TFile.Open(fin); ti = fi.Get("Delphes")
ti.SetBranchStatus("*", 1); ti.SetBranchStatus("Particle*", 0)
fo = ROOT.TFile.Open(pre + ".root", "RECREATE", "", 505)
to = ti.CloneTree(-1)
to.Write(); fo.Close(); fi.Close()
print(f"events={len(out['gnH'])} gnH histogram={np.bincount(ak.to_numpy(out['gnH'])).tolist()}")
