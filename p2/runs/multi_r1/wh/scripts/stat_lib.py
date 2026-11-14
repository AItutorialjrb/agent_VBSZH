#!/usr/bin/env python3
"""Statistics library (07): builds the m_gg histograms of the cut-based PRIMARY selection (05_selection.md: mjj>600, |deta|>4.0, pT(gg)>75, rest baseline) per process group from work/sel/table.npz,
the pyhf model (binned profile likelihood, 40 bins of 2 GeV in 100-180, Barlow-Beeston-lite staterror 'mcstat', nuisances pre-declared in 05a v2.1 sec. 'nuisance list' and 05 addendum), and
helpers for Eq. 1, exact-Poisson CLs and expected profile-likelihood Z / mu95 on Asimov datasets (expected only; no data exist)."""
import json, warnings, numpy as np, pyhf
warnings.filterwarnings("ignore")
import os
WH = os.environ.get("STAT_WH", "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh")
EDGES = np.arange(100.0, 180.01, 2.0); NB = len(EDGES)-1
CUTS = dict(mjj=600.0, deta=4.0, ptgg=75.0)
ASSUME = dict(lumi=0.025, photon_eff_per_photon=0.02, lepton_eff=0.01, phscale=0.005, phres=0.10)   # ASSUMPTIONS (no data, Delphes has no scale factors): labelled as such in 07
pyhf.set_backend("numpy", pyhf.optimize.scipy_optimizer())
V12 = os.environ.get("STAT_V12") == "1"; V11 = os.environ.get("STAT_V11") == "1" or V12; TABLE = os.environ.get("STAT_TABLE", "table"); YIELDS = os.environ.get("STAT_YIELDS", "yields"); SUF = "_v12" if V12 else ("_v11" if V11 else "")
def load():
    t = dict(np.load(f"{WH}/work/sel/{TABLE}.npz")); meta = json.load(open(f"{WH}/work/sel/{TABLE}_meta.json")); Y = json.load(open(f"{WH}/work/bgmodel/{YIELDS}.json")); return t, meta, Y
GROUPS = {  # name: (samples, extra mask key, weight key)
    "sig": (["S_EW_WHjj"], None), "hqcd": (["H_QCD_WH_mlm"], None), "tau": (["S_EW_WHjj_taunu"], None), "prompt_qcd": (["B_QCD_Waajj_nomjj"], None), "prompt_ew": (["B_EW_Waajj_nomjj", "T_ttaa_1l"], None),
    "fake1_qcd": (["F_QCD_Wajjj_nomjj", "T_tta_1l", "T_tWa_1l"], None), "fake1_ew": (["F_EW_Wajj_nomjj"], None), "fake2": (["F_Wjjjj", "T_ttjj_1l"], None),
    "npl_misid": (["Q_aajjj", "H_VBFH_jj", "H_ggF_jj"], "misid"), "npl_hf": (["Q_aajjj", "H_VBFH_jj", "H_ggF_jj"], "hf"),
    "efake_qcd_ll": ((["F_QCD_llajj_loose"], "ll") if V11 else (["ZH_Zajj_eFake"], "efqcd_ll")), "efake_qcd_eg": ((["F_QCD_llajj_loose"], "eg") if V11 else (["ZH_Zajj_eFake"], "efqcd_eg")), "efake_ew": (["ZH_Zajj_eFake"], "efew"),
    "ll_qcd": (["ZH_Zaajj_QCD_nomjj_lostlep"], None), "ll_other": (["ZH_Zaajj_EW_lostlep", "V_WWa_WH", "V_WZa_WH", "V_ZZa_WH"], None),
    "higgs_other": (["H_ggZH_wh", "H_ZH_tautau_wh", "H_ttH_1l", "H_ttH_dilep_wh", "H_tHq_lep", "H_tHW_1l", "ZH_EW_ZHjj_lostlep", "ZH_QCD_ZHjj_lostlep"], None)}
