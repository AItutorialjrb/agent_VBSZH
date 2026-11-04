# WH reports index (multi_r1)
| Phase | Report | Status | Note |
|---|---|---|---|
| 01 | 01_signal_definition.md | PASS (G1: PASS) | light-flavour EW (0,4) W±Hjj; WF = 0.9601; closure ±2 % (W⁻ deficit cause not established) |
| 02 | 02_background_overlap.md (+ config/sample_matrix.yaml, sample_registry.yaml) | PASS-with-conditions | no-mjj nominal samples (D8), D-WH-0/2/3/5 implemented; σ of B_EW/F_EW nomjj, F_Wjjjj, T_ttjj, V_*_WH pending; D-WH-11/12/13 open |
| 03 | 03_generation_validation.md | IN-PROGRESS | PASS only when every sample type has a verified test job: 31 types submitted (clusters 884456/884457/884934/884935/884936); waiting on clusters; verifier audit pending |
| 04 (pre-G2) | 04_production_plan.md | PARTIAL (G2 deliverable, rows with PENDING σ/N) | plan tables, nmc_check, deviations, submission plan; no bulk production submitted |
Templates: reports/0[234]_*.md.in; regenerate with scripts/assemble_reports.py (+ scripts/make_plan.py). Git commit: recorded by orchestrator.
