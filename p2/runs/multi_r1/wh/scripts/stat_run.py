#!/usr/bin/env python3
"""07 statistics driver. Usage: python3 -P stat_run.py <task> ; writes $STAT_WH/work/stat/<task>.json (task with ':' -> '_').
Tasks: rank | counting | pl:<lumi>:<a|b> | d36:<fake|npl>:<lumi> | reso | bounds.
All results are EXPECTED (Asimov, background-only for limits, signal+background for Z); no data exist. Selection: cut-based primary of 05_selection.md."""
import sys, json, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from stat_lib import *
t, meta, Y = load(); task = sys.argv[1]; LUMIS = (500.0, 1000.0, 3000.0)
sig = t["cls"] == meta["classes"]["signal"]; mw = selmask(t, window=True); m0 = selmask(t)
GCLASS = {"prompt_qcd": "prompt_irreducible", "prompt_ew": "prompt_irreducible", "fake1_qcd": "fake_photon_1", "fake1_ew": "fake_photon_1", "fake2": "fake_photon_2", "npl_misid": "nonprompt_lepton", "npl_hf": "nonprompt_lepton",
          "efake_qcd_ll": "lost_lepton_egamma", "efake_qcd_eg": "lost_lepton_egamma", "efake_ew": "lost_lepton_egamma", "ll_qcd": "lost_lepton_egamma", "ll_other": "lost_lepton_egamma", "higgs_other": "other_higgs", "hqcd": "other_higgs", "tau": "tau_feeddown"}
def templates():
    sidx = meta["classes"]["signal"]; mg = t["mgg"]; H = lambda x: hist(t, meta, "sig", m0, mgg=x)[0]; mu = 125.0
    return dict(scale_hi=H(mg*(1+ASSUME["phscale"])), scale_lo=H(mg*(1-ASSUME["phscale"])), res_hi=H(mu+(mg-mu)*(1+ASSUME["phres"])), res_lo=H(mu+(mg-mu)*(1-ASSUME["phres"])))
def window_sb(fs=None):
    """selected counting-window yields (cut-based primary, hw 3.5): s, b, sigma_b (MC stat) at 500/fb; fs = group scale dict"""
    s = float(t["w"][mw & sig].sum()); b = 0.0; v = 0.0
    for g in GROUPS:
        if g == "sig": continue
        h, h2 = hist(t, meta, g, mw); f = (fs or {}).get(g, 1.0); b += h.sum()*f; v += h2.sum()*f*f
    return s, b, float(np.sqrt(v))
def pl_block(lumi, mu_groups, **kw):
    out = {}; shp = templates()
    for name, o in (("full_syst_BB", dict(nuis=True, mcstat=True)), ("syst_noMCstat", dict(nuis=True, mcstat=False)), ("MCstat_only", dict(nuis=False, mcstat=True)), ("stat_only", dict(nuis=False, mcstat=False))):
        mod = build(t, meta, Y, lumi=lumi, mu_groups=mu_groups, shape_sig=(shp if o["nuis"] else None), **o, **kw); z, mh = z0_asimov(mod); out[name] = dict(Z0=z, mu95_exp=mu95_expected(mod), npar=len(mod.config.suggested_init()))
    return out
res = dict(task=task, assumptions=ASSUME, cuts=CUTS)
if task == "counting":
    s, b, sb = window_sb(); res["window_500"] = dict(s=s, b=b, sigma_b_MC=sb)
    for L in LUMIS:
        k = L/500.0; ss, bb, sg = s*k, b*k, sb*k
        res[f"L{int(L)}"] = dict(s=ss, b=bb, sigma_b=sg, Z_eq1=eq1(ss, bb), Z_eq1_bMCminus=eq1(ss, bb+sg), Z_eq1_bMCplus=eq1(ss, max(bb-sg, 1e-9)), mu95_poisson=pois_mu95_expected(ss, bb), s_over_sqrtb=ss/np.sqrt(bb))
    # signal definition (b): QCD WHjj added to s (QCD WH jj yield from H_QCD_WH_mlm; interference -0.3 % neglected)
    hq = float(hist(t, meta, "hqcd", mw)[0].sum()); res["def_b_window_500"] = dict(s=s+hq, b=b-hq, hqcd=hq)
    for L in LUMIS: k = L/500.0; res[f"def_b_L{int(L)}"] = dict(s=(s+hq)*k, b=(b-hq)*k, Z_eq1=eq1((s+hq)*k, (b-hq)*k), mu95_poisson=pois_mu95_expected((s+hq)*k, (b-hq)*k))
    # per-class selected yields
    res["classes_window_500"] = {g: float(hist(t, meta, g, mw)[0].sum()) for g in GROUPS}
    res["classes_window_500_stat"] = {g: float(np.sqrt(hist(t, meta, g, mw)[1].sum())) for g in GROUPS}
    res["classes_window_500_raw"] = {g: int((mw & np.isin(t["sid"], [i for i, s_ in enumerate(meta["samples"]) if s_ in GROUPS[g][0]])).sum()) for g in GROUPS}
elif task.startswith("pl:"):
    _, L, d = task.split(":"); L = float(L); res.update(lumi=L, definition=d, **pl_block(L, ("sig",) if d == "a" else ("sig", "hqcd")))
