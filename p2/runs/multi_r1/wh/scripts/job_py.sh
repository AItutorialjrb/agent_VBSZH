#!/bin/bash
# HTCondor wrapper for analysis-level jobs (05a): job_py.sh <mode: skim|rate> <sample> <out_eos_dir> <slim_root_eos_path[,path2,...]>  (rate table / scripts are transferred)
MODE=$1; SAMPLE=$2; OUTDIR=$3; INS=$4; EOSURL=root://eosuser.cern.ch
WD=${_CONDOR_SCRATCH_DIR:-$PWD}; cd "$WD" || exit 10
toxrd(){ echo "$1" | sed 's#^/eos/home-r/rjiang#/eos/user/r/rjiang#'; }
case $MODE in skim) EXT=npz;; rate) EXT=json;; esac
source setup_stack.sh || exit 11
rc=0
for IN in ${INS//,/ }; do
  TAG=$(basename "$IN" .root); OUTN=${MODE}_${SAMPLE}__${TAG}
  xrdfs $EOSURL stat "$(toxrd $OUTDIR)/$OUTN.json" >/dev/null 2>&1 && { echo "$OUTN exists -> skip"; continue; }
  rm -f $TAG.root ${TAG}_gen.root
  ok=0; for t in 1 2 3 4; do xrdcp -f -s $EOSURL/$(toxrd $IN) $TAG.root && xrdcp -f -s $EOSURL/$(toxrd ${IN%.root}_gen.root) ${TAG}_gen.root && { ok=1; break; }; echo "xrdcp attempt $t failed"; sleep $((20*t)); done
  [ $ok = 1 ] || { rc=12; continue; }
  if [ $MODE = skim ]; then python3 -P skim.py $SAMPLE $TAG.root $OUTN.npz --rates rate_table.json || { rc=14; continue; }; else python3 -P rate_genuine.py $TAG.root $OUTN.json || { rc=14; continue; }; fi
  [ $EXT != json ] && xrdcp -s $OUTN.$EXT $EOSURL/$(toxrd $OUTDIR)/$OUTN.$EXT; xrdcp -s $OUTN.json $EOSURL/$(toxrd $OUTDIR)/$OUTN.json   # json (written last) marks completion
  rm -f $TAG.root ${TAG}_gen.root $OUTN.*
done
exit $rc
