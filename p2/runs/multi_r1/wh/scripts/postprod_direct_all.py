#!/usr/bin/env python3
"""Direct (unweighted) counts of events with the real fake-origin photon in the pilot regions PRE / VBS / PEAK on ALL delivered files of the one-fake rows (04 sec. 20):
F_QCD_Wajjj_nomjj, F_EW_Wajj_nomjj, T_tta_1l, T_tWa_1l (one prompt photon in the ME + one Delphes photon of non-prompt origin, definition of postprod_direct.py nfake = 1). Yield = sigma*k*L*count/N_generated (events at 500 fb^-1).
Usage: bash scripts/envrun.sh python3 -P scripts/postprod_direct_all.py"""
import sys, os, json, glob
os.environ["DSAMPLE"] = "F_QCD_Wajjj_nomjj"; os.environ["NFAKE"] = "1"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import postprod_direct as D
from multiprocessing import Pool
WH = D.WH; PR = D.PR; ROWS = ["F_QCD_Wajjj_nomjj", "F_EW_Wajj_nomjj", "T_tta_1l", "T_tWa_1l"]
def work(f):
    r = D.dirc(f); r["sample"] = f.split("/")[-2]; return r
if __name__ == "__main__":
    fs = [f for s in ROWS for f in sorted(glob.glob(f"{PR}/{s}/*.root")) if not f.endswith("_gen.root")]
    with Pool(8) as p: R = p.map(work, fs, chunksize=2)
    out = {}
    for s in ROWS:
        sel = [r for r in R if r["sample"] == s]; N = sum(r["N"] for r in sel); sig = json.load(open(f"{WH}/work/ff_{s}.json"))["sigma_fb"]
        out[s] = dict(n_files=len(sel), N=N, sigma_k_fb=sig, **{reg: dict(count=sum(r[reg] for r in sel), yield_500=sig*500*sum(r[reg] for r in sel)/N, err=sig*500*max(sum(r[reg] for r in sel), 1)**0.5/N) for reg in ("PRE", "VBS", "PEAK")})
    json.dump(out, open(f"{WH}/work/postprod/direct_all.json", "w"), indent=1)
    for s, v in out.items(): print(s, v["n_files"], v["N"], {reg: (v[reg]["count"], round(v[reg]["yield_500"], 4), round(v[reg]["err"], 4)) for reg in ("PRE", "VBS", "PEAK")})
