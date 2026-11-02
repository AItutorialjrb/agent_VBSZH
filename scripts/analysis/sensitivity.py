#!/usr/bin/env python3
"""Phase-05 pilot sensitivity: normalisation, background model, cut optimisation on EXPECTED quantities, cutflows,
Asimov significances and expected CLs limits.  Inputs: work/m7_analysis/*.npz from scripts/analysis/ntuple.py.
Usage: python3 -P sensitivity.py <npz_dir> <out.json> [registry_override.json]
All numbers written to <out.json>; the report (reports/05_pilot_sensitivity.md) quotes them.

Estimation methods (per background, chosen automatically and recorded):
  direct      : sum of weights after all cuts; continuum samples use the m_gg-window factorisation
                N_win = N(all cuts, 105<m_gg<165) * f_win, f_win from an exponential MLE fit of that sample's m_gg
                at loose selection (smooth-shape assumption).  Resonant samples count the window directly.
  factorised  : if the direct raw count < 10:  N(all cuts except mjj/deta/zeppenfeld) * eps(VBS-jet cuts | loose).
  ff          : fake-factor rows (ntuple ff1/ff2) with f_flat=1e-3 nominal; band f=5e-4..2e-3; pT-dependent variant.
  proxy       : prompt Zgg+jj (no jj reco sample yet): sigma_est * L * eps_LG(llaa_0j reco) * eps_J(proxy jets).
"""
import sys, json, glob, numpy as np
from math import lgamma
from scipy import stats, optimize

D, OUT = sys.argv[1], sys.argv[2]
MZ, BGG, ZF = 91.1876, 0.002270, 0.9783
P = "/eos/home-r/rjiang/vbs_zh_codex_starter"

def tier1_sigma(s):
    J = [json.load(open(f)) for f in glob.glob(f"{P}/production/v1/{s}/*.json")]
    x = np.array([[float(v) for v in j["lhe_init_xsec_pb_err_pb_max_lprup"].split()[:2]] for j in J])
    w = 1/x[:, 1]**2
    return 1e3*(x[:, 0]*w).sum()/w.sum(), 1e3/np.sqrt(w.sum()), len(J)

sEW, eEW, nEW = tier1_sigma("ew_zhjj_zll"); sQCD, eQCD, nQCD = tier1_sigma("qcd_zhjj_zll")
# ----------------------------------------------------------------------------------------------------------------
# Registry: id -> (npz, sigma_fb, k-factor(BR), role, kind, syst_class, source)
#   kind: res (resonant H->gg), cont (continuum, direct), ff1/ff2 (fake factor), proxy
REG = {
 "S_EW_ZHjj":   dict(npz="S_EW_ZHjj", sig=sEW, k=ZF*BGG, kind="res", syst="other", src=f"Tier-1 v1, {nEW} jobs, LHE-init sigma (weighted mean)"),
 "H_QCD_ZHjj":  dict(npz="H_QCD_ZHjj", sig=sQCD, k=ZF*BGG, kind="res", syst="other", src=f"Tier-1 v1, {nQCD} jobs"),
 "H_ttH":       dict(npz="ttH_dilep", sig=17.98, k=BGG, kind="res", syst="other", src="work/m5/ttH_dilep LHE (500 ev) + PY8/Delphes slim_v1"),
 "B_QCD_Zaajj": dict(kind="proxy", syst="other", sig=None, src="ESTIMATE: sigma(llaa_0j)*sigma(llajj)/sigma(lla_0j); eps_LG llaa_0j reco; eps_J llajj_pilot"),
 "B_EW_Zaajj":  dict(kind="proxy", syst="other", sig=None, src="ESTIMATE: ref. EW/QCD Zaa ratio x sigma(llaa_0j); eps_LG llaa_0j; eps_J EW ZHjj"),
 "F_QCD_Za":    dict(npz="llajj_pilot", sig=1775.0, k=1.0, kind="ff1", syst="fake", src="llajj_pilot 5000 ev (Za+2j fixed order)"),
 "F_EW_Za":     dict(npz="ew_llajj", sig=35.6, k=1.0, kind="ff1", syst="fake", src="work/m5/ew_llajj LHE 200 ev"),
 "T_tta":       dict(npz="tta_dilep", sig=85.67, k=1.0, kind="ff1", syst="fake", src="work/m5/tta_dilep LHE 200 ev"),
 "T_tWa":       dict(npz="twa_dilep", sig=13.07, k=1.0, kind="ff1", syst="fake", src="work/m5/twa_dilep LHE 200 ev"),
 "F_Zjets":     dict(npz="zll_jj_pilot", sig=211500.0, k=1.0, kind="ff2", syst="fake", oom=True, src="zll_jj_pilot 5000 ev (Z+2j); order-of-magnitude only"),
 "T_tt":        dict(npz="tt_dilep", sig=23470.0, k=1.0, kind="ff2", syst="fake", oom=True, src="work/m5/tt_dilep LHE 200 ev"),
 "T_ttaa":      dict(npz="ttaa_dilep", sig=0.0949, k=1.0, kind="cont", syst="other", src="work/m5/ttaa_dilep LHE 200 ev"),
}
if len(sys.argv) > 3:
    for k, v in json.load(open(sys.argv[3])).items(): REG.setdefault(k, {}).update(v)
