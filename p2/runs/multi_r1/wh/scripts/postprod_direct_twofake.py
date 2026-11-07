#!/usr/bin/env python3
"""Direct counts of events with TWO non-prompt-origin photons in the regions PRE/VBS/PEAK on the two-fake rows (F_Wjjjj and T_ttjj_1l: all delivered files): Poisson counts, Garwood 68/95 % intervals and the 95 % CL upper limit on the yield (events at 500 fb^-1 scaled to the sub-sample).
Usage: bash scripts/envrun.sh python3 -P scripts/postprod_direct_twofake.py"""
import os, sys, json, glob
os.environ["DSAMPLE"] = "F_Wjjjj"; os.environ["NFAKE"] = "2"; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import postprod_direct as D
from multiprocessing import Pool
from scipy.stats import chi2
def garwood(k, cl): a = 1-cl; return (0.0 if k == 0 else chi2.ppf(a/2, 2*k)/2, chi2.ppf(1-a/2, 2*(k+1))/2)
if __name__ == "__main__":
    WH, PR = D.WH, D.PR; out = {}
    for s, k in (("F_Wjjjj", 1), ("T_ttjj_1l", 1)):
        fs = [f for f in sorted(glob.glob(f"{PR}/{s}/*.root")) if not f.endswith("_gen.root")][::k]
        sig = json.load(open(f"{WH}/work/ff_{s}.json"))["sigma_fb"]
        with Pool(8) as p: R = p.map(D.dirc, fs)
        N = sum(r["N"] for r in R); out[s] = dict(n_files=len(fs), N=N, sigma_k_fb=sig)
        for reg in ("PRE", "VBS", "PEAK"):
            c = sum(r[reg] for r in R); w = sig*500/N
            out[s][reg] = dict(count=c, yield_500=w*c, weight_per_raw_event=w, interval68=[w*x for x in garwood(c, 0.6827)], interval95=[w*x for x in garwood(c, 0.95)], UL95_yield=w*garwood(c, 0.90)[1])   # one-sided 95 % = upper edge of the 90 % central Garwood interval
        print(s, N, {reg: (out[s][reg]["count"], round(out[s][reg]["UL95_yield"], 2)) for reg in ("PRE", "VBS", "PEAK")}, flush=True)
    json.dump(out, open(f"{WH}/work/postprod/direct_twofake.json", "w"), indent=1)
