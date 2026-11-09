#!/usr/bin/env python3
"""Writes reports/06_systematics.md and reports/07_sensitivity.md from work/stat/*.json (all expected-only)."""
import json, os, datetime, numpy as np, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
WH = "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh"; S = f"{WH}/work/stat"
def _p(n): return f"{S}/{n}_v11.json" if os.path.exists(f"{S}/{n}_v11.json") else f"{S}/{n}.json"   # v1.1 results preferred (loose eFake QCD sample); rank has no v1.1 rerun
J = lambda n: json.load(open(_p(n))) if os.path.exists(_p(n)) else None
now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M"); L = [500, 1000, 3000]
c = J("counting"); sel = json.load(open(f"{WH}/work/sel/selection_final.json"))
# ---------------- 06
A = []; a = A.append
a(f"""# 06 Systematic and mass-window models (executor-wh FINAL, block 3)
Date UTC: {now}. Status: **PASS for verification** (expected results only; no data). Git commit: see orchestrator commit.
## Goal
Fix the signal-window / m_gg model and the nuisance model before the sensitivity numbers (07): window and resolution dependence, the pre-declared nuisance list of 05a v2.1 (sec. 'nuisance list') and 05 addendum, Barlow-Beeston, with/without MC stat.
## Inputs / commands
Cut-based PRIMARY selection (05_selection.md: mjj>600, |deta|>4.0, pT(gg)>75, rest baseline), table work/sel/table.npz (nominal 05a v2.1 weights). Code: scripts/stat_lib.py (model), stat_run.py (tasks), condor job_stat.sh (clusters 899917 removed after the Z0 factor-2 bug and the unsmoothed-template bias, 899918 results, 899919 ranking; schedd bigbird103). pyhf 0.7.6 (asymptotic q0 / q_mu~), seeds: none (Asimov, no toys).
## 1. m_gg model
Signal resolution: sigma_eff = 2.10 GeV, mean 125.06 GeV (selected signal). Fit range 100-180 GeV in 40 bins of 2 GeV. Window of the cut-based counting selection: |m_gg-125|<3.5 GeV (declared grid {{2.5,3.5,5.0}}). Sidebands (outside the window) constrain the background in the fit; no data are used.
**Background templates are smoothed (bias fix):** an Asimov dataset built from the unsmoothed MC in 2 GeV bins is biased high (bins with a low-fluctuating b inflate Z; the first PL numbers, Z0 about 0.66, were of this kind and are discarded, files work/stat_unsmoothed/). Non-resonant groups are replaced by exp(slope*(m-140 GeV)) x group integral (slope fitted per group when N_eff>=20, else the total-background slope); resonant groups (signal, tau feed-down, QCD WH, other Higgs) are kept raw. Barlow-Beeston-lite errors of smoothed groups = sqrt(h_smooth * wbar).
Mass scale/resolution: photon energy scale 0.5 % (histosys on the signal), resolution +-10 % (histosys): both ASSUMED (Delphes has no scale data); resolution dependence is scanned in 07 sec. 6.
## 2. Nuisance model (pyhf modifiers, all Gaussian-constrained unless stated)
| nuisance | groups | hi / lo (relative) | origin | basis |
|---|---|---|---|---|
| lumi | all | +-2.5 % | no luminosity measurement in the study | ASSUMPTION |
| pheff | all with real photons | +-4 % (two real photons), +-2 % (one) | 2 % per photon, Delphes has no scale factors | ASSUMPTION |
| lepeff | real-lepton groups | +-1 % | no scale factors in Delphes | ASSUMPTION |
| tau_r | W/Z groups | (1+2 r_tau)/(1+r_tau), 1/(1+r_tau), r_tau = 0.083 | D9 human-set +-100 % of the MC-measured tau uplift | human rule (judgement on the size) |
| scale_<group> | per group | 7-point QCD scale envelope of the 05a VBS-region sample envelopes (signal: selection-level from the LHE weights) | LHE weights | MC-derived (LO only) |
| pdf_sig | signal | rms of 100 NNPDF3.1 replicas at the selection | LHE weights | MC-derived |
| ps_qcd | B_QCD_Waajj, F_QCD_Wajjj/T_tta/T_tWa, ZH_Zaajj_QCD | 1.45 / 0.55 (correlated) | 04:136 declared 100 % PS-jet fraction (twin loss fractions 15-45 %) | judgement |
| C_eFake | eFake QCD part | 1.464 / 0.536 | C range [1, 2.732] about 1.866 (twin ratio with a full-difference systematic) | MC-derived range, judgement on the width |
| C_EW | eFake EW part | +-2.5 % | EW twin loss fraction 2.4 +- 0.3 % | MC-derived / judgement |
| C_ZaaEW | other lost-lepton (Zaajj EW, V_*) | +-6.4 % | 05a item 6 declared (twin statistics 0.061/0.958; reconciled in v3: v1/v2 of this block used 2.5 %) | MC-derived |
| cov_eFake | eFake QCD lost-lepton part | one-sided +105 % (theta in [0,3], half-normal) | 04:139 sigma ratio 1.679/0.818 pb | MC-derived bound, pessimistic by construction |
| fakerate | fake photons | one-fake +-20 %, two-fake -36 %/+44 % (c^2) | D39 floor (CMS syst/yield 19.6 %, record verified but no comparable phase space) | judgement |
| nonclosure | one-fake | one-sided -60 % (theta in [0,1.6]) | direct/FF closure 0.39-0.41 (3-6 raw events) | MC-derived, low statistics |
| fake2_scen | two-fake | x9 / x0.09 | D27 per-photon x3 / x0.3 scenarios | judgement (human D27) |
| npl_norm | light-misID | x3 / x0.3 | D35/D36 envelope (human question a); muon rate is a placeholder (D40) | judgement |
| hf_var | heavy-flavour factorised | x2 / ~0 | +-100 % on a factorised estimate with 5 raw rows | judgement |
| phscale, phres | signal | histosys, 0.5 % / 10 % | no photon calibration data | ASSUMPTION |
| mcstat | all | per-bin Barlow-Beeston-lite (staterror) | MC statistics | MC-derived |
Every nuisance not derived from MC or data is an ASSUMPTION or a judgement (stated in the last column); the combination of ps_qcd, C_eFake, cov_eFake, fakerate, nonclosure, npl_norm and hf_var constrains nothing from data (no data exist) and only widens the expected profile.
D29 100 % PS on V_WWa/WZa/ZZa (05a item 4): the three rows have ZERO MC rows at the selection, so the nuisance would act on nothing and is not added (logged deviation; the UL variant at PEAK, 0.65 events, is in sec. 5).
Not in the fit (variants in 07): zero-support ULs (V_* 0.65, non-prompt 0.76, direct-fake variation 0.97 events at PEAK, 05a), class lower/upper bounds, D29 PS 100 % on V_* (zero events at the selection).
Correlations: nuisances with the same name act coherently on all listed groups (e.g. tau_r, ps_qcd, fakerate). Correlation with ZH (combination) is handled in the combination block.""")
r = J("rank")
if r:
    a("\n## 3. Nuisance impact (500 fb^-1, def. a; one family removed at a time; computed with the v2.1 table before the v1.1 replacement, condor 899923; no nuisance moves Z0 by more than 0.8 % or mu95 by more than 1.2 %: the expected profile is dominated by the signal/background statistics and MC statistics, not by these systematics; the ASSUMPTION nuisances are therefore not driving the result)\n\n| removed | Z0 | mu95 median |\n|---|---|---|")
    for x in r["rows"]: a(f"| {x['removed']} | {x['Z0']:.4f} | {x['mu95']:.3f} |")
