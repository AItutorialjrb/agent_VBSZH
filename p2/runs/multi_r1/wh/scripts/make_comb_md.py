#!/usr/bin/env python3
import json, datetime
CB = "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/combination"; d = json.load(open(f"{CB}/VH_combination.json")); now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M"); L = []; a = L.append
a(f"""# VH combination (WH final analysis x frozen ZH), D32 item 5 / D37
Date UTC: {now}. Status: **PASS for verification**. All numbers are EXPECTED (Asimov), Delphes level, 13.6 TeV, LO, no data. Git commit: see orchestrator commit. Writer: executor-wh (VH files only; ZH_erratum.md belongs to the ZH-erratum executor).
## Inputs
* WH: p2/runs/multi_r1/wh/reports/07_sensitivity.md model (cut-based primary selection, m_gg 100-180 GeV 40-bin shape fit, nuisances of 06, Barlow-Beeston).
* ZH: SWAPPABLE table p2/combination/VH_inputs_zh.json, made by p2/runs/multi_r1/wh/scripts/make_zh_table.py from p2/combination/zh_check/zh_corrected_inputs.json (variant `corrected_nominal` = the D37 corrected fake-photon component; `frozen` (zh-final-v1.1 numbers) and the other variants are selectable with `python3 make_zh_table.py <variant>`; then rerun the six condor tasks comb:<L>:<a|b>, scripts/comb_run.py, and scripts/comb_lambda.py). The ZH channel is one counting bin per process row (y, MC error, nuisance magnitudes of the frozen final.json), signal rows: EW ZHjj (+ H_QCD_ZHjj in definition b). 1000 fb^-1 ZH rows = linear scaling of the 500 fb^-1 components.
## Correlation model (declared)
Shared (one parameter in both channels): luminosity (2.5 %, ASSUMPTION), photon efficiency (4 % for two photons, ASSUMPTION), lepton efficiency (WH 1 %, ZH 2 %, ASSUMPTION), VH signal theory (scale_sig: WH and ZH EW VH, magnitudes of each study), per-process-class theory (scale_prompt_qcd = QCD V gamma gamma, scale_prompt_ew = EW V gamma gamma, scale_hqcd = QCD VH, scale_higgs_other = ggZH/ttH/tHW/other), fake-photon rate (D39 floor 20 %). Not shared: ZH off-shell, Z gamma gamma interference, ggZH normalisation, top theory, the ZH CMS-calibration factor (26 %), per-row MC statistics, all WH-specific nuisances (tau, PS, C, coverage, non-closure, ...). The common signal strength mu multiplies the WH and ZH signals (SM VH ratio).
## Results: signal strength (expected)
| L [fb^-1] | def | WH Z0 | WH PL asymptotic (q~) CLs mu95 (-1s, median, +1s) | VH Z0 | VH PL asymptotic CLs mu95 (-1s, median, +1s) | ZH alone (table, frozen-code PL) Z, mu95 |
|---|---|---|---|---|---|---|""")
for k, v in d["mu95_Z0"].items():
    l, df = k.split("_"); m = v["WH_mu95"]; c = v["combined_mu95"]; z = v["ZH_alone_table"]
    a(f"| {l} | {df} | {v['WH_Z0']:.3f} | {m[0]:.2f}, {m[1]:.2f}, {m[2]:.2f} | {v['combined_Z0']:.3f} | {c[0]:.2f}, {c[1]:.2f}, {c[2]:.2f} | {z['fit_Z_syst']:.3f}, {z['fit_mu95_syst']:.1f} |")
a("\nThe ZH channel adds little (its own expected Z0 is 0.13-0.5, mu95 6-32): the combination improves the WH numbers by 4-8 % in Z0 and 5-8 % in mu95. The VH signal strength is defined with respect to the SM WH+ZH ratio.")
a("\n## Results: lambda_WZ (expected exclusion at the SM point, WH + ZH)\nq_VH(lambda) = q_WH + q_ZH (independent channels; WH-ZH nuisance correlations are NOT propagated in this additive approximation; ZH q curves are the FROZEN zh-final-v1.1 curves while the mu95/Z0 rows use the corrected ZH table: the erratum changes ZH b by -10 %, i.e. q_ZH by about +10 %, which changes the combined Z(lambda<0) by < 0.01 sigma (q_ZH is 0.009 against q_WH 0.14 at 500 fb^-1) and Z(lambda=-1) by < 0.05 sigma; not propagated, quantified here). Primary: WH with the analytic H->gamma gamma kappa dependence R_BR and the ZH rate-resolved curve; variant: samples as is (BR fixed to SM) with the ZH fixed-BR curve.\n\n| L | mode | Z(lambda=-1) WH / ZH / VH | Z(lambda<0 region, closest point lambda=0) WH / ZH / VH |\n|---|---|---|---|")
for k, v in d["lambda_"].items():
    l, m = k.split("_", 1); x = v["Z_lambda_m1"]; y = v["Z_lambda_neg_region"]
    a(f"| {l} | {m} | {x['WH']:.2f} / {x['ZH']:.2f} / {x['combined']:.2f} | {y['WH']:.2f} / {y['ZH']:.2f} / {y['combined']:.2f} |")
a("""
Interpretation (expected sensitivity, not a result): lambda_WZ = -1 is excluded at a high expected level mainly through the WH channel (rate and high-pT / mT shapes, plus the H->gamma gamma rate); the whole negative range is limited by its boundary point lambda about 0, where (with R_BR) the H->gamma gamma amplitude cancels and the signal vanishes. The ZH curve adds a minor contribution.
## Caveats
Expected only; additive-q approximation for lambda_WZ; ZH inputs: counting channel per row, no m_gg shape; ASSUMPTION nuisances (lumi, efficiencies); 13.6 TeV LO Delphes samples; the WH v1.1 row F_QCD_llajj_loose is included, H_ggF_jj is not yet; ZH_erratum numbers may be updated: the ZH table is swappable (above). Files: VH_combination.json, VH_combination_mu95.csv, VH_combination_lambda.csv.
""")
open(f"{CB}/VH_combination.md", "w").write("\n".join(L)); print("ok")
