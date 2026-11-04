#!/usr/bin/env python3
"""Production/pilot job bookkeeping and closure: for every sample directory in <prod_root>: number of complete jobs (root+gen+json), N_LHE, N_Delphes, mean PY8 sigma_gen over jobs (and spread) vs the MG5 gridpack sigma
(config/sample_matrix.yaml), CPU time per event, slim-ROOT bytes per event.  MLM samples: PY8 sigma is the matched sigma (= MG5 sigma x accepted fraction), compared to that.
Usage: pilot_check.py <matrix.yaml> <prod_root> <out.json>"""
import sys, json, glob, os, re, yaml, numpy as np
my, root, outj = sys.argv[1:4]; M = {s["name"]: s for s in yaml.safe_load(open(my))["samples"]}; res = {}
for d in sorted(glob.glob(f"{root}/*/")):
    n = os.path.basename(d.rstrip("/"))
    if n == "gridpacks" or n not in M: continue
    js = sorted(glob.glob(f"{d}/{n}_s[0-9]*.json"))
    if not js: continue
    rows = []
    for f in js:
        j = json.load(open(f)); ok = os.path.exists(f[:-5] + ".root") and os.path.exists(f[:-5] + "_gen.root")
        if not ok: continue
        py = float(re.findall(r"\|\s+([0-9.eE+-]+)\s+([0-9.eE+-]+)\s*\|\s*$", j["pythia_sum_line"])[0][0]) * 1e9
        rows.append(dict(seed=j["mg_seed"], n_lhe=j["n_lhe"], n_del=j["n_delphes"], py_pb=py, t=j["t_gridpack_s"] + j["t_py8_delphes_s"] + j["t_slim_s"], bytes=os.path.getsize(f[:-5] + ".root") + os.path.getsize(f[:-5] + "_gen.root")))
    N = sum(r["n_lhe"] for r in rows); ND = sum(r["n_del"] for r in rows); py = np.array([r["py_pb"] for r in rows]); w = np.array([r["n_lhe"] for r in rows], float)
    pym = float((py * w).sum() / w.sum()); pys = float(py.std(ddof=1) / np.sqrt(len(py))) if len(py) > 1 else None
    sg = M[n].get("sigma_pb"); mlm = n.startswith("T_ttbar_mlm")
    ref = sg * (ND / N if mlm else 1.0) if sg else None
    res[n] = dict(jobs=len(rows), N_lhe=N, N_delphes=ND, py8_sigma_pb=pym, py8_sigma_err_pb=pys, gridpack_sigma_pb=sg, ref_sigma_pb=ref, ratio=(pym / ref if ref else None), wall_s_per_lhe_event=float(sum(r["t"] for r in rows) / N),
                  bytes_per_delphes_event=float(sum(r["bytes"] for r in rows) / max(ND, 1)), bytes_per_lhe_event=float(sum(r["bytes"] for r in rows) / N), seeds=[r["seed"] for r in rows], match_eff=ND / N)
json.dump(res, open(outj, "w"), indent=1)
print("| sample | jobs | N_LHE | N_Delphes | σ_PY8 [pb] | σ_ref [pb] | PY8/ref | s/event | kB/event |\n|---|---|---|---|---|---|---|---|---|")
for n, r in res.items(): print(f"| {n} | {r['jobs']} | {r['N_lhe']} | {r['N_delphes']} | {r['py8_sigma_pb']:.5g} | {r['ref_sigma_pb'] if r['ref_sigma_pb'] is None else format(r['ref_sigma_pb'],'.5g')} | {'' if r['ratio'] is None else format(r['ratio'],'.3f')} | {r['wall_s_per_lhe_event']:.3f} | {r['bytes_per_lhe_event']/1e3:.2f} |")