SIG_QCD_ZAAJJ = 2.893 * 1775.0 / 10080.0          # fb, 90<m_aa<190, ptj>20 (cross-check: x sigma(ZHjj)/sigma(ZH) = 0.61 fb)
SIG_EW_ZAAJJ = 2.893 * (0.263 / 23.0) * 1.4       # fb, reference EW/QCD Zaa ratio x (QCD 0-2j ~ 1.4 x 0j); range 0.010-0.045
ALT_SIG = {"B_QCD_Zaajj": (2.893*sQCD/48.45, "x sigma(QCD ZHjj)/sigma(ZH 0j)"), "B_EW_Zaajj": (2.893*35.6/10080, "x sigma(EW llajj)/sigma(lla_0j)")}

def load(n):
    d = np.load(f"{D}/{n}.npz"); return {k: d[k] for k in d.files}
DATA = {}
for sid, r in REG.items():
    if r["kind"] == "proxy": continue
    nm = r["npz"] + ("_ff1" if r["kind"] == "ff1" else "_ff2" if r["kind"] == "ff2" else "")
    d = load(nm); d0 = load(r["npz"]); N = int(d0["nev_total"])
    d["w"] = r["sig"]*r["k"]/N * d["wf_flat"]          # events per 1 fb^-1 (scaled by L later)
    d["w_pt"] = r["sig"]*r["k"]/N * d["wf_pt"]
    r["N"] = N; r["w_evt_fb"] = r["sig"]*r["k"]/N
    DATA[sid] = d
LLAA = load("llaa_0j"); LLAJ = load("llajj_pilot")
# ------------------------------------------------------------------ m_gg resolution from the Delphes EW signal
m = DATA["S_EW_ZHjj"]["mgg"]; m = m[np.isfinite(m) & (m > 110) & (m < 140)]
h, e = np.histogram(m, bins=60, range=(110, 140)); c = 0.5*(e[1:] + e[:-1]); cw = (c > 121) & (c < 129)
(pA, pMU, pSIG), cov = optimize.curve_fit(lambda x, a, mu, s: a*np.exp(-0.5*((x-mu)/s)**2), c[cw], h[cw], p0=[h.max(), 125, 2])
q = np.sort(m); n = len(q); kk = int(0.683*n); wd = q[kk:] - q[:n-kk]; i = wd.argmin()
RES = dict(mu=pMU, sigma_core=abs(pSIG), sigma_core_err=float(np.sqrt(cov[2, 2])), sigma_eff=float(wd[i]/2))
MU, SIG = RES["mu"], RES["sigma_core"]

# ------------------------------------------------------------------ selection
BASE = dict(zwin=(70., 120.), mllgg=100., g1=20., g2=20., ratio=False, bveto=False, zep_gg=99., zep_Z=99.,
            mjj=700., deta=2.0, wk=2.0)
def zmask(d, c):
    lo, hi = (c["zwin"] if isinstance(c["zwin"], tuple) else (MZ - c["zwin"], MZ + c["zwin"]))
    return (d["mll"] > lo) & (d["mll"] < hi)
