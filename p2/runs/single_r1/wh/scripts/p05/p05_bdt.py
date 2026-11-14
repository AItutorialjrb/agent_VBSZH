#!/usr/bin/env python3
"""single_r1 WH Phase 05b: gradient-boosted BDT (xgboost) with 5-fold cross-validation, trained on expected (MC-weighted)
signal vs total background after a loose preselection; m_gg is NOT an input (it stays the fit / window variable).
Every row is scored by the model that did not see its fold (fold = event-number hash, pseudo-event rows of one event share
a fold); samples not used in training (coupling points, cross-checks) get the mean of the five models.
Adoption rule (declared in the task, A2): adopted only if Z_syst(500/fb, def. a) gains > 10 % over the cut-based optimum AND
the gain is stable: positive in every fold (fold-wise s, b scaled x5) and the train/test AUC difference < 0.02.
Output: wh/work/p05/bdt.json, wh/work/p05/bdt_scores/<sample>__<table>.npz.  Usage: python3 -P p05_bdt.py"""
import sys, os, json, zlib, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import whana as A
import xgboost as xgb
from sklearn.metrics import roc_auc_score
OUT = f"{A.WH}/work/p05"; os.makedirs(f"{OUT}/bdt_scores", exist_ok=True)
P5 = json.load(open(f"{OUT}/p05.json"))
OPT = {k: (tuple(v) if isinstance(v, list) else v) for k, v in P5["OPT"].items()}
PRE = dict(OPT, mjj=min(300., OPT["mjj"]), deta=min(2.0, OPT["deta"]), zgg=99., mtw=0., ptgg=0., met=min(20., OPT["met"]),
           ratio=(1/3, 1/4), j2pt=30., j1pt=30.)
FEAT = ["mjj", "detajj", "dphijj", "j1pt", "j2pt", "j1eta", "j2eta", "j3pt", "zgg", "zl", "ptgg_m", "g1pt_m", "g2pt_m", "g1eta", "g2eta",
        "met", "mtw", "l1pt", "l1eta", "drgg", "drlg", "drgj", "ptbal", "ht", "nj30", "ygg"]
def feats(T):
    X = []
    for f in FEAT:
        if f == "ptgg_m": v = T["ptgg"]/T["mgg"]
        elif f == "g1pt_m": v = T["g1pt"]/T["mgg"]
        elif f == "g2pt_m": v = T["g2pt"]/T["mgg"]
        elif f in ("j1eta", "j2eta", "g1eta", "g2eta", "l1eta"): v = np.abs(T[f])
        else: v = T[f]
        X.append(np.nan_to_num(np.asarray(v, float), nan=-1.0))
    return np.stack(X, -1)
S = A.Store()
S.ceg = {k: tuple(v) for k, v in P5["eg_closure_factor"].items()}   # e->gamma closure factors from p05
TRAIN = [k for k, r in A.R.items() if k in S.T and r["role"] in ("sig", "bkg", "qcdwh")]
rows = []   # (key, table, mask_pre, X, w, y, fold)
for k in S.T:
    for t in ("D", "F1", "F2", "FL", "EG"):
        T, w, use = S.rows(k, t, A.SC0)
        if T is None: continue
        m = A.sel(T, PRE, window=False) & use
        if A.R[k]["cls"] == "FL" and t == "D": m &= T["cat"] != "NPL"     # direct NPL handled by the max rule (kept out of training)
        fold = ((T["evt"].astype(np.int64) + zlib.crc32(k.encode())) % 5).astype(int)
        rows.append(dict(k=k, t=t, m=m, X=feats({f: T[f][m] for f in T if f not in ("cat",) and len(T[f]) == len(m)}) if m.any() else np.zeros((0, len(FEAT))),
                         w=w[m], y=int(A.R[k]["role"] == "sig"), fold=fold[m], train=k in TRAIN))
X = np.concatenate([r["X"] for r in rows if r["train"]]); W = np.concatenate([r["w"] for r in rows if r["train"]])
Y = np.concatenate([np.full(len(r["w"]), r["y"]) for r in rows if r["train"]]); F = np.concatenate([r["fold"] for r in rows if r["train"]])
WT = np.abs(W).copy(); WT[Y == 1] /= WT[Y == 1].sum(); WT[Y == 0] /= WT[Y == 0].sum(); WT *= len(WT)/2
print("training rows", len(Y), "signal", int(Y.sum()), "bkg", int((1 - Y).sum()))
MODELS, AUC = [], []
for f in range(5):
    tr, te = F != f, F == f
    mdl = xgb.XGBClassifier(n_estimators=400, max_depth=3, learning_rate=0.05, subsample=0.8, colsample_bytree=0.8, min_child_weight=1.0,
                            reg_lambda=1.0, tree_method="hist", n_jobs=4, random_state=2400000 + f)
    mdl.fit(X[tr], Y[tr], sample_weight=WT[tr])
    ptr, pte = mdl.predict_proba(X[tr])[:, 1], mdl.predict_proba(X[te])[:, 1]
    AUC.append(dict(fold=f, auc_train=float(roc_auc_score(Y[tr], ptr, sample_weight=WT[tr])), auc_test=float(roc_auc_score(Y[te], pte, sample_weight=WT[te]))))
    MODELS.append(mdl); print(AUC[-1])
    os.makedirs(f"{OUT}/bdt_models", exist_ok=True); mdl.get_booster().save_model(f"{OUT}/bdt_models/fold{f}.json")
