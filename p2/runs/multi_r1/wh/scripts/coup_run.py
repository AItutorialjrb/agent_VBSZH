#!/usr/bin/env python3
"""Couplings (07/08 block): lambda_WZ = kappa_W/kappa_Z and (kappa_W, kappa_Z) from the direct coupling samples (K_EW_WHjj_*, 8 CP-even points), expected only (Asimov at the SM point).
 * selection: cut-based primary (mjj>600, |deta|>4.0, pT(gg)>75, MET>30, pT(l)>25) and |m_gg-125|<3.5; sample yields = production weights x k (BR(H->gamma gamma) at its SM value inside k).
 * signal yield per bin: per-bin quadratic Y_i(kW,kZ) = (alpha_i kW^2 + beta_i kW kZ + gamma_i kZ^2) from the 8 points (weighted least squares), x R_BR(kW,kZ) (analytic H->gamma gamma BR and total-width kappa dependence, switch --no-br);
   leave-one-out closure per bin and in total.
 * binning: candidate variables mjj / pT(gg) / mT(W gg) (4 bins each, fixed beforehand) chosen by the expected Asimov exclusion of lambda=-1 (stat-only, MC backgrounds), then frozen.
 * fit: Poisson per bin; nuisances (Gaussian): per-class background normalisation (width = (high-low)/(2 nominal) of the 05a VBS class bounds), signal theory +-5 %, lumi 2.5 % (assumption), Barlow-Beeston-lite per bin.
 * outputs: q(lambda) expected exclusion curves, significance of lambda<0 (= q(0), the closest point of the negative range) and of lambda=-1, 2D (kW,kZ) map, D36 scans (fake photons, non-prompt leptons)."""
import sys, os, json, numpy as np
from scipy.optimize import minimize
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from stat_lib import WH, GROUPS, hist, load, selmask, scale_unc, SUF
NOBR = "--no-br" in sys.argv; KZNEG = "--kz-neg" in sys.argv   # sign convention: lambda = kW/kZ tested at kZ = -1 (kW = -lambda): the yield is even under (kW,kZ)->(-kW,-kZ), only R_BR differs (convention-independent treatment of the sign, D46)
LUM = float(sys.argv[sys.argv.index("--lumi")+1]) if "--lumi" in sys.argv else 500.0; TAG = ("_nobr" if NOBR else "") + ("_kzneg" if KZNEG else "") + ("" if LUM == 500.0 else f"_L{int(LUM)}") + SUF
t, meta, Y = load(); K = dict(np.load(f"{WH}/work/sel/table_K.npz")); Km = json.load(open(f"{WH}/work/sel/table_K_meta.json"))
PTS = {"K_EW_WHjj_lam_m100": (-1.0, 1.0), "K_EW_WHjj_lam_m050": (-0.5, 1.0), "K_EW_WHjj_lam_p000": (0.0, 1.0), "K_EW_WHjj_lam_p050": (0.5, 1.0), "K_EW_WHjj_lam_p100": (1.0, 1.0), "K_EW_WHjj_lam_p150": (1.5, 1.0),
       "K_EW_WHjj_kap_W15_Z075": (1.5, 0.75), "K_EW_WHjj_kap_W05_Z15": (0.5, 1.5)}
# H->gamma gamma kappa dependence: |A_gg|^2 with A_W = -8.32 kW, A_t = +1.84 (kt=1) (F_W(tau_W=0.604), F_t(tau_t=0.131) at mH = 125, verified numerically here), width Sum BR_i kappa_i^2 (YR4 BRs, mH=125; kb=kt=ktau=kc=1)
BRSM = dict(bb=0.5824, WW=0.2137, gg=0.0818, tautau=0.0627, cc=0.0289, ZZ=0.0264, gamgam=0.00227, Zgam=0.00154, mumu=0.00022)
def rbr(kW, kZ):
    if NOBR: return 1.0
    ag = (-8.32*kW+1.84)**2/(-8.32+1.84)**2; w = sum(BRSM.values())-BRSM["WW"]-BRSM["ZZ"]-BRSM["gamgam"]; w += BRSM["WW"]*kW**2+BRSM["ZZ"]*kZ**2+BRSM["gamgam"]*ag; w_sm = sum(BRSM.values()); return ag/(w/w_sm)
