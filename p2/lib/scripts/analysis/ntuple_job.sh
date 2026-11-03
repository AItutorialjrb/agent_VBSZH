#!/bin/bash
# Batch ntupling: ntuple.py over a list of Delphes files (direct mode -> skimmed; ffN modes unskimmed), staged to EOS.
# Usage: ntuple_job.sh <out_basename> <mode> <comma-separated delphes files (EOS fuse paths)>
set -o pipefail
OUT=$1; MODE=$2; FILES=$3
P=/eos/user/r/rjiang/vbs_zh_codex_starter; DEST=$P/work/final_ntuples
WD=${_CONDOR_SCRATCH_DIR:-$PWD}; cd "$WD" || exit 10
export PROJECT=$P; source $P/scripts/setup_stack.sh || exit 11
python3 -P $P/scripts/analysis/ntuple.py raw.npz $MODE $FILES || exit 12
if [ "$MODE" = direct ]; then python3 -P $P/scripts/analysis/skim_npz.py raw.npz out.npz || exit 13; else mv raw.npz out.npz; fi
xrdcp -f -s out.npz root://eosuser.cern.ch/$DEST/$OUT.npz || exit 16
rm -f raw.npz out.npz; echo "done OK $OUT"
