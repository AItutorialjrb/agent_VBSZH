# FINAL report — EW ZHjj (Z→ee/μμ, H→γγ) at √s = 13.6 TeV: Delphes-level feasibility study

- **Date:** 2026-11-03 02:20 UTC
- **Status:** **PASS with limitations**. Expected-limit/significance study for the current signal definition (D12 closed).
- **Git commit:** `55d4b11`. Reproduction: [08_reproducibility.md](08_reproducibility.md).
- **Inputs:** `work/final_ntuples/final.json` (written by `scripts/analysis/final_analysis.py`), `work/final_ntuples/verify.json`.
- **Comparison:** the reference ZγγJJ study, arXiv:2512.07689, is the methodological reference: same Delphes CMS card, Eq. 1 counting significance and the Fig. 4-style mjj–|Δηjj| scan.
- **Luminosity:** 3000 fb⁻¹ is a pure luminosity scaling at 13.6 TeV, not an HL-LHC detector projection.

## Summary

At the optimised Delphes-level selection, the EW ZHjj signal is **s = 0.088 events at 500 fb⁻¹** and 0.53 at 3000 fb⁻¹. The total background is b = 0.420 (2.52) events.
- **Significance:** Eq. 1 gives Z = 0.131 ± 0.002 (MC) at 500 fb⁻¹ and 0.321 ± 0.006 at 3000 fb⁻¹, for definition (a).
- **s < 1 at every luminosity and for both signal definitions, so Z alone is not a meaningful measure of sensitivity.** The physically meaningful quantity is the expected 95 % CL upper limit on the signal strength.
  - μ₉₅ = 34 at 500 fb⁻¹ and 8.7 at 3000 fb⁻¹ (exact-Poisson CLs, definition a).
  - The median background-only count is 0 at 500 fb⁻¹, so the limit is close to the zero-background value 3/s.
- **The process is not observable at the LHC Run 3 or with 3000 fb⁻¹ in this channel.** The tiny signal rate is the limiting factor: σ×BR×L = 1.44 events produced at 500 fb⁻¹ before any selection.
- **Dominant background:** the irreducible EW Zγγjj continuum under the mγγ peak. It cannot be suppressed by the VBS-jet cuts, because it shares the signal's VBS topology.

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
| B_QCD_Zaajj_vbs | final, fixed order, on-shell Z->ll, VBS-biased generation | 0.0356 | 0.9783 | 100000 | 2.87e+06 | 50/50 jobs OK; σ closure -0.10 % |
| B_EW_Zaajj_vbs_is1 | final, fixed order 4F, on-shell Z->ll, VBS-biased, beam-1 split | 0.01666 | 0.9783 | 20000 | 1.23e+06 | 10/10 jobs OK; σ closure -0.19 % |
| B_EW_Zaajj_vbs_is2 | final, fixed order 4F, on-shell Z->ll, VBS-biased, beam-1 split | 0.01575 | 0.9783 | 20000 | 1.3e+06 | 10/10 jobs OK; σ closure +0.04 % |
| B_EW_Zaajj_vbs_is3 | final, fixed order 4F, on-shell Z->ll, VBS-biased, beam-1 split | 0.0068 | 0.9783 | 20000 | 3.01e+06 | 10/10 jobs OK; σ closure -0.36 % |
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
- **EW Zγγjj** is 4-flavour with a 3-way split in the beam-1 parton class: u c / d s / ū c̄ d̄ s̄. Gluon-initiated processes do not exist at QCD⁰.
  - Split 1 was integrated with Monte-Carlo helicity sampling (`nhel 1`, same process) because helicity summation projected to 13 h.
  - σ closure per split is below 0.4 %.
- **EW Zγγjj is the dominant background** at the final selection. This was cross-checked against the reference, where EW Zγγjj is the *signal*: 0.263 fb inclusive and 0.057 fb after their initial selection. Our window-and-VBS yield corresponds to a few percent of that, as expected from the falling mγγ spectrum.
  - The sample contains no H→γγ peak, and the `sm` model has no hγγ vertex, so there is no double counting with the signal.
  - The Phase-05 pilot proxy (0.029 events at 500 fb⁻¹) underestimated this background by about an order of magnitude; the pilot results in report 05 are superseded.