VARS = {"mjj": [600, 800, 1000, 1500, 1e5], "ptgg": [75, 100, 150, 250, 1e5], "mtwgg": [0, 250, 350, 450, 1e5]}
def kmask(win=True):
    m = (K["mjj"] > 600) & (K["deta"] > 4.0) & (K["ptgg"] > 75) & (K["met"] > 30) & (K["ptl"] > 25)
    return m & (np.abs(K["mgg"]-125) < 3.5) if win else m
def sig_bins(var, edges):
    """per-bin yield (and sumw2) of each point at 500/fb"""
    m = kmask(); out = {}
    for i, s in enumerate(Km["samples"]):
        if s not in PTS: continue
        mm = m & (K["sid"] == i); out[s] = (np.histogram(K[var][mm], bins=edges, weights=K["w"][mm])[0]*LUM/500.0, np.histogram(K[var][mm], bins=edges, weights=K["w"][mm]**2)[0]*(LUM/500.0)**2)
    return out
def quad_cov(sb, loo=None):
    names = [s for s in PTS if s != loo]; A = np.array([[PTS[s][0]**2, PTS[s][0]*PTS[s][1], PTS[s][1]**2] for s in names]); nb = len(sb[names[0]][0]); C = []
    for i in range(nb):
        e = np.array([max(np.sqrt(sb[s][1][i]), 0.02*abs(sb[s][0][i]), 1e-4) for s in names]); W = 1/e; M = A*W[:, None]; C.append(np.linalg.inv(M.T@M))
    return C
def quad_fit(sb, loo=None):
    """weighted LSQ per bin: Y = a kW^2 + b kW kZ + c kZ^2 using all points (or all but `loo`); returns (n_bins,3)"""
    names = [s for s in PTS if s != loo]; A = np.array([[PTS[s][0]**2, PTS[s][0]*PTS[s][1], PTS[s][1]**2] for s in names]); nb = len(sb[names[0]][0]); co = np.zeros((nb, 3))
    for i in range(nb):
        y = np.array([sb[s][0][i] for s in names]); e = np.array([max(np.sqrt(sb[s][1][i]), 0.02*abs(sb[s][0][i]), 1e-4) for s in names]); W = 1/e
        co[i] = np.linalg.lstsq(A*W[:, None], y*W, rcond=None)[0]
    return co
def sig_pred(co, kW, kZ): return np.maximum((co[:, 0]*kW**2+co[:, 1]*kW*kZ+co[:, 2]*kZ**2)*rbr(kW, kZ), 0.0)
def bkg_bins(var, edges, fs=None):
    mw = selmask(t) & (np.abs(t["mgg"]-125) < 3.5); G = {}; fs = fs or {}
    for g in GROUPS:
        if g in ("sig",): continue
        ss, key = GROUPS[g]; sid = [i for i, s in enumerate(meta["samples"]) if s in ss]; m = mw & np.isin(t["sid"], sid); w = t["w"].copy()
        if key == "misid": w = w-t["whf"]
        elif key == "hf": w = t["whf"]
        elif key == "efqcd_ll": m &= t["qcddir"].astype(bool) & (t["ncls1"] == 0)
        elif key == "efqcd_eg": m &= t["qcddir"].astype(bool) & (t["ncls1"] >= 1)
        elif key == "efew": m &= ~t["qcddir"].astype(bool)
        f = fs.get(g, 1.0); G[g] = (np.histogram(t[var][m], bins=edges, weights=w[m])[0]*f*LUM/500.0, np.sqrt(np.histogram(t[var][m], bins=edges, weights=w[m]**2)[0])*f*LUM/500.0)
    return G
CLS = {"prompt_qcd": "prompt_irreducible", "prompt_ew": "prompt_irreducible", "fake1_qcd": "fake_photon_1", "fake1_ew": "fake_photon_1", "fake2": "fake_photon_2", "npl_misid": "nonprompt_lepton", "npl_hf": "nonprompt_lepton",
       "efake_qcd_ll": "lost_lepton_egamma", "efake_qcd_eg": "lost_lepton_egamma", "efake_ew": "lost_lepton_egamma", "ll_qcd": "lost_lepton_egamma", "ll_other": "lost_lepton_egamma", "higgs_other": "other_higgs", "hqcd": "other_higgs", "tau": "tau_feeddown"}
def class_sigma():
    C = Y["regions"]["VBS"]["classes"]; return {c: max((C[c]["high"]-C[c]["low"])/(2*C[c]["nom"]), 0.05) if C[c]["nom"] > 0 else 0.1 for c in set(CLS.values())}
