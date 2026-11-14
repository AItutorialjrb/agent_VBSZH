#!/bin/bash
# condor wrapper for 07 statistics tasks: job_stat.sh <task>  (inputs copied from EOS, output to work/stat on EOS)
TASK=$1; if [[ "$TASK" == v12:* ]]; then export STAT_V11=1 STAT_V12=1 STAT_TABLE=table_v12 STAT_YIELDS=yields_v12; TASK=${TASK#v12:}; fi; if [[ "$TASK" == v11:* ]]; then export STAT_V11=1 STAT_TABLE=table_v11 STAT_YIELDS=yields_v11; TASK=${TASK#v11:}; fi; EOSURL=root://eosuser.cern.ch; B=/eos/user/r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh
WD=${_CONDOR_SCRATCH_DIR:-$PWD}; cd "$WD" || exit 10; source setup_stack.sh || exit 11
mkdir -p wh/work/sel wh/work/bgmodel wh/work/stat wh/scripts
for f in work/sel/table_v12.npz work/sel/table_v12_meta.json work/bgmodel/yields_v12.json work/sel/table_v11.npz work/sel/table_v11_meta.json work/bgmodel/yields_v11.json work/sel/table.npz work/sel/lhe_rows.npz work/sel/table_meta.json work/bgmodel/yields.json; do xrdcp -f -s $EOSURL/$B/$f wh/$f || exit 12; done
cp stat_lib.py stat_run.py comb_run.py vh_build.py vh_run.py toys.py wh/scripts/; mkdir -p wh/vh_ws; xrdcp -f -s $EOSURL//eos/user/r/rjiang/vbs_zh_codex_starter/p2/combination/vh_ws/zh_channel_inputs.json wh/vh_ws/ || exit 16; export VH_WS=$PWD/wh/vh_ws; xrdcp -f -s $EOSURL/$B/work/stat/VH_inputs_zh.json wh/work/stat/ || exit 13; export STAT_WH=$PWD/wh
case $TASK in z0mu:*|map2d:*|ws) python3 -P wh/scripts/vh_run.py "$TASK" || exit 14;; comb:*) python3 -P wh/scripts/comb_run.py "$TASK" || exit 14;; *) python3 -P wh/scripts/stat_run.py "$TASK" || exit 14;; esac
if [ -n "$STAT_V12" ]; then SUF=_v12; elif [ -n "$STAT_V11" ]; then SUF=_v11; else SUF=; fi
case $TASK in z0mu:*|map2d:*) PFX=vh_;; *) PFX=;; esac
OUT=wh/work/stat/${PFX}$(echo $TASK | tr ':' '_')$SUF.json
xrdcp -f -s $OUT $EOSURL/$B/work/stat/$(basename $OUT) || exit 15
exit 0
