# FINAL report — EW ZHjj (Z→ee/μμ, H→γγ) at √s = 13.6 TeV: Delphes-level feasibility study

- **Date:** 2026-11-02 23:23 UTC
- **Status:** **DRAFT — EW Zγγjj (B_EW_zaajj_vbs_is1-3) gridpacks still integrating; EW Zγγjj not yet in b**. Expected-limit/significance study for the current signal definition (D12 closed).
- **Git commit:** `41898ef`. Reproduction: [08_reproducibility.md](08_reproducibility.md).
- **Inputs:** `work/final_ntuples/final_draft.json` (written by `scripts/analysis/final_analysis.py`), `work/final_ntuples/verify.json`.
- **Comparison:** the reference ZγγJJ study, arXiv:2512.07689, is the methodological reference: same Delphes CMS card, Eq. 1 counting significance and the Fig. 4-style mjj–|Δηjj| scan.
- **Luminosity:** 3000 fb⁻¹ is a pure luminosity scaling at 13.6 TeV, not an HL-LHC detector projection.

## Summary

At the optimised Delphes-level selection, the EW ZHjj signal is **s = 0.081 events at 500 fb⁻¹** and 0.48 at 3000 fb⁻¹. The total background is b = 0.140 (0.84) events.
- **Significance:** Eq. 1 gives Z = 0.20 ± 0.01 (MC) at 500 fb⁻¹ and 0.49 ± 0.03 at 3000 fb⁻¹, for definition (a).
- **s < 1 at every luminosity and for both signal definitions, so Z alone is not a meaningful measure of sensitivity.** The physically meaningful quantity is the expected 95 % CL upper limit on the signal strength.
  - μ₉₅ = 37 at 500 fb⁻¹ and 8.7 at 3000 fb⁻¹ (exact-Poisson CLs, definition a).
  - The median background-only count is 0 at 500 fb⁻¹, so the limit is close to the zero-background value 3/s.
- **The process is not observable at the LHC Run 3 or with 3000 fb⁻¹ in this channel.** The limiting factor is the tiny signal rate: σ×BR×L = 1.44 events produced at 500 fb⁻¹ before any selection. The background model is not the limiting factor.

## 1. Setup

| item | value |
|---|---|
| Stack | LCG_110 x86_64-el9-gcc13-opt; MG5_aMC 3.6.3 (upstream); Pythia 8.317 (CP5); Delphes 3.5.1 with the stock CMS card (slimmed output, physics unchanged, `cards/phase04_candidates/delphes_card_CMS_slim_v1.tcl`); NNPDF3.1 NNLO (LHAID 303600) via LHAPDF 6.5.5. Details: [03_stack.md](03_stack.md). |
| Order | LO for all samples; no k-factors |
| Generation | MG5 gridpacks on HTCondor (EosSubmit). Per job: gridpack → Pythia8 → Delphes → slim/GenTruth friend (`scripts/condor/run_job.sh`) |
| Analysis objects | `scripts/analysis/ntuple.py` (reference Sec. III object definitions): e pT > 15 GeV, \|η\| < 2.5; μ pT > 15 GeV, \|η\| < 2.4; OSSF pair closest to mZ; isolated Delphes photons pT > 20 GeV, \|η\| < 2.5 outside 1.4442–1.566, ΔR(γ,ℓ) > 0.4; anti-kT jets pT > 25 GeV, \|η\| < 4.7, ΔR > 0.4 to the leptons and photons; b-tag \|η\| < 2.5 |
| mγγ peak | Gaussian core fit of the Delphes EW signal: μ = 124.98 GeV, σ = 2.067 ± 0.017 GeV (σ_eff = 2.15 GeV). The stock Delphes CMS card has a worse mγγ resolution than real CMS (about 1.5 GeV). |

## 2. Samples and verification

All final yields come from Delphes reconstructed objects. In the table, N_MC is the number of Delphes events used, and the MC luminosity is N_MC/(σ×BR).
- **Verification** (`scripts/analysis/verify_final.py`): every job is checked for exit, outputs, event counts (n_lhe ≥ 0.9·n_requested, and n_delphes = n_lhe for fixed order) and σ closure (mean Pythia σ vs the gridpack total).
- **Ntuple check:** the event counts in the ntuples equal the verified totals (`N_closure_ok` in the JSON registry).

