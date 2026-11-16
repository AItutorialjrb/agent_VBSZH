#!/usr/bin/env python3
"""Aggregate the toy validation (A4) -> work/stat/toys_summary_v12.json (R2 version after verifier T1-T6).
q0: toys at mu=1 (s+b) and mu=0 (null). Expected Z0 from toys = Phi^-1(1 - p_mid), p_mid = P(q0_null > q) + 0.5 P(|q0_null - q| <= 1e-6) evaluated at the MEDIAN q of the s+b toys (the 1e-6 tie width = numerical noise of the fits: q0 values below ~1e-6 are numerical zeros), clipped at 0; the range evaluates the same map at the binomial +-1 sigma quantiles of that median (central value always inside the range). Fractions of q0 == 0 exactly, < 1e-6, < 1e-3 are reported for both sets.
lambda=-1: q(lambda=-1) of SM toys (all constrained nuisances thrown), Z_toy = sqrt(50 % quantile of q) (q is DISCRETE at these counts: plateau flag when the +-1 sigma quantile bracket is degenerate); band = q 16-84 %; base of q = minimum of the profile over the SM point and a lambda grid (vh_coup.py --toys).
mu95: CLs_exp(mu) = p_sb(q_med,b)/p_b(q_med,b) per mu point (p_b = 0.5 at the median of the b toys); expected mu95 from (i) linear interpolation of ln CLs in mu between neighbouring points and (ii) a weighted straight-line fit of ln CLs vs mu (error from the fit covariance); both reported."""
import json, glob, os, re, numpy as np
from scipy.stats import norm
WH = "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh"; T = f"{WH}/work/toys"; S = f"{WH}/work/stat"; rng = np.random.default_rng(7); EPS = 1e-6
out = dict(q0={}, lambda_m1={}, lambda_true_m1={}, mu95={}, notes="500 fb^-1, definition (a), expected (SM Asimov central point). Toys seeded per chunk (np.random.seed(seed) in toys.py; the vhcoup toys use default_rng(seed)); the earlier unseeded production is archived in work/toys_prefix/.")
def qrange(x):
    e = np.sqrt(0.25/len(x)); return float(np.quantile(x, 0.5-e)), float(np.quantile(x, 0.5+e))
def zof(qn, q):
    p = float((qn > q+EPS).mean() + 0.5*(np.abs(qn-q) <= EPS).mean()); return float(max(norm.isf(min(max(p, 1e-12), 1-1e-12)), 0.0)), p
for lab, ws, w in (("WH", "WH", "wh"), ("ZH", "ZH", "zh"), ("VH", "VH", "both")):
    fs = glob.glob(f"{T}/q0_{ws}_workspace_mu_s*.npy"); nf = glob.glob(f"{T}/q0null_{ws}_workspace_mu_s*.npy")
    if not fs: continue
    q = np.concatenate([np.load(f) for f in fs]); za = json.load(open(f"{S}/vh_z0mu_500_a_{w}_v12.json"))["Z0"]; med = float(np.median(q)); lo, hi = qrange(q)
    d_ = dict(Z0_asimov=za, ntoys=int(len(q)), median_q0_sb=med, frac_q0_exact_zero_sb=float((q == 0).mean()), frac_q0_lt_1em6_sb=float((q < 1e-6).mean()), frac_q0_lt_1em3_sb=float((q < 1e-3).mean()), mean_q0_sb=float(q.mean()), asimov_q0=za**2)
    if nf:
        qn = np.concatenate([np.load(f) for f in nf]); z0, p0 = zof(qn, med); zlo, _ = zof(qn, lo); zhi, _ = zof(qn, hi)
        d_.update(ntoys_null=int(len(qn)), frac_q0_exact_zero_null=float((qn == 0).mean()), frac_q0_lt_1em6_null=float((qn < 1e-6).mean()), frac_q0_lt_1em3_null=float((qn < 1e-3).mean()), p_mid_at_median=p0, Z0_toy_median=z0, Z0_toy_range=[min(zlo, z0, zhi), max(zlo, z0, zhi)], Z0_toy_err=0.5*(max(zlo, z0, zhi)-min(zlo, z0, zhi)),
                  Z0_toy_raw_p_ge=float(norm.isf(max(float((qn >= med).mean()), 1e-9))), note="Z0_toy_raw_p_ge uses the strict raw median with p = P(q0_null >= median) (no tie treatment): shown for transparency")
    out["q0"][lab] = d_
for conv, tag in (("kZ-sign", "kzneg"), ("kW-sign", "")):
    fs = glob.glob(f"{T}/vhcoup_toys{'_kzneg' if tag else ''}_v12_s*.json")
    if not fs: continue
    D = [json.load(open(f)) for f in fs]; ref = json.load(open(f"{S}/couplings_vh{'_kzneg' if tag else ''}_v12.json"))
    for lab in ("WH", "ZH", "VH"):
        q = np.concatenate([d["q_lambda_m1"][lab] for d in D]); med = float(np.median(q)); lo, hi = qrange(q)
        out["lambda_m1"][f"{conv}:{lab}"] = dict(Z_asimov=ref["curves"][lab]["Z_lambda_m1"], Z_toy_median=float(np.sqrt(med)), Z_toy_16=float(np.sqrt(np.percentile(q, 16))), Z_toy_84=float(np.sqrt(np.percentile(q, 84))), Z_toy_bracket=[float(np.sqrt(lo)), float(np.sqrt(hi))], plateau=bool(lo == hi), n_distinct_q=int(len(set(np.round(q, 6)))),
                                                 frac_q_lt_1=float((q < 1).mean()), asimov_q=ref["curves"][lab]["Z_lambda_m1"]**2, toy_median_q=med, ntoys=int(len(q)),
                                                 note="median of a DISCRETE q distribution (plateau when bracket is degenerate: the bracket error is then not meaningful, use the 16-84 % band); for q << 1 (ZH alone) the median is fluctuation-dominated and not comparable with the Asimov value")
