# VH combination: joint WH + ZH likelihood (D47 (1))
Date UTC: 2026-11-16 05:17. Analysis commit: ORCH_COMMIT_PLACEHOLDER. Status: **PASS for verification**. All numbers EXPECTED (Asimov SM data), Delphes level, 13.6 TeV, LO. Writer: executor-wh (ZH channel inputs: ZH-erratum executor, vh_ws/zh_channel_inputs.json, corrected fake-photon rows).
## Model
ONE pyhf workspace (committed: p2/combination/vh_ws/VH_workspace.json = common mu_VH, definition (a); VH_workspace_2d.json = (mu_WH, mu_ZH); *_defb.json for definition (b); WH_workspace.json and ZH_workspace.json = the single-channel versions built by the same code, scripts/vh_build.py; observations = SM Asimov data at 500 fb^-1, luminosity scaling is linear). WH channel: m_gg 100-180 GeV in 40 bins, cut-based primary selection, all WH nuisances, Barlow-Beeston-lite per bin. ZH channel: m_gg 105-165 GeV in 30 bins, 15 process samples with per-bin templates, per-bin MC statistics, systematics (zh_channel_inputs.json).
**Signal-like cross-feed samples (not fixed backgrounds):** the EW ZHjj lost-lepton rows in the WH SR (workspace sample zhjj_ew = ZH_EW_ZHjj_lostlep, 200k frozen events; zhjj_qcd in definition (b)) are scaled by the ZH signal strength (mu_ZH in the 2D fit, the common mu otherwise) and carry the ZH theory nuisances. Yield at 500 fb^-1 with the region and window stated (scripts/xfeed.py, work/stat/xfeed_v12.json): in the workspace (cut-based SR, m_gg 100-180 GeV, 40 bins) **0.0184** events; in the bins 122-128 GeV 0.0151; in 120-130 GeV (= +-2 sigma_eff = +-4.2 GeV bins) 0.0178; unbinned |m_gg-125|<3.5 GeV from the table 0.0162; the coupling-fit template (K_EW_ZHjj_lam_p100, the HC SM point, 50k events) in the +-3.5 GeV window and the four mT(W gg) bins 0.0159 (a different sample from the workspace row: the earlier quoted 0.0159 is this number). WH signal: workspace 100-180 0.6799, bins 120-130 0.6625, unbinned +-3.5 GeV 0.6123 (the +-4.2 GeV and +-3.5 GeV windows differ by 0.002 events: window-edge convention). (v1.2 bug fixed during verification: the ZHjj rows had been smoothed as non-resonant; they are now kept raw like the signal.) The WH signal in the ZH SR has ZERO MC support (0 raw events of 300k): UL95 4.65e-4 events, not in the fit (it would carry mu_WH). In the coupling fits both cross-feeds follow their own (kappa_W, kappa_Z) quadratic forms (ZHjj in the WH SR from the frozen K_EW_ZHjj samples).
**Orthogonality:** overlap 0 raw / 0 weighted over 47 samples (vh_ws/orthogonality.json); the SRs are exclusive by construction (ZH: two leptons pT>15; WH: exactly one lepton pT>10).
## Correlation scheme (vh_ws/correlation_scheme.json)
Correlated (one parameter in both channels): lumi, pheff, lepeff, phscale, phres (histosys on the real-photon EW signal samples), scale_sig and pdf_sig (EW VH signal family WH/ZH), scale_hqcd (QCD VH), scale_prompt_qcd / scale_prompt_ew (QCD / EW V gamma gamma), scale_higgs_other (ggZH, ttH, tH), and fakerate (D39 floor, fake-photon rows of both channels). The scale nuisances of the ZH j->gamma fake rows (scale_zjfake_qcd_zh, scale_zjfake_ew_zh) are NOT shared with the WH e->gamma lost-lepton rows (scale_efake_qcd_ll, scale_efake_ew): different fake mechanisms (j->gamma fake factor vs e->gamma object), decorrelated (verifier W2; no effect on Z0). Uncorrelated: MC statistics (mcstat per bin WH, mcstat_zh per bin ZH), channel-specific normalisations and modelling (WH: ps_qcd, C_*, cov_eFake, nonclosure, fake2_scen, npl_norm, hf_var, tau_r, tau_r_zrows; ZH: zh_* normalisations, scale_top_zh, zh_offshell, zh_int_zaa, zh_genmjj_*). tau: the ZH channel has no tau nuisance (Z->tautau->ll 0.31 %); in the WH SR the Z-lepton rows carry their own tau_r_zrows (not correlated with the W uplift tau_r).

