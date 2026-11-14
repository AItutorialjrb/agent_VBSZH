#!/usr/bin/env python3
"""single_r1 WH Phase 06-07: systematic model, counting results (Eq. 1 primary, Z with sigma_b, exact-Poisson CLs mu95),
binned m_gg profile-likelihood fit (definitions a and b), robustness table, lambda_WZ and (kappa_W, kappa_Z) interpretation.
Inputs: wh/work/p05/p05.json (OPT), optional wh/work/p05/bdt_scores/*.npz + bdt.json (adopted only if the BDT passed its rule).
Output: wh/work/p05/p07.json.   Usage: python3 -P p07_stats.py"""
import sys, os, json, glob, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import whana as A
from scipy import optimize, stats
OUT = f"{A.WH}/work/p05"
P5 = json.load(open(f"{OUT}/p05.json"))
def tup(c): return {k: (tuple(v) if isinstance(v, list) else v) for k, v in c.items()}
OPT = tup(P5["OPT"]); PEAK = P5["peak"]; MU0, SIG0 = PEAK["mu"], PEAK["sigma_core"]
S = A.Store()
S.ceg = {k: tuple(v) for k, v in P5["eg_closure_factor"].items()}   # e->gamma closure factors from p05
BDT = json.load(open(f"{OUT}/bdt.json")) if os.path.exists(f"{OUT}/bdt.json") else None
if BDT:   # attach k-fold scores (same row order as the ntuple tables)
    for f in glob.glob(f"{OUT}/bdt_scores/*.npz"):
        d = np.load(f); k, t = os.path.basename(f)[:-4].split("__")
        if k in S.T and S.T[k].get(t): assert len(d["score"]) == len(S.T[k][t]["w"]); S.T[k][t]["bdt"] = d["score"]
FINAL = tup(BDT["final_cuts"]) if BDT and BDT.get("adopted") else OPT
J = dict(final_cuts=FINAL, final_is_bdt=bool(BDT and BDT.get("adopted")), opt_cutbased=OPT)
# BDT cut (c['bdt']) is applied by whana.sel

RES_KEYS = {k for k, r in A.R.items() if r["th"] in ("sig", "qcdwh", "higgs", "top") and "BGG" in r["factors"]}   # m_gg-resonant
def is_res(k): return k in RES_KEYS
# ------------------------------------------------------------------ variations of the event content (JES, photon scale / resolution)
def varied(T, key, jes=0.0, pes=0.0, res=0.0):
    V = dict(T)
    if jes:
        for v in ("j1pt", "j2pt", "j3pt", "mjj", "ht"): V[v] = T[v]*(1 + jes)
    if pes or (res and is_res(key)):
        mg = T["mgg"]*(1 + pes)
        if res and is_res(key): mg = MU0 + (mg - MU0)*(1 + res)
        V["mgg"] = mg; V["g1pt"] = T["g1pt"]*mg/T["mgg"]; V["g2pt"] = T["g2pt"]*mg/T["mgg"]   # keep pT/m_gg fixed for resolution
        if pes: V["g1pt"] = T["g1pt"]*(1 + pes); V["g2pt"] = T["g2pt"]*(1 + pes)
    return V
MODELS = None
if BDT:
    import xgboost as xgb, zlib
    MODELS = []
    for f in range(5):
        m_ = xgb.Booster(); m_.load_model(f"{OUT}/bdt_models/fold{f}.json"); MODELS.append(m_)
    FEAT = BDT["features"]