- **Fake-factor cross-check (Delphes jets):** in the QCD Zγjj sample with the ff1 mode of `ntuple.py`, f = 5×10⁻⁴, 10⁻³ and 2×10⁻³ plus a pT-dependent variant give 0.0284 events (f = 10⁻³; band 0.0142–0.0568) at the final selection, 500 fb⁻¹. The direct Delphes result is 0.0181. Without the VBS cuts it is 0.128 (direct, 22 raw) vs 0.221 (FF). The Delphes fake rate therefore corresponds to f ≈ 5.8e-04 per jet.

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
- **Optimum:** 2 photons with pT > 25 GeV, pT(γ1)/mγγ > 0.33, pT(γ2)/mγγ > 0.25; |mℓℓ − mZ| < 25 GeV; mℓℓγγ > 100 GeV; no b-veto; no Zeppenfeld cut; mjj > 500 GeV, |Δηjj| > 3.5; 120.8 < mγγ < 129.1 GeV (±2.0σ, σ = 2.07 GeV).
- The mjj × |Δηjj| landscape (Fig. 4-style: `figures/scan_mjj_deta_*.png`, tables below) is smooth: at 500 fb⁻¹, Z_Eq1 ranges from 0.092 to 0.133.
  - Z rises slowly towards looser mjj and tighter |Δηjj|.
  - **The optimum lies on the mjj = 500 GeV scan boundary.** This is the loosest threshold allowed by the generator-level mjj > 400 GeV bias of the Zγ and Zγγ samples. The trend suggests only a few-percent gain below it.
  - Moving to mjj > 700 GeV, |Δηjj| > 3.0 changes Z by -0.010 (robustness table). This does not affect the conclusions.

## 6. Results

### PRIMARY: Eq. 1 counting significance (stat. only, ± MC stat) and limits

| L [fb⁻¹] | signal definition | s | b | Z_Eq1 ± MC | Z_syst (binned PL fit) | μ₉₅ CLs (exact Poisson, syst) | μ₉₅ (binned PL fit, asymptotic) |
|---|---|---|---|---|---|---|---|
| 500 | (a) EW ZHjj; QCD ZHjj in b | 0.088 | 0.420 | 0.131 ± 0.002 | 0.138 | 34.1 | 30.8 |
| 500 | (b) EW + QCD ZHjj | 0.135 | 0.373 | 0.210 ± 0.005 | 0.222 | 22.1 | 19.5 |
| 1000 | (a) EW ZHjj; QCD ZHjj in b | 0.176 | 0.841 | 0.185 ± 0.003 | 0.195 | 23.8 | 18.1 |
| 1000 | (b) EW + QCD ZHjj | 0.271 | 0.746 | 0.297 ± 0.007 | 0.313 | 15.6 | 11.4 |
| 3000 | (a) EW ZHjj; QCD ZHjj in b | 0.527 | 2.523 | 0.321 ± 0.006 | 0.336 | 8.7 | 8.3 |
| 3000 | (b) EW + QCD ZHjj | 0.812 | 2.238 | 0.514 ± 0.012 | 0.541 | 5.8 | 5.2 |

- **s < 1 in every row:** Z alone is not meaningful.
- **μ₉₅ from exact-Poisson CLs:** counting in the window, with b marginalised over a log-normal(σ_b/b). This is the robust number.
- **Asymptotic fit limit:** uses Asimov asymptotics, which are not valid at these counts. It is shown only because it was requested, and it underestimates the limit.
- **Largest background components** at 500 fb⁻¹, definition (a): B_EW_Zaajj_vbs_is2 0.0994; B_EW_Zaajj_vbs_is1 0.0966; H_ggZH 0.0539; H_QCD_ZHjj 0.0474; B_EW_Zaajj_vbs_is3 0.0414.

### Table R1 - PRIMARY: Eq. 1 counting significance (stat. only, +- MC stat), 13.6 TeV

| L [fb^-1] | signal def. | s +- MC | b +- MC | Z_Eq1 +- MC | Z_syst (counting, sigma_b) | mu95 CLs (exact Poisson, syst) | median n_obs (b-only) |
|---|---|---|---|---|---|---|---|
| 500 | (a) EW ZHjj; QCD ZHjj in b | 0.088 +- 0.001 | 0.420 +- 0.014 | 0.131 +- 0.002 | 0.131 | 34.1 | 0 |
| 500 | (b) EW+QCD ZHjj | 0.135 +- 0.002 | 0.373 +- 0.014 | 0.210 +- 0.005 | 0.210 | 22.1 | 0 |
| 1000 | (a) EW ZHjj; QCD ZHjj in b | 0.176 +- 0.002 | 0.841 +- 0.028 | 0.185 +- 0.003 | 0.185 | 23.8 | 1 |
| 1000 | (b) EW+QCD ZHjj | 0.271 +- 0.005 | 0.746 +- 0.028 | 0.297 +- 0.007 | 0.296 | 15.6 | 1 |
| 3000 | (a) EW ZHjj; QCD ZHjj in b | 0.527 +- 0.005 | 2.523 +- 0.084 | 0.321 +- 0.006 | 0.320 | 8.7 | 2 |
| 3000 | (b) EW+QCD ZHjj | 0.812 +- 0.015 | 2.238 +- 0.083 | 0.514 +- 0.012 | 0.511 | 5.8 | 2 |

