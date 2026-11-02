#!/usr/bin/env python3
"""In-job post-processing of a Delphes (CMS, slim_v1 card) file.
1) From the full generator record (Particle branch) compute overlap-removal truth (reports/02 §3):
   status-1 photons/leptons with a prompt flag (no hadron in the M1 ancestry; beam protons ignored),
   per-photon isolation inputs, N_prompt_photons (pT>15, |eta|<2.5, dR>0.4 to prompt leptons pT>10,
   to other such photons and to GenJets pT>20 not dominated by the photon itself), last-copy H/Z/W/t.
2) Write <out>_gen.root (TTree 'GenTruth', same entry order as 'Delphes').
3) Write <out>.root = Delphes tree cloned WITHOUT the Particle branch (ROOT TClonesArray format kept).
Usage: python3 -P slim_gentruth.py <full_delphes.root> <out_prefix>
"""
import sys, numpy as np, awkward as ak, uproot

fin, pre = sys.argv[1], sys.argv[2]
t = uproot.open(fin)["Delphes"]
A = lambda k: t[k].array()
pid, st, m1 = A("Particle/Particle.PID"), A("Particle/Particle.Status"), A("Particle/Particle.M1")
pt, eta, phi, mass = A("Particle/Particle.PT"), A("Particle/Particle.Eta"), A("Particle/Particle.Phi"), A("Particle/Particle.Mass")
apid = abs(pid)
# hadron: |pid|>100, not a beam proton, not a diquark (xx0y with 4 digits), not the Pythia system code 90
is_had = (apid > 100) & (apid != 2212) & ~((apid > 1000) & ((apid // 10) % 10 == 0))

def nonprompt_flag(sel):
    """sel: boolean jagged mask of particles to classify; returns jagged bool (True = hadron ancestor)."""
    idx = ak.local_index(pid)[sel]
    anc = m1[idx]
    flag = ak.zeros_like(anc, dtype=bool)
    for _ in range(400):
        valid = anc >= 0
        if not ak.any(valid):
            break
        safe = ak.where(valid, anc, 0)
        flag = flag | (valid & is_had[safe])
        anc = ak.where(valid & ~flag, m1[safe], -1)
    return flag

def dphi(a, b):
    return (a - b + np.pi) % (2 * np.pi) - np.pi

stable = st == 1
gsel = stable & (pid == 22) & (pt > 10) & (abs(eta) < 3.0)
lsel = stable & ((apid == 11) | (apid == 13)) & (pt > 5)
g_np = nonprompt_flag(gsel); l_np = nonprompt_flag(lsel)
G = ak.zip({"pt": pt[gsel], "eta": eta[gsel], "phi": phi[gsel], "prompt": ~g_np})
L = ak.zip({"pt": pt[lsel], "eta": eta[lsel], "phi": phi[lsel], "pid": pid[lsel], "prompt": ~l_np})
gj = ak.zip({"pt": A("GenJet/GenJet.PT"), "eta": A("GenJet/GenJet.Eta"), "phi": A("GenJet/GenJet.Phi")})
gj = gj[gj.pt > 20]

def min_dr(a, b, exclude_self=False):
    pa, pb = ak.unzip(ak.cartesian([a, b], axis=1, nested=True))
    dr = np.hypot(pa.eta - pb.eta, dphi(pa.phi, pb.phi))
    if exclude_self:
        dr = ak.where(dr < 1e-6, 999.0, dr)
    return ak.fill_none(ak.min(dr, axis=2), 999.0)

PL = L[L.prompt & (L.pt > 10)]
cand = G[G.prompt & (G.pt > 15) & (abs(G.eta) < 2.5)]
# GenJets dominated by the photon itself (dR<0.1 and pT within 50%) are not counted against it
pa, pb = ak.unzip(ak.cartesian([cand, gj], axis=1, nested=True))
drj = np.hypot(pa.eta - pb.eta, dphi(pa.phi, pb.phi))
selfjet = (drj < 0.1) & (abs(pb.pt - pa.pt) < 0.5 * pa.pt)
drj = ak.fill_none(ak.min(ak.where(selfjet, 999.0, drj), axis=2), 999.0)
iso = (min_dr(cand, PL) > 0.4) & (min_dr(cand, cand, exclude_self=True) > 0.4) & (drj > 0.4)
n_prompt = ak.sum(iso, axis=1)

# last-copy bosons / tops (daughters not same pid is not available cheaply -> take highest-index copy)
def last_copy(code):
    m = apid == code
    i = ak.argmax(ak.where(m, ak.local_index(pid), -1), axis=1, keepdims=True)
    has = ak.any(m, axis=1)
    get = lambda x: ak.where(has, ak.flatten(x[i]), -999.0)
    return get(pt), get(eta), get(phi), get(mass)

out = {"n_prompt_photons": ak.values_astype(n_prompt, np.int32),
       "gph_pt": G.pt, "gph_eta": G.eta, "gph_phi": G.phi, "gph_prompt": G.prompt,
       "glep_pt": L.pt, "glep_eta": L.eta, "glep_phi": L.phi, "glep_pid": L.pid, "glep_prompt": L.prompt}
for code, name in ((25, "H"), (23, "Z"), (24, "W"), (6, "t")):
    for v, x in zip(("pt", "eta", "phi", "m"), last_copy(code)):
        out[f"g{name}_{v}"] = ak.values_astype(x, np.float32)
with uproot.recreate(pre + "_gen.root") as f:
    f["GenTruth"] = out

import ROOT
ROOT.gROOT.SetBatch(True)
fi = ROOT.TFile.Open(fin); ti = fi.Get("Delphes")
ti.SetBranchStatus("*", 1); ti.SetBranchStatus("Particle*", 0)
fo = ROOT.TFile.Open(pre + ".root", "RECREATE", "", 505)  # ZSTD level 5
to = ti.CloneTree(-1)
to.Write(); fo.Close(); fi.Close()
print(f"events={len(n_prompt)} n_prompt_photons histogram={np.bincount(ak.to_numpy(n_prompt)).tolist()}")
