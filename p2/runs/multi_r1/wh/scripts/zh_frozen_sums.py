#!/usr/bin/env python3
"""READ-ONLY pass over the frozen ZH production files used as rows of SAMPLES.csv: per directory N_generated (json n_lhe), N_Delphes (tree entries), signed sum of Event.Weight[0] [pb], number of negative-weight events, mean |Event.Weight|. No file is modified or copied.
Usage: bash scripts/envrun.sh python3 -P scripts/zh_frozen_sums.py"""
import glob, json, os, numpy as np, uproot
from multiprocessing import Pool
Z = "/eos/home-r/rjiang/vbs_zh_codex_starter/production"
DIRS = ["v1/ew_zhjj_zll", "v1/qcd_zhjj_zll", "final/B_QCD_zaajj_nomjj", "final/B_QCD_zaajj_vbs", "final/B_EW_zaajj_vbs_is1h", "final/B_EW_zaajj_vbs_is2", "final/B_EW_zaajj_vbs_is3", "final/F_QCD_llajj_vbs", "final/F_EW_llajj_vbs", "final/F_QCD_llajj_nomjj"]
def work(f):
    w = np.array([x[0] for x in uproot.open(f)["Delphes"]["Event/Event.Weight"].array(library="np")]); js = f[:-5] + ".json"
    nl = json.load(open(js))["n_lhe"] if os.path.exists(js) else len(w)
    return f, float(w.sum()), int((w < 0).sum()), len(w), float(np.abs(w).sum()), nl
if __name__ == "__main__":
    fs = [f for d in DIRS for f in sorted(glob.glob(f"{Z}/{d}/*.root")) if not f.endswith(("_gen.root", "_full.root"))]
    with Pool(8) as p: R = p.map(work, fs, chunksize=8)
    out = {}
    for f, s, n, N, a, nl in R:
        d = os.path.relpath(os.path.dirname(f), Z); o = out.setdefault(d, dict(files=0, sumw_pb=0.0, n_neg=0, N_delphes=0, sum_abs_w=0.0, N_generated=0)); o["files"] += 1; o["sumw_pb"] += s; o["n_neg"] += n; o["N_delphes"] += N; o["sum_abs_w"] += a; o["N_generated"] += nl
    for d, o in out.items(): o["mean_abs_w_pb"] = o["sum_abs_w"]/o["N_delphes"]
    json.dump(out, open("/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh/work/zh_frozen_sums.json", "w"), indent=1)
    for d, o in out.items(): print(d, o["files"], o["N_generated"], o["N_delphes"], round(o["sumw_pb"], 4), o["n_neg"], round(o["mean_abs_w_pb"], 6))
