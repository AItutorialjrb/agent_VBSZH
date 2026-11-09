#!/usr/bin/env python3
"""single_r1 WH Phase 03: cross-section table, BR/decay closure, order closure, N_MC requirement table.
Inputs : wh/work/gridpacks/<card>_status.txt (gridpack builds), wh/work/xsec/<card>_s<seed>.status.txt (sigma-only runs),
         wh/work/test/<card>/*.json (test jobs: LHE init sigma, PY8 sum line).  All sigma are MG5 LO, before any BR factor
         that the sample does not already contain (see BR ledger in samples.yaml / 01 report).
Output : wh/work/p03/xsec.json + markdown tables on stdout.   Usage: python3 -P wh/scripts/xsec_table.py
"""
import os, re, sys, json, glob, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_cards as MC
WH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.makedirs(f"{WH}/work/p03", exist_ok=True)

def parse_status(path):
    if not os.path.exists(path): return None
    t = open(path).read(); m = re.search(r"Cross-section :\s*([-0-9.eE+]+) \+- ([0-9.eE+-]+) pb", t)
    rc = re.search(r"rc=(\d+)", t); w = re.search(r"wall_s=(\d+)", t); n = re.search(r"ncore=(\d+)", t)
    d = dict(rc=int(rc.group(1)) if rc else None, wall_s=int(w.group(1)) if w else None, ncore=int(n.group(1)) if n else None, src=path)
    if m: d.update(sigma_fb=1e3 * float(m.group(1)), err_fb=1e3 * float(m.group(2)))
    return d

X = {}
for s in MC.S:
    p = f"{WH}/work/gridpacks/{s['name']}_status.txt" if s["gridpack"] else f"{WH}/work/xsec/{s['name']}_s{s['seed_gp']}.status.txt"
    d = parse_status(p)
    if d: X[s["name"]] = {**d, "seed": s["seed_gp"], "br": s["br"], "role": s["role"]}
    for j in sorted(glob.glob(f"{WH}/work/test/{s['name']}/*.json")):
        J = json.load(open(j)); xs = [float(v) for v in J["lhe_init_xsec_pb_err_pb_max_lprup"].split()[:2]]
        lhe = j.replace(".json", ".lhe.gz")
        if os.path.exists(lhe):   # json keeps only the first <init> process line: sum ALL process lines (multi-group gridpacks)
            import gzip
            with gzip.open(lhe, "rt") as fh:
                ini = []
                for line in fh:
                    if "<init>" in line: ini = ["start"]; continue
                    if "</init>" in line: break
                    if ini: ini.append(line)
            procs = [[float(v) for v in l.split()[:2]] for l in ini[2:] if l.strip() and not l.strip().startswith("<")]
            xs = [sum(p[0] for p in procs), math.sqrt(sum(p[1]**2 for p in procs))]
        py = re.findall(r"([0-9.]+e[-+]\d+)", J["pythia_sum_line"])
        X.setdefault(s["name"], {})["test"] = dict(json=j, n_lhe=J["n_lhe"], n_delphes=J["n_delphes"], lhe_sigma_fb=1e3 * xs[0],
                                                   lhe_err_fb=1e3 * xs[1], py8_sigma_fb=(1e12 * float(py[-2]) if len(py) >= 2 else None),
                                                   py8_err_fb=(1e12 * float(py[-1]) if len(py) >= 2 else None))
sig = lambda n: (X[n]["sigma_fb"], X[n]["err_fb"]) if n in X and "sigma_fb" in X[n] else None

# ---- closures ----
GW, GLNU = 2.0476, 0.22756407993  # param-card W width; tree Gamma(W->l nu), massless l (01 report §4)
MW, MTA = 80.419002, 1.777
GTAU = GLNU * (1 - MTA**2 / MW**2)**2 * (1 + MTA**2 / (2 * MW**2))
C = {}
def ratio(a, b, expect, name):
    A, B = sig(a), sig(b)
    if not (A and B): return
    r = A[0] / B[0]; e = r * math.hypot(A[1] / A[0], B[1] / B[0])
    C[name] = dict(num=a, den=b, ratio=r, err=e, expected=expect, pull=(r - expect) / e if expect else None)
ratio("S_EW_WHjj", "S_EW_WHjj_nodec", 2 * GLNU / GW, "BR closure EW: sigma(W->e/mu nu)/sigma(undecayed) vs 2*G_lnu/G_W")
ratio("H_QCD_WHjj", "H_QCD_WHjj_nodec", 2 * GLNU / GW, "BR closure QCD: same")
ratio("S_EW_WHjj_taunu", "S_EW_WHjj_nodec", GTAU / GW, "BR closure tau: sigma(W->tau nu)/sigma(undecayed) vs G_taunu/G_W")
ratio("I_WHjj_nodec", "S_EW_WHjj_nodec", None, "interference / EW (undecayed)")
ratio("H_QCD_WHjj_nodec", "S_EW_WHjj_nodec", None, "QCD / EW (undecayed)")
ratio("S_EW_WHjj_offshell", "S_EW_WHjj", None, "off-shell l nu h jj (0,5) / on-shell decay chain")
ratio("S_EW_WHjj_5Fj_nodec", "S_EW_WHjj_nodec", None, "5F-jet EW (incl. resonant tHq) / 4F-jet EW")
ratio("S_EW_WHjj_5Fj_notop_nodec", "S_EW_WHjj_nodec", None, "5F-jet EW, on-shell top removed / 4F-jet EW")
if all(sig(n) for n in ("S_EW_WHjj_nodec", "H_QCD_WHjj_nodec", "I_WHjj_nodec", "C_WHjj_nodec")):
    parts = [sig(n) for n in ("S_EW_WHjj_nodec", "H_QCD_WHjj_nodec", "I_WHjj_nodec")]
    s_ = sum(p[0] for p in parts); e_ = math.sqrt(sum(p[1]**2 for p in parts)); c = sig("C_WHjj_nodec")
    C["order closure: EW+QCD+I vs coherent C"] = dict(sum=s_, err=e_, C=c[0], C_err=c[1], pull=(s_ - c[0]) / math.hypot(e_, c[1]))