| parameter | type | channels | status | declared common |
|---|---|---|---|---|
| fakerate | normsys | SR,ZH | correlated | True |
| lepeff | normsys | SR,ZH | correlated | True |
| lumi | normsys | SR,ZH | correlated | True |
| mu | normfactor | SR,ZH | correlated | True |
| pdf_sig | normsys | SR,ZH | correlated | True |
| pheff | normsys | SR,ZH | correlated | True |
| phres | histosys | SR,ZH | correlated | True |
| phscale | histosys | SR,ZH | correlated | True |
| scale_higgs_other | normsys | SR,ZH | correlated | True |
| scale_hqcd | normsys | SR,ZH | correlated | True |
| scale_prompt_ew | normsys | SR,ZH | correlated | True |
| scale_prompt_qcd | normsys | SR,ZH | correlated | True |
| scale_sig | normsys | SR,ZH | correlated | True |

## Results: common mu_VH (SM Asimov; Z0 asymptotic q0; mu95 asymptotic CLs q~, median and +-1 sigma)

| L | def | WH Z0 | WH mu95 (-1s, med, +1s) | ZH Z0 | ZH mu95 | VH Z0 | VH mu95 |
|---|---|---|---|---|---|---|---|
| 500 | a | 0.438 | 6.64 (4.26, 10.77) | 0.131 | 32.26 (19.34, 56.13) | 0.457 | 6.20 (4.00, 9.97) |
| 1000 | a | 0.608 | 4.28 (2.81, 6.77) | 0.184 | 19.09 (11.82, 32.18) | 0.634 | 4.02 (2.65, 6.30) |
| 3000 | a | 1.007 | 2.30 (1.55, 3.53) | 0.313 | 8.98 (5.82, 14.40) | 1.051 | 2.17 (1.47, 3.31) |
| 500 | b | 0.499 | 5.81 (3.72, 9.44) | 0.210 | 20.66 (12.26, 36.50) | 0.541 | 5.19 (3.35, 8.34) |
| 1000 | b | 0.693 | 3.74 (2.45, 5.91) | 0.295 | 12.15 (7.45, 20.81) | 0.752 | 3.36 (2.22, 5.25) |
| 3000 | b | 1.148 | 2.00 (1.35, 3.06) | 0.500 | 5.66 (3.63, 9.23) | 1.247 | 1.80 (1.22, 2.74) |

The ZH channel is a weak constraint (its own Z0 is 0.1-0.5); the common mu improves the WH numbers by a few percent. The WH-alone rows here come from the joint-workspace code (WH_workspace.json); the 07 numbers from stat_run.py agree to the second decimal (differences: the workspace adds the signal-like ZHjj rows).

## Results: (mu_WH, mu_ZH) and channel compatibility
The 2D workspaces (VH_workspace_2d*.json) declare the measurement m_2d_mu_WH with POI mu_WH (mu_ZH is the second free normalisation factor; both bounded [0, 100]); use mu_WH, mu_ZH as the two parameters of interest.