for d in ("a", "b"):
    p = [J(f"pl_{l}_{d}") for l in L]
    if all(p):
        a(f"\n## 4{'a' if d=='a' else 'b'}. With / without systematics and MC stat, signal definition ({d})\n\n| L | variant | expected Z0 | PL asymptotic CLs mu95 (-1s, median, +1s) | n par |\n|---|---|---|---|---|")
        for l, x in zip(L, p):
            for k, v in x.items():
                if isinstance(v, dict) and "Z0" in v: a(f"| {l} | {k} | {v['Z0']:.3f} | {', '.join('%.2f' % z for z in v['mu95_exp'])} | {v['npar']} |")
b = J("bounds")
if b:
    a("\n## 5. Class lower/upper bounds and zero-support variants (def. a)\n\n| variant | L | Z (Eq. 1 window) | Z0 (PL, syst+BB) | PL asymptotic mu95 median (-1s,+1s) |\n|---|---|---|---|---|")
    for x in b["rows"]: a(f"| bounds {x['bounds']} | {x['lumi']:.0f} | {x['Z_eq1']:.3f} | {x['Z0_PL']:.3f} | {('%.2f (%.2f, %.2f)' % (x['mu95_exp'][1], x['mu95_exp'][0], x['mu95_exp'][2])) if x['mu95_exp'] else '-'} |")
    for x in b["ul_variants"]: a(f"| UL variant {x['variant']} (UL {x['UL_events_at_500']:.2f} ev in PEAK, {x['extra_in_window_at_500']:.2f} ev in the +-3.5 GeV window, {x['extra_total_in_range']:.1f} in 100-180 at 500) | {x['lumi']:.0f} | {x['Z_eq1']:.3f} | {x['Z0_PL']:.3f} | - |")
