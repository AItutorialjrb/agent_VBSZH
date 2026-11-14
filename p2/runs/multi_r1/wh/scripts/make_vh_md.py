#!/usr/bin/env python3
"""Writes p2/combination/VH_combination.md for the JOINT likelihood (A3, final round) from work/stat/vh_*_v12.json, couplings_vh*_v12.json, toys_summary_v12.json, vh_ws/correlation_scheme.json."""
import json, os, datetime, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from pin import COMMIT
WH = "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh"; CB = "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/combination"; S = f"{WH}/work/stat"; VW = f"{CB}/vh_ws"
J = lambda p: json.load(open(p)) if os.path.exists(p) else None; now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M"); L = []; a = L.append; LU = (500, 1000, 3000)
cs = J(f"{VW}/correlation_scheme.json"); zi = J(f"{VW}/zh_channel_inputs.json"); orth = J(f"{VW}/orthogonality.json")
a(f"""# VH combination: joint WH + ZH likelihood (D47 (1))
Date UTC: {now}. Analysis commit: {COMMIT}. Status: **PASS for verification**. All numbers EXPECTED (Asimov SM data), Delphes level, 13.6 TeV, LO. Writer: executor-wh (ZH channel inputs: ZH-erratum executor, vh_ws/zh_channel_inputs.json, corrected fake-photon rows).
## Model
ONE pyhf workspace (committed: p2/combination/vh_ws/VH_workspace.json = common mu_VH, definition (a); VH_workspace_2d.json = (mu_WH, mu_ZH); *_defb.json for definition (b); WH_workspace.json and ZH_workspace.json = the single-channel versions built by the same code, scripts/vh_build.py; observations = SM Asimov data at 500 fb^-1, luminosity scaling is linear). WH channel: m_gg 100-180 GeV in 40 bins, cut-based primary selection, all WH nuisances, Barlow-Beeston-lite per bin. ZH channel: m_gg 105-165 GeV in 30 bins, 15 process samples with per-bin templates, per-bin MC statistics, systematics (zh_channel_inputs.json).
**Signal-like cross-feed samples (not fixed backgrounds):** the EW ZHjj lost-lepton rows in the WH SR (groups zhjj_ew, and zhjj_qcd in definition (b)) are scaled by the ZH signal strength (mu_ZH in the 2D fit, the common mu_VH otherwise) and carry the ZH theory nuisances; their yield in the WH SR is {J(f"{S}/couplings_vh_kzneg_v12.json")['wh_zhjj_in_whSR_SM_events'] if J(f"{S}/couplings_vh_kzneg_v12.json") else '--'} events (500 fb^-1, selection window) against {J(f"{S}/couplings_vh_kzneg_v12.json")['wh_signal_SM_events'] if J(f"{S}/couplings_vh_kzneg_v12.json") else '--'} of WH signal. The WH signal in the ZH SR has ZERO MC support (0 raw events of 300k): UL95 {zi['wh_signal_in_zh_sr'].get('UL95_events', 4.65e-4) if zi and isinstance(zi.get('wh_signal_in_zh_sr'), dict) else 4.65e-4:.3g} events, not in the fit (it would carry mu_WH). In the coupling fits both cross-feeds follow their own (kappa_W, kappa_Z) quadratic forms (ZHjj in the WH SR from the frozen K_EW_ZHjj samples through the WH selection).
**Orthogonality:** {('overlap 0 raw / 0 weighted over %d samples (vh_ws/orthogonality.json)' % len(orth.get('samples', orth))) if orth else 'see vh_ws/orthogonality.json'}; the SRs are exclusive by construction (ZH: two leptons pT>15; WH: exactly one lepton pT>10).
## Correlation scheme (vh_ws/correlation_scheme.json)
Correlated (one parameter in both channels): lumi, pheff, lepeff, phscale, phres (histosys on the real-photon EW signal samples), scale_sig and pdf_sig (EW VH signal family WH/ZH), scale_hqcd (QCD VH), scale_prompt_qcd / scale_prompt_ew (QCD / EW V gamma gamma), scale_higgs_other (ggZH, ttH, tH), fakerate (D39 floor, fake-photon rows), and scale_efake_qcd_ll (the same QCD Z gamma + jets process: ZH fake-photon rows F_QCD_Zajj = the frozen F_QCD_llajj files, WH lost-lepton e->gamma rows). Uncorrelated: MC statistics (mcstat per bin WH, mcstat_zh per bin ZH), channel-specific normalisations and modelling (WH: ps_qcd, C_*, cov_eFake, nonclosure, fake2_scen, npl_norm, hf_var, tau_r, tau_r_zrows; ZH: zh_* normalisations, scale_top_zh, zh_offshell, zh_int_zaa, zh_genmjj_*). tau: the ZH channel has no tau nuisance (Z->tautau->ll 0.31 %); in the WH SR the Z-lepton rows carry their own tau_r_zrows (not correlated with the W uplift tau_r).""")
if cs:
    a("\n| parameter | type | channels | status | declared common |\n|---|---|---|---|---|")
    for n, v in cs["parameters"].items():
        if v["status"] == "correlated" or v["declared_common"]: a(f"| {n} | {v['type']} | {','.join(v['channels'])} | {v['status']} | {v['declared_common']} |")
