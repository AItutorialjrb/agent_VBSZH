#!/usr/bin/env python3
"""G2-FIX (review item 1): gridpacks + test jobs for the non-prompt-lepton class (Q_aajj, H_VBFH_jj, H_ggF_jj). Writes work/condor/g3_gridpacks.sub and g3_tests.sub (tests submitted AFTER the gridpacks exist).
Seeds via seeds.py (J=100 gridpack, 101 test) with check."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import seeds as S, make_condor_g2 as G
GP = {"Q_aajj": (4, 8000, "workday"), "H_VBFH_jj": (4, 8000, "workday"), "H_ggF_jj": (8, 16000, "tomorrow")}
TEST = {"Q_aajj": ("py8_generic.cmnd", 5000, "longlunch"), "H_VBFH_jj": ("py8_h_haa.cmnd", 5000, "longlunch"), "H_ggF_jj": ("py8_h_haa.cmnd", 5000, "longlunch")}
E = G.E; seeds = []
g = open(f"{S.WH}/work/condor/g2_gridpacks.sub").read().split("queue card")[0].replace("g2_gridpacks.log", "g3_gridpacks.log") + "queue card, gseed, ncore, mem, flav from (\n"
for s, (nc, mem, fl) in GP.items(): sd = S.seed(s, 100); seeds.append(sd); g += f"  {s} {sd} {nc} {mem} {fl}\n"
open(f"{S.WH}/work/condor/g3_gridpacks.sub", "w").write(g + ")\n")
rows = []
for s, (cm, n, fl) in TEST.items():
    sd = S.seed(s, 101); seeds.append(sd); os.makedirs(f"{S.WH}/work/test/{s}", exist_ok=True)
    rows.append(f"  {s} {E}/work/gridpacks/{s}_gridpack_s{S.seed(s,100)}.tar.gz {cm} {n} 1 1 {fl} {sd} test\n")
open(f"{S.WH}/work/condor/g3_tests.sub", "w").write(G.tsub(rows, "g3_tests.log")); S.check(seeds); print(seeds)
