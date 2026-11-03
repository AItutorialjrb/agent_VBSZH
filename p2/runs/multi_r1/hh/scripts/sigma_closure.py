#!/usr/bin/env python3
"""sigma closure gridpack(MG5 integration) vs LHE init xsecup vs Pythia8 sigmaGen, plus event-count closure, from the Phase-03 test-job JSONs. Usage: sigma_closure.py"""
import json, glob, os, re, yaml
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M = {s["name"]: s for s in yaml.safe_load(open(f"{H}/config/sample_matrix.yaml"))["samples"]}
print("| sample | test seed | N_req | N_LHE | N_Delphes | σ gridpack [pb] | σ LHE-init [pb] | σ PY8 [pb] | LHE/gridpack | PY8/LHE |"); print("|---|---|---|---|---|---|---|---|---|---|")
for f in sorted(glob.glob(f"{H}/work/test/*/*.json")):
    j = json.load(open(f)); s = j["sample"]; sg = M[s]["sigma_pb"]
    lhe = float(j["lhe_init_xsec_pb_err_pb_max_lprup"].split()[0]); py = float(re.findall(r"\|\s+([0-9.eE+-]+)\s+([0-9.eE+-]+)\s*\|\s*$", j["pythia_sum_line"])[0][0]) * 1e9
    print(f"| {s} | {j['mg_seed']} | {j['n_requested']} | {j['n_lhe']} | {j['n_delphes']} | {sg:.5g} | {lhe:.5g} | {py:.5g} | {lhe/sg:.3f} | {py/lhe:.3f} |")
