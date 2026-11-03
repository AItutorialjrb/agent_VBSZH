#!/bin/bash
# sigma-only smoke runs for the Phase-02 matrix. Seeds 2110000+J (sample index 0 = smoke), J=12.. unique.
cd /eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh
declare -A S=( [S_EW_WHjj_smoke]=2110012 [S_EW_WHjj_taunu_smoke]=2110013 [H_ttH_1l_smoke]=2110014 [H_tHq_lep_smoke]=2110015 [H_tHW_1l_smoke]=2110016 [T_tta_1l_smoke]=2110017 [T_ttaa_1l_smoke]=2110018 [T_tWa_1l_smoke]=2110019 [T_tt_1l_smoke]=2110020 [F_Wjj_pilot_smoke]=2110021 [F_Wajj_pilot_smoke]=2110022 [H_QCD_WH_mlm_smoke]=2110023 [H_QCD_WHjj_fixed_smoke]=2110024 [I_WHjj_smoke]=2110025 [H_QCD_WH_0j_smoke]=2110028 [Q_aa_0j_smoke]=2110030 [Q_aajj_smoke]=2110031 )
for c in "$@"; do scripts/mg5_run_smoke.sh $c ${S[$c]} 1500; done
