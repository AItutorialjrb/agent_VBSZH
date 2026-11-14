# 07 Sensitivity (executor-wh FINAL, block 3)
Date UTC: 2026-11-14 09:53. Status: **PASS for verification**; ALL numbers are EXPECTED (Asimov datasets, nominal background model of 05a v2.1 + the v1.1 loose-cut eFake sample, primary = cut-based selection; D44). No claim of a result; a null or sub-1-sigma expectation is stated as such. Analysis commit: ORCH_COMMIT_PLACEHOLDER.
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

With/without MC-stat impact on Z0 at 500 fb^-1 and mu95 is in 06 sec. 4: Barlow-Beeston is mandatory (cut-based b N_eff 63 in v1.1, 135 in v2.1).

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
| -2.0 | 10.3 | 11.3 | 12.2 | 13.2 | 14.1 | 15.0 | 15.8 | 16.7 |
| -1.5 | 7.1 | 8.0 | 8.9 | 9.8 | 10.7 | 11.5 | 12.3 | 13.0 |
| -1.0 | 3.8 | 4.6 | 5.4 | 6.2 | 7.0 | 7.7 | 8.4 | 9.0 |
| -0.5 | 1.1 | 1.7 | 2.2 | 2.7 | 3.2 | 3.7 | 4.2 | 4.7 |
| +0.0 | 0.4 | 0.4 | 0.3 | 0.4 | 0.4 | 0.6 | 0.7 | 0.8 |
| +0.5 | 0.4 | 0.4 | 0.4 | 0.3 | 0.3 | 0.4 | 0.6 | 0.7 |
| +1.0 | 1.1 | 0.6 | 0.2 | 0.0 | 0.2 | 0.7 | 1.2 | 1.7 |
| +1.5 | 3.6 | 2.9 | 2.2 | 1.6 | 1.2 | 1.1 | 1.4 | 1.9 |
| +2.0 | 6.6 | 5.8 | 4.9 | 4.2 | 3.5 | 3.0 | 2.7 | 2.7 |
| +2.5 | 9.6 | 8.8 | 7.9 | 7.0 | 6.2 | 5.5 | 4.9 | 4.4 |
| +3.0 | 12.5 | 11.6 | 10.7 | 9.9 | 9.0 | 8.2 | 7.5 | 6.8 |
(entries are Z = sqrt(q); the SM point (1, 1) is 0 by construction; |kW| ~ 0.2-0.5 with kZ ~ 1 and the kW<0 sector near kW ~ 0 are not excluded, in line with the lambda<0 result.)

Leave-one-out closure of the per-bin quadratic (LSQ covariance included): totals |pull| <= 1.6; per-bin pulls up to 3.3.

### D36 scans for the lambda<0 exclusion (reduced coupling model, kW-sign convention)

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

### D36 scans for the lambda<0 exclusion, kZ convention (PRIMARY; reduced coupling model)

| kind | f | Z(lambda=-1) | Z(lambda=0) | Z(lambda=0.5) |
|---|---|---|---|---|
| fake | 0.3 | 3.77 | 0.37 | 0.62 |
| fake | 0.5 | 3.77 | 0.37 | 0.62 |
| fake | 1.0 | 3.76 | 0.37 | 0.61 |
| fake | 2.0 | 3.76 | 0.37 | 0.61 |
| fake | 3.0 | 3.75 | 0.36 | 0.61 |
| fake | 10.0 (beyond D36) | 3.70 | 0.32 | 0.58 |
| fake | 30.0 (beyond D36) | 3.50 | 0.24 | 0.50 |
| fake | 100.0 (beyond D36) | 2.93 | 0.12 | 0.30 |
| npl | 0.3 | 3.77 | 0.37 | 0.61 |
| npl | 0.5 | 3.76 | 0.37 | 0.61 |
| npl | 1.0 | 3.76 | 0.37 | 0.61 |
| npl | 2.0 | 3.76 | 0.37 | 0.61 |
| npl | 3.0 | 3.76 | 0.37 | 0.61 |
| npl | 10.0 (beyond D36) | 3.75 | 0.35 | 0.61 |
| npl | 30.0 (beyond D36) | 3.72 | 0.31 | 0.59 |
| npl | 100.0 (beyond D36) | 3.61 | 0.22 | 0.55 |

## 6. Mass-resolution dependence (signal m_gg smeared about 125 GeV by r; 500 fb^-1, def. a)

| r | s (+-3.5 window) | b | Z Eq. 1 | Z0 PL | mu95 median |
|---|---|---|---|---|---|
| 0.8 | 0.649 | 1.797 | 0.459 | 0.468 | 6.58 |
| 1.0 | 0.612 | 1.797 | 0.434 | 0.427 | 7.09 |
| 1.25 | 0.556 | 1.797 | 0.396 | 0.387 | 7.61 |
| 1.5 | 0.502 | 1.797 | 0.359 | 0.357 | 8.02 |
| 2.0 | 0.413 | 1.797 | 0.297 | 0.312 | 8.65 |

## 7. Caveats / what this is not
Expected only; the sensitivity is below 1 sigma at 500 fb^-1 and about 1 sigma at 3000 fb^-1 (PL, cut-based): no evidence is expected and none is claimed. Delphes-level, LO, no pile-up. ASSUMPTION nuisances (lumi, photon/lepton efficiency, mass scale/resolution) have no data basis. **The v1.1 lost-lepton class has N_eff = 7.6 at the selection, below the SPEC sec. 4.3 standard N_eff >= 10 (36 % MC stat; its QCD part is one raw row); the v1 estimate (vbs x C) is carried as the robustness row in 06 sec. 5; the v1.1 nominal is kept (pre-declared by 04:139 and D45).** Signal definition (b) adds QCD WHjj (H_QCD_WH_mlm) as signal; its interference (-0.3 % of EW) is neglected. The v1.1 row F_QCD_llajj_loose IS included (replaces the QCD part of ZH_Zajj_eFake; all numbers in this report are the v1.1 evaluation, files *_v11.json; D45 trigger not fired); H_ggF_jj is NOT in the nominal: its gridpack (893012) failed, the D38 scaled central proxy (05a sec. 12, 0.024 events in the window, +1.3 % of b) is a bound variant that lowers Z0 by about 0.6 % (work/stat/ggf_variant_v11.json). MVA alternative not carried through the statistics here (D44: alternative only). Figures: figures/mgg_selection, Z_vs_lumi, d36_*, lambda_exclusion*.

## 8. Next
Verification; VH combination with the frozen ZH (swappable ZH table); comparison with CMS/ATLAS; reproducibility and FINAL report; v1.1 re-evaluations.