def masks(d, c, proxy_single_photon=False):
    with np.errstate(invalid="ignore"):
        pre = np.isfinite(d["mll"]) & (d["ng"] >= 2) & (d["nj"] >= 2)
        lg = zmask(d, c) & (d["mllgg"] > c["mllgg"]) & (d["g1pt"] > c["g1"]) & (d["g2pt"] > c["g2"])
        if c["ratio"]: lg &= (d["g1pt"]/d["mgg"] > 1/3) & (d["g2pt"]/d["mgg"] > 1/4)
        jb = np.ones_like(pre) if not c["bveto"] else (d["nb"] == 0)
        vbs = (d["mjj"] > c["mjj"]) & (d["detajj"] > c["deta"]) & (d["zep_gg"] < c["zep_gg"]) & (d["zep_Z"] < c["zep_Z"])
    return pre, lg, jb, vbs
def window(c, scale=1.0): return MU - c["wk"]*SIG*scale, MU + c["wk"]*SIG*scale
WIDE = (105., 165.)

def fwin(mgg, w, c, scale=1.0):
    """fraction of a smooth (exponential, unbinned weighted MLE) m_gg spectrum inside the window, relative to WIDE"""
    sel = np.isfinite(mgg) & (mgg > WIDE[0]) & (mgg < WIDE[1]); x, ww = mgg[sel] - WIDE[0], w[sel]; L = WIDE[1] - WIDE[0]
    lo, hi = [v - WIDE[0] for v in window(c, scale)]
    if len(x) < 5: return (hi - lo)/L, len(x), 0.0
    def nll(lam):
        if abs(lam) < 1e-6: return (ww.sum()*np.log(L))
        return -(ww*(np.log(abs(lam)) - lam*x)).sum() + ww.sum()*np.log(abs(1 - np.exp(-lam*L)))
    lam = optimize.minimize_scalar(nll, bounds=(-0.2, 0.2), method="bounded").x
    F = (lambda a, b: (b - a)/L) if abs(lam) < 1e-6 else (lambda a, b: (np.exp(-lam*a) - np.exp(-lam*b))/(1 - np.exp(-lam*L)))
    return F(lo, hi), int(sel.sum()), float(lam)

def ywe(d, m, wkey="w"):
    w = d[wkey][m]; return w.sum(), np.sqrt((w**2).sum()), len(np.unique(d["evt"][m]))

def level2(sid, d, c, mg, wkey, resonant):
    """fully factorised estimate from the loose preselection (OSSF any mass + 2 photons + 2 jets): y_P * prod_i eps_i,
    each eps_i measured independently w.r.t. the preselection; zero-count cuts use the Jeffreys value (0.5/(n_P+1)).
    Assumes independence of the cuts -> 100% uncertainty assigned."""
    pre, lg, jb, vbs = masks(d, c)
    yP, _, nP = ywe(d, pre, wkey)
    if nP == 0: return 0.0, 0.0, 0, "NO MC SUPPORT (presel empty)", dict(n_P=0)
    w = d[wkey]; eps = {}
    lo, hi = window(c)
    with np.errstate(invalid="ignore"):
        cuts = {"zwin": zmask(d, c), "lg": masks(d, c)[1] | ~zmask(d, c) & False, "bveto": jb, "vbs": vbs}
        cuts["lg"] = (d["mllgg"] > c["mllgg"]) & (d["g1pt"] > c["g1"]) & (d["g2pt"] > c["g2"])
        if c["ratio"]: cuts["lg"] &= (d["g1pt"]/d["mgg"] > 1/3) & (d["g2pt"]/d["mgg"] > 1/4)
        cuts["window"] = (mg > lo) & (mg < hi)
    for k, m in cuts.items():
        n = len(np.unique(d["evt"][pre & m]))
        eps[k] = (w[pre & m].sum()/w[pre].sum()) if n > 0 else 0.5/(nP + 1)
        eps[k + "_n"] = n
    y = yP*np.prod([eps[k] for k in cuts])
    return y, y, int(nP), "fully-factorised (100% unc.)", dict(n_P=nP, **{k: float(v) for k, v in eps.items()})