GROUPS_VH_EXTRA = {"zhjj_ew": (["ZH_EW_ZHjj_lostlep"], None), "zhjj_qcd": (["ZH_QCD_ZHjj_lostlep"], None)}   # VH mode: ZH signal-like samples in the WH SR (lost lepton), scaled by mu_ZH / mu_VH
ALLGROUPS = dict(GROUPS); ALLGROUPS.update(GROUPS_VH_EXTRA)
TAUG_Z = {"efake_qcd_ll", "efake_qcd_eg", "efake_ew", "ll_qcd", "ll_other", "zhjj_ew", "zhjj_qcd"}
TAUG = {"zhjj_ew", "zhjj_qcd", "prompt_qcd", "prompt_ew", "fake1_qcd", "fake1_ew", "fake2", "efake_qcd_ll", "efake_qcd_eg", "efake_ew", "ll_qcd", "ll_other", "higgs_other", "hqcd"}   # r_tau groups (D9; hqcd is a W process too)
def selmask(t, cuts=CUTS, window=False):
    m = (t["mjj"] > cuts["mjj"]) & (t["deta"] > cuts["deta"]) & (t["ptgg"] > cuts["ptgg"]) & (t["met"] > 30) & (t["ptl"] > 25)
    if window: m &= np.abs(t["mgg"]-125) < 3.5
    return m
def hist(t, meta, g, m0, mgg=None):
    """-> (sumw, sumw2) per bin for group g, selection mask m0"""
    ss, key = ALLGROUPS[g]; sid = [i for i, s in enumerate(meta["samples"]) if s in ss]; m = m0 & np.isin(t["sid"], sid)
    w = t["w"].copy()
    if key == "misid": w = w-t["whf"]
    elif key == "hf": w = t["whf"]
    elif key == "ll": m &= t["ncls1"] == 0
    elif key == "eg": m &= t["ncls1"] >= 1
    elif key == "efqcd_ll": m &= t["qcddir"].astype(bool) & (t["ncls1"] == 0)
    elif key == "efqcd_eg": m &= t["qcddir"].astype(bool) & (t["ncls1"] >= 1)
    elif key == "efew": m &= ~t["qcddir"].astype(bool)
    x = t["mgg"] if mgg is None else mgg
    h = np.histogram(x[m], bins=EDGES, weights=w[m])[0]; h2 = np.histogram(x[m], bins=EDGES, weights=w[m]**2)[0]; return h, h2
RESONANT = {"sig", "tau", "hqcd", "higgs_other"}
CENT = 0.5*(EDGES[:-1]+EDGES[1:])
def _fit_slope(h, h2, wbar):
    from scipy.optimize import minimize_scalar
    var = np.maximum(h2, wbar**2); N = h.sum()
    def chi(b):
        f = np.exp(b*(CENT-140.0)); f = f/f.sum(); return float((((h-N*f)**2)/var).sum())
    return float(minimize_scalar(chi, bounds=(-0.3, 0.3), method="bounded").x)
def smooth_hists(H):
    """Asimov backgrounds from unsmoothed MC in narrow bins are biased (bins with fluctuated-low b inflate Z): non-resonant groups are replaced by exp(slope*(m-140)) x group integral
    (slope fitted per group when N_eff >= 20, else the total-background slope); BB errors become sqrt(h_smooth * wbar) (Poisson-equivalent, wbar = sum w^2/sum w). Resonant groups (sig, tau, hqcd, higgs_other) are kept raw."""
    nr = [g for g in H if g not in RESONANT and H[g][0].sum() != 0]
    tot = sum(H[g][0] for g in nr); tot2 = sum(H[g][1] for g in nr); wb = tot2.sum()/tot.sum(); btot = _fit_slope(tot, tot2, wb); out = {}; info = {}
    for g, (h, h2) in H.items():
        if g in RESONANT or h.sum() == 0: out[g] = (h, h2); continue
        wbar = abs(h2.sum()/h.sum()); neff = h.sum()**2/h2.sum(); b = _fit_slope(h, h2, wbar) if neff >= 20 else btot
        f = np.exp(b*(CENT-140.0)); f = f/f.sum(); hs = h.sum()*f; out[g] = (hs, hs*wbar); info[g] = dict(slope=b, neff=float(neff))
    return out, info
