#!/bin/bash
# Ready follow-up for the two long gridpacks (executor-wh). Usage: followup_after_gridpacks.sh <stage>
#   test     : when work/gridpacks/<s>_gridpack_s<seed>.tar.gz exist -> submit the single test job for B_EW_Waajj_nomjj (g2d_test_Bnomjj.sub, seed J=102) and V_ZZa_WH (g2d_test_ZZa.sub)
#   twinB    : after work/test/B_EW_Waajj_nomjj/*.json exists (test succeeded) -> submit the EW twin production g2_twins_ewB.sub (5 x 8000 ev, LHE kept)
# Every stage: seed check, duplicate check (condor_q on bigbird103 + output file existence), eossubmit. Never submits twice (touches work/condor/.submitted_<name>).
set -e; WH=/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh; cd $WH/work/condor
python3 $WH/scripts/check_sub_seeds.py
sub(){ n=$1; [ -e .submitted_$n ] && { echo "$n already submitted"; return; }
  bash -lc "module load lxbatch/eossubmit; condor_q -name bigbird103.cern.ch -nobatch 2>/dev/null | grep -c '$2' || true" | grep -q '^0$' || { echo "$2 already in queue"; return; }
  bash -lc "module load lxbatch/eossubmit; cd $WH/work/condor; condor_submit $n.sub" && touch .submitted_$n; }
case $1 in
 test)  ls $WH/work/gridpacks/B_EW_Waajj_nomjj_gridpack_s*.tar.gz >/dev/null && { ls $WH/work/test/B_EW_Waajj_nomjj/*.json >/dev/null 2>&1 || sub g2d_test_Bnomjj B_EW_Waajj_nomjj; }
        ls $WH/work/gridpacks/V_ZZa_WH_gridpack_s*.tar.gz >/dev/null && { ls $WH/work/test/V_ZZa_WH/*.json >/dev/null 2>&1 || sub g2d_test_ZZa V_ZZa_WH; } ;;
 twinB) ls $WH/work/test/B_EW_Waajj_nomjj/*[0-9].json >/dev/null && sub g2_twins_ewB twins_B_unused ;;
esac
