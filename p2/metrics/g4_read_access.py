#!/usr/bin/env python3
"""G4 (human decision D48, 2026-11-14) — read access for the multi_r1 orchestrator. TO BE RUN BY THE HUMAN.
The multi_r1 orchestrator must not edit its own permission settings.

D48: "watch runs/single_r1 STATUS and the ledger; read only its reports and metrics" and "(a) Blind G1 audit:
strip arm/run identifiers from the six WH Phase 01-03 reports (multi_r1-r3, single_r1-r3)".
multi_r1's D18 isolation denies Read of every other run directory and of p2/metrics/raw/**.

This script edits ONLY p2/runs/multi_r1/.claude/settings.json:
  - removes   Read(p2/runs/<run>/**)                for run in multi_r2, multi_r3, single_r1, single_r2, single_r3
  - adds      Read deny on code/data subtrees of those runs, so only reports, STATUS/PROGRESS and reviews stay readable:
              p2/runs/<run>/wh/{work,scripts,cards,config,patches}/**, p2/runs/<run>/hh/**, p2/runs/<run>/.claude/**
  - removes   Read(p2/metrics/raw/**)               (token/cost accounting for AI_results.md via metrics/parse_usage.py)
  - keeps     every Edit deny (other runs stay write-protected).
Idempotent. Run it only once all repeat runs have finished. The session needs a restart to load the new rules.
Usage: python3 p2/metrics/g4_read_access.py [--dry-run]
"""
import json, os, sys
P2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = "//" + P2.lstrip("/")
RUNS = ["multi_r2", "multi_r3", "single_r1", "single_r2", "single_r3"]
f = f"{P2}/runs/multi_r1/.claude/settings.json"
s = json.load(open(f)); deny = s["permissions"]["deny"]
drop = [f"Read({A}/runs/{r}/**)" for r in RUNS] + [f"Read({A}/metrics/raw/**)"]
add = []
for r in RUNS:
    add += [f"Read({A}/runs/{r}/wh/{d}/**)" for d in ("work", "scripts", "cards", "config", "patches")]
    add += [f"Read({A}/runs/{r}/hh/**)", f"Read({A}/runs/{r}/.claude/**)"]
rm = [x for x in drop if x in deny]; new = [x for x in add if x not in deny]
print(f"remove {len(rm)} Read deny rules:", *rm, sep="\n  ")
print(f"add {len(new)} narrower Read deny rules:", *new, sep="\n  ")
if "--dry-run" not in sys.argv:
    s["permissions"]["deny"] = [x for x in deny if x not in rm] + new
    json.dump(s, open(f, "w"), indent=1); open(f, "a").write("\n")
    print("written:", f)
