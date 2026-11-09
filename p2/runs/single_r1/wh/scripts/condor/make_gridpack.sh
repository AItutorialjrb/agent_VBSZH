#!/bin/bash
# HTCondor wrapper: build an MG5 gridpack on a worker (for processes too heavy for interactive smoke tests).
# Args: <card-name (.mg5 transferred)> <seed> <eos_out_dir> [ncores=8]
# Output: <card>_gridpack_s<seed>.tar.gz + <card>_mg5.log.gz + <card>_status.txt staged via xrdcp (no overwrite).
set -o pipefail
CARD=$1; SEED=$2; OUTDIR=$3; EOSURL=root://eosuser.cern.ch
WD=${_CONDOR_SCRATCH_DIR:-$PWD}; cd "$WD" || exit 10
# Without transfer_output_files HTCondor copies every new top-level scratch file back to the submit dir
# (scripts/condor). Everything needed is staged to EOS by xrdcp, so delete top-level job files on exit
# (keeps condor's own _condor_* / dot files / executable; subdirectories are never transferred).
trap 'find "$WD" -maxdepth 1 -type f ! -name "_condor_*" ! -name ".*" ! -name condor_exec.exe -newer "$WD/.vbszh_t0" -delete 2>/dev/null; find "$WD" -maxdepth 1 -type f \( -name "*.tar.gz" -o -name "*.lhe.gz" -o -name "*.tgz" -o -name "*.json" \) -delete 2>/dev/null' EXIT
touch "$WD/.vbszh_t0"
xrdfs $EOSURL stat "$OUTDIR/${CARD}_gridpack_s${SEED}.tar.gz" >/dev/null 2>&1 && { echo "exists, skip"; exit 0; }
export PROJECT=$WD/proj; mkdir -p $PROJECT/scripts; cp setup_stack.sh $PROJECT/scripts/
xrdcp -s $EOSURL//eos/user/r/rjiang/vbs_zh_codex_starter/software/install/MG5_aMC_v3.6.3_install.tgz mg5.tgz && tar xzf mg5.tgz || exit 11
export MG5_HOME=$WD/MG5_aMC_v3.6.3
# optional extra UFO (2026-11-03, coupling study): a transferred HC_NLO_X0_kVV.tgz is unpacked into MG5 models/
[ -f HC_NLO_X0_kVV.tgz ] && { tar xzf HC_NLO_X0_kVV.tgz -C $MG5_HOME/models || exit 11; }
[ -f heft.tgz ] && { tar xzf heft.tgz -C $MG5_HOME/models || exit 11; }   # single_r1 patch 002: HEFT UFO for ggF H+2j
source $PROJECT/scripts/setup_stack.sh || exit 12
NC=${4:-8}   # 4th argument = request_cpus from the submit file
sed -e "s#OUTDIR#$WD/proc#g" -e "s#SEED#$SEED#g" -e "s#set nb_core 4#set nb_core $NC#" "$CARD.mg5" > run.mg5
T0=$(date +%s); mg5_aMC run.mg5 > mg5.log 2>&1; RC=$?
echo "card=$CARD seed=$SEED rc=$RC wall_s=$(( $(date +%s)-T0 )) host=$(hostname) ncore=$NC utc=$(date -u +%FT%TZ)" > ${CARD}_status.txt
grep -E "Cross-section :|Nb of events :" mg5.log | tail -2 >> ${CARD}_status.txt
gzip -c mg5.log > ${CARD}_mg5.log.gz
GP=$(ls proc/*gridpack*.tar.gz 2>/dev/null | head -1)
[ -n "$GP" ] && mv "$GP" ${CARD}_gridpack_s${SEED}.tar.gz
for f in ${CARD}_status.txt ${CARD}_mg5.log.gz ${CARD}_gridpack_s${SEED}.tar.gz; do
  # status/log are diagnostics -> overwrite on retry (-f); the gridpack itself is never overwritten
  F=""; [ "$f" = "${CARD}_gridpack_s${SEED}.tar.gz" ] || F="-f"
  [ -f "$f" ] && { xrdcp -s $F "$f" "$EOSURL/$OUTDIR/$f" || exit 16; }
done
[ $RC = 0 ] && [ -n "$GP" ] || exit 15
