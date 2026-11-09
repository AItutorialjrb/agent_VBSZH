#!/usr/bin/env python3
"""v1.1 re-evaluation with the FROZEN cuts and FROZEN MVA models on work/sel/table_v11.npz; D45 retraining-trigger check (lost-lepton or non-prompt share of the selected b changes by > 30 % relative). Writes work/sel/selection_v11.json."""
import json, numpy as np, xgboost as xgb
WH = "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh"
def Z(s, b): return float(np.sqrt(2*((s+b)*np.log1p(s/b)-s))) if s > 0 and b > 0 else 0.0
res = {}; sel = json.load(open(f"{WH}/work/sel/selection_final.json")); cb = sel["cut_based"]["cuts"]
for tag in ("v1", "v11"):
    t = dict(np.load(f"{WH}/work/sel/{'table' if tag == 'v1' else 'table_v11'}.npz")); meta = json.load(open(f"{WH}/work/sel/{'table' if tag == 'v1' else 'table_v11'}_meta.json")); cid = meta["classes"]; y = t["cls"] == cid["signal"]; w = t["w"]
    m = (t["mjj"] > cb["mjj"]) & (t["deta"] > cb["deta"]) & (t["ptgg"] > cb["ptgg"]) & (t["met"] > cb["met"]) & (t["mt"] > cb["mt"]) & (t["ptl"] > cb["ptl"]) & (np.abs(t["mgg"]-125) < cb["hw"]) & (t["zstar"] < cb["zs"])
    s = w[m & y].sum(); wb = w[m & ~y]; b = wb.sum(); cl = {}
    for c, i in cid.items():
        x = w[m & (t["cls"] == i)]; cl[c] = dict(Y=float(x.sum()), stat=float(np.sqrt((x**2).sum())), nraw=int((m & (t["cls"] == i)).sum()), neff=float(x.sum()**2/(x**2).sum()) if len(x) else 0.0)
    out = dict(cut_based=dict(s=float(s), b=float(b), Z=Z(s, b), neff=float(b**2/(wb**2).sum()), relmc=float(np.sqrt((wb**2).sum())/b), classes=cl))
    # frozen MVA: mean of the 3 seeds x 5 fold models (v11 rows have no held-out predictions: all rows scored by the average model; v1 uses the same for like-for-like)
    VARS = json.load(open(f"{WH}/work/sel/mva.json"))["vars"]; X = np.stack([t[v] for v in VARS], 1); sc = np.zeros(len(y)); n = 0
    for seed in (11, 22, 33):
        for k in range(5):
            bo = xgb.Booster(); bo.load_model(f"{WH}/work/sel/model_seed{seed}_fold{k}.json"); sc += bo.predict(xgb.DMatrix(X, feature_names=None)); n += 1
    sc /= n; ch = sel["mva"]["choice"]; mm = (np.abs(t["mgg"]-125) < ch["hw"]) & (sc > ch["thr"]); sm = w[mm & y].sum(); wbm = w[mm & ~y]; bm = wbm.sum()
    out["mva_frozen_avgmodel"] = dict(s=float(sm), b=float(bm), Z=Z(sm, bm), neff=float(bm**2/(wbm**2).sum()), thr=ch["thr"], hw=ch["hw"], note="in-sample for the training rows (average of all fold models), so only the v11/v1 ratio is meaningful")
    res[tag] = out
b1 = res["v1"]["cut_based"]; b2 = res["v11"]["cut_based"]; sh = lambda r, c: r["classes"][c]["Y"]/r["b"]
res["D45"] = {c: dict(share_v1=sh(b1, c), share_v11=sh(b2, c), rel_change=(sh(b2, c)/sh(b1, c)-1) if sh(b1, c) > 0 else None) for c in ("lost_lepton_egamma", "nonprompt_lepton")}
res["D45_trigger_fired"] = any(abs(v["rel_change"]) > 0.30 for v in res["D45"].values() if v["rel_change"] is not None)
json.dump(res, open(f"{WH}/work/sel/selection_v11.json", "w"), indent=1, default=float); print(json.dumps({k: (v if k.startswith("D45") else dict(cut=(v["cut_based"]["s"], v["cut_based"]["b"], v["cut_based"]["Z"], v["cut_based"]["neff"]), mva=(v["mva_frozen_avgmodel"]["s"], v["mva_frozen_avgmodel"]["b"], v["mva_frozen_avgmodel"]["Z"]))) for k, v in res.items()}))
