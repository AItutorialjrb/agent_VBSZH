#!/bin/bash
# condor wrapper for toys (A4): job_toys.sh coup <kzneg|kw> <lumi> <seed> <N> | q0 <ws> <poi> <seed> <N> | qmu <ws> <poi> <mu> <seed> <N> <hyp>
KIND=$1; shift; EOSURL=root://eosuser.cern.ch; B=/eos/user/r/rjiang/vbs_zh_codex_starter/p2; W=$B/runs/multi_r1/wh
WD=${_CONDOR_SCRATCH_DIR:-$PWD}; cd "$WD" || exit 10; source setup_stack.sh || exit 11
mkdir -p wh/work/sel wh/work/bgmodel wh/work/stat wh/work/toys wh/scripts wh/vh_ws
for f in work/sel/table_v12.npz work/sel/table_v12_meta.json work/sel/table_K.npz work/sel/table_K_meta.json work/bgmodel/yields_v12.json; do xrdcp -f -s $EOSURL/$W/$f wh/$f || exit 12; done
for f in zh_channel_inputs.json VH_workspace.json VH_workspace_2d.json WH_workspace.json ZH_workspace.json VH_workspace_defb.json; do xrdcp -f -s $EOSURL/$B/combination/vh_ws/$f wh/vh_ws/$f || exit 13; done
cp stat_lib.py coup_run.py vh_coup.py toys.py wh/scripts/; export STAT_WH=$PWD/wh VH_WS=$PWD/wh/vh_ws STAT_V12=1 STAT_V11=1 STAT_TABLE=table_v12 STAT_YIELDS=yields_v12
case $KIND in
 coup) conv=$1; L=$2; SD=$3; N=$4; fl=""; [ $conv = kzneg ] && fl="--kz-neg"; python3 -P wh/scripts/vh_coup.py $fl --lumi $L --toys $N --seed $SD || exit 14;;
 q0) python3 -P wh/scripts/toys.py q0 wh/vh_ws/$1_workspace.json $2 $3 $4 || exit 14;;
 qmu) python3 -P wh/scripts/toys.py qmu wh/vh_ws/$1_workspace.json $2 $3 $4 $5 $6 || exit 14;;
esac
for f in wh/work/toys/*; do xrdcp -f -s $f $EOSURL/$W/work/toys/$(basename $f) || exit 15; done
exit 0