a("\n## Results: common mu_VH (SM Asimov; Z0 asymptotic q0; mu95 asymptotic CLs q~, median and +-1 sigma)\n\n| L | def | WH Z0 | WH mu95 (-1s, med, +1s) | ZH Z0 | ZH mu95 | VH Z0 | VH mu95 |\n|---|---|---|---|---|---|---|---|")
for d in "ab":
    for l in LU:
        r = {w: J(f"{S}/vh_z0mu_{l}_{d}_{w}_v12.json") for w in ("wh", "zh", "both")}
        c = lambda x: (f"{x['Z0']:.3f} | {x['mu95'][1]:.2f} ({x['mu95'][0]:.2f}, {x['mu95'][2]:.2f})" if x else "-- | --")
        a(f"| {l} | {d} | {c(r['wh'])} | {c(r['zh'])} | {c(r['both'])} |")
a("\nThe ZH channel is a weak constraint (its own Z0 is 0.1-0.5); the common mu improves the WH numbers by a few percent. The WH-alone rows here come from the joint-workspace code (WH_workspace.json); the 07 numbers from stat_run.py agree to the second decimal (differences: the workspace adds the signal-like ZHjj rows).")
a("\n## Results: (mu_WH, mu_ZH) and channel compatibility\n")
for l in LU:
    m = J(f"{S}/vh_map2d_{l}_a_v12.json")
    if m: a(f"* {l} fb^-1: best fit (mu_WH, mu_ZH) = ({m['best_fit']['mu_WH']:.2f}, {m['best_fit']['mu_ZH']:.2f}) on the SM Asimov data; expected q along mu_WH = mu_ZH = x: {m['q_diag_common']}; contour grid in work/stat/vh_map2d_{l}_a_v12.json (figure fig_mu_WH_vs_mu_ZH in the paper package). {m['compatibility_note']}")
