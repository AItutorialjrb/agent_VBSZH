# 07 — Sensitivity, robustness and coupling interpretation (single_r1, WH)

**Date:** 2026-11-14 10:53 UTC. **Status: PASS** (expected results only; Asimov; no observed data).
**Definitions:** (a) signal = EW W±Hjj, QCD W±H(+jets, MLM) is a resonant background; (b) signal = EW + QCD W±H. W→τν feed-down is background in both (it scales with the couplings in §3).

## 1. Counting (PRIMARY: Eq. 1, stat. only ± MC stat) and m_γγ profile-likelihood fit (supplementary)
Final selection: BDT (05 §6). Eq. 1: Z = √(2((s+b)ln(1+s/b) − s)); Z(σ_b) with the full background uncertainty; μ95: median expected exact-Poisson CLs with log-normal s and b marginalisation ("syst") and without ("stat").
| L [fb⁻¹] | def | s | b | σ_b | Z Eq. 1 ± MC | Z (σ_b) | μ95 CLs (syst) | μ95 CLs (stat) | Z fit (syst) | μ95 fit (syst) |
|---|---|---|---|---|---|---|---|---|---|---|
| 500 | a | 1.19 | 1.26 | 0.26 | 0.94 ± 0.01 | 0.91 | 3.50 | 3.37 | 0.90 | 3.11 |
| 500 | b | 1.27 | 1.18 | 0.25 | 1.02 ± 0.02 | 0.99 | 3.30 | 3.18 | 0.98 | 2.85 |
| 1000 | a | 2.38 | 2.53 | 0.53 | 1.33 ± 0.02 | 1.24 | 2.03 | 1.93 | 1.27 | 1.94 |
| 1000 | b | 2.54 | 2.37 | 0.50 | 1.44 ± 0.03 | 1.35 | 1.93 | 1.84 | 1.38 | 1.78 |
| 3000 | a | 7.15 | 7.58 | 1.58 | 2.30 ± 0.04 | 1.93 | 1.06 | 0.95 | 2.15 | 0.99 |
| 3000 | b | 7.62 | 7.10 | 1.49 | 2.50 ± 0.04 | 2.11 | 1.02 | 0.92 | 2.35 | 0.89 |

Fit stat-only (continuum still floating): Z = 0.91, 1.28, 2.22, 0.98, 1.39, 2.41; μ95 = 3.01, 1.87, 0.94, 2.77, 1.72, 0.85 (same order as above).
**Cut-based selection (reported alongside the BDT):**
| L [fb⁻¹] | def | s | b | σ_b | Z Eq. 1 ± MC | Z (σ_b) | μ95 CLs (syst) | μ95 CLs (stat) |  |  |
|---|---|---|---|---|---|---|---|---|---|---|
| 500 | a | 0.81 | 1.73 | 0.66 | 0.58 ± 0.01 | 0.51 | 5.07 | 6.10 |  |  |
| 500 | b | 0.87 | 1.67 | 0.64 | 0.62 ± 0.01 | 0.55 | 4.75 | 4.48 |  |  |
| 1000 | a | 1.63 | 3.46 | 1.32 | 0.82 ± 0.02 | 0.65 | 3.56 | 3.19 |  |  |
| 1000 | b | 1.74 | 3.35 | 1.27 | 0.88 ± 0.02 | 0.71 | 3.34 | 3.01 |  |  |
| 3000 | a | 4.88 | 10.38 | 3.95 | 1.41 ± 0.03 | 0.86 | 2.12 | 1.61 |  |  |
| 3000 | b | 5.21 | 10.05 | 3.82 | 1.53 ± 0.03 | 0.93 | 1.82 | 1.55 |  |  |

Figure: `figures/p07_mgg_final.png` (expected m_γγ at the final selection, 500 fb⁻¹).

