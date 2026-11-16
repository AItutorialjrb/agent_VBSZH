# multi_r3 WH G1 — verifier result (transcribed by orchestrator from verifier return; verifier is read-only)
| # | Item | Result | Evidence |
|---|---|---|---|
| 1 | Clusters 899739/899740 exit codes, event counts | PASS | wh/work/condor/gridpacks_test.log, test_jobs.log: all 8 jobs return 0, one submission each; 899740 4 holds ("gridpack not yet available", code 3) released; 2000/2000/2000 req/LHE/Delphes (wrapper JSON). condor_history timed out -> user logs only |
| 2 | Sum of ALL <init> rows vs reported σ | FAIL (labelling), no >1% mismatch | col-1 sums: S_EW 28.171 fb, H_QCD 59.287, ttH 108.029, B 4.6812; reported 28.32/59.42/108.17/4.681 are col 3 (total, repeated per row). Δ -0.5/-0.2/-0.1/0.0 %. wh/reports/03_generation_validation.md §2, wh/config/br_ledger.json source text wrong |
| 3 | PY8 sigmaGen vs LHE | PASS | S_EW 28.24±0.05, H_QCD 59.31±0.08, ttH 108.2±0.14, B 4.681±0.015 fb; vs col-1 sum +0.25/+0.04/+0.16/0.0 % |
| 4a | N_req recomputed (9 rows) | PASS | wh/config/br_ledger.json (T_tta 1207739; T_tWa 179617; F_Wajj 24162245; F_Wjj 6921191318; others 50000) |
| 4b | WF, B_gg once per sample | PASS structural / FAIL claim | only consumer wh/scripts/br_ledger.py; WF=0.960076; docstring line 2 says "asserted" but no assert statement |
| 5a | Seed formula SPEC_G0 §3.4 (P=2,R=3) | PASS | wh/config/sample_registry.py vs scripts/condor/*.sub |
| 5b | Seed uniqueness | PASS | 69 seeds unique in [2.3M,2.4M); make_submit.py:14 asserts |
Follow-ups: relabel/recompute σ from col 1; add the assert in br_ledger.py; mg_seed field holds test-job seed (naming); Delphes ROOT entries taken from wrapper JSON, not read from ROOT files.
