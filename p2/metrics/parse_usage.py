#!/usr/bin/env python3
"""p2 token / cost / time accounting, extending ZH scripts/metrics/parse_usage.py (zh-final-v1.1, frozen; logic for
de-duplication, prompt counting, compactions and active time is carried over unchanged).

Extensions for phase 2 (handoff §2.3, §8 step 1):
  * per-model, per-role, per-run, per-arm, per-phase aggregation, incl. subagent sidechains;
  * cost-equivalent from metrics/prices.json (5m / 1h cache writes split when the usage record provides it);
  * role attribution: main-session transcript -> 'orchestrator' (multi arm) or 'single' (single arm);
    subagent transcripts -> role from the spawn prompt tag 'ROLE=<role>' (first user message), else from the
    subagent .meta.json 'agentType', else 'subagent:unknown';
  * phase attribution: subagents -> 'PHASE=<p>' tag in the spawn prompt if present; everything else -> ledger
    windows (start/end events of the same run_id, role and process; 'ALL' process windows as fallback).

Inputs:  metrics/raw/claude/<run_id>/<session>.jsonl and metrics/raw/claude/<run_id>/<session>/subagents/*.jsonl
         (read-only copies; refresh with --sync <run_id>=<claude project dir> ...), metrics/ledger.csv, metrics/prices.json
Outputs: metrics/usage_p2.csv (one row per run, arm, role, model, phase) and metrics/usage_p2.md (tables by role/model
         and by phase). Usage: python3 -P p2/metrics/parse_usage.py [--sync multi_r1=/path/to/project_dir ...]
"""
import csv, json, glob, os, re, sys, shutil, datetime as dt
from collections import defaultdict
M = os.path.dirname(os.path.abspath(__file__))
RAW = f"{M}/raw/claude"
T = lambda s: dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
NOW = dt.datetime.now(dt.timezone.utc)

# ---- optional: copy transcripts (read-only source; never modified) ----
if "--sync" in sys.argv:
    for a in sys.argv[sys.argv.index("--sync") + 1:]:
        if "=" not in a: break
        run, src = a.split("=", 1); dst = f"{RAW}/{run}"; os.makedirs(dst, exist_ok=True)
        for f in glob.glob(f"{src}/*.jsonl") + glob.glob(f"{src}/*/subagents/*"):
            rel = os.path.relpath(f, src); os.makedirs(os.path.dirname(f"{dst}/{rel}"), exist_ok=True)
            shutil.copy2(f, f"{dst}/{rel}")

PR = json.load(open(f"{M}/prices.json"))
def cost(model, u):
    p = PR.get(model)
    if p is None:
        k = next((k for k in PR if not k.startswith("_") and k in (model or "")), None); p = PR.get(k)
    if p is None: return float("nan")
    cw5 = u["cw5"] if (u["cw5"] or u["cw1h"]) else u["cache_create"]
    return (u["input"]*p["input"] + cw5*p["cache_write_5m"] + u["cw1h"]*p["cache_write_1h"]
            + u["cache_read"]*p["cache_read"] + u["output"]*p["output"]) / 1e6

LED = list(csv.DictReader(open(f"{M}/ledger.csv")))
def windows(run, role, proc):
    w, open_ = [], {}
    for r in sorted(LED, key=lambda r: r["utc"]):
        if r["run_id"] != run or r["role"] != role or r["process"] != proc: continue
        if r["event"] == "start": open_[r["phase"]] = T(r["utc"])
        elif r["event"] in ("end", "gate") and r["phase"] in open_: w.append((r["phase"], open_.pop(r["phase"]), T(r["utc"])))
    w += [(p, t0, NOW) for p, t0 in open_.items()]
    return w
def phase_of(t, run, role):
    for proc in ("WH", "HH", "ALL"):
        for p, a, b in windows(run, role, proc):
            if a <= t < b: return p if proc == "ALL" else f"{proc}:{p}"
    return "unassigned"

ARM = lambda run: run.split("_")[0]
U = defaultdict(lambda: dict(input=0, output=0, cache_create=0, cw5=0, cw1h=0, cache_read=0, api_msgs=0, prompts=0,
                             tool_calls=0, compactions=0, active_s=0.0, first=None, last=None))
TAG = re.compile(r"ROLE=([\w-]+)"); PTAG = re.compile(r"PHASE=([\w:-]+)")

def text_of(d):
    c = d.get("message", {}).get("content")
    if isinstance(c, str): return c
    return " ".join(x.get("text", "") for x in (c or []) if isinstance(x, dict))

