#!/usr/bin/env python3
"""LHE-level (validation only): for W H j j events, fraction with an MG5 status-2 hadronic V (W/Z) resonance label, and its overlap with VBS-like
kinematics (m_jj>500, |deta|>2.5) and with the V-mass region 65<m_jj<105. MG5 diagram labels are NOT observables and not gauge invariant per diagram.
Usage: lhe_vjj.py <lhe.gz> <out.json>"""
import sys, gzip, json, math
def eta(p): pp = math.sqrt(p[0]**2+p[1]**2+p[2]**2); return 0.5*math.log((pp+p[2])/max(pp-p[2], 1e-9))
def mass(a, b):
    s = [a[i]+b[i] for i in range(4)]; return math.sqrt(max(s[3]**2-s[0]**2-s[1]**2-s[2]**2, 0))
n = 0; C = {"all": 0, "V": 0, "V&vbs": 0, "noV&vbs": 0, "mjjV": 0, "V&mjjV": 0, "vbs": 0}; ev = None
for l in gzip.open(sys.argv[1], "rt"):
    if l.startswith("<event>"): ev = []; first = True; continue
    if l.startswith("</event>"):
        n += 1; jets = [e for e in ev if e[5] == 1 and abs(e[4]) in (1, 2, 3, 4, 5, 21)][:2]
        hasV = any(abs(e[4]) in (23, 24) and e[5] == 2 for e in ev)
        vbs = len(jets) == 2 and mass(jets[0], jets[1]) > 500 and abs(eta(jets[0])-eta(jets[1])) > 2.5
        mv = len(jets) == 2 and 65 < mass(jets[0], jets[1]) < 105
        C["V"] += hasV; C["vbs"] += vbs; C["V&vbs"] += hasV and vbs; C["noV&vbs"] += (not hasV) and vbs; C["mjjV"] += mv; C["V&mjjV"] += hasV and mv; ev = None; continue
    if ev is None: continue
    if first: first = False; continue
    t = l.split()
    if len(t) >= 13: ev.append((float(t[6]), float(t[7]), float(t[8]), float(t[9]), int(t[0]), int(t[1])))
C["all"] = n; json.dump(C, open(sys.argv[2], "w")); print(C)