a("\n## 6. Caveats\nAll nuisance widths marked ASSUMPTION are placeholders; the dominant impacts are in sec. 3. Asymptotic formulas with b of order 0.1 events/bin are approximate; the counting exact-Poisson numbers of 07 are the cross-check. Systematics from the ZH side (combination) are not in this block.\n")
open(f"{WH}/reports/06_systematics.md", "w").write("\n".join(A))
# ---------------- 07
B = []; a = B.append
a(f"""# 07 Sensitivity (executor-wh FINAL, block 3)
Date UTC: {now}. Status: **PASS for verification**; ALL numbers are EXPECTED (Asimov datasets, nominal background model of 05a v2.1, primary = cut-based selection; D44). No claim of a result; a null or sub-1-sigma expectation is stated as such. Git commit: see orchestrator commit.
## Selection (frozen in 05): mjj>600, |deta_jj|>4.0, pT(gg)>75, MET>30, pT(l)>25, |m_gg-125|<3.5 (counting); MVA alternative not adopted.
## 1. Counting window (Eq. 1, stat only) and exact-Poisson CLs
Window yields at 500 fb^-1: s = {c['window_500']['s']:.3f}, b = {c['window_500']['b']:.3f} +- {c['window_500']['sigma_b_MC']:.3f} (MC stat).
| L [fb^-1] | s | b | Z Eq. 1 | Z (b -MC, b +MC) | exact-Poisson counting CLs mu95 (q16, median, q84) | def (b): s, b, Z, mu95 median |
|---|---|---|---|---|---|---|""")
for l in L:
    x = c[f"L{l}"]; y = c[f"def_b_L{l}"]; m = x["mu95_poisson"]; my = y["mu95_poisson"]
    a(f"| {l} | {x['s']:.3f} | {x['b']:.3f} | {x['Z_eq1']:.3f} | {x['Z_eq1_bMCplus']:.3f}, {x['Z_eq1_bMCminus']:.3f} | {m['q16_low_limit']:.2f}, {m['median']:.2f}, {m['q84_high_limit']:.2f} | {y['s']:.3f}, {y['b']:.3f}, {y['Z_eq1']:.3f}, {my['median']:.2f} |")
a("\nNOT the same quantity as the profile-likelihood mu95 of sec. 2 (asymptotic q~ CLs on the m_gg shape fit, pyhf). The Poisson 'q16/q84' columns are the observed-count quantiles of Poisson(b) mapped to mu95 (discrete).")
a("\n## 2. Profile likelihood (m_gg 100-180 GeV, 40 bins, all nuisances of 06 + Barlow-Beeston)\n\n| L | def | expected Z0 | PL asymptotic (q~) CLs mu95 median (-1s, +1s) | Z0 stat-only | Z0 without MC stat | Z0 MC-stat only |\n|---|---|---|---|---|---|---|")
for d in ("a", "b"):
    for l in L:
        x = J(f"pl_{l}_{d}")
        if x: f = x["full_syst_BB"]; a(f"| {l} | {d} | {f['Z0']:.3f} | {f['mu95_exp'][1]:.2f} ({f['mu95_exp'][0]:.2f}, {f['mu95_exp'][2]:.2f}) | {x['stat_only']['Z0']:.3f} | {x['syst_noMCstat']['Z0']:.3f} | {x['MCstat_only']['Z0']:.3f} |")
