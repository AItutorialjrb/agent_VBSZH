# VERIFY_REQUEST #3 (executor-wh) — new items only
New finished jobs (read via xrootd; outputs work/test/<s>/<s>_s<seed>*): F_QCD_Wajj_nomjj (884460.1, seed 2128001, 2000 ev, gridpack σ 5683±10 fb), B_QCD_Waajj_vbs (884860.0, seed 2124001, 2000 ev, gridpack σ 0.6327±0.0011 fb, PY8 0.6317), B_QCD_Waajj_nomjj (884460.0, seed 2125001, 2000 ev, gridpack σ 3.582 fb). k=WF=0.96008 (W->l nu in ME, no H). Expect LHE=Delphes=2000.
New gridpacks (884456): B_QCD_Waajj_vbs σ 0.6327 fb (wall 16439 s), B_QCD_Waajj_nomjj 3.582 fb (17341 s), F_EW_Wajj_vbs 89.63 fb, F_QCD_Wajj_vbs 712.4 fb, F_QCD_Wajj_nomjj 5683 fb.
Check: no duplicate test runs (test_wh.log: one 005 per proc; 884860 single proc), N_required in config/sample_matrix.yaml for F_EW (258k), F_QCD (2.05M), F_QCD_nomjj aux (1.6e7, ratio only); twin numbers reports/03 §7 (scripts/twin_safety.py: 37±9 % and 47.6±5.5 % of reco-selected events with parton mjj<400).
Still running: gridpack 884456.3 B_EW_Waajj_vbs (~5 h); held test 884457.3.
