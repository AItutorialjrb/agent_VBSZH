#!/usr/bin/env python3
"""A1 (2026-11-03): Delphes m_jj resolution and safety of the generator cut mmjj > 400 GeV used by the VBS-biased samples.
Inputs: Tier-1 v1 EW and QCD ZHjj (generated WITHOUT an mjj cut: mmjj = 0, ptj > 20) -> LHE (parton level) + Delphes.
Event i of the Delphes tree = event i of the LHE file (fixed order, no Pythia vetoes; checked by length).
Objects as in ntuple.py: electrons/muons pT>10 (all), photons pT>20 |eta|<2.5 (leading two, lepton-cleaned);
tag jets = two leading Delphes jets pT>25 |eta|<4.7 with dR>0.4 to all leptons and to the two leading photons.
Matched gen jets = nearest GenJet (dR<0.4) to each tag jet. Preselection-like requirement: >=2 leptons, >=2 photons.
Outputs work/theory/mjj_resolution.json:
  sigma68 of mjj(reco)/mjj(matched GenJets) - 1 overall and per gen-mjj bin;
  P(max parton-pair mjj < 400 | reco mjj > X [, |deta|>3.5]) for X = 400, 450, 500: the fraction of reco-selected events a
  generator cut mmjj > 400 (MG5 applies it to every parton pair) would remove.
Usage: python3 -P mjj_resolution.py [nfiles=20]"""
import sys, glob, gzip, json, numpy as np, uproot, awkward as ak
P = "/eos/user/r/rjiang/vbs_zh_codex_starter"; NF = int(sys.argv[1]) if len(sys.argv) > 1 else 20
def lhe_maxmjj(f):
    out = []; ev = None
    for line in gzip.open(f, "rt"):
        if line.startswith("<event"): ev = []; hdr = True; continue
        if line.startswith("</event"):
            q = [p for p in ev if np.hypot(p[0], p[1]) > 0]; best = 0.0
            for i in range(len(q)):
                for j in range(i + 1, len(q)):
                    s = q[i] + q[j]; best = max(best, np.sqrt(max(s[3]**2 - s[0]**2 - s[1]**2 - s[2]**2, 0)))
            out.append(best); ev = None; continue
        if ev is None: continue
        t = line.split()
        if hdr: hdr = False; continue
        if len(t) == 13 and t[1] == "1" and (abs(int(t[0])) <= 5 or t[0] == "21"): ev.append(np.array([float(t[6]), float(t[7]), float(t[8]), float(t[9])]))
    return np.array(out)
def dR(e1, p1, e2, p2): return np.hypot(e1 - e2, (p1 - p2 + np.pi) % (2*np.pi) - np.pi)
def mjj(pt, eta, phi, m):
    px, py, pz = pt*np.cos(phi), pt*np.sin(phi), pt*np.sinh(eta); E = np.sqrt(px**2 + py**2 + pz**2 + m**2)
    return np.sqrt(np.maximum(E.sum(1)**2 - px.sum(1)**2 - py.sum(1)**2 - pz.sum(1)**2, 0))
