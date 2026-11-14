# 06 — Mass window, sidebands and systematic model (single_r1, WH)

**Date:** 2026-11-14 10:53 UTC. **Status: PASS** (systematic model implemented for counting and the m_γγ fit; theory from the samples' own weights; all assumptions listed).
**Goal:** window/sideband definition and the nuisance model for 07.

## 1. Window and sidebands
Window 120.93–129.05 GeV = μ ± 2σ_core of the Delphes EW signal (μ = 124.99, σ_core = 2.03 GeV); fit range 105–160 GeV; sidebands = fit range minus window (used by the profile-likelihood fit; continuum normalisation and slope float). Continuum MC shapes: unbinned exponential MLE per component (L1). Resonant shape: two-Gaussian fit to the Delphes signal after the final selection (parameters in p07.json `fit.*.par_signal_shape`). Mass-resolution dependence: ±10 % resolution and ±0.5 % photon energy scale are nuisances (table below) and are profiled in the fit.

## 2. Nuisances (counting; absolute effect on the 500 fb⁻¹ SR yields, def. a; sum over samples within a nuisance)
| nuisance | Δb (events) | Δs (events) |
|---|---|---|
| jetmod | 0.191 | — |
| ps_sig | 0.012 | 0.119 |
| th_sig | 0.011 | 0.104 |
| shape_jes | 0.063 | 0.036 |
| fake_jg1 | 0.088 | — |
| eff_obj | 0.041 | 0.041 |
| lumi | 0.032 | 0.030 |
| th_fake | 0.055 | — |
| th_ewaa | 0.049 | — |
| fake_jl | 0.045 | — |
| fake_eg | 0.039 | — |
| l2_V_WWa_WH | 0.036 | — |
| ps_V_WWa_WH | 0.036 | — |
| shape_pes | 0.023 | 0.012 |
| shape_res | 0.008 | 0.027 |
| th_qcdaa | 0.032 | — |
| fake_jg2 | 0.031 | — |
| l2_F_QCD_llajj_loose | 0.025 | — |
| l2_F_QCD_Wajjj_nomjj | 0.018 | — |
| ps_F_EW_Wajj_nomjj | 0.017 | — |
| ps_H_VBFH_jj | 0.016 | — |
| ps_H_ggZH_wh | 0.015 | — |
| l2_Q_aajjj | 0.014 | — |
| ps_H_ggF_jj_nomjj | 0.010 | — |

Sizes: luminosity 2.5 % (as ZH, for the VH combination); object efficiencies 2 % per lepton and per photon (prompt objects); theory = 7-point scale envelope ⊕ PDF replica RMS from each sample's own LHE weights in the SR (proxies for samples without weights: fakes → their prompt analogue); fake classes 100 % (j→γ one fake), 150 % (two fakes), 100 % (j→ℓ, e→γ), correlated within a class; PS modelling 100 % for samples whose tag/fake jets come from the shower (V+γ, ggZH, VBF/ggF H fake ℓ, EW Wγjj, D29 rule); generator m_jj>400 correction of the frozen EW Zγγjj / ℓℓγjj rows 6.4 %; L2 components and zero-support sources 100 % each (uncorrelated); MC stat per sample; JES ±5 % (BDT rescored), photon scale ±0.5 %, resolution ±10 % (resonant samples); **jet modelling** (D-WH-14): |1 − ε(QCD WH, MLM)/ε(QCD WHjj, fixed order)| of the selection relative to a loose object region = 0.89 ± 0.19 → 19 % on every background prompt/FL component (cut-based selection: 45 %); **signal PS modelling 10 %** (assumption for EW VBS-type samples: recoil scheme / central jet activity).
Theory per sample (scale, PDF):
| sample | scale | PDF | rows |
|---|---|---|---|
| `B_EW_Waajj_nomjj` | 0.093 | 0.016 | 681 |
| `B_QCD_Waajj_nomjj` | 0.277 | 0.022 | 14 |
| `H_QCD_WH_mlm` | 0.053 | 0.028 | 37 |
| `H_QCD_WHjj_fixed` | 0.281 | 0.015 | 119 |
| `H_ggZH_wh` | 0.281 | 0.010 | 93 |
| `H_tHW_1l` | 0.120 | 0.045 | 27 |
| `H_tHq_lep` | 0.013 | 0.015 | 510 |
| `K_EW_WHjj_cpo_m2` | 0.109 | 0.013 | 5712 |
| `K_EW_WHjj_cpo_p2` | 0.109 | 0.014 | 5739 |
| `K_EW_WHjj_kap_W05_Z15` | 0.097 | 0.012 | 23039 |
| `K_EW_WHjj_kap_W15_Z075` | 0.092 | 0.011 | 16035 |
| `K_EW_WHjj_lam_m050` | 0.099 | 0.011 | 28087 |
| `K_EW_WHjj_lam_m100` | 0.099 | 0.012 | 27305 |
| `K_EW_WHjj_lam_p000` | 0.098 | 0.013 | 27662 |
| `K_EW_WHjj_lam_p050` | 0.094 | 0.011 | 19000 |
| `K_EW_WHjj_lam_p100` | 0.085 | 0.010 | 11241 |
| `K_EW_WHjj_lam_p150` | 0.089 | 0.011 | 13393 |
| `S_EW_WHjj` | 0.087 | 0.010 | 11180 |
| `S_EW_WHjj_taunu` | 0.087 | 0.018 | 708 |
| `ZH_B_QCD_zaajj_nomjj` | 0.309 | 0.017 | 13 |
| `ZH_B_EW_zaajj_vbs_is1h` | 0.102 | 0.067 | 108 |
| `ZH_B_EW_zaajj_vbs_is2` | 0.104 | 0.026 | 131 |
| `ZH_B_EW_zaajj_vbs_is3` | 0.089 | 0.045 | 91 |
| `ZH_ew_zhjj_zll` | 0.096 | 0.011 | 4153 |
| `ZH_qcd_zhjj_zll` | 0.311 | 0.033 | 24 |
| `ZH_B_QCD_zaajj_vbs` | 0.334 | 0.011 | 29 |

Shape-type (500 fb⁻¹ SR, relative; JES/photon scale/resolution):
| sample | JES | γ scale | resolution |
|---|---|---|---|
| `B_EW_Waajj_nomjj` | 0.018 | 0.023 | 0.000 |
| `B_QCD_Waajj_nomjj` | 0.151 | 0.006 | 0.000 |
| `F_EW_Wajj_nomjj` | 0.036 | 0.004 | 0.000 |
| `F_QCD_Wajjj_nomjj` | 0.030 | 0.011 | 0.000 |
| `F_Wjjjj` | 0.016 | 0.013 | 0.000 |
| `H_QCD_WH_mlm` | 0.184 | 0.036 | 0.019 |
| `H_VBFH_jj` | 0.020 | 0.011 | 0.022 |
| `H_ggZH_wh` | 0.037 | 0.034 | 0.022 |
| `H_tHq_lep` | 0.041 | 0.018 | 0.019 |
| `Q_aajjj` | 0.016 | 0.006 | 0.000 |
| `S_EW_WHjj` | 0.030 | 0.010 | 0.022 |
| `S_EW_WHjj_taunu` | 0.037 | 0.016 | 0.026 |
| `V_WWa_WH` | 0.033 | 0.015 | 0.000 |
| `F_QCD_llajj_loose` | 0.031 | 0.005 | 0.000 |
| `ZH_B_EW_zaajj_vbs_is1h` | 0.040 | 0.004 | 0.000 |
| `ZH_B_EW_zaajj_vbs_is2` | 0.039 | 0.013 | 0.000 |
| `ZH_ew_zhjj_zll` | 0.004 | 0.011 | 0.023 |
| `ZH_F_EW_llajj_vbs` | 0.169 | 0.008 | 0.000 |


## 3. Fit model (supplementary result in 07)
Binned (1 GeV) Poisson likelihood in 105–160 GeV, Asimov data; parameters: μ (signal strength), continuum normalisation and exponential slope (free), signal normalisation (Gaussian, σ_s/s from the counting model), resonant-background normalisation (30 %), photon energy scale (0.5 %) and resolution (10 %) acting on the common resonant shape. Z = √q₀ on Asimov s+b; μ95 = median expected from q_μ on Asimov b-only with the asymptotic CLs condition q_μ,A = 1.96². With O(1–10) events the asymptotic formulae are approximate (the counting μ95 uses exact Poisson CLs).

## 4. Checks and caveats
The theory, JES and fake nuisances are evaluated at the final selection; correlations: same nuisance name ⇒ 100 % correlated across samples, s and b. Not included: pile-up, trigger efficiency, b-tag scale factors, κ-dependence of BR(H→γγ). The jet-modelling estimate is statistics-limited (35 / 116 selected MC rows).
**Git:** see `git log -- wh/reports/06_systematics.md`.
