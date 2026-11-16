# verify_R2_production_d49 (haiku verifier, FINAL-R2, 2026-11-16) — saved by the orchestrator (verifier read-only)
VERDICT: FAIL (sev-1: 1)
1. [sev-1] D49 option 4 (D50) not reflected in headline reports: still "OPEN", central Z0/mu95 only, no upper-end row — wh/reports/FINAL_report.md:17; 05a_background_model.md:259; 06_systematics.md:77,108; 07_sensitivity.md:20,48,76; paper T4_Z_mu95.tex. Upper end (0.309/10.9 @500, 0.400/8.32 @1000, 0.544/6.45 @3000) only in STATUS.md:4 and VERIFY_REQUEST_production_reeval.md:32-37; VERIFY_REQUEST.md:6 says "Open".
2. [sev-2] VH ranking limitation (vh_rankvh_v12.json missing) only in STATUS/VERIFY_REQUEST_production_reeval; absent from VERIFY_REQUEST.md, VH_combination.md Limitations, paper README/tables; make_paper.py:107-115 silently skips VH T5. rank_v12.json complete (22 rows) feeds T5_WH.
3. [sev-2] ANALYSIS_COMMIT pin open (orchestrator step).
4. [sev-3] "913470 exceeded wall time twice" not confirmed: py_stat.log shows 913470.000 (WH rank) rc 0; 913470.001 (rankvh) removed by SYSTEM_PERIODIC_REMOVE once (11/16 02:25, ~24 h).
5. [sev-3] condor_history timed out; job logs confirm all return 0 (nomjj 52, loose top-up 44).
6. [sev-3] "Garwood 68 %" is 1σ (p=0.158655): [0.02095,0.39995]; exact 68 % [0.0211,0.3987]. 95 % [0.003069,0.675434] reproduced (w=0.121224).
7. [sev-3] Y0 uses gridpack σ 1.679 pb; closure σ gives 0.12101 (−0.17 %); V1.2_NOTES ratio 1.0856 vs 1.085.
8. [sev-3] 05a:259 calls the 0.176 cross-check "independent"; align wording (config use_vbs_x_C=false, OK).
9. [sev-3] ZH_Zaajj_QCD_nomjj_lostlep N_eff 2.0 (yield 0.0029) not called out.
PASS: changed numbers vs source keys (selection_v12, v12_lostlep_neff, 9 ll4 rows); D49 floor n=1 rel 1.00 > 0.30; N rule (nomjj 2.6e6 ≥ 2.447e6; loose 7.5e6 ≥ 5.037e6); seeds distinct; SHA256SUMS 3092 lines, no dups; class N_eff ≥ 10 except lost-lepton (11.2, one-event dominated, stated); D45 trigger evaluated (False), stated 05a:247.
