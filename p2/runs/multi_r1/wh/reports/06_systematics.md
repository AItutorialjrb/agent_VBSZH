# 06 Systematic and mass-window models (executor-wh FINAL, block 3)
Date UTC: 2026-11-16 05:17. Status: **PASS for verification** (expected results only; no data). Analysis commit: ORCH_COMMIT_PLACEHOLDER.
## Goal
Fix the signal-window / m_gg model and the nuisance model before the sensitivity numbers (07): window and resolution dependence, the pre-declared nuisance list of 05a v2.1 (sec. 'nuisance list') and 05 addendum, Barlow-Beeston, with/without MC stat.
## Inputs / commands
Cut-based PRIMARY selection (05_selection.md: mjj>600, |deta|>4.0, pT(gg)>75, rest baseline), table work/sel/table_v11.npz (05a v2.1 nominal weights with the v1.1 loose eFake sample; the v2.1 table.npz only for the robustness row and the ranking). Code: scripts/stat_lib.py (model), stat_run.py (tasks), condor job_stat.sh (clusters 899917 removed after the Z0 factor-2 bug and the unsmoothed-template bias, 899918 results, 899919 ranking; schedd bigbird103). pyhf 0.7.6 (asymptotic q0 / q_mu~), seeds: none (Asimov, no toys).
## 1. m_gg model
Signal resolution: sigma_eff = 2.10 GeV, mean 125.06 GeV (selected signal). Fit range 100-180 GeV in 40 bins of 2 GeV. Window of the cut-based counting selection: |m_gg-125|<3.5 GeV (declared grid {2.5,3.5,5.0}). Sidebands (outside the window) constrain the background in the fit; no data are used.
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
| ps_qcd | B_QCD_Waajj, F_QCD_Wajjj/T_tta/T_tWa, ZH_Zaajj_QCD, and (v1.1) the loose eFake QCD part | 1.45 / 0.55 (correlated) | 04:136 declared 100 % PS-jet fraction (twin loss fractions 15-45 %) | judgement |
| C_eFake | eFake QCD part (v2.1 model only; NOT used in v1.1: replaced by ps_qcd on the loose sample) | 1.464 / 0.536 | C range [1, 2.732] about 1.866 (twin ratio with a full-difference systematic) | MC-derived range, judgement on the width |
| C_EW | eFake EW part | +-2.5 % | EW twin loss fraction 2.4 +- 0.3 % | MC-derived / judgement |
| C_ZaaEW | other lost-lepton (Zaajj EW, V_*) | +-6.4 % | 05a item 6 declared (twin statistics 0.061/0.958; reconciled in v3: v1/v2 of this block used 2.5 %) | MC-derived |
| cov_eFake | eFake QCD lost-lepton part (v2.1 model only; NOT used in v1.1) | one-sided +105 % (theta in [0,3], half-normal) | 04:139 sigma ratio 1.679/0.818 pb | MC-derived bound, pessimistic by construction |
| fakerate | fake photons | one-fake +-20 %, two-fake -36 %/+44 % (c^2) | D39 floor (CMS syst/yield 19.6 %, record verified but no comparable phase space) | judgement |
| nonclosure | one-fake | one-sided -60 % (theta in [0,1.6]) | direct/FF closure 0.39-0.41 (3-6 raw events) | MC-derived, low statistics |
| fake2_scen | two-fake | x9 / x0.09 | D27 per-photon x3 / x0.3 scenarios | judgement (human D27) |
| npl_norm | light-misID | x3 / x0.3 | D35/D36 envelope (human question a); muon rate is a placeholder (D40) | judgement |
| hf_var | heavy-flavour factorised | x2 / ~0 | +-100 % on a factorised estimate with 5 raw rows | judgement |
| phscale, phres | signal | histosys, 0.5 % / 10 % | no photon calibration data | ASSUMPTION |
| mcstat | all | per-bin Barlow-Beeston-lite (staterror) | MC statistics | MC-derived |
Every nuisance not derived from MC or data is an ASSUMPTION or a judgement (stated in the last column); the combination of ps_qcd, C_eFake, cov_eFake, fakerate, nonclosure, npl_norm and hf_var constrains nothing from data (no data exist) and only widens the expected profile.
D29 100 % PS on V_WWa/WZa/ZZa (05a item 4): the three rows have ZERO MC rows at the selection, so the nuisance would act on nothing and is not added (logged deviation; the UL variant at PEAK, 0.65 events, is in sec. 5).
(The tables of this report are the v1.1 model: the v2.1-only nuisances are listed for the robustness row of sec. 5.)
Not in the fit (variants in 07): zero-support ULs (V_* 0.65, non-prompt 0.76, direct-fake variation 0.97 events at PEAK, 05a), class lower/upper bounds, D29 PS 100 % on V_* (zero events at the selection).
Correlations: nuisances with the same name act coherently on all listed groups (e.g. tau_r, ps_qcd, fakerate). Correlation with ZH (combination) is handled in the combination block.

