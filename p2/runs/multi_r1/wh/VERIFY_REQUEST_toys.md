# VERIFY_REQUEST: toy validation of the asymptotic numbers (A4, D47 (2))
Scripts: wh/scripts/toys.py (q0, q0 null, qmu), vh_coup.py --toys, toys_agg.py; condor job_toys.sh (clusters 913374 q0 s+b + lambda toys, 913378 qmu, 913379 q0 null); inputs the committed workspaces. Checks: toy generation (nuisances at nominal + auxiliary data thrown for q0/qmu; all constrained nuisances thrown for the lambda toys), the CLs construction and bootstrap errors, the discrete-q plateau remark, HEADLINE: the asymptotic Z0 (pre-declared) is the quoted headline, the toy expected Z0 (Z = Phi^-1(1-p), p from the null toys at the median s+b q0) is the validation: WH and VH asymptotic-vs-toy values are in the table below (deficit defined everywhere as Z_asymptotic / Z_toy - 1; the toy is the more reliable single VH number), ZH toy 0 (median q0 = 0) vs 0.13. ZH lambda=-1 toys: q is DISCRETE at these counts, the toy Z is sqrt of the 50 % quantile of q over 5000 toys (a plateau value 0.66) against the Asimov 0.084: at q < 1 the median is fluctuation-dominated and the two are not comparable; no ZH lambda sensitivity either way.

| quantity | old | new | source key (new; old in the same file family) |
|---|---|---|---|
| Z0 WH: asymptotic -> toys (null toys) | 0.456 | 0.425 | toys_summary_v12.json::q0/WH range [0.38127392479528904, 0.4718974335952135]; N = 2000 s+b, 2000 null |
| Z0 ZH: asymptotic -> toys (null toys) | 0.131 | 0.000 | toys_summary_v12.json::q0/ZH range [0.0, 0.0]; N = 2000 s+b, 2000 null |
| Z0 VH: asymptotic -> toys (null toys) | 0.473 | 0.461 | toys_summary_v12.json::q0/VH range [0.4330203305877187, 0.5029491838950579]; N = 2000 s+b, 2000 null |
| mu95 WH: asymptotic -> toys | 6.414 | 7.124 | toys_summary_v12.json::mu95/WH straight-line fit +- 0.30 |
| mu95 ZH: asymptotic -> toys | 32.259 | 33.510 | toys_summary_v12.json::mu95/ZH straight-line fit +- 1.84 |
| mu95 VH: asymptotic -> toys | 6.005 | 6.819 | toys_summary_v12.json::mu95/VH straight-line fit +- 0.58 |
| lambda=-1 Z kZ-sign:WH: asymptotic -> toy median q | 3.766 | 3.920 | toys_summary_v12.json::lambda_m1/kZ-sign:WH (q 16-84 %: 3.49-4.28; N = 5000) |
| lambda=-1 Z kZ-sign:ZH: asymptotic -> toy median q | 0.290 | 0.815 | toys_summary_v12.json::lambda_m1/kZ-sign:ZH (q 16-84 %: 0.33-0.82; N = 5000) |
| lambda=-1 Z kZ-sign:VH: asymptotic -> toy median q | 3.776 | 3.965 | toys_summary_v12.json::lambda_m1/kZ-sign:VH (q 16-84 %: 3.42-4.26; N = 5000) |
| lambda=-1 Z kW-sign:WH: asymptotic -> toy median q | 6.204 | 6.329 | toys_summary_v12.json::lambda_m1/kW-sign:WH (q 16-84 %: 5.83-6.70; N = 5000) |
| lambda=-1 Z kW-sign:ZH: asymptotic -> toy median q | 0.724 | 1.126 | toys_summary_v12.json::lambda_m1/kW-sign:ZH (q 16-84 %: 0.23-1.30; N = 5000) |
| lambda=-1 Z kW-sign:VH: asymptotic -> toy median q | 6.241 | 6.368 | toys_summary_v12.json::lambda_m1/kW-sign:VH (q 16-84 %: 5.87-6.71; N = 5000) |

## R2 (verifier T1-T6 fixes)
* WH toy mu95 6.98 -> 8.4 (asymptotic 7.06 unchanged): NOT the W1 fix and NOT the grid/fit method. Same 4-point grid (5.5/6.5/7.5/9.0), 8x50 toys per point and per hypothesis in both productions. Applying the CURRENT straight-line fit to the archived unseeded production gives 6.85, to the new seeded one 8.34, so the change is the toy realisation (new random streams, i.e. seeding T1): CLs_exp(mu=9.0) = 0.010 (old) vs 0.055 (new), two binomial points with 400 toys each (errors 0.005 and 0.018); the fit error on mu95 is 1.1, so 6.85 vs 8.34 is about 1 sigma of the combined error (about 1.5). W1 cannot be the cause since the asymptotic WH mu95 is identical (7.062) before and after it. Conclusion (wording, coordinator option b): the asymptotic mu95 agrees with the toys within the toy statistical error (WH +-1.1 = 13 %, ZH +-1.9, VH +-0.35 from the fit covariance); the toys constrain mu95 only to that precision, so mu95 is NOT called validated or confirmed; the archived unseeded set is not pooled because it was generated on the pre-W1 ZH/VH workspaces (WH only could be pooled, not done).\n* T1: seeds: toys.py now seeds np.random per chunk (pyhf uses the global RNG); the first production is archived (work/toys_prefix/) and ALL q0/qmu toys were rerun on the corrected workspaces (see W1); the lambda toys were already seeded (default_rng(seed)).
* T2: ZH toy Z0: tie-aware p_mid treatment with an explicit 1e-6 tie width, exact-zero fractions and the raw strict-median alternative reported, range always brackets the central value (toys_agg.py).
* T3: mu95 toys: VH grid refined to 5 points x 480 toys per hypothesis, straight-line fit of ln CLs vs mu with fit error instead of a plateau grid value ('confirmed' not used).
* T4: the missing chunk 913378.175 (mu 8.5 sb seed 1001) ended without an output file (cause not diagnosed: job log shows return value 0); all qmu toys were rerun (new production 913406), nothing depends on it.
* T5: ranges sorted (no negative errors); the WH kW-sign lambda toy bracket error 0 is flagged as a plateau (n_distinct_q, plateau flag in toys_summary_v12.json).
* T6: ZH lambda toy caveat (91 % of the toys have q < 1) and the grid-minimum base of q documented.


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