def process(f):
    B = uproot.open(f)["Delphes"].arrays(["Jet.PT", "Jet.Eta", "Jet.Phi", "Jet.Mass", "GenJet.PT", "GenJet.Eta", "GenJet.Phi", "GenJet.Mass",
        "Electron.PT", "Electron.Eta", "Electron.Phi", "Muon.PT", "Muon.Eta", "Muon.Phi", "Photon.PT", "Photon.Eta", "Photon.Phi"], library="ak")
    n = len(B); R = np.full((n, 4), np.nan)   # reco mjj, reco deta, matched-gen mjj, ok
    for i in range(n):
        le = np.r_[ak.to_numpy(B["Electron.Eta"][i])[ak.to_numpy(B["Electron.PT"][i]) > 10], ak.to_numpy(B["Muon.Eta"][i])[ak.to_numpy(B["Muon.PT"][i]) > 10]]
        lp = np.r_[ak.to_numpy(B["Electron.Phi"][i])[ak.to_numpy(B["Electron.PT"][i]) > 10], ak.to_numpy(B["Muon.Phi"][i])[ak.to_numpy(B["Muon.PT"][i]) > 10]]
        gpt, ge, gp = (ak.to_numpy(B[f"Photon.{k}"][i]) for k in ("PT", "Eta", "Phi"))
        gs = (gpt > 20) & (abs(ge) < 2.5) & np.array([np.all(dR(ge[k], gp[k], le, lp) > 0.4) for k in range(len(gpt))], bool)
        ge, gp = ge[gs][:2], gp[gs][:2]
        if len(le) < 2 or len(ge) < 2: continue
        ce, cp = np.r_[le, ge], np.r_[lp, gp]
        jpt, je, jp, jm = (ak.to_numpy(B[f"Jet.{k}"][i]) for k in ("PT", "Eta", "Phi", "Mass"))
        js = (jpt > 25) & (abs(je) < 4.7) & np.array([np.all(dR(je[k], jp[k], ce, cp) > 0.4) for k in range(len(jpt))], bool)
        if js.sum() < 2: continue
        o = np.where(js)[0][np.argsort(-jpt[js])][:2]
        R[i, 0] = mjj(jpt[o][None], je[o][None], jp[o][None], jm[o][None])[0]; R[i, 1] = abs(je[o[0]] - je[o[1]])
        hpt, he, hp, hm = (ak.to_numpy(B[f"GenJet.{k}"][i]) for k in ("PT", "Eta", "Phi", "Mass"))
        mt = [np.argmin(dR(je[k], jp[k], he, hp)) if len(he) and dR(je[k], jp[k], he, hp).min() < 0.4 else -1 for k in o]
        if min(mt) >= 0 and mt[0] != mt[1]: R[i, 2] = mjj(hpt[mt][None], he[mt][None], hp[mt][None], hm[mt][None])[0]
        R[i, 3] = 1
    return R
OUT = {}
for s in ("ew_zhjj_zll", "qcd_zhjj_zll"):
    fs = [f for f in sorted(glob.glob(f"{P}/production/v1/{s}/*.root")) if "_gen" not in f and glob.glob(f.replace(".root", ".lhe.gz"))][:NF]
    A, L = [], []
    for f in fs:
        R = process(f); m = lhe_maxmjj(f.replace(".root", ".lhe.gz"))
        if len(m) != len(R): print("skip (length mismatch)", f); continue
        A.append(R); L.append(m)
    A = np.concatenate(A); L = np.concatenate(L); ok = A[:, 3] == 1
    rec, de, gen = A[:, 0], A[:, 1], A[:, 2]; mg = ok & np.isfinite(gen) & (gen > 200)
    rel = rec[mg]/gen[mg] - 1; q = np.percentile(rel, [16, 50, 84])
    byb = []
    for lo, hi in ((200, 400), (400, 600), (600, 1000), (1000, 4000)):
        mm = mg & (gen > lo) & (gen < hi); r = rec[mm]/gen[mm] - 1
        qq = np.percentile(r, [16, 50, 84]) if mm.sum() > 20 else [np.nan]*3
        byb.append(dict(gen_mjj=[lo, hi], n=int(mm.sum()), median=float(qq[1]), sigma68=float((qq[2] - qq[0])/2)))
    o = dict(files=len(fs), n_events=int(len(A)), n_presel=int(ok.sum()), sigma68_rel=float((q[2] - q[0])/2), median_rel=float(q[1]), by_gen_mjj=byb)
    for X in (400, 450, 500):
        for dcut in (0.0, 3.5):
            sel = ok & (rec > X) & (de > dcut)
            o[f"P(parton_mjj<400 | reco_mjj>{X}, deta>{dcut})"] = float(((L < 400) & sel).sum()/max(sel.sum(), 1))
            o[f"N(reco_mjj>{X}, deta>{dcut})"] = int(sel.sum())
    OUT[s] = o; print(s, json.dumps(o))
json.dump(OUT, open(f"{P}/work/theory/mjj_resolution.json", "w"), indent=1)
