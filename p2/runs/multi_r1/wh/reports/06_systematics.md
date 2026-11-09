# 06 Systematic and mass-window models (executor-wh FINAL, block 3)
Date UTC: 2026-11-09 09:01. Status: **PASS for verification** (expected results only; no data). Git commit: see orchestrator commit.
## Goal
Fix the signal-window / m_gg model and the nuisance model before the sensitivity numbers (07): window and resolution dependence, the pre-declared nuisance list of 05a v2.1 (sec. 'nuisance list') and 05 addendum, Barlow-Beeston, with/without MC stat.
## Inputs / commands
Cut-based PRIMARY selection (05_selection.md: mjj>600, |deta|>4.0, pT(gg)>75, rest baseline), table work/sel/table.npz (nominal 05a v2.1 weights). Code: scripts/stat_lib.py (model), stat_run.py (tasks), condor job_stat.sh (clusters 899917 removed after the Z0 factor-2 bug and the unsmoothed-template bias, 899918 results, 899919 ranking; schedd bigbird103). pyhf 0.7.6 (asymptotic q0 / q_mu~), seeds: none (Asimov, no toys).
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
Correlations: nuisances with the same name act coherently on all listed groups (e.g. tau_r, ps_qcd, fakerate). Correlation with ZH (combination) is handled in the combination block.

## 3. Nuisance impact (500 fb^-1, def. a; one family removed at a time; computed with the v2.1 table before the v1.1 replacement, condor 899923; no nuisance moves Z0 by more than 0.8 % or mu95 by more than 1.2 %: the expected profile is dominated by the signal/background statistics and MC statistics, not by these systematics; the ASSUMPTION nuisances are therefore not driving the result)

| removed | Z0 | mu95 median |
|---|---|---|
| none | 0.4344 | 6.908 |
| lumi | 0.4346 | 6.896 |
| pheff | 0.4348 | 6.875 |
| lepeff | 0.4345 | 6.906 |
| tau_r | 0.4357 | 6.900 |
| scale_sig | 0.4344 | 6.834 |
| pdf_sig | 0.4344 | 6.907 |
| scale_prompt_qcd | 0.4352 | 6.904 |
| scale_prompt_ew | 0.4345 | 6.908 |
| scale_efake_qcd_ll | 0.4344 | 6.908 |
| scale_efake_ew | 0.4346 | 6.907 |
| ps_qcd | 0.4377 | 6.886 |
| C_eFake | 0.4351 | 6.904 |
| C_EW | 0.4344 | 6.908 |
| cov_eFake | 0.4345 | 6.908 |
| fakerate | 0.4344 | 6.908 |
| nonclosure | 0.4344 | 6.908 |
| fake2_scen | 0.4344 | 6.908 |
| npl_norm | 0.4344 | 6.908 |
| hf_var | 0.4344 | 6.908 |
| phscale | 0.4344 | 6.908 |
| phres | 0.4344 | 6.900 |

## 4a. With / without systematics and MC stat, signal definition (a)

| L | variant | expected Z0 | PL asymptotic CLs mu95 (-1s, median, +1s) | n par |
|---|---|---|---|---|
| 500 | full_syst_BB | 0.427 | 4.46, 7.10, 11.59 | 71 |
| 500 | syst_noMCstat | 0.432 | 4.33, 6.87, 11.18 | 31 |
| 500 | MCstat_only | 0.439 | 4.33, 6.89, 11.26 | 41 |
| 500 | stat_only | 0.444 | 4.18, 6.64, 10.81 | 1 |
| 1000 | full_syst_BB | 0.592 | 2.92, 4.55, 7.37 | 71 |
| 1000 | syst_noMCstat | 0.604 | 2.82, 4.27, 6.90 | 31 |
| 1000 | MCstat_only | 0.615 | 2.83, 4.33, 7.04 | 41 |
| 1000 | stat_only | 0.627 | 2.75, 4.11, 6.48 | 1 |
| 3000 | full_syst_BB | 0.973 | 1.68, 2.50, 3.84 | 71 |
| 3000 | syst_noMCstat | 1.033 | 1.54, 2.28, 3.48 | 31 |
| 3000 | MCstat_only | 1.027 | 1.60, 2.39, 3.67 | 41 |
| 3000 | stat_only | 1.087 | 1.45, 2.14, 3.24 | 1 |

## 4b. With / without systematics and MC stat, signal definition (b)