def estimate(sid, c, scale=1.0, wkey="w"):
    """expected yield per fb^-1, MC-stat error, raw MC count, method, details"""
    r = REG[sid]
    if r["kind"] == "proxy":
        d = LLAA; N = int(d["nev_total"])
        with np.errstate(invalid="ignore"):
            lgm = (d["ng"] >= 2) & np.isfinite(d["mll"]) & masks(d, c)[1]
        f, nfw, _ = fwin(d["mgg"], np.ones(len(d["mgg"])), dict(c, wk=c["wk"]), scale)
        nlg = (lgm & (d["mgg"] > WIDE[0]) & (d["mgg"] < WIDE[1])).sum()
        eLG = nlg/N*f
        J = LLAJ if sid == "B_QCD_Zaajj" else DATA["S_EW_ZHjj"]
        with np.errstate(invalid="ignore"):
            if sid == "B_QCD_Zaajj":   # single real photon in Za+jj: zeppenfeld of the photon direction as proxy for gg
                den = np.isfinite(J["mll"]) & zmask(J, c) & (J["ng"] >= 1)
                eta_g = J["g"][:, 0, 1]; j1, j2 = J["j"][:, 0, 1], J["j"][:, 1, 1]
                zg = np.abs(eta_g - 0.5*(j1 + j2))/np.abs(j1 - j2)
                num = den & (J["nj"] >= 2) & (J["mjj"] > c["mjj"]) & (J["detajj"] > c["deta"]) & (zg < c["zep_gg"]) & (J["zep_Z"] < c["zep_Z"])
            else:
                den = np.isfinite(J["mll"]) & zmask(J, c) & (J["ng"] >= 2)
                num = den & (J["nj"] >= 2) & masks(J, c)[3]
            if c["bveto"]: num &= (J["nb"] == 0)
        eJ = num.sum()/max(den.sum(), 1)
        sig = SIG_QCD_ZAAJJ if sid == "B_QCD_Zaajj" else SIG_EW_ZAAJJ
        y = sig*eLG*eJ
        rel = np.sqrt(1/max(nlg, 1) + 1/max(num.sum(), 1))
        return y, y*rel, int(min(nlg, num.sum())), "proxy", dict(n_LG=int(nlg), n_J=int(num.sum()), eps_LG=eLG, eps_J=eJ, f_win=f, sigma_fb=sig)
    d = DATA[sid]
    pre, lg, jb, vbs = masks(d, c)
    lo, hi = window(c, scale)
    if sid in ("S_EW_ZHjj", "H_QCD_ZHjj", "H_ttH") and scale != 1.0:   # resolution variation for resonant samples
        mg = MU + (d["mgg"] - MU)*scale
    else:
        mg = d["mgg"]
    full = pre & lg & jb & vbs
    if r["kind"] == "res":
        m1 = full & (mg > lo) & (mg < hi)
        y, e, n = ywe(d, m1, wkey)
        if n >= 10: return y, e, n, "direct", {}
        mA = pre & lg & jb & (mg > lo) & (mg < hi); yA, eA, nA = ywe(d, mA, wkey)
        mL = pre & zmask(d, c); yL, _, nL = ywe(d, mL, wkey); yV, _, nV = ywe(d, mL & vbs, wkey)
        if nA < 3 or nV < 3: return level2(sid, d, c, mg, wkey, True)
        eV = yV/yL if yL > 0 else 0.0
        y = yA*eV; rel = np.sqrt((eA/yA)**2 + 1/max(nV, 1)) if yA > 0 else 1.0
        return y, y*rel, int(min(nA, nV)), "factorised", dict(n_A=nA, n_V=nV, eps_V=eV, direct_raw=n)
    # continuum / fake-factor: window factorisation
    loose = pre & zmask(d, c)
    f, nf, lam = fwin(d["mgg"][loose], d[wkey][loose], c, scale)
    mW = full & (d["mgg"] > WIDE[0]) & (d["mgg"] < WIDE[1])
    y, e, n = ywe(d, mW, wkey)
    meth = "ff" if r["kind"] in ("ff1", "ff2") else "direct"
    if n >= 10:
        return y*f, e*f, n, meth + "+mgg-fact", dict(f_win=f, n_fit=nf, lam=lam)
    mA = pre & lg & jb & (d["mgg"] > WIDE[0]) & (d["mgg"] < WIDE[1]); yA, eA, nA = ywe(d, mA, wkey)
    mL = loose; yL, _, nL = ywe(d, mL, wkey); yV, _, nV = ywe(d, mL & vbs, wkey)
    if nA < 3 or nV < 3:
        y2, e2, n2, m2, det2 = level2(sid, d, c, d["mgg"], wkey, False)
        # continuum: replace the direct window cut by the smooth-fit fraction (relative to the preselection)
        if n2 > 0:
            pre_ = masks(d, c)[0]; inW = pre_ & (d["mgg"] > WIDE[0]) & (d["mgg"] < WIDE[1])
            fw = (d[wkey][inW].sum()/d[wkey][pre_].sum())*f if d[wkey][pre_].sum() > 0 else 0
            y2 = y2/det2["window"]*fw if det2["window"] > 0 else y2; det2["window_fit"] = fw
        return y2, y2, n2, meth + "+" + m2, dict(det2, f_win=f)
    eV = yV/yL if yL > 0 else 0.0; meth_v = "measured"
    y = yA*eV*f; rel = np.sqrt((eA/yA)**2 + 1/max(nV, 1)) if yA > 0 else 1.0
    return y, y*rel, int(min(nA, max(nV, 0))), meth + "+factorised", dict(f_win=f, n_A=nA, n_V=nV, eps_V=eV, eps_V_method=meth_v, direct_raw=n)

