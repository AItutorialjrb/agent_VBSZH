#!/bin/bash
# Generate-only syntax/order audit (no output/launch): runs import/define/generate/add lines of a card and
# records MG5's process and diagram counts.  Usage: scripts/mg5_genonly.sh <card> [timeout_s]
PROJECT=/eos/home-r/rjiang/vbs_zh_codex_starter; WH=$PROJECT/p2/runs/single_r1/wh
CARD=$1; TMO=${2:-900}; D=$WH/work/genonly; mkdir -p $D
source $PROJECT/p2/lib/scripts/setup_stack.sh >/dev/null
sed -n '/^import model/,/^output/p' $WH/cards/$CARD.mg5 | grep -v '^output' | sed 's%^import model heft%import model ./heft%' > $D/$CARD.gen.mg5
echo "display processes" >> $D/$CARD.gen.mg5
SCR=/tmp/$USER/wh_single_r1_gen_$CARD; mkdir -p $SCR; ln -sfn $WH/work/models/x/heft $SCR/heft   # local UFO copy (not installed into software/)
( cd $SCR && timeout $TMO nice -n 10 mg5_aMC $D/$CARD.gen.mg5 ) > $D/$CARD.log 2>&1; RC=$?
rm -rf $SCR
echo "$CARD rc=$RC $(grep -E 'Total: [0-9]+ processes with [0-9]+ diagrams' $D/$CARD.log | tr '\n' ' ')" | tee $D/$CARD.summary