### Table R2 - SUPPLEMENTARY: binned profile-likelihood fit in m_gg (window + sidebands, Asimov, asymptotic)

| L [fb^-1] | signal def. | Z (fit, stat only) | Z_syst (fit) | mu95 (fit, stat only) | mu95 (fit, syst) |
|---|---|---|---|---|---|
| 500 | (a) EW ZHjj; QCD ZHjj in b | 0.138 | 0.138 | 30.8 | 30.8 |
| 500 | (b) EW+QCD ZHjj | 0.222 | 0.222 | 19.5 | 19.5 |
| 1000 | (a) EW ZHjj; QCD ZHjj in b | 0.195 | 0.195 | 18.0 | 18.1 |
| 1000 | (b) EW+QCD ZHjj | 0.314 | 0.313 | 11.3 | 11.4 |
| 3000 | (a) EW ZHjj; QCD ZHjj in b | 0.338 | 0.336 | 8.3 | 8.3 |
| 3000 | (b) EW+QCD ZHjj | 0.544 | 0.541 | 5.2 | 5.2 |

### Table III-like - cutflow at the optimum, 500 fb^-1: expected events (raw MC events)

| step | S_EW_ZHjj | H_QCD_ZHjj | H_ggZH | H_ttH | H_ZH_tautau | H_tHW | B_QCD_Zaajj_vbs | B_EW_Zaajj_vbs_is1 | B_EW_Zaajj_vbs_is2 | B_EW_Zaajj_vbs_is3 | T_ttaa | F_QCD_Zajj | F_EW_Zajj | T_tta | T_tWa |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| N generated x sigma x BR | 1.44 (200000) | 11.3 (100000) | 5.68 (20000) | 20.6 (42000) | 28.3 (6565) | 0.893 (2000) | 17.4 (100000) | 8.15 (20000) | 7.7 (20000) | 3.33 (20000) | 48.5 (22000) | 3.47e+04 (5989548) | 5.52e+03 (500000) | 4.28e+04 (2000) | 6.52e+03 (2000) |
| OSSF + >=2 photons + >=2 jets | 0.199 (27721) | 1.09 (9644) | 0.429 (1513) | 0.952 (1945) | 0.013 (3) | 0.0487 (109) | 1.99 (11410) | 1.65 (4052) | 1.51 (3909) | 0.688 (4135) | 2.02 (917) | 8.34 (1439) | 2.14 (194) | 0 (0) | 0 (0) |
| + Z window & m_llgg | 0.195 (27194) | 1.07 (9453) | 0.427 (1503) | 0.3 (614) | 0 (0) | 0.0129 (29) | 1.95 (11216) | 1.62 (3987) | 1.47 (3829) | 0.677 (4068) | 0.505 (229) | 5.83 (1005) | 1.91 (173) | 0 (0) | 0 (0) |
| + photon pT, pT/m_gg | 0.169 (23532) | 0.933 (8229) | 0.376 (1324) | 0.249 (509) | 0 (0) | 0.00982 (22) | 1.51 (8675) | 1.21 (2961) | 1.1 (2850) | 0.499 (2998) | 0.328 (149) | 2.6 (449) | 0.928 (84) | 0 (0) | 0 (0) |
| + b-veto | 0.169 (23532) | 0.933 (8229) | 0.376 (1324) | 0.249 (509) | 0 (0) | 0.00982 (22) | 1.51 (8675) | 1.21 (2961) | 1.1 (2850) | 0.499 (2998) | 0.328 (149) | 2.6 (449) | 0.928 (84) | 0 (0) | 0 (0) |
| + mjj, deta_jj | 0.0945 (13152) | 0.05 (441) | 0.0559 (197) | 0.00783 (16) | 0 (0) | 0 (0) | 0.211 (1213) | 0.84 (2062) | 0.768 (1994) | 0.31 (1863) | 0.00882 (4) | 0.475 (82) | 0.564 (51) | 0 (0) | 0 (0) |
| + Zeppenfeld | 0.0945 (13152) | 0.05 (441) | 0.0559 (197) | 0.00783 (16) | 0 (0) | 0 (0) | 0.211 (1213) | 0.84 (2062) | 0.768 (1994) | 0.31 (1863) | 0.00882 (4) | 0.475 (82) | 0.564 (51) | 0 (0) | 0 (0) |
| + m_gg window (120.8-129.1) | 0.0879 (12226) | 0.0474 (418) | 0.0539 (190) | 0.00783 (16) | 0 (0) | 0 (0) | 0.0277 (159) | 0.0966 (237) | 0.0994 (258) | 0.0414 (249) | 0.0022 (1) | 0.029 (5) | 0.0111 (1) | 0 (0) | 0 (0) |

