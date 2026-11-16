# VERIFY_REQUEST: v1.2 production + frozen-cut re-evaluation (A1, A2, D1-D7 fixes)
Changes v1.1 -> v1.2 (cut-based selection, 500 fb^-1). Checks: SAMPLES.csv rows F_QCD_llajj_nomjj, F_QCD_llajj_loose_v12 (V1.2_NOTES.md; exit evidence work/v12_exit_evidence.json; sigma/closure; x1.083 = tau factor; v1/v1.1 prefixes), selection_v12.json D45 labels, 05a sec. 13 (D49 settled by D50 = option 4; N_eff >= 10 NOT met for the QCD lost-lepton part), config/lostlep_qcd.json single input (swap test: bg_yields output unchanged when re-run: verified identical).

| quantity | old | new | source key (new; old in the same file family) |
|---|---|---|---|
| cut-based b | 1.797 | 1.747 | work/sel/selection_v12.json::v12/cut_based/b (old: v11/cut_based/b) |
| cut-based Z | 0.4339 | 0.4395 | work/sel/selection_v12.json::v12/cut_based/Z (old: v11/cut_based/Z) |
| cut-based neff | 62.82 | 83.2 | work/sel/selection_v12.json::v12/cut_based/neff (old: v11/cut_based/neff) |
| share of b, lost_lepton_egamma | 0.2798 | 0.2591 | selection_v12.json::D45/lost_lepton_egamma/share_v12 (old share_v11); rel_change -0.074; trigger fired = False |
| share of b vs v1, lost_lepton_egamma | 0.2815 | 0.2591 | selection_v12.json::D45_vs_v1/lost_lepton_egamma |
| share of b, nonprompt_lepton | 0.0115 | 0.01183 | selection_v12.json::D45/nonprompt_lepton/share_v12 (old share_v11); rel_change +0.029; trigger fired = False |
| share of b vs v1, nonprompt_lepton | 0.01148 | 0.01183 | selection_v12.json::D45_vs_v1/nonprompt_lepton |
| lost-lepton class Y | 0.5028 | 0.4525 | work/v12_lostlep_neff.json::v1.2/_class/Y |
| lost-lepton class raw | 116 | 116 | work/v12_lostlep_neff.json::v1.2/_class/raw |
| lost-lepton class neff | 7.644 | 11.16 | work/v12_lostlep_neff.json::v1.2/_class/neff |
| QCD loose part: raw rows / row weight [events] | 1 / 0.1715 | 1 / 0.1212 | work/v12_lostlep_neff.json::v1.2/F_QCD_llajj_loose |
| QCD loose part 1-sigma (p = 0.1587 per side) Poisson interval | -- | [0.021, 0.400] | work/v12_lostlep_neff.json::QCD_part_poisson/interval68 |


## D49 (human: option 2 with the fallback -> option 4; D50 final: no new production)
Pre-declared (written before any production; scripts/d49_floor.py): C = Y(no-cut twin F_QCD_llajj_loose union, 7.5M)/Y(mmjj>400 loose sample) in the reco SR, ZH twin-correction method (frozen reports/FINAL_report.md:245; wh/reports/02_background_overlap.md:94), stat formula rel.err^2 = 1/n_twin + 1/n_cut >= 1/n_twin. The twin has ONE raw event in the SR: floor 100 % > 30 % whatever the cut sample size -> option (4): yield = one-event estimate with its 95 % Poisson interval as the uncertainty, Z/mu95 shown at the upper end; the v1 vbs x C estimate (0.176 [0.094, 0.257]) stays the cross-check (config/lostlep_qcd.json use_vbs_x_C). The central scenario reproduces the nominal Z0 (0.428 at 500) as a self-check. rankvh (VH nuisance ranking, cluster 913470) was removed once by SYSTEM_PERIODIC_REMOVE after about 24 h (913470.001; its sibling 913470.000, the WH rank, returned 0) and was not rerun: the WH ranking rank_v12.json exists, the VH ranking is not delivered (recorded as a limitation).

