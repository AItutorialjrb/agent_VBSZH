# 07 Sensitivity (executor-wh FINAL, block 3)
Date UTC: 2026-11-09 09:01. Status: **PASS for verification**; ALL numbers are EXPECTED (Asimov datasets, nominal background model of 05a v2.1, primary = cut-based selection; D44). No claim of a result; a null or sub-1-sigma expectation is stated as such. Git commit: see orchestrator commit.
## Selection (frozen in 05): mjj>600, |deta_jj|>4.0, pT(gg)>75, MET>30, pT(l)>25, |m_gg-125|<3.5 (counting); MVA alternative not adopted.
## 1. Counting window (Eq. 1, stat only) and exact-Poisson CLs
Window yields at 500 fb^-1: s = 0.612, b = 1.797 +- 0.227 (MC stat).
| L [fb^-1] | s | b | Z Eq. 1 | Z (b -MC, b +MC) | exact-Poisson counting CLs mu95 (q16, median, q84) | def (b): s, b, Z, mu95 median |
|---|---|---|---|---|---|---|
| 500 | 0.612 | 1.797 | 0.434 | 0.461, 0.411 | 4.89, 8.04, 10.01 | 0.683, 1.726, 0.490, 7.26 |
| 1000 | 1.225 | 3.594 | 0.614 | 0.652, 0.581 | 3.49, 4.19, 5.88 | 1.367, 3.452, 0.694, 3.80 |
| 3000 | 3.674 | 10.783 | 1.063 | 1.129, 1.007 | 1.69, 2.31, 3.11 | 4.100, 10.357, 1.201, 1.92 |

NOT the same quantity as the profile-likelihood mu95 of sec. 2 (asymptotic q~ CLs on the m_gg shape fit, pyhf). The Poisson 'q16/q84' columns are the observed-count quantiles of Poisson(b) mapped to mu95 (discrete).

## 2. Profile likelihood (m_gg 100-180 GeV, 40 bins, all nuisances of 06 + Barlow-Beeston)

| L | def | expected Z0 | PL asymptotic (q~) CLs mu95 median (-1s, +1s) | Z0 stat-only | Z0 without MC stat | Z0 MC-stat only |
|---|---|---|---|---|---|---|
| 500 | a | 0.427 | 7.10 (4.46, 11.59) | 0.444 | 0.432 | 0.439 |
| 1000 | a | 0.592 | 4.55 (2.92, 7.37) | 0.627 | 0.604 | 0.615 |
| 3000 | a | 0.973 | 2.50 (1.68, 3.84) | 1.087 | 1.033 | 1.027 |
| 500 | b | 0.484 | 6.05 (3.93, 10.24) | 0.503 | 0.489 | 0.498 |
| 1000 | b | 0.671 | 3.97 (2.62, 6.22) | 0.711 | 0.684 | 0.697 |
| 3000 | b | 1.103 | 2.17 (1.44, 3.40) | 1.232 | 1.170 | 1.166 |

With/without MC-stat impact on Z0 at 500 fb^-1 and mu95 is in 06 sec. 4: Barlow-Beeston is mandatory (cut-based b N_eff 135).

## 3. D36 scan: fake photons (per-photon rate x f; one-fake x f, two-fake x f^2), 500 fb^-1 (def. a, PL with all nuisances)
D36 range x0.3-x3; f = 10, 30, 100 are BEYOND D36 (robustness only).

| f | Z0 (PL) | mu95 median (-1s, +1s) | Z Eq. 1 counting | b window |
|---|---|---|---|---|
| 0.3 | 0.429 | 7.08 (4.44, 11.56) | 0.436 | 1.776 |
| 0.5 | 0.429 | 7.08 (4.45, 11.57) | 0.436 | 1.782 |
| 1.0 | 0.427 | 7.10 (4.46, 11.59) | 0.434 | 1.797 |
| 2.0 | 0.424 | 7.14 (4.50, 11.63) | 0.430 | 1.829 |
| 3.0 | 0.421 | 7.18 (4.53, 11.67) | 0.427 | 1.862 |
| 10.0 (beyond D36) | 0.396 | 7.49 (4.79, 11.98) | 0.401 | 2.137 |
| 30.0 (beyond D36) | 0.322 | 8.46 (5.60, 13.20) | 0.326 | 3.336 |
| 100.0 (beyond D36) | 0.174 | 13.94 (9.43, 21.41) | 0.173 | 12.348 |

