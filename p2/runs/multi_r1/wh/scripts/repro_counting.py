#!/usr/bin/env python3
"""Independent reproduction of the cut-based window yields (s, b per class) directly from the skims with bgmodel.regions/derived (no sel_tables.py, no table.npz): compares with work/stat/counting.json. Writes work/stat/repro_counting.json."""
import sys, os, json, numpy as np
V11 = os.environ.get("V11") == "1"
sys.path.insert(0, "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh/scripts")
from bgmodel import *
Y = json.load(open(f"{WH}/work/bgmodel/yields{'_v11' if V11 else ''}.json")); rtau = Y["regions"]["VBS"]["r_tau"]
CL = {"signal": ["S_EW_WHjj"], "tau": ["S_EW_WHjj_taunu"], "prompt": ["B_QCD_Waajj_nomjj", "B_EW_Waajj_nomjj", "T_ttaa_1l"], "fake1": ["F_QCD_Wajjj_nomjj", "F_EW_Wajj_nomjj", "T_tta_1l", "T_tWa_1l"], "fake2": ["F_Wjjjj", "T_ttjj_1l"],
      "npl": ["Q_aajjj", "H_VBFH_jj"], "lostlep": ["V_WWa_WH", "V_WZa_WH", "V_ZZa_WH", "ZH_Zaajj_QCD_nomjj_lostlep", "ZH_Zaajj_EW_lostlep"] + (["ZH_Zajj_eFake_EWonly", "F_QCD_llajj_loose"] if V11 else ["ZH_Zajj_eFake"]), "higgs": ["H_QCD_WH_mlm", "H_ggZH_wh", "H_ZH_tautau_wh", "H_ttH_1l", "H_ttH_dilep_wh", "H_tHq_lep", "H_tHW_1l", "ZH_EW_ZHjj_lostlep", "ZH_QCD_ZHjj_lostlep"]}
tauc = {"prompt", "fake1", "fake2", "lostlep", "higgs"}; out = {}
for c, ss in CL.items():
    tot = 0.0
    for s in ss:
        D = load(s); R, d = regions(D); m = R["VBS"] & (D["jets"][:, 0, 0] > 30)
        m &= (d["mjj"] > 600) & (d["deta"] > 4.0) & (D["met"][:, 0] > 30) & (D["lep"][:, 0] > 25) & (np.abs(d["mgg"]-125) < 3.5)
        ph = D["ph"]; e1, e2 = ph[:, 0], ph[:, 1]; px = e1[:, 0]*np.cos(e1[:, 2])+e2[:, 0]*np.cos(e2[:, 2]); py = e1[:, 0]*np.sin(e1[:, 2])+e2[:, 0]*np.sin(e2[:, 2]); m &= np.hypot(px, py) > 75
        k = D["kind"]; w = D["w"]*D["norm"]*LUMI*D["cfac"][:, 0]
        if c == "fake1": m &= k == 1; w = w*D["f"][:, 0]
        elif c == "fake2": m &= k == 2; w = w*D["f"][:, 0]
        elif c == "npl":
            ys = Y["regions"]["PRE"]["samples"][s]; ratio = ys["heavy_flavour_factorised"]["hf_PRE_direct"]/ys["fakelep_nom"]["Y"] if ys["fakelep_nom"]["Y"] > 0 else 0.0; m &= k == 5; w = w*4e-5*(1+ratio)
        else: m &= k == 0
        if c in tauc: w = w*(1+rtau)
        tot += float(w[m].sum())
    out[c] = tot
ref = json.load(open(f"{WH}/work/stat/counting{'_v11' if V11 else ''}.json")); out["b_total"] = sum(v for k, v in out.items() if k not in ("signal", "b_total")); out["ref_s"] = ref["window_500"]["s"]; out["ref_b"] = ref["window_500"]["b"]
json.dump(out, open(f"{WH}/work/stat/repro_counting{'_v11' if V11 else ''}.json", "w"), indent=1); print(json.dumps(out))
