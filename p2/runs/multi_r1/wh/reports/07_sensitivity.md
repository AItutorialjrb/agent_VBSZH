# 07 Sensitivity (executor-wh FINAL, block 3)
Date UTC: 2026-11-16 10:31. Status: **PASS for verification**; ALL numbers are EXPECTED (Asimov datasets, nominal background model of 05a v2.1 + the v1.1 loose-cut eFake sample, primary = cut-based selection; D44). No claim of a result; a null or sub-1-sigma expectation is stated as such. Analysis commit: ORCH_COMMIT_PLACEHOLDER.
## Selection (frozen in 05): mjj>600, |deta_jj|>4.0, pT(gg)>75, MET>30, pT(l)>25, |m_gg-125|<3.5 (counting); MVA alternative not adopted.
## 1. Counting window (Eq. 1, stat only) and exact-Poisson CLs
Window yields at 500 fb^-1: s = 0.612, b = 1.747 +- 0.191 (MC stat).
| L [fb^-1] | s | b | Z Eq. 1 | Z (b -MC, b +MC) | exact-Poisson counting CLs mu95 (q16, median, q84) | def (b): s, b, Z, mu95 median |
|---|---|---|---|---|---|---|
| 500 | 0.612 | 1.747 | 0.440 | 0.463, 0.419 | 4.89, 8.08, 10.07 | 0.683, 1.676, 0.497, 5.70 |
| 1000 | 1.225 | 3.494 | 0.622 | 0.655, 0.593 | 3.51, 4.22, 5.94 | 1.367, 3.352, 0.703, 3.83 |
| 3000 | 3.674 | 10.481 | 1.077 | 1.134, 1.027 | 1.55, 2.13, 3.18 | 4.100, 10.055, 1.217, 1.96 |

NOT the same quantity as the profile-likelihood mu95 of sec. 2 (asymptotic q~ CLs on the m_gg shape fit, pyhf). The Poisson 'q16/q84' columns are the observed-count quantiles of Poisson(b) mapped to mu95 (discrete).

## 2. Profile likelihood (m_gg 100-180 GeV, 40 bins, all nuisances of 06 + Barlow-Beeston)

| L | def | expected Z0 | PL asymptotic (q~) CLs mu95 median (-1s, +1s) | Z0 stat-only | Z0 without MC stat | Z0 MC-stat only |
|---|---|---|---|---|---|---|
| 500 | a | 0.445 | 6.58 (4.21, 10.67) | 0.458 | 0.447 | 0.456 |
| 1000 | a | 0.620 | 4.21 (2.76, 6.64) | 0.648 | 0.626 | 0.641 |
| 3000 | a | 1.038 | 2.22 (1.50, 3.38) | 1.122 | 1.069 | 1.091 |
| 500 | b | 0.505 | 5.79 (3.70, 9.41) | 0.519 | 0.507 | 0.517 |
| 1000 | b | 0.703 | 3.70 (2.42, 5.83) | 0.735 | 0.709 | 0.728 |
| 3000 | b | 1.177 | 1.94 (1.31, 2.96) | 1.272 | 1.211 | 1.239 |

With/without MC-stat impact on Z0 at 500 fb^-1 and mu95 is in 06 sec. 4: Barlow-Beeston is mandatory (cut-based b N_eff 63 in v1.1, 135 in v2.1).

## 3. D36 scan: fake photons (per-photon rate x f; one-fake x f, two-fake x f^2), 500 fb^-1 (def. a, PL with all nuisances)
D36 range x0.3-x3; f = 10, 30, 100 are BEYOND D36 (robustness only).

| f | Z0 (PL) | mu95 median (-1s, +1s) | Z Eq. 1 counting | b window |
|---|---|---|---|---|
| 0.3 | 0.448 | 6.56 (4.20, 10.64) | 0.442 | 1.726 |
| 0.5 | 0.447 | 6.56 (4.20, 10.65) | 0.441 | 1.732 |
| 1.0 | 0.445 | 6.58 (4.21, 10.67) | 0.440 | 1.747 |
| 2.0 | 0.441 | 6.61 (4.24, 10.72) | 0.436 | 1.778 |
| 3.0 | 0.438 | 6.65 (4.27, 10.77) | 0.432 | 1.812 |
| 10.0 (beyond D36) | 0.410 | 6.96 (4.49, 11.19) | 0.405 | 2.087 |
| 30.0 (beyond D36) | 0.330 | 8.12 (5.33, 12.78) | 0.328 | 3.286 |
| 100.0 (beyond D36) | 0.175 | 13.50 (9.19, 20.31) | 0.173 | 12.298 |

