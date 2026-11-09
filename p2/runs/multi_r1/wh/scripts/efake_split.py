#!/usr/bin/env python3
"""Split ZH_Zajj_eFake (and other real2 lost-lepton rows) into e->gamma (>=1 photon of class cls1: Delphes photon object within dR<0.2 of a prompt generator lepton) and lost-lepton (both photons cls0, lepton outside acceptance / not reconstructed) parts, per region, with C factors. Output work/bgmodel/efake_split.json"""
import sys, json, numpy as np
sys.path.insert(0, "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh/scripts")
from bgmodel import *
out = {}
tot = json.load(open(f"{WH}/work/bgmodel/yields.json"))
for s in ("ZH_Zajj_eFake", "ZH_Zaajj_QCD_nomjj_lostlep", "ZH_Zaajj_EW_lostlep", "V_WWa_WH", "V_WZa_WH", "V_ZZa_WH"):
    D = load(s); R, _ = regions(D); c = D["cfac"][:, 0]; ncls1 = (D["ph"][:, :, 3] == 1).sum(1); out[s] = {}
    for rn in ("PRE", "VBS", "PEAK"):
        cn = np.ones(len(c)) if rn == "PRE" else c; w = D["w"]*D["norm"]*LUMI*cn
        for lab, m in (("egamma", ncls1 >= 1), ("lostlep", ncls1 == 0)):
            mm = R[rn] & m; x = w[mm]; out[s].setdefault(rn, {})[lab] = dict(Y=float(x.sum()), stat=float(np.sqrt((x**2).sum())), nraw=int(mm.sum()))
json.dump(out, open(f"{WH}/work/bgmodel/efake_split.json", "w"), indent=1)
b = {rn: sum(v["nom"] for c_, v in tot["regions"][rn]["classes"].items() if c_ not in ("signal", "xcheck")) for rn in ("PRE", "VBS", "PEAK")}
print("SR background total (nominal, all classes except signal/xcheck):", b)
for s in out:
    for rn in ("PEAK", "VBS"): print(s, rn, {k: (round(v["Y"], 3), v["nraw"]) for k, v in out[s][rn].items()}, "frac of bkg lostlep %.3f" % (out[s][rn]["lostlep"]["Y"]/b[rn]))
