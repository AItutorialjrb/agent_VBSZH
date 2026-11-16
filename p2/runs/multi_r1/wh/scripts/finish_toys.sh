#!/bin/bash
# post-condor regeneration (run when all of 913403-913407 are done): xfeed, scheme, toy aggregation, VH json/md, final report, reports, paper package, verify requests
set -e; cd /eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh; export STAT_V12=1 STAT_V11=1 STAT_TABLE=table_v12 STAT_YIELDS=yields_v12
bash scripts/envrun.sh python3 -P scripts/xfeed.py > /dev/null; python3 scripts/vh_scheme.py > /dev/null
bash scripts/envrun.sh python3 -P scripts/toys_agg.py > /dev/null; python3 scripts/make_vh_json.py > /dev/null; python3 scripts/make_vh_md.py; python3 scripts/make_final.py; python3 scripts/make_report_07.py; python3 scripts/make_report_05a.py; python3 scripts/make_addendum_05.py > /dev/null
bash scripts/envrun.sh python3 -P scripts/make_paper.py; python3 scripts/make_verify_requests.py
