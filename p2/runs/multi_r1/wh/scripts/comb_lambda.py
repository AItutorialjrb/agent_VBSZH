#!/usr/bin/env python3
"""Combined lambda_WZ exclusion (WH + ZH) and the VH combination tables. q_VH(lambda) = q_WH(lambda) + q_ZH(lambda) (independent channels, Gaussian/asymptotic additivity of the expected q at the SM point; nuisance correlations between WH and ZH are NOT propagated here (they are in the mu95/Z0 pyhf combination); stated approximation).
WH primary: with R_BR (analytic H->gamma gamma kappa dependence), paired with the ZH 'resolved' (rate-resolved kappa_W) curve; variant: samples as is (no R_BR) paired with ZH 'fixed' (BR fixed to SM). ZH curves: frozen final.json['coupling'] (read-only; the fake-photon erratum changes ZH b by <10 %, not propagated: stated).
Outputs: p2/combination/VH_combination.json, VH_combination_mu95.csv, VH_combination_lambda.csv."""
import json, csv, os, numpy as np
WH = "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh"; CB = "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/combination"
F = json.load(open("/eos/home-r/rjiang/vbs_zh_codex_starter/work/final_ntuples/final.json"))["coupling"]; out = dict(mu95_Z0={}, lambda_={})
for l in (500, 1000, 3000):
    for d in ("a", "b"):
        c = json.load(open(f"{WH}/work/stat/comb_{l}_{d}_v11.json" if os.path.exists(f"{WH}/work/stat/comb_{l}_{d}_v11.json") else f"{WH}/work/stat/comb_{l}_{d}.json")); out["mu95_Z0"][f"{l}_{d}"] = dict(WH_Z0=c["WH"]["Z0"], WH_mu95=c["WH"]["mu95"], combined_Z0=c["combined"]["Z0"], combined_mu95=c["combined"]["mu95"], ZH_alone_table=c["ZH_alone_table"], zh_variant=c["zh_variant"])
    tag = "" if l == 500 else f"_L{l}"
    for mode, wtag, zk in (("primary_withBR", "", "resolved"), ("variant_noBR", "_nobr", "fixed")):
        w = json.load(open(f"{WH}/work/stat/couplings{wtag}{tag}_v11.json" if os.path.exists(f"{WH}/work/stat/couplings{wtag}{tag}_v11.json") else f"{WH}/work/stat/couplings{wtag}{tag}.json"))["expected_exclusion"]["reduced_model"]["q"]; lam = np.array(sorted(float(x) for x in w)); qw = np.array([w[str(float(x))] if str(float(x)) in w else w[repr(float(x))] for x in lam])
        z = F[f"lambda|{l}|{zk}"]; qz = np.interp(lam, z["lam"], z["q"]); qc = qw+qz; neg = lam <= 0
        out["lambda_"][f"{l}_{mode}"] = dict(Z_lambda_m1=dict(WH=float(np.sqrt(np.interp(-1.0, lam, qw))), ZH=float(np.sqrt(np.interp(-1.0, lam, qz))), combined=float(np.sqrt(np.interp(-1.0, lam, qc)))),
            Z_lambda_neg_region=dict(WH=float(np.sqrt(qw[neg].min())), ZH=float(np.sqrt(qz[neg].min())), combined=float(np.sqrt(qc[neg].min())), lambda_at_min_combined=float(lam[neg][qc[neg].argmin()])), lam=lam.tolist(), q_WH=qw.tolist(), q_ZH=qz.tolist(), q_comb=qc.tolist())
json.dump(out, open(f"{CB}/VH_combination.json", "w"), indent=1)
with open(f"{CB}/VH_combination_mu95.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["lumi_fb", "signal_def", "WH_Z0", "WH_mu95_median", "WH_mu95_-1s", "WH_mu95_+1s", "VH_Z0", "VH_mu95_median", "VH_mu95_-1s", "VH_mu95_+1s", "ZH_alone_fit_Z", "ZH_alone_fit_mu95", "zh_variant"])
    for k, v in out["mu95_Z0"].items():
        l, d = k.split("_"); w.writerow([l, d, round(v["WH_Z0"], 4), *[round(v["WH_mu95"][i], 3) for i in (1, 0, 2)], round(v["combined_Z0"], 4), *[round(v["combined_mu95"][i], 3) for i in (1, 0, 2)], round(v["ZH_alone_table"]["fit_Z_syst"], 4), round(v["ZH_alone_table"]["fit_mu95_syst"], 2), v["zh_variant"]])
with open(f"{CB}/VH_combination_lambda.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["lumi_fb", "mode", "Z_lambda_-1_WH", "Z_lambda_-1_ZH", "Z_lambda_-1_VH", "Z_lambda<0_WH", "Z_lambda<0_ZH", "Z_lambda<0_VH", "lambda_at_min"])
    for k, v in out["lambda_"].items():
        l, m = k.split("_", 1); a, b = v["Z_lambda_m1"], v["Z_lambda_neg_region"]; w.writerow([l, m, round(a["WH"], 3), round(a["ZH"], 3), round(a["combined"], 3), round(b["WH"], 3), round(b["ZH"], 3), round(b["combined"], 3), b["lambda_at_min_combined"]])
print(open(f"{CB}/VH_combination_lambda.csv").read()); print(open(f"{CB}/VH_combination_mu95.csv").read())
