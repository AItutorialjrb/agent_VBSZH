#!/bin/bash
# Local VALIDATION chain (1000 events): gridpack -> LHE -> PY8 (forced H->aa) + Delphes slim_v1 (Particle kept) -> validate_delphes_wh.py
# Usage: local_chain.sh <sample> <J> <nev> <py_cmnd>
set -o pipefail
WH=/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/single_r2/wh
S=$1; J=$2; NEV=$3; CM=$4
SEED=$(python3 $WH/scripts/seeds.py $S $J) || exit 4
GP=$(ls $WH/work/gridpacks/${S}_s*.tar.gz | head -1)
SCR=/tmp/$USER/wh_single_r2_chain/${S}_s$SEED; OUT=$WH/work/local/${S}_s$SEED
[ -e "$OUT/done" ] && { echo "exists"; exit 3; }
rm -rf "$SCR"; mkdir -p "$SCR/gp" "$OUT"
source /eos/home-r/rjiang/vbs_zh_codex_starter/p2/lib/scripts/setup_stack.sh >/dev/null
tar xzf "$GP" -C "$SCR/gp"
T0=$(date +%s)
( cd "$SCR/gp" && ./run.sh $NEV $SEED ) > "$OUT/gridpack.log" 2>&1 || { echo gridpack failed; exit 5; }
cp "$SCR/gp/events.lhe.gz" "$OUT/${S}_s$SEED.lhe.gz"
XS=$(zcat "$OUT/${S}_s$SEED.lhe.gz" | sed -n '/<init>/,/<\/init>/p' | sed -n 3p)
T1=$(date +%s)
PYSEED=$((SEED + 100000000))
bash $WH/scripts/run_py8_delphes_wh.sh "$OUT/${S}_s$SEED.lhe.gz" $WH/cards/py8/$CM $NEV $PYSEED "$SCR/delphes.root" > "$OUT/py8_delphes.log" 2>&1 || { echo py8 failed; tail $OUT/py8_delphes.log; exit 6; }
T2=$(date +%s)
cp "$SCR/delphes.root" "$OUT/${S}_s${SEED}_full.root"
echo "sample=$S mg_seed=$SEED py_seed=$PYSEED nev=$NEV gridpack=$GP lhe_init='$XS' t_gp=$((T1-T0)) t_py8del=$((T2-T1)) host=$(hostname) utc=$(date -u +%FT%TZ)" > "$OUT/status.txt"
grep -E '^ \| sum' "$OUT/py8_delphes.log" | tail -1 >> "$OUT/status.txt"
rm -rf "$SCR"; touch "$OUT/done"; cat "$OUT/status.txt"
