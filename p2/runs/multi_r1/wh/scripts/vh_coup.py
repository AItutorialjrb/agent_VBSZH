#!/usr/bin/env python3
"""Joint lambda_WZ / (kappa_W, kappa_Z) fits for WH, ZH and VH (A3), expected, SM Asimov data, asymptotic, REDUCED nuisance model (as coup_run.py: per-class normalisations, signal theory 5 %, lumi 2.5 %, per-bin Barlow-Beeston-lite); ZH channel from p2/combination/vh_ws/zh_channel_inputs.json (30-bin m_gg templates, per-bin quadratic of the EW ZHjj signal, R_BR as in WH, SAME sign convention).
VH = WH SR (4 mT(Wgg) bins; signal = EW WHjj quadratic + EW ZHjj lost-lepton quadratic from the frozen K_EW_ZHjj samples through the WH selection) + ZH SR; shared nuisances: lumi and the VH signal-theory nuisance; per-class background normalisations uncorrelated between channels (different processes/selections), MC statistics uncorrelated.
Flags as coup_run.py: --kz-neg (primary convention), --no-br, --lumi L. Env STAT_V12=1 STAT_TABLE=table_v12 STAT_YIELDS=yields_v12. Output work/stat/couplings_vh{TAG}.json"""
import sys, os, json, numpy as np
from scipy.optimize import minimize
_src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "coup_run.py")).read().split("res = dict(no_br=")[0]; exec(_src)   # definitions, K table, rbr, sig_bins, quad_fit, bkg_bins, Fit, q_curve (same conventions)
VW = os.environ.get("VH_WS", "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/combination/vh_ws"); ZJ = json.load(open(f"{VW}/zh_channel_inputs.json")); k_ = LUM/500.0
PTS_Z = {"K_EW_ZHjj_lam_m100": (-1.0, 1.0), "K_EW_ZHjj_lam_m050": (-0.5, 1.0), "K_EW_ZHjj_lam_p000": (0.0, 1.0), "K_EW_ZHjj_lam_p050": (0.5, 1.0), "K_EW_ZHjj_lam_p100": (1.0, 1.0), "K_EW_ZHjj_lam_p150": (1.5, 1.0)}
var = "mtwgg"; edges = VARS[var]
def sig_bins_pts(pts):
    m = kmask(); out = {}
    for i, s in enumerate(Km["samples"]):
        if s not in pts: continue
        mm = m & (K["sid"] == i); out[s] = (np.histogram(K[var][mm], bins=edges, weights=K["w"][mm])[0]*LUM/500.0, np.histogram(K[var][mm], bins=edges, weights=K["w"][mm]**2)[0]*(LUM/500.0)**2)
    return out
def quad_fit_pts(sb, pts):
    names = list(pts); A = np.array([[pts[s][0]**2, pts[s][0]*pts[s][1], pts[s][1]**2] for s in names]); nb = len(sb[names[0]][0]); co = np.zeros((nb, 3))
    for i in range(nb):
        y = np.array([sb[s][0][i] for s in names]); e = np.array([max(np.sqrt(sb[s][1][i]), 0.02*abs(sb[s][0][i]), 1e-4) for s in names]); W = 1/e; co[i] = np.linalg.lstsq(A*W[:, None], y*W, rcond=None)[0]
    return co
co_wh = quad_fit(sig_bins(var, edges), None) if False else quad_fit(sig_bins(var, edges))
co_zhwh = quad_fit_pts(sig_bins_pts(PTS_Z), PTS_Z)          # EW ZHjj lost-lepton rows in the WH SR (events at LUM)
G = bkg_bins(var, edges)
# ZH channel
zq = ZJ["coupling"]["quad"]; co_z = np.stack([zq["alpha"], zq["beta"], zq["gamma"]], 1)*k_; zs = ZJ["defs"]["a"]["samples"]
zb = sum(np.array(v["nominal"]) for n, v in zs.items() if v["role"] != "signal")*k_; zerr = np.sqrt(sum(np.array(v["mcstat"])**2 for n, v in zs.items() if v["role"] != "signal"))*k_
def relunc(v):
    u = [max(abs(x["norm_up"]-1), abs(1-x["norm_down"])) for x in v["nuis"].values() if "norm_up" in x]; return float(np.sqrt(np.sum(np.square(u)))) if u else 0.0
