#!/bin/bash
# Usage: run_py8_delphes.sh <lhe.gz> <sample-cmnd> <nevents> <pyseed> <out.root>
# Concatenates py8_common_CP5.cmnd + sample cmnd, runs DelphesPythia8 with the stock LCG_110 CMS card.
set -o pipefail
PROJECT=${PROJECT:-/eos/home-r/rjiang/vbs_zh_codex_starter}
LHE=$1; SC=$2; N=$3; SEED=$4; OUT=$5
source $PROJECT/scripts/setup_stack.sh >/dev/null
W=$(dirname "$OUT"); mkdir -p "$W"
case "$LHE" in *.gz) gunzip -c "$LHE" > "$W/in.lhe"; LHE="$W/in.lhe";; esac
CM="$W/py8.cmnd"
cat $PROJECT/cards/phase03_smoke/py8_common_CP5.cmnd > "$CM"
sed -e "s#NEVENTS#$N#; s#LHEFILE#$LHE#; s#PYSEED#$SEED#" "$SC" >> "$CM"
cp "${DELPHES_CARD:-$DELPHES_CMS_CARD}" "$W/delphes_card_CMS.tcl"   # override with DELPHES_CARD=<path>
# Delphes smearing seed: the stock card leaves RandomSeed=0 (clock-seeded, NOT reproducible) -> pin it to the job seed
sed -i "1i set RandomSeed $(( SEED % 900000000 + 1 ))" "$W/delphes_card_CMS.tcl"
( cd "$W" && DelphesPythia8 delphes_card_CMS.tcl py8.cmnd "$OUT" )
