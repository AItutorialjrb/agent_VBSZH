#!/usr/bin/env python3
"""Builds p2/combination/VH_combination.json/.csv from the JOINT-likelihood results (supersedes comb_lambda.py, the v2.1 additive-q combination): work/stat/vh_z0mu_*_v12.json (pyhf joint workspace) and couplings_vh*_v12.json (joint reduced-model templates)."""
import json, csv, os
S = "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh/work/stat"; CB = "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/combination"; J = lambda p: json.load(open(p)) if os.path.exists(p) else None
out = dict(source="joint pyhf workspace (vh_ws/VH_workspace.json) and joint coupling templates; written by wh/scripts/make_vh_json.py", mu95_Z0={}, lambda_={})
for l in (500, 1000, 3000):
    for d in "ab":
        w, z, b = (J(f"{S}/vh_z0mu_{l}_{d}_{k}_v12.json") for k in ("wh", "zh", "both"))
        if w and z and b: out["mu95_Z0"][f"{l}_{d}"] = dict(WH_Z0=w["Z0"], WH_mu95=w["mu95"], ZH_Z0=z["Z0"], ZH_mu95=z["mu95"], combined_Z0=b["Z0"], combined_mu95=b["mu95"], ZH_alone_table=dict(fit_Z_syst=z["Z0"], fit_mu95_syst=z["mu95"][1]), zh_variant="corrected (zh_channel_inputs.json)")
    for mode, tag in (("convention_kZneg_primary", "_kzneg"), ("convention_kWneg", "")):
        c = J(f"{S}/couplings_vh{tag}{'' if l == 500 else '_L%d' % l}_v12.json")
        if c: cv = c["curves"]; out["lambda_"][f"{l}_{mode}"] = dict(Z_lambda_m1=dict(WH=cv["WH"]["Z_lambda_m1"], ZH=cv["ZH"]["Z_lambda_m1"], combined=cv["VH"]["Z_lambda_m1"]), Z_lambda_neg_region=dict(WH=cv["WH"]["Z_lambda_neg"], ZH=cv["ZH"]["Z_lambda_neg"], combined=cv["VH"]["Z_lambda_neg"]), lam=cv["VH"]["lam"], q_WH=cv["WH"]["q"], q_ZH=cv["ZH"]["q"], q_comb=cv["VH"]["q"])
json.dump(out, open(f"{CB}/VH_combination.json", "w"), indent=1)
with open(f"{CB}/VH_combination_mu95.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["lumi_fb", "signal_def", "WH_Z0", "WH_mu95_median", "ZH_Z0", "ZH_mu95_median", "VH_Z0", "VH_mu95_median", "VH_mu95_-1s", "VH_mu95_+1s"])
    for k, v in out["mu95_Z0"].items(): l, d = k.split("_"); w.writerow([l, d, round(v["WH_Z0"], 4), round(v["WH_mu95"][1], 3), round(v["ZH_Z0"], 4), round(v["ZH_mu95"][1], 2), round(v["combined_Z0"], 4), round(v["combined_mu95"][1], 3), round(v["combined_mu95"][0], 3), round(v["combined_mu95"][2], 3)])
with open(f"{CB}/VH_combination_lambda.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["lumi_fb", "mode", "Z_lambda_-1_WH", "Z_lambda_-1_ZH", "Z_lambda_-1_VH", "Z_lambda<0_WH", "Z_lambda<0_ZH", "Z_lambda<0_VH"])
    for k, v in out["lambda_"].items(): l, m = k.split("_", 1); a, b = v["Z_lambda_m1"], v["Z_lambda_neg_region"]; w.writerow([l, m] + [round(a[x], 3) for x in ("WH", "ZH", "combined")] + [round(b[x], 3) for x in ("WH", "ZH", "combined")])
print(open(f"{CB}/VH_combination_mu95.csv").read()[:600])
