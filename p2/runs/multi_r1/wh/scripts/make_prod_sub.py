#!/usr/bin/env python3
"""Generates ONE production submit file per sample (work/condor/prod/prod_<sample>.sub) from work/plan.json. NOT submitted before G2 (no bulk production before G2).
Output stage-out: p2/production/wh/<sample>/ (canonical, shared). Slim Delphes only (keep_lhe=0, keep_full=0). Seeds: scripts/seeds.py J=200.. (asserted unique incl. preG1).
Usage: python3 scripts/make_prod_sub.py   -> prints the submission plan (cluster per sample, jobs, flavour). Submission after G2: `condor_q` duplicate check, then `condor_submit work/condor/prod/prod_<s>.sub` (EosSubmit schedd)."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import seeds as S, make_condor_g2 as G
WH, E, LIB = S.WH, G.E, G.LIB; PR = "/eos/user/r/rjiang/vbs_zh_codex_starter/p2/production/wh"
OLDGP = {"S_EW_WHjj": 2111000, "H_QCD_WH_mlm": 2113000, "H_ttH_1l": 2116000, "B_EW_Waajj_vbs": 2123000, "B_QCD_Waajj_vbs": 2124000, "B_QCD_Waajj_nomjj": 2125000, "F_EW_Wajj_vbs": 2126000, "F_QCD_Wajj_vbs": 2127000, "F_QCD_Wajj_nomjj": 2128000}
CM = dict((s, v[0]) for s, v in G.TEST.items()); CM.update({"F_QCD_Wajjj_nomjj": "py8_generic.cmnd", "Q_aajjj": "py8_generic.cmnd", **{f"K_EW_WHjj_{n}": "py8_whjj_haa.cmnd" for n in ("lam_m100","lam_m050","lam_p000","lam_p050","lam_p100","lam_p150","kap_W15_Z075","kap_W05_Z15","cpo_p2","cpo_m2")}, "Q_aajj": "py8_generic.cmnd", "H_VBFH_jj": "py8_h_haa.cmnd", "H_ggF_jj": "py8_h_haa.cmnd", "S_EW_WHjj": "py8_whjj_haa.cmnd", "H_QCD_WH_mlm": "py8_mlm_wh_haa.cmnd", "H_ttH_1l": "py8_h_haa.cmnd", "B_EW_Waajj_vbs": "py8_generic_dipole.cmnd", "B_QCD_Waajj_vbs": "py8_generic.cmnd", "B_QCD_Waajj_nomjj": "py8_generic.cmnd", "F_QCD_Wajj_nomjj": "py8_generic.cmnd"})
def gp(s): return f"{E}/work/gridpacks/{s}_gridpack_s{OLDGP[s]}.tar.gz" if s in OLDGP else G.gpfile(s)
plan = json.load(open(f"{WH}/work/plan.json")); os.makedirs(f"{WH}/work/condor/prod", exist_ok=True); allseeds = []
hdr = open(f"{WH}/work/condor/g2_tests.sub").read().split("queue sample")[0]
for s, p in plan.items():
    if not p.get("jobs") or p["jobs"] == "PENDING": print(f"{s:20s} PENDING (sigma / N not yet known)"); continue
    nj, evpj = [int(x) for x in p["jobs"].split(" x ")]; rows = ""
    MARK = f"{WH}/work/condor/prod/.submitted_{s}"
    if os.path.exists(MARK):   # ALREADY SUBMITTED: never rewrite the submitted file; if the plan grew, write a TOP-UP file with fresh seeds (J from 300) for the missing events
        import re as _re
        old = open(f"{WH}/work/condor/prod/prod_{s}.sub").read(); done = sum(int(l.split()[3]) for l in old.split("\n") if l.startswith("  ") and "tar.gz" in l)
        rem = p["plan"]*(1.0/ (1.0)) - done if False else None
        import math as _m
        acc = 1.0; need_ev = p["nlhe"] - done if p.get("nlhe") else p["plan"] - done
        if need_ev <= 0: print(f"{s:20s} already submitted ({done} ev), plan satisfied"); continue
        if os.path.exists(f"{WH}/work/condor/prod/.submitted_{s}_topup"): print(f"{s:20s} top-up already submitted: file kept as submitted"); continue
        ntop = int(_m.ceil(need_ev/evpj)); assert 300+ntop <= 999, f"{s}: top-up needs {ntop} jobs (> 699 seeds)"
        rows = "".join(f"  {s} {gp(s)} {CM[s]} {evpj} 0 0 {p['flav']} {S.seed(s, 300+j)} prod\n" for j in range(ntop)); allseeds += [S.seed(s, 300+j) for j in range(ntop)]
        t = hdr.replace(f"{E}/work/$(odir)/$(sample)", f"{PR}/$(sample)").replace(f"{E}/work/condor/$(odir)_$(sample)_$(seed).out", f"{E}/work/condor/prod/$(sample)_$(seed).out").replace(f"{E}/work/condor/$(odir)_$(sample)_$(seed).err", f"{E}/work/condor/prod/$(sample)_$(seed).err").replace("g2_tests.log", f"prod/prod_{s}_topup.log")
        open(f"{WH}/work/condor/prod/prod_{s}_topup.sub", "w").write(t.replace("request_memory = 2500", "request_memory = 8000") + "queue sample, gp, cmnd, nev, klhe, kfull, flav, seed, odir from (\n" + rows + ")\n")
        print(f"{s:20s} TOP-UP (already submitted {done} ev): {ntop} jobs x {evpj} ev, seeds {S.seed(s,300)}..{S.seed(s,300+ntop-1)}"); continue
    for j in range(nj):
        sd = S.seed(s, 200+j); allseeds.append(sd); rows += f"  {s} {gp(s)} {CM[s]} {evpj} 0 0 {p['flav']} {sd} prod\n"
    t = hdr.replace("$(odir)/$(sample)", "").replace(f"{E}/work/", "") if False else hdr
    t = t.replace(f"{E}/work/$(odir)/$(sample)", f"{PR}/$(sample)").replace(f"{E}/work/condor/$(odir)_$(sample)_$(seed).out", f"{E}/work/condor/prod/$(sample)_$(seed).out").replace(f"{E}/work/condor/$(odir)_$(sample)_$(seed).err", f"{E}/work/condor/prod/$(sample)_$(seed).err").replace("g2_tests.log", f"prod/prod_{s}.log")
    t = t.replace("request_memory = 2500", "request_memory = 8000") if evpj >= 30000 else t   # jobs with >= 41 000 events/job exceeded the 3 GB cgroup limit (peak 3-6 GB, HOLD code 34, 2026-11-06)
    open(f"{WH}/work/condor/prod/prod_{s}.sub", "w").write(t + "queue sample, gp, cmnd, nev, klhe, kfull, flav, seed, odir from (\n" + rows + ")\n")
    print(f"{s:20s} cluster-per-sample  {nj} jobs x {evpj} ev  flavour {p['flav']}  seeds {S.seed(s,200)}..{S.seed(s,200+nj-1)}")
S.check(allseeds); print(len(allseeds), "production seeds unique (incl. preG1 check)")