| quantity | old | new | source key (new; old in the same file family) |
|---|---|---|---|
| QCD lost-lepton C stat floor in the reco SR | (D49 settled by D50 = option 4) | 1.00 (> 0.30) | work/d49_floor.json::floor_rel_err_C; twin n=1 raw event, Garwood 1-sigma (p=0.1587 per side) [0.17280696442536914, 3.299159095941823] |
| info only: twin count, SR without the H mass window (information only) | -- | n=21, rel 0.22 | work/d49_floor.json::rows (NOT the D49 region; C there would need the 11M mmjj>400 sample: D50 closed, not done) |
| info only: twin count, SR without mjj, deta, window (information only) | -- | n=98, rel 0.10 | work/d49_floor.json::rows (NOT the D49 region; C there would need the 11M mmjj>400 sample: D50 closed, not done) |
| QCD part yield [events], 500 fb-1 SR | 0.121 (R2 text) | 0.121 (final, option 4) | work/v12_lostlep_neff.json::QCD_part_poisson/Y; config/lostlep_qcd.json::source = D49_option4_floor_gt30pct |
| QCD part 95 % interval [events] | [0.003, 0.68] (quoted) | [0.0031, 0.675] | work/v12_lostlep_neff.json::QCD_part_poisson/interval95 |
| WH Z0 / mu95 (-1s, med, +1s), 500 fb-1, QCD lost-lepton lower95 (0.0031) | (not shown) | 0.461 / 4.09, 6.41, 10.43 | work/stat/ll4_500_v12.json::rows/lower95 (task ll4:500, cluster 913556, scales groups efake_qcd_ll+efake_qcd_eg) |
| WH Z0 / mu95 (-1s, med, +1s), 500 fb-1, QCD lost-lepton central (0.1212) | (not shown) | 0.445 / 4.21, 6.58, 10.67 | work/stat/ll4_500_v12.json::rows/central (task ll4:500, cluster 913556, scales groups efake_qcd_ll+efake_qcd_eg) |
| WH Z0 / mu95 (-1s, med, +1s), 500 fb-1, QCD lost-lepton upper95 (0.6754) | (not shown) | 0.379 / 4.96, 7.82, 12.99 | work/stat/ll4_500_v12.json::rows/upper95 (task ll4:500, cluster 913556, scales groups efake_qcd_ll+efake_qcd_eg) |
| WH Z0 / mu95 (-1s, med, +1s), 1000 fb-1, QCD lost-lepton lower95 (0.0031) | (not shown) | 0.643 / 2.68, 4.08, 6.45 | work/stat/ll4_1000_v12.json::rows/lower95 (task ll4:1000, cluster 913556, scales groups efake_qcd_ll+efake_qcd_eg) |
| WH Z0 / mu95 (-1s, med, +1s), 1000 fb-1, QCD lost-lepton central (0.1212) | (not shown) | 0.620 / 2.76, 4.21, 6.64 | work/stat/ll4_1000_v12.json::rows/central (task ll4:1000, cluster 913556, scales groups efake_qcd_ll+efake_qcd_eg) |
| WH Z0 / mu95 (-1s, med, +1s), 1000 fb-1, QCD lost-lepton upper95 (0.6754) | (not shown) | 0.515 / 3.40, 5.27, 8.62 | work/stat/ll4_1000_v12.json::rows/upper95 (task ll4:1000, cluster 913556, scales groups efake_qcd_ll+efake_qcd_eg) |
| WH Z0 / mu95 (-1s, med, +1s), 3000 fb-1, QCD lost-lepton lower95 (0.0031) | (not shown) | 1.079 / 1.44, 2.14, 3.26 | work/stat/ll4_3000_v12.json::rows/lower95 (task ll4:3000, cluster 913556, scales groups efake_qcd_ll+efake_qcd_eg) |
| WH Z0 / mu95 (-1s, med, +1s), 3000 fb-1, QCD lost-lepton central (0.1212) | (not shown) | 1.038 / 1.50, 2.22, 3.38 | work/stat/ll4_3000_v12.json::rows/central (task ll4:3000, cluster 913556, scales groups efake_qcd_ll+efake_qcd_eg) |
| WH Z0 / mu95 (-1s, med, +1s), 3000 fb-1, QCD lost-lepton upper95 (0.6754) | (not shown) | 0.796 / 2.08, 3.19, 5.20 | work/stat/ll4_3000_v12.json::rows/upper95 (task ll4:3000, cluster 913556, scales groups efake_qcd_ll+efake_qcd_eg) |