def parse(files, run, role0, sub):
    recs = []
    for f in files:
        for l in open(f):
            try: d = json.loads(l)
            except ValueError: continue
            if d.get("timestamp"): recs.append((T(d["timestamp"]), d, f))
    recs.sort(key=lambda x: x[0])
    role, ptag = role0, None
    if sub:
        first = next((d for _, d, _ in recs if d.get("type") == "user"), None)
        if first:
            m = TAG.search(text_of(first)); role = m.group(1) if m else role0
            mp = PTAG.search(text_of(first)); ptag = mp.group(1) if mp else None
    seen, last = set(), {}
    for t, d, f in recs:
        if not sub and d.get("isSidechain"): continue      # older layout: sidechains counted via their own files
        if sub and d.get("type") == "user":                 # resumed subagents: latest PHASE= tag wins
            mp = PTAG.search(text_of(d))
            if mp: ptag = mp.group(1)
        model = d.get("message", {}).get("model") if d.get("type") == "assistant" else None
        ph = ptag or phase_of(t, run, role if not sub else role)
        key0 = (run, ARM(run), role, ph)
        if d.get("type") == "assistant":
            if model in (None, "<synthetic>"): continue
            k = key0 + (model,); u = U[k]
            if k in last and 0 < (t - last[k]).total_seconds() < 600: u["active_s"] += (t - last[k]).total_seconds()
            last[k] = t; u["first"] = u["first"] or t; u["last"] = t
            m = d["message"]; mk = (m.get("id"), d.get("requestId"))
            u["tool_calls"] += sum(1 for c in m.get("content", []) if isinstance(c, dict) and c.get("type") == "tool_use")
            if mk in seen: continue
            seen.add(mk); us = m.get("usage", {}) or {}; cc = us.get("cache_creation") or {}
            u["api_msgs"] += 1; u["input"] += us.get("input_tokens", 0) or 0; u["output"] += us.get("output_tokens", 0) or 0
            u["cache_create"] += us.get("cache_creation_input_tokens", 0) or 0; u["cache_read"] += us.get("cache_read_input_tokens", 0) or 0
            u["cw5"] += cc.get("ephemeral_5m_input_tokens", 0) or 0; u["cw1h"] += cc.get("ephemeral_1h_input_tokens", 0) or 0
        elif not sub and d.get("type") == "user" and not d.get("isMeta") and not d.get("isCompactSummary") \
                and not any(isinstance(x, dict) and x.get("type") == "tool_result" for x in (d.get("message", {}).get("content") or []) if not isinstance(d["message"]["content"], str)) \
                and text_of(d).strip() \
                and not text_of(d).lstrip().startswith(("<local-command", "<command-name", "<task-notification", "<system-reminder", "Tool loaded")):
            # ext. vs ZH: list-form user content (pasted text) also counts as a human message
            U[key0 + ("human",)]["prompts"] += 1
        elif d.get("type") == "system" and d.get("subtype") == "compact_boundary":
            U[key0 + ("human",)]["compactions"] += 1

for rd in sorted(glob.glob(f"{RAW}/*/")):
    run = os.path.basename(rd.rstrip("/")); main_role = "orchestrator" if ARM(run) == "multi" else "single"
    for f in sorted(glob.glob(f"{rd}*.jsonl")):
        parse([f], run, main_role, sub=False)
        sid = os.path.splitext(os.path.basename(f))[0]
        for sf in sorted(glob.glob(f"{rd}{sid}/subagents/*.jsonl")):
            meta = sf[:-6] + ".meta.json"; r0 = "subagent:unknown"
            if os.path.exists(meta):
                try: r0 = json.load(open(meta)).get("agentType") or r0
                except ValueError: pass
            parse([sf], run, r0, sub=True)

cols = ["run_id", "arm", "role", "phase", "model", "api_msgs", "tool_calls", "prompts", "compactions", "input", "cache_write",
        "cache_write_1h", "cache_read", "output", "cost_usd", "active_h", "first_utc", "last_utc"]
rows = []
for k, u in sorted(U.items(), key=lambda x: tuple(map(str, x[0]))):
    run, arm, role, ph, model = k
    rows.append(dict(run_id=run, arm=arm, role=role, phase=ph, model=model, api_msgs=u["api_msgs"], tool_calls=u["tool_calls"],
                     prompts=u["prompts"], compactions=u["compactions"], input=u["input"], cache_write=u["cache_create"],
                     cache_write_1h=u["cw1h"], cache_read=u["cache_read"], output=u["output"],
                     cost_usd=round(cost(model, u), 4) if model != "human" else 0.0, active_h=round(u["active_s"]/3600, 3),
                     first_utc=u["first"].isoformat() if u["first"] else "", last_utc=u["last"].isoformat() if u["last"] else ""))
with open(f"{M}/usage_p2.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, cols); w.writeheader(); w.writerows(rows)

def table(keyf, title):
    agg = defaultdict(lambda: defaultdict(float))
    for r in rows:
        a = agg[keyf(r)]
        for c in ("api_msgs", "prompts", "input", "cache_write", "cache_read", "output", "cost_usd", "active_h"): a[c] += r[c]
    out = [f"### {title}", "", "| key | API msgs | human msgs | input | cache write | cache read | output | cost-eq. USD | active h |", "|---|" + "---|"*8]
    for k in sorted(agg):
        a = agg[k]; out.append(f"| {' / '.join(k)} | {int(a['api_msgs'])} | {int(a['prompts'])} | {int(a['input']):,} | {int(a['cache_write']):,} | "
                               f"{int(a['cache_read']):,} | {int(a['output']):,} | {a['cost_usd']:.2f} | {a['active_h']:.2f} |")
    return out
md = ["# p2 usage (generated by p2/metrics/parse_usage.py)", f"generated {NOW:%Y-%m-%dT%H:%MZ}; prices: metrics/prices.json", ""]
md += table(lambda r: (r["run_id"], r["role"], r["model"]), "By run / role / model") + [""]
md += table(lambda r: (r["run_id"], r["role"], r["phase"]), "By run / role / phase") + [""]
md += table(lambda r: (r["arm"], r["model"]), "By arm / model")
open(f"{M}/usage_p2.md", "w").write("\n".join(md) + "\n")
print("\n".join(md))
