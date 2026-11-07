#!/usr/bin/env python3
"""Delphes electron -> photon-object rate (data input, FORMAT.md): per prompt gen electron/muon (GenTruth glep_*, prompt, pT>25, |eta|<2.5) of the W+4j production files (every 6th file), P(a reco Photon with pT>10 within dR<0.2) in bins of lepton pT and barrel/endcap,
split by gen lepton flavour; also P(a reco Photon pT>10 within dR<0.2 AND NO reco Electron/Muon within dR<0.2) = 'lepton lost and replaced by a photon object'. Usage: bash scripts/envrun.sh python3 -P scripts/postprod_egamma.py"""
import json, glob, numpy as np, uproot, awkward as ak
from multiprocessing import Pool
PR = "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/production/wh"; PT = [25, 40, 60, 100, 1000]
FS = sorted(f for f in glob.glob(f"{PR}/F_Wjjjj/*.root") if not f.endswith("_gen.root"))[::6]
def dphi(a, b): return (a-b+np.pi) % (2*np.pi)-np.pi
def work(f):
    T = uproot.open(f)["Delphes"]; G = uproot.open(f[:-5] + "_gen.root")["GenTruth"]
    a = T.arrays(["Photon.PT", "Photon.Eta", "Photon.Phi", "Electron.PT", "Electron.Eta", "Electron.Phi", "Muon.PT", "Muon.Eta", "Muon.Phi"], library="np"); g = G.arrays(["glep_pt", "glep_eta", "glep_phi", "glep_pid", "glep_prompt"], library="ak")
    LT, LE, LP, LI, LR = (ak.to_list(g[k]) for k in ("glep_pt", "glep_eta", "glep_phi", "glep_pid", "glep_prompt"))
    c = {fl: dict(n=np.zeros((2, len(PT)-1)), ph=np.zeros((2, len(PT)-1)), lost=np.zeros((2, len(PT)-1))) for fl in ("e", "mu")}
    for i in range(len(LT)):
        ph = [(q, e, p) for q, e, p in zip(a["Photon.PT"][i], a["Photon.Eta"][i], a["Photon.Phi"][i]) if q > 10 and abs(e) < 2.5]
        rl = [(e, p) for e, p in zip(a["Electron.Eta"][i], a["Electron.Phi"][i])] + [(e, p) for e, p in zip(a["Muon.Eta"][i], a["Muon.Phi"][i])]
        for q, e, p, pid, pr in zip(LT[i], LE[i], LP[i], LI[i], LR[i]):
            if not pr or q <= 25 or abs(e) >= 2.5: continue
            fl = "e" if abs(pid) == 11 else ("mu" if abs(pid) == 13 else None)
            if fl is None: continue
            ie = 0 if abs(e) < 1.5 else 1; ip = int(np.digitize(q, PT)-1)
            if not 0 <= ip < len(PT)-1: continue
            c[fl]["n"][ie, ip] += 1; m = [x for x in ph if np.hypot(e-x[1], dphi(p, x[2])) < 0.2]
            if m:
                c[fl]["ph"][ie, ip] += 1
                if not any(np.hypot(e-le, dphi(p, lp)) < 0.2 for le, lp in rl): c[fl]["lost"][ie, ip] += 1
    return {fl: {k: v.tolist() for k, v in d.items()} for fl, d in c.items()}
if __name__ == "__main__":
    with Pool(8) as p: R = p.map(work, FS, chunksize=1)
    out = {fl: {k: sum(np.array(r[fl][k]) for r in R).tolist() for k in ("n", "ph", "lost")} for fl in ("e", "mu")}
    out["pt_edges"] = PT; out["eta_bins"] = [[0, 1.5], [1.5, 2.5]]; out["n_files"] = len(FS)
    for fl in ("e", "mu"):
        n = np.array(out[fl]["n"]); out[fl]["rate_photon_within_0p2"] = (np.array(out[fl]["ph"])/np.maximum(n, 1)).tolist(); out[fl]["rate_lepton_lost_photon"] = (np.array(out[fl]["lost"])/np.maximum(n, 1)).tolist()
    json.dump(out, open("/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh/work/postprod/egamma_rate.json", "w"), indent=1)
    for fl in ("e", "mu"): print(fl, "n", np.array(out[fl]["n"]).sum(), "photon rate", np.round(np.array(out[fl]["rate_photon_within_0p2"]), 4).tolist(), "lost->photon", np.round(np.array(out[fl]["rate_lepton_lost_photon"]), 5).tolist())
