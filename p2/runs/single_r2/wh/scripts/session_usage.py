#!/usr/bin/env python3
"""Token/time usage of THIS run's Claude Code session (single_r2). De-duplicates assistant records by (message.id, requestId) as
lib/scripts/metrics/parse_usage.py. Phase windows are given as UTC boundaries; active time = sum of gaps < 10 min.
Usage: session_usage.py <session.jsonl> <label=startUTC> [<label=startUTC> ...] """
import json, sys, datetime as dt
T = lambda s: dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
win = [(a.split("=")[0], T(a.split("=")[1])) for a in sys.argv[2:]]
def ph(t):
    p = None
    for n, s in win:
        if t >= s: p = n
    return p
U = {n: dict(input=0, output=0, cache_create=0, cache_read=0, api_msgs=0, tool_calls=0, human_prompts=0, active_s=0.0, first=None, last=None) for n, _ in win}
seen = set(); last = None
for l in open(sys.argv[1]):
    try: r = json.loads(l)
    except Exception: continue
    ts = r.get("timestamp")
    if not ts: continue
    t = T(ts); p = ph(t)
    if p is None: continue
    u = U[p]; u["first"] = u["first"] or ts; u["last"] = ts
    if last and (t - last).total_seconds() < 600 and ph(last) == p: u["active_s"] += (t - last).total_seconds()
    last = t
    m = r.get("message", {})
    if r.get("type") == "assistant":
        k = (m.get("id"), r.get("requestId"))
        for c in m.get("content", []) or []:
            if isinstance(c, dict) and c.get("type") == "tool_use": u["tool_calls"] += 1
        if k in seen: continue
        seen.add(k); us = m.get("usage", {}) or {}
        u["input"] += us.get("input_tokens", 0); u["output"] += us.get("output_tokens", 0)
        u["cache_create"] += us.get("cache_creation_input_tokens", 0); u["cache_read"] += us.get("cache_read_input_tokens", 0); u["api_msgs"] += 1
    elif r.get("type") == "user" and isinstance(m.get("content"), str) and not r.get("isMeta"):
        u["human_prompts"] += 1
tot = {k: sum(U[n][k] for n in U) for k in ("input", "output", "cache_create", "cache_read", "api_msgs", "tool_calls", "human_prompts", "active_s")}
print("| window | first UTC | last UTC | input | output | cache write | cache read | API msgs | tool calls | human prompts | active [min] |")
print("|---|---|---|---|---|---|---|---|---|---|---|")
for n, u in list(U.items()) + [("TOTAL", dict(tot, first="", last=""))]:
    print(f"| {n} | {(u['first'] or '')[:19]} | {(u['last'] or '')[:19]} | {u['input']:,} | {u['output']:,} | {u['cache_create']:,} | {u['cache_read']:,} | {u['api_msgs']} | {u['tool_calls']} | {u['human_prompts']} | {u['active_s']/60:.0f} |")
