#!/usr/bin/env python3
"""Correlations of the not-in-jet non-prompt-origin photons (pT > 25, lepton-free, not within dR 0.4 of a GenJet pT > 15; W+4j production files, every 12th file): fraction of the host events with a reco e/mu (pT > 15), prompt gen lepton inside |eta| < 2.5 / pT > 25, MET distribution and |dphi(photon, MET)| compared with all events (n_prompt_photons == 0). Usage: bash scripts/envrun.sh python3 -P scripts/diag_notinjet_corr.py"""
import glob, json, numpy as np, uproot, awkward as ak
from multiprocessing import Pool
PR = "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/production/wh"
def dphi(a, b): return (a-b+np.pi) % (2*np.pi)-np.pi
def work(f):
    T = uproot.open(f)["Delphes"]; G = uproot.open(f[:-5] + "_gen.root")["GenTruth"]
    x = T.arrays(["Photon.PT", "Photon.Eta", "Photon.Phi", "GenJet.PT", "GenJet.Eta", "GenJet.Phi", "Electron.PT", "Muon.PT", "MissingET.MET", "MissingET.Phi"], library="np")
    g = G.arrays(["n_prompt_photons", "gph_eta", "gph_phi", "gph_prompt", "glep_pt", "glep_eta", "glep_phi", "glep_prompt", "glep_pid"], library="ak"); npr = ak.to_numpy(g["n_prompt_photons"]); L = [ak.to_list(g[k]) for k in ("gph_eta", "gph_phi", "gph_prompt", "glep_eta", "glep_phi", "glep_pt", "glep_prompt", "glep_pid")]
    o = dict(N=0, all_reco_lep=0, all_gen_acc=0, all_met=[], ph_n=0, ph_reco_lep=0, ph_gen_acc=0, ph_met=[], ph_dphi_met=[], ph_pt=[], ph_pid=[], ph_drlep=[], ph_dphilep=[])
    for i in range(len(npr)):
        if npr[i] != 0: continue
        recolep = (sum(1 for q in x["Electron.PT"][i] if q > 15) + sum(1 for q in x["Muon.PT"][i] if q > 15)) >= 1
        pl = [(e, p, q, pid) for e, p, q, r, pid in zip(L[3][i], L[4][i], L[5][i], L[6][i], L[7][i]) if r and q > 10]; acc = any(q > 25 and abs(e) < 2.5 for e, p, q, pid in pl)
        o["N"] += 1; o["all_reco_lep"] += recolep; o["all_gen_acc"] += acc
        if o["N"] % 10 == 0: o["all_met"].append(float(x["MissingET.MET"][i][0]))
        gp = [(e, p) for e, p, r in zip(L[0][i], L[1][i], L[2][i]) if r]
        for q, e, p in zip(x["Photon.PT"][i], x["Photon.Eta"][i], x["Photon.Phi"][i]):
            if q <= 25 or abs(e) >= 2.5 or 1.4442 < abs(e) < 1.566: continue
            if any(np.hypot(e-ge, dphi(p, gf)) < 0.1 for ge, gf in gp) or any(np.hypot(e-le, dphi(p, lp)) < 0.2 for le, lp, lq, pid in pl): continue
            if any(np.hypot(e-e2, dphi(p, p2)) < 0.4 for q2, e2, p2 in zip(x["GenJet.PT"][i], x["GenJet.Eta"][i], x["GenJet.Phi"][i]) if q2 > 15): continue
            o["ph_n"] += 1; o["ph_reco_lep"] += recolep; o["ph_gen_acc"] += acc; o["ph_met"].append(float(x["MissingET.MET"][i][0])); o["ph_dphi_met"].append(float(abs(dphi(p, x["MissingET.Phi"][i][0])))); o["ph_pt"].append(float(q)); o["ph_pid"].append(int(pl[0][3]) if pl else 0); o["ph_drlep"].append(float(min([np.hypot(e-le, dphi(p, lp)) for le, lp, lq, pid in pl] or [99]))); o["ph_dphilep"].append(float(min([abs(dphi(p, lp)) for le, lp, lq, pid in pl] or [9])))
    return o
if __name__ == "__main__":
    fs = [f for f in sorted(glob.glob(f"{PR}/F_Wjjjj/*.root")) if not f.endswith("_gen.root")][::12]
    with Pool(8) as p: R = p.map(work, fs)
    N = sum(r["N"] for r in R); n = sum(r["ph_n"] for r in R); gm = np.concatenate([r["all_met"] for r in R]); pm = np.concatenate([r["ph_met"] for r in R]); dp = np.concatenate([r["ph_dphi_met"] for r in R]); pid = np.concatenate([r["ph_pid"] for r in R])
    out = dict(files=len(fs), events=N, photons=n, frac_events_reco_lepton_all=sum(r["all_reco_lep"] for r in R)/N, frac_events_gen_lepton_in_acc_all=sum(r["all_gen_acc"] for r in R)/N,
               frac_host_events_reco_lepton=sum(r["ph_reco_lep"] for r in R)/n, frac_host_events_gen_lepton_in_acc=sum(r["ph_gen_acc"] for r in R)/n, median_MET_all=float(np.median(gm)), median_MET_host=float(np.median(pm)), frac_dphi_gt_2p5=float((dp > 2.5).mean()), frac_electron=float((np.abs(pid) == 11).mean()), frac_muon=float((np.abs(pid) == 13).mean()), drlep_hist=np.histogram(np.concatenate([r["ph_drlep"] for r in R]), bins=[0, 0.4, 1, 2, 3, 99])[0].tolist(), dphilep_gt_2p5=float((np.concatenate([r["ph_dphilep"] for r in R]) > 2.5).mean()))
    json.dump(out, open("/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh/work/postprod/notinjet_corr.json", "w"), indent=1); print(out)
