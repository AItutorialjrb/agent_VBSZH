# 08 Reproducibility (executor-wh FINAL)
Date UTC: 2026-11-09 10:11. Status: **PASS (independent re-derivation of the headline numbers); full independent verification = verifier agent**. Git commit: see orchestrator commit.
## Versions
LCG_110 (x86_64-el9-gcc13-opt): Python 3.13, ROOT/uproot/awkward as in p2/lib/scripts/setup_stack.sh; pyhf 0.7.6, xgboost 2.1.3, scipy 1.17.1, numpy; MG5_aMC v3.6.3, Pythia 8.317 (CP5), Delphes 3.5.1, NNPDF3.1 NNLO (LHAPDF 303600) for the production (wh-prod-v1). Seeds: production seeds in SAMPLES.csv; skim RNG seed = file seed + 777; MVA seeds 11, 22, 33; no toys (Asimov).
## Command chain (all under p2/runs/multi_r1/wh; stack via scripts/envrun.sh)
1. veto_validation.py; rate_genuine.py (condor job_py.sh, make_sub_py.py) -> rate_table.py; skim.py (condor) -> work/bgmodel/skim/.
2. bg_yields.py -> work/bgmodel/yields.json; make_report_05a.py -> reports/05a_background_model.md.
3. sel_tables.py -> work/sel/table.npz; sel_scan.py (cut-based, pre-declared grid); sel_mva.py (K=5 nested); sel_final.py; sel_diag_deta.py; reports/05_selection.md.
4. stat_run.py tasks (condor job_stat.sh, clusters 899918/899919): counting, pl:<L>:<a|b>, d36:*, reso, bounds, rank; coup_run.py (local, seconds); comb_run.py (condor 899921), make_zh_table.py, comb_lambda.py, make_comb_md.py -> p2/combination/VH_combination.*; make_report_07.py -> reports/06_systematics.md, 07_sensitivity.md; make_figs.py -> figures/.
## Independent re-derivation
scripts/repro_counting.py recomputes s and the class-resolved b in the counting window directly from the skims with bgmodel.regions (no sel_tables/stat_lib): s = 0.61229 (table 0.61229), b = 1.79710 (table 1.79710). Cut-based Eq. 1 Z = 0.4339 reproduced; the pyhf stat-only Z0 equals the binned Asimov formula (0.446, checked), and mle.fit returns -2 ln L (factor-2 bug found and fixed before any result was used).
## Checks performed
Sum w/N vs SAMPLES sigma for every row (05a); closure of the quadratic coupling parametrisation (07); unsmoothed-template bias found and fixed (06); pre-declaration order (05 sec. 0; not committed before the scan, stated); validation by ClusterId in the shared log prod_Q_aajjj.log for 899916 (its own log from now on).
## Not reproduced / pending
H_ggF_jj (893012) integration or D38 fallback (F_QCD_llajj_loose 899916 is integrated: work/v11_*.json, selection_v11.json); the MVA alternative has no statistics-stage results (D44).