### Table III-like - cutflow at the reference-like baseline, 500 fb^-1: expected events (raw MC events)

| step | S_EW_ZHjj | H_QCD_ZHjj | H_ggZH | H_ttH | H_ZH_tautau | H_tHW | B_QCD_Zaajj_vbs | B_EW_Zaajj_vbs_is1 | B_EW_Zaajj_vbs_is2 | B_EW_Zaajj_vbs_is3 | T_ttaa | F_QCD_Zajj | F_EW_Zajj | T_tta | T_tWa |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| N generated x sigma x BR | 1.44 (200000) | 11.3 (100000) | 5.68 (20000) | 20.6 (42000) | 28.3 (6565) | 0.893 (2000) | 17.4 (100000) | 8.15 (20000) | 7.7 (20000) | 3.33 (20000) | 48.5 (22000) | 3.47e+04 (5989548) | 5.52e+03 (500000) | 4.28e+04 (2000) | 6.52e+03 (2000) |
| OSSF + >=2 photons + >=2 jets | 0.199 (27721) | 1.09 (9644) | 0.429 (1513) | 0.952 (1945) | 0.013 (3) | 0.0487 (109) | 1.99 (11410) | 1.65 (4052) | 1.51 (3909) | 0.688 (4135) | 2.02 (917) | 8.34 (1439) | 2.14 (194) | 0 (0) | 0 (0) |
| + Z window & m_llgg | 0.195 (27125) | 1.07 (9446) | 0.426 (1501) | 0.297 (606) | 0 (0) | 0.0121 (27) | 1.95 (11226) | 1.63 (3994) | 1.47 (3825) | 0.678 (4076) | 0.503 (228) | 5.39 (929) | 1.87 (169) | 0 (0) | 0 (0) |
| + photon pT, pT/m_gg | 0.185 (25738) | 1.02 (8991) | 0.406 (1432) | 0.281 (574) | 0 (0) | 0.0103 (23) | 1.9 (10925) | 1.6 (3932) | 1.45 (3768) | 0.666 (4003) | 0.403 (183) | 3.62 (625) | 1.33 (120) | 0 (0) | 0 (0) |
| + b-veto | 0.185 (25738) | 1.02 (8991) | 0.406 (1432) | 0.281 (574) | 0 (0) | 0.0103 (23) | 1.9 (10925) | 1.6 (3932) | 1.45 (3768) | 0.666 (4003) | 0.403 (183) | 3.62 (625) | 1.33 (120) | 0 (0) | 0 (0) |
| + mjj, deta_jj | 0.0901 (12533) | 0.0449 (396) | 0.0528 (186) | 0.00685 (14) | 0 (0) | 0 (0) | 0.311 (1784) | 1.19 (2916) | 1.07 (2787) | 0.423 (2543) | 0.0176 (8) | 0.574 (99) | 0.751 (68) | 0 (0) | 0 (0) |
| + Zeppenfeld | 0.0901 (12533) | 0.0449 (396) | 0.0528 (186) | 0.00685 (14) | 0 (0) | 0 (0) | 0.311 (1784) | 1.19 (2916) | 1.07 (2787) | 0.423 (2543) | 0.0176 (8) | 0.574 (99) | 0.751 (68) | 0 (0) | 0 (0) |
| + m_gg window (120.8-129.1) | 0.083 (11550) | 0.0416 (367) | 0.0502 (177) | 0.00685 (14) | 0 (0) | 0 (0) | 0.0463 (266) | 0.139 (340) | 0.133 (345) | 0.0554 (333) | 0 (0) | 0.029 (5) | 0.0442 (4) | 0 (0) | 0 (0) |

### Table IV-like - per-process expected yields at the optimum (events), MC-stat, raw MC support, method