# score every row of every table (full length; rows outside PRE get -1)
for r in rows:
    T = S.T[r["k"]][r["t"]]; sc = np.full(len(T["w"]), -1.0, np.float32)
    if len(r["w"]):
        if r["train"]:
            p = np.zeros(len(r["w"]))
            for f in range(5):
                mm = r["fold"] == f
                if mm.any(): p[mm] = MODELS[f].predict_proba(r["X"][mm])[:, 1]
        else: p = np.mean([M.predict_proba(r["X"])[:, 1] for M in MODELS], 0)
        sc[np.nonzero(r["m"])[0]] = p
    T["bdt"] = sc; r["score"] = sc
    np.savez_compressed(f"{OUT}/bdt_scores/{r['k']}__{r['t']}.npz", score=sc)
# threshold optimisation on expected Z_syst (same uncertainty model as the cut-based optimisation in p05_run.py)
REL = A.REL
def summ_fold(c, fold, L=500.):
    """fold-wise check only (direct window counts in one fold, scaled x5): relative comparison BDT vs cut-based"""
    s = b = vb = var = 0.0
    for k in S.T:
        r = A.R[k]
        if r["role"] not in ("sig", "bkg", "qcdwh"): continue
        yk = vk = 0.0
        for t in ("D", "F1", "F2", "FL", "EG"):
            T, w, use = S.rows(k, t, A.SC0)
            if T is None: continue
            m = A.sel(T, c) & use & (((T["evt"].astype(np.int64) + zlib.crc32(k.encode())) % 5) == fold)
            if r["cls"] == "FL" and t == "D": m &= T["cat"] != "NPL"
            yk += w[m].sum()*L*5; vk += (w[m]**2).sum()*(L*5)**2
        if r["role"] == "sig": s += yk; continue
        b += yk; vb += vk; var += (REL[r["cls"]]*yk)**2
    sb = np.sqrt(var + vb + (0.025*b)**2); return A.z_syst(s, b, sb), s, b
def summ(c):
    t = A.summary(S, c)[0]; return t["Zsyst"], t["s"], t["b"]
cut = dict(PRE, win=OPT["win"])
TH = np.round(np.arange(0.50, 0.991, 0.02), 3); zs = [summ(dict(cut, bdt=t)) for t in TH]; zmax = max(z[0] for z in zs)
ok = [i for i, z in enumerate(zs) if z[0] >= 0.97*zmax]; ib = max(ok, key=lambda i: zs[i][1]); tbest = float(TH[ib])
zc = summ(OPT)
fz = [dict(fold=f, Z_bdt=summ_fold(dict(cut, bdt=tbest), f)[0], Z_cut=summ_fold(OPT, f)[0]) for f in range(5)]
gain = zs[ib][0]/zc[0] - 1 if zc[0] > 0 else 0.0
stable = all(x["Z_bdt"] > x["Z_cut"] for x in fz) and max(a["auc_train"] - a["auc_test"] for a in AUC) < 0.02
adopt = bool(gain > 0.10 and stable)
out = dict(features=FEAT, pre=PRE, auc=AUC, scan=[dict(t=float(t), Z=z[0], s=z[1], b=z[2]) for t, z in zip(TH, zs)], t_best=tbest,
           Z_bdt=zs[ib][0], s_bdt=zs[ib][1], b_bdt=zs[ib][2], Z_cut=zc[0], s_cut=zc[1], b_cut=zc[2], gain=gain, folds=fz, stable=stable, adopted=adopt,
           final_cuts=dict(cut, bdt=tbest) if adopt else OPT,
           importance=dict(zip(FEAT, np.mean([M.feature_importances_ for M in MODELS], 0).round(4).tolist())))
json.dump(out, open(f"{OUT}/bdt.json", "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
print(json.dumps({k: out[k] for k in ("t_best", "Z_bdt", "s_bdt", "b_bdt", "Z_cut", "s_cut", "b_cut", "gain", "stable", "adopted")}, indent=0))
