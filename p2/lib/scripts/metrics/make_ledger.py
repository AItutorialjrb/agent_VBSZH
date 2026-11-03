#!/usr/bin/env python3
"""C (2026-11-03): metrics/ledger.csv for process ZH, RECONSTRUCTED RETROSPECTIVELY on 2026-11-03 from the read-only
transcript backups (metrics/raw/), metrics/phases.csv and metrics/prompts/ZH/index.csv. Every row carries
note prefix 'retro:'. Columns: utc, process, arm, role, phase, event, session_id, note
event in {start, end, human_intervention, compaction, interrupt}. Usage: python3 -P scripts/metrics/make_ledger.py"""
import csv, json, glob, os
P = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ph = list(csv.DictReader(open(f"{P}/metrics/phases.csv")))
def phase_of(ts):
    for r in ph:
        if r["start_utc"] <= ts and (not r["end_utc"] or ts < r["end_utc"]): return r["phase"]
    return "?"
CL = "c6cda945-009c-4d75-b4e6-15b1e7b55c21"; CX = {"P00": "01a19c30-c21b-74a0-b6c3-c5ed08265005", "P01": "01a19c37-8e3c-7fe0-a736-6961c9441aa5"}
R = []
for r in ph:
    sid = CX.get(r["phase"], CL); role = r["agent"]
    R.append((r["start_utc"], "ZH", "single-agent", role, r["phase"], "start", sid, f"retro: {r['label']}"))
    if r["end_utc"]: R.append((r["end_utc"], "ZH", "single-agent", role, r["phase"], "end", sid, "retro: next phase prompt (phase boundary = human prompt time)"))
for r in csv.DictReader(open(f"{P}/metrics/prompts/ZH/index.csv")):
    ts = r["utc"][:19] + "Z"; sid = r["session"].split("-", 5)[-1].replace(".jsonl", "") if r["agent"] == "codex" else r["session"]
    if "corrective-intervention" in r["labels"]: ev = "human_intervention"
    elif r["labels"] in ("interrupt",): ev = "interrupt"
    else: continue
    R.append((ts, "ZH", "single-agent", "human", phase_of(ts), ev, sid, f"retro: [{r['corrective_classes']}] {r['note']}"))
for f in glob.glob(f"{P}/metrics/raw/claude/*.jsonl"):
    for l in open(f):
        d = json.loads(l)
        if d.get("type") == "system" and d.get("subtype") == "compact_boundary":
            m = d.get("compactMetadata", {}); ts = d["timestamp"][:19] + "Z"
            R.append((ts, "ZH", "single-agent", "claude", phase_of(ts), "compaction", d["sessionId"], f"retro: {m.get('trigger')} compaction, preTokens={m.get('preTokens')} postTokens={m.get('postTokens')}"))
        if d.get("type") == "system" and d.get("subtype") == "informational" and "Usage limit" in str(d.get("content")):
            ts = d["timestamp"][:19] + "Z"
            R.append((ts, "ZH", "single-agent", "system", phase_of(ts), "interrupt", d["sessionId"], f"retro: {d['content']}"))
R.sort()
with open(f"{P}/metrics/ledger.csv", "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["utc", "process", "arm", "role", "phase", "event", "session_id", "note"]); w.writerows(R)
print(len(R), "rows -> metrics/ledger.csv")
