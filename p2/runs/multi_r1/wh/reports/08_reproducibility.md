# 08 Reproducibility (executor-wh FINAL)
Date UTC: 2026-11-13 18:23. Analysis commit: ORCH_COMMIT_PLACEHOLDER. Status: **PASS (independent re-derivation of the counting numbers only; PL, couplings and combination were reproduced by the verifier agent)**.
## Versions
LCG_110 (x86_64-el9-gcc13-opt): Python 3.13, ROOT/uproot/awkward as in p2/lib/scripts/setup_stack.sh; pyhf 0.7.6, xgboost 2.1.3, scipy 1.17.1, numpy; MG5_aMC v3.6.3, Pythia 8.317 (CP5), Delphes 3.5.1, NNPDF3.1 NNLO (LHAPDF 303600) for the production (wh-prod-v1). Seeds: production seeds in SAMPLES.csv; skim RNG seed = file seed + 777; MVA seeds 11, 22, 33; no toys (Asimov).
## Command chain (all under p2/runs/multi_r1/wh; stack via scripts/envrun.sh)
1. veto_validation.py; rate_genuine.py (condor job_py.sh, make_sub_py.py) -> rate_table.py; skim.py (condor) -> work/bgmodel/skim/.
2. bg_yields.py -> work/bgmodel/yields.json; make_report_05a.py -> reports/05a_background_model.md.
3. sel_tables.py -> work/sel/table.npz; sel_scan.py (cut-based, pre-declared grid); sel_mva.py (K=5 nested); sel_final.py; sel_diag_deta.py; reports/05_selection.md.
3b. v1.1 chain: F_QCD_llajj_loose production cluster 899916 (test 899914), validate_v11.py, skim cluster 899980, bg_yields.py --v11 --tag _v11, `V11=1 sel_tables.py` (table_v11), sel_v11.py (frozen cuts/models, D45 check), v11_crosscheck.py; v1.1 manifest: SAMPLES.csv sha256 ebe54517cd0b7869c3a4da6a1190f7589b5187666359d9b023b113f98d2e0342, SHA256SUMS f964e6532b8cd926d5b16cd9ed17c7e3c4141f0f41deb658e36ca7ba7b9e90db (work/v11_manifest_{before,after}.txt; v1 prefix byte-identical); H_ggF_jj fallback: ggf_ul.py, ggf_variant.py.
4. stat_run.py tasks (condor job_stat.sh, clusters 899918/899919): counting, pl:<L>:<a|b>, d36:*, reso, bounds, rank; coup_run.py (local, seconds); comb_run.py (condor 899921, v1.1: 899982), make_zh_table.py (VH_inputs_zh.json from zh_corrected_inputs.json), comb_lambda.py, make_comb_md.py -> p2/combination/VH_combination.*; make_report_07.py -> reports/06_systematics.md, 07_sensitivity.md; make_figs.py -> figures/.
## Independent re-derivation
scripts/repro_counting.py recomputes s and the class-resolved b in the counting window directly from the skims with bgmodel.regions (no sel_tables/stat_lib): s = 0.61229 (table 0.61229), b = 1.79710 (table 1.79710). Cut-based Eq. 1 Z = 0.4339 reproduced; the pyhf stat-only Z0 equals the binned Asimov formula (0.446, checked), and mle.fit returns -2 ln L (factor-2 bug found and fixed before any result was used).
## Checks performed
Sum w/N vs SAMPLES sigma for every row (05a); closure of the quadratic coupling parametrisation (07); unsmoothed-template bias found and fixed (06); pre-declaration order (05 sec. 0; not committed before the scan, stated); validation by ClusterId in the shared log prod_Q_aajjj.log for 899916 (its own log from now on).
## Not reproduced / pending
none for the production (H_ggF_jj: D38 fallback applied; F_QCD_llajj_loose integrated: work/v11_*.json, selection_v11.json); the MVA alternative has no statistics-stage results (D44).
