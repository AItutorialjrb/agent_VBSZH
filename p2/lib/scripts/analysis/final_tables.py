#!/usr/bin/env python3
"""Render the FINAL report tables (markdown) from final_analysis.py JSON. No physics here.
Usage: python3 -P final_tables.py <final.json> > tables.md"""
import sys, json, numpy as np
d = json.load(open(sys.argv[1])); R, REG, F = d["results"], d["registry"], d["fit"]
g = lambda x, n=3: "%.*g" % (n, x)
lab = {"a": "(a) EW ZHjj; QCD ZHjj in b", "b": "(b) EW+QCD ZHjj"}
print("### Table R1 - PRIMARY: Eq. 1 counting significance (stat. only, +- MC stat), 13.6 TeV\n")
print("| L [fb^-1] | signal def. | s +- MC | b +- MC | sigma_b (incl. theory) | Z_Eq1 +- MC | Z_syst (counting, incl. theory) | Z_syst (no theory) | mu95 CLs (syst incl. theory) | mu95 (no theory) | mu95 (stat only) | median n_obs (b-only) |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|")
for k, v in R.items():
    print(f"| {int(v['L'])} | {lab[v['sigdef']]} | {v['s']:.3f} +- {v['s_mc']:.3f} | {v['b']:.3f} +- {v['b_mc']:.3f} | {v['sigma_b']:.3f} | {v['Z_eq1']:.3f} +- {v['Z_eq1_mcerr']:.3f} | {v['Z_syst_counting']:.3f} | {v['Z_syst_counting_notheory']:.3f} | {v['mu95_cls']:.1f} | {v['mu95_cls_notheory']:.1f} | {v['mu95_cls_stat']:.1f} | {v['n_median']} |")
print("\n### Table R2 - SUPPLEMENTARY: binned profile-likelihood fit in m_gg (window + sidebands, Asimov, asymptotic)\n")
print("| L [fb^-1] | signal def. | Z (fit, stat only) | Z_syst (fit) | mu95 (fit, stat only) | mu95 (fit, syst) |")
print("|---|---|---|---|---|---|")
for k, v in F.items():
    L, sd = k.split("_"); print(f"| {L} | {lab[sd]} | {v['Z_stat']:.3f} | {v['Z_syst']:.3f} | {v['mu95_stat']:.1f} | {v['mu95_syst']:.1f} |")
for tag, key in (("optimum", "cutflow"), ("reference-like baseline", "cutflow_baseline")):
    cf = d[key]; cols = [c for c in cf[0] if c != "step"]
    print(f"\n### Table III-like - cutflow at the {tag}" + (" (photon pT > 25 GeV; the reference uses 20 GeV)" if "baseline" in tag else "") + ", 500 fb^-1: expected events (raw MC events)\n")
    print("| step | " + " | ".join(cols) + " |"); print("|---" * (len(cols) + 1) + "|")
    for row in cf: print(f"| {row['step']} | " + " | ".join(f"{g(row[c]['y'])} ({row[c]['raw']})" for c in cols) + " |")
print("\n### Table IV-like - per-process expected yields at the optimum (events), MC-stat, raw MC support, method\n")
print("| process | role | sigma [fb] | x BR | N_MC | w_evt @500 | yield 500 | yield 1000 | yield 3000 | MC-stat @500 | raw in window | raw 105-165 | method |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for k, c in R["500_a"]["comp"].items():
    r = REG[k]; role = {"sig": "signal", "qcdzh": "bkg (a) / signal (b)"}.get(r["role"], "background")
    y3 = R["3000_a"]["comp"][k]["y"]
    print(f"| {k} | {role} | {g(r['sig'], 4)} | {g(r['k'], 4)} | {r['N']} | {g(c['w_evt'])} | {c['y']:.4f} | {2*c['y']:.4f} | {y3:.4f} | {c['mcstat']:.4f} | {c['raw_win']} | {c['raw_wide']} | {c['method']} |")
print("\n### Robustness at 500 fb^-1, definition (a) (all rows include the theory nuisances unless stated)\n")
print("| variation | s | b | Z_Eq1 | Z_syst | mu95 CLs |"); print("|---|---|---|---|---|---|")
for k, v in d["robustness"].items(): print(f"| {k} | {v['s']:.3f} | {v['b']:.3f} | {v['Z_eq1']:.3f} | {v['Z_syst']:.3f} | {v['mu95']:.1f} |")
ce = d.get("cms_eff", {}).get("results")
if ce:
    print("\n### CMS-like object-efficiency variation (A7), all luminosities\n")
    print("| L | def | s | b | Z_Eq1 | Z_syst | mu95 CLs |"); print("|---|---|---|---|---|---|---|")
    for k, v in ce.items(): L, sd = k.split("_"); print(f"| {L} | {sd} | {v['s']:.3f} | {v['b']:.3f} | {v['Z_eq1']:.3f} | {v['Z_syst']:.3f} | {v['mu95']:.1f} |")
print("\n### Uncertainty budget on b at 500 fb^-1, def. (a): correlated groups (events, summed linearly over processes)\n")
gb = R["500_a"]["groups_b"]; print("| group | delta b [events] | delta b / b |"); print("|---|---|---|")
for g_, v in sorted(gb.items(), key=lambda x: -x[1]): print(f"| {g_} | {v:.4f} | {100*v/R['500_a']['b']:.1f} % |")
print(f"| per-process normalisation (+) MC stat (uncorrelated) | {np.sqrt(max(R['500_a']['sigma_b']**2 - sum(v**2 for v in gb.values()), 0)):.4f} | |")
print(f"| **total sigma_b** | {R['500_a']['sigma_b']:.4f} | {100*R['500_a']['sigma_b']/R['500_a']['b']:.1f} % |")
print("\n### Reference-like baseline results (photon pT > 25 GeV instead of the reference's 20 GeV)\n")
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