def predict(M, X): return M.predict(xgb.DMatrix(X))
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
def rescore(T, k):
    """BDT score for (varied) rows: the held-out fold model for training samples, mean of the five otherwise; rows outside
    the BDT preselection keep -1 (preselection evaluated on the varied variables)"""
    pre = {kk: (tuple(v) if isinstance(v, list) else v) for kk, v in BDT["pre"].items()}
    m = A.sel(T, dict(pre, bdt=None), window=False); sc = np.full(len(T["w"]), -1.0, np.float32)
    if not m.any(): return sc
    X = feats({f: T[f][m] for f in ("mjj", "detajj", "dphijj", "j1pt", "j2pt", "j1eta", "j2eta", "j3pt", "zgg", "zl", "ptgg", "mgg", "g1pt", "g2pt",
                                    "g1eta", "g2eta", "met", "mtw", "l1pt", "l1eta", "drgg", "drlg", "drgj", "ptbal", "ht", "nj30", "ygg")})
    if A.R[k]["role"] in ("sig", "bkg", "qcdwh"):
        fold = ((T["evt"][m].astype(np.int64) + zlib.crc32(k.encode())) % 5).astype(int); p = np.zeros(m.sum())
        for f in range(5):
            mm = fold == f
            if mm.any(): p[mm] = predict(MODELS[f], X[mm])
    else: p = np.mean([predict(M, X) for M in MODELS], 0)
    sc[np.nonzero(m)[0]] = p; return sc
def yields_var(c, sc=A.SC0, window=True, **var):
    if not var: return A.yields(S, c, sc, window)
    keep = {k: {t: S.T[k][t] for t in S.T[k]} for k in S.T}
    S.cache.clear()
    try:
        for k in S.T:
            for t in list(S.T[k]):
                if S.T[k][t]:
                    V = varied(S.T[k][t], k, **var)
                    if MODELS is not None and var.get("jes"): V["bdt"] = rescore(V, k)
                    S.T[k][t] = V
        return A.yields(S, c, sc, window)
    finally:
        for k in S.T: S.T[k].update(keep[k])
        S.cache.clear()

# ------------------------------------------------------------------ theory per sample (7-point scale envelope (+) PDF replicas)
def theory(c):
    out = {}
    for k in S.T:
        T, w, use = S.rows(k, "D", A.SC0)
        if T is None or "scale" not in T or len(T["scale"]) != len(T["w"]): continue
        m = A.sel(T, c, window=False) & use
        if m.sum() < 5: m = A.sel(T, dict(c, mjj=300., deta=2.0, met=0.), window=False) & use   # loose region for low-stat samples
        if m.sum() < 5: continue
        y = w[m].sum(); sc = (w[m, None]*T["scale"][m]).sum(0)/y - 1; pdf = (w[m, None]*T["pdf"][m].astype(float)).sum(0)/y - 1
        out[k] = dict(scale=float(np.abs(sc).max()), pdf=float(np.sqrt((pdf**2).mean())), n=int(m.sum()))
        out[k]["total"] = float(np.hypot(out[k]["scale"], out[k]["pdf"]))
    return out
PROXY = {"F_QCD_Wajjj_nomjj": "B_QCD_Waajj_nomjj", "F_EW_Wajj_nomjj": "B_EW_Waajj_nomjj", "F_Wjjjj": "B_QCD_Waajj_nomjj",
         "T_ttjj_1l": "T_ttaa_1l", "T_tta_1l": "T_ttaa_1l", "T_tWa_1l": "T_ttaa_1l", "ZH_ew_zhjj_zll": "S_EW_WHjj", "ZH_qcd_zhjj_zll": "H_QCD_WH_mlm",
         "ZH_B_QCD_zaajj_nomjj": "B_QCD_Waajj_nomjj", "ZH_B_EW_zaajj_vbs_is1h": "B_EW_Waajj_nomjj", "ZH_B_EW_zaajj_vbs_is2": "B_EW_Waajj_nomjj",
         "ZH_B_EW_zaajj_vbs_is3": "B_EW_Waajj_nomjj", "F_QCD_llajj_loose": "B_QCD_Waajj_nomjj", "ZH_F_EW_llajj_vbs": "B_EW_Waajj_nomjj",
         "Q_aajjj": "B_QCD_Waajj_nomjj", "H_ggF_jj_nomjj": "H_QCD_WH_mlm", "H_VBFH_jj": "S_EW_WHjj"}