# R4/F2: toys THROWN AT lambda = -1: q(lambda=-1) vs the best fit; asymptotically chi2(1 dof). Reports the tail fractions against chi2(1) and the count above the Asimov q of the SM-data exclusion
from scipy.stats import chi2 as _c2
for conv, tag in (("kZ-sign", "kzneg"), ("kW-sign", "")):
    fs = glob.glob(f"{T}/vhcoup_lam1_toys{'_kzneg' if tag else ''}_v12_s*.json")
    if not fs: continue
    D = [json.load(open(f)) for f in fs]; ref = json.load(open(f"{S}/couplings_vh{'_kzneg' if tag else ''}_v12.json"))
    for lab in ("WH", "ZH", "VH"):
        q = np.concatenate([d["q_true_lambda_m1"][lab] for d in D]); n = len(q); qa = ref["curves"][lab]["Z_lambda_m1"]**2
        thr = (1.0, 2.71, 3.84, 6.63, 9.0, 10.83); fr = {str(t_): dict(toy=float((q > t_).mean()), chi2_1=float(_c2.sf(t_, 1)), n_toy=int((q > t_).sum())) for t_ in thr}
        out["lambda_true_m1"][f"{conv}:{lab}"] = dict(ntoys=int(n), q_asimov=qa, Z_asimov=ref["curves"][lab]["Z_lambda_m1"], n_ge_qasimov=int((q >= qa).sum()), p_chi2_at_qasimov=float(_c2.sf(qa, 1)), tail=fr, q_mean=float(q.mean()), q_max=float(q.max()),
            note="toys thrown at lambda=-1 (nuisances N(0,1), Poisson counts), q = fit(-1) minus the minimum over the SM point and the lambda grid; chi2(1 dof) expected; the toy count resolves p down to about 1/ntoys (about 3.5 sigma for 5000 toys): the 3.8 sigma tail itself is not toy-resolved")
for lab, w in (("WH", "wh"), ("ZH", "zh"), ("VH", "both")):
    mus = sorted({float(re.search(r"_mu([0-9.]+)_", f).group(1)) for f in glob.glob(f"{T}/qmu_{lab}_workspace_mu_mu*_sb_s*.npy")})
    if len(mus) < 2: continue
    cls = []
    for mu in mus:
        sb = np.concatenate([np.load(f) for f in glob.glob(f"{T}/qmu_{lab}_workspace_mu_mu{mu}_sb_s*.npy")]); b = np.concatenate([np.load(f) for f in glob.glob(f"{T}/qmu_{lab}_workspace_mu_mu{mu}_b_s*.npy")])
        f_ = lambda sbx, bx: (np.mean(sbx >= np.median(bx)) / max(np.mean(bx >= np.median(bx)), 1e-9)); c0 = f_(sb, b); bs = [f_(rng.choice(sb, len(sb)), rng.choice(b, len(b))) for _ in range(300)]; cls.append((mu, c0, float(np.std(bs)), len(sb), len(b)))
    mu_ = np.array([c[0] for c in cls]); c_ = np.array([c[1] for c in cls]); e_ = np.array([c[2] for c in cls]); ok = c_ > 0
    def interp(cv): return float(np.exp(np.interp(np.log(0.05), np.log(np.maximum(cv, 1e-6))[::-1], np.log(mu_)[::-1]))) if cv.min() < 0.05 < cv.max() else None
    # weighted straight line ln CLs = a + b mu
    X = np.stack([np.ones(ok.sum()), mu_[ok]], 1); y = np.log(c_[ok]); wgt = 1/np.maximum(e_[ok]/c_[ok], 0.05); A = X*wgt[:, None]; coef, *_ = np.linalg.lstsq(A, y*wgt, rcond=None); cov = np.linalg.inv(A.T@A)
    mfit = float((np.log(0.05)-coef[0])/coef[1]) if coef[1] < 0 else None; gradv = np.array([-1/coef[1], -(np.log(0.05)-coef[0])/coef[1]**2]); merr = float(np.sqrt(gradv@cov@gradv)) if mfit else None
    asy = json.load(open(f"{S}/vh_z0mu_500_a_{w}_v12.json"))["mu95"][1]
    out["mu95"][lab] = dict(mu95_asymptotic=asy, mu95_toy_interp=interp(c_), mu95_toy_fit=mfit, mu95_toy_fit_err=merr, points=[dict(mu=c[0], CLs_exp=c[1], err=c[2], n_sb=c[3], n_b=c[4]) for c in cls])
json.dump(out, open(f"{S}/toys_summary_v12.json", "w"), indent=1); print(json.dumps({k: v for k, v in out.items() if k != "notes"}, default=float)[:1800])
