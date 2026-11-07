#!/usr/bin/env python3
"""Per-event probability of a lepton-free non-prompt-origin reco photon (pT > 25, |eta| < 2.5, no crack; no prompt gen photon within dR 0.1, no prompt gen lepton within 0.2) vs the number of matrix-element jets of the sample, split into 'within dR < 0.4 of a GenJet (pT > 15)' (in-jet) and 'not in a jet':
W + 2j + prompt photon (F_QCD_Wajj_nomjj twin + test, n_prompt = 1), W + 3j + prompt photon (F_QCD_Wajjj_nomjj, every 4th file, n_prompt = 1), W + 4j (F_Wjjjj, every 6th file, n_prompt = 0). Usage: bash scripts/envrun.sh python3 -P scripts/diag_photon_vs_njets.py"""
import json, glob, numpy as np, uproot, awkward as ak
from multiprocessing import Pool
WH = "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh"; PR = "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/production/wh"
def dphi(a, b): return (a-b+np.pi) % (2*np.pi)-np.pi
def work(a):
    f, npw = a; T = uproot.open(f)["Delphes"]; G = uproot.open(f[:-5] + "_gen.root")["GenTruth"]
    x = T.arrays(["Photon.PT", "Photon.Eta", "Photon.Phi", "GenJet.PT", "GenJet.Eta", "GenJet.Phi"], library="np"); g = G.arrays(["n_prompt_photons", "gph_eta", "gph_phi", "gph_prompt", "glep_pt", "glep_eta", "glep_phi", "glep_prompt"], library="ak")
    npr = ak.to_numpy(g["n_prompt_photons"]); L = [ak.to_list(g[k]) for k in ("gph_eta", "gph_phi", "gph_prompt", "glep_eta", "glep_phi", "glep_pt", "glep_prompt")]; N = 0; nj = 0; nn = 0
    for i in range(len(npr)):
        if npr[i] != npw: continue
        N += 1; gp = [(e, p) for e, p, r in zip(L[0][i], L[1][i], L[2][i]) if r]; pl = [(e, p) for e, p, q, r in zip(L[3][i], L[4][i], L[5][i], L[6][i]) if r and q > 10]
        for q, e, p in zip(x["Photon.PT"][i], x["Photon.Eta"][i], x["Photon.Phi"][i]):
            if q <= 25 or abs(e) >= 2.5 or 1.4442 < abs(e) < 1.566: continue
            if any(np.hypot(e-ge, dphi(p, gf)) < 0.1 for ge, gf in gp) or any(np.hypot(e-le, dphi(p, lp)) < 0.2 for le, lp in pl): continue
            if any(np.hypot(e-e2, dphi(p, p2)) < 0.4 for q2, e2, p2 in zip(x["GenJet.PT"][i], x["GenJet.Eta"][i], x["GenJet.Phi"][i]) if q2 > 15): nj += 1
            else: nn += 1
    return N, nj, nn
if __name__ == "__main__":
    S = {"W+2j+gamma (F_QCD_Wajj_nomjj twin+test)": ([f for f in sorted(glob.glob(f"{WH}/work/twin/F_QCD_Wajj_nomjj/*.root")) if not f.endswith(("_gen.root", "_full.root"))] + [f"{WH}/work/test/F_QCD_Wajj_nomjj/F_QCD_Wajj_nomjj_s2128001.root"], 1),
         "W+3j+gamma (F_QCD_Wajjj_nomjj)": ([f for f in sorted(glob.glob(f"{PR}/F_QCD_Wajjj_nomjj/*.root")) if not f.endswith("_gen.root")][::4], 1),
         "W+4j (F_Wjjjj)": ([f for f in sorted(glob.glob(f"{PR}/F_Wjjjj/*.root")) if not f.endswith("_gen.root")][::6], 0)}
    out = {}
    with Pool(8) as p:
        for k, (fs, npw) in S.items():
            R = p.map(work, [(f, npw) for f in fs]); N = sum(r[0] for r in R); nj = sum(r[1] for r in R); nn = sum(r[2] for r in R)
            out[k] = dict(n_events=N, in_jet=nj, not_in_jet=nn, per_event_in_jet=nj/N, per_event_not_in_jet=nn/N, err_in_jet=max(nj, 1)**0.5/N, err_not_in_jet=max(nn, 1)**0.5/N); print(k, out[k], flush=True)
    json.dump(out, open(f"{WH}/work/postprod/photon_vs_njets.json", "w"), indent=1)
