#!/bin/bash
# Interactive smoke test (tiny runs only).  Usage: scripts/mg5_smoke.sh <card-name> <seed> [timeout_s]
# Runs MG5 in node-local scratch, stages small outputs (cards, logs, xsec, gridpack/LHE) to EOS work/m5/<card>/.
set -o pipefail
PROJECT=/eos/home-r/rjiang/vbs_zh_codex_starter
CARD=$1; SEED=$2; TMO=${3:-900}
[ -n "$CARD" ] && [ -n "$SEED" ] || { echo "usage: $0 card seed [timeout]"; exit 2; }
SCR=${SMOKE_SCRATCH:-/tmp/$USER/vbszh_smoke}; mkdir -p "$SCR"
OUT=$SCR/$CARD; DEST=$PROJECT/work/m5/$CARD
[ -e "$OUT" ] && { echo "scratch $OUT exists; refusing to overwrite"; exit 3; }
mkdir -p "$DEST"
source $PROJECT/scripts/setup_stack.sh >/dev/null
sed -e "s#OUTDIR#$OUT#g" -e "s#SEED#$SEED#g" $PROJECT/cards/phase03_smoke/$CARD.mg5 > "$DEST/$CARD.run.mg5"
T0=$(date +%s)
( cd "$SCR" && timeout "$TMO" mg5_aMC "$DEST/$CARD.run.mg5" ) > "$DEST/mg5.log" 2>&1
RC=$?; T1=$(date +%s)
echo "card=$CARD seed=$SEED rc=$RC wall_s=$((T1-T0)) host=$(hostname) stack=$VBSZH_STACK_TAG utc=$(date -u +%FT%TZ)" > "$DEST/status.txt"
# stage small outputs
cp -r "$OUT/Cards" "$DEST/" 2>/dev/null
cp "$OUT/SubProcesses/subproc.mg" "$DEST/" 2>/dev/null
ls "$OUT"/SubProcesses/P*/ -d 2>/dev/null | wc -l > "$DEST/n_subproc_dirs.txt"
for f in "$OUT"/Events/run_01*/*banner.txt "$OUT"/Events/run_01*/*.lhe.gz "$OUT"/crossx.html "$OUT"/HTML/run_01*/results.html; do [ -f "$f" ] && cp "$f" "$DEST/"; done
ls "$OUT"/*gridpack*.tar.gz >/dev/null 2>&1 && cp "$OUT"/*gridpack*.tar.gz "$DEST/"
grep -E "Cross-section :|Nb of events :" "$DEST/mg5.log" | tail -2 >> "$DEST/status.txt"
cat "$DEST/status.txt"