| process | source | σ [fb] | × BR | N_MC | MC lumi [fb⁻¹] | verification |
|---|---|---|---|---|---|---|
| S_EW_ZHjj | Tier-1 v1 (100 jobs, 200k ev) | 1.295 | 0.002221 | 200000 | 6.96e+07 | Tier-1 / test_v2 (reports 04/05) |
| H_QCD_ZHjj | Tier-1 v1 (50 jobs, 100k ev) | 10.21 | 0.002221 | 100000 | 4.41e+06 | Tier-1 / test_v2 (reports 04/05) |
| H_ggZH | final: gg->ZH loop-induced, Z->ll & H->gg forced in PY8 | 74.33 | 0.0001528 | 20000 | 1.76e+06 | 10/10 jobs OK; σ closure +0.91 % |
| H_ttH | final + test_v2 | 18.11 | 0.00227 | 42000 | 1.02e+06 | 20/20 jobs OK; σ closure -0.12 % |
| H_ZH_tautau | final + test_v2 (MLM) | 24.97 | 0.00227 | 6565 | 1.16e+05 | 4/4 jobs OK (MLM: σ after matching) |
| H_tHW | test_v2 | 0.7868 | 0.00227 | 2000 | 1.12e+06 | Tier-1 / test_v2 (reports 04/05) |
| B_EW_llaajj_is1 | — | — | — | — | — | **not available** (final) |
| B_EW_llaajj_is2 | — | — | — | — | — | **not available** (final) |
| B_EW_llaajj_is3 | — | — | — | — | — | **not available** (final) |
| B_EW_llaajj_is4 | — | — | — | — | — | **not available** (final) |
| B_QCD_Zaajj_vbs | final, fixed order, on-shell Z->ll, VBS-biased generation | 0.0356 | 0.9783 | 100000 | 2.87e+06 | 50/50 jobs OK; σ closure -0.10 % |
| B_QCD_llaa_0j | test_v2 (MLM exclusive 0j) | 1.604 | 1 | 2307 | 1.44e+03 | Tier-1 / test_v2 (reports 04/05) |
| T_ttaa | final + test_v2 | 0.097 | 1 | 22000 | 2.27e+05 | 10/10 jobs OK; σ closure -0.12 % |
| F_QCD_Zajj | final, direct Delphes fakes (VBS-biased generation) | 69.46 | 1 | 5989548 | 8.62e+04 | 2995/3000 jobs OK; σ closure -0.15 % |
| F_EW_Zajj | final, direct Delphes fakes (VBS-biased generation) | 11.05 | 1 | 500000 | 4.52e+04 | 250/250 jobs OK; σ closure -0.12 % |
| T_tta | test_v2 x Delphes TF from F_QCD_Zajj | 85.58 | 1 | 2000 | 23.4 | Tier-1 / test_v2 (reports 04/05) |
| T_tWa | test_v2 x Delphes TF from F_QCD_Zajj | 13.04 | 1 | 2000 | 153 | Tier-1 / test_v2 (reports 04/05) |

- **Dropped segments:** QCD Zγ+jets lost 5 of 3000 segments.
  - 2 segfault deterministically in Delphes for their fixed seed.
  - 3 jobs were lost after the LHE stage.
  - They were not resubmitted; normalisation uses the actual N.
- **Zero-weight samples:** the T_tta and T_tWa test samples (2000 events) are used only through the transfer-factor method (§4).

## 3. Normalisation and branching ratios

- **σ definitions:** σ is the MG5 cross section at the generator cuts, before any BR that is applied in the analysis. The cutflow's first row is σ × BR × L. After-cut yields are in Tables III and IV. These three quantities are kept distinct.
- **B(H→γγ) = 0.002270** is applied **once**, in the analysis (factor k). Pythia forces H→γγ with conditional BR = 1.
- **Z→ℓℓ:**
  - Signal, QCD ZHjj and on-shell-Z Zγγjj: in the MG5 matrix element or decay chain, with ZF = 0.9783 rescaling MG5's width-derived BR to PDG.
  - ggZH: Z undecayed at LHE level, Z→ee/μμ forced in Pythia8, so k = BR(Z→ee+μμ) = 0.067294 × B_γγ.
  - Both lepton flavours are always included; τ is excluded from the signal definition.
- **MLM-merged samples** (ZH→ττ, Zγγ 0j): normalised to the Pythia σ after matching.
- **Weight:** every event has w = σ·k/N_MC. No negative weights at LO.

## 4. Background model and overlap removal

The model is aligned with the reference: prompt Zγ and Zγγ (QCD and EW), tt̄γ, tWγ, tt̄γγ, plus resonant H→γγ backgrounds.

