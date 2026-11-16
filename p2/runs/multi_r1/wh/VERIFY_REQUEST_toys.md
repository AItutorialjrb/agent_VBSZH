# VERIFY_REQUEST: toy validation of the asymptotic numbers (A4, D47 (2))
Scripts: wh/scripts/toys.py (q0, q0 null, qmu), vh_coup.py --toys, toys_agg.py; condor job_toys.sh (clusters 913374 q0 s+b + lambda toys, 913378 qmu, 913379 q0 null); inputs the committed workspaces. Checks: toy generation (nuisances at nominal + auxiliary data thrown for q0/qmu; all constrained nuisances thrown for the lambda toys), the CLs construction and bootstrap errors, the discrete-q plateau remark, HEADLINE: the asymptotic Z0 (pre-declared) is the quoted headline, the toy expected Z0 (Z = Phi^-1(1-p), p from the null toys at the median s+b q0) is the validation: WH 0.41 vs 0.43 agree, VH 0.41 vs 0.46 (asymptotic about 11 % above the toy; the toy is the more reliable single number), ZH toy 0 (median q0 = 0) vs 0.13. ZH lambda=-1 toys: q is DISCRETE at these counts, the toy Z is sqrt of the 50 % quantile of q over 5000 toys (a plateau value 0.66) against the Asimov 0.084: at q < 1 the median is fluctuation-dominated and the two are not comparable; no ZH lambda sensitivity either way.

| quantity | old | new | source key (new; old in the same file family) |
|---|---|---|---|
| Z0 WH: asymptotic -> toys (null toys) | 0.438 | 0.406 | toys_summary_v12.json::q0/WH range [0.37857969874529823, 0.4357749779926946]; N = 2000 s+b, 2000 null |
| Z0 ZH: asymptotic -> toys (null toys) | 0.131 | 0.000 | toys_summary_v12.json::q0/ZH range [0.0, 0.0]; N = 2000 s+b, 2000 null |
| Z0 VH: asymptotic -> toys (null toys) | 0.457 | 0.406 | toys_summary_v12.json::q0/VH range [0.36648929388943374, 0.44129423383055216]; N = 2000 s+b, 2000 null |
| mu95 WH: asymptotic -> toys | 6.637 | 8.375 | toys_summary_v12.json::mu95/WH straight-line fit +- 1.11 |
| mu95 ZH: asymptotic -> toys | 32.259 | 34.287 | toys_summary_v12.json::mu95/ZH straight-line fit +- 1.93 |
| mu95 VH: asymptotic -> toys | 6.197 | 6.407 | toys_summary_v12.json::mu95/VH straight-line fit +- 0.35 |
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
| VH Z0 asymptotic (def a, 500) in toys table / T10 / VH_combination | 0.4474 | 0.4567 | toys_summary_v12.json::q0/VH/Z0_asimov |
| VH asymptotic over toy Z0 (toy 0.406 unchanged) | +0.103 | +0.126 | toys_summary_v12.json::q0/VH (percentage above the toy value) |
| VH mu95 asymptotic (def a, 500) | 6.512 | 6.197 | toys_summary_v12.json::mu95/VH/mu95_asymptotic |
| VH mu95 toy fit minus asymptotic [sigma_fit] | -0.3 | +0.6 | toys_summary_v12.json::mu95/VH (toy 6.41 +- 0.35 unchanged) |