def scale_unc(Y, samples):
    """(lo,hi) relative QCD-scale 7-point envelope of a group from the 05a VBS-region sample envelopes (events-weighted)"""
    num_lo = num_hi = den = 0.0
    for s in samples:
        r = Y["regions"]["VBS"]["samples"].get(s)
        if not r or not r.get("scale") or r["scale"]["nominal"] <= 0: continue
        sc = r["scale"]; num_lo += sc["min"]; num_hi += sc["max"]; den += sc["nominal"]
    return (num_lo/den, num_hi/den) if den > 0 else (1.0, 1.0)
def sig_theory(t, meta, m0):
    """signal scale envelope and PDF rms at the selection from the stored LHE weights; returns (scale_lo, scale_hi, pdf_rel)"""
    L = np.load(f"{WH}/work/sel/lhe_rows.npz")["lhe_S_EW_WHjj"]; sid = meta["samples"].index("S_EW_WHjj"); rows = np.nonzero(t["sid"] == sid)[0]; assert len(rows) == len(L)
    m = m0[rows]; w = t["w"][rows][m]; L = L[m]; nom = L[:, 22]; ok = np.abs(nom) > 0
    v = [float((w[ok]*L[ok, i]/nom[ok]).sum()) for i in (0, 5, 15, 22, 24, 34, 39)]; rep = np.array([float((w[ok]*L[ok, i]/nom[ok]).sum()) for i in range(45, 145)])
    n0 = float(w.sum()); return min(v)/n0, max(v)/n0, float(rep.std()/rep.mean())
