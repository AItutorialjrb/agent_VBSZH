#!/bin/bash
# Patch 002 of p2/lib/scripts/run_py8_delphes.sh: identical physics; stack/common CP5 card read from p2/lib (read-only),
# sample cmnd and Delphes card passed explicitly.  Usage: run_py8_delphes_wh.sh <lhe(.gz)> <sample-cmnd> <nevents> <pyseed> <out.root> [delphes_card]
set -o pipefail
LIB=${LIB:-/eos/home-r/rjiang/vbs_zh_codex_starter/p2/lib}
LHE=$1; SC=$2; N=$3; SEED=$4; OUT=$5; DC=${6:-$LIB/cards/phase04_candidates/delphes_card_CMS_slim_v1.tcl}
source $LIB/scripts/setup_stack.sh >/dev/null
W=$(dirname "$OUT"); mkdir -p "$W"
case "$LHE" in *.gz) gunzip -c "$LHE" > "$W/in.lhe"; LHE="$W/in.lhe";; esac
CM="$W/py8.cmnd"
cat $LIB/cards/phase03_smoke/py8_common_CP5.cmnd > "$CM"
sed -e "s#NEVENTS#$N#; s#LHEFILE#$LHE#; s#PYSEED#$SEED#" "$SC" >> "$CM"
cp "$DC" "$W/delphes_card.tcl"
sed -i "1i set RandomSeed $(( SEED % 900000000 + 1 ))" "$W/delphes_card.tcl"
( cd "$W" && DelphesPythia8 delphes_card.tcl py8.cmnd "$OUT" )