## 3. D36 scan: fake photons (per-photon rate x f; one-fake x f, two-fake x f^2), 3000 fb^-1 (def. a, PL with all nuisances)
D36 range x0.3-x3; f = 10, 30, 100 are BEYOND D36 (robustness only).

| f | Z0 (PL) | mu95 median (-1s, +1s) | Z Eq. 1 counting | b window |
|---|---|---|---|---|
| 0.3 | 1.044 | 2.21 (1.49, 3.37) | 1.083 | 10.353 |
| 0.5 | 1.042 | 2.21 (1.49, 3.37) | 1.081 | 10.389 |
| 1.0 | 1.038 | 2.22 (1.50, 3.38) | 1.077 | 10.481 |
| 2.0 | 1.031 | 2.23 (1.51, 3.40) | 1.068 | 10.671 |
| 3.0 | 1.023 | 2.25 (1.52, 3.42) | 1.059 | 10.870 |
| 10.0 (beyond D36) | 0.963 | 2.37 (1.61, 3.59) | 0.993 | 12.521 |
| 30.0 (beyond D36) | 0.790 | 2.83 (1.94, 4.24) | 0.803 | 19.716 |
| 100.0 (beyond D36) | 0.425 | 5.03 (3.51, 7.33) | 0.424 | 73.787 |

## 3. D36 scan: non-prompt leptons (light misID and heavy flavour x f), 500 fb^-1 (def. a, PL with all nuisances)
D36 range x0.3-x3; f = 10, 30, 100 are BEYOND D36 (robustness only).

| f | Z0 (PL) | mu95 median (-1s, +1s) | Z Eq. 1 counting | b window |
|---|---|---|---|---|
| 0.3 | 0.447 | 6.56 (4.20, 10.65) | 0.441 | 1.732 |
| 0.5 | 0.446 | 6.57 (4.21, 10.66) | 0.441 | 1.736 |
| 1.0 | 0.445 | 6.58 (4.21, 10.67) | 0.440 | 1.747 |
| 2.0 | 0.443 | 6.60 (4.23, 10.70) | 0.437 | 1.767 |
| 3.0 | 0.441 | 6.62 (4.24, 10.73) | 0.435 | 1.788 |
| 10.0 (beyond D36) | 0.426 | 6.78 (4.36, 10.95) | 0.420 | 1.933 |
| 30.0 (beyond D36) | 0.388 | 7.22 (4.68, 11.54) | 0.384 | 2.346 |
| 100.0 (beyond D36) | 0.309 | 8.50 (5.61, 13.31) | 0.306 | 3.793 |

## 3. D36 scan: non-prompt leptons (light misID and heavy flavour x f), 3000 fb^-1 (def. a, PL with all nuisances)
D36 range x0.3-x3; f = 10, 30, 100 are BEYOND D36 (robustness only).

| f | Z0 (PL) | mu95 median (-1s, +1s) | Z Eq. 1 counting | b window |
|---|---|---|---|---|
| 0.3 | 1.042 | 2.21 (1.49, 3.37) | 1.081 | 10.394 |
| 0.5 | 1.041 | 2.21 (1.49, 3.37) | 1.080 | 10.419 |
| 1.0 | 1.038 | 2.22 (1.50, 3.38) | 1.077 | 10.481 |
| 2.0 | 1.034 | 2.23 (1.51, 3.39) | 1.071 | 10.605 |
| 3.0 | 1.029 | 2.24 (1.51, 3.41) | 1.065 | 10.729 |
| 10.0 (beyond D36) | 0.995 | 2.30 (1.56, 3.50) | 1.028 | 11.597 |
| 30.0 (beyond D36) | 0.914 | 2.48 (1.69, 3.74) | 0.941 | 14.077 |
| 100.0 (beyond D36) | 0.741 | 3.00 (2.06, 4.46) | 0.751 | 22.759 |

