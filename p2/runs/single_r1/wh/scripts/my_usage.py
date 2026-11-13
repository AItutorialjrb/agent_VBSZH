#!/usr/bin/env python3
"""single_r1: token / time usage of THIS run's Claude session from its own transcript (dedup by message id: a streamed
message is written as several records with the same usage). Segments by UTC boundaries from metrics/ledger.csv.
Cost-equivalent from p2/metrics/prices.json (cache writes: the 5m / 1h split is taken from usage.cache_creation if present).
Usage: python3 -P wh/scripts/my_usage.py <transcript.jsonl> [segment_boundary_utc ...]"""
import sys, json
from datetime import datetime
f = sys.argv[1]; bounds = sorted(sys.argv[2:])
P = json.load(open("/eos/home-r/rjiang/vbs_zh_codex_starter/p2/metrics/prices.json"))
seen, rows, ts_all, sidechain = set(), [], [], 0
for line in open(f):
    try: r = json.loads(line)
    except Exception: continue
    t = r.get("timestamp")
    if t: ts_all.append(t)
    m = r.get("message") or {}
    if r.get("isSidechain"): sidechain += 1
    u = m.get("usage") if isinstance(m, dict) else None
    if not u or r.get("type") != "assistant": continue
    key = m.get("id") or r.get("requestId") or r.get("uuid")
    if key in seen: continue
    seen.add(key)
    cc = u.get("cache_creation") or {}
    rows.append(dict(t=t, model=m.get("model", "?"), inp=u.get("input_tokens", 0), out=u.get("output_tokens", 0),
                     cw=u.get("cache_creation_input_tokens", 0), cw1h=cc.get("ephemeral_1h_input_tokens", 0), cr=u.get("cache_read_input_tokens", 0)))
def seg(t):
    for i, b in enumerate(bounds):
        if t < b: return i
    return len(bounds)
names = (["before " + bounds[0]] if bounds else []) + [f"{a} → {b}" for a, b in zip(bounds, bounds[1:])] + ([f"after {bounds[-1]}"] if bounds else ["all"])
agg = {}
for r in rows:
    k = (seg(r["t"]), r["model"]); a = agg.setdefault(k, dict(n=0, inp=0, out=0, cw=0, cw1h=0, cr=0, t0=r["t"], t1=r["t"]))
    a["n"] += 1; a["t1"] = r["t"]
    for x in ("inp", "out", "cw", "cw1h", "cr"): a[x] += r[x]
print(f"transcript records with usage (dedup): {len(rows)}; sidechain records: {sidechain}; first/last timestamp: {min(ts_all)} / {max(ts_all)}")
print("| segment | model | API calls | input | output | cache write | cache read | cost-eq. USD | first → last call (UTC) |\n|---|---|---|---|---|---|---|---|---|")
tot = 0
for (s, mdl), a in sorted(agg.items()):
    pr = P.get(mdl, P["claude-opus-5-5"])
    usd = (a["inp"] * pr["input"] + a["out"] * pr["output"] + (a["cw"] - a["cw1h"]) * pr["cache_write_5m"] + a["cw1h"] * pr["cache_write_1h"] + a["cr"] * pr["cache_read"]) / 1e6
    tot += usd
    print(f"| {names[s]} | {mdl} | {a['n']} | {a['inp']:,} | {a['out']:,} | {a['cw']:,} | {a['cr']:,} | {usd:.2f} | {a['t0'][11:19]} → {a['t1'][11:19]} |")
print(f"| **total** | | | | | | | **{tot:.2f}** | |")
fmt = "%Y-%m-%dT%H:%M:%S"
ts = sorted(datetime.strptime(x[:19], fmt) for x in ts_all)
active = sum(min((b - a).total_seconds(), 300) for a, b in zip(ts, ts[1:]))
print(f"wall (first→last transcript record): {(ts[-1]-ts[0]).total_seconds()/3600:.2f} h; active (gaps capped at 5 min): {active/3600:.2f} h")