## 2. Robustness (Eq. 1 and Z(σ_b), μ95 CLs syst)
| variant | L | def | s | b | Z Eq. 1 | Z (σ_b) | μ95 |
|---|---|---|---|---|---|---|---|
| nominal | 500 | a | 1.19 | 1.26 | 0.94 | 0.91 | 3.50 |
| nominal | 500 | b | 1.27 | 1.18 | 1.02 | 0.99 | 3.30 |
| nominal | 3000 | a | 7.15 | 7.58 | 2.30 | 1.93 | 1.06 |
| nominal | 3000 | b | 7.62 | 7.10 | 2.50 | 2.11 | 1.02 |
| j->gamma x0.3 (low) | 500 | a | 1.19 | 1.18 | 0.96 | 0.93 | 3.53 |
| j->gamma x0.3 (low) | 500 | b | 1.27 | 1.10 | 1.05 | 1.02 | 3.32 |
| j->gamma x0.3 (low) | 3000 | a | 7.15 | 7.09 | 2.36 | 2.01 | 1.09 |
| j->gamma x0.3 (low) | 3000 | b | 7.62 | 6.62 | 2.56 | 2.20 | 0.92 |
| j->gamma x3 (high) | 500 | a | 1.19 | 1.60 | 0.85 | 0.79 | 3.44 |
| j->gamma x3 (high) | 500 | b | 1.27 | 1.52 | 0.92 | 0.85 | 3.24 |
| j->gamma x3 (high) | 3000 | a | 7.15 | 9.61 | 2.08 | 1.46 | 1.27 |
| j->gamma x3 (high) | 3000 | b | 7.62 | 9.14 | 2.26 | 1.57 | 1.22 |
| j->gamma Delphes-measured rate (FORMAT 6a) | 500 | a | 1.19 | 1.16 | 0.97 | 0.94 | 3.53 |
| j->gamma Delphes-measured rate (FORMAT 6a) | 500 | b | 1.27 | 1.08 | 1.05 | 1.02 | 3.33 |
| j->gamma Delphes-measured rate (FORMAT 6a) | 3000 | a | 7.15 | 6.98 | 2.37 | 2.02 | 1.10 |
| j->gamma Delphes-measured rate (FORMAT 6a) | 3000 | b | 7.62 | 6.50 | 2.58 | 2.21 | 0.93 |
| e->gamma 1 % (low) | 500 | a | 1.19 | 1.24 | 0.94 | 0.91 | 3.51 |
| e->gamma 1 % (low) | 500 | b | 1.27 | 1.16 | 1.03 | 0.99 | 3.31 |
| e->gamma 1 % (low) | 3000 | a | 7.15 | 7.46 | 2.31 | 1.95 | 1.07 |
| e->gamma 1 % (low) | 3000 | b | 7.62 | 6.99 | 2.51 | 2.13 | 1.03 |
| e->gamma 5 % (high) | 500 | a | 1.19 | 1.32 | 0.92 | 0.89 | 3.49 |
| e->gamma 5 % (high) | 500 | b | 1.27 | 1.24 | 1.00 | 0.96 | 3.29 |
| e->gamma 5 % (high) | 3000 | a | 7.15 | 7.93 | 2.26 | 1.85 | 1.18 |
| e->gamma 5 % (high) | 3000 | b | 7.62 | 7.46 | 2.45 | 2.02 | 1.01 |
| e->gamma Delphes-measured rate (FORMAT 6b) | 500 | a | 1.19 | 1.35 | 0.91 | 0.88 | 3.48 |
| e->gamma Delphes-measured rate (FORMAT 6b) | 500 | b | 1.27 | 1.27 | 0.99 | 0.95 | 3.28 |
| e->gamma Delphes-measured rate (FORMAT 6b) | 3000 | a | 7.15 | 8.09 | 2.24 | 1.82 | 1.17 |
| e->gamma Delphes-measured rate (FORMAT 6b) | 3000 | b | 7.62 | 7.62 | 2.43 | 1.97 | 1.00 |
| j->lepton 3e-5 (low) | 500 | a | 1.19 | 1.22 | 0.95 | 0.92 | 3.51 |
| j->lepton 3e-5 (low) | 500 | b | 1.27 | 1.15 | 1.03 | 1.00 | 3.31 |
| j->lepton 3e-5 (low) | 3000 | a | 7.15 | 7.35 | 2.33 | 1.97 | 1.07 |
| j->lepton 3e-5 (low) | 3000 | b | 7.62 | 6.87 | 2.53 | 2.15 | 1.03 |
| j->lepton 1e-3 (high) | 500 | a | 1.19 | 1.44 | 0.89 | 0.84 | 3.47 |
| j->lepton 1e-3 (high) | 500 | b | 1.27 | 1.36 | 0.96 | 0.91 | 3.27 |
| j->lepton 1e-3 (high) | 3000 | a | 7.15 | 8.65 | 2.18 | 1.65 | 1.16 |
| j->lepton 1e-3 (high) | 3000 | b | 7.62 | 8.18 | 2.36 | 1.78 | 1.12 |
| all fake/mis-ID rates high | 500 | a | 1.19 | 1.84 | 0.80 | 0.73 | 4.35 |
| all fake/mis-ID rates high | 500 | b | 1.27 | 1.76 | 0.87 | 0.79 | 4.11 |
| all fake/mis-ID rates high | 3000 | a | 7.15 | 11.04 | 1.97 | 1.31 | 1.33 |
| all fake/mis-ID rates high | 3000 | b | 7.62 | 10.57 | 2.12 | 1.41 | 1.28 |
| stock Delphes object efficiencies (no CMS-like reweighting) | 500 | a | 0.79 | 0.84 | 0.76 | 0.75 | 5.48 |
| stock Delphes object efficiencies (no CMS-like reweighting) | 500 | b | 0.85 | 0.79 | 0.83 | 0.81 | 5.14 |
| stock Delphes object efficiencies (no CMS-like reweighting) | 3000 | a | 4.76 | 5.06 | 1.87 | 1.65 | 1.43 |
| stock Delphes object efficiencies (no CMS-like reweighting) | 3000 | b | 5.09 | 4.73 | 2.04 | 1.80 | 1.17 |
| conservative: N_eff<10 sources at max(value, 3 w̄), zero-support at 3 w̄ | 500 | a | 1.19 | 1.88 | 0.79 | 0.70 | 4.37 |
| conservative: N_eff<10 sources at max(value, 3 w̄), zero-support at 3 w̄ | 500 | b | 1.27 | 1.81 | 0.86 | 0.75 | 4.12 |
| conservative: N_eff<10 sources at max(value, 3 w̄), zero-support at 3 w̄ | 3000 | a | 7.15 | 11.30 | 1.95 | 1.17 | 1.51 |
| conservative: N_eff<10 sources at max(value, 3 w̄), zero-support at 3 w̄ | 3000 | b | 7.62 | 10.83 | 2.10 | 1.25 | 1.32 |
| QCD WH x2 (def. a background) | 500 | a | 1.19 | 1.34 | 0.92 | 0.88 | 3.48 |
| QCD WH x2 (def. a background) | 500 | b | 1.35 | 1.18 | 1.07 | 1.04 | 3.11 |
| QCD WH x2 (def. a background) | 3000 | a | 7.15 | 8.05 | 2.24 | 1.87 | 1.16 |
| QCD WH x2 (def. a background) | 3000 | b | 8.10 | 7.10 | 2.63 | 2.22 | 0.96 |
| cut-based selection (no BDT) | 500 | a | 0.81 | 1.73 | 0.58 | 0.54 | 6.41 |
| cut-based selection (no BDT) | 500 | b | 0.87 | 1.67 | 0.62 | 0.59 | 4.68 |
| cut-based selection (no BDT) | 3000 | a | 4.88 | 10.38 | 1.41 | 1.06 | 1.93 |
| cut-based selection (no BDT) | 3000 | b | 5.21 | 10.05 | 1.53 | 1.14 | 1.83 |