## R3 (see also VERIFY_REQUEST_workspace.md for the old->new table) (verify_R2 sev-1 S1-S3 and sev-2/3 fixes)
* S1: W1 (RESONANT) does NOT change the workspace content: all 8 workspaces rebuilt with the current code (vh_run.py ws) are BYTE-IDENTICAL to the committed ones (copies of the previous ones in work/vh_ws_prev_20261114/; the file mtime 11-15 00:10 of stat_lib.py was the mu-bound edit 50 -> 200). The stale items were the four vh_z0mu_*_both_v12.json outputs (the 913430 'both' jobs hit the 2 h limit); rerun as cluster 913943 (flavour tomorrow); old files kept as *_v12_stale.json. The couplings/lambda inputs (vh_coup.py, zh_channel_inputs.json) were rerun with the current code and are bit-identical, so the lambda toys (generated earlier) remain valid; the map2d/compat files post-date the workspaces and are unchanged.
* S2/S3: D49 is settled by D50 = option 4 in FINAL, 05a, 06, 07, VH_combination, VERIFY_REQUEST, paper T3/T4c/T11 (upper end Z0/mu95 at 500/1000/3000, interval 95 % [0.0031, 0.675], the 68 % interval is relabelled 1-sigma central); 0.176 [0.094, 0.257] called a cross-check.
* Sev-2: VH ranking not delivered (VH_combination limitations, README, T5 captions, placeholder row T5-VH, T11); D47 (3) limitations table T11 + README; kappa at 1000 in T7b; ZH non-prompt lepton class stated as unestimated and unbounded; T2-ZH labelled frozen basis + corrected fake-row cutflow T2b; basis statement (T4 joint 0.438/6.64 vs stand-alone 0.428/6.81); kW-sign convention beside every number (T7, T9, T10, VH_combination) with the D46 range 5.1-7.1; T5-ZH caption; ZH lambda toy 'not comparable'; mu95 toy statement (1.6 sigma, seeds reused, non-monotone CLs, not validated); def a: SR ZHjj-QCD is background, correlation_scheme 'tau' text aligned.
* Sev-3 done: T2-ZH and T3 literals registered, Y0 -0.17 % normalisation note, ZH toy Z0 clipping stated, toy err defined, edge-limited intervals marked, Eq. 1 defined, CMS reference by DOI, T1 k column and pre-decay sigma defined, N_eff 2.0 of ZH_Zaajj_QCD_nomjj_lostlep called out, make_verify_requests KeyError fixed. Not done: signal raw count 8157 (class table) vs 8158 (selection_v12 total) is a counting convention difference not traced; figures for kappa/lambda remain at 500 fb-1 only.



## R4 (final-package review F1-F7; no preR4 headline survives unlabelled)
* F1 (sev-1): the LLQ (efake_qcd_ll + efake_qcd_eg) PL templates were normalised to their 100-180 GeV integral (2.542 events; 0.255 in |m_gg-125|<3.5) while the D49 estimate Y0 = 0.1212 is defined in the window: the nominal PL had 2.1 x Y0 in the window and the ll4 upper end 1.42 instead of 0.675. Fix: stat_lib.build rescales the template by 0.4751 so that the window content is Y0 (config/lostlep_qcd.json window_yield; llcfg.py default); the D49 ends are window ratios (5.57, 0.0253) of it; all workspaces rebuilt (work/vh_ws_prev_R4/ keeps the old ones; the ZH workspaces are identical), everything that reads them rerun on condor (914041-914048, 914157), toys rerun on the new workspaces with the same seeds (previous production 1.5 h wall), old outputs kept as *_preR4 and work/toys_preR4/.
* F2: lambda=-1 toys reworded (median-q check, q -> Z asymptotic, tail not toy-tested) and toys thrown at lambda=-1 added. F3: FINAL / VH_combination / T10 mu95 text aligned (toys and exact Poisson 8.08 suggest the asymptotic WH mu95 is low (numbers in the R4 table: toy fit above asymptotic by about 10 %, exact Poisson counting about 26 %); VH agreement is within toy noise). F4: lambda=-1 at the D49 ends (WH, VH, both conventions) in T4c, FINAL, VH_combination. F5: deficit defined as Z_asymptotic / Z_toy - 1 everywhere. F6: 'additive q' -> joint fit with shared nuisances. F7: D39-D45 closed by the human 2026-11-14T09:49Z. verify_R3 sev-3: toys header table-driven, VH-ranking limitation in FINAL, T4c Y column relabelled.

| quantity | old | new | source key (new; old in the same file family) |
|---|---|---|---|
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
