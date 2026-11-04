# VERIFY_REQUEST (hh, multi_r1, pre-G2) — PENDING
Please verify independently (paths relative to p2/runs/multi_r1/hh unless absolute):
1. Test jobs exit 0, N_LHE=N_Delphes=2000, sigma closure: clusters 884941 (H_WH_Wqq_bb), 884943 (H_ggH_jj_heft, V_Wjj_QCD_vbs, Q_4b_ht), 884945 (T_ttbar_mlm; N_Delphes=616 by MLM veto, sigma_matched=sigma_MG5 x accepted/processed). Expected sigma_gridpack [pb]: WH 0.1525 (sum of W+,W- in LHE init), ggHjj 2.642, Wjj 839, 4b 4.138, ttMLM(xq30) 180.3 (MG5) -> 55.5 matched in the 2000-ev test (PY8 56.07), 54.2 in the 100k pilot. work/g2/sigma_closure_tests.md.
2. Gridpacks (production/hh/gridpacks, sha256 in production/hh/MANIFEST.tsv): clusters 884937 (20), 884944 (3: ggZH loop 21.3 fb, EW Wjj 90.0 pb, QCD WZ 163 fb), 884946 (tt MLM twin).
3. Pilots: clusters 884938, 884942, 884947, 884948, 884949; 2.19 M events in production/hh/<sample>/; expected PY8/ref sigma in work/g2/pilot.md (0.98-1.02), seed uniqueness (scripts/check_seed_uniq.py), no duplicated seeds.
4. Twins: work/g2/twins.md (QCD nominal filter loses +25+-5 % / +29+-6 %); morphing closure work/g2/morph_delphes.json (T3 = (1.25,1.5,2), pulls <1.3); MLM variation work/g2/mlm_check.json.
5. nmc_check_hh: python3 scripts/nmc_check_hh.py (self-test with 6 malformed bounds) and work/g2/plan.txt ("PASSED, 24 rows"); plan numbers work/g2/plan.json.
6. ggF HH normalisation 33.62 fb @13.6 TeV (LHCHWG-2026-010; TWiki LHCHWGHHRecommendations r3): re-fetch and compare.

## G2-FIX additions (PENDING)
7. work/g2/sha_check_pilots.md: all pilot jobs' gridpack_sha256 equal MANIFEST.tsv. 8. work/g2/o1_partition.txt (0.986, 0.992). 9. twins.md tagw rows; plan.json twin basis. 10. HELD_do_not_submit/*.sub (twin2 gp+prod, QCD block, t-channel gp) are NOT submitted; condor_q must show no hh job. 11. X_tchan_boost sigma 2.894 +- 0.024 pb (interactive private-MG5 run, 500 ev; /tmp log not kept). 12. Python hook test: scripts/py8_fatjet_filter_proto.py (359/2000 pass, 17 s).

13. work/g2/tchan/mg5_log_X_tchan_sigma_only.txt (2.894 +- 0.0235 pb), tW UL 0.879 (04 §7), no live D14a/tchan .sub in scripts/condor, plan.json uses wall_h_new.
