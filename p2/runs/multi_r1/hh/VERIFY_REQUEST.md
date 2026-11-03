# VERIFY_REQUEST (hh, multi_r1) — post-audit items ONLY
Base: /eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/hh
1. Q_4j_vbs: gridpack work/gridpacks/Q_4j_vbs_status.txt (rc0, sigma 3.766e4 pb) + test job cluster 884577 -> work/test/Q_4j_vbs/ (exit 0, n_lhe = n_delphes = 2000, row in work/sigma_closure.md: LHE/gridpack 0.997, PY8/LHE 1.001).
2. config/sample_matrix.yaml br_total at full precision and = product of br_inputs over br_ledger (labels B_bb@H1/@H2, B_Zqq@Z1/@Z2); run: source ../../../lib/scripts/setup_stack.sh; python3 -P scripts/nmc_check_hh.py config/sample_matrix.yaml (self-test must print "OK (raised on all 5 bad entries)" and the matrix check must pass).
3. Strict signal N rule is applied to roles sig/basis/closure (scripts/nmc_check_hh.py SIG_ROLES); ZZ ledger no longer a false positive.
4. reports/03 §3: provenance table (which tarball per sample) and exit-code notes; verify sigma in work/gridpacks/ (884459) == work/gridpacks_v2/ (884461) for S_*, V_*HH*, G_ggHH_loop_kl1; wrappers scripts/condor/*_hh.sh exit 30 on no-op.
