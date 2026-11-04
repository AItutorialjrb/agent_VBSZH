#!/usr/bin/env python3
"""Generates ONE production submit file per sample (work/condor/prod/prod_<sample>.sub) from work/plan.json. NOT submitted before G2 (no bulk production before G2).
Output stage-out: p2/production/wh/<sample>/ (canonical, shared). Slim Delphes only (keep_lhe=0, keep_full=0). Seeds: scripts/seeds.py J=200.. (asserted unique incl. preG1).
Usage: python3 scripts/make_prod_sub.py   -> prints the submission plan (cluster per sample, jobs, flavour). Submission after G2: `condor_q` duplicate check, then `condor_submit work/condor/prod/prod_<s>.sub` (EosSubmit schedd)."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import seeds as S, make_condor_g2 as G
WH, E, LIB = S.WH, G.E, G.LIB; PR = "/eos/user/r/rjiang/vbs_zh_codex_starter/p2/production/wh"
OLDGP = {"S_EW_WHjj": 2111000, "H_QCD_WH_mlm": 2113000, "H_ttH_1l": 2116000, "B_EW_Waajj_vbs": 2123000, "B_QCD_Waajj_vbs": 2124000, "B_QCD_Waajj_nomjj": 2125000, "F_EW_Wajj_vbs": 2126000, "F_QCD_Wajj_vbs": 2127000, "F_QCD_Wajj_nomjj": 2128000}
CM = dict((s, v[0]) for s, v in G.TEST.items()); CM.update({"S_EW_WHjj": "py8_whjj_haa.cmnd", "H_QCD_WH_mlm": "py8_mlm_wh_haa.cmnd", "H_ttH_1l": "py8_h_haa.cmnd", "B_EW_Waajj_vbs": "py8_generic_dipole.cmnd", "B_QCD_Waajj_vbs": "py8_generic.cmnd", "B_QCD_Waajj_nomjj": "py8_generic.cmnd", "F_QCD_Wajj_nomjj": "py8_generic.cmnd"})
def gp(s): return f"{E}/work/gridpacks/{s}_gridpack_s{OLDGP[s]}.tar.gz" if s in OLDGP else G.gpfile(s)
plan = json.load(open(f"{WH}/work/plan.json")); os.makedirs(f"{WH}/work/condor/prod", exist_ok=True); allseeds = []
hdr = open(f"{WH}/work/condor/g2_tests.sub").read().split("queue sample")[0]
for s, p in plan.items():
    if not p.get("jobs") or p["jobs"] == "PENDING": print(f"{s:20s} PENDING (sigma / N not yet known)"); continue
    nj, evpj = [int(x) for x in p["jobs"].split(" x ")]; rows = ""
    for j in range(nj):
        sd = S.seed(s, 200+j); allseeds.append(sd); rows += f"  {s} {gp(s)} {CM[s]} {evpj} 0 0 {p['flav']} {sd} prod\n"
    t = hdr.replace("$(odir)/$(sample)", "").replace(f"{E}/work/", "") if False else hdr
    t = t.replace(f"{E}/work/$(odir)/$(sample)", f"{PR}/$(sample)").replace(f"{E}/work/condor/$(odir)_$(sample)_$(seed).out", f"{E}/work/condor/prod/$(sample)_$(seed).out").replace(f"{E}/work/condor/$(odir)_$(sample)_$(seed).err", f"{E}/work/condor/prod/$(sample)_$(seed).err").replace("g2_tests.log", f"prod/prod_{s}.log")
    open(f"{WH}/work/condor/prod/prod_{s}.sub", "w").write(t + "queue sample, gp, cmnd, nev, klhe, kfull, flav, seed, odir from (\n" + rows + ")\n")
    print(f"{s:20s} cluster-per-sample  {nj} jobs x {evpj} ev  flavour {p['flav']}  seeds {S.seed(s,200)}..{S.seed(s,200+nj-1)}")
S.check(allseeds); print(len(allseeds), "production seeds unique (incl. preG1 check)")