if all(sig(n + "_hp") for n in ("S_EW_WHjj_nodec", "H_QCD_WHjj_nodec", "I_WHjj_nodec", "C_WHjj_nodec")):
    parts = [sig(n + "_hp") for n in ("S_EW_WHjj_nodec", "H_QCD_WHjj_nodec", "I_WHjj_nodec")]
    s_ = sum(p[0] for p in parts); e_ = math.sqrt(sum(p[1]**2 for p in parts)); c = sig("C_WHjj_nodec_hp")
    C["order closure (10x events, independent seeds): EW+QCD+I vs C"] = dict(sum=s_, err=e_, C=c[0], C_err=c[1], pull=(s_ - c[0]) / math.hypot(e_, c[1]))
    for a, b in (("S_EW_WHjj_nodec", "EW"), ("C_WHjj_nodec", "C"), ("H_QCD_WHjj_nodec", "QCD"), ("I_WHjj_nodec", "I")):
        A, B = sig(a), sig(a + "_hp")
        C[f"repeat consistency {b}: first pass vs hp"] = dict(first=A[0], first_err=A[1], hp=B[0], hp_err=B[1], pull=(A[0] - B[0]) / math.hypot(A[1], B[1]))
    ratio("S_EW_WHjj", "S_EW_WHjj_nodec_hp", 2 * GLNU / GW, "BR closure EW (hp denominator)")
    ratio("S_EW_WHjj_taunu", "S_EW_WHjj_nodec_hp", GTAU / GW, "BR closure tau (hp denominator)")
    ratio("I_WHjj_nodec_hp", "S_EW_WHjj_nodec_hp", None, "interference / EW (hp)")
    ratio("H_QCD_WHjj_nodec_hp", "S_EW_WHjj_nodec_hp", None, "QCD / EW (hp)")
for n, v in X.items():
    t = v.get("test")
    if t and "sigma_fb" in v and t.get("py8_sigma_fb"):
        C[f"PY8 sigma closure {n}"] = dict(lhe=t["lhe_sigma_fb"], py8=t["py8_sigma_fb"], ratio=t["py8_sigma_fb"] / t["lhe_sigma_fb"],
                                           gridpack=v["sigma_fb"], gp_vs_lhe_pull=(t["lhe_sigma_fb"] - v["sigma_fb"]) / math.hypot(t["lhe_err_fb"], v["err_fb"]))
# ---- N_MC requirement (SPEC_G0 §1.5): N >= max(50k, sigma x BR x 3000 fb^-1) ----
N = {}
for s in MC.S:
    if s["role"] in ("validation", "interference", "bound", "systematic") or not sig(s["name"]): continue
    k = 1.0
    for f in s["br"]: k *= MC.BRF[f]
    sb = sig(s["name"])[0] * k
    N[s["name"]] = dict(sigma_fb=sig(s["name"])[0], k=k, sigmaBR_fb=sb, N_req=max(50000, math.ceil(sb * 3000)), role=s["role"])
json.dump(dict(xsec=X, closures=C, nmc=N, brf=MC.BRF), open(f"{WH}/work/p03/xsec.json", "w"), indent=1)

print("| sample | role | sigma [fb] | MC err [fb] | rc | wall s x cores | source |\n|---|---|---|---|---|---|---|")
for s in MC.S:
    v = X.get(s["name"])
    if not v or "sigma_fb" not in v:
        print(f"| {s['name']} | {s['role']} | — | — | {v.get('rc') if v else 'pending'} | | |"); continue
    print(f"| {s['name']} | {s['role']} | {v['sigma_fb']:.5g} | {v['err_fb']:.2g} | {v['rc']} | {v['wall_s']}x{v['ncore'] or 4} | `{os.path.relpath(v['src'], WH)}` |")
print("\n| closure | value |\n|---|---|")
for k, v in C.items():
    print(f"| {k} | " + ", ".join(f"{a}={b:.5g}" if isinstance(b, float) else f"{a}={b}" for a, b in v.items()) + " |")
print("\n| sample | sigma x BR [fb] | N_req = max(50k, sigma*BR*3000) |\n|---|---|---|")
for k, v in N.items(): print(f"| {k} | {v['sigmaBR_fb']:.4g} | {v['N_req']:,} |")
