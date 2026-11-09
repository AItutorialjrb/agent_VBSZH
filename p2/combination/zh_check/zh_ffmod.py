# exec'd inside the patched copy of the frozen final_analysis.py (namespace: np, glob, json, os, optimize, masks, REG, DATA, MU, SIG, WIDE, MZ ...)
# Replaces the direct-count estimate of the fake-photon rows F_QCD_Zajj / F_EW_Zajj by the fake-factor (H1 / D34) estimate.
FFDIR = "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/combination/zh_check/out"
FFSIDS = {"F_QCD_Zajj": "F_QCD_llajj_vbs", "F_EW_Zajj": "F_EW_llajj_vbs"}
FFKAPPA = float(os.environ.get("FFKAPPA", "1.0")); FFMODE = os.environ.get("FFMODE", "ff")     # ff | direct
exec(open("/eos/home-r/rjiang/vbs_zh_codex_starter/p2/combination/zh_check/zh_ffmod_lib.py").read())
def _rate_tables():
    A = {}
    for s in ("F_QCD_llajj_vbs", "F_EW_llajj_vbs"):
        for f in sorted(glob.glob(f"{FFDIR}/{s}__c[0-9][0-9][0-9]_rate.npz")):
            d = np.load(f)
            for k in d.files:
                if k != "nev_total": A[k] = A.get(k, 0) + d[k]
    return A
_RT = _rate_tables()
RATE = _RT["num_gen"]/np.maximum(_RT["den"], 1); RATE_ERR = np.sqrt(np.maximum(_RT["num_gen"], 1))/np.maximum(_RT["den"], 1)
PX = _RT["xh"].sum(0)/_RT["xh"].sum()
def _load_ffm(sample):
    ch = sorted(glob.glob(f"{FFDIR}/{sample}__c[0-9][0-9][0-9]_ffm.npz")); A = {}; off = 0
    for c in ch:
        d = np.load(c)
        for k in d.files:
            if k == "nev_total": continue
            A.setdefault(k, []).append(d[k] + (off if k == "evt" else 0))
        off += 10**8
    return {k: np.concatenate(v) for k, v in A.items()}
FFD_ = {}
for _sid, _smp in FFSIDS.items():
    if FFMODE == "ff": FFD_[_sid] = ff_expand(_load_ffm(_smp), rate=RATE, px=PX, kappa=FFKAPPA*(float(os.environ.get("FFKAPPA_EW", "1.0")) if _sid == "F_EW_Zajj" else 1.0))
def fwin_w(mgg, w, c):
    x = mgg - WIDE[0]; L = WIDE[1] - WIDE[0]; lo, hi = MU - c["wk"]*SIG - WIDE[0], MU + c["wk"]*SIG - WIDE[0]
    if len(x) < 5 or w.sum() <= 0: return (hi - lo)/L, 0.0
    w = w/w.sum()
    nll = lambda lam: (np.log(L)) if abs(lam) < 1e-6 else -(w*(np.log(abs(lam)) - lam*x)).sum() + np.log(abs(1 - np.exp(-lam*L)))
    lam = optimize.minimize_scalar(nll, bounds=(-0.2, 0.2), method="bounded").x
    if abs(lam) < 1e-6: return (hi - lo)/L, 0.0
    return (np.exp(-lam*lo) - np.exp(-lam*hi))/(1 - np.exp(-lam*L)), float(lam)
def _evt_err(evt, w):
    if len(w) == 0: return 0.0
    u, inv = np.unique(evt, return_inverse=True); s = np.bincount(inv, weights=w); return float(np.sqrt((s**2).sum()))
def ff_estimate(sid, c):
    """yield per fb^-1 and stat; L0 (window, >= 10 distinct events) else L1 (weighted exponential m_gg shape over WIDE)"""
    r = REG[sid]; d = dict(FFD_[sid]); we = r["w_evt_fb"]; d["w"] = d["wr"]*we
    pre, lg, jb, vbs, win, wide = masks(d, c); full = pre & lg & jb & vbs
    nwin_ev = len(np.unique(d["evt"][full & win])); nwide_ev = len(np.unique(d["evt"][full & wide]))
    if nwin_ev >= 10 or nwide_ev < 3:
        m = full & win; return d["w"][m].sum(), _evt_err(d["evt"][m], d["w"][m]), nwin_ev, nwide_ev, "FF L0 direct (window)", dict(neff_ev=nwin_ev)
    m = full & wide; f, lam = fwin_w(d["mgg"][m], d["w"][m], c); y = d["w"][m].sum()*f
    return y, _evt_err(d["evt"][m], d["w"][m])*f, nwin_ev, nwide_ev, "FF L1 m_gg-shape (weighted exp. fit)", dict(f_win=f, lam=lam, neff_ev=nwide_ev)
if FFMODE == "ff":
    _est0 = estimate
    def estimate(sid, c):
        return ff_estimate(sid, c) if sid in FFSIDS else _est0(sid, c)
FFD = float(os.environ.get("FFD", "0.0")); FFDD = {"F_QCD_Zajj": FFD, "F_EW_Zajj": float(os.environ.get("FFD_EW", str(FFD)))}     # relative calibration difference added in quadrature to the 50 % fake normalisation
FFINFO = dict(mode=FFMODE, kappa=FFKAPPA, kappa_ew_extra=float(os.environ.get("FFKAPPA_EW", "1.0")), ffd=FFDD, rate=RATE.tolist(), rate_err=RATE_ERR.tolist(), px=PX.tolist(), den=_RT["den"].tolist(), num_gen=_RT["num_gen"].tolist(),
              rows={k: int(len(v["evt"])) for k, v in FFD_.items()})
