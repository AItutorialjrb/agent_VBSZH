#!/usr/bin/env python3
"""Direct counts (one prompt photon + one non-prompt-origin photon, regions PRE/VBS/PEAK of postprod_direct.py) in the 2-jet+PS sample (40 000-event twin + 2 000-event test of F_QCD_Wajj_nomjj; 2 ME jets, PS jets) vs the 3-jet ME sample F_QCD_Wajjj_nomjj (all delivered files, from work/postprod/direct_all.json):
yield = sigma*k*L*count/N (events at 500 fb^-1). Usage: bash scripts/envrun.sh python3 -P scripts/diag_2j_vs_3j.py"""
import os, sys, json, glob
os.environ["DSAMPLE"] = "F_QCD_Wajj_nomjj"; os.environ["NFAKE"] = "1"; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import postprod_direct as D
from multiprocessing import Pool
WH = D.WH
if __name__ == "__main__":
    fs = sorted(f for f in glob.glob(f"{WH}/work/twin/F_QCD_Wajj_nomjj/*.root") if not f.endswith(("_gen.root", "_full.root"))) + [f"{WH}/work/test/F_QCD_Wajj_nomjj/F_QCD_Wajj_nomjj_s2128001.root"]
    with Pool(6) as p: R = p.map(D.dirc, fs)
    N = sum(r["N"] for r in R); sig = D.SIG; out = {"files": len(fs), "N": N, "sigma_k_fb": sig}
    for reg in ("PRE", "VBS", "PEAK"):
        c = sum(r[reg] for r in R); out[reg] = dict(count=c, yield_500=sig*500*c/N, err=sig*500*max(c, 1)**0.5/N)
    d3 = json.load(open(f"{WH}/work/postprod/direct_all.json"))["F_QCD_Wajjj_nomjj"]; out["F_QCD_Wajjj_direct"] = {reg: d3[reg] for reg in ("PRE", "VBS", "PEAK")}
    json.dump(out, open(f"{WH}/work/postprod/direct_2j.json", "w"), indent=1)
    print("2j", N, {reg: (out[reg]["count"], round(out[reg]["yield_500"], 2), round(out[reg]["err"], 2)) for reg in ("PRE", "VBS", "PEAK")})
    print("3j", {reg: (d3[reg]["count"], round(d3[reg]["yield_500"], 2), round(d3[reg]["err"], 2)) for reg in ("PRE", "VBS", "PEAK")})
