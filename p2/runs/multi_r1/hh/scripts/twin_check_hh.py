#!/usr/bin/env python3
"""Generator-filter twin check at Delphes level (SPEC 4.3(1), D-HH-6; review item 8).
For a nominal sample N (tight generator filter) and its twin T (looser filter), compare the weighted rate of reco boosted-tail stages, sigma*k/N_gen each:
  two  : >= 2 fat jets pT>=300, |eta|<2.4 ;  lead : + leading >= 450 ;  vbs : + VBS AK5 pair (mjj>500,|d eta|>3.5)  [= 'reco SR before the mass window'] ;  win : + both m_SD in [90,150] (raw)
  tagw : sum of truth-tag weights (nominal scenario) at stage vbs, x sigma/N_gen.
loss = 1 - rate_N/rate_T  (positive = the nominal generator filter removed events that the looser twin keeps), error from Poisson counts of both samples (ratio error propagation).
twin_ok := the loss at stage `vbs` is not significantly above 5 % : loss - 1.645*err <= 0.05 (one-sided 95 %) AND |loss| < 0.25 ; 'stat_limited' flag if err > 0.1.
Usage: twin_check_hh.py <matrix.yaml> <scenarios.yaml> <out.json> <prod_root> nominal:twin [nominal:twin ...]   (prod_root/<sample>/ holds the complete job files)"""
import sys, json, yaml, numpy as np, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hh_reco as R
my, sy, outj, root = sys.argv[1:5]; pairs = [p.split(":") for p in sys.argv[5:]]
M = {s["name"]: s for s in yaml.safe_load(open(my))["samples"]}; SC = yaml.safe_load(open(sy))["tagging"]["nominal"]
def rates(name, d):
    s = M[name]; sig = s["sigma_x_BR_fb"]; two, lead, vbs = R.stages(d); win = vbs & R.window(d); w = R.tag_weight(d, SC)
    ng = d["n_gen"]; out = {}
    for k, m in (("two", two), ("lead", lead), ("vbs", vbs), ("win", win)): out[k] = dict(k=int(m.sum()), rate_fb=sig * m.sum() / ng)
    out["tagw"] = dict(k=int(vbs.sum()), rate_fb=sig * float((w * vbs).sum()) / ng, sumw2=float((w * w * vbs).sum()) * (sig / ng) ** 2)
    return out
res = {}
for a, b in pairs:
    da, db = (R.load_named(x, root) for x in (a, b)); ra, rb = rates(a, da), rates(b, db); r = dict(nominal=a, twin=b, N_nominal=da["n_gen"], N_twin=db["n_gen"], stages={})
    for st in ("two", "lead", "vbs", "win", "tagw"):
        ka, kb = ra[st]["k"], rb[st]["k"]; fa, fb = ra[st]["rate_fb"], rb[st]["rate_fb"]
        if kb == 0 or fb <= 0: r["stages"][st] = dict(k_nominal=ka, k_twin=kb, loss=None, err=None, note="twin has zero raw events at this stage"); continue
        ratio = fa / fb; rel = np.hypot(1 / np.sqrt(max(ka, 1)), 1 / np.sqrt(kb)); loss = 1 - ratio; err = ratio * rel if ka > 0 else 1.0 / np.sqrt(kb)
        if ka == 0: err = max(err, 1.0)
        r["stages"][st] = dict(k_nominal=ka, k_twin=kb, rate_nominal_fb=fa, rate_twin_fb=fb, loss=float(loss), err=float(err), loss_UL95=float(loss + 1.645 * err))
    s = r["stages"]["vbs"]
    r["twin_ok"] = bool(s["loss"] is not None and (s["loss"] - 1.645 * s["err"] <= 0.05) and abs(s["loss"]) < 0.25)
    tg = r["stages"]["tagw"]
    r["twin_ok_tagw"] = bool(tg["loss"] is not None and (tg["loss"] - 1.645 * tg["err"] <= 0.05) and abs(tg["loss"]) < 0.25)   # same 5 % test on the tag-weighted VBS stage (SR yields are tag-weighted; G2 review item 5)
    r["stat_limited"] = bool(s["err"] is None or s["err"] > 0.10)
    res[a] = r
json.dump(res, open(outj, "w"), indent=1, default=float)
print("| nominal (N) | twin (N) | stage | k_nom | k_twin | loss ± stat | loss UL95 | twin_ok / stat-limited |\n|---|---|---|---|---|---|---|---|")
for a, r in res.items():
    for st, v in r["stages"].items():
        if v["loss"] is None: print(f"| {a} ({r['N_nominal']}) | {r['twin']} ({r['N_twin']}) | {st} | {v['k_nominal']} | {v['k_twin']} | n/a | n/a | |"); continue
        print(f"| {a} ({r['N_nominal']}) | {r['twin']} ({r['N_twin']}) | {st} | {v['k_nominal']} | {v['k_twin']} | {v['loss']*100:+.1f} ± {v['err']*100:.1f} % | {v['loss_UL95']*100:+.1f} % | " + (f"{r['twin_ok']} / {r['stat_limited']}" if st == "vbs" else "") + " |")
