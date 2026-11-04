#!/usr/bin/env python3
"""Delphes-level morphing closure and MC-stat amplification (G1 review item 3).  VALIDATION, not a result.
 (1) closure: SR-level yields (stages two / vbs / win and the m(HH)-proxy histogram in the pre-window region) predicted from the 6 basis samples via c(k)=m(k)M^-1 vs the direct samples at the closure points
     (T1=(1,0,1), T2=(1,2,1) and T3=(1.25,1.5,2) with kV!=1 and kl!=1).  Error of the prediction = sqrt(sum c_i^2 dY_i^2), dY_i = Y_i/sqrt(k_i) (Poisson on the raw count k_i; k_i=0 -> 1 used as a floor).
 (2) amplification over the scan ranges (kappa2V in [-1,3] at kV=kl=1; kappa_lambda in [-5,10] at kV=k2V=1; kV in [0.5,1.5] at k2V=kl=1; plus a 2-D (k2V,kl) grid): sum|c_i|, and the relative MC error of the morphed SR yield
     A(k) = sqrt(sum c_i^2 dY_i^2)/|Y(k)| for the pilot N and for the planned N (k_i scaled by N_planned/N_pilot).
Usage: morph_delphes.py <matrix.yaml> <out.json> <prod_root> <planned_N.json|-> """
import sys, json, yaml, numpy as np, os, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hh_reco as R
from morph import coeffs, mono
my, outj, root, plan = sys.argv[1:5]
S = {s["name"]: s for s in yaml.safe_load(open(my))["samples"] if s["cls"] == "signal" and s["role"] in ("basis", "closure")}
basis = [n for n, s in S.items() if s["role"] == "basis"]; clos = [n for n, s in S.items() if s["role"] == "closure"]
bpts = [tuple(S[n]["coupling_kV_k2V_kl"]) for n in basis]
D = {n: R.load(R.sample_files(f"{root}/{n}")) for n in basis + clos if R.sample_files(f"{root}/{n}")}
Nplan = json.load(open(plan)) if plan != "-" else {}
BINS = np.array([0, 600, 800, 1000, 1250, 1500, 2000, 3000, 1e5])
def info(n):
    d = D[n]; sig = S[n]["sigma_x_BR_fb"]; two, lead, v = R.stages(d); win = v & R.window(d); ng = d["n_gen"]
    st = {}
    for k, m in (("two", two), ("vbs", v), ("win", win)): st[k] = dict(k=int(m.sum()), Y=sig * m.sum() / ng, dY=sig * np.sqrt(max(m.sum(), 1)) / ng)
    h, _ = np.histogram(d["mHH"][v], BINS); st["hist"] = dict(k=h.astype(int).tolist(), Y=(sig * h / ng).tolist(), dY=(sig * np.sqrt(np.maximum(h, 1)) / ng).tolist())
    return st, ng
I = {n: info(n) for n in D}
res = dict(basis=basis, closure={}, amplification={})
def predict(k, key, idx=None):
    c = coeffs(bpts, k); Y = []; dY = []
    for n in basis:
        s = I[n][0][key]; Y.append(s["Y"] if idx is None else s["Y"][idx]); dY.append(s["dY"] if idx is None else s["dY"][idx])
    Y, dY = np.array(Y), np.array(dY); return float(c @ Y), float(np.sqrt((c**2 * dY**2).sum())), c
for n in clos:
    if n not in D: continue
    k = tuple(S[n]["coupling_kV_k2V_kl"]); r = dict(point=k, sum_abs_c=float(np.abs(coeffs(bpts, k)).sum()), stages={})
    for st in ("two", "vbs", "win"):
        yp, ep, _ = predict(k, st); yd, ed = I[n][0][st]["Y"], I[n][0][st]["dY"]
        r["stages"][st] = dict(k_direct=I[n][0][st]["k"], pred_fb=yp, pred_err=ep, direct_fb=yd, direct_err=ed, pull=(yp - yd) / np.hypot(ep, ed) if np.hypot(ep, ed) > 0 else None)
    chi, nd = 0.0, 0; hb = []
    for b in range(len(BINS) - 1):
        yp, ep, _ = predict(k, "hist", b); yd, ed = I[n][0]["hist"]["Y"][b], I[n][0]["hist"]["dY"][b]
        if I[n][0]["hist"]["k"][b] >= 5: chi += (yp - yd)**2 / (ep**2 + ed**2); nd += 1
        hb.append(dict(bin=[BINS[b], BINS[b+1]], pred=yp, direct=yd, k_direct=I[n][0]["hist"]["k"][b]))
    r["mHH_hist_pre_window"] = dict(chi2=chi, ndf=nd, bins=hb); res["closure"][n] = r
def amp(k, scale):
    c = coeffs(bpts, k); Y = np.array([I[n][0]["win"]["Y"] for n in basis]); kk = np.array([max(I[n][0]["win"]["k"], 1) for n in basis], float)
    sc = np.array([scale.get(n, 1.0) for n in basis]); dY = Y / np.sqrt(kk * sc); yk = float(c @ Y)
    return float(np.abs(c).sum()), yk, (float(np.sqrt((c**2 * dY**2).sum()) / abs(yk)) if yk != 0 else None)
scale_plan = {n: Nplan.get(n, I[n][1]) / I[n][1] for n in basis}
for label, grid in (("k2V", [(1, x, 1) for x in np.linspace(-1, 3, 17)]), ("kl", [(1, 1, x) for x in np.linspace(-5, 10, 31)]), ("kV", [(x, 1, 1) for x in np.linspace(0.5, 1.5, 11)])):
    rows = []
    for k in grid:
        s1, yk, a0 = amp(k, {}); _, _, a1 = amp(k, scale_plan); rows.append(dict(k=k, sum_abs_c=s1, Y_win_fb=yk, relerr_pilotN=a0, relerr_plannedN=a1))
    res["amplification"][label] = rows
g2 = []
for k2 in np.linspace(-1, 3, 9):
    for kl in np.linspace(-5, 10, 7):
        s1, yk, a0 = amp((1, k2, kl), {}); _, _, a1 = amp((1, k2, kl), scale_plan); g2.append(dict(k=(1, k2, kl), sum_abs_c=s1, Y_win_fb=yk, relerr_pilotN=a0, relerr_plannedN=a1))
res["amplification"]["k2V_kl_grid"] = g2
res["N_pilot"] = {n: I[n][1] for n in basis}; res["N_planned"] = {n: Nplan.get(n) for n in basis}; res["k_win_basis"] = {n: I[n][0]["win"]["k"] for n in basis}; res["k_vbs_basis"] = {n: I[n][0]["vbs"]["k"] for n in basis}
json.dump(res, open(outj, "w"), indent=1, default=float)
for n, r in res["closure"].items():
    print(n, r["point"], "sum|c|=%.2f" % r["sum_abs_c"], {s: (v["k_direct"], round(v["pull"], 2) if v["pull"] is not None else None) for s, v in r["stages"].items()}, "hist chi2/ndf=%.1f/%d" % (r["mHH_hist_pre_window"]["chi2"], r["mHH_hist_pre_window"]["ndf"]))
for lab in ("k2V", "kl", "kV"):
    rows = res["amplification"][lab]; print(lab, "max sum|c|=%.1f" % max(r["sum_abs_c"] for r in rows), "max relerr pilot=%s planned=%s" % tuple(("%.2f" % max(x for x in (r[k] for r in rows) if x is not None)) for k in ("relerr_pilotN", "relerr_plannedN")))