elif task.startswith("d36:"):
    _, kind, L = task.split(":"); L = float(L); fac = [0.3, 0.5, 1.0, 2.0, 3.0] + [10.0, 30.0, 100.0]; res.update(kind=kind, lumi=L, factors=fac, note="x0.3-x3 is the D36 range; 10, 30, 100 are BEYOND D36 (robustness only). fakes: per-photon rate x f (one-fake x f, two-fake x f^2); npl: light misID and heavy-flavour x f")
    shp = templates(); res["scan"] = []
    for f in fac:
        fs = {"fake1_qcd": f, "fake1_ew": f, "fake2": f*f} if kind == "fake" else {"npl_misid": f, "npl_hf": f}
        mod = build(t, meta, Y, lumi=L, fscale=fs, shape_sig=shp); z, _ = z0_asimov(mod); mu = mu95_expected(mod); s_, b_, sg_ = window_sb(fs)
        res["scan"].append(dict(f=f, Z0_PL=z, mu95_exp=mu, Z_eq1_counting=eq1(s_*L/500, b_*L/500), b_window=b_*L/500))
elif task == "reso":
    shp = templates(); res["scan"] = []; mg = t["mgg"]; s0 = None
    for r in (0.8, 1.0, 1.25, 1.5, 2.0):
        mgg_s = 125.0+(mg-125.0)*r; s_ = float(t["w"][mw & sig].sum()); hsig = hist(t, meta, "sig", m0, mgg=mgg_s)[0]; xw = mgg_s[m0 & sig]; ws = t["w"][m0 & sig]; sw = float(ws[np.abs(xw-125.0) < 3.5].sum())
        _, b_, _ = window_sb(); mod = build(t, meta, Y, lumi=500.0, sig_mgg=mgg_s); z, _ = z0_asimov(mod); mu = mu95_expected(mod)
        res["scan"].append(dict(resolution_factor=r, s_window=sw, b_window=b_, Z_eq1=eq1(sw, b_), Z0_PL=z, mu95_exp=mu))
    res["note"] = "signal m_gg smeared about 125 GeV by the factor r (fixed +-3.5 GeV counting window; PL uses all 40 bins); the ASSUMED photon scale (0.5 %) and resolution (10 %) nuisances are in the nominal fit"
elif task == "bounds":
    Cl = {c: Y["regions"]["VBS"]["classes"][c] for c in Y["regions"]["VBS"]["classes"]}; res["rows"] = []
    shp = templates()
    for lab in ("low", "nom", "high"):
        fs = {g: (Cl[GCLASS[g]][lab]/Cl[GCLASS[g]]["nom"] if Cl[GCLASS[g]]["nom"] > 0 else 1.0) for g in GCLASS}
        s_, b_, sg_ = window_sb(fs)
        for L in LUMIS:
            mod = build(t, meta, Y, lumi=L, fscale=fs, shape_sig=shp); z, _ = z0_asimov(mod); mu = mu95_expected(mod) if L in (500.0, 3000.0) else None
            res["rows"].append(dict(bounds=lab, lumi=L, Z_eq1=eq1(s_*L/500, b_*L/500), Z0_PL=z, mu95_exp=mu, b_window=b_*L/500))
    # zero-support UL sums as sensitivity variants (05a PEAK values, added flat to the window total)
    ul = Y["regions"]["PEAK"]["classes"]; extra = {"V_star_UL": ul["lost_lepton_egamma"]["UL95_sum_zero_support_rows"], "nonprompt_UL": ul["nonprompt_lepton"]["UL95_sum_zero_support_rows"], "direct_fake_variation_UL": ul["fake_photon_1"]["UL95_sum_direct_variation"]+ul["fake_photon_2"]["UL95_sum_direct_variation"]}
    res["ul_variants"] = []
    for nm, v in list(extra.items())+[("all_three", sum(extra.values()))]:
        # v = zero-support UL of the 05a PEAK block region (120-130 GeV): spread over the 40 bins with the smooth NOMINAL total-background shape, normalised so that 120-130 GeV (bins 10-14) holds v events (v1 bug: flat v/3.5 per bin put 11.4 v into the fit range)
        Hs0, _ = smooth_hists({g: hist(t, meta, g, m0) for g in GROUPS}); bsum = sum(Hs0[g][0] for g in Hs0 if g != "sig"); shape = bsum/bsum[10:15].sum(); flat = v*shape; frac_win = float(flat[np.abs(CENT-125.0) < 3.5].sum()/v) if v > 0 else 0.0
        for L in LUMIS:
            k = L/500.0; s_, b_, _ = window_sb(); mod = build(t, meta, Y, lumi=L, extra_bkg=flat*k, shape_sig=shp); z, _ = z0_asimov(mod)
            res["ul_variants"].append(dict(variant=nm, UL_events_at_500=v, lumi=L, Z_eq1=eq1(s_*k, (b_+v*frac_win)*k), Z0_PL=z, extra_in_window_at_500=v*frac_win, extra_total_in_range=float(flat.sum())))
elif task == "rank":
    names = ["lumi", "pheff", "lepeff", "tau_r", "scale_sig", "pdf_sig", "scale_prompt_qcd", "scale_prompt_ew", "scale_efake_qcd_ll", "scale_efake_ew", "ps_qcd", "C_eFake", "C_EW", "cov_eFake", "fakerate", "nonclosure", "fake2_scen", "npl_norm", "hf_var", "phscale", "phres"]
    shp = templates(); base = build(t, meta, Y, shape_sig=shp); res["rows"] = [dict(removed="none", Z0=z0_asimov(base)[0], mu95=mu95_expected(base)[1])]
    for n in names:
        mod = build(t, meta, Y, shape_sig=shp, drop_nuis=(n,)); res["rows"].append(dict(removed=n, Z0=z0_asimov(mod)[0], mu95=mu95_expected(mod)[1]))
os.makedirs(f"{WH}/work/stat", exist_ok=True); json.dump(res, open(f"{WH}/work/stat/{task.replace(':', '_')}{SUF}.json", "w"), indent=1, default=float); print(json.dumps(res, default=float)[:1500])