## 3. Nuisance impact (500 fb^-1, def. a; one family removed at a time; computed with the v2.1 table before the v1.1 replacement, condor 899923; no nuisance moves Z0 by more than 0.8 % or mu95 by more than 1.2 %: the expected profile is dominated by the signal/background statistics and MC statistics, not by these systematics; the ASSUMPTION nuisances are therefore not driving the result)

| removed | Z0 | mu95 median |
|---|---|---|
| none | 0.4280 | 6.814 |
| lumi | 0.4281 | 6.804 |
| pheff | 0.4283 | 6.788 |
| lepeff | 0.4280 | 6.812 |
| tau_r | 0.4285 | 6.812 |
| scale_sig | 0.4280 | 6.751 |
| pdf_sig | 0.4280 | 6.813 |
| scale_prompt_qcd | 0.4286 | 6.812 |
| scale_prompt_ew | 0.4281 | 6.814 |
| scale_efake_qcd_ll | 0.4281 | 6.814 |
| scale_efake_ew | 0.4280 | 6.814 |
| ps_qcd | 0.4352 | 6.773 |
| C_eFake | 0.4280 | 6.814 |
| C_EW | 0.4280 | 6.814 |
| cov_eFake | 0.4280 | 6.814 |
| fakerate | 0.4280 | 6.814 |
| nonclosure | 0.4280 | 6.814 |
| fake2_scen | 0.4280 | 6.814 |
| npl_norm | 0.4280 | 6.814 |
| hf_var | 0.4280 | 6.814 |
| phscale | 0.4280 | 6.814 |
| phres | 0.4280 | 6.806 |

## 4a. With / without systematics and MC stat, signal definition (a)

| L | variant | expected Z0 | PL asymptotic CLs mu95 (-1s, median, +1s) | n par |
|---|---|---|---|---|
| 500 | full_syst_BB | 0.428 | 4.37, 6.81, 11.06 | 72 |
| 500 | syst_noMCstat | 0.432 | 4.28, 6.65, 10.69 | 32 |
| 500 | MCstat_only | 0.440 | 4.27, 6.63, 10.68 | 41 |
| 500 | stat_only | 0.443 | 4.19, 6.47, 10.31 | 1 |
| 1000 | full_syst_BB | 0.594 | 2.88, 4.40, 6.94 | 72 |
| 1000 | syst_noMCstat | 0.604 | 2.80, 4.24, 6.62 | 32 |
| 1000 | MCstat_only | 0.617 | 2.79, 4.24, 6.65 | 41 |
| 1000 | stat_only | 0.627 | 2.71, 4.09, 6.33 | 1 |
| 3000 | full_syst_BB | 0.983 | 1.59, 2.36, 3.62 | 72 |
| 3000 | syst_noMCstat | 1.033 | 1.49, 2.19, 3.30 | 32 |
| 3000 | MCstat_only | 1.036 | 1.52, 2.25, 3.42 | 41 |
| 3000 | stat_only | 1.086 | 1.42, 2.08, 3.10 | 1 |

## 4b. With / without systematics and MC stat, signal definition (b)

