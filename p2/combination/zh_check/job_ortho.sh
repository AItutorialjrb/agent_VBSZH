#!/bin/bash
set -o pipefail
Z=/eos/home-r/rjiang/vbs_zh_codex_starter; WD=${_CONDOR_SCRATCH_DIR:-$PWD}; cd "$WD" || exit 10
export PROJECT=$Z; source $Z/scripts/setup_stack.sh >/dev/null 2>&1 || exit 11
python3 -P $Z/p2/combination/zh_check/ortho.py loc.json "$1" "$2" || exit 12
xrdcp -f -s loc.json root://eosuser.cern.ch//eos/user/r/rjiang/vbs_zh_codex_starter/p2/combination/zh_check/out/ortho_$1.json || exit 16
echo done OK $1
