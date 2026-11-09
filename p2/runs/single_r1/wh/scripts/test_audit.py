#!/usr/bin/env python3
"""single_r1 WH Phase 03: audit of the one-per-sample-type condor test jobs (read-only).
Per sample: exit code + host (condor user log), events requested/LHE/Delphes, sigma LHE (all <init> lines) vs PY8 vs gridpack,
seed uniqueness, output files present, sizes per event, step times. Output: markdown table on stdout + work/p03/test_audit.json.
Usage: python3 -P wh/scripts/test_audit.py"""
import os, re, sys, glob, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_cards as MC
WH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
X = json.load(open(f"{WH}/work/p03/xsec.json"))["xsec"]
# condor user logs: terminated events with return value, per job id
term = {}
for lg in glob.glob(f"{WH}/work/condor/test*.log"):
    txt = open(lg).read()
    for m in re.finditer(r"005 \((\d+)\.(\d+)\.\d+\) (\S+ \S+) Job terminated\.\n\s+\(1\) Normal termination \(return value (\d+)\)", txt):
        term.setdefault(f"{m.group(1)}.{m.group(2)}", []).append(int(m.group(4)))
rows, seeds = [], []
for s in MC.S:
    d = f"{WH}/work/test/{s['name']}"
    js = sorted(glob.glob(f"{d}/*.json"))
    if not js: continue
    J = json.load(open(js[0])); tag = os.path.basename(js[0])[:-5]
    files = {k: os.path.exists(f"{d}/{tag}{k}") for k in (".root", "_gen.root", "_logs.tgz", ".lhe.gz", "_full.root")}
    sz = os.path.getsize(f"{d}/{tag}.root") + os.path.getsize(f"{d}/{tag}_gen.root")
    t = X.get(s["name"], {}).get("test", {})
    seeds.append(J["mg_seed"])
    rows.append(dict(sample=s["name"], seed=J["mg_seed"], expected_seed=s["seed_gp"] + 1, n_req=J["n_requested"], n_lhe=J["n_lhe"],
                     n_delphes=J["n_delphes"], sig_gp=X[s["name"]].get("sigma_fb"), sig_lhe=t.get("lhe_sigma_fb"), sig_py8=t.get("py8_sigma_fb"),
                     kb_per_ev=sz / 1024 / J["n_delphes"], t_gp=J["t_gridpack_s"], t_py=J["t_py8_delphes_s"], host=J["host"], files=files))
assert len(seeds) == len(set(seeds)), "duplicate seeds among test jobs"
json.dump(dict(rows=rows, condor_return_values=term), open(f"{WH}/work/p03/test_audit.json", "w"), indent=1)
print("| sample | seed (=reg.+1) | N req/LHE/Delphes | σ gridpack [fb] | σ LHE [fb] | σ PY8 [fb] | PY8/LHE | slim kB/ev | t_LHE / t_PY8+Delphes [s] | outputs |")
print("|---|---|---|---|---|---|---|---|---|---|")
for r in rows:
    ok = "all" if all(v for k, v in r["files"].items() if k != "_full.root") else str(r["files"])
    print(f"| {r['sample']} | {r['seed']} ({'ok' if r['seed']==r['expected_seed'] else 'MISMATCH'}) | {r['n_req']}/{r['n_lhe']}/{r['n_delphes']} | {r['sig_gp']:.4g} | "
          f"{r['sig_lhe']:.4g} | {r['sig_py8']:.4g} | {r['sig_py8']/r['sig_lhe']:.4f} | {r['kb_per_ev']:.2f} | {r['t_gp']} / {r['t_py']} | {ok}{' +full' if r['files']['_full.root'] else ''} |")
bad = {k: v for k, v in term.items() if any(x != 0 for x in v)}
print(f"\ncondor test jobs terminated: {sum(len(v) for v in term.values())} terminations, non-zero return values (19 = waiting for gridpack, by design): "
      + json.dumps({k: v for k, v in bad.items()}))