## 3. D36 scan: fake photons (per-photon rate x f; one-fake x f, two-fake x f^2), 3000 fb^-1 (def. a, PL with all nuisances)
D36 range x0.3-x3; f = 10, 30, 100 are BEYOND D36 (robustness only).

| f | Z0 (PL) | mu95 median (-1s, +1s) | Z Eq. 1 counting | b window |
|---|---|---|---|---|
| 0.3 | 0.978 | 2.50 (1.67, 3.83) | 1.069 | 10.655 |
| 0.5 | 0.977 | 2.50 (1.67, 3.84) | 1.067 | 10.691 |
| 1.0 | 0.973 | 2.50 (1.68, 3.84) | 1.063 | 10.783 |
| 2.0 | 0.967 | 2.52 (1.69, 3.86) | 1.054 | 10.973 |
| 3.0 | 0.960 | 2.53 (1.70, 3.87) | 1.046 | 11.172 |
| 10.0 (beyond D36) | 0.910 | 2.63 (1.77, 3.98) | 0.982 | 12.823 |
| 30.0 (beyond D36) | 0.759 | 3.04 (2.07, 4.65) | 0.798 | 20.017 |
| 100.0 (beyond D36) | 0.420 | 5.33 (3.70, 7.86) | 0.423 | 74.089 |

## 3. D36 scan: non-prompt leptons (light misID and heavy flavour x f), 500 fb^-1 (def. a, PL with all nuisances)
D36 range x0.3-x3; f = 10, 30, 100 are BEYOND D36 (robustness only).

| f | Z0 (PL) | mu95 median (-1s, +1s) | Z Eq. 1 counting | b window |
|---|---|---|---|---|
| 0.3 | 0.429 | 7.09 (4.45, 11.57) | 0.436 | 1.783 |
| 0.5 | 0.428 | 7.09 (4.45, 11.58) | 0.435 | 1.787 |
| 1.0 | 0.427 | 7.10 (4.46, 11.59) | 0.434 | 1.797 |
| 2.0 | 0.425 | 7.13 (4.48, 11.61) | 0.432 | 1.818 |
| 3.0 | 0.424 | 7.15 (4.50, 11.64) | 0.429 | 1.838 |
| 10.0 (beyond D36) | 0.411 | 7.31 (4.64, 11.80) | 0.415 | 1.983 |
| 30.0 (beyond D36) | 0.377 | 7.73 (4.99, 12.23) | 0.380 | 2.397 |
| 100.0 (beyond D36) | 0.303 | 8.73 (5.82, 14.01) | 0.305 | 3.843 |

## 3. D36 scan: non-prompt leptons (light misID and heavy flavour x f), 3000 fb^-1 (def. a, PL with all nuisances)
D36 range x0.3-x3; f = 10, 30, 100 are BEYOND D36 (robustness only).

| f | Z0 (PL) | mu95 median (-1s, +1s) | Z Eq. 1 counting | b window |
|---|---|---|---|---|
| 0.3 | 0.976 | 2.50 (1.67, 3.84) | 1.067 | 10.696 |
| 0.5 | 0.975 | 2.50 (1.67, 3.84) | 1.066 | 10.721 |
| 1.0 | 0.973 | 2.50 (1.68, 3.84) | 1.063 | 10.783 |
| 2.0 | 0.969 | 2.51 (1.68, 3.85) | 1.057 | 10.907 |
| 3.0 | 0.965 | 2.52 (1.69, 3.86) | 1.052 | 11.031 |
| 10.0 (beyond D36) | 0.937 | 2.57 (1.73, 3.92) | 1.016 | 11.899 |
| 30.0 (beyond D36) | 0.868 | 2.71 (1.84, 4.07) | 0.931 | 14.379 |
| 100.0 (beyond D36) | 0.715 | 3.25 (2.22, 4.93) | 0.746 | 23.061 |