| class | samples | method |
|---|---|---|
| resonant H→γγ | QCD ZHjj (background in def. a), ggZH, tt̄H, ZH(H→γγ, Z→ττ), tHW | direct Delphes counting in the window |
| prompt Zγγ | QCD and EW Zγγjj, on-shell Z→ℓℓ, VBS-biased generation | direct counting, or the mγγ exponential-shape method |
| Zγ + jet→γ fake | QCD and EW Zγjj, VBS-biased generation | **direct Delphes fakes**: the second photon is a Delphes photon from a jet (π⁰/η) |
| tt̄γγ | tt̄γγ | direct, or VBS-factorised |
| tt̄γ, tWγ (one fake) | tt̄γ, tWγ test samples × transfer factor | TF = P(second Delphes photon passes the photon, mℓℓγγ and window cuts \| one-photon level), measured in the direct QCD Zγjj sample; 100 % uncertainty |
| double fakes (Z+jets, tt̄) | — | not in b. Order of magnitude only; the reference also neglects them. Direct Delphes support is zero, and the Phase-05 FF estimate was about 0.02 events at 500 fb⁻¹ |

- **Estimation hierarchy:** recorded per number in Table IV.
  - L0: direct, ≥ 10 raw events in the window.
  - L1: continuum only, N(105–165 GeV) × f_win from an exponential MLE fit of that sample's Delphes mγγ, with ≥ 10 raw events in the wide range.
  - L2: VBS-factorised, 100 % uncertainty.
  - L3: transfer factor.
  - UL: zero support. The central value is 1.14 w_evt (Poisson 68 % CL), with 100 % uncertainty and a 95 % UL of 3 w_evt.
- **Hard/soft photon overlap removal:** uses the GenTruth count of prompt photons (pT > 15 GeV, \|η\| < 2.5, ΔR > 0.4), matching the Zγγ ME phase space.
  - One-ME-photon samples (Zγjj, tt̄γ, tWγ) keep n_prompt ≤ 1.
  - Events with a second hard prompt photon (e.g. from QED shower FSR) are covered by the Zγγ samples and removed.
- **Generator biasing:** the Zγjj and Zγγjj samples are generated with pT(γ) > 25 GeV and mjj > 400 GeV (plus 100 < mγγ < 170 GeV for Zγγ). Every reconstructed selection used stays inside this phase space:
  - pT(γ) ≥ 25 GeV, and pT(γ2)/mγγ > 1/4 implies > 26 GeV in the 105–165 GeV range;
  - mjj ≥ 500 GeV in the scan;
  - the mγγ range is 105–165 GeV.
  - For this reason the reference-like baseline uses photon pT > 25 GeV instead of 20 GeV.
- **Zγγ on-shell Z:** the full ℓℓγγjj gridpack integration projected to 15 h (QCD) and >100 h (EW), so Zγγjj is generated as `p p > z a a j j, z > l+ l-`. Photons radiated in the Z decay are therefore missing. Such events have mℓℓγ or mℓℓγγ ≈ mZ and fail |mℓℓ − mZ| < 25 GeV or mℓℓγγ > 100 GeV; this is a limitation (§8).
- **EW Zγγjj** uses 4 flavours with a 3-way beam-1 split.
- **Fake-factor cross-check (Delphes jets):** in the QCD Zγjj sample with the ff1 mode of `ntuple.py`, f = 5×10⁻⁴, 10⁻³ and 2×10⁻³ plus a pT-dependent variant give 0.0205 events (f = 10⁻³; band 0.0102–0.0409) at the final selection, 500 fb⁻¹. The direct Delphes result is 0.0133. Without the VBS cuts it is 0.128 (direct, 22 raw) vs 0.221 (FF). The Delphes fake rate therefore corresponds to f ≈ 5.8e-04 per jet.

## 5. Selection and optimisation

- **Reference-like baseline** (arXiv:2512.07689 Sec. III):
  - OSSF pair with 70 < mℓℓ < 120 GeV and two photons with pT > 25 GeV (20 GeV in the reference);
  - mℓℓγγ > 100 GeV;
  - ≥ 2 jets with mjj > 700 GeV and |Δηjj| > 2.0;
  - mγγ within ±2σ of the Delphes signal peak.
- **Optimisation** uses expected quantities only, at 500 fb⁻¹ for definition (a); the data are never consulted.
  - Coordinate descent over: the mγγ window (±1.5σ / ±2σ), pT(γ)/mγγ thresholds, the Z window (70–120 GeV or ±25/20/15/10 GeV), the Zeppenfeld z*(γγ) cut, mℓℓγγ, the b-veto, and a joint mjj × |Δηjj| grid.
  - FOM: Z with σ_b (MC-stat ⊕ systematics).
  - **Plateau rule** against noisy scans: among points with Z ≥ 0.97 Z_max, take the one with the largest signal.
