#!/bin/bash
# Patch 003 of p2/lib/scripts/condor/make_gridpack.sh: MG5 integration (+gridpack if the card asks) on a worker.
# Differences: stages to this run's wh/work/gp_condor (never frozen production/), also stages process list, LHE (non-gridpack
# cards) and banner; success = rc 0 and a cross section in the log.  Args: <sample> <card.mg5 basename> <seed> <eos_out_dir> [ncores]
set -o pipefail
S=$1; CARD=$2; SEED=$3; OUTDIR=$4; NC=${5:-8}; EOSURL=root://eosuser.cern.ch
WD=${_CONDOR_SCRATCH_DIR:-$PWD}; cd "$WD" || exit 10
trap 'find "$WD" -maxdepth 1 -type f ! -name "_condor_*" ! -name ".*" ! -name condor_exec.exe -newer "$WD/.t0" -delete 2>/dev/null' EXIT
touch "$WD/.t0"; T=${S}_s${SEED}
xrdfs $EOSURL stat "$OUTDIR/${T}_status.txt" >/dev/null 2>&1 && { echo "exists, skip"; exit 0; }
xrdcp -s $EOSURL//eos/user/r/rjiang/vbs_zh_codex_starter/software/install/MG5_aMC_v3.6.3_install.tgz mg5.tgz && tar xzf mg5.tgz || exit 11
export MG5_HOME=$WD/MG5_aMC_v3.6.3
source ./setup_stack.sh || exit 12
sed -e "s#OUTDIR#$WD/proc#g" -e "s#SEED#$SEED#g" -e "s#set nb_core 4#set nb_core $NC#" "$CARD" > run.mg5
T0=$(date +%s); mg5_aMC run.mg5 > mg5.log 2>&1; RC=$?
echo "sample=$S card=$CARD seed=$SEED rc=$RC wall_s=$(( $(date +%s)-T0 )) host=$(hostname) ncore=$NC stack=$VBSZH_STACK_TAG utc=$(date -u +%FT%TZ) card_sha256=$(sha256sum $CARD|cut -c1-16)" > ${T}_status.txt
grep -E "Total: .* processes with .* diagrams" mg5.log | head -4 >> ${T}_status.txt
grep -E "Cross-section :|Nb of events :" mg5.log | tail -2 >> ${T}_status.txt
for d in proc/SubProcesses/P*/; do grep -h "^C *Process:" "$d"/matrix*.f 2>/dev/null; done | sort -u > ${T}_processes.txt
gzip -c mg5.log > ${T}_mg5.log.gz
FILES="${T}_mg5.log.gz ${T}_processes.txt"
GP=$(ls proc/*gridpack*.tar.gz 2>/dev/null | head -1); [ -n "$GP" ] && { mv "$GP" ${T}_gridpack.tar.gz; FILES="$FILES ${T}_gridpack.tar.gz"; }
LHE=$(ls proc/Events/run_01*/unweighted_events.lhe.gz 2>/dev/null | head -1); [ -n "$LHE" ] && { mv "$LHE" ${T}.lhe.gz; FILES="$FILES ${T}.lhe.gz"; }
BAN=$(ls proc/Events/run_01*/*banner.txt 2>/dev/null | head -1); [ -n "$BAN" ] && { cp "$BAN" ${T}_banner.txt; FILES="$FILES ${T}_banner.txt"; }
for f in $FILES ${T}_status.txt; do xrdcp -s "$f" "$EOSURL/$OUTDIR/$f" || exit 16; done
[ $RC = 0 ] && grep -q "Cross-section :" mg5.log || exit 15