## 4. Couplings (lambda_WZ, kappa_W/kappa_Z) from the direct samples, 500 fb^-1, expected, SM data (Asimov)
**The coupling fit uses a REDUCED nuisance model** (per-class background normalisations with the 05a VBS class-bound widths, signal theory 5 %, lumi 2.5 % (ASSUMPTION), Barlow-Beeston-lite), not the full 06 pyhf model; the stat-only, MC-stat-only and reduced results differ by <= 2 % in Z (table below), the additional nuisances of 06 are sub-dominant in the ranking of 06 sec. 3 but are not propagated here. Method (scripts/coup_run.py): per-bin quadratic Y_i = alpha_i kW^2 + beta_i kW kZ + gamma_i kZ^2 from the 8 CP-even points (weighted LSQ), x R_BR(kW,kZ) = analytic H->gamma gamma branching-ratio and total-width kappa dependence (A_W = -8.32 kW, A_t = +1.84 kt (standard H->gamma gamma loop functions, e.g. A. Djouadi, Phys. Rept. 457 (2008) 1, hep-ph/0503172; recomputed here with mH = 125 GeV, mW = 80.4 GeV, mt = 172.5 GeV: tau_W = mH^2/4mW^2 = 0.604 gives -8.32, tau_t = 0.131 with N_c Q_t^2 = 4/3 gives +1.84; the reference was not re-read for equation numbers); YR4 BRs (LHCHWG, mH = 125 GeV); kb=kt=ktau=kc=1). **The production samples carry the SM BR in k only; R_BR is an analytic correction applied on top (it matters: R_BR(lambda=-1) = 2.45, R_BR(0) = 0.10, R_BR(0.5) = 0.15).** Primary = with R_BR; the numbers without it (as the samples are) are given for transparency. c_A (CP-odd) is not done: only 2 CP-odd points exist (cost: >= 3 further points per axis; not cheap).
Binning chosen BEFORE the fit by the expected Asimov exclusion of lambda=-1 (stat + MC bkg): mtwgg (candidates q(lambda=-1): {"mjj": 34.3, "ptgg": 37.2, "mtwgg": 39.9}), edges [0, 250, 350, 450, 100000.0].
| | with R_BR (primary) | without R_BR (samples as is) |
|---|---|---|
| stat_only: Z(lambda=-1), Z(lambda=0), Z(lambda<0 region = its closest point lambda=0) | 6.32, 0.38, 0.38 | 3.80, 1.61, 1.61 |
| MCstat_only: Z(lambda=-1), Z(lambda=0), Z(lambda<0 region = its closest point lambda=0) | 6.32, 0.38, 0.38 | 3.79, 1.61, 1.61 |
| reduced_model: Z(lambda=-1), Z(lambda=0), Z(lambda<0 region = its closest point lambda=0) | 6.20, 0.37, 0.37 | 3.76, 1.61, 1.61 |

Expected exclusion Z(lambda) (reduced coupling model, with R_BR): -2.00: 13.17, -1.50: 9.83, -1.00: 6.20, -0.50: 2.70, +0.00: 0.37, +0.50: 0.33, +1.50: 1.61, +2.00: 4.17, +2.50: 7.02, +3.00: 9.87

**Closure sensitivity (the lambda<0 number is set at lambda about 0, where the leave-one-out per-bin pulls reach 3.2 sigma):** scaling the predicted signal of the TESTED hypothesis by 0.7 / 1.0 / 1.3 gives Z(lambda=0) = 0.35 / 0.37 / 0.41 and Z(lambda=-1) = 5.1 / 6.2 / 7.1: a +-30 % closure systematic changes the lambda<0 number by about +-0.04 sigma and lambda=-1 by about +-1 sigma, i.e. the qualitative statements stand but the quoted decimals are not meaningful.