- **Optimum:** 2 photons with pT > 25 GeV, pT(γ1)/mγγ > 0.33, pT(γ2)/mγγ > 0.25; |mℓℓ − mZ| < 25 GeV; mℓℓγγ > 100 GeV; no b-veto; no Zeppenfeld cut; mjj > 500 GeV, |Δηjj| > 4.0; 120.8 < mγγ < 129.1 GeV (±2.0σ, σ = 2.07 GeV).
- The mjj × |Δηjj| landscape (Fig. 4-style: `figures/scan_mjj_deta_*.png`, tables below) is flat. At 500 fb⁻¹ all points lie within the MC uncertainty of each other, so the choice of optimum does not affect the conclusions.

## 6. Results

### PRIMARY: Eq. 1 counting significance (stat. only, ± MC stat) and limits

| L [fb⁻¹] | signal definition | s | b | Z_Eq1 ± MC | Z_syst (binned PL fit) | μ₉₅ CLs (exact Poisson, syst) | μ₉₅ (binned PL fit, asymptotic) |
|---|---|---|---|---|---|---|---|
| 500 | (a) EW ZHjj; QCD ZHjj in b | 0.081 | 0.140 | 0.198 ± 0.012 | 0.202 | 37.2 | 27.9 |
| 500 | (b) EW + QCD ZHjj | 0.115 | 0.106 | 0.307 ± 0.022 | 0.313 | 26.1 | 19.0 |
| 1000 | (a) EW ZHjj; QCD ZHjj in b | 0.161 | 0.281 | 0.281 ± 0.017 | 0.285 | 18.6 | 15.5 |
| 1000 | (b) EW + QCD ZHjj | 0.230 | 0.213 | 0.434 ± 0.031 | 0.441 | 13.1 | 10.4 |
| 3000 | (a) EW ZHjj; QCD ZHjj in b | 0.484 | 0.842 | 0.486 ± 0.029 | 0.490 | 8.7 | 6.6 |
| 3000 | (b) EW + QCD ZHjj | 0.689 | 0.638 | 0.752 ± 0.054 | 0.758 | 4.4 | 4.3 |

- **s < 1 in every row:** Z alone is not meaningful.
- **μ₉₅ from exact-Poisson CLs:** counting in the window, with b marginalised over a log-normal(σ_b/b). This is the robust number.
- **Asymptotic fit limit:** uses Asimov asymptotics, which are not valid at these counts. It is shown only because it was requested, and it underestimates the limit.
- **Largest background components** at 500 fb⁻¹, definition (a): H_ggZH 0.0457; H_QCD_ZHjj 0.0341; B_QCD_Zaajj_vbs 0.0190; F_EW_Zajj 0.0165; F_QCD_Zajj 0.0133.

### Table R1 - PRIMARY: Eq. 1 counting significance (stat. only, +- MC stat), 13.6 TeV

| L [fb^-1] | signal def. | s +- MC | b +- MC | Z_Eq1 +- MC | Z_syst (counting, sigma_b) | mu95 CLs (exact Poisson, syst) | median n_obs (b-only) |
|---|---|---|---|---|---|---|---|
| 500 | (a) EW ZHjj; QCD ZHjj in b | 0.081 +- 0.001 | 0.140 +- 0.019 | 0.198 +- 0.012 | 0.198 | 37.2 | 0 |
| 500 | (b) EW+QCD ZHjj | 0.115 +- 0.002 | 0.106 +- 0.019 | 0.307 +- 0.022 | 0.306 | 26.1 | 0 |
| 1000 | (a) EW ZHjj; QCD ZHjj in b | 0.161 +- 0.002 | 0.281 +- 0.038 | 0.281 +- 0.017 | 0.279 | 18.6 | 0 |
| 1000 | (b) EW+QCD ZHjj | 0.230 +- 0.004 | 0.213 +- 0.038 | 0.434 +- 0.031 | 0.431 | 13.1 | 0 |
| 3000 | (a) EW ZHjj; QCD ZHjj in b | 0.484 +- 0.005 | 0.842 +- 0.115 | 0.486 +- 0.029 | 0.480 | 8.7 | 1 |
| 3000 | (b) EW+QCD ZHjj | 0.689 +- 0.013 | 0.638 +- 0.114 | 0.752 +- 0.054 | 0.738 | 4.4 | 0 |

### Table R2 - SUPPLEMENTARY: binned profile-likelihood fit in m_gg (window + sidebands, Asimov, asymptotic)

