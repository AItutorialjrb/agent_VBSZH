#!/bin/bash
# Generic analysis job (2026-11-03): run a project Python script on a worker (EOS FUSE paths) with the pinned stack.
# Usage: pyjob.sh <script relative to project> [args...]
P=/eos/user/r/rjiang/vbs_zh_codex_starter; WD=${_CONDOR_SCRATCH_DIR:-$PWD}; cd "$WD" || exit 10
export PROJECT=$P; source $P/scripts/setup_stack.sh >/dev/null 2>&1 || exit 11
S=$1; shift; T0=$(date +%s); python3 -P $P/$S "$@"; RC=$?; echo "rc=$RC wall_s=$(( $(date +%s)-T0 )) host=$(hostname)"; exit $RC
