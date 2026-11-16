# STATUS wh multi_r1 FINAL-R3 (executor-wh), 2026-11-16: DONE except pending items below; nothing running.
S1 closed: 913943 outputs complete (rc 0 x4); VH def-a 500 Z0 0.4474 -> 0.4567 (matches the committed workspace), mu95 med 6.51 -> 6.20; 1000b 0.7334 -> 0.7515; 3000a 1.0286 -> 1.0513; 3000b 1.2163 -> 1.2473 (old kept as *_v12_stale.json). All 8 workspaces rebuilt = byte-identical to committed (W1 changes no workspace content); couplings rerun bit-identical.
S2/S3 closed: D49 settled by D50 = option 4 everywhere (grep D49 + open/interim returns nothing in reports, paper, VH_combination, VERIFY_REQUESTs); upper end in 06, 07, FINAL, VH_combination, paper T4c.
Toys now: VH asymptotic Z0 0.457 vs toy 0.406 (asymptotic 12.6 % above); mu95 VH 6.20 vs toy 6.41 +- 0.35; WH 6.64 vs 8.38 +- 1.11 (1.6 sigma, not validated, fit error understated: same seeds per mu point).
finish_toys.sh and paper/regenerate.sh run (rc 0); compile_check.json 20/20 OK; 621 numbers, 0 missing.
8157 vs 8158 traced: the 5-step cutflow lacks the final MET/pTl/mT>0 cuts; one signal row (w 7.6e-5) has mT = 0.0 and fails mT > 0 (stated in T2-WH caption).
R3 old->new VERIFY lists: wh/VERIFY_REQUEST_{workspace,toys,paper,production_reeval}.md (R3 sections).
Pending: VH nuisance ranking not delivered (913470.001 removed once by SYSTEM_PERIODIC_REMOVE ~24 h; limitation stated); ANALYSIS_COMMIT pin by the orchestrator, then rerun finish_toys.sh + regenerate.sh. Kappa/lambda figures only at 500 fb-1.