zsig_rel = float(np.sqrt(sum(relunc(v)**2*np.sum(v["nominal"])**2 for n, v in zs.items() if v["role"] != "signal"))/max(np.sum(zb)/k_, 1e-12))
class VHFit:
    """channels: list of dict(co (nb,3), bkgc {class: array}, err array, sigma {class: rel}); shared signal-theory and lumi nuisances"""
    def __init__(s, chans, use=("WH", "ZH")):
        s.ch = [c for c in chans if c["name"] in use]; s.cl = [(c["name"], k) for c in s.ch for k in c["bkgc"]]; s.nb = [len(c["co"]) for c in s.ch]; s.sscale = 1.0
    def npar(s): return len(s.cl)+2+sum(s.nb)
    def mu(s, th, kW, kZ):
        ts, tl = th[len(s.cl)], th[len(s.cl)+1]; off = len(s.cl)+2; out = []; j = 0
        for c in s.ch:
            b = sum(c["bkgc"][k]*(1+c["sigma"][k]*th[s.cl.index((c["name"], k))]) for k in c["bkgc"]); nb = len(c["co"]); g = th[off:off+nb]; off += nb
            sg = sig_pred(c["co"], kW, kZ)*(1+0.05*ts)*(1+0.025*tl)*(1.0 if (kW == 1.0 and kZ == 1.0) else s.sscale); out.append(sg+b+c["err"]*g)
        return np.concatenate(out)
    def nll2(s, th, data, kW, kZ):
        nu = np.maximum(s.mu(th, kW, kZ), 1e-9); return 2*np.sum(nu-data*np.log(nu))+np.sum(th**2)
    def prof(s, data, kW, kZ):
        n = s.npar(); return minimize(s.nll2, np.zeros(n), args=(data, kW, kZ), method="L-BFGS-B", bounds=[(-4, 4)]*n).fun
bkgc = {c: np.array([sum(G[g][0][i] for g in G if CLS[g] == c) for i in range(4)]) for c in sorted(set(CLS.values()))}; sg_ = class_sigma()
chW = dict(name="WH", co=co_wh+co_zhwh, bkgc=bkgc, err=np.sqrt(np.array([sum(G[g][1][i]**2 for g in G) for i in range(4)])), sigma=sg_)
chZ = dict(name="ZH", co=co_z, bkgc={"zh_bkg": zb}, err=zerr, sigma={"zh_bkg": max(zsig_rel, 0.05)})
KZ = -1.0 if KZNEG else 1.0
if "--toys" in sys.argv:   # A4: toy validation of the lambda = -1 exclusion: q(lambda=-1) of pseudo-data thrown at the SM (all constrained nuisances thrown N(0,1), Poisson counts); base = minimum of the profile over the SM point and the lambda grid
    NT = int(sys.argv[sys.argv.index("--toys")+1]); SD = int(sys.argv[sys.argv.index("--seed")+1]); rng = np.random.default_rng(SD); gl = np.arange(-2.0, 3.01, 0.5); out = {}
    for lab, use in (("WH", ("WH",)), ("ZH", ("ZH",)), ("VH", ("WH", "ZH"))):
        f = VHFit([chW, chZ], use); qs = []
        for i in range(NT):
            th = rng.normal(size=f.npar()); d = rng.poisson(np.maximum(f.mu(th, 1.0, 1.0), 1e-9)).astype(float); n1 = f.prof(d, -1.0*KZ, KZ)
            nb = min([f.prof(d, 1.0, 1.0)]+[f.prof(d, l*KZ, KZ) for l in gl]); qs.append(max(n1-nb, 0.0))
        out[lab] = qs
    json.dump(dict(convention=("kZ-sign" if KZNEG else "kW-sign"), lumi=LUM, seed=SD, ntoys=NT, q_lambda_m1=out), open(f"{WH}/work/toys/vhcoup_toys{TAG}_s{SD}.json", "w")); sys.exit(0)
lamg = np.round(np.arange(-2.0, 3.001, 0.05), 2); res = dict(convention="kZ-sign primary (kZ=-1, kW=-lambda)" if KZNEG else "kW-sign variant (kZ=+1)", no_br=NOBR, lumi=LUM, zh_yields=dict(signal_SM_events=float(sig_pred(co_z, 1.0, 1.0).sum()), bkg_events=float(zb.sum())), wh_zhjj_in_whSR_SM_events=float(sig_pred(co_zhwh, 1.0, 1.0).sum()), wh_signal_SM_events=float(sig_pred(co_wh, 1.0, 1.0).sum()), curves={}, maps={})
for lab, use in (("WH", ("WH",)), ("ZH", ("ZH",)), ("VH", ("WH", "ZH"))):
    f = VHFit([chW, chZ], use); data = f.mu(np.zeros(f.npar()), 1.0, 1.0); base = f.prof(data, 1.0, 1.0)
    q = {float(l): max(f.prof(data, l*KZ, KZ)-base, 0.0) for l in lamg}; res["curves"][lab] = dict(Z_lambda_m1=float(np.sqrt(q[-1.0])), Z_lambda_0=float(np.sqrt(q[0.0])), Z_lambda_neg=float(np.sqrt(min(v for l, v in q.items() if l <= 0.0))), lam=list(q.keys()), q=list(q.values()))
    kWg = np.arange(-2.0, 3.01, 0.5); kZg = np.arange(0.25, 2.01, 0.25); res["maps"][lab] = dict(kW=[float(x) for x in kWg], kZ=[float(x) for x in kZg], q=[[float(max(f.prof(data, a, b)-base, 0.0)) for b in kZg] for a in kWg])
os.makedirs(f"{WH}/work/stat", exist_ok=True); json.dump(res, open(f"{WH}/work/stat/couplings_vh{TAG}.json", "w"), indent=1, default=float)
print(res["convention"], {k: (round(v["Z_lambda_m1"], 2), round(v["Z_lambda_neg"], 2)) for k, v in res["curves"].items()}, res["zh_yields"], res["wh_zhjj_in_whSR_SM_events"], res["wh_signal_SM_events"])