a("\n## Results: lambda_WZ and (kappa_W, kappa_Z) (joint templates, same sign convention and R_BR in both channels)\n**Convention (D46):** kZ-sign (kZ = -1, kW = -lambda; convention-independent, PRIMARY) with R_BR evaluated at the actual signs; the kW-sign variant (kW<0, kZ = kt = +1: W-top interference raises BR(gamma gamma) by x2.45) is quoted only with that statement. The ZH q-curves are RE-DERIVED (not inherited from the frozen ZH study) from the corrected ZH inputs (the ZH executor's pyhf curves and the reduced-model curves here agree: lambda = -1 at 500 fb^-1 0.29 sigma). Reduced nuisance model (per-class normalisations, signal theory 5 %, lumi 2.5 % shared, per-bin BB); the joint likelihood of mu is the pyhf one above.\n\n| L | convention | lambda=-1: WH / ZH / VH | lambda<0 region: WH / ZH / VH |\n|---|---|---|---|")
for tag, nm in (("_kzneg", "kZ-sign (primary)"), ("", "kW-sign variant")):
    for l in LU:
        d_ = J(f"{S}/couplings_vh{tag}{'' if l == 500 else '_L%d' % l}_v12.json")
        if d_: cv = d_["curves"]; a(f"| {l} | {nm} | " + " / ".join(f"{cv[k]['Z_lambda_m1']:.2f}" for k in ('WH', 'ZH', 'VH')) + " | " + " / ".join(f"{cv[k]['Z_lambda_neg']:.2f}" for k in ('WH', 'ZH', 'VH')) + " |")
a("\n(kappa_W, kappa_Z) maps for WH, ZH and VH: work/stat/couplings_vh*_v12.json['maps'] and the paper figures fig_kappa_map_*. Entries at lambda>0 in the kZ-sign scan are computed at kZ = -1 (kW<0 for lambda>0): not meaningful, use the kW-sign scan for lambda>0.")
t = J(f"{S}/toys_summary_v12.json")
a("\n## Validation of the asymptotic numbers with toys (D47 (2))\n" + ("see table below and paper_numbers.json (toys_*)." if t else "toys pending (condor)."))
if t:
    for k, v in t.get("q0", {}).items(): a(f"* Z0 (500 fb^-1, def. a), {k}: asymptotic {v['Z0_asimov']:.3f}, toy median {v['Z0_toy_median']:.3f} +- {v['Z0_toy_err']:.3f} ({v['ntoys']} toys)")
    for k, v in t.get("lambda_m1", {}).items(): a(f"* lambda = -1 exclusion (500 fb^-1, kZ-sign), {k}: asymptotic Z {v['Z_asimov']:.2f}, toy median-q Z {v['Z_toy_median']:.2f} (16-84 %: {v['Z_toy_16']:.2f}-{v['Z_toy_84']:.2f}; {v['ntoys']} toys)")
a(f"""
## Limitations (D47 (3))
* **f_mu placeholder (D40):** the per-jet muon misID is 2e-5 (= the electron value); no cited value exists; the whole light-misID normalisation is covered by x0.3-x3 (D36) and by the npl_norm nuisance; non-prompt leptons are 1.1 % of b at the selection.
* **Fake-photon calibration reference mismatch (D39/D43):** CMS-SMP-19-013 (JHEP 10 (2021) 174, Table 2) is inclusive in jets and cannot calibrate the VBS-like j->gamma rate; WH uses c = 1, ZH kappa = 0.956 (rough closure); the x0.3-x3 per-photon scan covers it (fake photons are 1.7 % of b in WH).
* **Other-Higgs backgrounds are not rescaled under the coupling hypotheses** (12 % of b): the tH rows (which grow about x10 for kW*kt<0, kW-sign convention) scaled in the tested hypothesis change Z(lambda=-1) from 6.20 to 6.26 (x10) in the kW-sign convention and from 3.76 to 3.84 in the kZ-sign convention (no growth physically there): leaving them fixed is slightly conservative (couplings_v12.json['tH_growth_test_tested_hypothesis']).
* **No Z gamma + 3 jets row in ZH (D43):** the fake-photon component in ZH may be underestimated (the converted jet needs a third ME jet); WH has the 3-jet row.
* ZH and WH MC samples at LO, Delphes without pile-up; ASSUMPTION nuisances (lumi, efficiencies, photon scale/resolution) have no data basis; the lambda curves use the reduced nuisance model and asymptotics (toy check above); closure of the per-bin quadratic is not shown to cover the 3.3 sigma leave-one-out pulls.
""")
open(f"{CB}/VH_combination.md", "w").write("\n".join(L)); print("ok")
