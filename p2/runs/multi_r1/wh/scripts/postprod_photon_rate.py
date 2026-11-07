#!/usr/bin/env python3
"""Per-event rate of non-prompt-origin ('fake') reco photons (data for FORMAT.md; the jet-associated rate of sec. 6a captures only ~7 % of them): in events with n_prompt_photons == 0 of the W+4j (F_Wjjjj, every 6th file) and ttbar+jj (T_ttjj_1l, all files) production files,
the number of reco Photons (pT > 25 GeV, |eta| < 2.5, no crack) with NO prompt gen photon within dR < 0.1 and NO prompt gen lepton (pT > 10) within dR < 0.2, per event and per photon-pT bin, barrel/endcap, plus the fraction of those photons within dR < 0.4 of a GenJet (pT > 15).
Usage: bash scripts/envrun.sh python3 -P scripts/postprod_photon_rate.py"""
import json, glob, numpy as np, uproot, awkward as ak
from multiprocessing import Pool
PR = "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/production/wh"; PT = [25, 35, 50, 75, 100, 1000]
SP = [("F_Wjjjj", "W", 6), ("T_ttjj_1l", "TT", 1)]
def dphi(a, b): return (a-b+np.pi) % (2*np.pi)-np.pi
def work(a):
    f, cls = a; T = uproot.open(f)["Delphes"]; G = uproot.open(f[:-5] + "_gen.root")["GenTruth"]
    x = T.arrays(["Photon.PT", "Photon.Eta", "Photon.Phi", "GenJet.PT", "GenJet.Eta", "GenJet.Phi"], library="np"); g = G.arrays(["n_prompt_photons", "gph_eta", "gph_phi", "gph_prompt", "glep_pt", "glep_eta", "glep_phi", "glep_prompt"], library="ak")
    npr = ak.to_numpy(g["n_prompt_photons"]); L = [ak.to_list(g[k]) for k in ("gph_eta", "gph_phi", "gph_prompt", "glep_eta", "glep_phi", "glep_pt", "glep_prompt")]
    n = np.zeros((2, len(PT)-1)); injet = np.zeros((2, len(PT)-1)); N = 0
    for i in range(len(npr)):
        if npr[i] != 0: continue
        N += 1; gp = [(e, p) for e, p, r in zip(L[0][i], L[1][i], L[2][i]) if r]; pl = [(e, p) for e, p, q, r in zip(L[3][i], L[4][i], L[5][i], L[6][i]) if r and q > 10]
        for q, e, p in zip(x["Photon.PT"][i], x["Photon.Eta"][i], x["Photon.Phi"][i]):
            if q <= 25 or abs(e) >= 2.5 or 1.4442 < abs(e) < 1.566: continue
            if any(np.hypot(e-ge, dphi(p, gf)) < 0.1 for ge, gf in gp) or any(np.hypot(e-le, dphi(p, lp)) < 0.2 for le, lp in pl): continue
            ie = 0 if abs(e) < 1.5 else 1; ip = int(np.digitize(q, PT)-1); n[ie, ip] += 1
            if any(np.hypot(e-e2, dphi(p, p2)) < 0.4 for q2, e2, p2 in zip(x["GenJet.PT"][i], x["GenJet.Eta"][i], x["GenJet.Phi"][i]) if q2 > 15): injet[ie, ip] += 1
    return cls, N, n, injet
if __name__ == "__main__":
    fs = [(f, c) for s, c, k in SP for f in sorted(x for x in glob.glob(f"{PR}/{s}/*.root") if not x.endswith("_gen.root"))[::k]]
    with Pool(8) as p: R = p.map(work, fs, chunksize=2)
    out = {}
    for c in ("W", "TT"):
        N = sum(r[1] for r in R if r[0] == c); n = sum(r[2] for r in R if r[0] == c); j = sum(r[3] for r in R if r[0] == c)
        out[c] = dict(n_events=int(N), count=n.tolist(), per_event=(n/N).tolist(), err=(np.sqrt(np.maximum(n, 1))/N).tolist(), frac_within_dR0p4_of_genjet=(j.sum()/max(n.sum(), 1)))
    out["pt_edges"] = PT; json.dump(out, open("/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh/work/postprod/photon_rate_per_event.json", "w"), indent=1)
    for c in ("W", "TT"): print(c, out[c]["n_events"], "total/event", np.array(out[c]["per_event"]).sum(), "in-jet frac", out[c]["frac_within_dR0p4_of_genjet"])
