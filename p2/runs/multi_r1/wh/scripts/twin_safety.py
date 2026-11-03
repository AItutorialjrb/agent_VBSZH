#!/usr/bin/env python3
"""Generator-cut safety from a twin (mmjj=0) sample: among events passing a loose reco VBS-like selection (>=1 lepton pT>25, >=1 photon pT>25 |eta|<2.5, >=2 jets pT>30 with mjj>MJJ, |deta|>2.5),
fraction whose parton-level (LHE outgoing partons) m_jj is below the production generator cut (400 GeV). Usage (pinned environment, uproot/awkward/numpy from the LCG_110 view; NOT `python3 -I`, which drops PYTHONPATH):
  source <repo>/p2/lib/scripts/setup_stack.sh; python3 -P scripts/twin_safety.py <slim.root> <lhe.gz> <out.json>
Inputs are the slim Delphes file and LHE of the twin test job copied with xrdcp (see work/xrd/). Selection is deliberately loose (>=1 lepton, >=1 photon); statistics 27/82 selected events."""
import sys, gzip, json, math, numpy as np, uproot, awkward as ak
slim, lhe, out = sys.argv[1:4]
t = uproot.open(slim)["Delphes"]; A = lambda k: t[k].array()
jpt, jeta, jphi, jm = A("Jet/Jet.PT"), A("Jet/Jet.Eta"), A("Jet/Jet.Phi"), A("Jet/Jet.Mass")
ept, mpt, gpt, geta = A("Electron/Electron.PT"), A("Muon/Muon.PT"), A("Photon/Photon.PT"), A("Photon/Photon.Eta")
mg = []; ev = None
for l in gzip.open(lhe, "rt"):
    if l.startswith("<event>"): ev = []; first = True; continue
    if l.startswith("</event>"):
        p = [e for e in ev if e[5] == 1 and (abs(e[4]) <= 5 or e[4] == 21)][:2]
        s = [p[0][i]+p[1][i] for i in range(4)]; mg.append(math.sqrt(max(s[3]**2-s[0]**2-s[1]**2-s[2]**2, 0))); ev = None; continue
    if ev is None: continue
    if first: first = False; continue
    x = l.split()
    if len(x) >= 13: ev.append((float(x[6]), float(x[7]), float(x[8]), float(x[9]), int(x[0]), int(x[1])))
mg = np.array(mg); N = len(mg); assert N == t.num_entries
res = {"N": N, "frac_parton_mjj_lt_400_all": float((mg < 400).mean())}
for MJJ in (500, 700):
    sel = np.zeros(N, bool)
    for i in range(N):
        J = [(jpt[i][k], jeta[i][k], jphi[i][k], jm[i][k]) for k in range(len(jpt[i])) if jpt[i][k] > 30 and abs(jeta[i][k]) < 4.7]
        if len(J) < 2 or not ((ak.sum(ept[i] > 25) + ak.sum(mpt[i] > 25)) >= 1) or not ak.sum((gpt[i] > 25) & (abs(geta[i]) < 2.5)) >= 1: continue
        v = [np.array([j[0]*math.cos(j[2]), j[0]*math.sin(j[2]), j[0]*math.sinh(j[1]), math.sqrt((j[0]*math.cosh(j[1]))**2+j[3]**2)]) for j in J[:2]]; s = v[0]+v[1]
        sel[i] = math.sqrt(max(s[3]**2-s[0]**2-s[1]**2-s[2]**2, 0)) > MJJ and abs(J[0][1]-J[1][1]) > 2.5
    n = int(sel.sum()); k = int((sel & (mg < 400)).sum())
    res[f"reco_mjj_gt_{MJJ}"] = {"n_selected": n, "n_with_parton_mjj_lt_400": k, "lost_frac": (k/n if n else None), "lost_frac_err": (math.sqrt(k*(n-k)/n)/n if n else None)}
json.dump(res, open(out, "w"), indent=1); print(json.dumps(res))
