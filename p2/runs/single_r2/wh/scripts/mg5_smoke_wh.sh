#!/bin/bash
# WH interactive smoke runner (patch 001 of p2/lib/scripts/mg5_smoke.sh): same logic, but cards/outputs live in this
# process directory (never the frozen ZH work/), seed taken from the registry, diagram/process summary extracted.
# Usage: scripts/mg5_smoke_wh.sh <card-path-relative-to-wh> <sample-name> [J=0] [timeout_s=900]
set -o pipefail
WH=/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/single_r2/wh
CARDP=$1; SAMPLE=$2; J=${3:-0}; TMO=${4:-900}
[ -n "$CARDP" ] && [ -n "$SAMPLE" ] || { echo "usage: $0 card sample [J] [timeout]"; exit 2; }
SEED=$(python3 $WH/scripts/seeds.py "$SAMPLE" "$J") || exit 4
SCR=${SMOKE_SCRATCH:-/tmp/$USER/wh_single_r2_smoke}; mkdir -p "$SCR"
OUT=$SCR/${SAMPLE}_s$SEED; DEST=$WH/work/smoke/${SAMPLE}_s$SEED
[ -e "$OUT" ] && { echo "scratch $OUT exists; refusing to overwrite"; exit 3; }
[ -e "$DEST/status.txt" ] && { echo "$DEST/status.txt exists; refusing to overwrite"; exit 3; }
mkdir -p "$DEST"
source /eos/home-r/rjiang/vbs_zh_codex_starter/p2/lib/scripts/setup_stack.sh >/dev/null
sed -e "s#OUTDIR#$OUT#g" -e "s#SEED#$SEED#g" "$WH/$CARDP" > "$DEST/run.mg5"
T0=$(date +%s)
( cd "$SCR" && timeout "$TMO" mg5_aMC "$DEST/run.mg5" ) > "$DEST/mg5.log" 2>&1
RC=$?; T1=$(date +%s)
echo "sample=$SAMPLE card=$CARDP seed=$SEED rc=$RC wall_s=$((T1-T0)) host=$(hostname) stack=$VBSZH_STACK_TAG utc=$(date -u +%FT%TZ) card_sha256=$(sha256sum $WH/$CARDP|cut -c1-16)" > "$DEST/status.txt"
cp -r "$OUT/Cards" "$DEST/" 2>/dev/null
cp "$OUT/SubProcesses/subproc.mg" "$DEST/" 2>/dev/null
ls -d "$OUT"/SubProcesses/P*/ 2>/dev/null | wc -l > "$DEST/n_subproc_dirs.txt"
# list of all partonic subprocesses (one line per process in each P* dir) for order/flavour audits
for d in "$OUT"/SubProcesses/P*/; do [ -f "$d/auto_dsig.f" ] && grep -h "^C *Process:" "$d"/matrix*.f 2>/dev/null; done | sort -u > "$DEST/processes.txt"
for f in "$OUT"/Events/run_01*/*banner.txt "$OUT"/Events/run_01*/*.lhe.gz "$OUT"/HTML/run_01*/results.html; do [ -f "$f" ] && cp "$f" "$DEST/"; done
ls "$OUT"/*gridpack*.tar.gz >/dev/null 2>&1 && cp "$OUT"/*gridpack*.tar.gz "$DEST/"
grep -E "Total: .* processes with .* diagrams|^INFO: Generated helas calls" "$DEST/mg5.log" | head -5 >> "$DEST/status.txt"
grep -E "Cross-section :|Nb of events :" "$DEST/mg5.log" | tail -2 >> "$DEST/status.txt"
[ "${KEEP_SCRATCH:-0}" = 1 ] || rm -rf "$OUT"
cat "$DEST/status.txt"