SYST = {"fake": 0.50, "other": 0.10}
def totals(c, L, sigdef="a", scale=1.0, fake_syst=0.5, wkey="w", proxy_syst=None, incl_oom=False):
    s = 0.0; b = 0.0; var = 0.0; comp = {}
    for sid in REG:
        y, e, n, meth, det = estimate(sid, c, scale, wkey if REG[sid]["kind"] in ("ff1", "ff2") else "w")
        y, e = y*L, e*L
        comp[sid] = dict(y=y, mcstat=e, raw=n, method=meth, **{k: (float(v) if isinstance(v, (float, np.floating)) else v) for k, v in det.items()})
        is_sig = sid == "S_EW_ZHjj" or (sigdef == "b" and sid == "H_QCD_ZHjj")
        if is_sig: s += y; continue
        if REG[sid].get("oom") and not incl_oom: continue   # double-fake classes: order-of-magnitude only (reference: neglected)
        rs = fake_syst if REG[sid]["syst"] == "fake" else SYST["other"]
        if proxy_syst is not None and REG[sid]["kind"] == "proxy": rs = proxy_syst
        b += y; var += (rs*y)**2 + e**2
    return s, b, np.sqrt(var), comp

def z_stat(s, b): return np.sqrt(2*((s + b)*np.log(1 + s/b) - s)) if b > 0 and s > 0 else 0.0
def z_syst(s, b, sb):
    if sb <= 0: return z_stat(s, b)
    t1 = (s + b)*np.log((s + b)*(b + sb**2)/(b**2 + (s + b)*sb**2)); t2 = b**2/sb**2*np.log(1 + sb**2*s/(b*(b + sb**2)))
    return np.sqrt(max(2*(t1 - t2), 0))

def cls_limit(s, b, sb, alpha=0.05):
    """median expected 95% CL upper limit on mu (CLs, Poisson counting, b marginalised over a log-normal of width sb/b)"""
    if s <= 0: return np.inf
    rel = sb/b if b > 0 else 0
    if rel > 0:
        gx, gw = np.polynomial.hermite_e.hermegauss(40); gw = gw/gw.sum()
        bs = b*np.exp(np.sqrt(np.log(1 + rel**2))*gx - 0.5*np.log(1 + rel**2))
    else: bs, gw = np.array([b]), np.array([1.0])
    cdf = lambda n, mu: (gw*stats.poisson.cdf(n, mu*s + bs)).sum()
    # median of the marginal background-only count distribution
    nn = np.arange(0, int(b + 10*np.sqrt(b + 1) + 10*sb + 20)); cb = np.array([cdf(k, 0) for k in nn])
    nmed = nn[np.searchsorted(cb, 0.5)]
    f = lambda mu: cdf(nmed, mu)/cdf(nmed, 0) - alpha
    hi = 1.0
    while f(hi) > 0: hi *= 2
    return optimize.brentq(f, 0, hi), int(nmed)

# ------------------------------------------------------------------ optimisation (expected quantities only)
GRID = dict(wk=[1.5, 2.0], ratio=[False, True], zwin=[(70., 120.), 25., 20., 15., 10.], zep_gg=[99., 1.0, 0.7, 0.5],
            zep_Z=[99., 1.0, 0.7, 0.5], mllgg=[100., 200., 250.], bveto=[False, True], g1=[20., 25., 30., 35.], g2=[20., 25.])