## 4. Couplings (lambda_WZ = kappa_W/kappa_Z, (kappa_W, kappa_Z)) from the direct samples, expected, SM data (Asimov), asymptotic
**Sign convention (SPEC D46, orchestrator default pending the human).** The signal yield is even under (kW, kZ) -> (-kW, -kZ), so (kW, kZ) = (-1, 1) and (1, -1) are the same point for the VBS yield; they differ only in the H->gamma gamma branching ratio, through the sign of kW*kt in the W-top loop (A_W = -8.32 kW, A_t = +1.84 kt, standard loop functions, e.g. A. Djouadi, Phys. Rept. 457 (2008) 1, hep-ph/0503172; recomputed here at mH = 125 GeV, mW = 80.4, mt = 172.5; YR4 BRs; kb = kt = ktau = kc = 1).
* **PRIMARY (convention-independent): lambda = -1 realised as kZ = -1, kW = +1 (sign carried by kZ, R_BR = 1 at this point): expected exclusion Z = 3.8 sigma at 500 fb^-1 (stat-only 3.8).**
* kW-sign convention (kW = -1, kZ = +1 = kt): the W-top interference raises BR(gamma gamma) by x2.45 and the expected exclusion is ~6 sigma (6.2 sigma central; 5.1-7.1 under a +-30 % closure variation of the predicted signal), asymptotic. This number needs the convention and the BR modelling: it is NOT the headline.
* Whole lambda<0 region: expected Z = 0.35 sigma (kZ-sign convention; its closest point is lambda about -0.05, where the signal is similar to the lambda about 0.2 gamma gamma amplitude zero) and 0.37 sigma (kW-sign convention): robust to the convention; the lambda<0 region cannot be excluded in this channel.
* "R_BR = 1 for all lambda" (the samples with the SM BR only, 1.61 sigma at lambda=0) is UNPHYSICAL and is not a result: the gamma gamma amplitude and the width depend on kW at every lambda.
Method (scripts/coup_run.py): per-bin quadratic Y_i = alpha_i kW^2 + beta_i kW kZ + gamma_i kZ^2 from the 8 CP-even points (weighted LSQ) x R_BR(kW, kZ). **REDUCED nuisance model** (per-class background normalisations with the 05a class-bound widths, signal theory 5 %, lumi 2.5 % ASSUMPTION, Barlow-Beeston-lite), not the full 06 model: stat-only / MC-stat / reduced differ by <= 2 % in Z; the full-model ranking (06 sec. 3) says no nuisance moves Z0 by more than 0.8 %. Binning chosen before the fit by the expected exclusion of lambda=-1: mtwgg (edges [0, 250, 350, 450, 100000.0]).
**Other-Higgs backgrounds (12 % of b: QCD WH, ggZH, ttH, tH) are NOT rescaled under the coupling hypotheses; only the signal carries kappa and R_BR.** tHq grows by about x10 at kW*kt < 0; leaving it unscaled is likely conservative for the exclusion of lambda=-1 (more background would lower it) but untested.
**Precision:** these are expected values from the asymptotic formula; the 4 bins hold O(1) events and no toy or exact check of the ~4-6 sigma tail exists. The +-30 % closure variation of the tested signal (Z(lambda=-1) 3.1 / 3.8 / 4.4 for 0.7 / 1.0 / 1.3 in the kZ convention = PRIMARY band; 5.1 / 6.2 / 7.1 in the kW convention) is NOT shown to cover the leave-one-out per-bin pulls (up to 3.3 sigma at lambda = 0 and -0.5); read the numbers to the nearest sigma.

### (kappa_W, kappa_Z) map (kW-sign convention, reduced model, 500 fb^-1): expected q = Z^2 of excluding the point against the SM data

| kW \ kZ | 0.25 | 0.50 | 0.75 | 1.00 | 1.25 | 1.50 | 1.75 | 2.00 |
|---|---|---|---|---|---|---|---|---|
| -2.0 | 10.3 | 11.3 | 12.2 | 13.2 | 14.1 | 15.0 | 15.9 | 16.7 |
| -1.5 | 7.1 | 8.0 | 8.9 | 9.8 | 10.7 | 11.5 | 12.3 | 13.0 |
| -1.0 | 3.8 | 4.6 | 5.4 | 6.2 | 7.0 | 7.7 | 8.4 | 9.0 |
| -0.5 | 1.1 | 1.7 | 2.2 | 2.7 | 3.2 | 3.7 | 4.2 | 4.7 |
| +0.0 | 0.4 | 0.4 | 0.4 | 0.4 | 0.5 | 0.6 | 0.7 | 0.8 |
| +0.5 | 0.4 | 0.4 | 0.4 | 0.3 | 0.3 | 0.4 | 0.6 | 0.7 |
| +1.0 | 1.1 | 0.6 | 0.2 | 0.0 | 0.2 | 0.7 | 1.2 | 1.7 |
| +1.5 | 3.6 | 2.9 | 2.2 | 1.6 | 1.2 | 1.2 | 1.4 | 1.9 |
| +2.0 | 6.6 | 5.8 | 5.0 | 4.2 | 3.5 | 3.0 | 2.7 | 2.7 |
| +2.5 | 9.6 | 8.8 | 7.9 | 7.0 | 6.2 | 5.5 | 4.9 | 4.5 |
| +3.0 | 12.5 | 11.6 | 10.7 | 9.9 | 9.0 | 8.2 | 7.5 | 6.8 |
(entries are Z = sqrt(q); the SM point (1, 1) is 0 by construction; |kW| ~ 0.2-0.5 with kZ ~ 1 and the kW<0 sector near kW ~ 0 are not excluded, in line with the lambda<0 result.)