| L [fb^-1] | signal def. | Z (fit, stat only) | Z_syst (fit) | mu95 (fit, stat only) | mu95 (fit, syst) |
|---|---|---|---|---|---|
| 500 | (a) EW ZHjj; QCD ZHjj in b | 0.202 | 0.202 | 27.9 | 27.9 |
| 500 | (b) EW+QCD ZHjj | 0.314 | 0.313 | 19.0 | 19.0 |
| 1000 | (a) EW ZHjj; QCD ZHjj in b | 0.286 | 0.285 | 15.5 | 15.5 |
| 1000 | (b) EW+QCD ZHjj | 0.444 | 0.441 | 10.4 | 10.4 |
| 3000 | (a) EW ZHjj; QCD ZHjj in b | 0.495 | 0.490 | 6.6 | 6.6 |
| 3000 | (b) EW+QCD ZHjj | 0.768 | 0.758 | 4.3 | 4.3 |

### Table III-like - cutflow at the optimum, 500 fb^-1: expected events (raw MC events)

| step | S_EW_ZHjj | H_QCD_ZHjj | H_ggZH | H_ttH | H_ZH_tautau | H_tHW | B_QCD_Zaajj_vbs | T_ttaa | F_QCD_Zajj | F_EW_Zajj | T_tta | T_tWa |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| N generated x sigma x BR | 1.44 (200000) | 11.3 (100000) | 5.68 (20000) | 20.6 (42000) | 28.3 (6565) | 0.893 (2000) | 17.4 (100000) | 48.5 (22000) | 3.47e+04 (5989548) | 5.52e+03 (500000) | 4.28e+04 (2000) | 6.52e+03 (2000) |
| OSSF + >=2 photons + >=2 jets | 0.199 (27721) | 1.09 (9644) | 0.429 (1513) | 0.952 (1945) | 0.013 (3) | 0.0487 (109) | 1.99 (11410) | 2.02 (917) | 8.34 (1439) | 2.14 (194) | 0 (0) | 0 (0) |
| + Z window & m_llgg | 0.195 (27194) | 1.07 (9453) | 0.427 (1503) | 0.3 (614) | 0 (0) | 0.0129 (29) | 1.95 (11216) | 0.505 (229) | 5.83 (1005) | 1.91 (173) | 0 (0) | 0 (0) |
| + photon pT, pT/m_gg | 0.169 (23532) | 0.933 (8229) | 0.376 (1324) | 0.249 (509) | 0 (0) | 0.00982 (22) | 1.51 (8675) | 0.328 (149) | 2.6 (449) | 0.928 (84) | 0 (0) | 0 (0) |
| + b-veto | 0.169 (23532) | 0.933 (8229) | 0.376 (1324) | 0.249 (509) | 0 (0) | 0.00982 (22) | 1.51 (8675) | 0.328 (149) | 2.6 (449) | 0.928 (84) | 0 (0) | 0 (0) |
| + mjj, deta_jj | 0.0867 (12062) | 0.0365 (322) | 0.0477 (168) | 0.00343 (7) | 0 (0) | 0 (0) | 0.143 (824) | 0.00661 (3) | 0.342 (59) | 0.442 (40) | 0 (0) | 0 (0) |
| + Zeppenfeld | 0.0867 (12062) | 0.0365 (322) | 0.0477 (168) | 0.00343 (7) | 0 (0) | 0 (0) | 0.143 (824) | 0.00661 (3) | 0.342 (59) | 0.442 (40) | 0 (0) | 0 (0) |
| + m_gg window (120.8-129.1) | 0.0806 (11219) | 0.0341 (301) | 0.0457 (161) | 0.00343 (7) | 0 (0) | 0 (0) | 0.019 (109) | 0.0022 (1) | 0.0174 (3) | 0 (0) | 0 (0) | 0 (0) |

### Table III-like - cutflow at the reference-like baseline, 500 fb^-1: expected events (raw MC events)

