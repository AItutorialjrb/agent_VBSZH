#!/bin/bash
# HTCondor wrapper (theory weights, 2026-11-03): run an existing (use_syst=True) gridpack to LHE only and stage
# <name>_s<seed>.lhe.gz (scale + NNPDF3.1 replica weights) to <eos_out_dir>. Never overwrites.
# Args: <name> <gridpack_eos_path> <nevents> <seed> <eos_out_dir>
set -o pipefail
N=$1; GP=$2; NEV=$3; SEED=$4; OUTDIR=$5; EOSURL=root://eosuser.cern.ch
WD=${_CONDOR_SCRATCH_DIR:-$PWD}; cd "$WD" || exit 10
trap 'find "$WD" -maxdepth 1 -type f ! -name "_condor_*" ! -name ".*" ! -name condor_exec.exe -newer "$WD/.vbszh_t0" -delete 2>/dev/null' EXIT
touch "$WD/.vbszh_t0"; T=${N}_s${SEED}
xrdfs $EOSURL stat "$OUTDIR/$T.lhe.gz" >/dev/null 2>&1 && { echo "exists, skip"; exit 0; }
export PROJECT=$WD/proj; mkdir -p $PROJECT/scripts; cp setup_stack.sh $PROJECT/scripts/
export MG5_HOME=/nonexistent; source $PROJECT/scripts/setup_stack.sh || exit 11
xrdcp -s $EOSURL/$GP gp.tar.gz || exit 12; mkdir gp && tar xzf gp.tar.gz -C gp || exit 13
T0=$(date +%s); ( cd gp && ./run.sh "$NEV" "$SEED" ) > lhe.log 2>&1 || { tail -20 lhe.log; exit 14; }
echo "name=$N seed=$SEED nev=$NEV n_lhe=$(zgrep -c '<event>' gp/events.lhe.gz) wall_s=$(( $(date +%s)-T0 )) host=$(hostname)" ; mv gp/events.lhe.gz $T.lhe.gz
xrdcp -s $T.lhe.gz $EOSURL/$OUTDIR/$T.lhe.gz || exit 16