PS100 = {"V_WWa_WH", "V_WZa_WH", "V_ZZa_WH", "H_ggZH_wh", "H_ggF_jj_nomjj", "H_VBFH_jj", "F_EW_Wajj_nomjj"}   # D29-type PS-modelling 100 %
GENMJJ = {"ZH_B_EW_zaajj_vbs_is1h": 0.064, "ZH_B_EW_zaajj_vbs_is2": 0.064, "ZH_B_EW_zaajj_vbs_is3": 0.064, "ZH_F_EW_llajj_vbs": 0.064}
FAKE_REL = dict(F1=("jg1", 1.0), F2=("jg2", 1.5), FL=("jl", 1.0), EG=("eg", 1.0))
LUMI = 0.025; EFF_L, EFF_G = 0.02, 0.02
JMREL = [0.0]   # set from jetmod() for the selection in use (backgrounds)
PS_SIG = 0.10   # assumed parton-shower (recoil scheme / central jet activity) uncertainty of EW VBS-type samples on the selection

def nuisances(c, Y, TH):
    """relative uncertainty per (sample, nuisance) on the SR yield; nuisances are 100 % correlated across samples sharing a name"""
    N = {}
    for k, y in Y.items():
        r = A.R[k]
        if r["role"] in ("xcheck", "coup"): continue
        n = {"lumi": LUMI}
        th = TH.get(k) or TH.get(PROXY.get(k, ""), None)
        n[f"th_{r['th']}"] = th["total"] if th else 0.10
        comp = y["comp"] or {}
        yy = {t: comp[t]["y"] for t in ("D", "F1", "F2", "FL", "EG") if t in comp and isinstance(comp[t], dict)}
        tot = sum(yy.values()) or 1.0
        if not any(v > 0 for v in yy.values()): yy = {"D": 1.0}; tot = 1.0
        fD = yy.get("D", 0.0)/tot
        n["eff_obj"] = fD*np.sqrt(EFF_L**2 + 2*EFF_G**2) + (1 - fD)*EFF_L
        if r["role"] == "sig" or r["th"] == "sig": n["ps_sig"] = PS_SIG      # EW (VBS-jet) samples: assumed PS-modelling unc.
        else: n["jetmod"] = JMREL[0]*(fD + yy.get("FL", 0.0)/tot)
        for t, (nm, rel) in FAKE_REL.items():
            if yy.get(t, 0) > 0: n[f"fake_{nm}"] = rel*yy[t]/tot
        if k in PS100: n[f"ps_{k}"] = 1.0
        if k in GENMJJ: n["genmjj_zh"] = GENMJJ[k]
        if y["nraw"] == 0 and y["y"] <= 0: n[f"ul_{k}"] = 1.0
        if y.get("l2", 0) > 0 and y["y"] > 0: n[f"l2_{k}"] = y["l2"]/y["y"]
        N[k] = n
    return N
def shape_nuis(c):
    """JES +-5 %, photon energy scale +-0.5 %, m_gg resolution +-10 % (resonant samples): relative yield change per sample"""
    Y0 = A.yields(S, c); out = {}
    for nm, var in (("jes", dict(jes=0.05)), ("jes_dn", dict(jes=-0.05)), ("pes", dict(pes=0.005)), ("pes_dn", dict(pes=-0.005)), ("res", dict(res=0.10)), ("res_dn", dict(res=-0.10))):
        Yv = yields_var(c, **var)
        for k in Y0:
            if Y0[k]["y"] > 0: out.setdefault(k, {})[nm] = Yv[k]["y"]/Y0[k]["y"] - 1
    return {k: {n: 0.5*(abs(v.get(n, 0)) + abs(v.get(n + "_dn", 0))) for n in ("jes", "pes", "res")} for k, v in out.items()}

WB = {}
def wbar(k, c):
    """mean per-row weight [fb at 1/fb] in a loose region (no VBS / MET / b / BDT cuts): the per-event weight scale for ULs"""
    key = (k, json.dumps(c, sort_keys=True, default=str))
    if key not in WB:
        cl = dict(c, mjj=0., deta=0., met=0., bveto=False, bdt=None); wl = []
        for t in ("D", "F1", "F2", "FL", "EG"):
            T, w, use = S.rows(k, t, A.SC0)
            if T is None: continue
            mm = A.sel(T, cl, window=False) & use
            if mm.any(): wl.append(w[mm])
        r = A.R[k]; WB[key] = float(np.mean(np.concatenate(wl))) if wl else 1e3*r["k"]*S.M[k]["sumw"]/r["N"]/max(S.M[k]["nev"], 1)
    return WB[key]