| L | variant | expected Z0 | PL asymptotic CLs mu95 (-1s, median, +1s) | n par |
|---|---|---|---|---|
| 500 | full_syst_BB | 0.485 | 3.84, 6.00, 9.75 | 72 |
| 500 | syst_noMCstat | 0.489 | 3.77, 5.86, 9.43 | 32 |
| 500 | MCstat_only | 0.498 | 3.76, 5.86, 9.45 | 41 |
| 500 | stat_only | 0.502 | 3.69, 5.71, 9.13 | 1 |
| 1000 | full_syst_BB | 0.673 | 2.53, 3.86, 6.10 | 72 |
| 1000 | syst_noMCstat | 0.684 | 2.46, 3.73, 5.83 | 32 |
| 1000 | MCstat_only | 0.699 | 2.46, 3.74, 5.87 | 41 |
| 1000 | stat_only | 0.710 | 2.39, 3.60, 5.59 | 1 |
| 3000 | full_syst_BB | 1.114 | 1.39, 2.07, 3.17 | 72 |
| 3000 | syst_noMCstat | 1.169 | 1.31, 1.92, 2.89 | 32 |
| 3000 | MCstat_only | 1.176 | 1.33, 1.97, 3.00 | 41 |
| 3000 | stat_only | 1.231 | 1.25, 1.83, 2.73 | 1 |

## 5. Class lower/upper bounds and zero-support variants (def. a)

| variant | L | Z (Eq. 1 window) | Z0 (PL, syst+BB) | PL asymptotic mu95 median (-1s,+1s) |
|---|---|---|---|---|
| bounds low | 500 | 0.494 | 0.483 | 6.24 (3.96, 10.22) |
| bounds low | 1000 | 0.698 | 0.672 | - |
| bounds low | 3000 | 1.209 | 1.120 | 2.08 (1.39, 3.19) |
| bounds nom | 500 | 0.440 | 0.428 | 6.81 (4.37, 11.06) |
| bounds nom | 1000 | 0.622 | 0.594 | - |
| bounds nom | 3000 | 1.077 | 0.983 | 2.36 (1.59, 3.62) |
| bounds high | 500 | 0.376 | 0.365 | 7.67 (4.97, 12.30) |
| bounds high | 1000 | 0.532 | 0.506 | - |
| bounds high | 3000 | 0.921 | 0.830 | 2.79 (1.89, 4.25) |
| UL variant V_star_UL (UL 0.65 ev in PEAK, 0.41 ev in the +-3.5 GeV window, 4.0 in 100-180 at 500) | 500 | 0.399 | 0.389 | - |
| UL variant V_star_UL (UL 0.65 ev in PEAK, 0.41 ev in the +-3.5 GeV window, 4.0 in 100-180 at 500) | 1000 | 0.565 | 0.541 | - |
| UL variant V_star_UL (UL 0.65 ev in PEAK, 0.41 ev in the +-3.5 GeV window, 4.0 in 100-180 at 500) | 3000 | 0.978 | 0.900 | - |
| UL variant nonprompt_UL (UL 0.76 ev in PEAK, 0.48 ev in the +-3.5 GeV window, 4.7 in 100-180 at 500) | 500 | 0.394 | 0.383 | - |
| UL variant nonprompt_UL (UL 0.76 ev in PEAK, 0.48 ev in the +-3.5 GeV window, 4.7 in 100-180 at 500) | 1000 | 0.557 | 0.534 | - |
| UL variant nonprompt_UL (UL 0.76 ev in PEAK, 0.48 ev in the +-3.5 GeV window, 4.7 in 100-180 at 500) | 3000 | 0.964 | 0.889 | - |
| UL variant direct_fake_variation_UL (UL 324.39 ev in PEAK, 204.20 ev in the +-3.5 GeV window, 1996.2 in 100-180 at 500) | 500 | 0.043 | 0.042 | - |
| UL variant direct_fake_variation_UL (UL 324.39 ev in PEAK, 204.20 ev in the +-3.5 GeV window, 1996.2 in 100-180 at 500) | 1000 | 0.060 | 0.059 | - |
| UL variant direct_fake_variation_UL (UL 324.39 ev in PEAK, 204.20 ev in the +-3.5 GeV window, 1996.2 in 100-180 at 500) | 3000 | 0.104 | 0.102 | - |
| UL variant all_three (UL 325.80 ev in PEAK, 205.08 ev in the +-3.5 GeV window, 2004.8 in 100-180 at 500) | 500 | 0.043 | 0.042 | - |
| UL variant all_three (UL 325.80 ev in PEAK, 205.08 ev in the +-3.5 GeV window, 2004.8 in 100-180 at 500) | 1000 | 0.060 | 0.059 | - |
| UL variant all_three (UL 325.80 ev in PEAK, 205.08 ev in the +-3.5 GeV window, 2004.8 in 100-180 at 500) | 3000 | 0.104 | 0.102 | - |
| ROBUSTNESS v1 model: vbs x C eFake QCD (C_eFake, cov_eFake nuisances), full syst+BB | 500 | - | 0.434 | 6.91 (4.34, 11.29) |
| ROBUSTNESS v1 model: vbs x C eFake QCD (C_eFake, cov_eFake nuisances), full syst+BB | 1000 | - | 0.606 | 4.34 (2.83, 7.04) |
| ROBUSTNESS v1 model: vbs x C eFake QCD (C_eFake, cov_eFake nuisances), full syst+BB | 3000 | - | 1.017 | 2.35 (1.58, 3.61) |
| H_ggF_jj D38 scaled proxy added (0.024 ev in the window at 500) | 500 | - | 0.425 (PL; nominal 0.427) | - |
| H_ggF_jj D38 scaled proxy added (0.024 ev in the window at 500) | 1000 | - | 0.589 (PL; nominal 0.592) | - |
| H_ggF_jj D38 scaled proxy added (0.024 ev in the window at 500) | 3000 | - | 0.968 (PL; nominal 0.973) | - |

