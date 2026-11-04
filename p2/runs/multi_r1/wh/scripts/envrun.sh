#!/bin/bash
# run a command inside the pinned stack: scripts/envrun.sh python3 -P script.py ...
source /eos/home-r/rjiang/vbs_zh_codex_starter/p2/lib/scripts/setup_stack.sh || exit 1
exec "$@"
