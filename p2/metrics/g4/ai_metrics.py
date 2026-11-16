#!/usr/bin/env python3
"""G4(b) metrics for AI_results.md (multi_r1 orchestrator, 2026-11-15).
Input: metrics/usage_events_p2.csv (parse_usage.py --events), metrics/ledger.csv. Output: metrics/g4/ai_metrics.json.
Windows (pre-declared here, applied identically to every run):
  * P01-03: from the run's first transcript event to its G1 gate (ledger 'gate' event, phase G1, first one).
  * E2E (single_r1, multi_r1 WH): from first event to the FINAL gate (single_r1 2026-11-14T10:56:18Z;
    multi_r1 first final 2026-11-13T18:25:20Z, plus the final round FINAL-R2 up to the cut time, reported separately).
Exclusions (human-error cost, metrics/human_error_cost.md): single_r1 duplicate sessions e11a5b3e*, ffcf95fa*;
  multi_r1 events 2026-11-08T20:14:43Z-20:29:58Z (misdirected multi_r2 prompt). G4 audit work (role reviewer phase G4a,
  orchestrator after G4 start) is excluded from run totals and reported as evaluation cost.
Role scopes for multi_r1 WH comparisons: executor-hh excluded (HH stream, A1); executor-zh-erratum reported separately
  (VH combination work, no single-arm counterpart); orchestrator/verifier/reviewer included in full (shared WH+HH before A1:
  stated as an upper bound on WH cost).
Active time: union over all roles of inter-message gaps < 10 min. Wall time: window length.
"""
import csv, json, os, datetime as dt
from collections import defaultdict
M = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = lambda s: dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
EV = list(csv.DictReader(open(f"{M}/usage_events_p2.csv")))
LED = list(csv.DictReader(open(f"{M}/ledger.csv")))
EXCL_FILES = ("single_r1/e11a5b3e", "single_r1/ffcf95fa")
EXCL_WIN = [("multi_r1", T("2026-11-08T20:14:43Z"), T("2026-11-08T20:29:58Z"))]
G4_START = min(T(r["utc"]) for r in LED if r["phase"] == "G4" and r["event"] == "start" and r["run_id"] == "multi_r1")
def g1(run):
    return min(T(r["utc"]) for r in LED if r["run_id"] == run and r["phase"] == "G1" and r["event"] == "gate")
FINAL = {"single_r1": T("2026-11-14T10:56:18Z"), "multi_r1": T("2026-11-13T18:25:20Z")}
def excluded(e):
    t = T(e["utc"])
    if e["file"].startswith(EXCL_FILES): return "human_error"
    if any(e["run_id"] == r and a <= t <= b for r, a, b in EXCL_WIN): return "human_error"
    if e["run_id"] == "multi_r1" and (e["phase"] == "G4a" or (e["role"] == "orchestrator" and t >= G4_START)): return "g4_eval"
    return None
def agg(evs):
    a = defaultdict(float); ts = sorted(T(e["utc"]) for e in evs if e["kind"] == "api")
    for e in evs:
        if e["kind"] == "human": a["human_msgs"] += 1; continue
        a["api_msgs"] += 1; a["cost_usd"] += float(e["cost_usd"])
        for k in ("input", "output", "cache_create", "cache_read"): a[k] += int(e[k])
        a[f"cost_{e['model']}"] += float(e["cost_usd"]); a[f"out_{e['model']}"] += int(e["output"])
    a["active_h"] = sum((b - x).total_seconds() for x, b in zip(ts, ts[1:]) if (b - x).total_seconds() < 600) / 3600
    a["tokens_total"] = a["input"] + a["output"] + a["cache_create"] + a["cache_read"]
    return {k: round(v, 4) for k, v in a.items()}
out = {"windows": {}, "runs": {}, "excluded": {}}
runs = sorted({e["run_id"] for e in EV})
for run in runs:
    evs = [e for e in EV if e["run_id"] == run]
    keep = [e for e in evs if not excluded(e)]
    t0 = min(T(e["utc"]) for e in keep); tg1 = g1(run)
    p13 = [e for e in keep if T(e["utc"]) <= tg1]
    if run == "multi_r1": p13_wh = [e for e in p13 if e["role"] != "executor-hh"]
    else: p13_wh = p13
    r = {"start": t0.isoformat(), "G1": tg1.isoformat(), "wall_h_P01_03": round((tg1 - t0).total_seconds() / 3600, 2),
         "P01_03_all_roles": agg(p13), "P01_03_WH": agg(p13_wh)}
    if run in FINAL:
        tf = FINAL[run]; e2e = [e for e in keep if T(e["utc"]) <= tf]
        if run == "multi_r1":
            r["E2E_WH_excl_hh_zh"] = agg([e for e in e2e if e["role"] not in ("executor-hh", "executor-zh-erratum")])
            r["E2E_zh_erratum"] = agg([e for e in e2e if e["role"] == "executor-zh-erratum"])
            r["E2E_hh"] = agg([e for e in e2e if e["role"] == "executor-hh"])
            r["FINAL_R2_round"] = agg([e for e in keep if T(e["utc"]) > tf])
        else:
            r["E2E"] = agg(e2e)
        r["wall_h_E2E"] = round((tf - t0).total_seconds() / 3600, 2)
    r["by_role_P01_03"] = {ro: agg([e for e in p13 if e["role"] == ro]) for ro in sorted({e["role"] for e in p13})}
    out["runs"][run] = r
    for why in ("human_error", "g4_eval"):
        x = [e for e in evs if excluded(e) == why]
        if x: out["excluded"][f"{run}:{why}"] = agg(x)
out["windows"] = {"G4_start": G4_START.isoformat(), "final": {k: v.isoformat() for k, v in FINAL.items()}}
json.dump(out, open(f"{M}/g4/ai_metrics.json", "w"), indent=1)
for run, r in out["runs"].items():
    p = r["P01_03_WH"]; print(f"{run:10s} P01-03 WH: cost ${p['cost_usd']:.2f} tokens {p['tokens_total']/1e6:.1f}M out {p['output']/1e3:.0f}k "
                              f"active {p['active_h']:.2f} h wall {r['wall_h_P01_03']} h human {p.get('human_msgs',0):.0f}")
for k, v in out["excluded"].items(): print("excluded", k, f"${v['cost_usd']:.2f}", v.get("human_msgs", 0))
for run in FINAL:
    r = out["runs"][run]; k = "E2E" if run == "single_r1" else "E2E_WH_excl_hh_zh"
    print(run, k, f"${r[k]['cost_usd']:.2f} active {r[k]['active_h']:.2f} h wall {r['wall_h_E2E']} h human {r[k].get('human_msgs',0):.0f}")
