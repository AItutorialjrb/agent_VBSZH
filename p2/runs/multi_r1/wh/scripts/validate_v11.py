#!/usr/bin/env python3
"""Validation of a v1.1 production row: files, N, sum of weights vs sigma, negative fraction, seeds, sha256. Usage: validate_v11.py <sample> <sigma_pb> <N_expected_per_job>. Writes work/v11_<sample>.json"""
import sys, glob, re, json, hashlib, numpy as np, uproot
s, sig, nj = sys.argv[1], float(sys.argv[2]), int(sys.argv[3]); PR = "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/production/wh"; WH = "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh"
fs = sorted(f for f in glob.glob(f"{PR}/{s}/{s}_s*.root") if not f.endswith("_gen.root")); N = 0; SW = 0.0; neg = 0; seeds = []; sha = {}; bad = []; mean_abs = []
for f in fs:
    seed = int(re.search(r"_s(\d+)\.root", f).group(1)); seeds.append(seed); t = uproot.open(f)["Delphes"]; n = t.num_entries; w = t["Event/Event.Weight"].array(library="np"); w0 = np.array([x[0] for x in w])
    g = uproot.open(f[:-5]+"_gen.root")["GenTruth"].num_entries
    if n != nj or g != n: bad.append((f, n, g))
    N += n; SW += float(w0.sum()); neg += int((w0 < 0).sum()); mean_abs.append(float(np.abs(w0).mean()))
    for ff in (f, f[:-5]+"_gen.root"): sha[ff.split("/")[-2]+"/"+ff.split("/")[-1]] = hashlib.sha256(open(ff, "rb").read()).hexdigest()
out = dict(sample=s, n_files=len(fs), N_total=N, sum_w_pb=SW, sigma_pb=sig, ratio_sumw_over_N_sigma=SW/(N*sig), negative_fraction=neg/N, seeds_min=min(seeds), seeds_max=max(seeds), seeds_unique=len(set(seeds)) == len(seeds), mean_abs_w_range=[min(mean_abs), max(mean_abs)], bad_files=bad)
json.dump(out, open(f"{WH}/work/v11_{s}.json", "w"), indent=1); json.dump(sha, open(f"{WH}/work/v11_{s}_sha256.json", "w"), indent=1); print(json.dumps(out))
