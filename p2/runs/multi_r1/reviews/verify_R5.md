# verify_R5 (haiku verifier, FINAL-R2 R5, 2026-11-16) — saved by the orchestrator
VERDICT: FAIL (one open sev-2 text item; all numbers match their sources)
[sev-2] V3 VH toy-grid change (5×480 → 4×240; 6.41→6.82 mixes workspace and grid) stated only in VERIFY_REQUEST_toys, not in T10/VH_combination/FINAL/T11. -> fixed in the final pinned regeneration (orchestrator grep check).
[sev-3] VH_combination.csv does not exist (files are _lambda.csv, _mu95.csv). [sev-3] compile_check.json has no "missing" field (20/20 OK). [sev-3] final.json:154-198 WH-only keys covered by NOTE_WH_only only.
Check 1 PASS: 140 fb-1 from vh_z0mu_140_a_wh_v12.json (06:50 > 06:35 rebuild), μ95 16.0 in FINAL:14, T9:7; 17.24 gone; stand-alone 500 0.4451/6.58 = T5/T6 captions, FINAL:34.
Check 2 PASS: no stale pre-R4 values in targets; remaining literal hits are current or unrelated quantities (D36 scan points 0.438/0.309, 1000 fb-1 band 6.64, λ grid points, MVA fold Z 0.428).
Check 3 PASS: final.json PRIMARY_joint_basis WH 3.7659, VH 3.7764, kW 6.2036; WH-only relabelled.
Closure: V1, V2, V4 CLOSED; V3 OPEN; recheck 8-13 CLOSED. Compile 20/20.
