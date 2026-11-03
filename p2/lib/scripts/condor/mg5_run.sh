#!/bin/bash
# HTCondor wrapper (theory runs, 2026-11-03): run an MG5 card (event generation, no gridpack) and stage
# unweighted_events.lhe.gz + status (cross section) + log to <eos_out_dir>/<card>_s<seed>.*  (never overwrites).
# Args: <card-name (.mg5 transferred)> <seed> <eos_out_dir> [ncores=4]
set -o pipefail
CARD=$1; SEED=$2; OUTDIR=$3; NC=${4:-4}; EOSURL=root://eosuser.cern.ch
WD=${_CONDOR_SCRATCH_DIR:-$PWD}; cd "$WD" || exit 10
trap 'find "$WD" -maxdepth 1 -type f ! -name "_condor_*" ! -name ".*" ! -name condor_exec.exe -newer "$WD/.vbszh_t0" -delete 2>/dev/null' EXIT
touch "$WD/.vbszh_t0"
T=${CARD}_s${SEED}
xrdfs $EOSURL stat "$OUTDIR/$T.lhe.gz" >/dev/null 2>&1 && { echo "exists, skip"; exit 0; }
export PROJECT=$WD/proj; mkdir -p $PROJECT/scripts; cp setup_stack.sh $PROJECT/scripts/
xrdcp -s $EOSURL//eos/user/r/rjiang/vbs_zh_codex_starter/software/install/MG5_aMC_v3.6.3_install.tgz mg5.tgz && tar xzf mg5.tgz || exit 11
export MG5_HOME=$WD/MG5_aMC_v3.6.3; source $PROJECT/scripts/setup_stack.sh || exit 12
sed -e "s#OUTDIR#$WD/proc#g" -e "s#SEED#$SEED#g" -e "s#set nb_core 4#set nb_core $NC#" "$CARD.mg5" > run.mg5
T0=$(date +%s); mg5_aMC run.mg5 > mg5.log 2>&1; RC=$?
echo "card=$CARD seed=$SEED rc=$RC wall_s=$(( $(date +%s)-T0 )) host=$(hostname) ncore=$NC utc=$(date -u +%FT%TZ)" > $T.status.txt
grep -E "Cross-section :|Nb of events :" mg5.log | tail -2 >> $T.status.txt
gzip -c mg5.log > $T.mg5.log.gz
L=$(ls proc/Events/run_01/unweighted_events.lhe.gz 2>/dev/null); [ -n "$L" ] && cp "$L" $T.lhe.gz
for f in $T.status.txt $T.mg5.log.gz $T.lhe.gz; do [ -f $f ] && { xrdcp -s -f $f $EOSURL/$OUTDIR/$f || exit 16; }; done
[ -f $T.lhe.gz ] || exit 17
