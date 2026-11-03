# hh patches (lib/ is read-only; every modification lives here)
| # | File | One-line rationale |
|---|---|---|
| 001 | 001_make_hh_model.sh, 001b_make_loop_model.sh | UFO from built-in sm/loop_sm exposing kV,k2V,kl separately (distinct non-0/1 restrict defaults, else MG5 fixes/merges them) |
| 002 | 002_delphes_card_fatjets.patch | slim_v1 card removed the FatJet branch; re-enable it and add particle-level GenFatJet (R=0.8, soft-drop/nsubjettiness already computed by the stock module); no detector change |
| 003 | 003_patch_cuts_vbs.py | stock MG5 WBF cut acts on the two hardest jets (= Higgs jets in boosted topologies); replace by an any-pair VBS filter (|dy|, mjj via run-card deltaeta/xetamin) |
| 004 | 004_make_gridpack_hh.patch | make_gridpack.sh: unpack UFO_*.tgz, split card at `output` to patch cuts.f, assert iseed==SEED, no-op rerun exits 30 (not 0) |
| 005 | 005a_run_job_hh.patch, 005b_slim_hh_truth.patch | run_job.sh -> hh card + truth script; slim_gentruth (photon overlap truth) replaced by fat-jet/Higgs/top/b-hadron truth and hard-process b counts for truth-tag weighting and QCD flavour partition |
| 006 | 006_nmc_check_hh.py | extended nmc_check: signal N>=max(50k,sigma*BR*L); backgrounds effective-N rule (twin_ok, N_eff>=10 or bound); BR-once ledger assertion; self-test fails loudly |
