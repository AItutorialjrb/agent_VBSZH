#!/bin/bash
# usage: job.sh <name> <modes> <files>; writes p2/combination/zh_check/out/<name>_{rate,dir,ffm}.npz
set -o pipefail
Z=/eos/home-r/rjiang/vbs_zh_codex_starter; WD=${_CONDOR_SCRATCH_DIR:-$PWD}; cd "$WD" || exit 10
export PROJECT=$Z; source $Z/scripts/setup_stack.sh >/dev/null 2>&1 || exit 11
python3 -P $Z/p2/combination/zh_check/zh_ntuple.py loc "${2//+/,}" "$3" || exit 12
for f in loc_*.npz; do xrdcp -f -s $f root://eosuser.cern.ch//eos/user/r/rjiang/vbs_zh_codex_starter/p2/combination/zh_check/out/${1}${f#loc}; done || exit 16
echo "done OK $1"
