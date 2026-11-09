# PROGRESS (wh, multi_r1)
- 2026-11-03T16:14:48Z Phase 01 START
- 2026-11-03T16:29:27Z smoke sigma runs + PY8/Delphes validation script done (wp light wdec)
- 2026-11-03T16:36:00Z LHE classification (b-class) done; Phase 02/03 cards written (cards/prod, cards/smoke)
- 2026-11-03T16:44:34Z condor: gridpacks cluster 884456 (11 jobs), test jobs submitted (hold-release until gridpack)
- 2026-11-03T16:47:53Z PY8+Delphes validation done wp/wm/tau (1000/1000/500 ev)
- 2026-11-03T16:51:29Z Phase 01 END (report written; bwcutoff row pending)
- 2026-11-03T16:51:29Z Phase 02 START
- 2026-11-03T16:57:16Z released held test jobs with existing gridpacks (S_EW_WHjj, H_QCD_WH_mlm, F_Wjj_pilot)
- 2026-11-03T16:58:47Z report 02 draft (.in) written; awaiting gridpacks/test jobs
- 2026-11-03T17:08:52Z pilot F_Wjj analysed
- 2026-11-03T17:10:07Z Phase 02 END (ledger; sigma of 6 continuum samples pending gridpacks); Phase 03 reports drafted (IN-PROGRESS)
- 2026-11-03T17:10:12Z session end: STATUS/VERIFY_REQUEST/INDEX written; Phase 03 IN-PROGRESS
- 2026-11-03T17:19:33Z verifier FAIL items fixed; VERIFY_REQUEST #2
- 2026-11-03T21:50:27Z Phase 03 NOT complete: B_EW_Waajj_vbs gridpack pending; reports/03 finalised as IN-PROGRESS; extra tests B_QCD vbs/nomjj, twin numbers done
- 2026-11-03T21:59:27Z G1 review fixes applied (items 1-9,11-14, F-1); Phase 03 still IN-PROGRESS (no end time)
- 2026-11-03T22:29:54Z ROLE=executor-wh PHASE=PRE-G2: seeds.py + preG1 list; cards (nomjj EW twins, V_WZa/WWa/ZZa_WH, F_Wjjjj, T_ttjj_1l); submitted gridpacks 884934 (16), tests 884935 (21, hold-release), QCD twins 884936 (10)
- 2026-11-03T22:42:27Z ROLE=executor-wh PHASE=PRE-G2: reports 02/03 revised, 04_production_plan.md PARTIAL, STATUS/VERIFY_REQUEST #4/INDEX written; waiting on clusters 884934/884935/884936/884456
- 2026-11-04T09:07:44Z ROLE=executor-wh PHASE=PRE-G2: VERIFY#4 fixes, QCD twins analysed, resubmitted 885043/885044/885045; waiting
- 2026-11-04T10:16:03Z ROLE=executor-wh PHASE=PRE-G2: tests/analyses done except 2 gridpack-dependent; VERIFY #6; waiting on 884934.13, 885044
- 2026-11-04T10:23:45Z VERIFY#6 fixes done, VERIFY #7 written
- 2026-11-04T10:46:16Z G2-FIX items done except gridpack-dependent; VERIFY #8
- 2026-11-04T10:52:30Z VERIFY#8 fixes; VERIFY #9

- 2026-11-06 PROD resume: B_EW/ZZa tarballs verified, tests 893009/893010 and H_ggF_jj gridpack 893011 (testmatch) submitted; loose sigma ratio +1.053 recorded in STATUS. Steps 2-4 pending.

- 2026-11-06 (coordinator order): coupling cards+gridpacks 893013, tests 893022; KFOLD=5 in make_plan; 04 sec 6c/10-13; 02 H->gg fix; D28 HEPData negative (D-WH-16); 893011 replaced by 893012 (seed clash).

- 2026-11-06 follow-up chain: tests audited (coupling closures, param_card zeros), twinB 893415 submitted, V_ZZa UL, 04 sec 14, make_prod_sub K fix, VERIFY #11.

- 2026-11-06: twinB done (loss 1.56 %, C 1.026), plan regenerated, STATUS READY FOR G2-RECHECK (H_ggF_jj pending).

- 2026-11-06 recheck fixes: Q_aajj full N, D29 table+cards, ratio_C fix, jet->photon rate, text fixes (04 sec. 15), VERIFY #14.

- 2026-11-06: bulk submitted 893600-893630 (31 samples), fixes 4/7a-c, VERIFY #16.

- 2026-11-06 recheck2: F_EW/Q_aajj bulk, top-ups 893633/4, rate v3 (parentage, class, closure), 04 sec 16, VERIFY #17.

- 2026-11-06 late: D29 comparison (sec 18), memory/wall-time incidents fixed, Q_aajj resub 893876, validate_prod.py, VERIFY #19.

- 2026-11-06 22:58Z: condor fixes A1-3, report fixes B4-6, F_QCD_Wajjj replaces 2j row (sec 19), cluster 893883, VERIFY #20.
- 2026-11-07: VERIFY #20 defects (893883/893876 1cpu/8000, 893633 procs, job reconciliation, fix_memory_holds.sh)

- 2026-11-07: post-production checks (sec 20), rate correction (lepton contamination), direct closure fail x5, Q_aajj D29 trigger raised, package built, VERIFY #22.

- 2026-11-07: Q_aajjj delivered, origin diagnosis (sec 21), package fixes, background_total.json, VERIFY #23.
- 2026-11-09 submitted 899824 (fake skims); rate table built (W 465 files, TT 19)
- 2026-11-09 background-model block done: reports/05a_background_model.md, VERIFY_REQUEST.md written; 1502 skim + 484 rate jobs OK. Selection not started (waiting for verify/review).
- 2026-11-09 05a v2 reissued after HOLD; VERIFY_REQUEST rewritten
- 2026-11-09 selection fixed (05_selection.md), 05a v2.1, loose sample 899916 submitted
