#!/usr/bin/env python3
"""Lost-lepton class v1 (vbs twin x C) vs v1.1 (loose direct) at the selection, per-event weights, N_eff, share of sum w^2. Writes work/v11_crosscheck.json"""
import json, numpy as np
WH = "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh"; cb = json.load(open(f"{WH}/work/sel/selection_final.json"))["cut_based"]["cuts"]
def sel(t):
    return (t["mjj"] > cb["mjj"]) & (t["deta"] > cb["deta"]) & (t["ptgg"] > cb["ptgg"]) & (t["met"] > cb["met"]) & (t["mt"] > cb["mt"]) & (t["ptl"] > cb["ptl"]) & (np.abs(t["mgg"]-125) < cb["hw"]) & (t["zstar"] < cb["zs"])
o = {}
for tag, f in (("v1", "table"), ("v11", "table_v11")):
    t = dict(np.load(f"{WH}/work/sel/{f}.npz")); meta = json.load(open(f"{WH}/work/sel/{f}_meta.json")); cid = meta["classes"]["lost_lepton_egamma"]; m = sel(t); ll = m & (t["cls"] == cid); b = m & (t["cls"] != meta["classes"]["signal"])
    W2all = float((t["w"][b]**2).sum()); d = {}
    for name, mk in (("all_lostlep_class", ll), ("eFake_QCD_part" if tag == "v1" else "loose_QCD_part", ll & (np.isin(t["sid"], [i for i, s in enumerate(meta["samples"]) if s in ("ZH_Zajj_eFake", "F_QCD_llajj_loose")])) & ((t["qcddir"].astype(bool)) if tag == "v1" else np.isin(t["sid"], [meta["samples"].index("F_QCD_llajj_loose")])))):
        w = t["w"][mk]; d[name] = dict(Y=float(w.sum()), stat=float(np.sqrt((w**2).sum())), nraw=int(mk.sum()), neff=float(w.sum()**2/(w**2).sum()) if mk.any() else 0.0, share_of_b_sumw2=float((w**2).sum()/W2all), mean_abs_w=float(np.abs(w).mean()) if mk.any() else 0.0)
    o[tag] = d
q1 = o["v1"]["eFake_QCD_part"]["Y"]; o["v1_C_range_QCD_part"] = dict(C_low_1=q1/1.866, central=q1, C_high_2p732=q1*2.732/1.866, v11_loose=o["v11"]["loose_QCD_part"]["Y"], v11_loose_stat=o["v11"]["loose_QCD_part"]["stat"])
o["weight_ratio_loose_to_vbs"] = o["v11"]["loose_QCD_part"]["mean_abs_w"]/(o["v1"]["eFake_QCD_part"]["mean_abs_w"]/1.866)
json.dump(o, open(f"{WH}/work/v11_crosscheck.json", "w"), indent=1); print(json.dumps(o))
