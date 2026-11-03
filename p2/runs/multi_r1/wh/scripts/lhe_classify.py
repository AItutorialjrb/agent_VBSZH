#!/usr/bin/env python3
"""LHE-level (validation only, NOT a yield) classification of W+ H j j events generated with b quarks in p/j (5F):
 class A: no b/b~ among external partons;  class B: b external and some (W+ , b) or (W-, b~) pair within |m - 173| < 25 GeV (top-resonant, tHq/tHW-like)
 class C: b external, not top-resonant.  Also VBS-like fraction (m_jj>500, |deta_jj|>2.5 for the two final-state partons) per class.
Usage: lhe_classify.py <lhe.gz> <sigma_fb> <out.json>"""
import sys, gzip, json, math
fn, sig, out = sys.argv[1], float(sys.argv[2]), sys.argv[3]
cl = {k: [0, 0] for k in "ABC"}; n = 0
def m(*ps):
    E = sum(p[3] for p in ps); px = sum(p[0] for p in ps); py = sum(p[1] for p in ps); pz = sum(p[2] for p in ps)
    return math.sqrt(max(E*E-px*px-py*py-pz*pz, 0))
ev = None
for line in gzip.open(fn, "rt"):
    if line.startswith("<event>"): ev = []; hdr = None; continue
    if line.startswith("</event>"):
        n += 1; ini = [p for p in ev if p[5] == -1]; fin = [p for p in ev if p[5] == 1]
        W = [p for p in fin if abs(p[4]) == 24]; jets = [p for p in fin if abs(p[4]) in (1, 2, 3, 4, 5, 21)]
        hasb = any(abs(p[4]) == 5 for p in ev if p[5] in (-1, 1))
        top = any(abs(m(w, j) - 173.0) < 25 for w in W for j in jets if abs(j[4]) == 5 and w[4]*j[4] < 0 + 0*1 or False) if hasb else False
        # (W+ b) -> t ; W+ has pid +24, b has pid +5  (t -> W+ b): same sign pair
        top = any(abs(m(w, j) - 173.0) < 25 for w in W for j in jets if abs(j[4]) == 5 and w[4]*j[4] > 0) if hasb else False
        c = "A" if not hasb else ("B" if top else "C")
        jj = jets[:2]
        def eta(p): return 0.5*math.log((math.sqrt(p[0]**2+p[1]**2+p[2]**2)+p[2])/max(math.sqrt(p[0]**2+p[1]**2+p[2]**2)-p[2], 1e-9))
        vbs = len(jj) == 2 and m(*jj) > 500 and abs(eta(jj[0])-eta(jj[1])) > 2.5
        cl[c][0] += 1; cl[c][1] += vbs; ev = None; continue
    if ev is None: continue
    t = line.split()
    if len(t) == 13 and hdr is not None or (len(t) == 13 and ev is not None and hdr is None and ev == [] and False): pass
    if hdr is None and ev == []: hdr = line; continue          # event header line (NUP, IDPRUP, ...)
    if len(t) >= 13: ev.append((float(t[6]), float(t[7]), float(t[8]), float(t[9]), int(t[0]), int(t[4]) if False else int(t[1])))
res = {"n_events": n, "sigma_fb_total": sig, "classes": {k: dict(n=v[0], frac=v[0]/n, sigma_fb=sig*v[0]/n, n_vbs=v[1], vbs_frac=(v[1]/v[0] if v[0] else None), sigma_vbs_fb=sig*v[1]/n) for k, v in cl.items()}}
json.dump(res, open(out, "w"), indent=1); print(json.dumps(res["classes"]))
