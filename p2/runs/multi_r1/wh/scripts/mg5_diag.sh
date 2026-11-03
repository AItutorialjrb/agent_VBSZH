#!/bin/bash
# Diagram/subprocess audit (generate+output only, NO integration).  Usage: mg5_diag.sh <card.mg5 in cards/diag/> [timeout_s]
# MG5 runs in node-local scratch; logs + subproc list + diagram counts staged to work/diag/<card>/.
CARD=$1; TMO=${2:-1500}
WH=/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh
SCR=${DIAG_SCRATCH:-/tmp/$USER/wh_diag}; mkdir -p $SCR; OUT=$SCR/$CARD; DEST=$WH/work/diag/$CARD
[ -e "$OUT" ] && { echo "scratch exists"; exit 3; }; mkdir -p $DEST
source /eos/home-r/rjiang/vbs_zh_codex_starter/p2/lib/scripts/setup_stack.sh >/dev/null
sed -e "s#OUTDIR#$OUT#g" $WH/cards/diag/$CARD.mg5 > $DEST/run.mg5
T0=$(date +%s); ( cd $SCR && timeout $TMO mg5_aMC $DEST/run.mg5 ) > $DEST/mg5.log 2>&1; RC=$?
echo "rc=$RC wall=$(( $(date +%s)-T0 ))s" > $DEST/status.txt
grep -E "^Total:|processes with|diagrams" $DEST/mg5.log | tail -3 >> $DEST/status.txt
cp $OUT/SubProcesses/subproc.mg $DEST/ 2>/dev/null
ls -d $OUT/SubProcesses/P*/ 2>/dev/null | xargs -n1 basename > $DEST/subprocs.txt
for d in $OUT/SubProcesses/P*/; do n=$(grep -c "^Diagram\|^ *diagram" $d/matrix.f 2>/dev/null); echo "$(basename $d) $(grep -m1 "Process:" $d/matrix*.f | cut -c1-120)" ; done > $DEST/proc_list.txt 2>/dev/null
cat $DEST/status.txt