* 500 fb^-1: best fit (mu_WH, mu_ZH) = (1.00, 1.00) on the SM Asimov data; expected q along mu_WH = mu_ZH = x: {'0.5': 0.047113975591763335, '1.0': 0.0, '1.5': 0.03968260169807536, '2.0': 0.14728430893767808}; contour grid in work/stat/vh_map2d_500_a_v12.json (figure fig_mu_WH_vs_mu_ZH in the paper package). SM Asimov data: mu_hat_WH = mu_hat_ZH = 1, so the expected channel-compatibility q (common mu vs separate) is 0 and p = 1 by construction; the sensitivity to incompatibility is read from the map (q at (mu_WH, mu_ZH) = (1, 4), (1, 8), (2, 1), ...)
  Channel-compatibility test q = -2 ln[L(mu_hat common)/L(mu_hat_WH, mu_hat_ZH)] (chi2, 1 dof), on Asimov data generated at the point (value, p): SM (1,1): q = 0.00, p = 1.000; (mu_WH,mu_ZH)=(1,2.0): q = 0.01, p = 0.912; (mu_WH,mu_ZH)=(1,4.0): q = 0.10, p = 0.754; (mu_WH,mu_ZH)=(1,8.0): q = 0.45, p = 0.504; (mu_WH,mu_ZH)=(1,16.0): q = 1.58, p = 0.209; (mu_WH,mu_ZH)=(1,32.0): q = 4.70, p = 0.030; (mu_WH,mu_ZH)=(0.0,1): q = 0.01, p = 0.903; (mu_WH,mu_ZH)=(0.5,1): q = 0.00, p = 0.953; (mu_WH,mu_ZH)=(2.0,1): q = 0.01, p = 0.914; (mu_WH,mu_ZH)=(3.0,1): q = 0.04, p = 0.837. The SM Asimov point has q = 0 (p = 1) and carries no information; the point where p drops to 0.05 (q = 3.84) is the expected sensitivity to a WH-ZH disagreement.
* 1000 fb^-1: best fit (mu_WH, mu_ZH) = (1.00, 1.00) on the SM Asimov data; expected q along mu_WH = mu_ZH = x: {'0.5': 0.09098056117942122, '1.0': 0.0, '1.5': 0.07642475645748448, '2.0': 0.2832522030874145}; contour grid in work/stat/vh_map2d_1000_a_v12.json (figure fig_mu_WH_vs_mu_ZH in the paper package). SM Asimov data: mu_hat_WH = mu_hat_ZH = 1, so the expected channel-compatibility q (common mu vs separate) is 0 and p = 1 by construction; the sensitivity to incompatibility is read from the map (q at (mu_WH, mu_ZH) = (1, 4), (1, 8), (2, 1), ...)
  Channel-compatibility test q = -2 ln[L(mu_hat common)/L(mu_hat_WH, mu_hat_ZH)] (chi2, 1 dof), on Asimov data generated at the point (value, p): SM (1,1): q = 0.00, p = 1.000; (mu_WH,mu_ZH)=(1,2.0): q = 0.02, p = 0.876; (mu_WH,mu_ZH)=(1,4.0): q = 0.19, p = 0.659; (mu_WH,mu_ZH)=(1,8.0): q = 0.88, p = 0.347; (mu_WH,mu_ZH)=(1,16.0): q = 3.11, p = 0.078; (mu_WH,mu_ZH)=(1,32.0): q = 9.23, p = 0.002; (mu_WH,mu_ZH)=(0.0,1): q = 0.03, p = 0.864; (mu_WH,mu_ZH)=(0.5,1): q = 0.01, p = 0.934; (mu_WH,mu_ZH)=(2.0,1): q = 0.02, p = 0.879; (mu_WH,mu_ZH)=(3.0,1): q = 0.08, p = 0.771. The SM Asimov point has q = 0 (p = 1) and carries no information; the point where p drops to 0.05 (q = 3.84) is the expected sensitivity to a WH-ZH disagreement.
