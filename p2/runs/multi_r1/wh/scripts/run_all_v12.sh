#!/bin/bash
# Rebuild the WH/ZH/VH results after changing the single lost-lepton input config/lostlep_qcd.json (and/or the production rows):
# 1 skim new rows (make_sub_py.py skim ... + condor), 2 yields + tables, 3 selection re-evaluation (frozen cuts/models, D45), 4 statistics + joint workspace tasks (condor), 5 reports and paper.
set -e; cd /eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh; export STAT_V12=1 STAT_V11=1 STAT_TABLE=table_v12 STAT_YIELDS=yields_v12
bash scripts/envrun.sh python3 -P scripts/bg_yields.py --v11 --tag _v12 > work/bgmodel/bg_yields_v12.log 2>&1
V12=1 bash scripts/envrun.sh python3 -P scripts/sel_tables.py > work/sel/tables_v12.log 2>&1
bash scripts/envrun.sh python3 -P scripts/sel_v12.py; bash scripts/envrun.sh python3 -P scripts/ll_neff.py
echo "next: condor_submit work/condor/py_stat_v12.sub, py_stat_v12d.sub (z0mu/map2d), py_toys_*.sub; then scripts/vh_run.py ws, vh_scheme.py, vh_coup.py, toys_agg.py, make_report_*.py, make_final.py, make_vh_md.py, make_paper.py"