a("\nWith/without MC-stat impact on Z0 at 500 fb^-1 and mu95 is in 06 sec. 4: Barlow-Beeston is mandatory (cut-based b N_eff 135).")
for kind, ttl in (("fake", "fake photons (per-photon rate x f; one-fake x f, two-fake x f^2)"), ("npl", "non-prompt leptons (light misID and heavy flavour x f)")):
    for l in (500, 3000):
        d = J(f"d36_{kind}_{l}")
        if d:
            a(f"\n## 3. D36 scan: {ttl}, {l} fb^-1 (def. a, PL with all nuisances)\nD36 range x0.3-x3; f = 10, 30, 100 are BEYOND D36 (robustness only).\n\n| f | Z0 (PL) | mu95 median (-1s, +1s) | Z Eq. 1 counting | b window |\n|---|---|---|---|---|")
            for r in d["scan"]: a(f"| {r['f']}{' (beyond D36)' if r['f'] > 3 else ''} | {r['Z0_PL']:.3f} | {r['mu95_exp'][1]:.2f} ({r['mu95_exp'][0]:.2f}, {r['mu95_exp'][2]:.2f}) | {r['Z_eq1_counting']:.3f} | {r['b_window']:.3f} |")
cp = J("couplings"); cn = J("couplings_nobr")
if cp:
    a(f"""
## 4. Couplings (lambda_WZ, kappa_W/kappa_Z) from the direct samples, 500 fb^-1, expected, SM data (Asimov)
**The coupling fit uses a REDUCED nuisance model** (per-class background normalisations with the 05a VBS class-bound widths, signal theory 5 %, lumi 2.5 % (ASSUMPTION), Barlow-Beeston-lite), not the full 06 pyhf model; the stat-only, MC-stat-only and reduced results differ by <= 2 % in Z (table below), the additional nuisances of 06 are sub-dominant in the ranking of 06 sec. 3 but are not propagated here. Method (scripts/coup_run.py): per-bin quadratic Y_i = alpha_i kW^2 + beta_i kW kZ + gamma_i kZ^2 from the 8 CP-even points (weighted LSQ), x R_BR(kW,kZ) = analytic H->gamma gamma branching-ratio and total-width kappa dependence (A_W = -8.32 kW, A_t = +1.84 kt (standard H->gamma gamma loop functions, e.g. A. Djouadi, Phys. Rept. 457 (2008) 1, hep-ph/0503172; recomputed here with mH = 125 GeV, mW = 80.4 GeV, mt = 172.5 GeV: tau_W = mH^2/4mW^2 = 0.604 gives -8.32, tau_t = 0.131 with N_c Q_t^2 = 4/3 gives +1.84; the reference was not re-read for equation numbers); YR4 BRs (LHCHWG, mH = 125 GeV); kb=kt=ktau=kc=1). **The production samples carry the SM BR in k only; R_BR is an analytic correction applied on top (it matters: R_BR(lambda=-1) = {cp['rbr']['K_EW_WHjj_lam_m100']:.2f}, R_BR(0) = {cp['rbr']['K_EW_WHjj_lam_p000']:.2f}, R_BR(0.5) = {cp['rbr']['K_EW_WHjj_lam_p050']:.2f}).** Primary = with R_BR; the numbers without it (as the samples are) are given for transparency. c_A (CP-odd) is not done: only 2 CP-odd points exist (cost: >= 3 further points per axis; not cheap).
Binning chosen BEFORE the fit by the expected Asimov exclusion of lambda=-1 (stat + MC bkg): {cp['binning_chosen']} (candidates q(lambda=-1): {json.dumps({k: round(v['q_lam_m1'], 1) for k, v in cp['binning_choice'].items()})}), edges {cp['binning_choice'][cp['binning_chosen']]['edges']}.
| | with R_BR (primary) | without R_BR (samples as is) |
|---|---|---|""")
    for lab in ("stat_only", "MCstat_only", "reduced_model"):
        e = cp["expected_exclusion"][lab]; f2 = cn["expected_exclusion"][lab] if cn else None
        a(f"| {lab}: Z(lambda=-1), Z(lambda=0), Z(lambda<0 region = its closest point lambda=0) | {e['Z_lam_m1']:.2f}, {e['Z_lam_0']:.2f}, {e['Z_lambda_lt0']:.2f} | {('%.2f, %.2f, %.2f' % (f2['Z_lam_m1'], f2['Z_lam_0'], f2['Z_lambda_lt0'])) if f2 else '-'} |")
    a("\nExpected exclusion Z(lambda) (reduced coupling model, with R_BR): " + ", ".join(f"{float(l):+.2f}: {np.sqrt(q):.2f}" for l, q in cp["expected_exclusion"]["reduced_model"]["q"].items() if float(l) in (-2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.5, 2.0, 2.5, 3.0)))
    cs = cp["closure_sensitivity_signal_scale_of_tested_hypothesis"]; a("\n**Closure sensitivity (the lambda<0 number is set at lambda about 0, where the leave-one-out per-bin pulls reach 3.2 sigma):** scaling the predicted signal of the TESTED hypothesis by 0.7 / 1.0 / 1.3 gives Z(lambda=0) = {:.2f} / {:.2f} / {:.2f} and Z(lambda=-1) = {:.1f} / {:.1f} / {:.1f}: a +-30 % closure systematic changes the lambda<0 number by about +-0.04 sigma and lambda=-1 by about +-1 sigma, i.e. the qualitative statements stand but the quoted decimals are not meaningful.".format(cs["0.7"]["Z_lam_0"], cs["1.0"]["Z_lam_0"], cs["1.3"]["Z_lam_0"], cs["0.7"]["Z_lam_m1"], cs["1.0"]["Z_lam_m1"], cs["1.3"]["Z_lam_m1"])); a("\n**Interpretation:** lambda_WZ = -1 is expected to be excluded at a high level, because the W-loop/interference makes BR(gamma gamma) and the VBS-like yield and the high-pT(gg)/mT shapes very different; the whole negative range cannot be excluded better than its boundary point lambda=0 (0.4 sigma with R_BR): at lambda about 0.2 the H->gamma gamma amplitude cancels (A_W + A_t = 0) and the signal vanishes. This is an expected-sensitivity statement for the SM hypothesis, not a result.")
    a("\nLeave-one-out closure of the per-bin quadratic (LSQ-covariance included): totals |pull| <= {:.1f}; per-bin pulls up to {:.1f} (bins at lambda=0 and -0.5 where the point yields are small/low-weight): a closure caveat, quoted not hidden.".format(max(abs(r["pull_total"]) for r in cp["closure_loo"]), max(abs(p) for r in cp["closure_loo"] for p in r["pulls_per_bin"])))
    a("\n### D36 scans for the lambda<0 exclusion (reduced coupling model, primary)\n\n| kind | f | Z(lambda=-1) | Z(lambda=0) | Z(lambda=0.5) |\n|---|---|---|---|---|")
    for r in cp["d36_lambda"]: a(f"| {r['kind']} | {r['f']}{' (beyond D36)' if r['beyond_D36'] else ''} | {r['Z_lam_m1']:.2f} | {r['Z_lam_0']:.2f} | {r['Z_lam_p05']:.2f} |")