| step | S_EW_ZHjj | H_QCD_ZHjj | H_ggZH | H_ttH | H_ZH_tautau | H_tHW | B_QCD_Zaajj_vbs | T_ttaa | F_QCD_Zajj | F_EW_Zajj | T_tta | T_tWa |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| N generated x sigma x BR | 1.44 (200000) | 11.3 (100000) | 5.68 (20000) | 20.6 (42000) | 28.3 (6565) | 0.893 (2000) | 17.4 (100000) | 48.5 (22000) | 3.47e+04 (5989548) | 5.52e+03 (500000) | 4.28e+04 (2000) | 6.52e+03 (2000) |
| OSSF + >=2 photons + >=2 jets | 0.199 (27721) | 1.09 (9644) | 0.429 (1513) | 0.952 (1945) | 0.013 (3) | 0.0487 (109) | 1.99 (11410) | 2.02 (917) | 8.34 (1439) | 2.14 (194) | 0 (0) | 0 (0) |
| + Z window & m_llgg | 0.195 (27125) | 1.07 (9446) | 0.426 (1501) | 0.297 (606) | 0 (0) | 0.0121 (27) | 1.95 (11226) | 0.503 (228) | 5.39 (929) | 1.87 (169) | 0 (0) | 0 (0) |
| + photon pT, pT/m_gg | 0.185 (25738) | 1.02 (8991) | 0.406 (1432) | 0.281 (574) | 0 (0) | 0.0103 (23) | 1.9 (10925) | 0.403 (183) | 3.62 (625) | 1.33 (120) | 0 (0) | 0 (0) |
| + b-veto | 0.185 (25738) | 1.02 (8991) | 0.406 (1432) | 0.281 (574) | 0 (0) | 0.0103 (23) | 1.9 (10925) | 0.403 (183) | 3.62 (625) | 1.33 (120) | 0 (0) | 0 (0) |
| + mjj, deta_jj | 0.0901 (12533) | 0.0449 (396) | 0.0528 (186) | 0.00685 (14) | 0 (0) | 0 (0) | 0.311 (1784) | 0.0176 (8) | 0.574 (99) | 0.751 (68) | 0 (0) | 0 (0) |
| + Zeppenfeld | 0.0901 (12533) | 0.0449 (396) | 0.0528 (186) | 0.00685 (14) | 0 (0) | 0 (0) | 0.311 (1784) | 0.0176 (8) | 0.574 (99) | 0.751 (68) | 0 (0) | 0 (0) |
| + m_gg window (120.8-129.1) | 0.083 (11550) | 0.0416 (367) | 0.0502 (177) | 0.00685 (14) | 0 (0) | 0 (0) | 0.0463 (266) | 0 (0) | 0.029 (5) | 0.0442 (4) | 0 (0) | 0 (0) |

### Table IV-like - per-process expected yields at the optimum (events), MC-stat, raw MC support, method

| process | role | sigma [fb] | x BR | N_MC | w_evt @500 | yield 500 | yield 1000 | yield 3000 | MC-stat @500 | raw in window | raw 105-165 | method |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S_EW_ZHjj | signal | 1.295 | 0.002221 | 200000 | 7.19e-06 | 0.0806 | 0.1613 | 0.4838 | 0.0008 | 11219 | 11916 | L0 direct |
| H_QCD_ZHjj | bkg (a) / signal (b) | 10.21 | 0.002221 | 100000 | 0.000113 | 0.0341 | 0.0683 | 0.2048 | 0.0020 | 301 | 320 | L0 direct |
| H_ggZH | background | 74.33 | 0.0001528 | 20000 | 0.000284 | 0.0457 | 0.0914 | 0.2742 | 0.0036 | 161 | 168 | L0 direct |
| H_ttH | background | 18.11 | 0.00227 | 42000 | 0.000489 | 0.0060 | 0.0120 | 0.0359 | 0.0060 | 7 | 7 | L2 VBS-factorised (100% unc.) |
| H_ZH_tautau | background | 24.97 | 0.00227 | 6565 | 0.00432 | 0.0049 | 0.0098 | 0.0295 | 0.0049 | 0 | 0 | UL (zero support): 1.14 w_evt |
| H_tHW | background | 0.7868 | 0.00227 | 2000 | 0.000447 | 0.0002 | 0.0003 | 0.0010 | 0.0002 | 0 | 0 | L2 VBS-factorised (100% unc.) |
| B_QCD_Zaajj_vbs | background | 0.0356 | 0.9783 | 100000 | 0.000174 | 0.0190 | 0.0380 | 0.1139 | 0.0018 | 109 | 695 | L0 direct |
| T_ttaa | background | 0.097 | 1 | 22000 | 0.0022 | 0.0007 | 0.0013 | 0.0039 | 0.0007 | 1 | 3 | L2 VBS-factorised (100% unc.) |
| F_QCD_Zajj | background | 69.46 | 1 | 5989548 | 0.0058 | 0.0133 | 0.0267 | 0.0801 | 0.0036 | 3 | 14 | L1 m_gg-shape (exp. fit, Delphes) |
| F_EW_Zajj | background | 11.05 | 1 | 500000 | 0.0111 | 0.0165 | 0.0330 | 0.0989 | 0.0165 | 0 | 9 | L2 VBS-factorised (100% unc.) |
| T_tta | background | 85.58 | 1 | 2000 | 21.4 | 0.0000 | 0.0001 | 0.0003 | 0.0000 | 0 | 0 | L3 transfer (Delphes TF, 100% unc.) |
| T_tWa | background | 13.04 | 1 | 2000 | 3.26 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0 | 0 | L3 transfer (Delphes TF, 100% unc.) |

### Robustness at 500 fb^-1, definition (a)

