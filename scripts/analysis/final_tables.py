#!/usr/bin/env python3
"""Render the FINAL report tables (markdown) from final_analysis.py JSON. No physics here.
Usage: python3 -P final_tables.py <final.json> > tables.md"""
import sys, json
d = json.load(open(sys.argv[1])); R, REG, F = d["results"], d["registry"], d["fit"]
g = lambda x, n=3: "%.*g" % (n, x)
lab = {"a": "(a) EW ZHjj; QCD ZHjj in b", "b": "(b) EW+QCD ZHjj"}
print("### Table R1 - PRIMARY: Eq. 1 counting significance (stat. only, +- MC stat), 13.6 TeV\n")
print("| L [fb^-1] | signal def. | s +- MC | b +- MC | Z_Eq1 +- MC | Z_syst (counting, sigma_b) | mu95 CLs (exact Poisson, syst) | median n_obs (b-only) |")
print("|---|---|---|---|---|---|---|---|")
for k, v in R.items():
    print(f"| {int(v['L'])} | {lab[v['sigdef']]} | {v['s']:.3f} +- {v['s_mc']:.3f} | {v['b']:.3f} +- {v['b_mc']:.3f} | {v['Z_eq1']:.3f} +- {v['Z_eq1_mcerr']:.3f} | {v['Z_syst_counting']:.3f} | {v['mu95_cls']:.1f} | {v['n_median']} |")
print("\n### Table R2 - SUPPLEMENTARY: binned profile-likelihood fit in m_gg (window + sidebands, Asimov, asymptotic)\n")
print("| L [fb^-1] | signal def. | Z (fit, stat only) | Z_syst (fit) | mu95 (fit, stat only) | mu95 (fit, syst) |")
print("|---|---|---|---|---|---|")
for k, v in F.items():
    L, sd = k.split("_"); print(f"| {L} | {lab[sd]} | {v['Z_stat']:.3f} | {v['Z_syst']:.3f} | {v['mu95_stat']:.1f} | {v['mu95_syst']:.1f} |")
for tag, key in (("optimum", "cutflow"), ("reference-like baseline", "cutflow_baseline")):
    cf = d[key]; cols = [c for c in cf[0] if c != "step"]
    print(f"\n### Table III-like - cutflow at the {tag}, 500 fb^-1: expected events (raw MC events)\n")
    print("| step | " + " | ".join(cols) + " |"); print("|---" * (len(cols) + 1) + "|")
    for row in cf: print(f"| {row['step']} | " + " | ".join(f"{g(row[c]['y'])} ({row[c]['raw']})" for c in cols) + " |")
print("\n### Table IV-like - per-process expected yields at the optimum (events), MC-stat, raw MC support, method\n")
print("| process | role | sigma [fb] | x BR | N_MC | w_evt @500 | yield 500 | yield 1000 | yield 3000 | MC-stat @500 | raw in window | raw 105-165 | method |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for k, c in R["500_a"]["comp"].items():
    r = REG[k]; role = {"sig": "signal", "qcdzh": "bkg (a) / signal (b)"}.get(r["role"], "background")
    y3 = R["3000_a"]["comp"][k]["y"]
    print(f"| {k} | {role} | {g(r['sig'], 4)} | {g(r['k'], 4)} | {r['N']} | {g(c['w_evt'])} | {c['y']:.4f} | {2*c['y']:.4f} | {y3:.4f} | {c['mcstat']:.4f} | {c['raw_win']} | {c['raw_wide']} | {c['method']} |")
print("\n### Robustness at 500 fb^-1, definition (a)\n")
print("| variation | s | b | Z_Eq1 | Z_syst |"); print("|---|---|---|---|---|")
for k, v in d["robustness"].items(): print(f"| {k} | {v['s']:.3f} | {v['b']:.3f} | {v['Z_eq1']:.3f} | {v['Z_syst']:.3f} |")
print("\n### Reference-like baseline results\n")
print("| L | def | s | b | Z_Eq1 +- MC | mu95 |"); print("|---|---|---|---|---|---|")
for k, v in d["results_baseline"].items(): print(f"| {int(v['L'])} | {v['sigdef']} | {v['s']:.3f} | {v['b']:.3f} | {v['Z_eq1']:.3f} +- {v['Z_eq1_mcerr']:.3f} | {v['mu95_cls']:.1f} |")
if d.get("ff_xcheck"):
    print("\n### Fake-factor cross-check on Delphes jets (QCD Zg+jets, 500 fb^-1)\n")
    print("| estimate | final selection | optimum without VBS-jet cuts |"); print("|---|---|---|")
    for k, v in d["ff_xcheck"].items(): print(f"| {k} | {v['final']:.4f} | {v['noVBS']:.4f} |")
sc = d["scan"]
for L in ("500", "3000"):
    mj = sorted({float(k.split('|')[1].split(',')[0]) for k in sc}); de = sorted({float(k.split(',')[1]) for k in sc})
    print(f"\n### Joint mjj x |deta_jj| scan, Z_Eq1 (def. a), {L} fb^-1\n")
    print("| mjj \\ deta | " + " | ".join(f">{x:.1f}" for x in de) + " |"); print("|---" * (len(de) + 1) + "|")
    for a in mj: print(f"| >{a:.0f} | " + " | ".join(f"{sc[f'{L}|{a:.0f},{b:.1f}']['Z']:.3f}" for b in de) + " |")