* 3000 fb^-1: best fit (mu_WH, mu_ZH) = (1.00, 1.00) on the SM Asimov data; expected q along mu_WH = mu_ZH = x: {'0.5': 0.24881258026189812, '1.0': 0.0, '1.5': 0.20568010538131887, '2.0': 0.7549426246243343}; contour grid in work/stat/vh_map2d_3000_a_v12.json (figure fig_mu_WH_vs_mu_ZH in the paper package). SM Asimov data: mu_hat_WH = mu_hat_ZH = 1, so the expected channel-compatibility q (common mu vs separate) is 0 and p = 1 by construction; the sensitivity to incompatibility is read from the map (q at (mu_WH, mu_ZH) = (1, 4), (1, 8), (2, 1), ...)
  Channel-compatibility test q = -2 ln[L(mu_hat common)/L(mu_hat_WH, mu_hat_ZH)] (chi2, 1 dof), on Asimov data generated at the point (value, p): SM (1,1): q = 0.00, p = 1.000; (mu_WH,mu_ZH)=(1,2.0): q = 0.07, p = 0.791; (mu_WH,mu_ZH)=(1,4.0): q = 0.56, p = 0.454; (mu_WH,mu_ZH)=(1,8.0): q = 2.54, p = 0.111; (mu_WH,mu_ZH)=(1,16.0): q = 8.82, p = 0.003; (mu_WH,mu_ZH)=(1,32.0): q = 23.31, p = 0.000; (mu_WH,mu_ZH)=(0.0,1): q = 0.08, p = 0.771; (mu_WH,mu_ZH)=(0.5,1): q = 0.02, p = 0.888; (mu_WH,mu_ZH)=(2.0,1): q = 0.07, p = 0.795; (mu_WH,mu_ZH)=(3.0,1): q = 0.25, p = 0.621. The SM Asimov point has q = 0 (p = 1) and carries no information; the point where p drops to 0.05 (q = 3.84) is the expected sensitivity to a WH-ZH disagreement.

