#!/usr/bin/env python3
"""Phase-02 BOUND (not a yield): QCD gamma-gamma+jets with one jet faking an isolated lepton.  Delphes objects; per event the
fake weight = f_l x (number of reco jets pT>25 |eta|<2.5 that are not one of the two leading tag jets); fake lepton pT = jet pT x 0.85.
Selection = WH illustrative: >=2 photons (pT>20,|eta|<2.5, no crack), no real lepton, fake lepton pT>25, MET>30, 2 tag jets
(leading two among remaining) mjj>500 |deta|>2.5, 120<mgg<130.  f_l scenarios {3e-5, 1e-4, 1e-3} (ZH 02 §4 range).
Usage: fakelep_bound.py <delphes.root> <sigma_fb> <out.json>"""
import sys, json, math, numpy as np, uproot
f, sig, outp = sys.argv[1], float(sys.argv[2]), sys.argv[3]
t = uproot.open(f)["Delphes"]; N = t.num_entries
A = {k: t[k].array(library="np") for k in ["Photon.PT", "Photon.Eta", "Photon.Phi", "Electron.PT", "Muon.PT", "Jet.PT", "Jet.Eta", "Jet.Phi", "Jet.Mass", "MissingET.MET"]}
def p4(pt, eta, phi, m=0.0): return np.array([pt*math.cos(phi), pt*math.sin(phi), pt*math.sinh(eta), math.sqrt((pt*math.cosh(eta))**2 + m*m)])
def M(a, b): s = a + b; return math.sqrt(max(s[3]**2 - s[0]**2 - s[1]**2 - s[2]**2, 0))
cnt = dict(two_photons=0, no_real_lepton=0, met30=0, vbs=0, peak=0); wsum = dict(vbs=0.0, peak=0.0, pre=0.0); wpk = []
for i in range(N):
    g = [(p, e, h) for p, e, h in zip(A["Photon.PT"][i], A["Photon.Eta"][i], A["Photon.Phi"][i]) if p > 20 and abs(e) < 2.5 and not 1.4442 < abs(e) < 1.566]
    if len(g) < 2: continue
    cnt["two_photons"] += 1
    if (A["Electron.PT"][i] > 15).any() or (A["Muon.PT"][i] > 15).any(): continue
    cnt["no_real_lepton"] += 1
    if A["MissingET.MET"][i][0] <= 30: continue
    cnt["met30"] += 1
    J = [(p, e, h, m) for p, e, h, m in zip(A["Jet.PT"][i], A["Jet.Eta"][i], A["Jet.Phi"][i], A["Jet.Mass"][i]) if p > 25 and abs(e) < 4.7]
    if len(J) < 3: continue
    nfake = 0
    for k, j in enumerate(J):  # candidate fake lepton k; tags = two leading of the rest
        if abs(j[1]) >= 2.5 or 0.85*j[0] <= 25: continue
        rest = [x for kk, x in enumerate(J) if kk != k][:2]
        if M(p4(*rest[0]), p4(*rest[1])) > 500 and abs(rest[0][1] - rest[1][1]) > 2.5: nfake += 1
    wsum["pre"] += 0
    if nfake == 0: continue
    cnt["vbs"] += 1; wsum["vbs"] += nfake
    if 120 < M(p4(*g[0][:3]), p4(*g[1][:3])) < 130: cnt["peak"] += 1; wsum["peak"] += nfake; wpk.append(nfake)
w = sig*500.0/N
res = dict(file=f, N=N, sigma_fb=sig, w_evt_500=w, raw_counts=cnt, candidate_sum=wsum,
           yields_500={str(fl): dict(VBS=w*fl*wsum["vbs"], PEAK=w*fl*wsum["peak"], PEAK_ul95_if_zero=(3*w*fl if cnt["peak"] == 0 else None),
                                     PEAK_window_scaled=w*fl*wsum["vbs"]*10/70) for fl in (3e-5, 1e-4, 1e-3)},
           note="PEAK_window_scaled = VBS x 10/70 (flat m_gg in the 100-170 generator window): used when raw PEAK count is too small")
json.dump(res, open(outp, "w"), indent=1); print(json.dumps(res, indent=1))
