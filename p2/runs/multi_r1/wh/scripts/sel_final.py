#!/usr/bin/env python3
"""Freeze the selections and write cutflows: reads work/sel/{table.npz,scan.json,mva_scores_seed*.npy}; writes work/sel/selection_final.json and work/sel/selection_tables.md.
MVA used = ensemble mean of the 3 seeds' held-out scores; cut + hw chosen with the plateau rule (sel_mva.best)."""
import json, numpy as np, sys
sys.argv = [sys.argv[0]]
WH = "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh"
t = dict(np.load(f"{WH}/work/sel/table.npz")); meta = json.load(open(f"{WH}/work/sel/table_meta.json")); cid = meta["classes"]; scan = json.load(open(f"{WH}/work/sel/scan.json")); mva = json.load(open(f"{WH}/work/sel/mva.json"))
y = (t["cls"] == cid["signal"]).astype(int); w = t["w"]; n = len(y); fold = t["fold"].astype(int)
def Z(s, b): return float(np.sqrt(2*((s+b)*np.log1p(s/b)-s))) if s > 0 and b > 0 else 0.0
score = np.mean([np.load(f"{WH}/work/sel/mva_scores_seed{s}.npy") for s in (11, 22, 33)], 0)
thr = np.unique(np.quantile(score[y == 0], np.linspace(0.5, 0.9995, 40))); out = []
for hw in (2.5, 3.5, 5.0):
    for th in thr:
        m = (np.abs(t["mgg"]-125) < hw) & (score > th); s = w[m & (y == 1)].sum(); wb = w[m & (y == 0)]; b = wb.sum()
        if s > 0 and b > 0: out.append(dict(s=float(s), b=float(b), Z=Z(s, b), neff=float(b**2/(wb**2).sum()), relmc=float(np.sqrt((wb**2).sum())/b), thr=float(th), hw=hw))
adm = [r for r in out if r["neff"] >= 30 and r["relmc"] <= 0.3]; zm = max(r["Z"] for r in adm); mv = max([r for r in adm if r["Z"] >= 0.97*zm], key=lambda r: (r["s"], r["neff"]))
cb = scan["chosen"]["cuts"]
mask_cb = (t["mjj"] > cb["mjj"]) & (t["deta"] > cb["deta"]) & (t["ptgg"] > cb["ptgg"]) & (t["met"] > cb["met"]) & (t["mt"] > cb["mt"]) & (t["ptl"] > cb["ptl"]) & (np.abs(t["mgg"]-125) < cb["hw"]) & (t["zstar"] < cb["zs"])
mask_mv = (np.abs(t["mgg"]-125) < mv["hw"]) & (score > mv["thr"])
# fold stability (ensemble)
fz = []; fn = []
for k in range(5):
    m = (fold == k) & mask_mv; s = 5*w[m & (y == 1)].sum(); wb = w[m & (y == 0)]; fz.append(Z(s, 5*wb.sum())); fn.append(float(wb.sum()**2/(wb**2).sum()))
fzc = []; fnc = []
for k in range(5):
    m = (fold == k) & mask_cb; s = 5*w[m & (y == 1)].sum(); wb = w[m & (y == 0)]; fzc.append(Z(s, 5*wb.sum())); fnc.append(float(wb.sum()**2/(wb**2).sum()))
# nested threshold choice on the ensemble score (threshold/hw chosen on 4 folds, applied to the 5th)
def bestrows(rows):
    o = []
    for hw in (2.5, 3.5, 5.0):
        for th in thr:
            m = rows & (np.abs(t["mgg"]-125) < hw) & (score > th); s_ = w[m & (y == 1)].sum(); wb = w[m & (y == 0)]; b_ = wb.sum()
            if s_ > 0 and b_ > 0: o.append(dict(s=float(s_), b=float(b_), Z=Z(s_, b_), neff=float(b_**2/(wb**2).sum()), relmc=float(np.sqrt((wb**2).sum())/b_), thr=float(th), hw=hw))
    a = [r for r in o if r["neff"] >= 30 and r["relmc"] <= 0.3]; zz = max(r["Z"] for r in a); return max([r for r in a if r["Z"] >= 0.97*zz], key=lambda r: (r["s"], r["neff"]))
ns = nb = nw2 = 0.0
for k in range(5):
    ck = bestrows(fold != k); mk = (fold == k) & (np.abs(t["mgg"]-125) < ck["hw"]) & (score > ck["thr"]); ns += w[mk & (y == 1)].sum(); wbk = w[mk & (y == 0)]; nb += wbk.sum(); nw2 += (wbk**2).sum()
