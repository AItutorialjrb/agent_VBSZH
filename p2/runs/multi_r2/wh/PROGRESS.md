# wh PROGRESS (multi_r2, executor-wh)
| item | status |
|---|---|
| read SPEC_G0/handoff/lib | done |
| parse audit, 13 cards (work/p01/parse) | done PASS |
| model widths W/Z, WF | done |
| LO sigma runs (15 validation runs incl. 2nd seeds, fixed-scale closure) | done |
| PY8 H->gg forced check | done |
| reports/01_signal_definition.md, INDEX, STATUS | done; Phase 01 PASS; stopped |
| P02: 26 cards (scripts/make_cards_p02.py -> cards/phase02/{prod,parse,val}), registry idx, BR ledger (scripts/br_ledger.py -> config/br_ledger.json) | done |
| P02: parse audits 25 cards (work/p02/parse, parse_summary.txt) all rc=0 | done |
| P02: short LO sigma runs, 25 val cards (work/p02/val): 18 ok; 7 timed out at 2400 s (6 Wggjj variants, W+4j) | done; see report |
| P02: frozen ZH lost-lepton coverage (scripts/zh_lostlepton_coverage.py, work/p02/zh_coverage.json, zh_lostlep_table.md) | done |
| P02: extra cards H_VBF_Hjj, T_ttjj_1l, H_QCD_ZHjj_tautau: val runs | done (VBF 4099 fb, ZHjj tautau 5.07 fb; ttjj sigma estimate 9.04e4 fb, event run timed out) |
| P02: fake bounds (scripts/fake_bounds.py), numbers table, report 02, registry yaml, INDEX, STATUS | done; Phase 02 PASS, stopped |
| P03: 30 condor test jobs submitted (cluster 900153; manifest config/p03_condor_manifest.json; scripts/p03_submit.py, scripts/condor/p03_job.sh; new cards S_EW_WHjj_Wlnu, H_QCD_WHjj_Wlnu) | running |
| P03: condor 900153 (30 jobs) analysed: sigma closure, BR, Delphes validation, twins; report 03 written (8 jobs still running) | done |
