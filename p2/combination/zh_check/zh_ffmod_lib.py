import numpy as np
PTB_ = np.array([25, 35, 50, 75, 100, 150, 1000.]); XC_ = 0.5*(np.linspace(0, 1.5, 16)[1:] + np.linspace(0, 1.5, 16)[:-1])
def _p4(pt, eta, phi, m=0.0): return np.stack([pt*np.cos(phi), pt*np.sin(phi), pt*np.sinh(eta), np.sqrt((pt*np.cosh(eta))**2 + m**2)], -1)
def _kin(P):
    px, py, pz, e = P[..., 0], P[..., 1], P[..., 2], P[..., 3]
    m = np.sqrt(np.maximum(e**2 - px**2 - py**2 - pz**2, 0)); pt = np.hypot(px, py)
    with np.errstate(all="ignore"): y = 0.5*np.log((e + pz)/(e - pz))
    return m, pt, y
def ff_expand(F, rate=None, px=None, kappa=1.0, ptmin=20.0):
    """rows x x-bins -> derived-variable dict with weights (rate x P(x)); the faking GenJet defines the photon direction"""
    ib = np.clip(np.digitize(F["jc"][:, 0], PTB_) - 1, 0, 5); ie = (np.abs(F["jc"][:, 1]) >= 1.5).astype(int)
    n = len(ib); out = {}
    reps = lambda a: np.repeat(a, len(XC_), axis=0)
    jc = reps(F["jc"]); x = np.tile(XC_, n); wr = reps(rate[ib, ie])*np.tile(px, n)*kappa
    fpt = x*jc[:, 0]; ok = (fpt > ptmin) & (np.abs(jc[:, 1]) < 2.5) & ~((np.abs(jc[:, 1]) > 1.4442) & (np.abs(jc[:, 1]) < 1.566))
    g0 = reps(F["g0"]); la = reps(F["la"]); lb = reps(F["lb"]); j = reps(F["j"])
    sw = fpt > g0[:, 0]
    pt1 = np.where(sw, fpt, g0[:, 0]); pt2 = np.where(sw, g0[:, 0], fpt)
    e1 = np.where(sw, jc[:, 1], g0[:, 1]); e2 = np.where(sw, g0[:, 1], jc[:, 1]); f1 = np.where(sw, jc[:, 2], g0[:, 2]); f2 = np.where(sw, g0[:, 2], jc[:, 2])
    PZ = _p4(la[:, 0], la[:, 1], la[:, 2]) + _p4(lb[:, 0], lb[:, 1], lb[:, 2]); PG = _p4(pt1, e1, f1) + _p4(pt2, e2, f2)
    PJ1, PJ2 = _p4(j[:, 0, 0], j[:, 0, 1], j[:, 0, 2], j[:, 0, 3]), _p4(j[:, 1, 0], j[:, 1, 1], j[:, 1, 2], j[:, 1, 3])
    out["mgg"], out["ptgg"], ygg = _kin(PG); out["mjj"], _, _ = _kin(PJ1 + PJ2); _, _, y1 = _kin(PJ1); _, _, y2 = _kin(PJ2); out["mllgg"], _, _ = _kin(PZ + PG)
    out["detajj"] = np.abs(j[:, 0, 1] - j[:, 1, 1])
    with np.errstate(all="ignore"): out["zep_gg"] = np.abs(ygg - 0.5*(y1 + y2))/np.abs(y1 - y2)
    out["g1pt"], out["g2pt"] = pt1, pt2; out["mll"] = reps(F["mll"]); out["ng"] = np.full(len(x), 2); out["nj"] = reps(F["nj"]); out["nb"] = reps(F["nb"])
    out["evt"] = reps(F["evt"]); out["flav"] = reps(F["flav"]); out["l1pt"] = np.fmax(la[:, 0], lb[:, 0]); out["l2pt"] = np.fmin(la[:, 0], lb[:, 0]); out["x"] = x; out["ok"] = ok; out["wr"] = wr
    return {k: v[ok] for k, v in out.items()}
