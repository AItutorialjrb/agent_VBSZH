#!/usr/bin/env python3
"""LHE-level VALIDATION summary (not a yield): init-block sigma per process id, parton-level mjj of the two outgoing partons,
fraction with an s-channel W/Z resonance written by MG5, charge split.  Usage: lhe_summary.py <lhe.gz> [out.json]"""
import gzip, sys, json, math, re
f = sys.argv[1]; txt = gzip.open(f, "rt").read()
init = txt[txt.index("<init>"):txt.index("</init>")].strip().splitlines()[2:]
procs = [list(map(float, l.split()[:4])) for l in init if l.strip() and not l.strip().startswith("<")]
sig = sum(p[0] for p in procs); err = math.sqrt(sum(p[1]**2 for p in procs))
ev = re.findall(r"<event>(.*?)</event>", txt, re.S)
n = len(ev); nres = 0; nwp = 0; mj = []; vbs = 0
for e in ev:
    L = [l.split() for l in e.strip().splitlines()[1:] if l.strip() and not l.lstrip().startswith("<") and not l.lstrip().startswith("#")]
    parts = [x for x in L if len(x) >= 13]
    pid = [int(x[0]) for x in parts]; st = [int(x[1]) for x in parts]; m1 = [int(x[2]) for x in parts]
    if 24 in pid: nwp += 1
    # hadronic s-channel resonance: status 2 W/Z whose daughters are quarks
    for k, x in enumerate(parts):
        if st[k] == 2 and abs(pid[k]) in (23, 24):
            ds = [abs(pid[j]) for j in range(len(parts)) if m1[j] == k + 1]
            if ds and max(ds) <= 5: nres += 1; break
    q = [x for k, x in enumerate(parts) if st[k] == 1 and (abs(pid[k]) <= 5 or pid[k] == 21)]
    if len(q) >= 2:
        E = sum(float(x[9]) for x in q[:2]); px = sum(float(x[6]) for x in q[:2]); py = sum(float(x[7]) for x in q[:2]); pz = sum(float(x[8]) for x in q[:2])
        m = math.sqrt(max(E*E - px*px - py*py - pz*pz, 0)); mj.append(m)
        eta = lambda x: math.asinh(float(x[8])/math.hypot(float(x[6]), float(x[7])))
        if m > 500 and abs(eta(q[0]) - eta(q[1])) > 2.5: vbs += 1
out = dict(file=f, sigma_fb=sig*1000, err_fb=err*1000, per_process_fb=[p[0]*1000 for p in procs], n_events=n,
           frac_hadronic_V_resonance=nres/n, frac_Wplus=nwp/n, frac_parton_mjj_60_110=sum(60 < m < 110 for m in mj)/n,
           frac_parton_mjj500_deta2p5=vbs/n, median_parton_mjj=sorted(mj)[len(mj)//2] if mj else None)
print(json.dumps(out, indent=1))
if len(sys.argv) > 2: json.dump(out, open(sys.argv[2], "w"), indent=1)
