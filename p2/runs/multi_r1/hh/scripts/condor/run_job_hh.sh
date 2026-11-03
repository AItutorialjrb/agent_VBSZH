#!/bin/bash
# hh VARIANT of lib run_job.sh (patch 005): slim_hh_truth.py (fat-jet truth) and the slim_hh_v1 Delphes card (FatJet branch). Otherwise identical.
# HTCondor wrapper (v2): gridpack -> LHE -> Pythia8 (CP5) + Delphes (CMS slim_v1 card, seed pinned)
#                        -> in-job overlap truth + slimming (scripts/slim_hh_truth.py) -> xrdcp to EOS.
# Args: <sample> <gridpack_eos_path> <nevents> <mg_seed> <py_cmnd_basename> <eos_out_dir> [keep_lhe=0|1] [keep_full=0|1]
# Seeds: mg_seed unique per job; Pythia seed = mg_seed + 1e8; Delphes RandomSeed derived from Pythia seed.
# Outputs: <tag>.root (Delphes tree, no Particle branch), <tag>_gen.root (GenTruth friend tree, same entry order),
#          <tag>.json (metadata), <tag>_logs.tgz; optionally <tag>.lhe.gz and <tag>_full.root (with Particle).
# Duplicate protection: names contain the seed; job exits 0 early if <tag>.root exists; xrdcp never uses -f.
set -o pipefail
SAMPLE=$1; GP=$2; NEV=$3; SEED=$4; CMND=$5; OUTDIR=$6; KEEP_LHE=${7:-0}; KEEP_FULL=${8:-0}
EOSURL=root://eosuser.cern.ch
WD=${_CONDOR_SCRATCH_DIR:-$PWD}; cd "$WD" || exit 10
# Without transfer_output_files HTCondor copies every new top-level scratch file back to the submit dir
# (scripts/condor). Everything needed is staged to EOS by xrdcp, so delete top-level job files on exit
# (keeps condor's own _condor_* / dot files / executable; subdirectories are never transferred).
trap 'find "$WD" -maxdepth 1 -type f ! -name "_condor_*" ! -name ".*" ! -name condor_exec.exe -newer "$WD/.vbszh_t0" -delete 2>/dev/null; find "$WD" -maxdepth 1 -type f \( -name "*.tar.gz" -o -name "*.lhe.gz" -o -name "*.tgz" -o -name "*.json" \) -delete 2>/dev/null' EXIT
touch "$WD/.vbszh_t0"
TAG=${SAMPLE}_s${SEED}
log(){ echo "[$(date -u +%FT%TZ)] $*"; }
log "host=$(hostname) wd=$WD sample=$SAMPLE seed=$SEED nev=$NEV keep_lhe=$KEEP_LHE keep_full=$KEEP_FULL"
if xrdfs $EOSURL stat "$OUTDIR/${TAG}.root" >/dev/null 2>&1; then log "NOOP: output exists -> nothing done, exit 30"; exit 30; fi
# test_v2 jobs may start before their gridpack exists: exit 19 -> on_exit_hold, periodic_release retries later (see make_submit.py)
xrdfs $EOSURL stat "$GP" >/dev/null 2>&1 || { log "gridpack not yet available: $GP"; exit 19; }
export PROJECT=$WD/proj; mkdir -p $PROJECT/scripts $PROJECT/cards/phase03_smoke $PROJECT/cards/phase04_candidates
cp setup_stack.sh run_py8_delphes.sh slim_hh_truth.py $PROJECT/scripts/
cp py8_common_CP5.cmnd "$CMND" $PROJECT/cards/phase03_smoke/
cp delphes_card_CMS_slim_hh_v1.tcl $PROJECT/cards/phase04_candidates/
export MG5_HOME=/nonexistent   # gridpack is self-contained
source $PROJECT/scripts/setup_stack.sh || exit 11
xrdcp -s $EOSURL/$GP gp.tar.gz || exit 12
GPSHA=$(sha256sum gp.tar.gz | cut -d' ' -f1)
mkdir gp && tar xzf gp.tar.gz -C gp || exit 13
T0=$(date +%s)
( cd gp && ./run.sh "$NEV" "$SEED" ) > mg_gridpack.log 2>&1 || { tail -20 mg_gridpack.log; exit 14; }
T1=$(date +%s); NLHE=$(zgrep -c '<event>' gp/events.lhe.gz); log "LHE events: $NLHE"
XS=$(zcat gp/events.lhe.gz | sed -n '/<init>/,/<\/init>/p' | sed -n 3p)
PYSEED=$((SEED + 100000000))
DELPHES_CARD=$PROJECT/cards/phase04_candidates/delphes_card_CMS_slim_hh_v1.tcl \
  bash $PROJECT/scripts/run_py8_delphes.sh "$WD/gp/events.lhe.gz" "$PROJECT/cards/phase03_smoke/$CMND" "$NLHE" "$PYSEED" "$WD/out/full.root" > py8_delphes.log 2>&1 || { tail -30 py8_delphes.log; exit 15; }
T2=$(date +%s)
python3 -P $PROJECT/scripts/slim_hh_truth.py out/full.root out/${TAG} > slim.log 2>&1 || { tail -20 slim.log; exit 18; }
T3=$(date +%s)
NDEL=$(python3 -P -c "import uproot;print(uproot.open('out/${TAG}.root')['Delphes'].num_entries)")
SIGPY=$(grep -E '^ \| sum' py8_delphes.log | tail -1)
cat > ${TAG}.json <<EOF
{"sample":"$SAMPLE","mg_seed":$SEED,"py_seed":$PYSEED,"n_requested":$NEV,"n_lhe":$NLHE,"n_delphes":$NDEL,
 "lhe_init_xsec_pb_err_pb_max_lprup":"$XS","pythia_sum_line":"$SIGPY",
 "gridpack":"$GP","gridpack_sha256":"$GPSHA","py_cmnd":"$CMND","delphes_card":"delphes_card_CMS_slim_hh_v1.tcl",
 "t_gridpack_s":$((T1-T0)),"t_py8_delphes_s":$((T2-T1)),"t_slim_s":$((T3-T2)),
 "stack":"$VBSZH_STACK_TAG","host":"$(hostname)","utc":"$(date -u +%FT%TZ)"}
EOF
tar czf ${TAG}_logs.tgz mg_gridpack.log py8_delphes.log slim.log
FILES="out/${TAG}.root out/${TAG}_gen.root ${TAG}.json ${TAG}_logs.tgz"
[ "$KEEP_LHE" = 1 ] && { mv gp/events.lhe.gz ${TAG}.lhe.gz; FILES="$FILES ${TAG}.lhe.gz"; }
[ "$KEEP_FULL" = 1 ] && { mv out/full.root out/${TAG}_full.root; FILES="$FILES out/${TAG}_full.root"; }
# stage the main ROOT file LAST so that its existence implies a complete job (used by the skip check)
for f in $(echo $FILES | tr ' ' '\n' | grep -v "out/${TAG}.root\$") out/${TAG}.root; do
  ok=0; for try in 1 2 3; do xrdcp -s "$f" "$EOSURL/$OUTDIR/$(basename $f)" && { ok=1; break; }; sleep 30; done
  [ $ok = 1 ] || { log "stage-out failed for $f"; exit 16; }
  r=$(xrdfs $EOSURL stat "$OUTDIR/$(basename $f)" | awk '/Size/{print $2}'); l=$(stat -c %s "$f")
  [ "$r" = "$l" ] || { log "size mismatch $f local=$l remote=$r"; exit 17; }
done
log "done OK"
