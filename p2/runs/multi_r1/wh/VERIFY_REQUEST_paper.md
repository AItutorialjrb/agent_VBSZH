# VERIFY_REQUEST: paper results package (A6)
p2/combination/paper/: README.md, regenerate.sh, paper_numbers.json (717 numbers; missing: []), tables/*.tex (T1-T10), figures/*.pdf|png. Checks: every number in tables/figures is in paper_numbers.json with a source json key (spot-check 20 random entries against their source files); the CMS/ATLAS comparison numbers vs wh/work/refs/; consistency with FINAL_report.md / VH_combination.md; one-command regeneration reproduces identical files; no new physics numbers beyond the registry (all old->new changes are listed in the other three requests: the paper package is new).

## R2 (verifier P1-P12 fixes)
* P1: T8_cA_ZH rebuilt: readable interval unions for frozen and corrected values, corrected values used (two changed intervals marked *). P2: every .tex table compiled with pdflatex in a scratch directory (tables/compile_check.json). P3: T10 rebuilt (R2 toy numbers, ZH toy and lambda caveats, no negative errors, lambda=-1 rows incl. ZH). P4: D49 flag on the T3 WH lost-lepton row. P5: added T4b (ZH codes), T5_systematics_VH, T6 ZH lepton row (not modelled, reason stated), T3 ZH non-prompt-lepton row (absent by construction), T7b (kappa_W, kappa_Z) numbers (68/95 % extents), T1 note that VH is the union. P6: T4 all on the joint pyhf code, ZH frozen-code values in T4b. P7: basis stated in T4 caption. P8: T2 ZH caption reconciles 0.4505 / 0.5196 / 0.4687. P9: T5_systematics_WH regenerated on v1.2 (rank_v12.json). P10: published values registered with citations (pub.* in paper_numbers.json), study row = VH, matched luminosity stated, lambda numbers direct at 140 fb^-1. P11: D46 cited in T7, lambda<0 numbers unified on the joint-template basis (FINAL uses couplings_vh*). P12: T1 sigma in pb everywhere, k column labelled, T6 states the D40 placeholder.


## R3 (see also VERIFY_REQUEST_workspace.md for the old->new table) (verify_R2 sev-1 S1-S3 and sev-2/3 fixes)
* S1: W1 (RESONANT) does NOT change the workspace content: all 8 workspaces rebuilt with the current code (vh_run.py ws) are BYTE-IDENTICAL to the committed ones (copies of the previous ones in work/vh_ws_prev_20261114/; the file mtime 11-15 00:10 of stat_lib.py was the mu-bound edit 50 -> 200). The stale items were the four vh_z0mu_*_both_v12.json outputs (the 913430 'both' jobs hit the 2 h limit); rerun as cluster 913943 (flavour tomorrow); old files kept as *_v12_stale.json. The couplings/lambda inputs (vh_coup.py, zh_channel_inputs.json) were rerun with the current code and are bit-identical, so the lambda toys (generated earlier) remain valid; the map2d/compat files post-date the workspaces and are unchanged.
* S2/S3: D49 is settled by D50 = option 4 in FINAL, 05a, 06, 07, VH_combination, VERIFY_REQUEST, paper T3/T4c/T11 (upper end Z0/mu95 at 500/1000/3000, interval 95 % [0.0031, 0.675], the 68 % interval is relabelled 1-sigma central); 0.176 [0.094, 0.257] called a cross-check.
* Sev-2: VH ranking not delivered (VH_combination limitations, README, T5 captions, placeholder row T5-VH, T11); D47 (3) limitations table T11 + README; kappa at 1000 in T7b; ZH non-prompt lepton class stated as unestimated and unbounded; T2-ZH labelled frozen basis + corrected fake-row cutflow T2b; basis statement (T4 joint 0.438/6.64 vs stand-alone 0.428/6.81); kW-sign convention beside every number (T7, T9, T10, VH_combination) with the D46 range 5.1-7.1; T5-ZH caption; ZH lambda toy 'not comparable'; mu95 toy statement (1.6 sigma, seeds reused, non-monotone CLs, not validated); def a: SR ZHjj-QCD is background, correlation_scheme 'tau' text aligned.
* Sev-3 done: T2-ZH and T3 literals registered, Y0 -0.17 % normalisation note, ZH toy Z0 clipping stated, toy err defined, edge-limited intervals marked, Eq. 1 defined, CMS reference by DOI, T1 k column and pre-decay sigma defined, N_eff 2.0 of ZH_Zaajj_QCD_nomjj_lostlep called out, make_verify_requests KeyError fixed. Not done: signal raw count 8157 (class table) vs 8158 (selection_v12 total) is a counting convention difference not traced; figures for kappa/lambda remain at 500 fb-1 only.



R3 downstream (VH headline from the replaced both-files; paper T4/T10 and VH_combination read the same keys):

| quantity | old | new | source key (new; old in the same file family) |
|---|---|---|---|
| VH Z0 asymptotic (def a, 500) in toys table / T10 / VH_combination | 0.4474 | 0.4734 | toys_summary_v12.json::q0/VH/Z0_asimov |
| VH asymptotic over toy Z0 (toy 0.406 unchanged) | -0.029 | +0.027 | toys_summary_v12.json::q0/VH (percentage above the toy value) |
| VH mu95 asymptotic (def a, 500) | 6.512 | 6.005 | toys_summary_v12.json::mu95/VH/mu95_asymptotic |
| VH mu95 toy fit minus asymptotic [sigma_fit] | +0.5 | +1.4 | toys_summary_v12.json::mu95/VH (toy 6.41 +- 0.35 unchanged) |


## R4 (final-package review F1-F7; no preR4 headline survives unlabelled)
* F1 (sev-1): the LLQ (efake_qcd_ll + efake_qcd_eg) PL templates were normalised to their 100-180 GeV integral (2.542 events; 0.255 in |m_gg-125|<3.5) while the D49 estimate Y0 = 0.1212 is defined in the window: the nominal PL had 2.1 x Y0 in the window and the ll4 upper end 1.42 instead of 0.675. Fix: stat_lib.build rescales the template by 0.4751 so that the window content is Y0 (config/lostlep_qcd.json window_yield; llcfg.py default); the D49 ends are window ratios (5.57, 0.0253) of it; all workspaces rebuilt (work/vh_ws_prev_R4/ keeps the old ones; the ZH workspaces are identical), everything that reads them rerun on condor (914041-914048, 914157), toys rerun on the new workspaces with the same seeds (previous production 1.5 h wall), old outputs kept as *_preR4 and work/toys_preR4/.
* F2: lambda=-1 toys reworded (median-q check, q -> Z asymptotic, tail not toy-tested) and toys thrown at lambda=-1 added. F3: FINAL / VH_combination / T10 mu95 text aligned (toys and exact Poisson 8.08 suggest the asymptotic WH mu95 is low (numbers in the R4 table: toy fit above asymptotic by about 10 %, exact Poisson counting about 26 %); VH agreement is within toy noise). F4: lambda=-1 at the D49 ends (WH, VH, both conventions) in T4c, FINAL, VH_combination. F5: deficit defined as Z_asymptotic / Z_toy - 1 everywhere. F6: 'additive q' -> joint fit with shared nuisances. F7: D39-D45 closed by the human 2026-11-14T09:49Z. verify_R3 sev-3: toys header table-driven, VH-ranking limitation in FINAL, T4c Y column relabelled.

| quantity | old | new | source key (new; old in the same file family) |
|---|---|---|---|
| stand-alone WH Z0 / mu95 (-1s, med, +1s), 500, (a) | 0.4280 / 4.37, 6.81, 11.06 | 0.4451 / 4.21, 6.58, 10.67 | pl_500_a_v12.json::full_syst_BB (old: pl_500_a_v12_preR4.json) |
| WH (joint ws) Z0 / mu95 (-1s, med, +1s), 500, (a) | 0.4381 / 4.26, 6.64, 10.77 | 0.4555 / 4.11, 6.41, 10.40 | vh_z0mu_500_a_wh_v12.json (old: _preR4) |
| ZH Z0 / mu95 (-1s, med, +1s), 500, (a) | 0.1310 / 19.34, 32.26, 56.13 | 0.1310 / 19.34, 32.26, 56.13 | vh_z0mu_500_a_zh_v12.json (old: _preR4) |
| VH Z0 / mu95 (-1s, med, +1s), 500, (a) | 0.4567 / 4.00, 6.20, 9.97 | 0.4734 / 3.87, 6.01, 9.66 | vh_z0mu_500_a_both_v12.json (old: _preR4) |
| stand-alone WH Z0 / mu95 (-1s, med, +1s), 500, (b) | 0.4848 / 3.84, 6.00, 9.75 | 0.5046 / 3.70, 5.79, 9.41 | pl_500_b_v12.json::full_syst_BB (old: pl_500_b_v12_preR4.json) |
| WH (joint ws) Z0 / mu95 (-1s, med, +1s), 500, (b) | 0.4993 / 3.72, 5.81, 9.44 | 0.5197 / 3.59, 5.61, 9.11 | vh_z0mu_500_b_wh_v12.json (old: _preR4) |
| ZH Z0 / mu95 (-1s, med, +1s), 500, (b) | 0.2096 / 12.26, 20.66, 36.50 | 0.2096 / 12.26, 20.66, 36.50 | vh_z0mu_500_b_zh_v12.json (old: _preR4) |
| VH Z0 / mu95 (-1s, med, +1s), 500, (b) | 0.5406 / 3.35, 5.19, 8.34 | 0.5594 / 3.25, 5.03, 8.09 | vh_z0mu_500_b_both_v12.json (old: _preR4) |
| stand-alone WH Z0 / mu95 (-1s, med, +1s), 1000, (a) | 0.5943 / 2.88, 4.40, 6.94 | 0.6201 / 2.76, 4.21, 6.64 | pl_1000_a_v12.json::full_syst_BB (old: pl_1000_a_v12_preR4.json) |
| WH (joint ws) Z0 / mu95 (-1s, med, +1s), 1000, (a) | 0.6084 / 2.81, 4.28, 6.77 | 0.6347 / 2.69, 4.10, 6.47 | vh_z0mu_1000_a_wh_v12.json (old: _preR4) |
| ZH Z0 / mu95 (-1s, med, +1s), 1000, (a) | 0.1840 / 11.82, 19.09, 32.18 | 0.1840 / 11.82, 19.09, 32.18 | vh_z0mu_1000_a_zh_v12.json (old: _preR4) |
| VH Z0 / mu95 (-1s, med, +1s), 1000, (a) | 0.6345 / 2.65, 4.02, 6.30 | 0.6596 / 2.55, 3.87, 6.06 | vh_z0mu_1000_a_both_v12.json (old: _preR4) |
| stand-alone WH Z0 / mu95 (-1s, med, +1s), 1000, (b) | 0.6730 / 2.53, 3.86, 6.10 | 0.7029 / 2.42, 3.70, 5.83 | pl_1000_b_v12.json::full_syst_BB (old: pl_1000_b_v12_preR4.json) |
| WH (joint ws) Z0 / mu95 (-1s, med, +1s), 1000, (b) | 0.6932 / 2.45, 3.74, 5.91 | 0.7239 / 2.35, 3.58, 5.65 | vh_z0mu_1000_b_wh_v12.json (old: _preR4) |
| ZH Z0 / mu95 (-1s, med, +1s), 1000, (b) | 0.2948 / 7.45, 12.15, 20.81 | 0.2948 / 7.45, 12.15, 20.81 | vh_z0mu_1000_b_zh_v12.json (old: _preR4) |
| VH Z0 / mu95 (-1s, med, +1s), 1000, (b) | 0.7515 / 2.22, 3.36, 5.25 | 0.7796 / 2.14, 3.24, 5.06 | vh_z0mu_1000_b_both_v12.json (old: _preR4) |
| stand-alone WH Z0 / mu95 (-1s, med, +1s), 3000, (a) | 0.9834 / 1.59, 2.36, 3.62 | 1.0383 / 1.50, 2.22, 3.38 | pl_3000_a_v12.json::full_syst_BB (old: pl_3000_a_v12_preR4.json) |
| WH (joint ws) Z0 / mu95 (-1s, med, +1s), 3000, (a) | 1.0070 / 1.55, 2.30, 3.53 | 1.0628 / 1.46, 2.16, 3.30 | vh_z0mu_3000_a_wh_v12.json (old: _preR4) |
| ZH Z0 / mu95 (-1s, med, +1s), 3000, (a) | 0.3125 / 5.82, 8.98, 14.40 | 0.3125 / 5.82, 8.98, 14.40 | vh_z0mu_3000_a_zh_v12.json (old: _preR4) |
| VH Z0 / mu95 (-1s, med, +1s), 3000, (a) | 1.0513 / 1.47, 2.17, 3.31 | 1.1045 / 1.39, 2.06, 3.11 | vh_z0mu_3000_a_both_v12.json (old: _preR4) |
| stand-alone WH Z0 / mu95 (-1s, med, +1s), 3000, (b) | 1.1141 / 1.39, 2.07, 3.17 | 1.1771 / 1.31, 1.94, 2.96 | pl_3000_b_v12.json::full_syst_BB (old: pl_3000_b_v12_preR4.json) |
| WH (joint ws) Z0 / mu95 (-1s, med, +1s), 3000, (b) | 1.1478 / 1.35, 2.00, 3.06 | 1.2123 / 1.27, 1.88, 2.86 | vh_z0mu_3000_b_wh_v12.json (old: _preR4) |
| ZH Z0 / mu95 (-1s, med, +1s), 3000, (b) | 0.5002 / 3.63, 5.66, 9.23 | 0.5002 / 3.63, 5.66, 9.23 | vh_z0mu_3000_b_zh_v12.json (old: _preR4) |
| VH Z0 / mu95 (-1s, med, +1s), 3000, (b) | 1.2473 / 1.22, 1.80, 2.74 | 1.3062 / 1.16, 1.71, 2.59 | vh_z0mu_3000_b_both_v12.json (old: _preR4) |
| wh Z0 / mu95, 140, (a) | 0.2368 / 9.94, 16.39, 28.16 | 0.2453 / 9.70, 16.01, 27.54 | vh_z0mu_140_a_wh_v12.json (old: _preR4) |
| zh Z0 / mu95, 140, (a) | 0.0696 / 52.58, 92.82, 100.00 | 0.0696 / 52.58, 92.82, 100.00 | vh_z0mu_140_a_zh_v12.json (old: _preR4) |
| both Z0 / mu95, 140, (a) | 0.2467 / 9.23, 15.07, 25.64 | 0.2549 / 9.02, 14.76, 25.14 | vh_z0mu_140_a_both_v12.json (old: _preR4) |
| WH ranking: nominal Z0 / mu95 ('none' row) | 0.4280 / 6.814 | 0.4451 / 6.580 | rank_v12.json::rows/0 (old: _preR4) |
| D36 fake x0.3, 500: Z0 / mu95 med | 0.4302 / 6.79 | 0.4476 / 6.56 | d36_fake_500_v12.json::scan (old: _preR4) |
| D36 fake x1.0, 500: Z0 / mu95 med | 0.4280 / 6.81 | 0.4451 / 6.58 | d36_fake_500_v12.json::scan (old: _preR4) |
| D36 fake x3.0, 500: Z0 / mu95 med | 0.4215 / 6.88 | 0.4378 / 6.65 | d36_fake_500_v12.json::scan (old: _preR4) |
| D36 fake x0.3, 3000: Z0 / mu95 med | 0.9879 / 2.36 | 1.0436 / 2.21 | d36_fake_3000_v12.json::scan (old: _preR4) |
| D36 fake x1.0, 3000: Z0 / mu95 med | 0.9834 / 2.36 | 1.0383 / 2.22 | d36_fake_3000_v12.json::scan (old: _preR4) |
| D36 fake x3.0, 3000: Z0 / mu95 med | 0.9700 / 2.39 | 1.0226 / 2.25 | d36_fake_3000_v12.json::scan (old: _preR4) |
| D36 npl x0.3, 500: Z0 / mu95 med | 0.4293 / 6.80 | 0.4466 / 6.56 | d36_npl_500_v12.json::scan (old: _preR4) |
| D36 npl x1.0, 500: Z0 / mu95 med | 0.4280 / 6.81 | 0.4451 / 6.58 | d36_npl_500_v12.json::scan (old: _preR4) |
| D36 npl x3.0, 500: Z0 / mu95 med | 0.4243 / 6.85 | 0.4409 / 6.62 | d36_npl_500_v12.json::scan (old: _preR4) |
| D36 npl x0.3, 3000: Z0 / mu95 med | 0.9862 / 2.36 | 1.0416 / 2.21 | d36_npl_3000_v12.json::scan (old: _preR4) |
| D36 npl x1.0, 3000: Z0 / mu95 med | 0.9834 / 2.36 | 1.0383 / 2.22 | d36_npl_3000_v12.json::scan (old: _preR4) |
| D36 npl x3.0, 3000: Z0 / mu95 med | 0.9752 / 2.38 | 1.0287 / 2.24 | d36_npl_3000_v12.json::scan (old: _preR4) |
| 2D map best fit (mu_WH, mu_ZH), 500, (a) | {'mu_WH': 1.0, 'mu_ZH': 1.0} | {'mu_WH': 1.0, 'mu_ZH': 1.0} | vh_map2d_500_a_v12.json::best_fit (old: _preR4) |
| 2D map best fit (mu_WH, mu_ZH), 500, (b) | {'mu_WH': 1.0, 'mu_ZH': 1.0} | {'mu_WH': 1.0, 'mu_ZH': 1.0} | vh_map2d_500_b_v12.json::best_fit (old: _preR4) |
| 2D map best fit (mu_WH, mu_ZH), 1000, (a) | {'mu_WH': 1.0, 'mu_ZH': 1.0} | {'mu_WH': 1.0, 'mu_ZH': 1.0} | vh_map2d_1000_a_v12.json::best_fit (old: _preR4) |
| 2D map best fit (mu_WH, mu_ZH), 1000, (b) | {'mu_WH': 1.0, 'mu_ZH': 1.0} | {'mu_WH': 1.0, 'mu_ZH': 1.0} | vh_map2d_1000_b_v12.json::best_fit (old: _preR4) |
| 2D map best fit (mu_WH, mu_ZH), 3000, (a) | {'mu_WH': 1.0, 'mu_ZH': 1.0} | {'mu_WH': 1.0, 'mu_ZH': 1.0} | vh_map2d_3000_a_v12.json::best_fit (old: _preR4) |
| 2D map best fit (mu_WH, mu_ZH), 3000, (b) | {'mu_WH': 1.0, 'mu_ZH': 1.0} | {'mu_WH': 1.0, 'mu_ZH': 1.0} | vh_map2d_3000_b_v12.json::best_fit (old: _preR4) |
| couplings_vh: max |Delta Z_lambda_m1| | -- | 0.0e+00 | couplings (reduced model, event-level window: unchanged by R4) |
| couplings_vh_L1000: max |Delta Z_lambda_m1| | -- | 0.0e+00 | couplings (reduced model, event-level window: unchanged by R4) |
| couplings_vh_L3000: max |Delta Z_lambda_m1| | -- | 0.0e+00 | couplings (reduced model, event-level window: unchanged by R4) |
| couplings_vh_L140: max |Delta Z_lambda_m1| | -- | 0.0e+00 | couplings (reduced model, event-level window: unchanged by R4) |
| couplings_vh_kzneg: max |Delta Z_lambda_m1| | -- | 0.0e+00 | couplings (reduced model, event-level window: unchanged by R4) |
| couplings_vh_kzneg_L1000: max |Delta Z_lambda_m1| | -- | 0.0e+00 | couplings (reduced model, event-level window: unchanged by R4) |
| couplings_vh_kzneg_L3000: max |Delta Z_lambda_m1| | -- | 0.0e+00 | couplings (reduced model, event-level window: unchanged by R4) |
| couplings_vh_kzneg_L140: max |Delta Z_lambda_m1| | -- | 0.0e+00 | couplings (reduced model, event-level window: unchanged by R4) |
| D49 ll4 WH Z0 / mu95 (-1s, med, +1s), 500, lower95 (window Y 0.0031; old scale basis: whole template) | 0.460 / 4.10, 6.42, 10.43 | 0.461 / 4.09, 6.41, 10.43 | ll4_500_v12.json::rows/lower95 (old: _preR4) |
| D49 ll4 WH Z0 / mu95 (-1s, med, +1s), 500, central (window Y 0.1212; old scale basis: whole template) | 0.428 / 4.37, 6.81, 11.06 | 0.445 / 4.21, 6.58, 10.67 | ll4_500_v12.json::rows/central (old: _preR4) |
| D49 ll4 WH Z0 / mu95 (-1s, med, +1s), 500, upper95 (window Y 0.6754; old scale basis: whole template) | 0.309 / 6.51, 10.91, 21.54 | 0.379 / 4.96, 7.82, 12.99 | ll4_500_v12.json::rows/upper95 (old: _preR4) |
| D49 ll4 WH Z0 / mu95 (-1s, med, +1s), 1000, lower95 (window Y 0.0031; old scale basis: whole template) | 0.642 / 2.68, 4.09, 6.46 | 0.643 / 2.68, 4.08, 6.45 | ll4_1000_v12.json::rows/lower95 (old: _preR4) |
| D49 ll4 WH Z0 / mu95 (-1s, med, +1s), 1000, central (window Y 0.1212; old scale basis: whole template) | 0.594 / 2.88, 4.40, 6.94 | 0.620 / 2.76, 4.21, 6.64 | ll4_1000_v12.json::rows/central (old: _preR4) |
| D49 ll4 WH Z0 / mu95 (-1s, med, +1s), 1000, upper95 (window Y 0.6754; old scale basis: whole template) | 0.400 / 4.92, 8.32, 17.21 | 0.515 / 3.40, 5.27, 8.62 | ll4_1000_v12.json::rows/upper95 (old: _preR4) |
| D49 ll4 WH Z0 / mu95 (-1s, med, +1s), 3000, lower95 (window Y 0.0031; old scale basis: whole template) | 1.078 / 1.44, 2.14, 3.26 | 1.079 / 1.44, 2.14, 3.26 | ll4_3000_v12.json::rows/lower95 (old: _preR4) |
| D49 ll4 WH Z0 / mu95 (-1s, med, +1s), 3000, central (window Y 0.1212; old scale basis: whole template) | 0.983 / 1.59, 2.36, 3.62 | 1.038 / 1.50, 2.22, 3.38 | ll4_3000_v12.json::rows/central (old: _preR4) |
| D49 ll4 WH Z0 / mu95 (-1s, med, +1s), 3000, upper95 (window Y 0.6754; old scale basis: whole template) | 0.544 / 3.69, 6.45, 14.24 | 0.796 / 2.08, 3.19, 5.20 | ll4_3000_v12.json::rows/upper95 (old: _preR4) |
| D49 lambda=-1 Z (WH / VH) 500, kW-sign (kW<0, kZ=kt=+1, BR x2.45): lower / central / upper | (not shown) | 6.204 / 6.242 ; 6.204 / 6.241 ; 6.202 / 6.239 | couplings_vh[_ll0.0253|_ll5.57]_v12.json |
| D49 lambda=-1 Z (WH / VH) 1000, kW-sign (kW<0, kZ=kt=+1, BR x2.45): lower / central / upper | (not shown) | 8.606 / 8.653 ; 8.605 / 8.653 ; 8.604 / 8.651 | couplings_vh_L1000[_ll0.0253|_ll5.57]_v12.json |
| D49 lambda=-1 Z (WH / VH) 3000, kW-sign (kW<0, kZ=kt=+1, BR x2.45): lower / central / upper | (not shown) | 13.975 / 14.041 ; 13.975 / 14.040 ; 13.975 / 14.040 | couplings_vh_L3000[_ll0.0253|_ll5.57]_v12.json |
| D49 lambda=-1 Z (WH / VH) 500, kZ-sign: lower / central / upper | (not shown) | 3.766 / 3.776 ; 3.766 / 3.776 ; 3.766 / 3.776 | couplings_vh_kzneg[_ll0.0253|_ll5.57]_v12.json |
| D49 lambda=-1 Z (WH / VH) 1000, kZ-sign: lower / central / upper | (not shown) | 5.282 / 5.296 ; 5.282 / 5.296 ; 5.282 / 5.296 | couplings_vh_kzneg_L1000[_ll0.0253|_ll5.57]_v12.json |
| D49 lambda=-1 Z (WH / VH) 3000, kZ-sign: lower / central / upper | (not shown) | 8.859 / 8.878 ; 8.859 / 8.877 ; 8.856 / 8.875 | couplings_vh_kzneg_L3000[_ll0.0253|_ll5.57]_v12.json |
| toys Z0 WH: asymptotic / toy median | 0.438 / 0.406 | 0.456 / 0.425 | toys_summary_v12.json::q0/WH (old: _preR4; toys rerun on the rebuilt workspaces, same seeds) |
| toys mu95 WH: asymptotic / toy fit +- err | 6.64 / 8.38 +- 1.11 | 6.41 / 7.12 +- 0.30 | toys_summary_v12.json::mu95/WH |
| toys Z0 ZH: asymptotic / toy median | 0.131 / 0.000 | 0.131 / 0.000 | toys_summary_v12.json::q0/ZH (old: _preR4; toys rerun on the rebuilt workspaces, same seeds) |
| toys mu95 ZH: asymptotic / toy fit +- err | 32.26 / 34.29 +- 1.93 | 32.26 / 33.51 +- 1.84 | toys_summary_v12.json::mu95/ZH |
| toys Z0 VH: asymptotic / toy median | 0.457 / 0.406 | 0.473 / 0.461 | toys_summary_v12.json::q0/VH (old: _preR4; toys rerun on the rebuilt workspaces, same seeds) |
| toys mu95 VH: asymptotic / toy fit +- err | 6.20 / 6.41 +- 0.35 | 6.01 / 6.82 +- 0.58 | toys_summary_v12.json::mu95/VH |
| toys lambda=-1 (SM pseudo-data) kZ-sign:WH: Asimov Z / toy median | 3.77 / 3.92 | 3.77 / 3.92 | toys_summary_v12.json::lambda_m1/kZ-sign:WH (unchanged: reduced model, not rerun) |
| toys lambda=-1 (SM pseudo-data) kZ-sign:ZH: Asimov Z / toy median | 0.29 / 0.82 | 0.29 / 0.82 | toys_summary_v12.json::lambda_m1/kZ-sign:ZH (unchanged: reduced model, not rerun) |
| toys lambda=-1 (SM pseudo-data) kZ-sign:VH: Asimov Z / toy median | 3.78 / 3.97 | 3.78 / 3.97 | toys_summary_v12.json::lambda_m1/kZ-sign:VH (unchanged: reduced model, not rerun) |
| toys lambda=-1 (SM pseudo-data) kW-sign:WH: Asimov Z / toy median | 6.20 / 6.33 | 6.20 / 6.33 | toys_summary_v12.json::lambda_m1/kW-sign:WH (unchanged: reduced model, not rerun) |
| toys lambda=-1 (SM pseudo-data) kW-sign:ZH: Asimov Z / toy median | 0.72 / 1.13 | 0.72 / 1.13 | toys_summary_v12.json::lambda_m1/kW-sign:ZH (unchanged: reduced model, not rerun) |
| toys lambda=-1 (SM pseudo-data) kW-sign:VH: Asimov Z / toy median | 6.24 / 6.37 | 6.24 / 6.37 | toys_summary_v12.json::lambda_m1/kW-sign:VH (unchanged: reduced model, not rerun) |
| NEW toys thrown at lambda=-1 kZ-sign:WH: P(q>3.84) / P(q>6.63) / P(q>10.83) vs chi2(1) | -- | 0.047 / 0.0108 / 0.0012 vs 0.050 / 0.0100 / 0.0010 | toys_summary_v12.json::lambda_true_m1/kZ-sign:WH (5000 toys; Asimov q 14.2, toys above: 0) |
| NEW toys thrown at lambda=-1 kZ-sign:ZH: P(q>3.84) / P(q>6.63) / P(q>10.83) vs chi2(1) | -- | 0.019 / 0.0032 / 0.0000 vs 0.050 / 0.0100 / 0.0010 | toys_summary_v12.json::lambda_true_m1/kZ-sign:ZH (5000 toys; Asimov q 0.1, toys above: 4277) |
| NEW toys thrown at lambda=-1 kZ-sign:VH: P(q>3.84) / P(q>6.63) / P(q>10.83) vs chi2(1) | -- | 0.039 / 0.0130 / 0.0024 vs 0.050 / 0.0100 / 0.0010 | toys_summary_v12.json::lambda_true_m1/kZ-sign:VH (5000 toys; Asimov q 14.3, toys above: 1) |
| NEW toys thrown at lambda=-1 kW-sign:WH: P(q>3.84) / P(q>6.63) / P(q>10.83) vs chi2(1) | -- | 0.034 / 0.0094 / 0.0010 vs 0.050 / 0.0100 / 0.0010 | toys_summary_v12.json::lambda_true_m1/kW-sign:WH (5000 toys; Asimov q 38.5, toys above: 0) |
| NEW toys thrown at lambda=-1 kW-sign:ZH: P(q>3.84) / P(q>6.63) / P(q>10.83) vs chi2(1) | -- | 0.021 / 0.0046 / 0.0006 vs 0.050 / 0.0100 / 0.0010 | toys_summary_v12.json::lambda_true_m1/kW-sign:ZH (5000 toys; Asimov q 0.5, toys above: 2305) |
| NEW toys thrown at lambda=-1 kW-sign:VH: P(q>3.84) / P(q>6.63) / P(q>10.83) vs chi2(1) | -- | 0.032 / 0.0102 / 0.0008 vs 0.050 / 0.0100 / 0.0010 | toys_summary_v12.json::lambda_true_m1/kW-sign:VH (5000 toys; Asimov q 38.9, toys above: 0) |


## R5 (text/regeneration only; no new jobs)
* V1 captions of T5-WH and T6 generated from the registry (no literal pre-R4 numbers remain in captions or reports outside labelled old->new tables). V2 final.json: PRIMARY_joint_basis keys added, the WH-only reduced-model keys relabelled. V3 VH mu95 toy grid (4 points x 240 vs the earlier 5 x 480, 6.41 -> 6.82 mixes workspace and grid/statistics changes) stated in T10, VH_combination, this file; not rerun. V4 pl_140_a_v12.json renamed *_prebuild (FINAL / T9 now read the fresh joint-workspace 140 value), counting_v12 / couplings_* stated workspace-independent, D49 ends / toys / map2d best fits added to VH_combination.json. R8 lambda-toy provenance text (raw window MC, no workspace read), R9 'differ in the second decimal', R10 lambda=-1 at the D49 ends columns + 'insensitive' sentence in the FINAL / VH_combination / 06 / 07 D49 tables, R11 VH tail comment next to the quoted VH 3.8 sigma (FINAL, VH_combination), R12 ZH q<1 fractions data-driven (91 % kZ-sign, 43 % kW-sign) and template tail remarks removed for ZH, R13 mu95 caveat in the FINAL headline bullet.

| quantity | old | new | source key (new; old in the same file family) |
|---|---|---|---|
| T5-WH / T6 captions: stand-alone WH Z0 / mu95 (a), 500 | 0.428 / 6.81 (pre-R4 literal) | 0.445 / 6.58 | make_paper registry wh.standalone.500.Z0 / .mu95 (pl_500_a_v12.json::full_syst_BB); captions now generated |
| FINAL / T9: WH PL mu95 at 140 fb-1 (stand-alone file predated the R4 fix) | 17.24 | 16.01 | vh_z0mu_140_a_wh_v12.json::mu95 (joint-workspace WH, rerun R4); pl_140_a_v12.json renamed pl_140_a_v12_prebuild.json |
| final.json couplings primary kZ-sign WH Z_lambda_m1 | 3.7640 (WH-only coup_run model, relabelled) | 3.7659 (joint basis) | final.json::couplings/PRIMARY_joint_basis/kZ_sign_primary/WH_Z_lambda_m1 (couplings_vh_kzneg_v12.json) |
| final.json kW-sign WH Z_lambda_m1 | 6.1973 (WH-only model, relabelled) | 6.2036 (joint basis) | final.json::couplings/PRIMARY_joint_basis/kW_sign_convention_D46/WH_Z_lambda_m1 (couplings_vh_v12.json) |
| VH_combination.md: fraction of ZH lambda toys with q<1 (kZ-sign / kW-sign) | 91 % / 91 % (template) | 91 % / 43 % | toys_summary_v12.json::lambda_m1/*:ZH/frac_q_lt_1 (now data-driven) |
| VH thrown-toy tail comment: P(q>10.83) vs chi2(1) (new text) | -- | 0.0024 vs 0.0010 (12 toys vs 5) | toys_summary_v12.json::lambda_true_m1/kZ-sign:VH/tail/10.83 |
