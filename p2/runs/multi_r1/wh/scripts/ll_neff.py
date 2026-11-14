#!/usr/bin/env python3
"""Per-sample N_eff / raw rows of the lost-lepton class at the frozen cut-based selection, v1.1 vs v1.2 tables; one-event Poisson interval of the QCD loose part. Writes work/v12_lostlep_neff.json"""
import json, numpy as np
from scipy.stats import chi2
WH = "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh"; cb = json.load(open(f"{WH}/work/sel/selection_final.json"))["cut_based"]["cuts"]; out = {}
for tag, f in (("v1.1", "table_v11"), ("v1.2", "table_v12")):
    t = dict(np.load(f"{WH}/work/sel/{f}.npz")); meta = json.load(open(f"{WH}/work/sel/{f}_meta.json")); cid = meta["classes"]; 
    m = (t["mjj"] > cb["mjj"]) & (t["deta"] > cb["deta"]) & (t["ptgg"] > cb["ptgg"]) & (t["met"] > cb["met"]) & (t["mt"] > cb["mt"]) & (t["ptl"] > cb["ptl"]) & (np.abs(t["mgg"]-125) < cb["hw"]) & (t["zstar"] < cb["zs"])
    ll = m & (t["cls"] == cid["lost_lepton_egamma"]); w2c = float((t["w"][ll]**2).sum()); w = t["w"][ll]; d = {}
    for i, s in enumerate(meta["samples"]):
        k = ll & (t["sid"] == i)
        if k.any(): x = t["w"][k]; d[s] = dict(Y=float(x.sum()), raw=int(k.sum()), neff=float(x.sum()**2/(x**2).sum()), share_class_sumw2=float((x**2).sum()/w2c), mean_row_weight=float(np.abs(x).mean()))
    d["_class"] = dict(Y=float(w.sum()), raw=int(ll.sum()), neff=float(w.sum()**2/w2c))
    out[tag] = d
q = out["v1.2"].get("F_QCD_llajj_loose")
if q:
    n = q["raw"]; wt = q["mean_row_weight"]; lo68, hi68 = chi2.ppf(0.1587, 2*n)/2, chi2.ppf(1-0.1587, 2*(n+1))/2; lo95, hi95 = chi2.ppf(0.025, 2*n)/2, chi2.ppf(0.975, 2*(n+1))/2
    out["QCD_part_poisson"] = dict(n_raw=n, row_weight_events=wt, Y=q["Y"], interval68=[lo68*wt, hi68*wt], interval95=[lo95*wt, hi95*wt], note="central Garwood intervals for the observed count n, scaled by the per-row weight (which includes the tau factor 1+r_tau = 1.083)")
json.dump(out, open(f"{WH}/work/v12_lostlep_neff.json", "w"), indent=1); print(json.dumps({k: v for k, v in out.items() if k in ("QCD_part_poisson",)}), {t: {s: (round(v["Y"], 4), v["raw"], round(v["neff"], 1)) for s, v in d.items()} for t, d in out.items() if t.startswith("v1.")})
