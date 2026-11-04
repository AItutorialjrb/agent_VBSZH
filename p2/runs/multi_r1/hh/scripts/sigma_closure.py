#!/usr/bin/env python3
"""sigma closure gridpack(MG5 integration) vs LHE init xsecup vs Pythia8 sigmaGen, plus event-count closure, from the Phase-03 test-job JSONs. Usage: sigma_closure.py"""
import json, glob, os, re, yaml
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M = {s["name"]: s for s in yaml.safe_load(open(f"{H}/config/sample_matrix.yaml"))["samples"]}
print("| sample | test seed | N_req | N_LHE | N_Delphes | σ gridpack [pb] | σ LHE-init [pb] | σ PY8 [pb] | LHE/gridpack | PY8/LHE |"); print("|---|---|---|---|---|---|---|---|---|---|")
for f in sorted(glob.glob(f"{H}/work/test/*/*.json")):
    j = json.load(open(f)); s = j["sample"]; sg = M[s]["sigma_pb"]
    lhe = float(j["lhe_init_xsec_pb_err_pb_max_lprup"].split()[0]); lf = f[:-5] + ".lhe.gz"
    if os.path.exists(lf):       # multi-process cards ('add process'): the <init> block has one line per subprocess -> SUM the cross sections (first line alone is only one subprocess)
        import gzip
        L = []; ini = False
        for ln in gzip.open(lf, "rt"):
            if ln.startswith("<init>"): ini = True; nl = 0; continue
            if ini and ln.startswith("</init>"): break
            if ini:
                nl += 1
                if nl >= 2 and not ln.lstrip().startswith("<"): L.append(float(ln.split()[0]))
        lhe = sum(L)
    py = float(re.findall(r"\|\s+([0-9.eE+-]+)\s+([0-9.eE+-]+)\s*\|\s*$", j["pythia_sum_line"])[0][0]) * 1e9
    print(f"| {s} | {j['mg_seed']} | {j['n_requested']} | {j['n_lhe']} | {j['n_delphes']} | {sg:.5g} | {lhe:.5g} | {py:.5g} | {lhe/sg:.3f} | {py/lhe:.3f} |")
