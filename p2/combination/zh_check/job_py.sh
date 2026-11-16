#!/bin/bash
# usage: job_py.sh <script in zh_check> <args...>  (stack + python -P)
Z=/eos/home-r/rjiang/vbs_zh_codex_starter; WD=${_CONDOR_SCRATCH_DIR:-$PWD}; cd "$WD" || exit 10
export PROJECT=$Z; source $Z/scripts/setup_stack.sh >/dev/null 2>&1 || exit 11
S=$1; shift; python3 -P $Z/p2/combination/zh_check/$S "$@"