nested = dict(s=float(ns), b=float(nb), Z=Z(ns, nb), neff=float(nb**2/nw2))
flat = {}
for lo_, hi_ in ((100, 110), (110, 120), (120, 130), (130, 150), (150, 180)):
    mm = (t["mgg"] > lo_) & (t["mgg"] < hi_) & (y == 0); flat[f"{lo_}-{hi_}"] = float(w[mm & (score > mv["thr"])].sum()/w[mm].sum())
names = {v: k for k, v in cid.items()}
def table(mask):
    rows = {}
    for c, i in cid.items():
        m = mask & (t["cls"] == i); x = w[m]; rows[c] = dict(Y=float(x.sum()), stat=float(np.sqrt((x**2).sum())), nraw=int(m.sum()), neff=float(x.sum()**2/(x**2).sum()) if m.any() else 0.0)
    return rows
res = dict(mva_nested=nested, mva_bkg_eff_vs_mgg=flat, cut_based=dict(cuts=cb, **{k: scan["chosen"][k] for k in ("s", "b", "Z", "neff", "relmc")}, classes=table(mask_cb), fold_Z_scaled=fzc, fold_neff=fnc, fold_Z_rms_rel=float(np.std(fzc)/np.mean(fzc)), fold_Z_range_rel=float((max(fzc)-min(fzc))/np.mean(fzc))),
           mva=dict(choice=mv, classes=table(mask_mv), fold_Z_scaled=fz, fold_neff=fn, fold_Z_rms_rel=float(np.std(fz)/np.mean(fz)), fold_Z_range_rel=float((max(fz)-min(fz))/np.mean(fz)), seed_Z=[mva["seeds"][s]["chosen"]["Z"] for s in mva["seeds"]], seed_spread_rel=mva["Z_mva_seed_spread_rel"]),
           Zmax_cut=scan["Zmax"], gain_mva_over_cut=mv["Z"]/scan["chosen"]["Z"]-1)
# cut-based cutflow (sequential), signal and total bkg
steps = [("VBS block region (baseline, 100<mgg<180)", np.ones(n, bool)), (f"mjj>{cb['mjj']}", t["mjj"] > cb["mjj"]), (f"|deta|>{cb['deta']}", t["deta"] > cb["deta"]), (f"pT(gg)>{cb['ptgg']}", t["ptgg"] > cb["ptgg"]), (f"MET>{cb['met']}", t["met"] > cb["met"]), (f"mT>{cb['mt']}", t["mt"] > cb["mt"]), (f"pT(l)>{cb['ptl']}", t["ptl"] > cb["ptl"]),
         (f"z*<{cb['zs']}", t["zstar"] < cb["zs"]), (f"|mgg-125|<{cb['hw']}", np.abs(t["mgg"]-125) < cb["hw"])]
cur = np.ones(n, bool); cf = []
for nm, m in steps:
    cur &= m; cf.append(dict(step=nm, s=float(w[cur & (y == 1)].sum()), b=float(w[cur & (y == 0)].sum()), nraw_s=int((cur & (y == 1)).sum()), nraw_b=int((cur & (y == 0)).sum())))
res["cutflow_cut_based"] = cf
json.dump(res, open(f"{WH}/work/sel/selection_final.json", "w"), indent=1, default=float)
L = ["| class | cut-based Y | stat | raw N | N_eff | MVA Y | stat | raw N | N_eff |", "|---|---|---|---|---|---|---|---|---|"]
for c in cid: a, b = res["cut_based"]["classes"][c], res["mva"]["classes"][c]; L.append(f"| {c} | {a['Y']:.4g} | {a['stat']:.2g} | {a['nraw']} | {a['neff']:.0f} | {b['Y']:.4g} | {b['stat']:.2g} | {b['nraw']} | {b['neff']:.0f} |")
L += ["", "| cutflow step | s | b | raw s | raw b |", "|---|---|---|---|---|"] + [f"| {r['step']} | {r['s']:.4g} | {r['b']:.4g} | {r['nraw_s']} | {r['nraw_b']} |" for r in cf]
open(f"{WH}/work/sel/selection_tables.md", "w").write("\n".join(L)); print("\n".join(L)); print(json.dumps({k: res[k] for k in ("gain_mva_over_cut",)})); print("MVA", mv); print("NESTED", nested, "flat", flat); print("fold Z mva", fz, "rms", res["mva"]["fold_Z_rms_rel"], "range", res["mva"]["fold_Z_range_rel"]); print("fold Z cut", fzc, res["cut_based"]["fold_Z_rms_rel"])
