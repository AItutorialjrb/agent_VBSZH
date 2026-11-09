#!/usr/bin/env python3
"""Aggregate work/bgmodel/rate/rate_*.json (per-file, scripts/rate_genuine.py) into work/bgmodel/rate_table.json (read by skim.py) and a disjoint even/odd-seed closure.
Classes W (F_Wjjjj, all files) and TT (T_ttjj_1l). Variants per [barrel,endcap] x jet-pT bin: nom = genuine in-jet photons (veto R>=0.5), up/dn = nom +- Clopper-Pearson 68 % half-width,
all = genuine + artefact (artefact-included rate = 'uncalibrated direct'), r03/r07 = veto cut 0.3/0.7.  TT bins with < 5 genuine counts use the pooled (W+TT) rate and pooled x histogram (stated)."""
import json, glob, re, sys, numpy as np
from scipy.stats import beta
WH = "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh"; PT = [25, 35, 50, 75, 100, 150, 1000]; XB = np.linspace(0, 1.5, 16)
R = {"W": [], "TT": []}
for f in sorted(glob.glob(f"{WH}/work/bgmodel/rate/rate_*.json")):
    d = json.load(open(f)); c = "W" if "/rate_F_Wjjjj__" in f else ("TT" if "/rate_T_ttjj_1l__" in f else None)
    if c: d["seed"] = int(re.search(r"_s(\d+)\.json", f).group(1)); R[c].append(d)
def cp(k, n): return (float(beta.ppf(0.16, k, n-k+1)) if k > 0 else 0.0, float(beta.ppf(0.84, k+1, n-k)) if n else 1.0)
def tot(L, key, k=None): return sum((np.array(d[key]) if k is None else np.array(d[key])[k] for d in L), np.zeros((6, 15)) if key == 'xh' else np.zeros((2, 6)))
def table(Ls):
    S = {}
    for c, L in Ls.items():
        S[c] = dict(den=tot(L, "den"), g=[tot(L, "num_gen", k) for k in range(3)], a=tot(L, "num_art"), xh=tot(L, "xh"), n=len(L))
    P = dict(den=S["W"]["den"]+S["TT"]["den"], g=[S["W"]["g"][k]+S["TT"]["g"][k] for k in range(3)], a=S["W"]["a"]+S["TT"]["a"], xh=S["W"]["xh"]+S["TT"]["xh"])
    out = {"pt_edges": PT, "x_edges": XB.tolist(), "eta_bins": [[0, 1.5], [1.5, 2.5]], "n_files": {c: S[c]["n"] for c in S}}
    for c in S:
        den = S[c]["den"]; pool = S[c]["n"] == 0 or c == "TT"
        use = lambda num, pnum: np.where((S[c]["g"][1] >= 5) | (c == "W"), num, pnum)   # TT: pooled where sparse
        def rate(num, pnum, den_c, pden): return np.where(den_c > 0, use(num, pnum)/np.maximum(np.where((S[c]["g"][1] >= 5) | (c == "W"), den_c, pden), 1), 0.0)
        nom = rate(S[c]["g"][1], P["g"][1], den, P["den"]); nn = np.where((S[c]["g"][1] >= 5) | (c == "W"), S[c]["g"][1], P["g"][1]); dd = np.where((S[c]["g"][1] >= 5) | (c == "W"), den, P["den"])
        err = np.array([[0.5*(cp(nn[i, j], dd[i, j])[1]-cp(nn[i, j], dd[i, j])[0]) if dd[i, j] > 0 else 0 for j in range(6)] for i in range(2)])
        out["nom_"+c] = nom.tolist(); out["up_"+c] = (nom+err).tolist(); out["dn_"+c] = np.maximum(nom-err, 0).tolist()
        out["all_"+c] = rate(S[c]["g"][1]+S[c]["a"], P["g"][1]+P["a"], den, P["den"]).tolist()
        out["r03_"+c] = rate(S[c]["g"][0], P["g"][0], den, P["den"]).tolist(); out["r07_"+c] = rate(S[c]["g"][2], P["g"][2], den, P["den"]).tolist()
        out["den_"+c] = den.tolist(); out["num_gen_"+c] = S[c]["g"][1].tolist(); out["num_art_"+c] = S[c]["a"].tolist(); out["x_hist_"+c] = (S[c]["xh"] if c == "W" else np.where(S[c]["xh"].sum(1, keepdims=True) >= 5, S[c]["xh"], P["xh"])).tolist()
    return out
out = table(R); json.dump(out, open(f"{WH}/work/bgmodel/rate_table.json", "w"), indent=1)
clo = {}
for a, b in ((0, 1), (1, 0)):
    A = table({c: [d for d in R[c] if d["seed"] % 2 == a] for c in R}); Bd = {c: [d for d in R[c] if d["seed"] % 2 == b] for c in R}
    tot_chi = 0; nd = 0
    for c in ("W",):
        den = tot(Bd[c], "den"); obs = tot(Bd[c], "num_gen", 1); pred = np.array(A["nom_"+c])*den; sig = np.sqrt(np.maximum(pred, 1e-9)+(den*0.5*(np.array(A["up_"+c])-np.array(A["dn_"+c])))**2)
        z = np.where(den > 0, (obs-pred)/sig, 0); tot_chi += float((z**2).sum()); nd += int((den > 0).sum())
    clo[f"measure_{'even' if a == 0 else 'odd'}_test_{'odd' if a == 0 else 'even'}"] = dict(chi2=tot_chi, ndof=nd)
json.dump(clo, open(f"{WH}/work/bgmodel/rate_closure.json", "w"), indent=1)
print("files", out["n_files"]); 
for c in ("W", "TT"):
    print(c, "rate nom [%] barrel", np.round(np.array(out["nom_"+c])[0]*100, 5), "endcap", np.round(np.array(out["nom_"+c])[1]*100, 5)); print("  genuine counts", np.array(out["num_gen_"+c]).astype(int).tolist(), "artefact", np.array(out["num_art_"+c]).astype(int).tolist(), "den", np.array(out["den_"+c]).astype(int).tolist())
print(clo)