def totals(c, L, sigdef="a", sc=A.SC0, TH=None, SH=None, theory_on=True, scale_keys=None, extra_ul=False):
    Y = A.yields(S, c, sc, detail=True)
    if scale_keys:
        for k, f in scale_keys.items():
            if k in Y: Y[k] = dict(Y[k], y=Y[k]["y"]*f, var=Y[k]["var"]*f*f)
    N = nuisances(c, Y, TH or {})
    s = b = vs = vb = 0.0; Gb, Gs, comp = {}, {}, {}
    for k, y in Y.items():
        r = A.R[k]
        if r["role"] in ("xcheck", "coup"): continue
        yy, vv = y["y"]*L, y["var"]*L*L
        if y.get("l2", 0) > 0: vv = max(vv - (y["l2"]*L)**2, 0.0)       # L2 parts carry the 100 % l2_<k> nuisance instead of MC stat
        if y["nraw"] == 0 and y["y"] <= 0:          # zero raw support: central 1.14 w̄ with 100 % (nuisance ul_<k>), 95 % UL = 3 w̄
            yy = (3.0 if extra_ul else 1.14)*wbar(k, c)*L
        elif extra_ul and y["neff"] < 10:
            yy = max(yy, 3.0*wbar(k, c)*L)
        comp[k] = dict(y=yy, mc=np.sqrt(vv), nraw=y["nraw"], neff=y["neff"])
        isig = r["role"] == "sig" or (sigdef == "b" and r["role"] == "qcdwh")
        G = Gs if isig else Gb
        for nm, rel in list(N.get(k, {}).items()) + [(f"shape_{x}", v) for x, v in (SH or {}).get(k, {}).items()]:
            if not theory_on and nm.startswith("th_"): continue
            G[nm] = G.get(nm, 0.0) + rel*yy
        if isig: s += yy; vs += vv
        else: b += yy; vb += vv
    sb = float(np.sqrt(vb + sum(v**2 for v in Gb.values()))); ss = float(np.sqrt(vs + sum(v**2 for v in Gs.values())))
    return dict(s=s, b=b, s_mc=np.sqrt(vs), b_mc=np.sqrt(vb), sigma_b=sb, sigma_s=ss, groups_b=Gb, groups_s=Gs, comp=comp)

def counting(c, TH, SH, sc=A.SC0, tag="nominal", **kw):
    out = {}
    for L in A.LUMIS:
        for sd in ("a", "b"):
            T = totals(c, L, sd, sc, TH, SH, **kw); T0 = totals(c, L, sd, sc, TH, SH, theory_on=False, **kw)
            mu, nmed = A.cls_limit(T["s"], T["b"], T["sigma_b"], ss=T["sigma_s"]); mu0, _ = A.cls_limit(T["s"], T["b"], 0.0)
            out[f"{int(L)}_{sd}"] = dict(L=L, sigdef=sd, s=T["s"], b=T["b"], s_mc=T["s_mc"], b_mc=T["b_mc"], sigma_b=T["sigma_b"], sigma_s=T["sigma_s"],
                Z_eq1=A.zeq1(T["s"], T["b"]), Z_eq1_mcerr=A.zeq1_err(T["s"], T["b"], T["s_mc"], T["b_mc"]),
                Z_syst=A.z_syst(T["s"], T["b"], T["sigma_b"]), Z_syst_notheory=A.z_syst(T0["s"], T0["b"], T0["sigma_b"]),
                mu95_cls=mu, mu95_cls_stat=mu0, n_median=nmed, groups_b={k: float(v) for k, v in T["groups_b"].items()},
                groups_s={k: float(v) for k, v in T["groups_s"].items()}, comp=T["comp"] if L == 500. else None)
    return out