| variation | s | b | Z_Eq1 | Z_syst |
|---|---|---|---|---|
| optimum | 0.081 | 0.140 | 0.198 | 0.198 |
| window +-1.5 sigma | 0.073 | 0.120 | 0.193 | 0.193 |
| reference-like baseline | 0.083 | 0.210 | 0.171 | 0.171 |
| b-veto toggled | 0.078 | 0.125 | 0.202 | 0.201 |
| Zeppenfeld z* < 1.0 | 0.081 | 0.140 | 0.198 | 0.198 |
| mjj > 700, |deta| > 3.0 | 0.076 | 0.139 | 0.189 | 0.188 |
| fake syst 25% | 0.081 | 0.140 | 0.198 | 0.198 |
| fake syst 100% | 0.081 | 0.140 | 0.198 | 0.198 |
| window x0.75 (resolution proxy) | 0.073 | 0.120 | 0.193 | 0.193 |
| window x1.25 (resolution proxy) | 0.084 | 0.154 | 0.197 | 0.197 |

### Reference-like baseline results

| L | def | s | b | Z_Eq1 +- MC | mu95 |
|---|---|---|---|---|---|
| 500 | a | 0.083 | 0.210 | 0.171 +- 0.004 | 36.1 |
| 500 | b | 0.125 | 0.168 | 0.275 +- 0.009 | 24.0 |
| 1000 | a | 0.166 | 0.420 | 0.242 +- 0.006 | 18.0 |
| 1000 | b | 0.249 | 0.337 | 0.388 +- 0.013 | 12.0 |
| 3000 | a | 0.498 | 1.260 | 0.418 +- 0.011 | 8.1 |
| 3000 | b | 0.748 | 1.011 | 0.672 +- 0.022 | 5.5 |

### Fake-factor cross-check on Delphes jets (QCD Zg+jets, 500 fb^-1)

| estimate | final selection | optimum without VBS-jet cuts |
|---|---|---|
| f=0.0005 | 0.0102 | 0.1105 |
| f=0.001 | 0.0205 | 0.2210 |
| f=0.002 | 0.0409 | 0.4420 |
| pT-dependent | 0.0204 | 0.2110 |
| direct Delphes | 0.0133 | 0.1276 |

### Joint mjj x |deta_jj| scan, Z_Eq1 (def. a), 500 fb^-1

| mjj \ deta | >2.0 | >2.5 | >3.0 | >3.5 | >4.0 | >4.5 |
|---|---|---|---|---|---|---|
| >500 | 0.165 | 0.173 | 0.181 | 0.192 | 0.198 | 0.195 |
| >600 | 0.171 | 0.177 | 0.186 | 0.196 | 0.202 | 0.200 |
| >700 | 0.175 | 0.181 | 0.189 | 0.197 | 0.202 | 0.201 |
| >800 | 0.176 | 0.180 | 0.187 | 0.194 | 0.201 | 0.200 |
| >900 | 0.174 | 0.178 | 0.186 | 0.191 | 0.197 | 0.198 |
| >1000 | 0.171 | 0.175 | 0.180 | 0.185 | 0.190 | 0.193 |
| >1200 | 0.164 | 0.167 | 0.170 | 0.174 | 0.178 | 0.183 |

### Joint mjj x |deta_jj| scan, Z_Eq1 (def. a), 3000 fb^-1

| mjj \ deta | >2.0 | >2.5 | >3.0 | >3.5 | >4.0 | >4.5 |
|---|---|---|---|---|---|---|
| >500 | 0.404 | 0.423 | 0.443 | 0.469 | 0.486 | 0.477 |
| >600 | 0.418 | 0.435 | 0.455 | 0.479 | 0.496 | 0.489 |
| >700 | 0.429 | 0.443 | 0.462 | 0.482 | 0.496 | 0.493 |
| >800 | 0.432 | 0.441 | 0.458 | 0.474 | 0.492 | 0.490 |
| >900 | 0.426 | 0.437 | 0.455 | 0.467 | 0.481 | 0.484 |
| >1000 | 0.418 | 0.428 | 0.441 | 0.453 | 0.465 | 0.472 |
| >1200 | 0.403 | 0.409 | 0.417 | 0.426 | 0.437 | 0.449 |


## 7. Systematic uncertainties (supplementary fit and Z_syst)

- **Background normalisation:**
  - 10 % per process for prompt and resonant backgrounds;
  - **50 % for fake-photon processes** (Zγjj, tt̄γ, tWγ). Robustness variants use 25 % and 100 %.
