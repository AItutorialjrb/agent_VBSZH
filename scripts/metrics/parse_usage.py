#!/usr/bin/env python3
"""C (2026-11-03): per-phase agent usage for process ZH.
Claude Code: metrics/raw/claude/*.jsonl (read-only backup). Assistant records are de-duplicated by (message.id, requestId)
  (a streamed message is written as several records with the same usage). Per phase: input / output / cache-creation /
  cache-read tokens, API messages, human prompts, tool calls, compactions; wall time = phase window; active time = sum of
  gaps < 10 min between consecutive records.
Codex (Phase 00-01): metrics/raw/codex/rollout-*.jsonl (read-only copy; ~/.codex / $CODEX_HOME never touched): last
  cumulative token_count per session (input incl. cached, cached, output, reasoning).
Condor: core-hours = RemoteWallClockTime x RequestCpus / 3600 per job, assigned to the phase containing QDate; from
  `condor_history <user>` (cached in metrics/condor_history.csv; refreshed with --condor-raw).
Outputs: metrics/usage_by_phase.csv and .md. Usage: python3 -P scripts/metrics/parse_usage.py [--condor-raw <condor_history dump>]"""
import csv, json, glob, os, sys, datetime as dt
P = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); M = f"{P}/metrics"
ph = list(csv.DictReader(open(f"{M}/phases.csv")))
T = lambda s: dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
NOW = dt.datetime.now(dt.timezone.utc)
def phase_of(t):
    for r in ph:
        if T(r["start_utc"]) <= t and (not r["end_utc"] or t < T(r["end_utc"])): return r["phase"]
    return None
U = {r["phase"]: dict(input=0, output=0, cache_create=0, cache_read=0, api_msgs=0, prompts=0, tool_calls=0, compactions=0, active_s=0.0, records=0) for r in ph}
seen = set(); last = None; lastp = None
RECS = []
for f in sorted(glob.glob(f"{M}/raw/claude/*.jsonl")):
    for l in open(f):
        d = json.loads(l); ts = d.get("timestamp")
        if ts: RECS.append((T(ts), d))
RECS.sort(key=lambda x: x[0])   # records are not strictly time-ordered in the file (background tasks, sidechains)
if True:
    for t, d in RECS:
        p = phase_of(t)
        if p is None: continue
        u = U[p]; u["records"] += 1
        if last is not None and lastp == p and 0 < (t - last).total_seconds() < 600: u["active_s"] += (t - last).total_seconds()
        last, lastp = t, p
        if d.get("type") == "assistant":
            m = d.get("message", {}); key = (m.get("id"), d.get("requestId"))
            u["tool_calls"] += sum(1 for c in m.get("content", []) if isinstance(c, dict) and c.get("type") == "tool_use")
            if key in seen: continue
            seen.add(key); us = m.get("usage", {}) or {}
            u["api_msgs"] += 1; u["input"] += us.get("input_tokens", 0) or 0; u["output"] += us.get("output_tokens", 0) or 0
            u["cache_create"] += us.get("cache_creation_input_tokens", 0) or 0; u["cache_read"] += us.get("cache_read_input_tokens", 0) or 0
        elif d.get("type") == "user" and not d.get("isMeta") and not d.get("isCompactSummary") and isinstance(d.get("message", {}).get("content"), str) \
                and not d["message"]["content"].startswith(("<local-command", "<command-name", "<task-notification")):
            u["prompts"] += 1
        elif d.get("type") == "system" and d.get("subtype") == "compact_boundary": u["compactions"] += 1
for f in sorted(glob.glob(f"{M}/raw/codex/rollout-*.jsonl")):
    tok = None; first = None; lastc = None; n = 0; prompts = 0; tools = 0
    for l in open(f):
        d = json.loads(l); t = T(d["timestamp"]); first = first or t; lastc = t; pl = d.get("payload", {})
        if pl.get("type") == "token_count" and pl.get("info"): tok = pl["info"]["total_token_usage"]; n += 1
        if d.get("type") == "response_item" and pl.get("type") in ("custom_tool_call", "function_call"): tools += 1
        if d.get("type") == "response_item" and pl.get("type") == "message" and pl.get("role") == "user":
            prompts += not " ".join(x.get("text", "") for x in pl.get("content", []) if isinstance(x, dict)).lstrip().startswith("# AGENTS.md")
    p = phase_of(first); u = U[p]
    u.update(input=tok["input_tokens"] - tok["cached_input_tokens"], cache_read=tok["cached_input_tokens"], output=tok["output_tokens"],
             reasoning=tok.get("reasoning_output_tokens", 0), api_msgs=n, prompts=prompts, tool_calls=tools, active_s=(lastc - first).total_seconds())
