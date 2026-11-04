#!/usr/bin/env python3
"""tt-gamma / tt-gamma-gamma / tW-gamma overlap bound at RECO level after the b-veto (G1 item 4, D10). Uses the G2 test jobs (2000 events each; statistics are poor and are quoted).
For T_tta_1l / T_tWa_1l: events with n_prompt_photons>=2 (GenTruth) are the part REMOVED from the 1-photon sample; reco-SR-proxy (scripts/srsel.py, ng=2: 2 photons 100<m_gg<170, 1 lepton, MET>30,
b-veto, VBS jets) yield of that removed part = sigma*k*L * n_pass/N ; compared with the same SR-proxy yield of T_ttaa_1l (sigma*k*L*n_pass/N). L = 500 fb^-1. Output: work/ttg_overlap.json"""
import sys, os, glob, json, math, yaml, numpy as np, uproot
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from srsel import select
WH = "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh"; M = {r["id"]: r for r in yaml.safe_load(open(f"{WH}/config/sample_matrix.yaml"))["samples"]}
res = {}
def f(s): return sorted(x for x in glob.glob(f"{WH}/work/test/{s}/*.root") if not x.endswith(("_gen.root", "_full.root")))
for s in ("T_tta_1l", "T_tWa_1l", "T_ttaa_1l"):
    fs = f(s)
    if not fs: res[s] = "PENDING (no test job output)"; continue
    sel = select(fs[0], 2); npr = uproot.open(fs[0][:-5] + "_gen.root")["GenTruth"].arrays(["n_prompt_photons"], library="np")["n_prompt_photons"]; N = len(sel); sk = M[s]["sigma_fb"]*M[s]["k_external"]; L = 500.0
    ge2 = npr >= 2; k = int((sel & ge2).sum()); kall = int(sel.sum())
    res[s] = dict(N=N, sigma_k_fb=sk, frac_ge2_prompt_photons=float(ge2.mean()), n_SRproxy_all=kall, n_SRproxy_ge2prompt=k, yield_all_500=sk*L*kall/N, yield_ge2prompt_500=sk*L*k/N,
                  err_ge2prompt_500=(sk*L*math.sqrt(max(k, 1))/N), note="Poisson error; 0 events => UL 3 events: %.3g" % (sk*L*3/N))
json.dump(res, open(f"{WH}/work/ttg_overlap.json", "w"), indent=1); print(json.dumps(res, indent=1))
