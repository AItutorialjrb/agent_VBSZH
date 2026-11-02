# production_v2 gridpack cards — UNVALIDATED
Generated from the Phase-02 ledger (config/sample_matrix_phase02.yaml, numbers in config/production_v2.yaml).
Build with scripts/condor/gridpacks_v2.sub; a sample becomes production-ready only after (1) its gridpack job
succeeds, (2) σ is consistent with reports/03_generation_validation.md where measured, and (3) one test job via
scripts/condor/test_v2.sub passes. Splits: B_EW_llaajj_is1-4 and B_QCD_llaa_2j_is1-4 are disjoint beam-1 parton
classes (closure test on Z+2j: -1.4 %, pull -2.1 — recheck at higher precision). *_check samples validate dropping
the 0/1-jet ME bins in the fake samples. MLM: xqcut 10 GeV; Pythia qCut 19 GeV (py8_mlm_*.cmnd), DJR check pending.
H_ggZH uses loop_sm + MadSpin (syntax untested).