# ------------------------------------------------------------------ m_gg binned profile-likelihood fit (Asimov)
EDG = np.arange(105., 160.001, 1.0); CEN = 0.5*(EDG[1:] + EDG[:-1])
def templates(c, sigdef="a", L=500., TH=None):
    """expected per-bin counts: signal (resonant shape from Delphes S_EW_WHjj), resonant bkg, continuum (exp. fit to MC)"""
    cw = dict(c); Y = A.yields(S, cw, window=False, detail=False)
    # resonant shape: 2-Gaussian fit to the Delphes EW signal m_gg after the full selection (window off)
    T, w, use = S.rows("S_EW_WHjj", "D", A.SC0); m = A.sel(T, cw, window=False) & use
    x, ww = T["mgg"][m], w[m]
    h, _ = np.histogram(x, bins=EDG, weights=ww)
    f2 = lambda q, a, mu, s1, fr, s2: a*(fr*np.exp(-0.5*((q - mu)/s1)**2)/s1 + (1 - fr)*np.exp(-0.5*((q - mu)/s2)**2)/s2)
    p, _ = optimize.curve_fit(f2, CEN, h, p0=[h.sum()/2.5, 125, 1.8, 0.8, 5], bounds=([0, 120, 0.5, 0, 2], [np.inf, 130, 4, 1, 20]))
    shape = lambda mu=p[1], sc=1.0: (lambda v: v/v.sum())(f2(CEN, 1, mu, p[2]*sc, p[3], p[4]*sc))
    s = rb = 0.0; xc, wc = [], []
    for k, y in Y.items():
        r = A.R[k]
        if r["role"] in ("xcheck", "coup"): continue
        isig = r["role"] == "sig" or (sigdef == "b" and r["role"] == "qcdwh")
        if isig: s += y["y"]*L
        elif is_res(k): rb += y["y"]*L
        else:
            for t in ("D", "F1", "F2", "FL", "EG"):
                T, w, use = S.rows(k, t, A.SC0)
                if T is None: continue
                mm = A.sel(T, cw, window=False) & use
                if A.R[k]["cls"] == "FL" and t == "D": mm &= T["cat"] != "NPL"
                xc.append(T["mgg"][mm]); wc.append(w[mm]*L)
    xc, wc = np.concatenate(xc), np.concatenate(wc); B = wc.sum()
    nll = lambda lam: -(wc*(np.log(abs(lam) + 1e-12) - lam*(xc - 105.))).sum() + B*np.log(abs(1 - np.exp(-lam*55.)) + 1e-300)
    lam = optimize.minimize_scalar(nll, bounds=(1e-4, 0.2), method="bounded").x
    cont = B*(np.exp(-lam*(EDG[:-1] - 105.)) - np.exp(-lam*(EDG[1:] - 105.)))/(1 - np.exp(-lam*55.))
    return dict(s=s, rb=rb, B=B, lam=lam, shape=shape, cont=cont, par=p.tolist(), n_cont_rows=len(xc))