Leave-one-out closure of the per-bin quadratic (LSQ covariance included): totals |pull| <= 1.6; per-bin pulls up to 3.3.

### D36 scans for the lambda<0 exclusion (reduced coupling model, kW-sign convention)

| kind | f | Z(lambda=-1) | Z(lambda=0) | Z(lambda=0.5) |
|---|---|---|---|---|
| fake | 0.3 | 6.20 | 0.38 | 0.34 |
| fake | 0.5 | 6.20 | 0.38 | 0.34 |
| fake | 1.0 | 6.20 | 0.37 | 0.34 |
| fake | 2.0 | 6.19 | 0.37 | 0.33 |
| fake | 3.0 | 6.19 | 0.37 | 0.33 |
| fake | 10.0 (beyond D36) | 6.12 | 0.32 | 0.27 |
| fake | 30.0 (beyond D36) | 5.87 | 0.24 | 0.15 |
| fake | 100.0 (beyond D36) | 5.18 | 0.12 | 0.05 |
| npl | 0.3 | 6.20 | 0.38 | 0.34 |
| npl | 0.5 | 6.20 | 0.38 | 0.34 |
| npl | 1.0 | 6.20 | 0.37 | 0.34 |
| npl | 2.0 | 6.20 | 0.37 | 0.34 |
| npl | 3.0 | 6.19 | 0.37 | 0.33 |
| npl | 10.0 (beyond D36) | 6.18 | 0.36 | 0.32 |
| npl | 30.0 (beyond D36) | 6.14 | 0.31 | 0.26 |
| npl | 100.0 (beyond D36) | 5.99 | 0.22 | 0.15 |

### D36 scans for the lambda<0 exclusion, kZ convention (PRIMARY; reduced coupling model)

| kind | f | Z(lambda=-1) | Z(lambda=0) | Z(lambda=0.5) |
|---|---|---|---|---|
| fake | 0.3 | 3.77 | 0.38 | 0.62 |
| fake | 0.5 | 3.77 | 0.38 | 0.62 |
| fake | 1.0 | 3.76 | 0.37 | 0.61 |
| fake | 2.0 | 3.76 | 0.37 | 0.61 |
| fake | 3.0 | 3.75 | 0.37 | 0.61 |
| fake | 10.0 (beyond D36) | 3.70 | 0.32 | 0.58 |
| fake | 30.0 (beyond D36) | 3.50 | 0.24 | 0.51 |
| fake | 100.0 (beyond D36) | 2.93 | 0.12 | 0.30 |
| npl | 0.3 | 3.77 | 0.38 | 0.62 |
| npl | 0.5 | 3.76 | 0.38 | 0.62 |
| npl | 1.0 | 3.76 | 0.37 | 0.61 |
| npl | 2.0 | 3.76 | 0.37 | 0.61 |
| npl | 3.0 | 3.76 | 0.37 | 0.61 |
| npl | 10.0 (beyond D36) | 3.75 | 0.36 | 0.61 |
| npl | 30.0 (beyond D36) | 3.72 | 0.31 | 0.59 |
| npl | 100.0 (beyond D36) | 3.62 | 0.22 | 0.55 |

## 6. Mass-resolution dependence (signal m_gg smeared about 125 GeV by r; 500 fb^-1, def. a)

| r | s (+-3.5 window) | b | Z Eq. 1 | Z0 PL | mu95 median |
|---|---|---|---|---|---|
| 0.8 | 0.649 | 1.747 | 0.465 | 0.486 | 6.19 |
| 1.0 | 0.612 | 1.747 | 0.440 | 0.445 | 6.57 |
| 1.25 | 0.556 | 1.747 | 0.401 | 0.405 | 7.02 |
| 1.5 | 0.502 | 1.747 | 0.364 | 0.373 | 7.43 |
| 2.0 | 0.413 | 1.747 | 0.301 | 0.328 | 8.17 |

