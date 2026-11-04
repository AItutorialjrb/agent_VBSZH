#!/usr/bin/env python3
"""MEASURED N/N_eff check (run after production; here run on the pilots to show the current, honest status).
For every plan row: N_gen = sum n_lhe of complete jobs; effective-N rows: sr_sumw/sr_sumw2 = sums of the nominal truth-tag weights of events in the HARD-window SR (measured, not projected);
twin_ok from work/g2/plan.json. Bound-only rows need their structured UL record (as in g2_plan). Prints violations (SystemExit) or PASSED. Usage: nmc_post_production.py"""
import json, os, sys, yaml, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hh_reco as R
from nmc_check_hh import nmc_check_hh
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); P = f"{H}/../../../production/hh"
plan = json.load(open(f"{H}/work/g2/plan.json"))["rows"]; M = {s["name"]: s for s in yaml.safe_load(open(f"{H}/config/sample_matrix.yaml"))["samples"]}
BRI = {k: v["value"] for k, v in yaml.safe_load(open(f"{H}/config/sample_matrix.yaml"))["br_inputs"].items()}
SC = yaml.safe_load(open(f"{H}/config/tagging_scenarios.yaml"))["tagging"]["nominal"]; reg = []
for n, r in plan.items():
    if r["rule"].startswith(("bound", "effective-N via bound")) or n in ("T_ttbar_boost", "Q_4b_ht", "Q_4j_vbs", "Q_bbjj_vbs"): continue
    d = R.load_named(n, P); full = r["rule"].startswith("full")
    e = dict(name=n, role=("basis" if M[n]["role"].startswith("basis") else "closure" if M[n]["role"].startswith("closure") else ("sig" if full else "bkg")), N_gen=d["n_gen"], sigma_fb=r["sigma_norm_fb"], br_total=r["br_total"], br_ledger=r["br_ledger"], strict=full)
    if not full:
        two, ld, v = R.stages(d); w = R.tag_weight(d, SC) * (v & R.window(d)); e.update(twin_ok=bool(r["twin"]["ok"]), sr_sumw=float(w.sum()), sr_sumw2=float((w * w).sum()))
    reg.append(e)
print("measured N_eff (hard-window SR, nominal tagging) per effective-N row:", {e["name"]: round(e["sr_sumw"] ** 2 / e["sr_sumw2"], 1) if e.get("sr_sumw2") else 0 for e in reg if "sr_sumw" in e})
nmc_check_hh(reg, br_inputs=BRI); print("measured check PASSED")