def fit_result(Tm, unc_s, unc_rb, stat_only=False):
    """Asimov fits: Z from q0 (data = s+b), mu95 from q_mu on Asimov b-only (median, asymptotic CLs: q_mu,A = 1.96^2).
    Free: mu, continuum norm and slope.  Constrained (Gaussian, unless stat_only): signal norm theta_s (unc_s),
    resonant-bkg norm theta_r (unc_rb), photon energy scale (0.5 %), m_gg resolution (10 %)."""
    s, rb, sh = Tm["s"], Tm["rb"], Tm["shape"]; B0, lam0 = Tm["B"], Tm["lam"]
    def expect(mu, nB, lam, ts, tr, tp, tw):
        shp = sh(MU0*(1 + 0.005*tp), 1 + 0.10*tw)
        cont = nB*(np.exp(-lam*(EDG[:-1] - 105.)) - np.exp(-lam*(EDG[1:] - 105.)))/(1 - np.exp(-lam*55.))
        return mu*s*max(1 + unc_s*ts, 1e-3)*shp + rb*max(1 + unc_rb*tr, 1e-3)*shp + cont
    def nll(par, data, mu=None):
        if mu is None: mu, par = par[0], par[1:]
        nB, lam, ts, tr, tp, tw = par
        if stat_only: ts = tr = tp = tw = 0.0
        e = np.maximum(expect(mu, nB, lam, ts, tr, tp, tw), 1e-12)
        return (e - data*np.log(e)).sum() + 0.5*(ts**2 + tr**2 + tp**2 + tw**2)
    x0 = [B0, lam0, 0, 0, 0, 0]; bnds = [(0.05*B0, 20*B0), (1e-4, 0.2), (-5, 5), (-5, 5), (-5, 5), (-3, 3)]
    def prof(data, mu):
        r = optimize.minimize(lambda p: nll(p, data, mu), x0, bounds=bnds, method="L-BFGS-B"); return r.fun
    def glob_(data):
        r = optimize.minimize(lambda p: nll(p, data), [1.0] + x0, bounds=[(-5, 20)] + bnds, method="L-BFGS-B"); return r.fun, r.x[0]
    d1 = expect(1, B0, lam0, 0, 0, 0, 0); d0 = expect(0, B0, lam0, 0, 0, 0, 0)
    g1, mh = glob_(d1); q0 = max(2*(prof(d1, 0.0) - g1), 0.0)
    g0, mh0 = glob_(d0); mh0 = max(mh0, 0.0)
    qmu = lambda mu: max(2*(prof(d0, mu) - g0), 0.0) - 1.96**2
    hi = 1.0
    while qmu(hi) < 0 and hi < 1e4: hi *= 2
    mu95 = optimize.brentq(qmu, 1e-4, hi) if qmu(hi) > 0 else float("nan")
    return dict(Z=float(np.sqrt(q0)), mu95=float(mu95), muhat_sb=float(mh), s=s, rb=rb, B=B0, lam=lam0)

# ------------------------------------------------------------------ jet-modelling nuisance on the selection efficiency (D-WH-14)
def jetmod(c):
    """|1 - eps(MLM QCD WH)/eps(fixed-order QCD WHjj)|, eps = y(c)/y(loose objects, fit range, window): two different jet
    modellings (ME 0-2 jets + MLM vs 2 ME jets + PS) of the same process; applied to every prompt (D) component and to the
    FL component (third-jet / jet-activity dependence), 100 % correlated."""
    e = {}
    for k in ("H_QCD_WH_mlm", "H_QCD_WHjj_fixed"):
        T, w, use = S.rows(k, "D", A.SC0); lo = dict(A.LOOSE, win=c["win"])
        mL = A.sel(T, lo) & use; mF = A.sel(T, c) & use; e[k] = (w[mF].sum()/w[mL].sum(), mF.sum(), mL.sum())
    r = e["H_QCD_WH_mlm"][0]/e["H_QCD_WHjj_fixed"][0]
    st = np.sqrt(1/max(e["H_QCD_WH_mlm"][1], 1) + 1/max(e["H_QCD_WHjj_fixed"][1], 1))
    return dict(ratio=float(r), stat=float(st), rel=float(max(abs(r - 1), st)), eff={k: [float(v[0]), int(v[1]), int(v[2])] for k, v in e.items()})
# ------------------------------------------------------------------ run
JM = jetmod(FINAL); J["jetmod"] = JM; J["jetmod_cutbased"] = jetmod(OPT); print("jetmod", JM, J["jetmod_cutbased"]); JMREL[0] = JM["rel"]
TH = theory(FINAL); J["theory"] = TH
SH = shape_nuis(FINAL); J["shape_unc"] = SH
J["counting"] = counting(FINAL, TH, SH)
if J["final_is_bdt"]:
    JMREL[0] = J["jetmod_cutbased"]["rel"]; TH_c = theory(OPT); SH_c = shape_nuis(OPT)
    J["counting_cutbased"] = counting(OPT, TH_c, SH_c); J["theory_cutbased"] = TH_c; J["shape_unc_cutbased"] = SH_c
    JMREL[0] = JM["rel"]
else: J["counting_cutbased"] = None
FIT = {}
for sd in ("a", "b"):
    for L in A.LUMIS:
        Tm = templates(FINAL, sd, L)
        cn = J["counting"][f"{int(L)}_{sd}"]
        us = cn["sigma_s"]/cn["s"] if cn["s"] > 0 else 0.1
        urb = 0.3   # resonant-background normalisation (theory + fake/PS components of tt̄H, tH, ZH, ggF/VBF H), Gaussian
        FIT[f"{int(L)}_{sd}"] = dict(syst=fit_result(Tm, us, urb), stat=fit_result(Tm, 0, 0, stat_only=True), par_signal_shape=Tm["par"], n_cont_rows=Tm["n_cont_rows"])
        print("fit", sd, L, FIT[f"{int(L)}_{sd}"]["syst"])