| process | role | sigma [fb] | x BR | N_MC | w_evt @500 | yield 500 | yield 1000 | yield 3000 | MC-stat @500 | raw in window | raw 105-165 | method |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S_EW_ZHjj | signal | 1.295 | 0.002221 | 200000 | 7.19e-06 | 0.0879 | 0.1758 | 0.5273 | 0.0008 | 12226 | 12985 | L0 direct |
| H_QCD_ZHjj | bkg (a) / signal (b) | 10.21 | 0.002221 | 100000 | 0.000113 | 0.0474 | 0.0948 | 0.2844 | 0.0023 | 418 | 439 | L0 direct |
| H_ggZH | background | 74.33 | 0.0001528 | 20000 | 0.000284 | 0.0539 | 0.1079 | 0.3236 | 0.0039 | 190 | 197 | L0 direct |
| H_ttH | background | 18.11 | 0.00227 | 42000 | 0.000489 | 0.0078 | 0.0157 | 0.0470 | 0.0020 | 16 | 16 | L0 direct |
| H_ZH_tautau | background | 24.97 | 0.00227 | 6565 | 0.00432 | 0.0049 | 0.0098 | 0.0295 | 0.0049 | 0 | 0 | UL (zero support): 1.14 w_evt |
| H_tHW | background | 0.7868 | 0.00227 | 2000 | 0.000447 | 0.0003 | 0.0007 | 0.0020 | 0.0003 | 0 | 0 | L2 VBS-factorised (100% unc.) |
| B_QCD_Zaajj_vbs | background | 0.0356 | 0.9783 | 100000 | 0.000174 | 0.0277 | 0.0554 | 0.1661 | 0.0022 | 159 | 1025 | L0 direct |
| B_EW_Zaajj_vbs_is1 | background | 0.01666 | 0.9783 | 20000 | 0.000407 | 0.0966 | 0.1931 | 0.5794 | 0.0063 | 237 | 1721 | L0 direct |
| B_EW_Zaajj_vbs_is2 | background | 0.01575 | 0.9783 | 20000 | 0.000385 | 0.0994 | 0.1988 | 0.5963 | 0.0062 | 258 | 1668 | L0 direct |
| B_EW_Zaajj_vbs_is3 | background | 0.0068 | 0.9783 | 20000 | 0.000166 | 0.0414 | 0.0828 | 0.2485 | 0.0026 | 249 | 1556 | L0 direct |
| T_ttaa | background | 0.097 | 1 | 22000 | 0.0022 | 0.0011 | 0.0021 | 0.0063 | 0.0011 | 1 | 3 | L2 VBS-factorised (100% unc.) |
| F_QCD_Zajj | background | 69.46 | 1 | 5989548 | 0.0058 | 0.0181 | 0.0362 | 0.1087 | 0.0042 | 5 | 19 | L1 m_gg-shape (exp. fit, Delphes) |
| F_EW_Zajj | background | 11.05 | 1 | 500000 | 0.0111 | 0.0218 | 0.0436 | 0.1308 | 0.0063 | 1 | 12 | L1 m_gg-shape (exp. fit, Delphes) |
| T_tta | background | 85.58 | 1 | 2000 | 21.4 | 0.0000 | 0.0001 | 0.0003 | 0.0000 | 0 | 0 | L3 transfer (Delphes TF, 100% unc.) |
| T_tWa | background | 13.04 | 1 | 2000 | 3.26 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0 | 0 | L3 transfer (Delphes TF, 100% unc.) |

### Robustness at 500 fb^-1, definition (a)

| variation | s | b | Z_Eq1 | Z_syst |
|---|---|---|---|---|
| optimum | 0.088 | 0.420 | 0.131 | 0.131 |
| window +-1.5 sigma | 0.080 | 0.329 | 0.134 | 0.134 |
| reference-like baseline | 0.083 | 0.537 | 0.111 | 0.110 |
| b-veto toggled | 0.084 | 0.385 | 0.131 | 0.131 |
| Zeppenfeld z* < 1.0 | 0.088 | 0.420 | 0.131 | 0.131 |
| mjj > 700, |deta| > 3.0 | 0.076 | 0.373 | 0.121 | 0.121 |
| fake syst 25% | 0.088 | 0.420 | 0.131 | 0.131 |
| fake syst 100% | 0.088 | 0.420 | 0.131 | 0.131 |
| window x0.75 (resolution proxy) | 0.080 | 0.329 | 0.134 | 0.134 |
| window x1.25 (resolution proxy) | 0.091 | 0.506 | 0.125 | 0.125 |

