#!/usr/bin/env python3
"""Safety of the generator cut ptj>20 of the ME+1-jet model F_QCD_Wajjj_nomjj for the CONVERTED jet (recheck 3 item 4; D4). In the 2-jet+PS twin (F_QCD_Wajj_nomjj, 40 000 events, no cut on the PS jet) every reco jet that can be converted into the
fake photon is weighted with the measured W-class j->gamma rate f(pT_jet, eta) x P(x*pT_jet>25) (x from the measured histogram); events: exactly one e/mu pT>25, MET>30, one prompt (n_prompt_photons==1) reco photon pT>25, >=2 remaining jets pT>30 (dR>0.4 from photon and converted jet)
with mjj>500, |deta|>2.5 (VBS region of the pilots). Reported: weighted fraction of conversions whose GenJet (dR<0.3) has pT<20 GeV or no GenJet (such a jet would be removed by ptj>20 in the 3j ME), also for <25 and <30 GeV.
Usage: convjet_cut_safety.py <out.json> <slim.root> [...]   (twin files, read-only)"""
import sys, json, numpy as np, uproot, awkward as ak
out, files = sys.argv[1], sys.argv[2:]
R = json.load(open("/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh/work/jgamma_rate.json"))
PTE = np.array(R["pt_edges"]); RT = np.array(R["rate_W"]); XH = np.array(R["x_hist_per_ptbin_W"], float); XE = np.array(R["x_edges"]); XC = 0.5*(XE[1:]+XE[:-1])
def ptb(q): return min(max(int(np.digitize(q, PTE)-1), 0), len(PTE)-2)
def pacc(q): h = XH[ptb(q)]; return float(h[XC*q > 25].sum()/h.sum()) if h.sum() else 0.0
def dr(a, b, c, d): return np.hypot(a-c, (b-d+np.pi) % (2*np.pi)-np.pi)
def mjj(j1, j2):
    v = lambda q, e, p: np.array([q*np.cos(p), q*np.sin(p), q*np.sinh(e), q*np.cosh(e)]); s = v(*j1)+v(*j2); return np.sqrt(max(s[3]**2-s[0]**2-s[1]**2-s[2]**2, 0))
THR = (20, 25, 30); W = 0.0; low = {t: 0.0 for t in THR}; n_ev = 0; n_conv = 0
for f in files:
    g = f[:-5] + "_gen.root"; npr = ak.to_numpy(uproot.open(g)["GenTruth"]["n_prompt_photons"].array())
    T = uproot.open(f)["Delphes"]; a = T.arrays(["Jet.PT", "Jet.Eta", "Jet.Phi", "GenJet.PT", "GenJet.Eta", "GenJet.Phi", "Photon.PT", "Photon.Eta", "Photon.Phi", "Electron.PT", "Electron.Eta", "Muon.PT", "Muon.Eta", "MissingET.MET"], library="np")
    for i in range(len(a["Jet.PT"])):
        if npr[i] != 1 or a["MissingET.MET"][i][0] <= 30: continue
        nl = [q for q, e in zip(a["Electron.PT"][i], a["Electron.Eta"][i]) if q > 10 and abs(e) < 2.5]+[q for q, e in zip(a["Muon.PT"][i], a["Muon.Eta"][i]) if q > 10 and abs(e) < 2.5]
        if len(nl) != 1 or nl[0] <= 25: continue
        ph = [(q, e, p) for q, e, p in zip(a["Photon.PT"][i], a["Photon.Eta"][i], a["Photon.Phi"][i]) if q > 25 and abs(e) < 2.5]
        if not ph: continue
        r0 = ph[0]; J = [(q, e, p) for q, e, p in zip(a["Jet.PT"][i], a["Jet.Eta"][i], a["Jet.Phi"][i]) if q > 25 and abs(e) < 4.7 and dr(e, p, r0[1], r0[2]) > 0.4]
        n_ev += 1
        for k, (q, e, p) in enumerate(J):
            if abs(e) >= 2.5: continue
            tags = sorted([x for m_, x in enumerate(J) if m_ != k and x[0] > 30], reverse=True)
            if len(tags) < 2 or mjj(tags[0], tags[1]) <= 500 or abs(tags[0][1]-tags[1][1]) <= 2.5: continue
            w = RT[0 if abs(e) < 1.5 else 1][ptb(q)]*pacc(q)
            if w <= 0: continue
            gm = [gq for gq, ge, gp in zip(a["GenJet.PT"][i], a["GenJet.Eta"][i], a["GenJet.Phi"][i]) if dr(e, p, ge, gp) < 0.3]
            gpt = max(gm) if gm else 0.0; W += w; n_conv += 1
            for t in THR:
                if gpt < t: low[t] += w
res = dict(n_events_used=n_ev, n_conversions=n_conv, weighted_total=W, frac_lt={str(t): (low[t]/W if W else None) for t in THR}, note=__doc__.split("Usage")[0].strip())
json.dump(res, open(out, "w"), indent=1); print({k: v for k, v in res.items() if k != "note"})
