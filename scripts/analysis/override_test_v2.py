#!/usr/bin/env python3
"""Build a registry override for sensitivity.py from finished test_v2 jobs (2000 events each), replacing the
200/500-event pilots where a test_v2 sample exists.  sigma: LHE init (fixed order) or Pythia accepted sigma
(MLM samples, after matching).  Writes <out.json>; prints which samples were swapped.
Usage: python3 -P override_test_v2.py <npz_dir> <out.json>"""
import sys, json, glob, os
P = "/eos/home-r/rjiang/vbs_zh_codex_starter/production/test_v2"
D, OUT = sys.argv[1:3]
BGG = 0.002270
# test_v2 id -> (registry id, kind, k, mlm)
MAP = {"H_ttH": ("H_ttH", "res", BGG, False), "T_tta": ("T_tta", "ff1", 1.0, False), "T_tWa": ("T_tWa", "ff1", 1.0, False),
       "T_tt": ("T_tt", "ff2", 1.0, False), "T_ttaa": ("T_ttaa", "cont", 1.0, False),
       "H_QCD_ZH_mlm": ("X_QCD_ZH_mlm", "res", 0.9783*BGG, True), "H_ZH_tautau": ("H_ZH_tautau", "res", BGG, True),
       "H_tHW": ("H_tHW", "res", BGG, False), "H_ggZH": ("H_ggZH", "res", BGG, False)}
ov = {}
for tid, (rid, kind, k, mlm) in MAP.items():
    js = glob.glob(f"{P}/{tid}/*.json")
    if not js or not os.path.exists(f"{D}/tv2_{tid}.npz"): continue
    j = json.load(open(js[0]))
    if mlm:   # Pythia ' | sum ... | sigma_mb err_mb |'
        sig = float(j["pythia_sum_line"].split("|")[-2].split()[0]) * 1e12   # mb -> fb
    else:   # LHE <init> line 3 holds only the FIRST subprocess -> use the gridpack's total (MG5 status file)
        st = open(f"/eos/home-r/rjiang/vbs_zh_codex_starter/production/gridpacks/{tid}_status.txt").read()
        sig = float(st.split("Cross-section :")[1].split()[0]) * 1e3
    ov[rid] = dict(npz=f"tv2_{tid}", sig=sig, k=k, kind=kind, syst=("fake" if kind.startswith("ff") else "other"),
                   src=f"test_v2 {tid} ({j['n_delphes']} ev, seed {j['mg_seed']}); sigma {'PY8 matched' if mlm else 'MG5 gridpack total'}")
    if rid in ("X_QCD_ZH_mlm", "H_ZH_tautau", "H_tHW", "H_ggZH"): ov[rid]["xcheck"] = True   # reported, not added to b
    if tid == "T_tt": ov[rid]["oom"] = True
json.dump(ov, open(OUT, "w"), indent=1)
print(json.dumps({k: (v["sig"], v["src"]) for k, v in ov.items()}, indent=1))