- **Luminosity:** 2.5 % on all MC-normalised processes.
- **MC statistics:** per process, from the raw count of the estimate. L2, L3 and UL estimates carry 100 % uncertainty.
- **Fit:** binned Poisson likelihood in mγγ with 16 bins over 105–165 GeV.
  - Window bins: ±1σ and ±2σ around the Delphes peak. Sidebands: 5 GeV bins.
  - Templates: the Delphes signal shape for resonant processes; exponential fits for the continuum.
  - Nuisances: one log-normal per background process (normalisation ⊕ MC stat) plus luminosity.
  - Asimov data; q₀ for Z; asymptotic CLs (q̃μ) for μ₉₅.
- **Not included:** no theory uncertainty (scale, PDF, LO→NLO) on the signal or on the background shapes.

## 8. Limitations

1. **The statistical regime limits the result, not the background model.** s < 1 even at 3000 fb⁻¹, so the Z values are illustrative.
2. **The Delphes CMS card is not real CMS.**
   - σ_mγγ is about 2.1 GeV, against about 1.5 GeV in data.
   - Electron reconstruction efficiency is low: OSSF acceptance about 36 % for signal (D11: stock card kept for comparability with the reference). A CMS-like lepton efficiency would raise s by up to ×1.7, and the conclusions would not change.
   - The **Delphes jet→photon fake rate is an assumption of the detector card**, not a measurement. The FF band (§4) brackets it within a factor of about 2.
3. **Zγγjj uses an on-shell Z.** Photons radiated in the Z decay are not included (§4).
4. **Generator-level biasing** of Zγ and Zγγ: pT(γ) > 25 GeV and mjj > 400 GeV. The reference-like baseline therefore uses photon pT > 25 GeV.
5. **Factorised and transfer-factor estimates assume cut independence.** These are tt̄γ, tWγ, tt̄γγ and tHW, all ≪ s. Each carries 100 % uncertainty.
6. **Everything is LO, with no k-factors.** QCD ZHjj uses fixed-order ZH+2j; the merged 0–2j cross-check is in report 05.
7. **Double-fake backgrounds** (Z+jets, tt̄) are not in b. They are order-of-magnitude only, as in the reference.
8. **3000 fb⁻¹ is luminosity scaling at 13.6 TeV,** with no pile-up and no HL-LHC detector.
9. **EW–QCD ZHjj interference** is not included; its size is in report 03.
10. **EW Zγγjj (B_EW_zaajj_vbs_is1-3) gridpacks still integrating; EW Zγγjj not yet in b**

## 9. Outlook: VHjj

- **Wider signal definition.** Adding Z→νν, W→ℓν (WHjj) and τ final states raises the produced signal by roughly an order of magnitude. Each brings its own dominant backgrounds: Wγγ, Zγγ with Z→νν, and fakes. This needs a new Phase 01.
- **Other Higgs decays.** H→bb̄ (BR ≈ 58 %) gives about 250× more signal before selection, against tt̄ and Z+bb̄ backgrounds; a boosted H→bb̄ VBS selection is the natural next study. H→WW*/ττ are intermediate options.
- **Within H→γγ, the gains are bounded:**
  - CMS-like resolution and lepton efficiency: up to ×1.7 in s;
  - a multivariate VBS tagger: typically 20–40 % in Z;
  - combining ZHjj with WHjj.
  - Even together, these do not reach s ≫ 1 at 3000 fb⁻¹ in the ZHjj, H→γγ channel alone.

## 10. Figures (`figures/`, PDF + PNG)

All distributions are at 3000 fb⁻¹, Delphes level, after all optimum cuts except the VBS-jet cuts and the mγγ window. The signal is unstacked; the mℓℓ plot uses a relaxed mℓℓ window.
- `m_gg`, `m_ll`, `m_jj`, `deta_jj`, `photon1_pt`, `photon2_pt`, `zeppenfeld`
- `scan_mjj_deta_500`, `scan_mjj_deta_3000`: Eq. 1 significance vs the mjj and |Δηjj| thresholds, other cuts at the optimum (the reference's Fig. 4).

## 11. Checks

- **σ closure:** below 1 % for every final sample (see the table in §2).
- **Ntuples:** event counts equal the verified job totals.
- **ggZH decay closure** (GenTruth, first job, 2000 events):
  - 98.4 % of events have a prompt ee or μμ pair (49.2 % ee, 50.6 % μμ, no ττ), confirming that the forced Z→ee/μμ was applied once;
  - 86.8 % have two prompt photons with pT > 10 GeV (forced H→γγ; the rest is acceptance).
  - Signal/QCD ZHjj BR closure: report 05 §1.
- **Fake rate:** the FF and direct Delphes fake estimates agree within the FF band.
- **Re-optimisation:** the optimum Z_syst differs from the reference-like baseline by +0.027 at 500 fb⁻¹.
- **Robustness:** see the table above.
