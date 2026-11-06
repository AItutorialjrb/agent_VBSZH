#!/usr/bin/env python3
"""G1 decisions D18/D21 — repeat-run isolation. TO BE RUN BY THE HUMAN (multi_r1's deny rules block the orchestrator
from editing other runs' .claude/ files, by design).

1. Adds Read/Edit deny rules to every repeat run's .claude/settings.json so repeats cannot read multi_r1 outputs
   that live outside runs/multi_r1/: p2/SPEC.md (contains multi_r1 G1 decisions), p2/production/**,
   p2/metrics/review_log.csv, p2/metrics/usage_p2.*; and Edit of p2/SPEC_G0.md (frozen).
2. (D21) multi_r2/r3: moves .claude/agents/ -> .claude/role_prompts/ so the custom agent types are NOT loaded
   natively; the orchestrator then spawns general-purpose subagents with model override + the role prompt text,
   as in multi_r1 Phase 01-03. Skip with --keep-agents.
3. (A2, 2026-11-06) --single-r1-prod: SECOND STAGE, run only after tag wh-prod-v1 and after single_r1 has
   finished its WH Phase 01-03 (G1). Lets single_r1 read the frozen WH production data
   (p2/production/wh/**: ntuples, SAMPLES.csv, FORMAT.md, SHA256SUMS) and nothing else from multi_r1:
   removes the Read/Edit deny on p2/production/** for single_r1 only, adds Read+Edit deny on
   p2/production/hh/** and Edit deny on p2/production/wh/** (read-only). runs/multi_r1/** stays denied.
Idempotent. Usage: python3 p2/metrics/g1_repeat_isolation.py [--keep-agents] [--dry-run] [--single-r1-prod]
"""
import json, os, sys, shutil
P2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = "//" + P2.lstrip("/")
ADD = [f"Read({A}/SPEC.md)", f"Edit({A}/SPEC.md)", f"Edit({A}/SPEC_G0.md)",
       f"Read({A}/production/**)", f"Edit({A}/production/**)",
       f"Read({A}/metrics/review_log.csv)", f"Read({A}/metrics/usage_p2.csv)", f"Read({A}/metrics/usage_p2.md)",
       f"Read({A}/metrics/heptools_*)"]
dry = "--dry-run" in sys.argv
for run in ["multi_r2", "multi_r3", "single_r1", "single_r2", "single_r3"]:
    f = f"{P2}/runs/{run}/.claude/settings.json"
    s = json.load(open(f)); deny = s.setdefault("permissions", {}).setdefault("deny", [])
    new = [r for r in ADD if r not in deny]
    print(f"{run}: +{len(new)} deny rules")
    if not dry and new:
        deny += new; json.dump(s, open(f, "w"), indent=1); open(f, "a").write("\n")
    a, r = f"{P2}/runs/{run}/.claude/agents", f"{P2}/runs/{run}/.claude/role_prompts"
    if run.startswith("multi") and "--keep-agents" not in sys.argv and os.path.isdir(a):
        print(f"{run}: move .claude/agents -> .claude/role_prompts")
        if not dry: shutil.move(a, r)
if "--single-r1-prod" in sys.argv:
    f = f"{P2}/runs/single_r1/.claude/settings.json"; s = json.load(open(f)); deny = s["permissions"]["deny"]
    drop = [f"Read({A}/production/**)", f"Edit({A}/production/**)"]
    add = [f"Read({A}/production/hh/**)", f"Edit({A}/production/hh/**)", f"Edit({A}/production/wh/**)"]
    new = [r for r in deny if r not in drop] + [r for r in add if r not in deny]
    print(f"single_r1 (A2 stage 2): -{len(deny) + len([r for r in add if r not in deny]) - len(new)} +{len([r for r in add if r not in deny])} rules")
    if not dry: s["permissions"]["deny"] = new; json.dump(s, open(f, "w"), indent=1); open(f, "a").write("\n")
print("done (dry run)" if dry else "done; commit with: git add p2/runs/*/.claude && git commit")
