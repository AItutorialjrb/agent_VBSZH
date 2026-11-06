#!/usr/bin/env python3
"""Non-prompt-lepton (jet -> lepton) per-jet probability weighting for samples WITHOUT a real lepton (G2 review item 1; D-WH-4 / D28 pending).
Usage: fakelep_pilot.py <slim.root> <gen.root> <sigma_fb_times_k> <out.json> [lumi=500]       env: BVETO=1 (default 1), PHOTON_PT=25
 Event selection: no reco e/mu with pT>10; >=2 reco photons pT>25 |eta|<2.5 (two leading, crack excluded); MET>30 (event MET, ASSUMPTION: unchanged by the jet->lepton conversion);
 each reco jet with pT>25, |eta|<2.5 may be the 'lepton' with weight f_l(base)=2e-4 (the lepton carries x*pT_jet, x~N(0.85,0.1) truncated [0.5,1], must exceed 25 GeV);
 the remaining jets (pT>30, dR>0.4 from photons and lepton-jet) give the two tag jets; b-veto = no b-tag among remaining jets (pT>30,|eta|<2.5) if BVETO.
 Regions: PRE = above with >=2 tag jets; VBS = PRE + mjj>500,|deta|>2.5; PEAK = VBS + 120<m_gg<130.
 f_l per D28 (cited range, ATLAS arXiv:1110.3174 p.4: jet rejection 5e4/5e3/5e2 = tight/medium/loose -> 2e-5/2e-4/2e-3): yields are reported at f_l = 2e-5 and 2e-3 (nominal 2e-4); ZH-comparison variants 3e-5/1e-4/1e-3 kept, all labelled 'assumption anchored to a cited ID-rejection range, not data-driven'; N_eff does not depend on f_l (uniform scale).
 Q_aajj has prompt photons by construction (n_prompt>=2 not required here: all events used)."""
import sys, os, json, numpy as np, awkward as ak, uproot
slim, genf, sk, outj = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4]; lumi = float(sys.argv[5]) if len(sys.argv) > 5 else 500.0
BVETO = os.environ.get("BVETO", "1") == "1"; PTG = float(os.environ.get("PHOTON_PT", "25")); F0 = 2e-4
rng = np.random.default_rng(13600777); t = uproot.open(slim)["Delphes"]; N = t.num_entries; A = lambda k: t[k].array()
def lv(pt, eta, phi): return np.array([pt*np.cos(phi), pt*np.sin(phi), pt*np.sinh(eta), pt*np.cosh(eta)])
def m(a, b): s = a+b; return np.sqrt(max(s[3]**2-s[0]**2-s[1]**2-s[2]**2, 0.0))
def dr(e1, p1, e2, p2): return np.hypot(e1-e2, (p1-p2+np.pi) % (2*np.pi)-np.pi)
jpt, jeta, jphi, jb = A("Jet/Jet.PT"), A("Jet/Jet.Eta"), A("Jet/Jet.Phi"), A("Jet/Jet.BTag")
ept, mpt = A("Electron/Electron.PT"), A("Muon/Muon.PT"); gpt, geta, gphi = A("Photon/Photon.PT"), A("Photon/Photon.Eta"), A("Photon/Photon.Phi"); met = A("MissingET/MissingET.MET")
reg = {r: [] for r in ("PRE", "VBS", "PEAK")}
for i in range(N):
    if len(met[i]) == 0 or met[i][0] < 30 or ak.sum(ept[i] > 10) + ak.sum(mpt[i] > 10) > 0: continue
    G = sorted([(gpt[i][k], geta[i][k], gphi[i][k]) for k in range(len(gpt[i])) if gpt[i][k] > PTG and abs(geta[i][k]) < 2.5 and not (1.4442 < abs(geta[i][k]) < 1.566)], reverse=True)
    if len(G) < 2: continue
    mgg = m(lv(*G[0]), lv(*G[1])); J = [(jpt[i][k], jeta[i][k], jphi[i][k], bool(jb[i][k] > 0)) for k in range(len(jpt[i])) if jpt[i][k] > 20 and abs(jeta[i][k]) < 4.7]
    acc = {r: 0.0 for r in reg}
    for a, (pt, eta, phi, b) in enumerate(J):
        x = float(np.clip(rng.normal(0.85, 0.10), 0.5, 1.0))
        if not (pt > 25 and abs(eta) < 2.5 and x*pt > 25): continue
        rest = [j for k, j in enumerate(J) if k != a and j[0] > 30 and all(dr(j[1], j[2], g[1], g[2]) > 0.4 for g in G[:2]) and dr(j[1], j[2], eta, phi) > 0.4]
        if BVETO and any(j[3] and abs(j[1]) < 2.5 for j in rest): continue
        if len(rest) < 2: continue
        acc["PRE"] += F0; j1, j2 = sorted(rest, reverse=True)[:2]
        if m(lv(*j1[:3]), lv(*j2[:3])) > 500 and abs(j1[1]-j2[1]) > 2.5:
            acc["VBS"] += F0
            if 120 < mgg < 130: acc["PEAK"] += F0
    for r in reg:
        if acc[r] > 0: reg[r].append(acc[r])
w0 = sk*lumi/N; res = {"selection": __doc__.split("Event selection:")[1].split("f_l is PENDING")[0].strip(), "N_gen": N, "sigma_k_fb": sk, "lumi_fb": lumi, "f_l_nominal": F0, "f_l_range_assumed": [2e-5, 2e-3], "f_l_status": "D28: cited range ATLAS 1110.3174 p.4 (tight/medium/loose ID rejection), not data-driven", "regions": {}}
for r, lst in reg.items():
    if not lst: res["regions"][r] = {"n_events": 0, "UL95_events_3": float(3*w0*F0*0+0)}; continue
    W = w0*np.array(lst); res["regions"][r] = {"n_events": len(lst), "N_eff": float(W.sum()**2/(W**2).sum()), "yield_nominal": float(W.sum()), "yield_f2e-5": float(W.sum()*0.1), "yield_f2e-3": float(W.sum()*10.0), "yield_f3e-5_ZHcmp": float(W.sum()*0.15), "yield_f1e-4_ZHcmp": float(W.sum()*0.5), "yield_f1e-3_ZHcmp": float(W.sum()*5.0)}
json.dump(res, open(outj, "w"), indent=1); print(json.dumps(res, indent=1))
