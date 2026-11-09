# VH combination (WH final analysis x frozen ZH), D32 item 5 / D37
Date UTC: 2026-11-09 09:01. Status: **PASS for verification**. All numbers are EXPECTED (Asimov), Delphes level, 13.6 TeV, LO, no data. Git commit: see orchestrator commit. Writer: executor-wh (VH files only; ZH_erratum.md belongs to the ZH-erratum executor).
## Inputs
* WH: p2/runs/multi_r1/wh/reports/07_sensitivity.md model (cut-based primary selection, m_gg 100-180 GeV 40-bin shape fit, nuisances of 06, Barlow-Beeston).
* ZH: SWAPPABLE table p2/combination/VH_inputs_zh.json, made by p2/runs/multi_r1/wh/scripts/make_zh_table.py from p2/combination/zh_check/zh_corrected_inputs.json (variant `corrected_nominal` = the D37 corrected fake-photon component; `frozen` (zh-final-v1.1 numbers) and the other variants are selectable with `python3 make_zh_table.py <variant>`; then rerun the six condor tasks comb:<L>:<a|b>, scripts/comb_run.py, and scripts/comb_lambda.py). The ZH channel is one counting bin per process row (y, MC error, nuisance magnitudes of the frozen final.json), signal rows: EW ZHjj (+ H_QCD_ZHjj in definition b). 1000 fb^-1 ZH rows = linear scaling of the 500 fb^-1 components.
## Correlation model (declared)
Shared (one parameter in both channels): luminosity (2.5 %, ASSUMPTION), photon efficiency (4 % for two photons, ASSUMPTION), lepton efficiency (WH 1 %, ZH 2 %, ASSUMPTION), VH signal theory (scale_sig: WH and ZH EW VH, magnitudes of each study), per-process-class theory (scale_prompt_qcd = QCD V gamma gamma, scale_prompt_ew = EW V gamma gamma, scale_hqcd = QCD VH, scale_higgs_other = ggZH/ttH/tHW/other), fake-photon rate (D39 floor 20 %). Not shared: ZH off-shell, Z gamma gamma interference, ggZH normalisation, top theory, the ZH CMS-calibration factor (26 %), per-row MC statistics, all WH-specific nuisances (tau, PS, C, coverage, non-closure, ...). The common signal strength mu multiplies the WH and ZH signals (SM VH ratio).
## Results: signal strength (expected)
| L [fb^-1] | def | WH Z0 | WH PL asymptotic (q~) CLs mu95 (-1s, median, +1s) | VH Z0 | VH PL asymptotic CLs mu95 (-1s, median, +1s) | ZH alone (table, frozen-code PL) Z, mu95 |
|---|---|---|---|---|---|---|
| 500 | a | 0.427 | 4.46, 7.09, 11.58 | 0.444 | 4.13, 6.52, 10.77 | 0.131, 31.8 |
| 500 | b | 0.484 | 3.93, 6.04, 10.23 | 0.522 | 3.59, 5.54, 8.72 | 0.210, 20.3 |
| 1000 | a | 0.592 | 2.91, 4.54, 7.36 | 0.616 | 2.77, 4.16, 6.76 | 0.184, 18.8 |
| 1000 | b | 0.671 | 2.62, 3.97, 6.21 | 0.724 | 2.39, 3.63, 5.65 | 0.295, 11.9 |
| 3000 | a | 0.973 | 1.67, 2.50, 3.83 | 1.014 | 1.59, 2.37, 3.63 | 0.314, 8.8 |
| 3000 | b | 1.103 | 1.44, 2.16, 3.39 | 1.195 | 1.30, 1.91, 2.87 | 0.502, 5.5 |

The ZH channel adds little (its own expected Z0 is 0.13-0.5, mu95 6-32): the combination improves the WH numbers by 4-8 % in Z0 and 5-8 % in mu95. The VH signal strength is defined with respect to the SM WH+ZH ratio.

## Results: lambda_WZ (expected exclusion at the SM point, WH + ZH)
q_VH(lambda) = q_WH + q_ZH (independent channels; WH-ZH nuisance correlations are NOT propagated in this additive approximation; ZH q curves are the FROZEN zh-final-v1.1 curves while the mu95/Z0 rows use the corrected ZH table: the erratum changes ZH b by -10 %, i.e. q_ZH by about +10 %, which changes the combined Z(lambda<0) by < 0.01 sigma (q_ZH is 0.009 against q_WH 0.14 at 500 fb^-1) and Z(lambda=-1) by < 0.05 sigma; not propagated, quantified here). Primary: WH with the analytic H->gamma gamma kappa dependence R_BR and the ZH rate-resolved curve; variant: samples as is (BR fixed to SM) with the ZH fixed-BR curve.

| L | mode | Z(lambda=-1) WH / ZH / VH | Z(lambda<0 region, closest point lambda=0) WH / ZH / VH |
|---|---|---|---|
| 500 | primary_withBR | 6.20 / 0.81 / 6.25 | 0.37 / 0.09 / 0.39 |
| 500 | variant_noBR | 3.76 / 0.43 / 3.79 | 1.61 / 0.13 / 1.61 |
| 1000 | primary_withBR | 8.60 / 1.15 / 8.67 | 0.51 / 0.13 / 0.53 |
| 1000 | variant_noBR | 5.28 / 0.61 / 5.31 | 2.27 / 0.18 / 2.27 |
| 3000 | primary_withBR | 13.96 / 1.98 / 14.10 | 0.83 / 0.22 / 0.87 |
| 3000 | variant_noBR | 8.85 / 1.05 / 8.92 | 3.89 / 0.31 / 3.90 |

Interpretation (expected sensitivity, not a result): lambda_WZ = -1 is excluded at a high expected level mainly through the WH channel (rate and high-pT / mT shapes, plus the H->gamma gamma rate); the whole negative range is limited by its boundary point lambda about 0, where (with R_BR) the H->gamma gamma amplitude cancels and the signal vanishes. The ZH curve adds a minor contribution.
## Caveats
Expected only; additive-q approximation for lambda_WZ; ZH inputs: counting channel per row, no m_gg shape; ASSUMPTION nuisances (lumi, efficiencies); 13.6 TeV LO Delphes samples; the WH v1.1 row F_QCD_llajj_loose is included, H_ggF_jj is not yet; ZH_erratum numbers may be updated: the ZH table is swappable (above). Files: VH_combination.json, VH_combination_mu95.csv, VH_combination_lambda.csv.