| L | variant | expected Z0 | PL asymptotic CLs mu95 (-1s, median, +1s) | n par |
|---|---|---|---|---|
| 500 | full_syst_BB | 0.484 | 3.93, 6.05, 10.24 | 71 |
| 500 | syst_noMCstat | 0.489 | 3.86, 5.92, 9.73 | 31 |
| 500 | MCstat_only | 0.498 | 3.86, 5.94, 9.86 | 41 |
| 500 | stat_only | 0.503 | 3.79, 5.81, 9.28 | 1 |
| 1000 | full_syst_BB | 0.671 | 2.62, 3.97, 6.22 | 71 |
| 1000 | syst_noMCstat | 0.684 | 2.54, 3.84, 5.91 | 31 |
| 1000 | MCstat_only | 0.697 | 2.55, 3.87, 5.98 | 41 |
| 1000 | stat_only | 0.711 | 2.47, 3.73, 5.74 | 1 |
| 3000 | full_syst_BB | 1.103 | 1.44, 2.17, 3.40 | 71 |
| 3000 | syst_noMCstat | 1.170 | 1.32, 1.93, 2.91 | 31 |
| 3000 | MCstat_only | 1.166 | 1.35, 2.03, 3.19 | 41 |
| 3000 | stat_only | 1.232 | 1.27, 1.87, 2.78 | 1 |

## 5. Class lower/upper bounds and zero-support variants (def. a)

| variant | L | Z (Eq. 1 window) | Z0 (PL, syst+BB) | PL asymptotic mu95 median (-1s,+1s) |
|---|---|---|---|---|
| bounds low | 500 | 0.487 | 0.482 | 6.34 (4.02, 10.75) |
| bounds low | 1000 | 0.689 | 0.670 | - |
| bounds low | 3000 | 1.194 | 1.112 | 2.17 (1.44, 3.41) |
| bounds nom | 500 | 0.434 | 0.427 | 7.10 (4.46, 11.59) |
| bounds nom | 1000 | 0.614 | 0.592 | - |
| bounds nom | 3000 | 1.063 | 0.973 | 2.50 (1.68, 3.84) |
| bounds high | 500 | 0.371 | 0.364 | 7.98 (5.18, 12.58) |
| bounds high | 1000 | 0.525 | 0.503 | - |
| bounds high | 3000 | 0.910 | 0.819 | 2.86 (1.94, 4.50) |
| UL variant V_star_UL (UL 0.65 ev in PEAK, 0.41 ev in the +-3.5 GeV window, 4.0 in 100-180 at 500) | 500 | 0.395 | 0.388 | - |
| UL variant V_star_UL (UL 0.65 ev in PEAK, 0.41 ev in the +-3.5 GeV window, 4.0 in 100-180 at 500) | 1000 | 0.559 | 0.539 | - |
| UL variant V_star_UL (UL 0.65 ev in PEAK, 0.41 ev in the +-3.5 GeV window, 4.0 in 100-180 at 500) | 3000 | 0.968 | 0.893 | - |
| UL variant nonprompt_UL (UL 0.76 ev in PEAK, 0.48 ev in the +-3.5 GeV window, 4.7 in 100-180 at 500) | 500 | 0.390 | 0.383 | - |
| UL variant nonprompt_UL (UL 0.76 ev in PEAK, 0.48 ev in the +-3.5 GeV window, 4.7 in 100-180 at 500) | 1000 | 0.551 | 0.532 | - |
| UL variant nonprompt_UL (UL 0.76 ev in PEAK, 0.48 ev in the +-3.5 GeV window, 4.7 in 100-180 at 500) | 3000 | 0.954 | 0.881 | - |
| UL variant direct_fake_variation_UL (UL 324.39 ev in PEAK, 204.22 ev in the +-3.5 GeV window, 2003.7 in 100-180 at 500) | 500 | 0.043 | 0.042 | - |
| UL variant direct_fake_variation_UL (UL 324.39 ev in PEAK, 204.22 ev in the +-3.5 GeV window, 2003.7 in 100-180 at 500) | 1000 | 0.060 | 0.059 | - |
| UL variant direct_fake_variation_UL (UL 324.39 ev in PEAK, 204.22 ev in the +-3.5 GeV window, 2003.7 in 100-180 at 500) | 3000 | 0.104 | 0.102 | - |
| UL variant all_three (UL 325.80 ev in PEAK, 205.11 ev in the +-3.5 GeV window, 2012.4 in 100-180 at 500) | 500 | 0.043 | 0.042 | - |
| UL variant all_three (UL 325.80 ev in PEAK, 205.11 ev in the +-3.5 GeV window, 2012.4 in 100-180 at 500) | 1000 | 0.060 | 0.059 | - |
| UL variant all_three (UL 325.80 ev in PEAK, 205.11 ev in the +-3.5 GeV window, 2012.4 in 100-180 at 500) | 3000 | 0.104 | 0.102 | - |

## 6. Caveats
All nuisance widths marked ASSUMPTION are placeholders; the dominant impacts are in sec. 3. Asymptotic formulas with b of order 0.1 events/bin are approximate; the counting exact-Poisson numbers of 07 are the cross-check. Systematics from the ZH side (combination) are not in this block.
