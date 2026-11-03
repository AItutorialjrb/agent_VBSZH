#!/bin/bash
# sigma-only interactive MG5 run.  Usage: mg5_run_smoke.sh <card in cards/smoke> <seed> [timeout_s]
# Derived from lib/scripts/mg5_smoke.sh (rationale: paths -> wh process dir; patch 001). MG5 runs in node-local scratch.
CARD=$1; SEED=$2; TMO=${3:-1500}
WH=/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh
SCR=${SMOKE_SCRATCH:-/tmp/$USER/wh_smoke}; mkdir -p $SCR; OUT=$SCR/$CARD; DEST=$WH/work/smoke/$CARD
[ -e "$OUT" ] && { echo "scratch $OUT exists; refusing"; exit 3; }; mkdir -p $DEST
source /eos/home-r/rjiang/vbs_zh_codex_starter/p2/lib/scripts/setup_stack.sh >/dev/null
sed -e "s#OUTDIR#$OUT#g" -e "s#SEED#$SEED#g" $WH/cards/smoke/$CARD.mg5 > $DEST/run.mg5
T0=$(date +%s); ( cd $SCR && timeout $TMO mg5_aMC $DEST/run.mg5 ) > $DEST/mg5.log 2>&1; RC=$?
echo "card=$CARD seed=$SEED rc=$RC wall_s=$(( $(date +%s)-T0 )) host=$(hostname) utc=$(date -u +%FT%TZ)" > $DEST/status.txt
grep -E "Cross-section :|Nb of events :" $DEST/mg5.log | tail -2 >> $DEST/status.txt
cp -r $OUT/Cards $DEST/ 2>/dev/null; for f in $OUT/Events/run_01*/*banner.txt $OUT/Events/run_01*/*.lhe.gz; do [ -f $f ] && cp $f $DEST/; done
cat $DEST/status.txt
