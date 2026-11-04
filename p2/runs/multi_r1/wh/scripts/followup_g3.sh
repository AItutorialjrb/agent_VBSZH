#!/bin/bash
# G2-FIX follow-up: for each of Q_aajj, H_VBFH_jj, H_ggF_jj submit its 5000-event test job when (a) the gridpack exists, (b) no test json exists, (c) not already submitted/queued. Usage: followup_g3.sh
WH=/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh; cd $WH/work/condor; python3 $WH/scripts/check_sub_seeds.py || exit 1
for s in Q_aajj H_VBFH_jj H_ggF_jj; do
  ls $WH/work/gridpacks/${s}_gridpack_s*.tar.gz >/dev/null 2>&1 || { echo "$s: gridpack missing"; continue; }
  ls $WH/work/test/$s/*[0-9].json >/dev/null 2>&1 && { echo "$s: test done"; continue; }
  [ -e .submitted_g3_$s ] && { echo "$s: already submitted"; continue; }
  bash -lc "module load lxbatch/eossubmit; cd $WH/work/condor; condor_submit g3_test_$s.sub 2>&1 | tail -1" && touch .submitted_g3_$s
done