**Interpretation:** lambda_WZ = -1 is expected to be excluded at a high level, because the W-loop/interference makes BR(gamma gamma) and the VBS-like yield and the high-pT(gg)/mT shapes very different; the whole negative range cannot be excluded better than its boundary point lambda=0 (0.4 sigma with R_BR): at lambda about 0.2 the H->gamma gamma amplitude cancels (A_W + A_t = 0) and the signal vanishes. This is an expected-sensitivity statement for the SM hypothesis, not a result.

Leave-one-out closure of the per-bin quadratic (LSQ-covariance included): totals |pull| <= 1.6; per-bin pulls up to 3.3 (bins at lambda=0 and -0.5 where the point yields are small/low-weight): a closure caveat, quoted not hidden.

### D36 scans for the lambda<0 exclusion (reduced coupling model, primary)

| kind | f | Z(lambda=-1) | Z(lambda=0) | Z(lambda=0.5) |
|---|---|---|---|---|
| fake | 0.3 | 6.20 | 0.37 | 0.34 |
| fake | 0.5 | 6.20 | 0.37 | 0.34 |
| fake | 1.0 | 6.20 | 0.37 | 0.33 |
| fake | 2.0 | 6.19 | 0.37 | 0.33 |
| fake | 3.0 | 6.19 | 0.36 | 0.32 |
| fake | 10.0 (beyond D36) | 6.12 | 0.32 | 0.26 |
| fake | 30.0 (beyond D36) | 5.86 | 0.24 | 0.15 |
| fake | 100.0 (beyond D36) | 5.18 | 0.12 | 0.05 |
| npl | 0.3 | 6.20 | 0.37 | 0.34 |
| npl | 0.5 | 6.20 | 0.37 | 0.33 |
| npl | 1.0 | 6.20 | 0.37 | 0.33 |
| npl | 2.0 | 6.20 | 0.37 | 0.33 |
| npl | 3.0 | 6.19 | 0.37 | 0.33 |
| npl | 10.0 (beyond D36) | 6.18 | 0.35 | 0.31 |
| npl | 30.0 (beyond D36) | 6.14 | 0.31 | 0.26 |
| npl | 100.0 (beyond D36) | 5.99 | 0.22 | 0.15 |

## 6. Mass-resolution dependence (signal m_gg smeared about 125 GeV by r; 500 fb^-1, def. a)

| r | s (+-3.5 window) | b | Z Eq. 1 | Z0 PL | mu95 median |
|---|---|---|---|---|---|
| 0.8 | 0.649 | 1.797 | 0.459 | 0.468 | 6.58 |
| 1.0 | 0.612 | 1.797 | 0.434 | 0.427 | 7.09 |
| 1.25 | 0.556 | 1.797 | 0.396 | 0.387 | 7.61 |
| 1.5 | 0.502 | 1.797 | 0.359 | 0.357 | 8.02 |
| 2.0 | 0.413 | 1.797 | 0.297 | 0.312 | 8.65 |

## 7. Caveats / what this is not
Expected only; the sensitivity is below 1 sigma at 500 fb^-1 and about 1 sigma at 3000 fb^-1 (PL, cut-based): no evidence is expected and none is claimed. Delphes-level, LO, no pile-up. ASSUMPTION nuisances (lumi, photon/lepton efficiency, mass scale/resolution) have no data basis. Signal definition (b) adds QCD WHjj (H_QCD_WH_mlm) as signal; its interference (-0.3 % of EW) is neglected. The v1.1 row F_QCD_llajj_loose IS included (replaces the QCD part of ZH_Zajj_eFake; all numbers in this report are the v1.1 evaluation, files *_v11.json; D45 trigger not fired); H_ggF_jj is not yet included (cluster 893012, D38 fallback). MVA alternative not carried through the statistics here (D44: alternative only). Figures: figures/mgg_selection, Z_vs_lumi, d36_*, lambda_exclusion*.

## 8. Next
Verification; VH combination with the frozen ZH (swappable ZH table); comparison with CMS/ATLAS; reproducibility and FINAL report; v1.1 re-evaluations.