## 3. λ_WZ = κ_W/κ_Z and (κ_W, κ_Z)
Coupling samples `K_EW_WHjj_*` (HC_NLO_X0_kVV) through the same selection (BDT scored by the mean of the five fold models). The SR yield is an exact quadratic form Y = α κ_W² + β κ_W κ_Z + γ κ_Z²; α, β, γ fitted to the six λ_WZ points at κ_Z = 1 (χ²/ndf = 0.97/3); closure on independent points (500 fb⁻¹): K_EW_WHjj_kap_W15_Z075: predicted 3.830, sample 3.895 ± 0.032; K_EW_WHjj_kap_W05_Z15: predicted 4.192, sample 4.161 ± 0.029; S_EW_WHjj (SM, separate sample): predicted 1.204, sample 1.192 ± 0.012.
Interpretation model: signal and τν feed-down scale with Y(κ_W, κ_Z)/Y_SM, QCD WH with κ_W², other backgrounds fixed; **BR(H→γγ) fixed to its SM value** (the samples do not include its κ dependence; with κ_γ resolved through the W loop, λ_WZ < 0 would raise BR(H→γγ) by ≈ 2× and strengthen the exclusions — not used). Test statistic: Poisson likelihood ratio on the SM Asimov count with the Gaussian-profiled σ_b.
| L [fb⁻¹] | Z excl. λ_WZ = −1 | Z excl. λ_WZ < 0 (min. at λ) | λ_WZ 68 % interval | λ_WZ 95 % interval |
|---|---|---|---|---|
| 500 | 4.16 | 1.21 (-0.01) | [0.07, 1.48] | [-0.27, 1.82] |
| 1000 | 5.88 | 1.70 (-0.01) | [0.19, 1.37] | [-0.07, 1.63] |
| 3000 | 10.12 | 2.88 (-0.01) | [0.31, 1.24] | [0.14, 1.42] |

The λ_WZ < 0 test is limited by the boundary λ → 0⁻, whose rate (Y(0)/Y(1) = γ/(α+β+γ) = 2.92) is close to the SM; the rate alone cannot separate λ ≈ 0.2–1 (flat valley in `figures/p07_lambdaWZ_scan.png`). (κ_W, κ_Z) 68/95 % contours: `figures/p07_kappa_contours.png`.

## 4. Caveats
Asymptotic fit formulae at O(1–10) events; BDT stability marginal (05 §6); jet-modelling nuisance statistics-limited; rate-only coupling interpretation; BR(H→γγ) fixed; no VH combination here (outside this run's scope).
**Git:** see `git log -- wh/reports/07_sensitivity.md`.