## 6. Caveats
All nuisance widths marked ASSUMPTION are placeholders; the dominant impacts are in sec. 3. Asymptotic formulas with b of order 0.1 events/bin are approximate; the counting exact-Poisson numbers of 07 are the cross-check. Systematics from the ZH side (combination) are not in this block.


## D49 option (4): central and upper-end result (systematic range of the QCD lost-lepton part)

D49 SETTLED by D50 = option (4): the QCD lost-lepton / e->gamma part is the one-event estimate 0.121 events (one selected raw F_QCD_llajj_loose row, 7.5M-event union), 95 % Garwood interval [0.0031, 0.675] (1-sigma central interval [0.021, 0.400]); the pre-declared reco-SR twin correction C has a stat floor of 100 % (> 30 %), so no cut sample was produced (work/d49_floor.json); the v1 vbs x C estimate (0.176 [0.094, 0.257]) is a CROSS-CHECK, not an independent estimate; the upper-end result is shown with the central one (table in this report). The class still does NOT meet the D42 N_eff >= 10 rule (one-event dominated; stated limitation).

WH alone, definition (a), stand-alone WH workspace, full systematics (task ll4:L, the two QCD groups efake_qcd_ll + efake_qcd_eg scaled to the interval ends, whole m_gg template; the central row reproduces the nominal fit). Y0 uses the gridpack sigma (the closure sigma gives 0.12101, -0.17 %, a normalisation note, not a change of the estimate). The sample ZH_Zaajj_QCD_nomjj_lostlep of the same class has N_eff = 2.0 (yield 0.0029): it too is below the N_eff >= 10 rule.

| L (fb-1) | QCD lost-lepton part | Y at 500 fb-1 (events) | Z0 (PL) | mu95 median (-1s, +1s) |
|---|---|---|---|---|
| 500 | lower95 | 0.0031 | 0.460 | 6.42 (4.10, 10.43) |
| 500 | central | 0.1212 | 0.428 | 6.81 (4.37, 11.06) |
| 500 | upper95 | 0.6754 | 0.309 | 10.91 (6.51, 21.54) |
| 1000 | lower95 | 0.0031 | 0.642 | 4.09 (2.68, 6.46) |
| 1000 | central | 0.1212 | 0.594 | 4.40 (2.88, 6.94) |
| 1000 | upper95 | 0.6754 | 0.400 | 8.32 (4.92, 17.21) |
| 3000 | lower95 | 0.0031 | 1.078 | 2.14 (1.44, 3.26) |
| 3000 | central | 0.1212 | 0.983 | 2.36 (1.59, 3.62) |
| 3000 | upper95 | 0.6754 | 0.544 | 6.45 (3.69, 14.24) |