### Reference-like baseline results

| L | def | s | b | Z_Eq1 +- MC | mu95 |
|---|---|---|---|---|---|
| 500 | a | 0.083 | 0.537 | 0.111 +- 0.002 | 36.1 |
| 500 | b | 0.125 | 0.495 | 0.170 +- 0.004 | 24.0 |
| 1000 | a | 0.166 | 1.074 | 0.156 +- 0.003 | 24.6 |
| 1000 | b | 0.249 | 0.991 | 0.241 +- 0.006 | 16.5 |
| 3000 | a | 0.498 | 3.221 | 0.271 +- 0.005 | 10.6 |
| 3000 | b | 0.748 | 2.972 | 0.417 +- 0.010 | 7.3 |

### Fake-factor cross-check on Delphes jets (QCD Zg+jets, 500 fb^-1)

| estimate | final selection | optimum without VBS-jet cuts |
|---|---|---|
| f=0.0005 | 0.0142 | 0.1105 |
| f=0.001 | 0.0284 | 0.2210 |
| f=0.002 | 0.0568 | 0.4420 |
| pT-dependent | 0.0281 | 0.2110 |
| direct Delphes | 0.0181 | 0.1276 |

### Joint mjj x |deta_jj| scan, Z_Eq1 (def. a), 500 fb^-1

| mjj \ deta | >2.0 | >2.5 | >3.0 | >3.5 | >4.0 | >4.5 |
|---|---|---|---|---|---|---|
| >500 | 0.119 | 0.122 | 0.126 | 0.131 | 0.133 | 0.128 |
| >600 | 0.117 | 0.120 | 0.124 | 0.129 | 0.131 | 0.128 |
| >700 | 0.115 | 0.118 | 0.121 | 0.124 | 0.128 | 0.125 |
| >800 | 0.111 | 0.113 | 0.116 | 0.119 | 0.123 | 0.121 |
| >900 | 0.106 | 0.108 | 0.110 | 0.113 | 0.117 | 0.116 |
| >1000 | 0.102 | 0.103 | 0.105 | 0.108 | 0.111 | 0.111 |
| >1200 | 0.092 | 0.093 | 0.094 | 0.096 | 0.099 | 0.101 |

### Joint mjj x |deta_jj| scan, Z_Eq1 (def. a), 3000 fb^-1

| mjj \ deta | >2.0 | >2.5 | >3.0 | >3.5 | >4.0 | >4.5 |
|---|---|---|---|---|---|---|
| >500 | 0.291 | 0.299 | 0.309 | 0.321 | 0.326 | 0.315 |
| >600 | 0.287 | 0.295 | 0.303 | 0.315 | 0.321 | 0.313 |
| >700 | 0.282 | 0.288 | 0.296 | 0.305 | 0.312 | 0.307 |
| >800 | 0.273 | 0.277 | 0.283 | 0.292 | 0.301 | 0.296 |
| >900 | 0.260 | 0.264 | 0.270 | 0.278 | 0.286 | 0.284 |
| >1000 | 0.250 | 0.252 | 0.257 | 0.265 | 0.273 | 0.273 |
| >1200 | 0.226 | 0.228 | 0.231 | 0.236 | 0.243 | 0.246 |


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
5. **ggZH jets come only from the parton shower.** ggZH is LO loop-induced with no ME jets, so its VBS-region jets come from the Pythia8 power shower. Its selection efficiency is therefore about 2× that of fixed-order QCD ZHjj, and the yield is uncertain by about a factor of 2. A merged gg→ZH+jets sample is beyond LO MG5 in this setup.
6. **Factorised and transfer-factor estimates assume cut independence.** These are tt̄γ, tWγ, tt̄γγ and tHW, all ≪ s. Each carries 100 % uncertainty.
7. **Everything is LO, with no k-factors.** QCD ZHjj uses fixed-order ZH+2j; the merged 0–2j cross-check is in report 05.
8. **Double-fake backgrounds** (Z+jets, tt̄) are not in b. They are order-of-magnitude only, as in the reference.
9. **3000 fb⁻¹ is luminosity scaling at 13.6 TeV,** with no pile-up and no HL-LHC detector.
10. **EW–QCD ZHjj interference** is not included; its size is in report 03.


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
- **Re-optimisation:** the optimum Z_syst differs from the reference-like baseline by +0.021 at 500 fb⁻¹.
- **Robustness:** see the table above.