x = J("reso")
if x:
    a("\n## 6. Mass-resolution dependence (signal m_gg smeared about 125 GeV by r; 500 fb^-1, def. a)\n\n| r | s (+-3.5 window) | b | Z Eq. 1 | Z0 PL | mu95 median |\n|---|---|---|---|---|---|")
    for r in x["scan"]: a(f"| {r['resolution_factor']} | {r['s_window']:.3f} | {r['b_window']:.3f} | {r['Z_eq1']:.3f} | {r['Z0_PL']:.3f} | {r['mu95_exp'][1]:.2f} |")
a("""
## 7. Caveats / what this is not
Expected only; the sensitivity is below 1 sigma at 500 fb^-1 and about 1 sigma at 3000 fb^-1 (PL, cut-based): no evidence is expected and none is claimed. Delphes-level, LO, no pile-up. ASSUMPTION nuisances (lumi, photon/lepton efficiency, mass scale/resolution) have no data basis. Signal definition (b) adds QCD WHjj (H_QCD_WH_mlm) as signal; its interference (-0.3 % of EW) is neglected. The v1.1 row F_QCD_llajj_loose IS included (replaces the QCD part of ZH_Zajj_eFake; all numbers in this report are the v1.1 evaluation, files *_v11.json; D45 trigger not fired); H_ggF_jj is not yet included (cluster 893012, D38 fallback). MVA alternative not carried through the statistics here (D44: alternative only). Figures: figures/mgg_selection, Z_vs_lumi, d36_*, lambda_exclusion*.

## 8. Next
Verification; VH combination with the frozen ZH (swappable ZH table); comparison with CMS/ATLAS; reproducibility and FINAL report; v1.1 re-evaluations.
""")
open(f"{WH}/reports/07_sensitivity.md", "w").write("\n".join(B)); print("written")