CH = f"{M}/condor_history.csv"
# condor_history is slow (minutes) on the EosSubmit schedd: dump it once, then pass the dump with --condor-raw <file>:
#   condor_history rjiang -constraint 'QDate > 1793620000' -af ClusterId ProcId QDate RemoteWallClockTime RequestCpus JobStatus ExitCode Cmd > dump.txt
if "--condor-raw" in sys.argv:
    out = open(sys.argv[sys.argv.index("--condor-raw") + 1]).read()
    old = {(r["cluster"], r["proc"]): r for r in csv.DictReader(open(CH))} if os.path.exists(CH) else {}
    for line in out.splitlines():
        x = line.split()
        if len(x) < 8: continue
        old[(x[0], x[1])] = dict(cluster=x[0], proc=x[1], qdate=x[2], wall_s=x[3], cpus=x[4], status=x[5], exit=x[6], cmd=os.path.basename(x[7]))
    with open(CH, "w", newline="") as fh:
        w = csv.DictWriter(fh, ["cluster", "proc", "qdate", "wall_s", "cpus", "status", "exit", "cmd"]); w.writeheader(); w.writerows(old.values())
for r in ph: U[r["phase"]].update(core_h=0.0, jobs=0)
for r in (csv.DictReader(open(CH)) if os.path.exists(CH) else []):
    try: t = dt.datetime.fromtimestamp(int(r["qdate"]), dt.timezone.utc); p = phase_of(t)
    except ValueError: continue
    if p and r["wall_s"] not in ("undefined", ""):
        U[p]["core_h"] += float(r["wall_s"])*float(r["cpus"] if r["cpus"] != "undefined" else 1)/3600; U[p]["jobs"] += 1
cols = ["phase", "agent", "label", "start_utc", "end_utc", "wall_h", "active_h", "prompts", "api_msgs", "tool_calls", "compactions",
        "input", "cache_create", "cache_read", "output", "reasoning", "condor_jobs", "condor_core_h"]
rows = []
for r in ph:
    u = U[r["phase"]]; end = T(r["end_utc"]) if r["end_utc"] else NOW
    rows.append(dict(phase=r["phase"], agent=r["agent"], label=r["label"], start_utc=r["start_utc"], end_utc=r["end_utc"] or f"(open, {NOW:%Y-%m-%dT%H:%MZ})",
                     wall_h=round((end - T(r["start_utc"])).total_seconds()/3600, 2), active_h=round(u["active_s"]/3600, 2), prompts=u["prompts"], api_msgs=u["api_msgs"],
                     tool_calls=u["tool_calls"], compactions=u["compactions"], input=u["input"], cache_create=u["cache_create"], cache_read=u["cache_read"],
                     output=u["output"], reasoning=u.get("reasoning", ""), condor_jobs=u["jobs"], condor_core_h=round(u["core_h"], 1)))
with open(f"{M}/usage_by_phase.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, cols); w.writeheader(); w.writerows(rows)
md = ["| phase | agent | wall [h] | active [h] | human msgs | API msgs | tool calls | compactions | input | cache write | cache read | output | condor jobs | core-h |", "|" + "---|"*14]
for x in rows:
    md.append(f"| {x['phase']} | {x['agent']} | {x['wall_h']} | {x['active_h']} | {x['prompts']} | {x['api_msgs']} | {x['tool_calls']} | {x['compactions']} | {x['input']:,} | {x['cache_create']:,} | {x['cache_read']:,} | {x['output']:,} | {x['condor_jobs']} | {x['condor_core_h']} |")
tot = {k: sum(x[k] for x in rows if isinstance(x[k], (int, float))) for k in ("input", "cache_create", "cache_read", "output", "condor_core_h", "condor_jobs", "prompts", "api_msgs")}
md.append(f"| **total** | | | | {tot['prompts']} | {tot['api_msgs']} | | | {tot['input']:,} | {tot['cache_create']:,} | {tot['cache_read']:,} | {tot['output']:,} | {tot['condor_jobs']} | {tot['condor_core_h']:.1f} |")
open(f"{M}/usage_by_phase.md", "w").write("# ZH usage by phase (generated by scripts/metrics/parse_usage.py)\n\n" + "\n".join(md) + "\n\nPhase windows: metrics/phases.csv (boundaries = human prompt times). Codex: input excludes cached input (cache read column). Claude: input = uncached input tokens. Condor: jobs whose QDate falls in the phase window, from condor_history (retention-limited: older jobs may be missing; see the jobs column).\n")
print("\n".join(md))
