# verify_R3 (haiku verifier, FINAL-R2 R3 recheck, 2026-11-16) — saved by the orchestrator
VERDICT: PASS (no sev-1 open; two sev-2 pin items OPEN — orchestrator commit/pin steps)
1. [sev-2] "byte-identical to the committed ones": rebuilt workspaces match work/vh_ws_prev_20261114 (8/8) but differ from git HEAD (WIP c693b76); resolved by the orchestrator commit. OPEN until commit.
2. [sev-2] ANALYSIS_COMMIT placeholder in paper T1..T4c headers and FINAL_report.md:2. OPEN until pin.
3. [sev-3] VERIFY_REQUEST_toys.md header "WH 0.41 vs 0.43", "about 11 %" vs table 0.438 / +12.6 %.
4. [sev-3] FINAL_report.md lacks the VH-ranking limitation (present in VH_combination.md:112, README:14, T5_VH, T11).
5. [sev-3] T4c "Y at 500 fb-1" column repeats 0.1212 in 1000/3000 rows.
6. [sev-3] WH and VH toy p_mid both 685/2000 (coincidence; arrays differ).
7. [sev-3] final.json legacy WH kW λ=-1 6.1973 vs joint 6.2036 (both 6.20; labelled legacy).
8. [sev-3] wh/STATUS.md:3 only "D49 + open" hit (status sentence).
Check 1: VH def-a 500 Z0 reproduced by pyhf 0.45668 = vh_z0mu_500_a_both_v12.json; reruns newer than workspaces; 1000_b 0.75153/3.355, 3000_a 1.05132/2.173, 3000_b 1.24727/1.803 match; no unlabelled stale value; couplings byte-identical to _stale; λ Z values reproduced (all lumis, both conventions).
Check 4: compile 20/20, missing []; 453 direct-key paper_numbers re-resolved exactly.
Check 5: toy vs asymptotic consistent (VH Z0 +12.6 %; μ95 6.197 vs 6.407±0.347; WH 1.6σ "not validated"; ZH λ "not comparable").
Closures: R2 sev-1 (a) stale VH headline CLOSED; (b) D49 option 4 CLOSED. R2 sev-2: VH ranking limitation, D47(3) limitations, κ@1000, ZH non-prompt unestimated, T2_ZH frozen + T2b, T4 vs T5/T6 basis, κW-sign convention + D46 range, T5_ZH caption, ZH λ toy not comparable, μ95 toy wording, def-a zhjj_qcd background: all CLOSED. Commit pin and "committed" wording: OPEN (orchestrator).
