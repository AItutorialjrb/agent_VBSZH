#!/usr/bin/env python3
"""Render the markdown tables of reports/05_pilot_sensitivity.md from the sensitivity JSON (no physics here).
Usage: python3 -P tables05.py <sens.json> > tables.md"""
import sys, json
d = json.load(open(sys.argv[1]))
R = d["results"]; REG = d["registry"]
f = lambda x, n=3: ("%.*g" % (n, x)) if isinstance(x, (int, float)) else str(x)
print("### T1 — Expected results (13.6 TeV; 3000 fb^-1 = luminosity scaling only, not HL-LHC)\n")
print("| L [fb^-1] | signal def. | s | b | sigma_b (syst+MC) | b MC-stat | Z_stat (Eq. 1) | Z_syst | median n_obs (b-only) | mu_95 (CLs, syst) | mu_95 (CLs, stat) |")
print("|---|---|---|---|---|---|---|---|---|---|---|")
for k, v in R.items():
    lab = "(a) EW ZHjj; QCD ZHjj in b" if v["sigdef"] == "a" else "(b) EW+QCD ZHjj"
    print(f"| {int(v['L'])} | {lab} | {v['s']:.3f} | {v['b']:.3f} | {v['sigma_b']:.3f} | {v['b_mcstat']:.3f} | {v['Z_stat']:.3f} | {v['Z_syst']:.3f} | {v['n_median']} | {v['mu95']:.1f} | {v['mu95_statonly']:.1f} |")
print("\n### T2 — Per-process expected yield at the optimum, 500 fb^-1 (events), with raw MC support and method\n")
print("| process | role | sigma used [fb] | x BR | yield | MC-stat | raw MC events | method | source |")
print("|---|---|---|---|---|---|---|---|---|")
for k, v in R["500_a"]["comp"].items():
    r = REG[k]; role = "signal" if k == "S_EW_ZHjj" else ("bkg (a) / signal (b)" if k == "H_QCD_ZHjj" else ("order-of-magnitude only (not in b)" if r.get("oom") else ("cross-check only (not in b)" if r.get("xcheck") else "background")))
    sig = r.get("sig") if r.get("sig") is not None else v.get("sigma_fb")
    kf = r.get("k", 1.0)
    print(f"| {k} | {role} | {f(sig, 4)} | {f(kf, 4)} | {v['y']:.4f} | {v['mcstat']:.4f} | {v['raw']} | {v['method']} | {r.get('src', '')} |")
print("\n### T3 — Cutflow at the optimum, 500 fb^-1: expected events (raw MC events)\n")
cols = list(d["cutflow"][0].keys())[1:]
print("| step | " + " | ".join(cols) + " |"); print("|---" * (len(cols) + 1) + "|")
for row in d["cutflow"]:
    print(f"| {row['step']} | " + " | ".join(f"{row[c]['y']:.3g} ({row[c]['raw']})" for c in cols) + " |")
print("\nBefore the window, fake-factor rows are sums of f-weighted combinations (raw = distinct MC events); proxy rows are the factorised estimate (raw = min of the two factors).")
print("\n### T4 — Robustness at 500 fb^-1, definition (a)\n")
print("| variation | s | b | Z_stat | Z_syst |"); print("|---|---|---|---|---|")
for k, v in d["robustness"].items():
    print(f"| {k} | {v['s']:.3f} | {v['b']:.3f} | {v['Z_stat']:.3f} | {f(v.get('Z_syst', '—'))} |")
print("\n### T5 — Joint (mjj, |deta_jj|) scan of Z_syst at 500 fb^-1, other cuts at the optimum\n")
sc = d["scan_mjj_deta"]; mj = sorted({float(k.split(',')[0]) for k in sc}); de = sorted({float(k.split(',')[1]) for k in sc})
print("| mjj \\ deta | " + " | ".join(f"{x:.1f}" for x in de) + " |"); print("|---" * (len(de) + 1) + "|")
for a in mj:
    print(f"| >{a:.0f} | " + " | ".join(f"{sc[f'{a:.0f},{b:.1f}']:.3f}" for b in de) + " |")
