#!/usr/bin/env python3
"""Phase-02 relevance estimate (NOT a yield): e->gamma fake from frozen ZH QCD/EW l+l-gamma jj Delphes samples (zh-final-v1.1).
Events with exactly 2 reco electrons (pT>15,|eta|<2.5), 0 muons, >=1 reco photon: each electron may fake a photon with f_e
(fake photon pT = electron pT); the other electron is the WH lepton (pT>25).  Then MET>30, b-veto, 2 tag jets mjj>500 |deta|>2.5
(jets cleaned against both electrons), 120<m(gamma, e->gamma)<130.  f_e in {1,2,5}% (ZH 02 §4).  QCD sample x C=2.05 generator-mjj
correction (ZH FINAL §4) is applied.  PEAK_Zveto adds |m(lepton,photon)-mZ|>10 GeV for both photons.  Usage: efake_frozen_zh.py <out.json> [nfiles]"""
import sys, glob, json, math, numpy as np, uproot
ZH = "/eos/home-r/rjiang/vbs_zh_codex_starter/production/final"
S = {"F_QCD_Zajj": (f"{ZH}/F_QCD_llajj_vbs/*_s*[0-9].root", 69.46, 2.052), "F_EW_Zajj": (f"{ZH}/F_EW_llajj_vbs/*_s*[0-9].root", 11.05, 1.0)}
NF = int(sys.argv[2]) if len(sys.argv) > 2 else 20
K = ["Photon.PT", "Photon.Eta", "Photon.Phi", "Electron.PT", "Electron.Eta", "Electron.Phi", "Muon.PT", "Jet.PT", "Jet.Eta", "Jet.Phi", "Jet.Mass", "Jet.BTag", "MissingET.MET"]
def p4(pt, eta, phi, m=0.0): return np.array([pt*math.cos(phi), pt*math.sin(phi), pt*math.sinh(eta), math.sqrt((pt*math.cosh(eta))**2 + m*m)])
def M(a, b): s = a + b; return math.sqrt(max(s[3]**2 - s[0]**2 - s[1]**2 - s[2]**2, 0))
dr = lambda e1, p1, e2, p2: math.hypot(e1 - e2, (p1 - p2 + math.pi) % (2*math.pi) - math.pi)
res = {}
for sid, (pat, sig, C) in S.items():
    files = sorted(glob.glob(pat))[:NF]; N = 0; vbs = 0; peak = 0; peak_zv = 0
    for fn in files:
        A = uproot.open(fn)["Delphes"].arrays(K, library="np"); n = len(A["MissingET.MET"]); N += n
        for i in range(n):
            el = [(p, e, h) for p, e, h in zip(A["Electron.PT"][i], A["Electron.Eta"][i], A["Electron.Phi"][i]) if p > 15 and abs(e) < 2.5]
            if len(el) != 2 or (A["Muon.PT"][i] > 15).any() or A["MissingET.MET"][i][0] <= 30: continue
            g = [(p, e, h) for p, e, h in zip(A["Photon.PT"][i], A["Photon.Eta"][i], A["Photon.Phi"][i]) if p > 20 and abs(e) < 2.5 and not 1.4442 < abs(e) < 1.566]
            if not g: continue
            J = [(p, e, h, m) for p, e, h, m, b in zip(A["Jet.PT"][i], A["Jet.Eta"][i], A["Jet.Phi"][i], A["Jet.Mass"][i], A["Jet.BTag"][i])
                 if p > 25 and abs(e) < 4.7 and all(dr(e, h, x[1], x[2]) > 0.4 for x in el + g[:1])]
            bt = [b for p, e, b in zip(A["Jet.PT"][i], A["Jet.Eta"][i], A["Jet.BTag"][i]) if p > 25 and abs(e) < 2.5 and b > 0]
            if len(J) < 2 or bt or not (M(p4(*J[0]), p4(*J[1])) > 500 and abs(J[0][1] - J[1][1]) > 2.5): continue
            for k in (0, 1):
                fake, lep = el[k], el[1 - k]
                if lep[0] <= 25 or not (abs(fake[1]) < 2.5 and not 1.4442 < abs(fake[1]) < 1.566) or dr(fake[1], fake[2], g[0][1], g[0][2]) < 0.4: continue
                vbs += 1
                if 120 < M(p4(*g[0]), p4(*fake)) < 130:
                    peak += 1
                    # Z-veto on m(lepton, any selected photon) (applies to the e->gamma candidate and the real photon)
                    if all(abs(M(p4(*lep), p4(*x)) - 91.19) > 10 for x in (fake, g[0])): peak_zv += 1
    w = sig*C*500.0/N
    res[sid] = dict(files=len(files), N=N, sigma_fb=sig, C_genmjj=C, w_evt_500=w, raw_candidates=dict(VBS=vbs, PEAK=peak, PEAK_Zveto=peak_zv),
                    yields_500={str(fe): dict(VBS=w*fe*vbs, PEAK=w*fe*peak, PEAK_Zveto=w*fe*peak_zv, PEAK_Zveto_ul95_if_zero=(3*w*fe if peak_zv == 0 else None)) for fe in (0.01, 0.02, 0.05)})
    print(sid, res[sid]["raw_candidates"], {k: (round(v["PEAK"], 4), round(v["PEAK_Zveto"], 4)) for k, v in res[sid]["yields_500"].items()})
json.dump(res, open(sys.argv[1], "w"), indent=1)