class Fit:
    def __init__(s, co, G, syst=True, bb=True):
        s.co = co; s.G = G; s.sscale = 1.0; s.syst = syst; s.bb = bb; s.classes = sorted(set(CLS.values())); s.sig_c = class_sigma(); s.nb = len(co)
        s.bkg = np.array([sum(G[g][0][i] for g in G) for i in range(s.nb)]); s.bkgc = {c: np.array([sum(G[g][0][i] for g in G if CLS[g] == c) for i in range(s.nb)]) for c in s.classes}
        s.bkgerr = np.sqrt(np.array([sum(G[g][1][i]**2 for g in G) for i in range(s.nb)]))
    def mu_exp(s, th, kW, kZ):
        ncl = len(s.classes); ts = th[ncl] if s.syst else 0.0; tl = th[ncl+1] if s.syst else 0.0; g = th[ncl+2:ncl+2+s.nb] if s.bb else np.zeros(s.nb)
        b = sum(s.bkgc[c]*(1+s.sig_c[c]*th[j]) for j, c in enumerate(s.classes)) if s.syst else s.bkg.copy()
        sg = sig_pred(s.co, kW, kZ)*(1+0.05*ts)*(1+0.025*tl)*(1.0 if (kW == 1.0 and kZ == 1.0) else s.sscale)
        return sg+b+s.bkgerr*g
    def nll2(s, th, data, kW, kZ):
        nu = np.maximum(s.mu_exp(th, kW, kZ), 1e-9); v = 2*np.sum(nu-data*np.log(nu)+0)
        ncl = len(s.classes); pen = 0.0
        if s.syst: pen += np.sum(th[:ncl]**2)+th[ncl]**2+th[ncl+1]**2
        if s.bb: pen += np.sum(th[ncl+2:ncl+2+s.nb]**2)
        return v+pen
    def prof(s, data, kW, kZ):
        n = len(s.classes)+2+s.nb; th0 = np.zeros(n); r = minimize(s.nll2, th0, args=(data, kW, kZ), method="L-BFGS-B", bounds=[(-4, 4)]*n); return r.fun
def q_curve(fit, data, lam_grid, kZ=(-1.0 if KZNEG else 1.0), ref=None):
    base = fit.prof(data, 1.0, 1.0) if ref is None else ref; return {float(l): max(fit.prof(data, l*kZ, kZ)-base, 0.0) for l in lam_grid}
res = dict(no_br=NOBR, assumptions=dict(signal_theory=0.05, lumi=0.025), points=PTS, rbr={str(k): rbr(*v) for k, v in PTS.items()})
# 1. quadratic closure for a given binning
def closure(var, edges):
    sb = sig_bins(var, edges); co = quad_fit(sb); rows = []
    for s in PTS:
        cl = quad_fit(sb, loo=s); Cv = quad_cov(sb, loo=s); a = np.array([PTS[s][0]**2, PTS[s][0]*PTS[s][1], PTS[s][1]**2]); pred = sig_pred_raw(cl, *PTS[s]); obs = np.array(sb[s][0])
        vp = np.array([a@C@a for C in Cv]); err = np.sqrt(np.array(sb[s][1])+vp)   # predicted variance from the LSQ covariance included (bins independent; total pull treats bins as uncorrelated)
        tot = (pred.sum()-obs.sum())/np.sqrt(np.sum(err**2)+1e-12)
        rows.append(dict(point=s, obs_total=float(obs.sum()), pred_total=float(pred.sum()), pull_total=float(tot), pulls_per_bin=[float((p-o)/max(e, 1e-6)) for p, o, e in zip(pred, obs, err)]))
    return rows
def sig_pred_raw(co, kW, kZ): return np.maximum(co[:, 0]*kW**2+co[:, 1]*kW*kZ+co[:, 2]*kZ**2, 0.0)
lam = np.round(np.arange(-2.0, 3.001, 0.05), 2)
# 2. binning choice by expected exclusion of lambda=-1 (stat + MC bkg only, no nuisances)
choice = {}
for var, edges in VARS.items():
    sb = sig_bins(var, edges); co = quad_fit(sb); G = bkg_bins(var, edges); f = Fit(co, G, syst=False, bb=False); data = sig_pred(co, 1.0, 1.0)+f.bkg
    choice[var] = dict(edges=edges, q_lam_m1=float(q_curve(f, data, [-1.0])[-1.0]), q_lam_0=float(q_curve(f, data, [0.0])[0.0]), closure_total_pulls=[r["pull_total"] for r in closure(var, edges)])
