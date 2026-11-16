# VERIFY_REQUEST: joint WH+ZH likelihood and combination (A3)
Files: p2/combination/vh_ws/{VH_workspace,VH_workspace_2d,VH_workspace_defb,VH_workspace_2d_defb,WH_workspace,ZH_workspace}.json + correlation_scheme.json (built by wh/scripts/vh_build.py, vh_run.py, vh_scheme.py, vh_coup.py); VH_combination.{md,json,csv} (make_vh_md.py, make_vh_json.py). Checks: reload VH_workspace.json in pyhf and refit Z0/mu95 (expected 0.447 / 6.51 at 500, def a); the cross-feeds (EW ZHjj lost-lepton rows are signal-like, WH signal in the ZH SR has zero MC support); correlated names (correlation_scheme.json) vs the declared scheme; ZH q-curves re-derived (compare with the ZH executor's pyhf curves 0.29 sigma at lambda=-1); same sign convention and R_BR in both channels; tau_r_zrows; (mu_WH, mu_ZH) maps (vh_map2d_*_v12.json).

| quantity | old | new | source key (new; old in the same file family) |
|---|---|---|---|
| WH Z0, 500, (a) | 0.4273 | 0.4381 | vh_z0mu_500_a_wh_v12.json::Z0 (old comb_500_a_v11.json::WH/Z0) |
| WH mu95, 500, (a) | 7.094 | 6.637 | vh_z0mu_500_a_wh_v12.json::mu95/1 |
| VH Z0, 500, (a) | 0.4444 | 0.4567 | vh_z0mu_500_a_both_v12.json::Z0 (old: additive v1.1 combination, counting ZH channel) |
| VH mu95, 500, (a) | 6.521 | 6.197 | vh_z0mu_500_a_both_v12.json::mu95/1 |
| ZH alone Z0 / mu95, 500, (a) | 0.131 / 31.8 | 0.131 / 32.3 | vh_z0mu_500_a_zh_v12.json (old: frozen-code table in comb_*_v11.json::ZH_alone_table) |
| WH Z0, 500, (b) | 0.484 | 0.4993 | vh_z0mu_500_b_wh_v12.json::Z0 (old comb_500_b_v11.json::WH/Z0) |
| WH mu95, 500, (b) | 6.044 | 5.812 | vh_z0mu_500_b_wh_v12.json::mu95/1 |
| VH Z0, 500, (b) | 0.5219 | 0.5406 | vh_z0mu_500_b_both_v12.json::Z0 (old: additive v1.1 combination, counting ZH channel) |
| VH mu95, 500, (b) | 5.539 | 5.185 | vh_z0mu_500_b_both_v12.json::mu95/1 |
| ZH alone Z0 / mu95, 500, (b) | 0.210 / 20.3 | 0.210 / 20.7 | vh_z0mu_500_b_zh_v12.json (old: frozen-code table in comb_*_v11.json::ZH_alone_table) |
| WH Z0, 1000, (a) | 0.5922 | 0.6084 | vh_z0mu_1000_a_wh_v12.json::Z0 (old comb_1000_a_v11.json::WH/Z0) |
| WH mu95, 1000, (a) | 4.539 | 4.283 | vh_z0mu_1000_a_wh_v12.json::mu95/1 |
| VH Z0, 1000, (a) | 0.6163 | 0.6345 | vh_z0mu_1000_a_both_v12.json::Z0 (old: additive v1.1 combination, counting ZH channel) |
| VH mu95, 1000, (a) | 4.161 | 4.022 | vh_z0mu_1000_a_both_v12.json::mu95/1 |
| ZH alone Z0 / mu95, 1000, (a) | 0.184 / 18.8 | 0.184 / 19.1 | vh_z0mu_1000_a_zh_v12.json (old: frozen-code table in comb_*_v11.json::ZH_alone_table) |
| WH Z0, 1000, (b) | 0.6708 | 0.6932 | vh_z0mu_1000_b_wh_v12.json::Z0 (old comb_1000_b_v11.json::WH/Z0) |
| WH mu95, 1000, (b) | 3.965 | 3.739 | vh_z0mu_1000_b_wh_v12.json::mu95/1 |
| VH Z0, 1000, (b) | 0.7243 | 0.7515 | vh_z0mu_1000_b_both_v12.json::Z0 (old: additive v1.1 combination, counting ZH channel) |
| VH mu95, 1000, (b) | 3.628 | 3.355 | vh_z0mu_1000_b_both_v12.json::mu95/1 |
| ZH alone Z0 / mu95, 1000, (b) | 0.295 / 11.9 | 0.295 / 12.2 | vh_z0mu_1000_b_zh_v12.json (old: frozen-code table in comb_*_v11.json::ZH_alone_table) |
| WH Z0, 3000, (a) | 0.9734 | 1.007 | vh_z0mu_3000_a_wh_v12.json::Z0 (old comb_3000_a_v11.json::WH/Z0) |
| WH mu95, 3000, (a) | 2.499 | 2.303 | vh_z0mu_3000_a_wh_v12.json::mu95/1 |
| VH Z0, 3000, (a) | 1.014 | 1.051 | vh_z0mu_3000_a_both_v12.json::Z0 (old: additive v1.1 combination, counting ZH channel) |
| VH mu95, 3000, (a) | 2.366 | 2.173 | vh_z0mu_3000_a_both_v12.json::mu95/1 |
| ZH alone Z0 / mu95, 3000, (a) | 0.314 / 8.8 | 0.313 / 9.0 | vh_z0mu_3000_a_zh_v12.json (old: frozen-code table in comb_*_v11.json::ZH_alone_table) |
| WH Z0, 3000, (b) | 1.103 | 1.148 | vh_z0mu_3000_b_wh_v12.json::Z0 (old comb_3000_b_v11.json::WH/Z0) |
| WH mu95, 3000, (b) | 2.163 | 2.002 | vh_z0mu_3000_b_wh_v12.json::mu95/1 |
| VH Z0, 3000, (b) | 1.195 | 1.247 | vh_z0mu_3000_b_both_v12.json::Z0 (old: additive v1.1 combination, counting ZH channel) |
| VH mu95, 3000, (b) | 1.914 | 1.803 | vh_z0mu_3000_b_both_v12.json::mu95/1 |
| ZH alone Z0 / mu95, 3000, (b) | 0.502 / 5.5 | 0.500 / 5.7 | vh_z0mu_3000_b_zh_v12.json (old: frozen-code table in comb_*_v11.json::ZH_alone_table) |
| VH lambda=-1 / lambda<0 Z, 500, kZ-sign (primary) | 3.788 / 0.373 | 3.776 / 0.381 | couplings_vh_kzneg_v12.json::curves/VH (old: v1.1 additive q_WH + q_ZH(frozen curves)) |
| VH lambda=-1 / lambda<0 Z, 500, kW-sign | 6.250 / 0.385 | 6.241 / 0.399 | couplings_vh_v12.json::curves/VH (old: v1.1 additive q_WH + q_ZH(frozen curves)) |
| VH lambda=-1 / lambda<0 Z, 1000, kZ-sign (primary) | 5.314 / 0.514 | 5.296 / 0.525 | couplings_vh_kzneg_L1000_v12.json::curves/VH (old: v1.1 additive q_WH + q_ZH(frozen curves)) |
| VH lambda=-1 / lambda<0 Z, 1000, kW-sign | 8.673 / 0.534 | 8.653 / 0.553 | couplings_vh_L1000_v12.json::curves/VH (old: v1.1 additive q_WH + q_ZH(frozen curves)) |
| VH lambda=-1 / lambda<0 Z, 3000, kZ-sign (primary) | 8.916 / 0.822 | 8.877 / 0.837 | couplings_vh_kzneg_L3000_v12.json::curves/VH (old: v1.1 additive q_WH + q_ZH(frozen curves)) |
| VH lambda=-1 / lambda<0 Z, 3000, kW-sign | 14.103 / 0.869 | 14.040 / 0.901 | couplings_vh_L3000_v12.json::curves/VH (old: v1.1 additive q_WH + q_ZH(frozen curves)) |
| ZH-alone lambda=-1 Z (re-derived, kZ-sign, 500) | 0.429 | 0.2896 | couplings_vh_kzneg_v12.json::curves/ZH/Z_lambda_m1 (old: frozen ZH final.json coupling lambda|500|fixed corrected) |

## R2 (verifier W1-W6 fixes)
* W1: the ZHjj cross-feed was SMOOTHED as a non-resonant row (stat_lib RESONANT now contains zhjj_ew, zhjj_qcd); workspace yield 0.0184 (100-180), 0.0151 (122-128), 0.0178 (120-130), unbinned +-3.5 GeV 0.0162, coupling-template (K_EW_ZHjj_lam_p100, a different sample) 0.0159: region, window and sample stated in VH_combination.md (work/stat/xfeed_v12.json). All VH numbers re-run (old -> new in the table above are the R2 values).
* W2: ZH j->gamma fake scales renamed by the ZH executor (scale_zjfake_qcd_zh, scale_zjfake_ew_zh): decorrelated from WH e->gamma scales; correlation_scheme.json and the VH_combination.md table regenerated (no effect on Z0).
* W3: 2D workspaces now declare measurement m_2d_mu_WH with POI mu_WH (stat_lib spec), usage recorded in VH_combination.md.
* W4: compatibility test q = -2 ln[L(common)/L(mu_WH, mu_ZH)] (chi2 1 dof) with expected sensitivity points (p = 0.05 at q = 3.84): work/stat/vh_map2d_*_v12.json::compat.
* W5: mu95 uses a refined scan (stat_lib.mu95_expected: 9-point fine grid inside the bracketing interval); all mu95 numbers re-run.
* W6: tolerances and window-edge conventions stated (VH_combination.md).


## R3 (verify_R2 sev-1 S1-S3 and sev-2/3 fixes)
* S1: W1 (RESONANT) does NOT change the workspace content: all 8 workspaces rebuilt with the current code (vh_run.py ws) are BYTE-IDENTICAL to the committed ones (copies of the previous ones in work/vh_ws_prev_20261114/; the file mtime 11-15 00:10 of stat_lib.py was the mu-bound edit 50 -> 200). The stale items were the four vh_z0mu_*_both_v12.json outputs (the 913430 'both' jobs hit the 2 h limit); rerun as cluster 913943 (flavour tomorrow); old files kept as *_v12_stale.json. The couplings/lambda inputs (vh_coup.py, zh_channel_inputs.json) were rerun with the current code and are bit-identical, so the lambda toys (generated earlier) remain valid; the map2d/compat files post-date the workspaces and are unchanged.
* S2/S3: D49 is settled by D50 = option 4 in FINAL, 05a, 06, 07, VH_combination, VERIFY_REQUEST, paper T3/T4c/T11 (upper end Z0/mu95 at 500/1000/3000, interval 95 % [0.0031, 0.675], the 68 % interval is relabelled 1-sigma central); 0.176 [0.094, 0.257] called a cross-check.
* Sev-2: VH ranking not delivered (VH_combination limitations, README, T5 captions, placeholder row T5-VH, T11); D47 (3) limitations table T11 + README; kappa at 1000 in T7b; ZH non-prompt lepton class stated as unestimated and unbounded; T2-ZH labelled frozen basis + corrected fake-row cutflow T2b; basis statement (T4 joint 0.438/6.64 vs stand-alone 0.428/6.81); kW-sign convention beside every number (T7, T9, T10, VH_combination) with the D46 range 5.1-7.1; T5-ZH caption; ZH lambda toy 'not comparable'; mu95 toy statement (1.6 sigma, seeds reused, non-monotone CLs, not validated); def a: SR ZHjj-QCD is background, correlation_scheme 'tau' text aligned.
* Sev-3 done: T2-ZH and T3 literals registered, Y0 -0.17 % normalisation note, ZH toy Z0 clipping stated, toy err defined, edge-limited intervals marked, Eq. 1 defined, CMS reference by DOI, T1 k column and pre-decay sigma defined, N_eff 2.0 of ZH_Zaajj_QCD_nomjj_lostlep called out, make_verify_requests KeyError fixed. Not done: signal raw count 8157 (class table) vs 8158 (selection_v12 total) is a counting convention difference not traced; figures for kappa/lambda remain at 500 fb-1 only.

| quantity | old | new | source key (new; old in the same file family) |
|---|---|---|---|
| VH Z0 / mu95 (-1s, med, +1s), 500, (a) [STALE file replaced] | 0.4474 / 4.09, 6.51, 10.65 | 0.4567 / 4.00, 6.20, 9.97 | vh_z0mu_500_a_both_v12.json (old: vh_z0mu_500_a_both_v12_stale.json, predates VH_workspace.json) |
| VH Z0 / mu95 (-1s, med, +1s), 1000, (b) [STALE file replaced] | 0.7334 / 2.36, 3.58, 5.54 | 0.7515 / 2.22, 3.36, 5.25 | vh_z0mu_1000_b_both_v12.json (old: vh_z0mu_1000_b_both_v12_stale.json, predates VH_workspace.json) |
| VH Z0 / mu95 (-1s, med, +1s), 3000, (a) [STALE file replaced] | 1.0286 / 1.56, 2.32, 3.56 | 1.0513 / 1.47, 2.17, 3.31 | vh_z0mu_3000_a_both_v12.json (old: vh_z0mu_3000_a_both_v12_stale.json, predates VH_workspace.json) |
| VH Z0 / mu95 (-1s, med, +1s), 3000, (b) [STALE file replaced] | 1.2163 / 1.28, 1.88, 2.82 | 1.2473 / 1.22, 1.80, 2.74 | vh_z0mu_3000_b_both_v12.json (old: vh_z0mu_3000_b_both_v12_stale.json, predates VH_workspace.json) |
| number of WH-alone / ZH-alone z0mu files whose Z0 changed | -- | 0 | vh_z0mu_*_{wh,zh}_v12.json vs *_stale (these were already computed on the committed workspaces) |
| couplings_vh: max |Delta Z_lambda_m1| over WH/ZH/VH | -- | 0.00e+00 | couplings_vh_v12.json vs _stale (rerun with the current code) |
| couplings_vh_L1000: max |Delta Z_lambda_m1| over WH/ZH/VH | -- | 0.00e+00 | couplings_vh_L1000_v12.json vs _stale (rerun with the current code) |
| couplings_vh_L3000: max |Delta Z_lambda_m1| over WH/ZH/VH | -- | 0.00e+00 | couplings_vh_L3000_v12.json vs _stale (rerun with the current code) |
| couplings_vh_L140: max |Delta Z_lambda_m1| over WH/ZH/VH | -- | 0.00e+00 | couplings_vh_L140_v12.json vs _stale (rerun with the current code) |
| couplings_vh_kzneg: max |Delta Z_lambda_m1| over WH/ZH/VH | -- | 0.00e+00 | couplings_vh_kzneg_v12.json vs _stale (rerun with the current code) |
| couplings_vh_kzneg_L1000: max |Delta Z_lambda_m1| over WH/ZH/VH | -- | 0.00e+00 | couplings_vh_kzneg_L1000_v12.json vs _stale (rerun with the current code) |
| couplings_vh_kzneg_L3000: max |Delta Z_lambda_m1| over WH/ZH/VH | -- | 0.00e+00 | couplings_vh_kzneg_L3000_v12.json vs _stale (rerun with the current code) |
| couplings_vh_kzneg_L140: max |Delta Z_lambda_m1| over WH/ZH/VH | -- | 0.00e+00 | couplings_vh_kzneg_L140_v12.json vs _stale (rerun with the current code) |


R3 downstream (VH headline from the replaced both-files; paper T4/T10 and VH_combination read the same keys):

| quantity | old | new | source key (new; old in the same file family) |
|---|---|---|---|
| VH Z0 asymptotic (def a, 500) in toys table / T10 / VH_combination | 0.4474 | 0.4567 | toys_summary_v12.json::q0/VH/Z0_asimov |
| VH asymptotic over toy Z0 (toy 0.406 unchanged) | +0.103 | +0.126 | toys_summary_v12.json::q0/VH (percentage above the toy value) |
| VH mu95 asymptotic (def a, 500) | 6.512 | 6.197 | toys_summary_v12.json::mu95/VH/mu95_asymptotic |
| VH mu95 toy fit minus asymptotic [sigma_fit] | -0.3 | +0.6 | toys_summary_v12.json::mu95/VH (toy 6.41 +- 0.35 unchanged) |
