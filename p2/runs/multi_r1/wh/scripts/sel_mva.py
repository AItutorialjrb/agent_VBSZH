#!/usr/bin/env python3
"""(v2: pT inputs of the photons are divided by m_gg (pt1m, pt2m, ptggm): the absolute pt1, pt2, ptgg, drgg rebuilt m_gg exactly and sculpted the background m_gg (review 05 item 1); weights: |w| for training (negative-weight fractions <= 1.4 %); folds = (evt + const) mod 5.)
K=5 k-fold BDT (xgboost) per the pre-declaration in reports/05_selection.md sec. 0. Inputs work/sel/table.npz; writes work/sel/mva.json and work/sel/mva_scores_seed<k>.npy.
Training: signal (def. a) vs all other classes, rows 100<mgg<180, mgg NOT an input; |w| weights, signal reweighted to the background total; train on 4 folds, predict the held-out fold (disjoint). Cut on the score + mgg half-width chosen with the same plateau rule (admissible: N_eff>=30, rel MC<=30 %, Z>=0.97 Zmax, loosest = largest s)."""
import json, numpy as np, xgboost as xgb
WH = "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh"
t = dict(np.load(f"{WH}/work/sel/table.npz")); meta = json.load(open(f"{WH}/work/sel/table_meta.json")); cid = meta["classes"]
VARS = ["mjj", "deta", "ptggm", "drgg", "ptl", "etal", "mt", "met", "pt1m", "pt2m", "ptj1", "ptj2", "etaj1", "etaj2", "zstar", "drlg", "dphijjgg", "njets", "ptj3"]
X = np.stack([t[v] for v in VARS], 1); y = (t["cls"] == cid["signal"]).astype(int); w = t["w"]; fold = t["fold"].astype(int); n = len(y)
def Z(s, b): return float(np.sqrt(2*((s+b)*np.log1p(s/b)-s))) if s > 0 and b > 0 else 0.0
def best(score, mask_rows, hws=(2.5, 3.5, 5.0), nq=40):
    """plateau rule on (score threshold, hw) over the given rows"""
    thr = np.unique(np.quantile(score[y == 0], np.linspace(0.5, 0.9995, nq))); out = []
    for hw in hws:
        win = mask_rows & (np.abs(t["mgg"]-125) < hw)
        for th in thr:
            m = win & (score > th); s = w[m & (y == 1)].sum(); mb = m & (y == 0); wb = w[mb]; b = wb.sum()
            if b <= 0 or s <= 0: continue
            ne = b**2/(wb**2).sum(); rel = np.sqrt((wb**2).sum())/b
            out.append(dict(s=float(s), b=float(b), Z=Z(s, b), neff=float(ne), relmc=float(rel), thr=float(th), hw=hw))
    adm = [r for r in out if r["neff"] >= 30 and r["relmc"] <= 0.3]; zm = max(r["Z"] for r in adm); pl = [r for r in adm if r["Z"] >= 0.97*zm]
    return max(pl, key=lambda r: (r["s"], r["neff"])), max(adm, key=lambda r: r["Z"])
res = dict(vars=VARS, seeds={}); allrows = np.ones(n, bool)
for seed in (11, 22, 33):
    score = np.zeros(n)
    for k in range(5):
        tr = fold != k; wt = np.abs(w[tr]).copy(); yt = y[tr]; wt[yt == 1] *= wt[yt == 0].sum()/wt[yt == 1].sum()
        mdl = xgb.XGBClassifier(n_estimators=250, max_depth=4, learning_rate=0.05, subsample=0.8, colsample_bytree=0.8, min_child_weight=1e-3, random_state=seed, n_jobs=4, tree_method="hist")
        mdl.fit(X[tr], yt, sample_weight=wt); mdl.get_booster().save_model(f"{WH}/work/sel/model_seed{seed}_fold{k}.json"); score[fold == k] = mdl.predict_proba(X[fold == k])[:, 1]
    ch, bs = best(score, allrows)
    # nested threshold: choose (thr, hw) on the 4 other folds' held-out rows, apply to the 5th; sum over folds
    ns = nb = 0.0; nw2 = 0.0
    for k in range(5):
        ck, _ = best(score, fold != k); mk = (fold == k) & (np.abs(t["mgg"]-125) < ck["hw"]) & (score > ck["thr"]); ns += w[mk & (y == 1)].sum(); wbk = w[mk & (y == 0)]; nb += wbk.sum(); nw2 += (wbk**2).sum()
    nested = dict(s=float(ns), b=float(nb), Z=Z(ns, nb), neff=float(nb**2/nw2)); sb = {}
    for lo_, hi_ in ((100, 110), (110, 120), (120, 130), (130, 150), (150, 180)):
        mm = (t["mgg"] > lo_) & (t["mgg"] < hi_) & (y == 0); sb[f"{lo_}-{hi_}"] = float(w[mm & (score > ch["thr"])].sum()/w[mm].sum())
    np.save(f"{WH}/work/sel/mva_scores_seed{seed}.npy", score)
    # fold-to-fold: same threshold/hw on each fold alone, yields scaled x5
    fz = []; fne = []; fsn = []
    for k in range(5):
        m = (fold == k) & (np.abs(t["mgg"]-125) < ch["hw"]) & (score > ch["thr"]); s = 5*w[m & (y == 1)].sum(); wb = w[m & (y == 0)]; b = 5*wb.sum(); fz.append(Z(s, b)); fsn.append(float(w[m & (y == 1)].sum()**2/(w[m & (y == 1)]**2).sum())); fne.append(float(wb.sum()**2/(wb**2).sum()) if len(wb) else 0.0)
    res["seeds"][seed] = dict(chosen=ch, nested=nested, bkg_eff_vs_mgg=sb, Zmax=bs, fold_Z_scaled=fz, fold_neff_bkg=fne, fold_neff_sig=fsn)
    print(seed, "nested", nested, "bkg eff vs mgg", sb, "chosen", ch, "fold Z", np.round(fz, 3), "fold neff", np.round(fne, 1), flush=True)
Zs = [r["chosen"]["Z"] for r in res["seeds"].values()]; res["Z_mva_mean"] = float(np.mean(Zs)); res["Z_mva_seed_spread_rel"] = float((max(Zs)-min(Zs))/np.mean(Zs))
json.dump(res, open(f"{WH}/work/sel/mva.json", "w"), indent=1, default=float); print("Z seeds", Zs, "mean", res["Z_mva_mean"], "spread", res["Z_mva_seed_spread_rel"])