MJJ = [200., 300., 400., 500., 600., 700., 800., 1000.]; DETA = [0., 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
LOPT = 500.0
def fom(c):
    s, b, sb, _ = totals(c, LOPT); return z_syst(s, b, sb), s
def pick(cands):  # plateau rule: among Z >= 0.97 Zmax take the largest signal (loosest) point
    zmax = max(z for z, s, _ in cands); ok = [(s, -i, v) for i, (z, s, v) in enumerate(cands) if z >= 0.97*zmax]
    return max(ok)[2]
c = dict(BASE); log = []
for it in range(3):
    old = dict(c)
    cands = [(*fom(dict(c, mjj=a, deta=b2)), (a, b2)) for a in MJJ for b2 in DETA]
    c["mjj"], c["deta"] = pick(cands); log.append(("mjj,deta", c["mjj"], c["deta"], max(x[0] for x in cands)))
    for k, vals in GRID.items():
        cands = [(*fom(dict(c, **{k: v})), v) for v in vals]
        c[k] = pick(cands); log.append((k, c[k], max(x[0] for x in cands)))
    if c == old: break
OPT = c
# 2D scan table (for the report)
SCAN = {f"{a:.0f},{b2:.1f}": fom(dict(OPT, mjj=a, deta=b2))[0] for a in MJJ for b2 in DETA}

# ------------------------------------------------------------------ results
def cutflow(c, L=500.0):
    steps = [("presel: OSSF + 2gamma(20) + 2jets(25)", dict(zwin=(0., 1e9), mllgg=0., g1=20., g2=20., ratio=False, bveto=False, zep_gg=99., zep_Z=99., mjj=0., deta=0., wk=99.)),]
    cc = dict(steps[0][1])
    for lab, upd in (("Z window", dict(zwin=c["zwin"])), ("m_llgg", dict(mllgg=c["mllgg"])),
                     ("photon pT / pT/m", dict(g1=c["g1"], g2=c["g2"], ratio=c["ratio"])), ("b-veto", dict(bveto=c["bveto"])),
                     ("Zeppenfeld", dict(zep_gg=c["zep_gg"], zep_Z=c["zep_Z"])), ("mjj, |deta_jj|", dict(mjj=c["mjj"], deta=c["deta"])),
                     (f"m_gg window +-{c['wk']} sigma", dict(wk=c["wk"]))):
        cc = dict(cc, **upd); steps.append((lab, dict(cc)))
    rows = []
    for lab, cs in steps:
        row = {"step": lab}
        for sid in REG:
            if REG[sid]["kind"] == "proxy":
                y, e, n, meth, det = estimate(sid, dict(cs, wk=min(cs["wk"], 30.)))
            elif cs["wk"] > 50:   # before the window: plain sums (no window factorisation), WIDE range not imposed
                d = DATA[sid]; pre, lg, jb, vbs = masks(d, cs); mm = pre & lg & jb & vbs
                y, e, n = ywe(d, mm); meth = "direct" if REG[sid]["kind"] not in ("ff1", "ff2") else "ff"
            else:
                y, e, n, meth, _ = estimate(sid, cs)
            row[sid] = dict(y=y*L, e=e*L, raw=int(n), method=meth)
        rows.append(row)
    return rows

RESULTS = {}
for L in (500., 1000., 3000.):
    for sd in ("a", "b"):
        s, b, sb, comp = totals(OPT, L, sd)
        bstat = np.sqrt(sum(v["mcstat"]**2 for k, v in comp.items() if not (k == "S_EW_ZHjj" or (sd == "b" and k == "H_QCD_ZHjj"))))
        lim, nmed = cls_limit(s, b, sb)
        lim0, _ = cls_limit(s, b, 0.0)
        RESULTS[f"{int(L)}_{sd}"] = dict(L=L, sigdef=sd, s=s, b=b, sigma_b=sb, b_mcstat=bstat, Z_stat=z_stat(s, b), Z_syst=z_syst(s, b, sb),
                                          mu95=lim, mu95_statonly=lim0, n_median=nmed, comp=comp)
# robustness / dependence studies at 500 fb^-1, definition (a)
ROB = {}
for lab, kw in (("nominal", {}), ("fake syst 25%", dict(fake_syst=0.25)), ("fake syst 100%", dict(fake_syst=1.0)),
                ("proxy Zgg syst 50%", dict(proxy_syst=0.5)), ("m_gg resolution x0.75", dict(scale=0.75)),
                ("m_gg resolution x1.25", dict(scale=1.25)), ("fake rate pT-dependent", dict(wkey="w_pt")), ("incl. Z+jets & tt (2 fakes)", dict(incl_oom=True))):
    s, b, sb, comp = totals(OPT, 500., "a", **kw); ROB[lab] = dict(s=s, b=b, sb=sb, Z_stat=z_stat(s, b), Z_syst=z_syst(s, b, sb))
for lab, fs in (("f=5e-4", 0.5), ("f=2e-3", 2.0)):
    s, b, sb, comp = totals(OPT, 500., "a")
    bf = sum(v["y"] for k, v in comp.items() if REG[k]["kind"] in ("ff1", "ff2") and k != "S_EW_ZHjj")
    pw = {"ff1": fs, "ff2": fs**2}
    b2 = b + sum(v["y"]*(pw[REG[k]["kind"]] - 1) for k, v in comp.items() if REG[k]["kind"] in ("ff1", "ff2") and not REG[k].get("oom"))
    ROB[lab] = dict(s=s, b=b2, Z_stat=z_stat(s, b2))
# reference-like selection (mjj>700, |deta|>2.0, 70<mll<120, mllgg>100, +-2 sigma window) for comparison
s, b, sb, comp = totals(BASE, 500., "a"); ROB["reference-like cuts"] = dict(s=s, b=b, sb=sb, Z_stat=z_stat(s, b), Z_syst=z_syst(s, b, sb),
                                                                          comp={k: v["y"] for k, v in comp.items()})
# FF vs reference Delphes-fake rate cross-check: fraction of Za+2j events passing the reference initial selection
d = DATA["F_QCD_Za"]; pre = np.isfinite(d["mll"]) & (d["ng"] >= 2) & (d["nj"] >= 2)
FFX = dict(ff_fraction_initial_sel=float(d["wf_flat"][pre].sum()/REG["F_QCD_Za"]["N"]), reference_direct_fraction=1.0e-4,
           direct_delphes_presel_raw=int((np.isfinite(LLAJ["mll"]) & (LLAJ["ng"] >= 2) & (LLAJ["nj"] >= 2)).sum()),
           direct_delphes_2gamma_noOSSF_raw=int((~np.isfinite(LLAJ["mll"]) & (LLAJ["ng"] >= 2)).sum()),
           N=int(LLAJ["nev_total"]))
for lab, (gname, val) in (("EW Zaajj sigma low (0.010 fb)", ("SIG_EW_ZAAJJ", ALT_SIG["B_EW_Zaajj"][0])),
                          ("QCD Zaajj sigma alt (ZH ratio, 0.61 fb)", ("SIG_QCD_ZAAJJ", ALT_SIG["B_QCD_Zaajj"][0]))):
    keep = globals()[gname]; globals()[gname] = val
    s, b, sb, _ = totals(OPT, 500., "a"); ROB[lab] = dict(s=s, b=b, sb=sb, Z_stat=z_stat(s, b), Z_syst=z_syst(s, b, sb))
    globals()[gname] = keep

out = dict(resolution=RES, optimum={k: (list(v) if isinstance(v, tuple) else v) for k, v in OPT.items()}, opt_log=log, scan_mjj_deta=SCAN,
           results=RESULTS, robustness=ROB, cutflow=cutflow(OPT), cutflow_reference=cutflow(BASE), ff_crosscheck=FFX,
           registry={k: {kk: vv for kk, vv in v.items()} for k, v in REG.items()},
           sigma_proxy=dict(QCD_Zaajj=SIG_QCD_ZAAJJ, EW_Zaajj=SIG_EW_ZAAJJ, alt={k: v[0] for k, v in ALT_SIG.items()}),
           tier1_sigma=dict(EW=(sEW, eEW, nEW), QCD=(sQCD, eQCD, nQCD)))
json.dump(out, open(OUT, "w"), indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
print(json.dumps({k: out[k] for k in ("resolution", "optimum")}, default=str))
for k, v in RESULTS.items():
    print(k, "s=%.4f b=%.3f sb=%.3f Zstat=%.3f Zsyst=%.3f mu95=%.1f" % (v["s"], v["b"], v["sigma_b"], v["Z_stat"], v["Z_syst"], v["mu95"]))
for k, v in RESULTS["500_a"]["comp"].items(): print("  %-12s y=%.4f mc=%.4f raw=%d %s" % (k, v["y"], v["mcstat"], v["raw"], v["method"]))
for k, v in ROB.items(): print("ROB", k, {kk: round(vv, 4) for kk, vv in v.items() if isinstance(vv, float)})
