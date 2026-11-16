#!/bin/bash
# One command: regenerates every table (.tex), figure (PDF+PNG) and paper_numbers.json of the paper package from the analysis jsons.
# Usage: bash p2/combination/paper/regenerate.sh   (login node is fine: json + matplotlib only)
cd /eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh && bash scripts/envrun.sh python3 -P scripts/make_paper.py
