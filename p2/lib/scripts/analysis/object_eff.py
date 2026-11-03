#!/usr/bin/env python3
"""A7 (2026-11-03): Delphes (stock CMS card, slim_v1) reconstruction x isolation efficiency of prompt leptons and photons,
measured on the Tier-1 EW ZHjj sample (prompt Z leptons, prompt H photons), for the CMS-like efficiency reweighting.
eff(type, |eta| bin, pT bin) = N(gen prompt object matched within dR<0.1 to a Delphes object of the same type) / N(gen prompt object)
Gen: GenTruth friend tree (glep_*, gph_* with *_prompt == 1); reco: Delphes Electron / Muon / Photon output collections
(after the card's efficiency + isolation modules). Photons in the EB-EE crack are excluded (acceptance, not efficiency).
Output: work/theory/object_eff.json. Usage: python3 -P object_eff.py [nfiles=20]"""
import sys, glob, json, numpy as np, uproot, awkward as ak
P = "/eos/user/r/rjiang/vbs_zh_codex_starter"; NF = int(sys.argv[1]) if len(sys.argv) > 1 else 20
ETA = {"e": [0, 1.5, 2.5], "m": [0, 1.5, 2.4], "g": [0, 1.4442, 2.5]}
PT = {"e": [10, 20, 30, 50, 1e9], "m": [10, 20, 30, 50, 1e9], "g": [20, 30, 40, 60, 1e9]}
num = {k: np.zeros((len(ETA[k]) - 1, len(PT[k]) - 1)) for k in "emg"}; den = {k: np.zeros_like(v) for k, v in num.items()}
def dR(e1, p1, e2, p2): return np.hypot(e1 - e2, (p1 - p2 + np.pi) % (2*np.pi) - np.pi)
fs = [f for f in sorted(glob.glob(f"{P}/production/v1/ew_zhjj_zll/*.root")) if "_gen" not in f][:NF]
for f in fs:
    G = uproot.open(f.replace(".root", "_gen.root"))["GenTruth"].arrays(library="ak")
    R = uproot.open(f)["Delphes"].arrays(["Electron.PT", "Electron.Eta", "Electron.Phi", "Muon.PT", "Muon.Eta", "Muon.Phi", "Photon.PT", "Photon.Eta", "Photon.Phi"], library="ak")
    if len(G) != len(R): print("skip", f); continue
    for i in range(len(G)):
        for k, gpt, geta, gphi, gsel, coll in (
                ("e", G.glep_pt[i], G.glep_eta[i], G.glep_phi[i], (abs(G.glep_pid[i]) == 11) & (G.glep_prompt[i] == 1), "Electron"),
                ("m", G.glep_pt[i], G.glep_eta[i], G.glep_phi[i], (abs(G.glep_pid[i]) == 13) & (G.glep_prompt[i] == 1), "Muon"),
                ("g", G.gph_pt[i], G.gph_eta[i], G.gph_phi[i], G.gph_prompt[i] == 1, "Photon")):
            gpt, geta, gphi = (ak.to_numpy(x[gsel]) for x in (gpt, geta, gphi))
            if not len(gpt): continue
            rpt, reta, rphi = (ak.to_numpy(R[f"{coll}.{v}"][i]) for v in ("PT", "Eta", "Phi"))
            for pt, eta, phi in zip(gpt, geta, gphi):
                ae = abs(eta)
                if k == "g" and 1.4442 < ae < 1.566: continue
                ie = np.searchsorted(ETA[k], ae) - 1; ip = np.searchsorted(PT[k], pt) - 1
                if ie < 0 or ie >= len(ETA[k]) - 1 or ip < 0 or ip >= len(PT[k]) - 1: continue
                den[k][ie, ip] += 1
                if len(rpt) and dR(eta, phi, reta, rphi).min() < 0.1: num[k][ie, ip] += 1
OUT = {k: dict(eta_edges=ETA[k], pt_edges=PT[k], eff=(num[k]/np.maximum(den[k], 1)).tolist(), n=den[k].tolist(),
               err=(np.sqrt(num[k]/np.maximum(den[k], 1)*(1 - num[k]/np.maximum(den[k], 1))/np.maximum(den[k], 1))).tolist()) for k in "emg"}
OUT["files"] = len(fs); json.dump(OUT, open(f"{P}/work/theory/object_eff.json", "w"), indent=1)
for k in "emg": print(k, np.round(num[k]/np.maximum(den[k], 1), 3).tolist(), den[k].astype(int).tolist())
