#!/usr/bin/env python3
"""Summarise condor test jobs (work/test/<sample>/*.json): event counts, sigma(LHE init) vs gridpack sigma, PY8 sigma, sizes, times. Writes work/test_summary.md.
NOTE: the independent job/log audit is done by the verifier; this is the executor's own tabulation."""
import glob, json, os, re, subprocess, sys
WH = "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh"
out = ["| sample | seed | n_req / LHE / Delphes entries (MLM: accepted) | σ_LHE init [fb] | σ_gridpack [fb] | σ_PY8 [fb] | LHE vs PY8 | wall gridpack/PY8+Delphes/slim [s] | slim ROOT+gen [kB/ev] | worker |", "|---|---|---|---|---|---|---|---|---|---|"]
EOS = "root://eosuser.cern.ch"; EP = WH.replace("/eos/home-r/", "/eos/user/r/")
def xls(path): return subprocess.run(["xrdfs", EOS, "ls", path], capture_output=True, text=True).stdout.split()
def xsize(path):
    o = subprocess.run(["xrdfs", EOS, "stat", path], capture_output=True, text=True).stdout
    return int(re.search(r"Size:\s+(\d+)", o).group(1))
jl = [f for d in xls(f"{EP}/work/test") for f in xls(d) if f.endswith(".json")]   # xrootd listing: robust against FUSE dentry-cache lag
for jx in sorted(jl):
    os.makedirs(f"{WH}/work/xrd", exist_ok=True); j = f"{WH}/work/xrd/{os.path.basename(jx)}"
    subprocess.run(["xrdcp", "-s", "-f", EOS + "/" + jx, j], check=True)
    d = json.load(open(j)); s = d["sample"]; tag = os.path.basename(j)[:-5]; dd = os.path.dirname(jx)
    x = d["lhe_init_xsec_pb_err_pb_max_lprup"].split(); xs, xe = float(x[0])*1e3, float(x[1])*1e3     # first process line only (multi-process cards have several)
    m = re.search(r"\|\s+sum\s+\|\s+(\d+)\s+(\d+)\s+(\d+)\s+\|\s+(\S+)\s+(\S+)\s+\|", d["pythia_sum_line"]); py = float(m.group(4))*1e12 if m else None   # mb -> fb (1 mb = 1e12 fb)
    gps = f"{WH}/work/gridpacks/{s}_status.txt"; g = re.search(r"Cross-section :\s+(\S+) \+- (\S+) pb", open(gps).read()) if os.path.exists(gps) else None
    gv = f"{float(g.group(1))*1e3:.4g} ± {float(g.group(2))*1e3:.2g}" if g else "n/a"
    sz = (xsize(f"{dd}/{tag}.root") + xsize(f"{dd}/{tag}_gen.root"))/d["n_delphes"]/1e3
    out.append(f"| {s} | {d['mg_seed']} | {d['n_requested']} / {d['n_lhe']} / {d['n_delphes']} | {xs:.4g} ± {xe:.2g} (1st proc.) | {gv} | {('%.4g'%py) if py else 'n/a'} | {('%+.1f %%'%(100*(py/ (float(g.group(1))*1e3)-1))) if (py and g) else ''} | {d['t_gridpack_s']}/{d['t_py8_delphes_s']}/{d['t_slim_s']} | {sz:.2f} | {d['host'].split('.')[0]} |")
open(f"{WH}/work/test_summary.md", "w").write("\n".join(out)+"\n"); print("\n".join(out))