best = max(choice, key=lambda v: choice[v]["q_lam_m1"]); res["binning_choice"] = choice; res["binning_chosen"] = best
var, edges = best, VARS[best]; sb = sig_bins(var, edges); co = quad_fit(sb); G = bkg_bins(var, edges); res["closure_loo"] = closure(var, edges)
res["signal_bins_SM"] = [float(x) for x in sig_pred(co, 1.0, 1.0)]; res["bkg_bins"] = [float(x) for x in sum(G[g][0] for g in G)]
res["quad_coeffs_total"] = [float(co[:, i].sum()) for i in range(3)]
# 3. expected exclusion curves
out = {}
for lab, kw in (("stat_only", dict(syst=False, bb=False)), ("MCstat_only", dict(syst=False, bb=True)), ("reduced_model", dict(syst=True, bb=True))):
    f = Fit(co, G, **kw); data = sig_pred(co, 1.0, 1.0)+f.bkg; qc = q_curve(f, data, lam)
    out[lab] = dict(q=qc, Z_lam_m1=float(np.sqrt(qc[-1.0])), Z_lam_0=float(np.sqrt(qc[0.0])), Z_lambda_lt0=float(np.sqrt(min(qc[l] for l in lam if l < 0 or l == 0.0))))
res["expected_exclusion"] = out
# 3b. closure sensitivity: the per-bin quadratic misses by up to ~3 sigma in single bins at lambda=0/-0.5 (LOO): vary the predicted signal of the TESTED hypothesis by +-30 % (cheap closure systematic; SM Asimov data unchanged)
f = Fit(co, G); data = sig_pred(co, 1.0, 1.0)+f.bkg; base0 = f.prof(data, 1.0, 1.0); cs = {}
for sc_ in (0.7, 1.0, 1.3):
    f.sscale = sc_; cs[str(sc_)] = dict(Z_lam_m1=float(np.sqrt(max(f.prof(data, -1.0*(-1.0 if KZNEG else 1.0), (-1.0 if KZNEG else 1.0))-base0, 0))), Z_lam_0=float(np.sqrt(max(f.prof(data, 0.0, (-1.0 if KZNEG else 1.0))-base0, 0))))   # tested point (lambda*kZ, kZ) in the convention of the run
res["closure_sensitivity_signal_scale_of_tested_hypothesis"] = cs
# 4. 2D map (full)
f = Fit(co, G); data = sig_pred(co, 1.0, 1.0)+f.bkg; base = f.prof(data, 1.0, 1.0); kWg = np.arange(-2.0, 3.01, 0.5); kZg = np.arange(0.25, 2.01, 0.25)
res["map2d"] = dict(kW=[float(x) for x in kWg], kZ=[float(x) for x in kZg], q=[[float(max(f.prof(data, a, b)-base, 0.0)) for b in kZg] for a in kWg])
# 5. D36 scans of the lambda<0 exclusion versus background normalisation
sc = []
for kind in ("fake", "npl"):
    for fct in (0.3, 0.5, 1.0, 2.0, 3.0, 10.0, 30.0, 100.0):
        fs = {"fake1_qcd": fct, "fake1_ew": fct, "fake2": fct*fct} if kind == "fake" else {"npl_misid": fct, "npl_hf": fct}
        Gs = bkg_bins(var, edges, fs); fs_ = Fit(co, Gs); d = sig_pred(co, 1.0, 1.0)+fs_.bkg; qc = q_curve(fs_, d, [-1.0, 0.0, 0.5])
        sc.append(dict(kind=kind, f=fct, Z_lam_m1=float(np.sqrt(qc[-1.0])), Z_lam_0=float(np.sqrt(qc[0.0])), Z_lam_p05=float(np.sqrt(qc[0.5])), beyond_D36=fct > 3.0))
res["d36_lambda"] = sc
# 6. no-BR variant of lambda<0 numbers is produced by running with --no-br (TAG)
os.makedirs(f"{WH}/work/stat", exist_ok=True); json.dump(res, open(f"{WH}/work/stat/couplings{TAG}.json", "w"), indent=1, default=float)
print("chosen", best, json.dumps({k: choice[k]["q_lam_m1"] for k in choice}), "Z excl:", {k: (round(v["Z_lam_m1"], 2), round(v["Z_lam_0"], 2)) for k, v in out.items()})
