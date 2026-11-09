#!/usr/bin/env python3
"""single_r1 WH: pilot event counts at 500 fb^-1 (illustrative baseline, NOT yields) from work/p03/{delphes_validation,egamma_pilot}.json.
External BR factor applied once per sample from the registry (make_cards.BRF). Usage: python3 -P wh/scripts/bounds_table.py"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_cards as MC
WH = MC.WH; L = 500.0
D = json.load(open(f"{WH}/work/p03/delphes_validation.json")); E = json.load(open(f"{WH}/work/p03/egamma_pilot.json"))
K = {}
for s in MC.S:
    k = 1.0
    for f in s["br"]: k *= MC.BRF[f]
    K[s["name"]] = k
K.update({"F_QCD_llajj_vbs": 1.0, "F_EW_llajj_vbs": 1.0})   # frozen ZH: off-shell ll in ME, no BR factor
print("| component | path / scenario | ext. BR | fit range 105–160, after b-veto: events @ 500 fb⁻¹ (MC ev) | + 120<m_γγ<130 (MC ev) |\n|---|---|---|---|---|")
rows = [(n, k[8:], R[k]) for n, R in D.items() for k in R if k.startswith("cutflow")] + \
       [(n + " (frozen ZH)" if n != "T_tta_1l" else n, f"e→γ {sc}", E[n][sc]) for n in ("F_QCD_llajj_vbs", "F_EW_llajj_vbs", "T_tta_1l") for sc in ("low", "nom", "high")]
for n, path, cf in rows:
    k = K[n.split(" ")[0]]; a, b = cf[7], cf[8]
    print(f"| {n} | {path} | {k:.4g} | {a['sigma_fb']*k*L:.3g} ± {a['err_fb']*k*L:.2g} ({a['n_mc']}) | {b['sigma_fb']*k*L:.3g} ± {b['err_fb']*k*L:.2g} ({b['n_mc']}) |")