## Results: lambda_WZ and (kappa_W, kappa_Z) (joint templates, same sign convention and R_BR in both channels)
**Convention (D46):** kZ-sign (kZ = -1, kW = -lambda; convention-independent, PRIMARY) with R_BR evaluated at the actual signs; the kW-sign variant (kW<0, kZ = kt = +1: W-top interference raises BR(gamma gamma) by x2.45) is quoted only with that statement. The ZH q-curves are RE-DERIVED (not inherited from the frozen ZH study) from the corrected ZH inputs (the ZH executor's pyhf curves and the reduced-model curves here agree: lambda = -1 at 500 fb^-1 0.29 sigma). Reduced nuisance model (per-class normalisations, signal theory 5 %, lumi 2.5 % shared, per-bin BB); the joint likelihood of mu is the pyhf one above.

| L | convention | lambda=-1: WH / ZH / VH | lambda<0 region: WH / ZH / VH |
|---|---|---|---|
| 500 | kZ-sign (primary) | 3.77 / 0.29 / 3.78 | 0.36 / 0.01 / 0.38 |
| 1000 | kZ-sign (primary) | 5.28 / 0.41 / 5.30 | 0.50 / 0.02 / 0.53 |
| 3000 | kZ-sign (primary) | 8.86 / 0.70 / 8.88 | 0.78 / 0.03 / 0.84 |
| 500 | kW-sign variant | 6.20 / 0.72 / 6.24 | 0.38 / 0.01 / 0.40 |
| 1000 | kW-sign variant | 8.61 / 1.02 / 8.65 | 0.53 / 0.01 / 0.55 |
| 3000 | kW-sign variant | 13.98 / 1.76 / 14.04 | 0.85 / 0.02 / 0.90 |

(kappa_W, kappa_Z) maps for WH, ZH and VH: work/stat/couplings_vh*_v12.json['maps'] and the paper figures fig_kappa_map_*. Entries at lambda>0 in the kZ-sign scan are computed at kZ = -1 (kW<0 for lambda>0): not meaningful, use the kW-sign scan for lambda>0.

## Validation of the asymptotic numbers with toys (D47 (2))
see table below and paper_numbers.json (toys_*).

| quantity (500 fb^-1, def. a unless stated) | channel | asymptotic | toys (median, +-1 sigma binomial range) | N toys |
|---|---|---|---|---|
| Z0 (null from b-only toys) | WH | 0.438 | 0.406 (0.379-0.436) | 2000 s+b / 2000 null |
| Z0 (null from b-only toys) | ZH | 0.131 | 0.000 (0.000-0.000) | 2000 s+b / 2000 null |
| Z0 (null from b-only toys) | VH | 0.457 | 0.406 (0.366-0.441) | 2000 s+b / 2000 null |
| mu95 (expected CLs) | WH | 6.64 | 8.38 +- 1.11 (straight-line fit of ln CLs) | 400 sb + 400 b per point x 4 points |
| mu95 (expected CLs) | ZH | 32.26 | 34.29 +- 1.93 (straight-line fit of ln CLs) | 400 sb + 400 b per point x 4 points |
| mu95 (expected CLs) | VH | 6.20 | 6.41 +- 0.35 (straight-line fit of ln CLs) | 480 sb + 480 b per point x 5 points |
| lambda=-1 exclusion Z, kZ-sign (sign carried by kZ; convention-independent; primary) | WH | 3.77 | 3.92 (q 16-84 %: Z 3.49-4.28) | 5000 |
| lambda=-1 exclusion Z, kZ-sign (sign carried by kZ; convention-independent; primary) | ZH | 0.29 | 0.82 (q 16-84 %: Z 0.33-0.82) | 5000 (ZH: NOT COMPARABLE: the q distribution is far from asymptotic, 91 % of the toys have q < 1) |
| lambda=-1 exclusion Z, kZ-sign (sign carried by kZ; convention-independent; primary) | VH | 3.78 | 3.97 (q 16-84 %: Z 3.42-4.26) | 5000 |
| lambda=-1 exclusion Z, kW-sign (kW<0, kZ=kt=+1, BR x2.45; D46 closure range 5.1-7.1 for WH at 500 fb-1) | WH | 6.20 | 6.33 (q 16-84 %: Z 5.83-6.70) | 5000 |
| lambda=-1 exclusion Z, kW-sign (kW<0, kZ=kt=+1, BR x2.45; D46 closure range 5.1-7.1 for WH at 500 fb-1) | ZH | 0.72 | 1.13 (q 16-84 %: Z 0.23-1.30) | 5000 (ZH: NOT COMPARABLE: the q distribution is far from asymptotic, 91 % of the toys have q < 1) |
| lambda=-1 exclusion Z, kW-sign (kW<0, kZ=kt=+1, BR x2.45; D46 closure range 5.1-7.1 for WH at 500 fb-1) | VH | 6.24 | 6.37 (q 16-84 %: Z 5.87-6.71) | 5000 |

**Headline (one message).** The headline expected numbers are the PRE-DECLARED ASYMPTOTIC ones (Z0 and mu95 scale to 1000/3000 fb^-1, where no toys were run); the toy values at 500 fb^-1 are quoted beside them. WHERE THEY DIFFER: the VH toy expected Z0 is 0.406 against the asymptotic 0.457 (13 % lower) (if a single VH number is quoted at 500 fb^-1 the toy value is the more reliable one); WH agrees; ZH alone has no discovery sensitivity in the toys.
* Z0 WH: asymptotic 0.438; toy 0.406 (range 0.379-0.436); p_mid at the median = 0.343; q0 = 0 exactly: 14 % (s+b) / 19 % (null); q0 < 1e-6 (numerical zero of the fits): 29 % / 41 %; q0 < 1e-3: 40 % / 57 %; raw strict-median treatment (p = P(q0_null >= median), no tie width): Z = 0.41 (2000 s+b, 2000 null toys).
* Z0 ZH: asymptotic 0.131; toy 0.000 (CLIPPED at 0 from an unclipped value of -0.46; the range 0.000-0.000 is a clipping artefact) (range 0.000-0.000); p_mid at the median = 0.677; q0 = 0 exactly: 31 % (s+b) / 31 % (null); q0 < 1e-6 (numerical zero of the fits): 61 % / 64 %; q0 < 1e-3: 62 % / 65 %; raw strict-median treatment (p = P(q0_null >= median), no tie width): Z = -0.01 (2000 s+b, 2000 null toys).
* Z0 VH: asymptotic 0.457; toy 0.406 (range 0.366-0.441); p_mid at the median = 0.343; q0 = 0 exactly: 12 % (s+b) / 18 % (null); q0 < 1e-6 (numerical zero of the fits): 30 % / 39 %; q0 < 1e-3: 40 % / 56 %; raw strict-median treatment (p = P(q0_null >= median), no tie width): Z = 0.41 (2000 s+b, 2000 null toys).

Toy expected Z0 definition: Z = Phi^-1(1 - p_mid), p_mid = P(q0_null > q) + 0.5 P(|q0_null - q| <= 1e-6) at the median q of the s+b toys (1e-6 = tie width, the numerical noise of the fits: values below it are numerical zeros), clipped at 0; the range evaluates the same map at the binomial +-1 sigma quantiles of that median (the central value is always inside the range). A ZH toy value of 0 means that the median s+b q0 is numerically zero (more than half of the toys cannot distinguish the signal), not that the asymptotic 0.13 is wrong: both say no ZH discovery sensitivity.
* mu95 WH: asymptotic 6.64; toys (straight-line fit of ln CLs vs mu over 4 points, 400 sb + 400 b toys per point) 8.38 +- 1.11; interpolation 9.00.
* mu95 ZH: asymptotic 32.26; toys (straight-line fit of ln CLs vs mu over 4 points, 400 sb + 400 b toys per point) 34.29 +- 1.93; interpolation 34.35.
* mu95 VH: asymptotic 6.20; toys (straight-line fit of ln CLs vs mu over 5 points, 480 sb + 480 b toys per point) 6.41 +- 0.35; interpolation 6.65.

mu95 toy comparison (toy mu95 minus asymptotic, in units of the toy fit error; the fit error is UNDERSTATED because the same seeds are reused at every mu point and the CLs curve is non-monotone): WH: asymptotic 6.64 vs toy 8.38 +- 1.11 (+1.6 sigma); ZH: asymptotic 32.26 vs toy 34.29 +- 1.93 (+1.1 sigma); VH: asymptotic 6.20 vs toy 6.41 +- 0.35 (+0.6 sigma). WH is a 1.6 sigma difference (the interpolated 9.00 is the grid end); the toys therefore constrain mu95 only to about +-15-25 % and mu95 is NOT called validated or confirmed by them. Two independent WH toy realisations differ (6.85 vs 8.34 with the same fit). The asymptotic mu95 uses a refined scan grid (v1.2 fix).
* lambda=-1 kZ-sign:WH: asymptotic Z 3.77; toy median-q Z 3.92 (q 16-84 %: Z 3.49-4.28); 207 distinct q values in 5000 toys; 0 % of the toys have q < 1; convention: kZ-sign (sign carried by kZ; convention-independent; primary).
* lambda=-1 kZ-sign:ZH: asymptotic Z 0.29; toy median-q Z 0.82 (q 16-84 %: Z 0.33-0.82); 2107 distinct q values in 5000 toys; 91 % of the toys have q < 1; NOT COMPARABLE with the Asimov value (the q distribution is far from asymptotic); convention: kZ-sign (sign carried by kZ; convention-independent; primary).
* lambda=-1 kZ-sign:VH: asymptotic Z 3.78; toy median-q Z 3.97 (q 16-84 %: Z 3.42-4.26); 4112 distinct q values in 5000 toys; 0 % of the toys have q < 1; convention: kZ-sign (sign carried by kZ; convention-independent; primary).
* lambda=-1 kW-sign:WH: asymptotic Z 6.20; toy median-q Z 6.33 (q 16-84 %: Z 5.83-6.70); 207 distinct q values in 5000 toys; 0 % of the toys have q < 1; PLATEAU: the median bracket is degenerate, its error is not meaningful; convention: kW-sign (kW<0, kZ=kt=+1, BR x2.45; D46 closure range 5.1-7.1 for WH at 500 fb-1).
* lambda=-1 kW-sign:ZH: asymptotic Z 0.72; toy median-q Z 1.13 (q 16-84 %: Z 0.23-1.30); 2285 distinct q values in 5000 toys; 43 % of the toys have q < 1; NOT COMPARABLE with the Asimov value (the q distribution is far from asymptotic); convention: kW-sign (kW<0, kZ=kt=+1, BR x2.45; D46 closure range 5.1-7.1 for WH at 500 fb-1).
* lambda=-1 kW-sign:VH: asymptotic Z 6.24; toy median-q Z 6.37 (q 16-84 %: Z 5.87-6.71); 4121 distinct q values in 5000 toys; 0 % of the toys have q < 1; convention: kW-sign (kW<0, kZ=kt=+1, BR x2.45; D46 closure range 5.1-7.1 for WH at 500 fb-1).

lambda toys: q(lambda=-1) of SM toys is a DISCRETE variable at these counts (few events in 4 mT bins (WH) or 30 bins with 2-3 events (ZH)); the toy Z is sqrt of the 50 % quantile of q over the toys (a plateau value when many toys share the same q). The base of q is the minimum of the profile over the SM point and a lambda grid {-2, -1.5, ..., 3} (vh_coup.py --toys), not the exact global minimum: slightly conservative. For ZH alone the toy median q = 0.66 sits on such a plateau (91 % of the ZH toys have q < 1) against the Asimov q = 0.084: for q << 1 the median is fluctuation-dominated and is not comparable with the Asimov value; both mean no ZH lambda sensitivity. WH and VH agree with Asimov within 4-6 % in Z. Seeds: the toys of this version are seeded per chunk (np.random.seed(seed); the lambda toys use default_rng(seed)); the first toy production was not seed-reproducible and is archived (work/toys_prefix/).

Tolerances: the ZH lambda = -1 curves of the ZH executor (pyhf templates) and the reduced-model joint fits here agree within 2.8 % in Z (largest at 3000 fb^-1 in the kW-sign convention; 0.29 / 0.41 / 0.70 against 0.29 / 0.41 / 0.69 in the kZ-sign convention).

## Limitations (D47 (3))
* **f_mu placeholder (D40):** the per-jet muon misID is 2e-5 (= the electron value); no cited value exists; the whole light-misID normalisation is covered by x0.3-x3 (D36) and by the npl_norm nuisance; non-prompt leptons are 1.1 % of b at the selection.
* **Fake-photon calibration reference mismatch (D39/D43):** CMS-SMP-19-013 (JHEP 10 (2021) 174, Table 2) is inclusive in jets and cannot calibrate the VBS-like j->gamma rate; WH uses c = 1, ZH kappa = 0.956 (rough closure); the x0.3-x3 per-photon scan covers it (fake photons are 1.7 % of b in WH).
* **Other-Higgs backgrounds are not rescaled under the coupling hypotheses** (12 % of b): the tH rows (which grow about x10 for kW*kt<0, kW-sign convention) scaled in the tested hypothesis change Z(lambda=-1) from 6.20 to 6.26 (x10) in the kW-sign convention and from 3.76 to 3.84 in the kZ-sign convention (no growth physically there): leaving them fixed is slightly conservative (couplings_v12.json['tH_growth_test_tested_hypothesis']).
* **No Z gamma + 3 jets row in ZH (D43):** the fake-photon component in ZH may be underestimated (the converted jet needs a third ME jet); WH has the 3-jet row.
* ZH and WH MC samples at LO, Delphes without pile-up; ASSUMPTION nuisances (lumi, efficiencies, photon scale/resolution) have no data basis; the lambda curves use the reduced nuisance model and asymptotics (toy check above); closure of the per-bin quadratic is not shown to cover the 3.3 sigma leave-one-out pulls.


* **D49 (settled by D50 = option 4):** the QCD lost-lepton one-event estimate (0.121 events, 95 % interval [0.0031, 0.675]) does not meet the D42 N_eff >= 10 rule; the upper end is shown in the D49 section below (WH alone).
* **VH nuisance ranking not delivered:** vh_run.py rankvh (913470.001) was removed once by SYSTEM_PERIODIC_REMOVE after about 24 h (913470.000, the WH ranking, returned 0); not rerun (over the 30 min budget).
* **ZH non-prompt-lepton class:** no MC exists and none will be produced (D50); the class is unestimated and unbounded, not negligible.
* **Toys:** the mu95 toys reuse the same seeds at every mu point (understated fit errors) and the WH/ZH/VH sets share seeds; the lambda toys were generated before the final rebuild, but the workspaces rebuilt with the current code are byte-identical to the committed ones and the coupling inputs reproduce bit-identically (couplings_vh*_v12_stale.json), so the lambda toys remain valid.
* **Definition (a):** the SR ZHjj-QCD lost-lepton row is a background (no normalisation factor); only EW ZHjj is signal-like (correlation_scheme.json 'tau' aligned).


## D49 option (4): WH-alone upper-end of the QCD lost-lepton part

D49 SETTLED by D50 = option (4): the QCD lost-lepton / e->gamma part is the one-event estimate 0.121 events (one selected raw F_QCD_llajj_loose row, 7.5M-event union), 95 % Garwood interval [0.0031, 0.675] (1-sigma central interval [0.021, 0.400]); the pre-declared reco-SR twin correction C has a stat floor of 100 % (> 30 %), so no cut sample was produced (work/d49_floor.json); the v1 vbs x C estimate (0.176 [0.094, 0.257]) is a CROSS-CHECK, not an independent estimate; the upper-end result is shown with the central one (table in this report). The class still does NOT meet the D42 N_eff >= 10 rule (one-event dominated; stated limitation).

WH alone, definition (a), stand-alone WH workspace, full systematics (task ll4:L, the two QCD groups efake_qcd_ll + efake_qcd_eg scaled to the interval ends, whole m_gg template; the central row reproduces the nominal fit). Y0 uses the gridpack sigma (the closure sigma gives 0.12101, -0.17 %, a normalisation note, not a change of the estimate). The sample ZH_Zaajj_QCD_nomjj_lostlep of the same class has N_eff = 2.0 (yield 0.0029): it too is below the N_eff >= 10 rule.

| L (fb-1) | QCD lost-lepton part | Y at 500 fb-1 (events) | Z0 (PL) | mu95 median (-1s, +1s) |
|---|---|---|---|---|
| 500 | lower95 | 0.0031 | 0.460 | 6.42 (4.10, 10.43) |
| 500 | central | 0.1212 | 0.428 | 6.81 (4.37, 11.06) |
| 500 | upper95 | 0.6754 | 0.309 | 10.91 (6.51, 21.54) |
| 1000 | lower95 | 0.0031 | 0.642 | 4.09 (2.68, 6.46) |
| 1000 | central | 0.1212 | 0.594 | 4.40 (2.88, 6.94) |
| 1000 | upper95 | 0.6754 | 0.400 | 8.32 (4.92, 17.21) |
| 3000 | lower95 | 0.0031 | 1.078 | 2.14 (1.44, 3.26) |
| 3000 | central | 0.1212 | 0.983 | 2.36 (1.59, 3.62) |
| 3000 | upper95 | 0.6754 | 0.544 | 6.45 (3.69, 14.24) |

Note: the joint VH numbers above use the central one-event estimate; the upper-end scenario is evaluated with the stand-alone WH workspace only (the lost-lepton QCD part enters the ZH channel through frozen ZH rows, unchanged).