def build(t, meta, Y, lumi=500.0, mu_groups=("sig",), nuis=True, mcstat=True, fscale=None, shape_sig=None, drop=(), extra_bkg=None, sig_mgg=None, class_scale=None, smooth=True, drop_nuis=(), zh_channel=None, vh=False, poi="mu", zh_samples=None):
    """returns (model, data_asimov_bonly, spec). fscale: dict group-> multiplicative factor on nominal (D36 scans). shape_sig: dict(shift=..., res=...) templates for signal.
    nuis=False -> only mu and (optionally) mcstat."""
    m0 = selmask(t); GV = dict(GROUPS)
    if vh: GV.update(GROUPS_VH_EXTRA); GV["higgs_other"] = ([x for x in GV["higgs_other"][0] if x not in ("ZH_EW_ZHjj_lostlep", "ZH_QCD_ZHjj_lostlep")], None)
    H = {g: hist(t, meta, g, m0, mgg=(sig_mgg if g == "sig" else None)) for g in GV}
    fs = dict(fscale or {}); k = lumi/500.0
    if smooth: H, _ = smooth_hists(H)
    sc = {g: scale_unc(Y, GV[g][0]) for g in GV}; sc["sig"] = sig_theory(t, meta, m0)[:2]; pdf_sig = sig_theory(t, meta, m0)[2]
    rtau = Y["regions"]["VBS"]["r_tau"]; samples = []; nuisdef = {}
    def nsys(name, g, hi, lo, bounds=None, kind="normsys"):
        nuisdef.setdefault(name, dict(bounds=bounds, kind=kind))
        return dict(name=name, type="normsys", data=dict(hi=hi, lo=lo))
    for g, (h, h2) in H.items():
        if g in drop or h.sum() == 0: continue
        h = h*k*fs.get(g, 1.0); err = np.sqrt(h2)*k*fs.get(g, 1.0); mods = []
        if g in mu_groups: mods.append(dict(name=(mu_groups[g] if isinstance(mu_groups, dict) else "mu"), type="normfactor", data=None))
        if mcstat: mods.append(dict(name="mcstat", type="staterror", data=list(np.maximum(err, 1e-12))))
        if nuis:
            mods.append(nsys("lumi", g, 1+ASSUME["lumi"], 1-ASSUME["lumi"]))
            if g in ("fake2",): pass
            elif g.startswith("fake1"): mods.append(nsys("pheff", g, 1+ASSUME["photon_eff_per_photon"], 1-ASSUME["photon_eff_per_photon"]))
            else: mods.append(nsys("pheff", g, 1+2*ASSUME["photon_eff_per_photon"], 1-2*ASSUME["photon_eff_per_photon"]))
            if not g.startswith("npl"): mods.append(nsys("lepeff", g, 1+ASSUME["lepton_eff"], 1-ASSUME["lepton_eff"]))
            if g in TAUG: mods.append(nsys("tau_r_zrows" if g in TAUG_Z else "tau_r", g, (1+2*rtau)/(1+rtau), 1/(1+rtau)))   # Z-lepton rows (lost lepton, ZHjj) carry their own tau nuisance (not correlated with the W uplift; ZH channel has none: Z->tautau->ll is 0.31 %)
            lo_, hi_ = sc[g]
            if abs(hi_-1) > 1e-4 or abs(lo_-1) > 1e-4: mods.append(nsys({"zhjj_ew": "scale_sig", "zhjj_qcd": "scale_hqcd"}.get(g, "scale_"+g), g, hi_, lo_))
            if g == "sig": mods.append(nsys("pdf_sig", g, 1+pdf_sig, 1-pdf_sig))
            if g in ("prompt_qcd", "fake1_qcd", "ll_qcd") or (V11 and g in ("efake_qcd_ll", "efake_qcd_eg")): mods.append(nsys("ps_qcd", g, 1.45, 0.55))   # v1.1: the loose sample has no C range, so the PS-jet-fraction nuisance applies to it
            if g in ("efake_qcd_ll", "efake_qcd_eg") and not V11: mods.append(nsys("C_eFake", g, 1.464, 0.536))
            if g == "efake_ew": mods.append(nsys("C_EW", g, 1.025, 0.975))
            if g == "ll_other": mods.append(nsys("C_ZaaEW", g, 1.064, 0.936))   # declared 05a item 6: Zaajj EW C +-6.4 % (twin stat); V_* rows have 0 events at the selection (ps_V acts on nothing, logged)
            if g == "efake_qcd_ll" and not V11: mods.append(nsys("cov_eFake", g, 2.053, 1.0, bounds=(0.0, 3.0)))
            if g.startswith("fake1"): mods.append(nsys("fakerate", g, 1.2, 0.8)); mods.append(nsys("nonclosure", g, 0.4, 1.0, bounds=(0.0, 1.6)))
            if g == "fake2": mods.append(nsys("fakerate", g, 1.44, 0.64)); mods.append(nsys("fake2_scen", g, 9.0, 0.09))
            if g == "npl_misid": mods.append(nsys("npl_norm", g, 3.0, 0.3))
            if g == "npl_hf": mods.append(nsys("hf_var", g, 2.0, 0.01))
            if g == "sig" and shape_sig is not None:
                mods.append(dict(name="phscale", type="histosys", data=dict(hi_data=list(shape_sig["scale_hi"]*k), lo_data=list(shape_sig["scale_lo"]*k))))
                mods.append(dict(name="phres", type="histosys", data=dict(hi_data=list(shape_sig["res_hi"]*k), lo_data=list(shape_sig["res_lo"]*k))))
        mods = [m_ for m_ in mods if m_["name"] not in drop_nuis]
        samples.append(dict(name=g, data=list(h), modifiers=mods))
    if extra_bkg is not None: samples.append(dict(name="extra", data=list(extra_bkg), modifiers=[]))
    chans = [dict(name="SR", samples=samples)]; obs = [dict(name="SR", data=[0.0]*NB)]
    if zh_channel is not None:
        zs = []
        for nm, (y, mcs, mods_) in zh_channel.items():
            mm = []
            if nm == "zh_sig": mm.append(dict(name="mu", type="normfactor", data=None))
            mm.append(dict(name="mcstat_zh", type="staterror", data=[max(float(mcs), 1e-9)]))
            for (nn, hi, lo, bnd) in mods_:
                if nn in drop_nuis: continue
                mm.append(nsys(nn, "zh", hi, lo, bounds=bnd))
            zs.append(dict(name=nm, data=[float(y)], modifiers=mm))
        chans.append(dict(name="ZH", samples=zs)); obs.append(dict(name="ZH", data=[0.0]))
    if zh_samples is not None:
        nb_z = len(zh_samples[0]["data"]); chans.append(dict(name="ZH", samples=zh_samples)); obs.append(dict(name="ZH", data=[0.0]*nb_z))
    spec = dict(channels=chans, observations=obs, measurements=[dict(name="m", config=dict(poi="mu", parameters=[]))], version="1.0.0")
    model = pyhf.Model(spec, poi_name=poi, validate=False); model._spec_for_ws = spec
    bounds = model.config.suggested_bounds(); init = model.config.suggested_init()
    for name, d in nuisdef.items():
        if d["bounds"] is not None and name in model.config.par_map: sl = model.config.par_slice(name); bounds[sl.start] = d["bounds"]
    bounds[model.config.poi_index] = (0.0, 50.0)
    for nm_ in model.config.par_map:
        if nm_.startswith('mu'): bounds[model.config.par_slice(nm_).start] = (0.0, 50.0)
    model._bounds = bounds
    return model
