# Phase 02 candidate cards — **UNVALIDATED**
Process definitions for the ledger in `reports/02_background_overlap.md` / `config/sample_matrix_phase02.yaml`.
None of these has been generated except where `reports/03_generation_validation.md` says so
(H_QCD fixed-order ZHjj, B_EW_llaajj and B_QCD_llaa_mlm smoke tests live in `cards/phase03_smoke/`).
Known open points: decay-chain photon radiation in top samples; tWγ DR/DS; loop_sm ggZH syntax and
Z decay route; MLM xqcut/qCut need DJR validation; `l+ l- l+ vl a` uses an `l+` multiparticle twice
(includes same- and different-flavour combinations; check symmetry factors). Do not run in production
before a Phase 03b smoke test passes for each.
