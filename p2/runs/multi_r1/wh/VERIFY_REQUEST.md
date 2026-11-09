# VERIFY_REQUEST (executor-wh FINAL): block 1 v2 = background model after review HOLD, 2026-11-09
Report: reports/05a_background_model.md (changelog at top). Code: scripts/{bgmodel,bg_yields,skim,make_report_05a}.py (+ rate_genuine, rate_table, veto_validation). Data: work/bgmodel/yields.json, bg_yields.log. No new condor jobs (skims unchanged; only bgmodel.py/bg_yields.py changed).
Verify independently:
1. Frozen-row normalisation per directory (dkey) and C factors/ranges (bgmodel.CFAC, cvec): expected PEAK eFake 2.41 (C=1) / 3.38 (C central), Zaajj EW 0.113; sum w/N table vs SAMPLES.
2. D35 bounds (x0.3 / x3), robustness variants labelled, heavy-flavour factorised variant, class bounds composition in bg_yields.run (non-closure 0.4 one-fake, floor 0.2, direct count).
3. Closure numbers (6/15.3 PRE, 3/7.4 VBS) and zero-support ULs (direct variation).
4. Pre-declared nuisance list in 05a is complete vs review items 4,5,9.
Open human: D39, D40, D35 reading (question a), question (c). H_ggF_jj pending (893012). Selection not started.