def asimov(model, mu=0.0):
    pars = model.config.suggested_init(); pars[model.config.poi_index] = mu
    return model.expected_data(pars)
def fit_nll(model, data, mu=None, init=None):
    bounds = model._bounds; init = list(init or model.config.suggested_init()); fixed = model.config.suggested_fixed()
    if mu is not None: init[model.config.poi_index] = mu; fixed[model.config.poi_index] = True
    r = pyhf.infer.mle.fit(data, model, init_pars=init, par_bounds=bounds, fixed_params=fixed, return_fitted_val=True); return r[0], float(r[1])
def z0_asimov(model):  # note: pyhf mle.fit returns -2 ln L (twice_nll), so q0 = difference without factor 2
    """expected discovery significance: Asimov data at mu=1 (signal+background), q0 = 2 (NLL(mu=0) - NLL(mu_hat))"""
    d = asimov(model, 1.0); p0, n0 = fit_nll(model, d, mu=0.0); ph, nh = fit_nll(model, d); q0 = max(n0-nh, 0.0); return float(np.sqrt(q0)), float(ph[model.config.poi_index])
def mu95_expected(model, scan=None):
    """expected CLs mu95 (median and +-1 sigma band as [-1s, median, +1s]) on the background-only Asimov dataset, asymptotic q_mu~ (pyhf hypotest, expected set), found by interpolating CLs(mu) = 0.05 on a scan"""
    d = asimov(model, 0.0); scan = np.geomspace(0.3, 40.0, 14) if scan is None else scan; E = []
    for mu in scan:
        r = pyhf.infer.hypotest(float(mu), d, model, test_stat="qtilde", par_bounds=model._bounds, return_expected_set=True); E.append([float(x) for x in r[1]])
    E = np.array(E); out = []
    for idx in (1, 2, 3):   # -1 sigma, median, +1 sigma of the expected CLs set (index 0..4 = -2s..+2s)
        c = E[:, idx]; lm = np.log(scan)
        out.append(float(np.exp(np.interp(0.05, c[::-1], lm[::-1]))) if c.min() < 0.05 < c.max() else (float(scan[-1]) if c.min() > 0.05 else float(scan[0])))
    return out
def eq1(s, b): return float(np.sqrt(2*((s+b)*np.log1p(s/b)-s))) if s > 0 and b > 0 else 0.0
def pois_cls_mu95(s, b, n):
    """exact Poisson CLs upper limit on mu for observed count n (single bin, no systematics): CLs = P(N<=n|mu s+b)/P(N<=n|b) = 0.05"""
    from scipy.stats import poisson; from scipy.optimize import brentq
    f = lambda mu: poisson.cdf(n, mu*s+b)/poisson.cdf(n, b)-0.05
    return float(brentq(f, 0.0, 1e4)) if f(0.0) > 0 else 0.0
def pois_mu95_expected(s, b):
    """median and +-1sigma expected exact-Poisson CLs mu95: observed n at the 16/50/84 % quantiles of Poisson(b)"""
    from scipy.stats import poisson
    return {k: pois_cls_mu95(s, b, int(poisson.ppf(q, b))) for k, q in (("q16_low_limit", 0.16), ("median", 0.5), ("q84_high_limit", 0.84))}