J["fit"] = FIT
# robustness (500 and 3000 /fb, def. a and b)
ROB = []
def rob(name, sc=A.SC0, c=FINAL, **kw):
    for L in (500., 3000.):
        for sd in ("a", "b"):
            T = totals(c, L, sd, sc, TH, SH, **kw); mu, _ = A.cls_limit(T["s"], T["b"], T["sigma_b"], ss=T["sigma_s"])
            ROB.append(dict(variant=name, L=L, sigdef=sd, s=T["s"], b=T["b"], Z_eq1=A.zeq1(T["s"], T["b"]), Z_syst=A.z_syst(T["s"], T["b"], T["sigma_b"]), mu95=mu))
rob("nominal")
for nm, sc in (("j->gamma x0.3 (low)", dict(A.SC0, jg="low")), ("j->gamma x3 (high)", dict(A.SC0, jg="high")),
               ("j->gamma Delphes-measured rate (FORMAT 6a)", dict(A.SC0, jgrate="delphes")),
               ("e->gamma 1 % (low)", dict(A.SC0, eg="low")), ("e->gamma 5 % (high)", dict(A.SC0, eg="high")),
               ("e->gamma Delphes-measured rate (FORMAT 6b)", dict(A.SC0, egrate="delphes")),
               ("j->lepton 3e-5 (low)", dict(A.SC0, jl="low")), ("j->lepton 1e-3 (high)", dict(A.SC0, jl="high")),
               ("all fake/mis-ID rates high", dict(A.SC0, jg="high", eg="high", jl="high")),
               ("stock Delphes object efficiencies (no CMS-like reweighting)", dict(A.SC0, eff="delphes"))):
    rob(nm, sc)
rob("conservative: N_eff<10 sources at max(value, 3 w̄), zero-support at 3 w̄", extra_ul=True)
rob("QCD WH x2 (def. a background)", scale_keys={"H_QCD_WH_mlm": 2.0})
rob("cut-based selection (no BDT)" if J["final_is_bdt"] else "baseline (pre-declared) selection", c=OPT if J["final_is_bdt"] else tup(A.BASE))
J["robustness"] = ROB

# ------------------------------------------------------------------ couplings: lambda_WZ = kW/kZ and (kW, kZ)
KPTS = {"K_EW_WHjj_lam_m100": (-1.0, 1.0), "K_EW_WHjj_lam_m050": (-0.5, 1.0), "K_EW_WHjj_lam_p000": (0.0, 1.0), "K_EW_WHjj_lam_p050": (0.5, 1.0),
        "K_EW_WHjj_lam_p100": (1.0, 1.0), "K_EW_WHjj_lam_p150": (1.5, 1.0), "K_EW_WHjj_kap_W15_Z075": (1.5, 0.75), "K_EW_WHjj_kap_W05_Z15": (0.5, 1.5)}
def coupling(c, L):
    Y = A.yields(S, c, keys=[k for k in KPTS if k in S.T] + ["S_EW_WHjj", "S_EW_WHjj_taunu"])
    pts = [(KPTS[k][0], KPTS[k][1], Y[k]["y"]*L, np.sqrt(Y[k]["var"])*L) for k in KPTS if k in Y]
    lam = [(kw, y, e) for kw, kz, y, e in pts if kz == 1.0]
    X = np.array([[kw**2, kw, 1.0] for kw, _, _ in lam]); yv = np.array([y for _, y, _ in lam]); ev = np.array([max(e, 1e-9) for _, _, e in lam])
    coef, *_ = np.linalg.lstsq(X/ev[:, None], yv/ev, rcond=None)     # Y(kW, kZ) = a kW^2 + b kW kZ + g kZ^2
    a, bq, g = coef; chi2 = float(((((X @ coef) - yv)/ev)**2).sum())
    clos = {k: dict(pred=a*KPTS[k][0]**2 + bq*KPTS[k][0]*KPTS[k][1] + g*KPTS[k][1]**2, mc=Y[k]["y"]*L, mc_err=np.sqrt(Y[k]["var"])*L)
            for k in ("K_EW_WHjj_kap_W15_Z075", "K_EW_WHjj_kap_W05_Z15") if k in Y}
    clos["S_EW_WHjj (SM, separate sample)"] = dict(pred=a + bq + g, mc=Y["S_EW_WHjj"]["y"]*L, mc_err=np.sqrt(Y["S_EW_WHjj"]["var"])*L)
    return dict(a=a, b=bq, g=g, chi2=chi2, ndf=len(lam) - 3, points=pts, closure=clos)