## 7. Caveats / what this is not
Expected only; the sensitivity is below 1 sigma at 500 fb^-1 and about 1 sigma at 3000 fb^-1 (PL, cut-based): no evidence is expected and none is claimed. Delphes-level, LO, no pile-up. ASSUMPTION nuisances (lumi, photon/lepton efficiency, mass scale/resolution) have no data basis. **The v1.1 lost-lepton class has N_eff = 7.6 at the selection, below the SPEC sec. 4.3 standard N_eff >= 10 (36 % MC stat; its QCD part is one raw row); the v1 estimate (vbs x C) is carried as the robustness row in 06 sec. 5; the v1.1 nominal is kept (pre-declared by 04:139 and D45).** Signal definition (b) adds QCD WHjj (H_QCD_WH_mlm) as signal; its interference (-0.3 % of EW) is neglected. The v1.1 row F_QCD_llajj_loose IS included (replaces the QCD part of ZH_Zajj_eFake; all numbers in this report are the v1.1 evaluation, files *_v11.json; D45 trigger not fired); H_ggF_jj is NOT in the nominal: its gridpack (893012) failed, the D38 scaled central proxy (05a sec. 12, 0.024 events in the window, +1.3 % of b) is a bound variant that lowers Z0 by about 0.6 % (work/stat/ggf_variant_v11.json). MVA alternative not carried through the statistics here (D44: alternative only). Figures: figures/mgg_selection, Z_vs_lumi, d36_*, lambda_exclusion*.

## 8. Next
Verification; VH combination with the frozen ZH (swappable ZH table); comparison with CMS/ATLAS; reproducibility and FINAL report; v1.1 re-evaluations.


## D49 option (4): central and upper-end result

D49 SETTLED by D50 = option (4): the QCD lost-lepton / e->gamma part is the one-event estimate 0.121 events (one selected raw F_QCD_llajj_loose row, 7.5M-event union), 95 % Garwood interval [0.0031, 0.675] (1-sigma central interval [0.021, 0.400]); the pre-declared reco-SR twin correction C has a stat floor of 100 % (> 30 %), so no cut sample was produced (work/d49_floor.json); the v1 vbs x C estimate (0.176 [0.094, 0.257]) is a CROSS-CHECK, not an independent estimate; the upper-end result is shown with the central one (table in this report). The class still does NOT meet the D42 N_eff >= 10 rule (one-event dominated; stated limitation).

WH alone, definition (a), stand-alone WH workspace, full systematics (task ll4:L, the two QCD groups efake_qcd_ll + efake_qcd_eg scaled to the interval ends, whole m_gg template; the central row reproduces the nominal fit). Y0 uses the gridpack sigma (the closure sigma gives 0.12101, -0.17 %, a normalisation note, not a change of the estimate). The sample ZH_Zaajj_QCD_nomjj_lostlep of the same class has N_eff = 2.0 (yield 0.0029): it too is below the N_eff >= 10 rule.

| L (fb-1) | QCD lost-lepton part | Y at 500 fb-1 (window, events; scaled with L in the fit) | Z0 (PL) | mu95 median (-1s, +1s) | lambda=-1 Z WH / VH, kZ-sign (primary) | lambda=-1 Z WH / VH, kW-sign (kW<0, kZ=kt=+1, BR x2.45; D46) |
|---|---|---|---|---|---|---|
| 500 | lower95 | 0.0031 | 0.461 | 6.41 (4.09, 10.43) | 3.766 / 3.776 | 6.204 / 6.242 |
| 500 | central | 0.1212 | 0.445 | 6.58 (4.21, 10.67) | 3.766 / 3.776 | 6.204 / 6.241 |
| 500 | upper95 | 0.6754 | 0.379 | 7.82 (4.96, 12.99) | 3.766 / 3.776 | 6.202 / 6.239 |
| 1000 | lower95 | 0.0031 | 0.643 | 4.08 (2.68, 6.45) | 5.282 / 5.296 | 8.606 / 8.653 |
| 1000 | central | 0.1212 | 0.620 | 4.21 (2.76, 6.64) | 5.282 / 5.296 | 8.605 / 8.653 |
| 1000 | upper95 | 0.6754 | 0.515 | 5.27 (3.40, 8.62) | 5.282 / 5.296 | 8.604 / 8.651 |
| 3000 | lower95 | 0.0031 | 1.079 | 2.14 (1.44, 3.26) | 8.859 / 8.878 | 13.975 / 14.041 |
| 3000 | central | 0.1212 | 1.038 | 2.22 (1.50, 3.38) | 8.859 / 8.877 | 13.975 / 14.040 |
| 3000 | upper95 | 0.6754 | 0.796 | 3.19 (2.08, 5.20) | 8.856 / 8.875 | 13.975 / 14.040 |

The lambda=-1 exclusion (reduced coupling model, QCD lost-lepton groups scaled to the same interval ends) is INSENSITIVE to the lost-lepton level; the Z0 / mu95 columns move.
