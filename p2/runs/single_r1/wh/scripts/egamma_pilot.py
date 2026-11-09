#!/usr/bin/env python3
"""single_r1 WH Phase 02/03: e->gamma pilot bound on one frozen ZH Z(ll)gamma jj file (read-only) and the WH tt~gamma test job.
one frozen file (2000 ev) is used as an unbiased subsample: its events are normalised to the full-sample sigma (frozen gridpack status).
Output: wh/work/p03/egamma_pilot.json.   Usage: python3 -P wh/scripts/egamma_pilot.py"""
import os, sys, glob, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import validate_delphes as V
WH = V.WH; Z = "/eos/home-r/rjiang/vbs_zh_codex_starter/production/final"
out = {}
for s, sig in (("F_QCD_llajj_vbs", 69.46), ("F_EW_llajj_vbs", 11.05)):
    f = sorted(f for f in glob.glob(f"{Z}/{s}/*.root") if not f.endswith(("_gen.root", "_full.root")))[0]
    ev = V.load(f)
    out[s] = {sc: V.cutflow(ev, sig, fake="e", scen=sc) for sc in V.FE}; out[s]["file"] = f; out[s]["sigma_fb_sample"] = sig
    out[s]["genuine"] = V.cutflow(ev, sig)
    print(s, {sc: (out[s][sc][-2]["sigma_fb"], out[s][sc][-2]["n_mc"]) for sc in V.FE})
f = [x for x in glob.glob(f"{WH}/work/test/T_tta_1l/*.root") if not x.endswith(("_gen.root", "_full.root"))][0]
ev = V.load(f); sig = V.XS["T_tta_1l"]["sigma_fb"]
out["T_tta_1l"] = {sc: V.cutflow(ev, sig, fake="e", scen=sc) for sc in V.FE}
print("T_tta_1l", {sc: (out["T_tta_1l"][sc][-2]["sigma_fb"], out["T_tta_1l"][sc][-2]["n_mc"]) for sc in V.FE})
json.dump(out, open(f"{WH}/work/p03/egamma_pilot.json", "w"), indent=1)