def nll_count(n, mu_b, sb, s_h):
    """-2 ln L ratio for Asimov n vs hypothesis with signal s_h; Gaussian-constrained b (profiled), Poisson"""
    def f(t):
        e = max(s_h + mu_b + sb*t, 1e-9); return 2*(e - n*np.log(e)) + t*t
    r = optimize.minimize_scalar(f, bounds=(-5, 5), method="bounded"); return r.fun
COUP = {}
for L in A.LUMIS:
    cf = coupling(FINAL, L); T = totals(FINAL, L, "a", A.SC0, TH, SH)
    s_sm, b = T["s"], T["b"]; sb = T["sigma_b"]
    ytau = T["comp"].get("S_EW_WHjj_taunu", {}).get("y", 0.0); yq = T["comp"].get("H_QCD_WH_mlm", {}).get("y", 0.0)
    Ysm = cf["a"] + cf["b"] + cf["g"]
    def pred(kw, kz):
        """signal (quadratic form, normalised to the SM S_EW_WHjj yield) + tau feed-down (same scaling) + QCD WH (x kW^2) + other b"""
        r = (cf["a"]*kw**2 + cf["b"]*kw*kz + cf["g"]*kz**2)/Ysm
        return s_sm*r, ytau*r, yq*kw**2, b - ytau - yq
    n = s_sm + b
    def q(kw, kz):
        s_, t_, q_, o_ = pred(kw, kz); return nll_count(n, o_ + t_ + q_, sb, s_) - nll_count(n, b, sb, s_sm)
    lams = np.linspace(-2, 3, 501); ql = np.array([q(l, 1.0) for l in lams])
    neg = lams < 0
    lo68 = lams[ql < 1.0]; lo95 = lams[ql < 3.84]
    kws, kzs = np.linspace(-2, 2.5, 91), np.linspace(0, 2.5, 51)
    Q2 = np.array([[q(a_, b_) for a_ in kws] for b_ in kzs])
    COUP[int(L)] = dict(quad=cf, Ysm_quad=Ysm, s_sm=s_sm, b=b, sigma_b=sb, qcdwh=yq, taunu=ytau,
        Z_excl_lam_m1=float(np.sqrt(max(q(-1.0, 1.0), 0))), Z_excl_lam_neg=float(np.sqrt(max(ql[neg].min(), 0))),
        lam_at_min_neg=float(lams[neg][ql[neg].argmin()]), lam68=[float(lo68.min()), float(lo68.max())] if len(lo68) else None,
        lam95=[float(lo95.min()), float(lo95.max())] if len(lo95) else None, lam95_disjoint=bool(len(lo95) and np.any(np.diff(np.nonzero(ql < 3.84)[0]) > 1)),
        scan_lam=dict(lam=lams[::5].tolist(), q=ql[::5].tolist()), scan2d=dict(kw=kws.tolist(), kz=kzs.tolist(), q=Q2.tolist()))
    print("coupling", L, COUP[int(L)]["Z_excl_lam_m1"], COUP[int(L)]["Z_excl_lam_neg"], COUP[int(L)]["lam95"])
J["coupling"] = COUP
json.dump(J, open(f"{OUT}/p07.json", "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else (float(o) if isinstance(o, (np.floating,)) else str(o)))
print("wrote", f"{OUT}/p07.json")
