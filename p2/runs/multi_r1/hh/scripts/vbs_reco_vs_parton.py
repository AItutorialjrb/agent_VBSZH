#!/usr/bin/env python3
"""VBS tagging-jet validation: reco-level (Delphes AK5, any opposite-hemisphere pair, pT>30,|eta|<4.7) vs parton-level (LHE any-pair) fraction passing mjj>500,|d eta|>3.5 for the SM signal test job.
Usage: vbs_reco_vs_parton.py <delphes.root> <lhe.gz>"""
import sys, numpy as np, awkward as ak, uproot
sys.path.insert(0, __file__.rsplit("/", 1)[0]); from morph_closure import read_lhe
t = uproot.open(sys.argv[1])["Delphes"]; n = t.num_entries
pt, eta, phi, m = (t[f"Jet/Jet.{k}"].array() for k in ("PT", "Eta", "Phi", "Mass"))
J = ak.zip({"pt": pt, "eta": eta, "phi": phi, "m": m}); J = J[(J.pt > 30) & (abs(J.eta) < 4.7)]
x, y = ak.unzip(ak.combinations(J, 2, axis=1))
px = x.pt*np.cos(x.phi)+y.pt*np.cos(y.phi); py = x.pt*np.sin(x.phi)+y.pt*np.sin(y.phi); pz = x.pt*np.sinh(x.eta)+y.pt*np.sinh(y.eta)
e = np.sqrt(x.m**2+(x.pt*np.cosh(x.eta))**2)+np.sqrt(y.m**2+(y.pt*np.cosh(y.eta))**2); mjj = np.sqrt(np.maximum(e**2-px**2-py**2-pz**2, 0))
ok = ak.any((mjj > 500) & (abs(x.eta-y.eta) > 3.5) & (x.eta*y.eta < 0), axis=1); fr = float(ak.mean(ok))
xs, nl, o = read_lhe(sys.argv[2]); fp = float(np.mean((o["mjj"] > 500) & (o["deta"] > 3.5)))
print(f"reco any-pair (mjj>500,|deta|>3.5,opp. hemisphere) fraction = {fr:.3f} +- {np.sqrt(fr*(1-fr)/n):.3f} (N={n});  parton hardest-two-non-Higgs pair fraction = {fp:.3f} (N={nl})")
