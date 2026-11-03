#!/usr/bin/env python3
"""Assemble config/sample_matrix.yaml = sample_matrix_gen.yaml + MG5 gridpack sigma (status files) + N_MC requirements + planned storage. Usage: make_matrix.py"""
import yaml, os, math, glob, re
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
m = yaml.safe_load(open(f"{H}/config/sample_matrix_gen.yaml"))
KB = dict(X=3.5, S=2.85, G=2.85, Q=5.2, T=4.0, H=3.5, V=3.2)    # kB/event of slim root, measured on test jobs (03 report) ; T,Q provisional
def sigma(s):
    for d in ("gridpacks_v2", "gridpacks"):
        f = f"{H}/work/{d}/{s['name']}_status.txt"
        if os.path.exists(f):
            t = open(f).read(); r = re.search(r"Cross-section :\s+(\S+) \+- (\S+) pb", t)
            if r: return float(r.group(1)), float(r.group(2)), f"MG5 LO gridpack integration ({d}/{s['name']}_status.txt)"
    return None, None, "not yet available (no gridpack in Phase 03)"
L = 3000.0
for s in m["samples"]:
    sg, se, src = sigma(s); s["sigma_pb"], s["sigma_err_pb"], s["sigma_source"] = sg, se, src
    if sg is not None:
        s["sigma_fb"] = sg * 1e3; s["sigma_x_BR_fb"] = sg * 1e3 * s["br_total"]; s["brute_force_N_for_3000fb"] = math.ceil(sg * 1e3 * s["br_total"] * L)
        if s["cls"] == "signal" or s["role"].split("(")[0] == "closure":
            s["N_MC_required"] = max(50000, s["brute_force_N_for_3000fb"]); s["N_MC_policy"] = "signal: N>=max(50k, sigma*BR*3000 fb^-1)"
        elif s["cls"] != "validation":
            s["N_MC_policy"] = "effective-N (SPEC 4.3): looser gen filter + twin; truth-tag weights; N_eff>=10 in SR or bound; brute force N shown for reference only"
    s["storage_kB_per_event"] = KB[s["name"][0]]
    if s.get("N_MC_required"): s["storage_GB_planned"] = round(s["N_MC_required"] * s["storage_kB_per_event"] / 1e6, 2)
yaml.safe_dump(m, open(f"{H}/config/sample_matrix.yaml", "w"), sort_keys=False, width=200)
tot = sum(s.get("storage_GB_planned", 0) for s in m["samples"]); print("signal+ planned storage GB:", round(tot, 2))
for s in m["samples"]:
    if s.get("sigma_fb") is not None: print(f"{s['name']:28s} sigma={s['sigma_fb']:.5g} fb  sigmaBR={s['sigma_x_BR_fb']:.5g} fb  brute N(3000)={s['brute_force_N_for_3000fb']:.3g} Nreq={s.get('N_MC_required','-')}")
