# FINAL report — EW ZHjj (Z→ee/μμ, H→γγ) at √s = 13.6 TeV: Delphes-level feasibility study and VH coupling interpretation

- **Date:** 2026-11-03 14:25 UTC
- **Status:** **PASS with limitations**. Expected-limit/significance study for the current signal definition, plus the λWZ / κZ / CP-odd coupling interpretation (§9).
- **Git commit:** `b8f2a7d`. Reproduction: [08_reproducibility.md](08_reproducibility.md). Self-review: [ZH_self_review.md](ZH_self_review.md).
- **Inputs:** `work/final_ntuples/final.json` (written by `scripts/analysis/final_analysis.py`, which also executes `scripts/analysis/coupling_section.py`), `work/final_ntuples/verify.json`, `work/theory/theory_summary.json`.
- **Comparison with the reference** (arXiv:2512.07689: same Delphes CMS card, Eq. 1, Fig. 4-style scan). **Deviation marked everywhere it matters: our photon pT threshold is 25 GeV, the reference's is 20 GeV.** The reason is that the VBS-biased Zγ/Zγγ samples are generated with pT(γ) > 25 GeV. Every comparison to reference numbers below carries the tag **[γ pT 25 vs 20 GeV]**.
- **Luminosity:** 3000 fb⁻¹ is a pure luminosity scaling at 13.6 TeV, not an HL-LHC detector projection.

## Summary

At the optimised Delphes-level selection, the EW ZHjj signal is **s = 0.088 events at 500 fb⁻¹** and 0.53 at 3000 fb⁻¹. The background is b = 0.520 (3.12).
- **Significance:** Z_Eq1 = 0.119 ± 0.002 (MC) at 500 fb⁻¹ and 0.291 ± 0.005 at 3000 fb⁻¹, definition (a).
- **Systematics:** they now include theory (scale ⊕ PDF per process, correlated within groups), the off-shell/FSR correction of Zγγ, the Zγγjj interference, the ggZH ×2 normalisation and the generator-mjj correction of the QCD-type samples. With these, Z_syst = 0.118 and μ₉₅ = 35 at 500 fb⁻¹; Z_syst = 0.282 and μ₉₅ = 10.4 at 3000 fb⁻¹.
- **s < 1 at every luminosity, so Z alone is not a meaningful measure of sensitivity.** The process is not observable in this channel at Run 3 or with 3000 fb⁻¹.
- **Dominant background:** the irreducible EW Zγγjj continuum under the mγγ peak.
- **Coupling interpretation (§9):** the measured observable is the yield and the mllgg shape of EW ZHjj in the signal region.
  - **λWZ = −1** gives a signal-region yield 3.8× the SM. Excluding it alone (κZ = 1, BR(H→γγ) fixed to SM) has an expected significance of **Z = 0.43 at 500 fb⁻¹ and 1.05 at 3000 fb⁻¹**.
  - The **whole region λWZ < 0** cannot be excluded: Z = 0.14 at 500 fb⁻¹ and 0.33 at 3000 fb⁻¹. The reason is that λWZ → 0⁻ (minimum at λWZ = -0.05) gives a yield and mℓℓγγ shape close to the SM's: 0.89× the SM yield at λWZ = 0.
  - Resolving the H→γγ rate in κW (W loop) gives Z(λWZ = −1) = 1.98 at 3000 fb⁻¹. That gain comes from inclusive-H→γγ rate information that other measurements already constrain.
  - **This channel cannot test the sign of λWZ at the level of the CMS/ATLAS WH(bb̄) results.**

## 1. Setup

| item | value |
|---|---|
| Stack | LCG_110 x86_64-el9-gcc13-opt; MG5_aMC 3.6.3 (upstream); Pythia 8.317 (CP5); Delphes 3.5.1 with the stock CMS card (slimmed output, physics unchanged); NNPDF3.1 NNLO (LHAID 303600) via LHAPDF 6.5.5. Details: [03_stack.md](03_stack.md). |
| Order | LO for all samples; no k-factors. Theory uncertainties are scale ⊕ PDF from MG5 weights (§7) |
| Generation | MG5 gridpacks on HTCondor (EosSubmit); per job: gridpack → Pythia8 → Delphes → slim/GenTruth friend (`scripts/condor/run_job.sh`) |
| Analysis objects | `scripts/analysis/ntuple.py` (reference Sec. III object definitions): e/μ pT > 15 GeV; isolated Delphes photons pT > 20 GeV, \|η\| < 2.5 outside 1.4442–1.566, ΔR(γ,ℓ) > 0.4; anti-kT jets pT > 25 GeV, \|η\| < 4.7, ΔR > 0.4 to the leptons and photons |
| mγγ peak | Gaussian core fit of the Delphes EW signal: μ = 124.98 GeV, σ = 2.067 ± 0.017 GeV (σ_eff = 2.15 GeV) |
| mjj resolution (A1) | Delphes reco vs matched GenJets, same jet cleaning as the analysis: σ68/mjj = 8.8 % (EW ZHjj), 8.0 % (QCD ZHjj); median bias -1.7 % (`work/theory/mjj_resolution.json`) |

## 2. Samples, verification and the N_MC ≥ σ×BR×3000 fb⁻¹ requirement

All final yields are Delphes-level.
- **Verification** (`scripts/analysis/verify_final.py`): job exit, outputs, event counts and σ closure.
- **Ntuple check:** the event counts in the ntuples equal the verified totals.

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
| T_ttaa | final + test_v2 | 0.097 | 1 | 22000 | 2.27e+05 | 10/10 jobs OK; σ closure -0.12 % |
| F_QCD_Zajj | final, direct Delphes fakes (VBS-biased generation) | 69.46 | 1 | 5989548 | 8.62e+04 | 2995/3000 jobs OK; σ closure -0.15 % |
| F_EW_Zajj | final, direct Delphes fakes (VBS-biased generation) | 11.05 | 1 | 500000 | 4.52e+04 | 250/250 jobs OK; σ closure -0.12 % |
| T_tta | final, direct Delphes (ref. Table I: both t -> b l nu), N = 4.05 x sigma x 3000 fb^-1 | 85.58 | 1 | 1040000 | 1.22e+04 | 520/520 jobs OK; σ closure +0.06 % |
| T_tWa | final, direct Delphes (ref. Table I: tW-a + t~W+a, both W -> l nu), N = 4.1 x sigma x 3000 fb^-1 | 13.04 | 1 | 160000 | 1.23e+04 | 80/80 jobs OK; σ closure +0.21 % |

**Per-sample N_MC vs σ×BR×3000 fb⁻¹ (A10).**
- The table is produced by `nmc_check()` in `final_analysis.py`, which **raises SystemExit if any sample entering s or b (including the BSM coupling samples) has N_MC < σ×BR×L**. This run passed.
- w_evt is the event weight at 3000 fb⁻¹, i.e. the events per MC event.

| sample | σ×BR [fb] | σ×BR×3000 fb⁻¹ | N_MC | N_MC/(σ×BR×L) | w_evt at 3000 fb⁻¹ |
|---|---|---|---|---|---|
| S_EW_ZHjj | 0.002875 | 8.625 | 200000 | 23188.12 | 4.31e-05 |
| H_QCD_ZHjj | 0.02268 | 68.03 | 100000 | 1469.89 | 0.00068 |
| H_ggZH | 0.01135 | 34.06 | 20000 | 587.14 | 0.0017 |
| H_ttH | 0.04111 | 123.3 | 42000 | 340.55 | 0.00294 |
| H_ZH_tautau | 0.05669 | 170.1 | 6565 | 38.60 | 0.0259 |
| H_tHW | 0.001786 | 5.358 | 2000 | 373.27 | 0.00268 |
| B_QCD_Zaajj_vbs | 0.03483 | 104.5 | 100000 | 957.10 | 0.00104 |
| B_EW_Zaajj_vbs_is1 | 0.0163 | 48.9 | 20000 | 409.04 | 0.00244 |
| B_EW_Zaajj_vbs_is2 | 0.01541 | 46.22 | 20000 | 432.67 | 0.00231 |
| B_EW_Zaajj_vbs_is3 | 0.006652 | 19.96 | 20000 | 1002.14 | 0.000998 |
| T_ttaa | 0.097 | 291 | 22000 | 75.60 | 0.0132 |
| F_QCD_Zajj | 69.46 | 2.084e+05 | 5989548 | 28.74 | 0.0348 |
| F_EW_Zajj | 11.05 | 3.315e+04 | 500000 | 15.08 | 0.0663 |
| T_tta | 85.58 | 2.567e+05 | 1040000 | 4.05 | 0.247 |
| T_tWa | 13.04 | 3.912e+04 | 160000 | 4.09 | 0.244 |
| F_QCD_llajj_nomjj (aux, ratio only) | 817.8 | 2.453e+06 | 200000 | 0.08 **(flagged: auxiliary, ratio only)** | 12.3 |
| B_QCD_zaajj_nomjj (aux, ratio only) | 0.268 | 803.9 | 100000 | 124.40 **(flagged: auxiliary, ratio only)** | 0.00804 |
| K_EW_ZHjj_lam_m100 | 0.00529 | 15.87 | 50000 | 3150.71 | 0.000317 |
| K_EW_ZHjj_lam_m050 | 0.002667 | 8.001 | 50000 | 6248.96 | 0.00016 |
| K_EW_ZHjj_lam_p000 | 0.001256 | 3.767 | 50000 | 13271.45 | 7.53e-05 |
| K_EW_ZHjj_lam_p050 | 0.0009525 | 2.857 | 50000 | 17498.26 | 5.71e-05 |
| K_EW_ZHjj_lam_p100 | 0.001791 | 5.374 | 50000 | 9303.34 | 0.000107 |
| K_EW_ZHjj_lam_p150 | 0.00376 | 11.28 | 50000 | 4432.96 | 0.000226 |
| K_EW_ZHjj_cpo_m2 | 0.06616 | 198.5 | 48000 | 241.85 | 0.00413 |
| K_EW_ZHjj_cpo_p2 | 0.06591 | 197.7 | 50000 | 252.86 | 0.00395 |

- **tt̄γ and tWγ (A9)** were regenerated with the reference Table I process definitions:
  - tt̄γ: `p p > t t~ a`, both t → b W, W → ℓν;
  - tWγ: `p p > t w- a` and `p p > t~ w+ a`, both W → ℓν, with `$$` removing the tt̄ overlap.
  - Statistics: 1.04 M and 160 k events, i.e. ≥ 4 × σ×BR×3000 fb⁻¹. The 2000-event test samples are no longer used.
  - No generator-level filter was needed: the production gridpacks have pT(γ) > 15 GeV, looser than the reco cut.
- **Dropped segments:** QCD Zγ+jets lost 5 of 3000 segments (2 deterministic Delphes segfaults, 3 lost after the LHE stage). Normalisation uses the actual N.
- **Flagged decision:** the no-mjj-cut twins used for the generator-mjj correction (§4) are below σ×BR×3000 fb⁻¹. Only the ratio C enters b, and its MC-stat uncertainty is propagated as a nuisance, so they are accepted as auxiliary samples. They are flagged in the table above.
- **Removed from the registry:** the unused 0-jet MLM Zγγ check sample (B_QCD_llaa_0j) had N = 2307 < σ×L(3000) = 4812. It never entered s or b.

## 3. Normalisation and branching ratios (A6)

- **σ definitions:** σ is the MG5 cross section at the generator cuts, before any analysis BR. The cutflow's first row is σ × BR × L, and after-cut yields are in Tables III/IV.
- **B(H→γγ) = 0.002270** (LHCHXSWG YR4, mH = 125 GeV) is applied **once**, in the analysis. Pythia forces H→γγ with conditional BR = 1.
- **The factor ZF = 0.9783 (Z→ℓℓ in the MG5 matrix element):**
  - MG5 LO computes Γ(Z→ℓℓ) and Γ_Z from its own electroweak inputs (sm model: 2Γ_ℓℓ/Γ_Z = 2 × 83.965 MeV / 2.441404 GeV = 0.06878 for ee + μμ).
  - The closure test σ(ZHjj→ℓℓHjj)/σ(ZHjj) = 0.06964 ± 0.00083 agrees with this ([01_addendum_claude.md](01_addendum_claude.md) item 5).
  - The PDG values are B(Z→ee) = 0.033632 and B(Z→μμ) = 0.033662, giving per-flavour rescalings 0.033632/0.034392 = 0.9779 and 0.033662/0.034392 = 0.9788. **Combined: ZF = 0.067294/0.068784 = 0.9783.**
  - ZF therefore converts MG5's LO width-derived Z→ℓℓ BR to PDG. It is applied only to samples whose Z→ℓℓ decay happens in MG5 with the BR taken from the MG5 widths: the decay chains and the on-shell-Z Zγγ samples.
- **Samples with ℓℓ in the matrix element without a Z decay chain** (Zγjj: `p p > l+ l- a j j`) include γ*/Z interference and need no BR.
- **ggZH:** the Z is undecayed at LHE level and Z→ee/μμ is forced in Pythia8, so k = BR_PDG(Z→ee+μμ) = 0.067294 × B_γγ.

**Per-sample BR ledger.**
- The table is produced by `final_analysis.py`. It asserts that the product of the listed factors equals the k used in the event weight, and that no factor appears twice; otherwise the analysis aborts.
- The last column is the off-shell/FSR correction (§4), which is not a BR.

| sample | Z/W/t decay | H decay | factors in k | k | off-shell corr. |
|---|---|---|---|---|---|
| S_EW_ZHjj | Z->ll in MG5 ME (e,mu) | H->gg forced in PY8 (cond. BR 1) | ZF × BGG | 0.00222074 | 1 |
| H_QCD_ZHjj | Z->ll in MG5 ME (e,mu) | H->gg forced in PY8 (cond. BR 1) | ZF × BGG | 0.00222074 | 1 |
| H_ggZH | Z->ee/mumu forced in PY8 (cond. BR 1) | H->gg forced in PY8 (cond. BR 1) | BR_ZLL × BGG | 0.000152757 | 1 |
| H_ttH | t->b l nu in MG5 (l=e,mu) | H->gg forced in PY8 (cond. BR 1) | BGG | 0.00227 | 1 |
| H_ZH_tautau | Z->tautau in MG5 ME | H->gg forced in PY8 (cond. BR 1) | BGG | 0.00227 | 1 |
| H_tHW | t, W -> l nu in MG5 | H->gg forced in PY8 (cond. BR 1) | BGG | 0.00227 | 1 |
| B_QCD_Zaajj_vbs | Z->ll in MG5 decay chain | no H (prompt photons in ME) | ZF | 0.9783 | 1.128 |
| B_EW_Zaajj_vbs_is1 | Z->ll in MG5 decay chain | no H (prompt photons in ME) | ZF | 0.9783 | 1.128 |
| B_EW_Zaajj_vbs_is2 | Z->ll in MG5 decay chain | no H (prompt photons in ME) | ZF | 0.9783 | 1.128 |
| B_EW_Zaajj_vbs_is3 | Z->ll in MG5 decay chain | no H (prompt photons in ME) | ZF | 0.9783 | 1.128 |
| T_ttaa | t->b l nu in MG5 | no H | one | 1 | 1 |
| F_QCD_Zajj | l+l- in ME (gamma*/Z, no decay chain) | no H | one | 1 | 1 |
| F_EW_Zajj | l+l- in ME (gamma*/Z, no decay chain) | no H | one | 1 | 1 |
| T_tta | t->b l nu in MG5 | no H | one | 1 | 1 |
| T_tWa | t, W -> l nu in MG5 | no H | one | 1 | 1 |

## 4. Background model, overlap removal and generator-level checks

The background model is aligned with the reference: prompt Zγ and Zγγ (QCD and EW), tt̄γ, tWγ, tt̄γγ, plus resonant H→γγ backgrounds (QCD ZHjj in def. a, ggZH, tt̄H, ZH(ττ), tHW).

**Estimation hierarchy** (recorded per number in Table IV):
- **L0:** direct, ≥ 10 raw events in the window.
- **L1:** continuum, N(105–165 GeV) × f_win (exponential MLE of the sample's Delphes mγγ).
- **L2:** VBS-factorised.
- **L2b:** VBS- and window-factorised, using the direct sample (fallback when L2 has no support in the wide mγγ range).
- **UL:** zero support, central value 1.14 w_evt.
- L2, L2b and UL carry 100 % uncertainty. **The transfer-factor method (old L3) is no longer used for yields.**

**Hard/soft photon overlap removal:** uses the GenTruth count of prompt photons (pT > 15 GeV, \|η\| < 2.5, ΔR > 0.4). One-ME-photon samples keep n_prompt ≤ 1.

**tt̄γ / tWγ (A9).**
- **Direct yields at the optimum:**
  - tt̄γ: 0.0031 events at 500 fb⁻¹ via L2 VBS-factorised (100% unc.).
  - tWγ: 0.0003 events via L2 VBS-factorised (100% unc.).
  - Zero raw events pass all cuts. The direct zero-count 95 % UL is 3 w_evt = 0.123 and 0.122 events; using it instead is a robustness row.
- **Transfer-factor cross-check** (old method): 0.0006 and 0.0001 events.
- **Cross-check against the reference [γ pT 25 vs 20 GeV]:**
  - Reference-like baseline (70 < mℓℓ < 120 GeV, mℓℓγγ > 100 GeV, mjj > 700 GeV, |Δηjj| > 2.0, **photon pT > 25 GeV**), **before any mγγ window**: tt̄γ has 5 raw events, so y < 0.000 events at 500 fb⁻¹ (95 % CL). The preselection has 480 raw events and the lepton/photon cuts keep 84.
  - The reference quotes **0.15 ± 0.10** events (Table IV, photon pT > 20 GeV, no Higgs window). The results are compatible within the reference's uncertainty.
  - Expected differences: the higher photon threshold, the n_prompt ≤ 1 overlap removal (not applied in the reference), and the reference's 2.5-event-weight statistics.

**tt̄γ / tWγ cut-flow cross-check against the reference (closeout check 1; `scripts/analysis/tta_xcheck.py`, `work/final_ntuples/tta_xcheck.json`).**
- Reference cut flow, before any mγγ window, at 500 fb⁻¹.
- The reference column gives arXiv:2512.07689 Table III, converted to events, and Table IV for the final row (0.15 ± 0.10).
- `ovl` = our hard/soft-photon overlap removal (n_prompt ≤ 1).
- `gpt` = photon pT threshold: 20 GeV is the reference's, 25 GeV ours.

*T_tta, ovl=True, gpt=20* (w_evt = 0.0411 events at 500 fb⁻¹)

| step | raw | yield at 500 fb⁻¹ | eff. vs previous step | reference |
|---|---|---|---|---|
| initial selection | 60 | 2.469 | — | 32.2 |
| + m_llgg > 100 | 59 | 2.428 | 0.983 | 32 |
| + 70 < m_ll < 120 | 10 | 0.411 | 0.169 | 8.8 |
| + mjj > 700, |deta| > 2.0 (full ref. cut flow) | 0 | 0 (< 0.047 @68 %, < 0.123 @95 %) | 0.000 | 0.15 |
| [ours] + pT1/mgg > 1/3, pT2/mgg > 1/4 | 0 | 0 (< 0.047 @68 %, < 0.123 @95 %) | 0.000 | — |

*T_tta, ovl=False, gpt=20* (w_evt = 0.0411 events at 500 fb⁻¹)

| step | raw | yield at 500 fb⁻¹ | eff. vs previous step | reference |
|---|---|---|---|---|
| initial selection | 479 | 19.708 | — | 32.2 |
| + m_llgg > 100 | 474 | 19.502 | 0.990 | 32 |
| + 70 < m_ll < 120 | 115 | 4.732 | 0.243 | 8.8 |
| + mjj > 700, |deta| > 2.0 (full ref. cut flow) | 5 | 0.206 | 0.043 | 0.15 |
| [ours] + pT1/mgg > 1/3, pT2/mgg > 1/4 | 4 | 0.165 | 0.800 | — |

*T_tta, ovl=False, gpt=25* (w_evt = 0.0411 events at 500 fb⁻¹)

| step | raw | yield at 500 fb⁻¹ | eff. vs previous step | reference |
|---|---|---|---|---|
| initial selection | 350 | 14.400 | — | 32.2 |
| + m_llgg > 100 | 349 | 14.359 | 0.997 | 32 |
| + 70 < m_ll < 120 | 84 | 3.456 | 0.241 | 8.8 |
| + mjj > 700, |deta| > 2.0 (full ref. cut flow) | 5 | 0.206 | 0.060 | 0.15 |
| [ours] + pT1/mgg > 1/3, pT2/mgg > 1/4 | 4 | 0.165 | 0.800 | — |

*T_tWa, ovl=True, gpt=20* (w_evt = 0.0408 events at 500 fb⁻¹)

| step | raw | yield at 500 fb⁻¹ | eff. vs previous step | reference |
|---|---|---|---|---|
| initial selection | 10 | 0.408 | — | 32.2 |
| + m_llgg > 100 | 10 | 0.408 | 1.000 | 32 |
| + 70 < m_ll < 120 | 5 | 0.204 | 0.500 | 8.8 |
| + mjj > 700, |deta| > 2.0 (full ref. cut flow) | 0 | 0 (< 0.046 @68 %, < 0.122 @95 %) | 0.000 | 0.15 |
| [ours] + pT1/mgg > 1/3, pT2/mgg > 1/4 | 0 | 0 (< 0.046 @68 %, < 0.122 @95 %) | 0.000 | — |

*T_tWa, ovl=False, gpt=20* (w_evt = 0.0408 events at 500 fb⁻¹)

| step | raw | yield at 500 fb⁻¹ | eff. vs previous step | reference |
|---|---|---|---|---|
| initial selection | 67 | 2.730 | — | 32.2 |
| + m_llgg > 100 | 67 | 2.730 | 1.000 | 32 |
| + 70 < m_ll < 120 | 23 | 0.937 | 0.343 | 8.8 |
| + mjj > 700, |deta| > 2.0 (full ref. cut flow) | 0 | 0 (< 0.046 @68 %, < 0.122 @95 %) | 0.000 | 0.15 |
| [ours] + pT1/mgg > 1/3, pT2/mgg > 1/4 | 0 | 0 (< 0.046 @68 %, < 0.122 @95 %) | 0.000 | — |

- **Finding:**
  - With `ovl=True`, 87 % of the tt̄γ initial selection was discarded (479 → 60 raw). The second "prompt" photon in those events is mostly radiated by top-decay products, which the decay-chain tt̄γγ matrix element does not contain.
  - Without the removal, the full reference cut flow at pT > 20 GeV gives 5 raw events = 0.21 ± 0.09, against **0.15 ± 0.10** in the reference: consistent at 0.4σ.
  - The initial selection is 1.6× below the reference (19.7 vs 32.2 events). This is expected from the different generator lepton cuts and pT thresholds, and it does not propagate to the final row.
- **Fix applied:** tt̄γ/tWγ are **not** overlap-removed. This is conservative and follows the reference. Double counting with tt̄γγ is bounded by the latter's full yield.
- **Measured efficiencies on our sample** (tt̄γ, no overlap removal):
  - photon pT > 25 vs 20 GeV: 350/479 = 0.73 at the initial selection;
  - mℓℓγγ > 100 GeV: 0.99;
  - Z window 70–120 GeV: 0.24;
  - mjj > 700 GeV, |Δηjj| > 2.0: 0.043;
  - pT/mγγ cuts (ours, not in the reference): 0.80.
- **In the signal region** (Z window ±25 GeV, mjj > 500 GeV, |Δηjj| > 3.5, mγγ window), tt̄γ/tWγ have **zero raw events** and enter through a factorised estimate (L2 VBS-factorised (100% unc.), 100 % uncertainty): tt̄γ 0.0031, tWγ 0.0003 events at 500 fb⁻¹. The direct zero-count 95 % upper limits are a robustness row.

**Zγγ on-shell Z and off-shell/FSR (A4).**
- The Zγγjj samples are `p p > z a a j j, z > l+ l-`, so photons radiated in the Z decay and off-shell γ*/Z are missing.
- **Bound from a dedicated MG5 pair** (`cards/theory/Q_*0j.mg5`, 20 k events each, QCD 0-jet proxy, all non-jet analysis cuts):
  - σ(`p p > l+ l- a a`) / σ(`p p > z a a, z > l+ l-`) = **1.128 ± 0.024**, compared with 2.73 before cuts.
  - The reference's inclusive/on-shell EW ratio is 1.128 after its mℓℓ cut and 1.078 after all cuts (Tables III–IV) **[γ pT 25 vs 20 GeV]**.
- **Applied:** the on-shell-Z Zγγ samples (QCD and EW) are scaled by **1.128**, with a correlated ±5.7 % nuisance (half the correction).

**EW–QCD interference (A3; as reference Sec. II C).**
- **ZHjj** (I_ZHjj, 20 k signed-weight events; Z and H undecayed):
  - Inclusive: σ_I = -0.124 fb. In the VBS jet region (mjj > 500 GeV, |Δη| > 3.5): σ_I = -0.0174 ± 0.0018 fb.
  - This is **-0.20 ± 0.02 % of EW ZHjj** (def. a) and -0.13 % of EW + QCD ZHjj (def. b). It is negligible and not included.
- **Zγγjj:** σ_I/σ_EW = **+2.3 ± 0.3 %** in the VBS + photon region (inclusive +6.4 %), from dedicated MG5 runs with an undecayed on-shell Z (squared-order syntax cannot be combined with a decay chain in MG5 3.6.3).
  - It is non-negligible, so it is included as a ±2.3 % nuisance on EW Zγγjj.

**Generator mjj > 400 GeV cut of the VBS-biased samples (A1).**
- Measured on the Tier-1 samples generated without an mjj cut. The quantity is P(max parton-pair mjj < 400 GeV | reco mjj > 500 GeV, |Δηjj| > 3.5), i.e. the fraction of the reco region removed by the generator cut:
  - **EW ZHjj: 1.4 %.** The cut is safe for EW-type samples (EW Zγγjj, EW Zγjj, coupling samples), given the 9 % mjj resolution and the 100 GeV margin.
  - **QCD ZHjj: 64 %.** In QCD-type events the reco tag jets are often parton-shower jets, so **the cut is not safe for QCD-type samples.**
- **Correction for QCD-type samples:** QCD Zγjj and QCD Zγγjj are corrected by C(cuts) = Y(no-mjj-cut twin)/Y(VBS-biased), measured directly at Delphes level with the same VBS, Z-window and photon cuts. The twins are 200 k / 100 k events with mmjj = 0.
  - F_QCD_Zajj: C = 2.05 ± 3 % (raw 875 / 150317); B_QCD_Zaajj_vbs: C = 2.37 ± 6 % (raw 412 / 1340).
  - The statistical uncertainty of C is a nuisance. C statistics at the optimum (relaxed selection: same VBS, Z-window and photon pT cuts; 1 photon for Zγ+jets, 2 photons in 105–165 GeV for Zγγ):

| process | twin sample | raw (twin) | raw (VBS-biased) | C | MC stat twin | MC stat biased | rel. unc. of C | δb at 500 fb⁻¹ | δb / b |
|---|---|---|---|---|---|---|---|---|---|
| F_QCD_Zajj | F_QCD_llajj_nomjj | 875 | 150317 | 2.052 | 3.4 % | 0.26 % | 3.4 % | 0.0013 | 0.24 % |
| B_QCD_Zaajj_vbs | B_QCD_zaajj_nomjj | 412 | 1340 | 2.366 | 4.9 % | 2.73 % | 5.6 % | 0.0042 | 0.80 % |

  - The last two columns are the `genmjj_*` entries of the b uncertainty budget (§6).
- **The optimum at the mjj = 500 GeV scan boundary** (`figures/z_vs_mjj`, `z_vs_deta`):
  - Cuts below 500 GeV are shaded in the figure because, for the QCD-type samples, they rely entirely on the correction above.
  - Z_Eq1 (Z with σ_b) at 500 fb⁻¹ for mjj > 400 / 450 / 500 / 600 GeV, with the other cuts at the optimum: 0.119 (0.118) / 0.119 (0.118) / 0.119 (0.118) / 0.117 (0.117).
  - Going below the boundary therefore changes Z by +0 % at most. That gain would rely on the QCD-type correction extrapolated to a region where the generator cut sits inside the resolution tail.

**Fake-factor cross-check (Delphes jets).**
- f = 10⁻³ gives 0.0284 events (band 0.0142–0.0568), vs 0.0372 direct, at the final selection and 500 fb⁻¹.
- These values are before the generator-mjj correction.

## 5. Selection and optimisation

- **Reference-like baseline** (arXiv:2512.07689 Sec. III) **[γ pT 25 vs 20 GeV]:** OSSF 70 < mℓℓ < 120 GeV; two photons with **pT > 25 GeV** (reference: 20 GeV); mℓℓγγ > 100 GeV; mjj > 700 GeV, |Δηjj| > 2.0; mγγ within ±2σ.
- **Optimisation** uses expected quantities only, at 500 fb⁻¹ for def. (a). It is a coordinate descent with the FOM Z(σ_b), where σ_b includes theory. A plateau rule picks the highest-signal point within 97 % of Z_max.
- **Optimum:** 2 photons with pT > 25 GeV, pT(γ1)/mγγ > 0.33, pT(γ2)/mγγ > 0.25; |mℓℓ − mZ| < 25 GeV; mℓℓγγ > 100 GeV; no b-veto; no Zeppenfeld cut; mjj > 500 GeV, |Δηjj| > 3.5; 120.8 < mγγ < 129.1 GeV (±2.0σ, σ = 2.07 GeV).
- **mjj × |Δηjj| landscape** (`figures/scan_mjj_deta_*`, tables below): Z_Eq1 at 500 fb⁻¹ ranges from 0.087 to 0.121.
- **1D curves (A1):**
  - mjj cut from 400 to 1200 GeV: Z_Eq1 at 500 fb⁻¹ ranges from 0.090 to 0.119.
  - |Δηjj| from 2.0 to 5.0: Z_Eq1 ranges from 0.107 to 0.121.

## 6. Results

### PRIMARY: Eq. 1 counting significance (stat. only, ± MC stat), Z_syst (incl. theory) and limits

| L [fb⁻¹] | signal definition | s | b | Z_Eq1 ± MC | Z_syst counting (incl. theory) | Z_syst (binned PL fit, incl. theory) | μ₉₅ CLs (exact Poisson, syst incl. theory) | μ₉₅ (binned PL fit, asymptotic) |
|---|---|---|---|---|---|---|---|---|
| 500 | (a) EW ZHjj; QCD ZHjj in b | 0.088 | 0.520 | 0.119 ± 0.002 | 0.118 | 0.125 | 34.5 | 32.5 |
| 500 | (b) EW + QCD ZHjj | 0.135 | 0.472 | 0.188 ± 0.005 | 0.187 | 0.200 | 22.7 | 20.8 |
| 1000 | (a) EW ZHjj; QCD ZHjj in b | 0.176 | 1.039 | 0.168 ± 0.003 | 0.166 | 0.176 | 23.7 | 19.3 |
| 1000 | (b) EW + QCD ZHjj | 0.271 | 0.944 | 0.266 ± 0.006 | 0.264 | 0.281 | 15.8 | 12.3 |
| 3000 | (a) EW ZHjj; QCD ZHjj in b | 0.527 | 3.118 | 0.291 ± 0.005 | 0.282 | 0.300 | 10.4 | 9.1 |
| 3000 | (b) EW + QCD ZHjj | 0.812 | 2.833 | 0.462 ± 0.011 | 0.447 | 0.478 | 7.0 | 5.7 |

- **s < 1 in every row:** Z alone is not meaningful.
- **μ₉₅ (exact-Poisson CLs):** counting in the window, with b and s marginalised over log-normals (σ_b and σ_s include theory). This is the robust number.
- **Asymptotic fit limits** are shown for completeness only; they underestimate the limit at these counts.
- **Largest background components** at 500 fb⁻¹, def. (a): B_EW_Zaajj_vbs_is2 0.1121; B_EW_Zaajj_vbs_is1 0.1090; B_QCD_Zaajj_vbs 0.0739; H_ggZH 0.0539; H_QCD_ZHjj 0.0474.

### Table R1 - PRIMARY: Eq. 1 counting significance (stat. only, +- MC stat), 13.6 TeV

| L [fb^-1] | signal def. | s +- MC | b +- MC | sigma_b (incl. theory) | Z_Eq1 +- MC | Z_syst (counting, incl. theory) | Z_syst (no theory) | mu95 CLs (syst incl. theory) | mu95 (no theory) | mu95 (stat only) | median n_obs (b-only) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 500 | (a) EW ZHjj; QCD ZHjj in b | 0.088 +- 0.001 | 0.520 +- 0.018 | 0.070 | 0.119 +- 0.002 | 0.118 | 0.119 | 34.5 | 34.1 | 34.1 | 0 |
| 500 | (b) EW+QCD ZHjj | 0.135 +- 0.002 | 0.472 +- 0.018 | 0.068 | 0.188 +- 0.005 | 0.187 | 0.188 | 22.7 | 22.2 | 22.1 | 0 |
| 1000 | (a) EW ZHjj; QCD ZHjj in b | 0.176 +- 0.002 | 1.039 +- 0.035 | 0.140 | 0.168 +- 0.003 | 0.166 | 0.167 | 23.7 | 23.4 | 23.3 | 1 |
| 1000 | (b) EW+QCD ZHjj | 0.271 +- 0.005 | 0.944 +- 0.035 | 0.136 | 0.266 +- 0.006 | 0.264 | 0.266 | 15.8 | 15.3 | 15.3 | 1 |
| 3000 | (a) EW ZHjj; QCD ZHjj in b | 0.527 +- 0.005 | 3.118 +- 0.106 | 0.421 | 0.291 +- 0.005 | 0.282 | 0.288 | 10.4 | 10.2 | 10.1 | 3 |
| 3000 | (b) EW+QCD ZHjj | 0.812 +- 0.015 | 2.833 +- 0.105 | 0.407 | 0.462 +- 0.011 | 0.447 | 0.457 | 7.0 | 6.8 | 6.8 | 3 |

### Table R2 - SUPPLEMENTARY: binned profile-likelihood fit in m_gg (window + sidebands, Asimov, asymptotic)

| L [fb^-1] | signal def. | Z (fit, stat only) | Z_syst (fit) | mu95 (fit, stat only) | mu95 (fit, syst) |
|---|---|---|---|---|---|
| 500 | (a) EW ZHjj; QCD ZHjj in b | 0.126 | 0.125 | 32.2 | 32.5 |
| 500 | (b) EW+QCD ZHjj | 0.201 | 0.200 | 20.4 | 20.8 |
| 1000 | (a) EW ZHjj; QCD ZHjj in b | 0.178 | 0.176 | 19.0 | 19.3 |
| 1000 | (b) EW+QCD ZHjj | 0.284 | 0.281 | 12.0 | 12.3 |
| 3000 | (a) EW ZHjj; QCD ZHjj in b | 0.308 | 0.300 | 8.9 | 9.1 |
| 3000 | (b) EW+QCD ZHjj | 0.492 | 0.478 | 5.6 | 5.7 |

### Table III-like - cutflow at the optimum, 500 fb^-1: expected events (raw MC events)

| step | S_EW_ZHjj | H_QCD_ZHjj | H_ggZH | H_ttH | H_ZH_tautau | H_tHW | B_QCD_Zaajj_vbs | B_EW_Zaajj_vbs_is1 | B_EW_Zaajj_vbs_is2 | B_EW_Zaajj_vbs_is3 | T_ttaa | F_QCD_Zajj | F_EW_Zajj | T_tta | T_tWa |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| N generated x sigma x BR | 1.44 (200000) | 11.3 (100000) | 5.68 (20000) | 20.6 (42000) | 28.3 (6565) | 0.893 (2000) | 17.4 (100000) | 8.15 (20000) | 7.7 (20000) | 3.33 (20000) | 48.5 (22000) | 3.47e+04 (5989548) | 5.52e+03 (500000) | 4.28e+04 (1040000) | 6.52e+03 (160000) |
| OSSF + >=2 photons + >=2 jets | 0.199 (27721) | 1.09 (9644) | 0.429 (1513) | 0.952 (1945) | 0.013 (3) | 0.0487 (109) | 2.24 (11410) | 1.86 (4052) | 1.7 (3909) | 0.776 (4135) | 2.02 (917) | 8.34 (1439) | 2.14 (194) | 19.7 (480) | 2.73 (67) |
| + Z window & m_llgg | 0.195 (27194) | 1.07 (9453) | 0.427 (1503) | 0.3 (614) | 0 (0) | 0.0129 (29) | 2.2 (11216) | 1.83 (3987) | 1.66 (3829) | 0.763 (4068) | 0.505 (229) | 5.83 (1005) | 1.91 (173) | 4.94 (120) | 0.774 (19) |
| + photon pT, pT/m_gg | 0.169 (23532) | 0.933 (8229) | 0.376 (1324) | 0.249 (509) | 0 (0) | 0.00982 (22) | 1.7 (8675) | 1.36 (2961) | 1.24 (2850) | 0.563 (2998) | 0.328 (149) | 2.6 (449) | 0.928 (84) | 2.92 (71) | 0.285 (7) |
| + b-veto | 0.169 (23532) | 0.933 (8229) | 0.376 (1324) | 0.249 (509) | 0 (0) | 0.00982 (22) | 1.7 (8675) | 1.36 (2961) | 1.24 (2850) | 0.563 (2998) | 0.328 (149) | 2.6 (449) | 0.928 (84) | 2.92 (71) | 0.285 (7) |
| + mjj, deta_jj | 0.0945 (13152) | 0.05 (441) | 0.0559 (197) | 0.00783 (16) | 0 (0) | 0 (0) | 0.238 (1213) | 0.948 (2062) | 0.867 (1994) | 0.35 (1863) | 0.00882 (4) | 0.475 (82) | 0.564 (51) | 0.0823 (2) | 0.0407 (1) |
| + Zeppenfeld | 0.0945 (13152) | 0.05 (441) | 0.0559 (197) | 0.00783 (16) | 0 (0) | 0 (0) | 0.238 (1213) | 0.948 (2062) | 0.867 (1994) | 0.35 (1863) | 0.00882 (4) | 0.475 (82) | 0.564 (51) | 0.0823 (2) | 0.0407 (1) |
| + m_gg window (120.8-129.1) | 0.0879 (12226) | 0.0474 (418) | 0.0539 (190) | 0.00783 (16) | 0 (0) | 0 (0) | 0.0312 (159) | 0.109 (237) | 0.112 (258) | 0.0467 (249) | 0.0022 (1) | 0.029 (5) | 0.0111 (1) | 0 (0) | 0 (0) |

### Table III-like - cutflow at the reference-like baseline (photon pT > 25 GeV; the reference uses 20 GeV), 500 fb^-1: expected events (raw MC events)

| step | S_EW_ZHjj | H_QCD_ZHjj | H_ggZH | H_ttH | H_ZH_tautau | H_tHW | B_QCD_Zaajj_vbs | B_EW_Zaajj_vbs_is1 | B_EW_Zaajj_vbs_is2 | B_EW_Zaajj_vbs_is3 | T_ttaa | F_QCD_Zajj | F_EW_Zajj | T_tta | T_tWa |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| N generated x sigma x BR | 1.44 (200000) | 11.3 (100000) | 5.68 (20000) | 20.6 (42000) | 28.3 (6565) | 0.893 (2000) | 17.4 (100000) | 8.15 (20000) | 7.7 (20000) | 3.33 (20000) | 48.5 (22000) | 3.47e+04 (5989548) | 5.52e+03 (500000) | 4.28e+04 (1040000) | 6.52e+03 (160000) |
| OSSF + >=2 photons + >=2 jets | 0.199 (27721) | 1.09 (9644) | 0.429 (1513) | 0.952 (1945) | 0.013 (3) | 0.0487 (109) | 2.24 (11410) | 1.86 (4052) | 1.7 (3909) | 0.776 (4135) | 2.02 (917) | 8.34 (1439) | 2.14 (194) | 19.7 (480) | 2.73 (67) |
| + Z window & m_llgg | 0.195 (27125) | 1.07 (9446) | 0.426 (1501) | 0.297 (606) | 0 (0) | 0.0121 (27) | 2.21 (11226) | 1.84 (3994) | 1.66 (3825) | 0.765 (4076) | 0.503 (228) | 5.39 (929) | 1.87 (169) | 4.73 (115) | 0.937 (23) |
| + photon pT, pT/m_gg | 0.185 (25738) | 1.02 (8991) | 0.406 (1432) | 0.281 (574) | 0 (0) | 0.0103 (23) | 2.15 (10925) | 1.81 (3932) | 1.64 (3768) | 0.751 (4003) | 0.403 (183) | 3.62 (625) | 1.33 (120) | 3.46 (84) | 0.53 (13) |
| + b-veto | 0.185 (25738) | 1.02 (8991) | 0.406 (1432) | 0.281 (574) | 0 (0) | 0.0103 (23) | 2.15 (10925) | 1.81 (3932) | 1.64 (3768) | 0.751 (4003) | 0.403 (183) | 3.62 (625) | 1.33 (120) | 3.46 (84) | 0.53 (13) |
| + mjj, deta_jj | 0.0901 (12533) | 0.0449 (396) | 0.0528 (186) | 0.00685 (14) | 0 (0) | 0 (0) | 0.351 (1784) | 1.34 (2916) | 1.21 (2787) | 0.477 (2543) | 0.0176 (8) | 0.574 (99) | 0.751 (68) | 0.206 (5) | 0 (0) |
| + Zeppenfeld | 0.0901 (12533) | 0.0449 (396) | 0.0528 (186) | 0.00685 (14) | 0 (0) | 0 (0) | 0.351 (1784) | 1.34 (2916) | 1.21 (2787) | 0.477 (2543) | 0.0176 (8) | 0.574 (99) | 0.751 (68) | 0.206 (5) | 0 (0) |
| + m_gg window (120.8-129.1) | 0.083 (11550) | 0.0416 (367) | 0.0502 (177) | 0.00685 (14) | 0 (0) | 0 (0) | 0.0523 (266) | 0.156 (340) | 0.15 (345) | 0.0625 (333) | 0 (0) | 0.029 (5) | 0.0442 (4) | 0 (0) | 0 (0) |

### Table IV-like - per-process expected yields at the optimum (events), MC-stat, raw MC support, method

| process | role | sigma [fb] | x BR | N_MC | w_evt @500 | yield 500 | yield 1000 | yield 3000 | MC-stat @500 | raw in window | raw 105-165 | method |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S_EW_ZHjj | signal | 1.295 | 0.002221 | 200000 | 7.19e-06 | 0.0879 | 0.1758 | 0.5273 | 0.0008 | 12226 | 12985 | L0 direct |
| H_QCD_ZHjj | bkg (a) / signal (b) | 10.21 | 0.002221 | 100000 | 0.000113 | 0.0474 | 0.0948 | 0.2844 | 0.0023 | 418 | 439 | L0 direct |
| H_ggZH | background | 74.33 | 0.0001528 | 20000 | 0.000284 | 0.0539 | 0.1079 | 0.3236 | 0.0039 | 190 | 197 | L0 direct |
| H_ttH | background | 18.11 | 0.00227 | 42000 | 0.000489 | 0.0078 | 0.0157 | 0.0470 | 0.0020 | 16 | 16 | L0 direct |
| H_ZH_tautau | background | 24.97 | 0.00227 | 6565 | 0.00432 | 0.0049 | 0.0098 | 0.0295 | 0.0049 | 0 | 0 | UL (zero support): 1.14 w_evt |
| H_tHW | background | 0.7868 | 0.00227 | 2000 | 0.000447 | 0.0003 | 0.0007 | 0.0020 | 0.0003 | 0 | 0 | L2 VBS-factorised (100% unc.) |
| B_QCD_Zaajj_vbs | background | 0.0356 | 0.9783 | 100000 | 0.000196 | 0.0739 | 0.1478 | 0.4434 | 0.0059 | 159 | 1025 | L0 direct |
| B_EW_Zaajj_vbs_is1 | background | 0.01666 | 0.9783 | 20000 | 0.00046 | 0.1090 | 0.2179 | 0.6538 | 0.0071 | 237 | 1721 | L0 direct |
| B_EW_Zaajj_vbs_is2 | background | 0.01575 | 0.9783 | 20000 | 0.000435 | 0.1121 | 0.2243 | 0.6728 | 0.0070 | 258 | 1668 | L0 direct |
| B_EW_Zaajj_vbs_is3 | background | 0.0068 | 0.9783 | 20000 | 0.000188 | 0.0467 | 0.0935 | 0.2804 | 0.0030 | 249 | 1556 | L0 direct |
| T_ttaa | background | 0.097 | 1 | 22000 | 0.0022 | 0.0011 | 0.0021 | 0.0063 | 0.0011 | 1 | 3 | L2 VBS-factorised (100% unc.) |
| F_QCD_Zajj | background | 69.46 | 1 | 5989548 | 0.0058 | 0.0372 | 0.0744 | 0.2231 | 0.0085 | 5 | 19 | L1 m_gg-shape (exp. fit, Delphes) |
| F_EW_Zajj | background | 11.05 | 1 | 500000 | 0.0111 | 0.0218 | 0.0436 | 0.1308 | 0.0063 | 1 | 12 | L1 m_gg-shape (exp. fit, Delphes) |
| T_tta | background | 85.58 | 1 | 1040000 | 0.0411 | 0.0031 | 0.0062 | 0.0186 | 0.0031 | 0 | 1 | L2 VBS-factorised (100% unc.) |
| T_tWa | background | 13.04 | 1 | 160000 | 0.0407 | 0.0003 | 0.0007 | 0.0020 | 0.0003 | 0 | 0 | L2 VBS-factorised (100% unc.) |

### Robustness at 500 fb^-1, definition (a) (all rows include the theory nuisances unless stated)

| variation | s | b | Z_Eq1 | Z_syst | mu95 CLs |
|---|---|---|---|---|---|
| optimum | 0.088 | 0.520 | 0.119 | 0.118 | 34.5 |
| window +-1.5 sigma | 0.080 | 0.406 | 0.121 | 0.121 | 38.1 |
| reference-like baseline (photon pT > 25 GeV, not 20) | 0.083 | 0.646 | 0.101 | 0.101 | 36.5 |
| b-veto toggled | 0.084 | 0.520 | 0.114 | 0.113 | 35.9 |
| Zeppenfeld z* < 1.0 | 0.088 | 0.520 | 0.119 | 0.118 | 34.5 |
| mjj > 700, |deta| > 3.0 | 0.076 | 0.448 | 0.111 | 0.110 | 39.9 |
| fake syst 25% | 0.088 | 0.520 | 0.119 | 0.118 | 34.5 |
| fake syst 100% | 0.088 | 0.520 | 0.119 | 0.118 | 34.5 |
| window x0.75 (resolution proxy) | 0.080 | 0.406 | 0.121 | 0.121 | 38.1 |
| window x1.25 (resolution proxy) | 0.091 | 0.630 | 0.112 | 0.112 | 33.2 |
| theory / off-shell / interference nuisances removed | 0.088 | 0.520 | 0.119 | 0.119 | 34.1 |
| ggZH normalisation x2 | 0.088 | 0.574 | 0.113 | 0.112 | 34.5 |
| ggZH normalisation x0.5 | 0.088 | 0.493 | 0.122 | 0.121 | 34.5 |
| no off-shell/FSR correction of Zgg (x1/1.128) | 0.088 | 0.481 | 0.123 | 0.123 | 34.5 |
| ttgamma, tWgamma at their direct zero-count 95% UL (3 w_evt each) | 0.088 | 0.762 | 0.099 | 0.096 | 48.9 |
| CMS-like e/mu/gamma efficiencies (A7 reweighting) | 0.180 | 1.117 | 0.166 | 0.164 | 23.0 |

### CMS-like object-efficiency variation (A7), all luminosities

| L | def | s | b | Z_Eq1 | Z_syst | mu95 CLs |
|---|---|---|---|---|---|---|
| 500 | a | 0.180 | 1.117 | 0.166 | 0.164 | 23.0 |
| 500 | b | 0.275 | 1.021 | 0.261 | 0.258 | 15.4 |
| 3000 | a | 1.078 | 6.700 | 0.406 | 0.383 | 6.2 |
| 3000 | b | 1.650 | 6.128 | 0.640 | 0.601 | 4.3 |

### Uncertainty budget on b at 500 fb^-1, def. (a): correlated groups (events, summed linearly over processes)

| group | delta b [events] | delta b / b |
|---|---|---|
| ggzh_norm | 0.0374 | 7.2 % |
| th_qcdzaa | 0.0241 | 4.6 % |
| th_ewzaa | 0.0238 | 4.6 % |
| offshell | 0.0194 | 3.7 % |
| th_qcdzh | 0.0156 | 3.0 % |
| th_ggzh | 0.0148 | 2.8 % |
| lumi | 0.0130 | 2.5 % |
| th_fqcd | 0.0118 | 2.3 % |
| int_zaa | 0.0061 | 1.2 % |
| genmjj_B_QCD_Zaajj_vbs | 0.0042 | 0.8 % |
| th_tth | 0.0024 | 0.5 % |
| th_zhtt | 0.0016 | 0.3 % |
| th_few | 0.0016 | 0.3 % |
| genmjj_F_QCD_Zajj | 0.0013 | 0.2 % |
| th_top | 0.0012 | 0.2 % |
| per-process normalisation (+) MC stat (uncorrelated) | 0.0340 | |
| **total sigma_b** | 0.0701 | 13.5 % |

### Reference-like baseline results (photon pT > 25 GeV instead of the reference's 20 GeV)

| L | def | s | b | Z_Eq1 +- MC | mu95 |
|---|---|---|---|---|---|
| 500 | a | 0.083 | 0.646 | 0.101 +- 0.002 | 36.5 |
| 500 | b | 0.125 | 0.604 | 0.155 +- 0.004 | 24.6 |
| 1000 | a | 0.166 | 1.292 | 0.143 +- 0.002 | 24.5 |
| 1000 | b | 0.249 | 1.209 | 0.220 +- 0.005 | 16.7 |
| 3000 | a | 0.498 | 3.876 | 0.248 +- 0.004 | 12.3 |
| 3000 | b | 0.748 | 3.627 | 0.380 +- 0.009 | 7.1 |

### Fake-factor cross-check on Delphes jets (QCD Zg+jets, 500 fb^-1)

| estimate | final selection | optimum without VBS-jet cuts |
|---|---|---|
| f=0.0005 | 0.0142 | 0.1105 |
| f=0.001 | 0.0284 | 0.2210 |
| f=0.002 | 0.0568 | 0.4420 |
| pT-dependent | 0.0281 | 0.2110 |
| direct Delphes | 0.0372 | 0.1276 |

### Joint mjj x |deta_jj| scan, Z_Eq1 (def. a), 500 fb^-1

| mjj \ deta | >2.0 | >2.5 | >3.0 | >3.5 | >4.0 | >4.5 |
|---|---|---|---|---|---|---|
| >500 | 0.107 | 0.110 | 0.114 | 0.119 | 0.121 | 0.117 |
| >600 | 0.107 | 0.109 | 0.112 | 0.117 | 0.120 | 0.117 |
| >700 | 0.106 | 0.108 | 0.111 | 0.114 | 0.117 | 0.115 |
| >800 | 0.103 | 0.104 | 0.106 | 0.110 | 0.113 | 0.111 |
| >900 | 0.098 | 0.100 | 0.102 | 0.105 | 0.109 | 0.108 |
| >1000 | 0.095 | 0.096 | 0.098 | 0.101 | 0.104 | 0.104 |
| >1200 | 0.087 | 0.087 | 0.088 | 0.090 | 0.093 | 0.094 |

### Joint mjj x |deta_jj| scan, Z_Eq1 (def. a), 3000 fb^-1

| mjj \ deta | >2.0 | >2.5 | >3.0 | >3.5 | >4.0 | >4.5 |
|---|---|---|---|---|---|---|
| >500 | 0.262 | 0.270 | 0.279 | 0.291 | 0.296 | 0.286 |
| >600 | 0.261 | 0.267 | 0.275 | 0.287 | 0.293 | 0.287 |
| >700 | 0.259 | 0.264 | 0.271 | 0.280 | 0.287 | 0.282 |
| >800 | 0.251 | 0.255 | 0.261 | 0.269 | 0.277 | 0.273 |
| >900 | 0.241 | 0.244 | 0.250 | 0.258 | 0.266 | 0.264 |
| >1000 | 0.232 | 0.235 | 0.240 | 0.247 | 0.255 | 0.255 |
| >1200 | 0.213 | 0.214 | 0.216 | 0.221 | 0.228 | 0.231 |


## 7. Systematic uncertainties

- **Background normalisation** (uncorrelated per process): 10 % for prompt and resonant processes; **50 % for fake-photon processes** (Zγjj, tt̄γ, tWγ), with robustness rows at 25 % and 100 %.
- **Luminosity:** 2.5 %, correlated.
- **MC statistics:** per process. L2, L2b and UL estimates carry 100 % uncertainty.
- **Theory (A2).** MG5 weights give the 7-point scale envelope (μR, μF ∈ {½, 1, 2}, without (½,2) and (2,½)) and the NNPDF3.1 replica standard deviation.
  - Signal and QCD ZHjj: from the Tier-1 LHE (40 k events each).
  - Background samples (LHE deleted after production): from dedicated small LHE-only runs of the *production gridpacks* (`scripts/condor/lhe_only.sh`, 3–10 k events, `work/theory/`).
  - Region: the parton-level proxy of the signal region (two leading partons with mjj > 500 GeV and |Δη| > 3.5; Z window; photon pT and pT/mγγ cuts; mℓℓγγ > 100 GeV), or inclusive for ggZH, tt̄H and top.
  - Symmetrised as max(up, down) ⊕ PDF. Correlated within a theory group (e.g. the three EW Zγγ splits; tt̄γγ/tt̄γ/tWγ) and uncorrelated between groups. Signal theory enters σ_s (μ₉₅) and the fit.

| process | theory group | weight source | region | scale up / down [%] | PDF [%] | total used [%] |
|---|---|---|---|---|---|---|
| S_EW_ZHjj | th_sig | S_EW_ZHjj | R | 8.5 / −7.3 | 1.1 | 8.6 |
| H_QCD_ZHjj | th_qcdzh | H_QCD_ZHjj | R | 32.9 / −23.0 | 1.1 | 33.0 |
| H_ggZH | th_ggzh | H_ggZH_py8dec | incl | 27.3 / −20.3 | 1.0 | 27.4 |
| H_ttH | th_tth | H_ttH | incl | 29.6 / −21.3 | 1.1 | 29.6 |
| H_ZH_tautau | th_zhtt | H_QCD_ZHjj (proxy) | R | 32.9 / −23.0 | 1.1 | 33.0 |
| H_tHW | th_tth | H_ttH (proxy) | incl | 29.6 / −21.3 | 1.1 | 29.6 |
| B_QCD_Zaajj_vbs | th_qcdzaa | B_QCD_zaajj_vbs | R | 32.6 / −22.8 | 1.1 | 32.6 |
| B_EW_Zaajj_vbs_is1 | th_ewzaa | B_EW_zaajj_vbs_is1h | R | 8.2 / −7.1 | 1.3 | 8.3 |
| B_EW_Zaajj_vbs_is2 | th_ewzaa | B_EW_zaajj_vbs_is2 | R | 8.9 / −7.7 | 2.0 | 9.2 |
| B_EW_Zaajj_vbs_is3 | th_ewzaa | B_EW_zaajj_vbs_is3 | R | 7.4 / −6.6 | 5.8 | 9.4 |
| T_ttaa | th_top | T_ttaa | incl | 28.2 / −20.4 | 1.7 | 28.2 |
| F_QCD_Zajj | th_fqcd | F_QCD_llajj_vbs | R | 31.6 / −22.3 | 0.9 | 31.6 |
| F_EW_Zajj | th_few | F_EW_llajj_vbs | R | 7.3 / −6.4 | 0.9 | 7.3 |
| T_tta | th_top | T_tta | incl | 29.2 / −21.1 | 1.0 | 29.2 |
| T_tWa | th_top | T_tWa | incl | 10.4 / −8.6 | 1.2 | 10.5 |

- **Other nuisances:**
  - off-shell/FSR of Zγγ: ±5.7 %, correlated EW+QCD;
  - Zγγjj interference: ±2.3 % on EW Zγγ;
  - **ggZH normalisation ×2 / ×0.5** (log-normal, σ = ln 2), covering the LO loop-induced normalisation and the shower-only jets (robustness rows ×2 and ×0.5);
  - generator-mjj correction of the QCD-type samples (statistical uncertainty of C).
- **Fit:** binned Poisson likelihood in mγγ (16 bins over 105–165 GeV). Per-process log-normals, plus one shared nuisance per correlated group, plus luminosity. Asimov data.

## 8. Limitations

1. **Statistical regime:** s < 1 even at 3000 fb⁻¹, so the Z values are illustrative; the limit is the meaningful quantity.
2. **The Delphes CMS card is not real CMS.**
   - σ_mγγ is about 2.1 GeV (real CMS: about 1.5 GeV).
   - The Delphes prompt-object efficiencies on signal are low (`work/theory/object_eff.json`): electrons 39–73 % (barrel), muons 59–87 %, photons 59–89 %.
   - The CMS-like reweighting (A7, robustness table) raises s by ×2.05, and b by ×2.15.
   - The reweighting uses *assumed* CMS-like efficiencies (e: 65–92 %, μ: 93–96 %, γ: 80–92 % by pT/η; CMS JINST 16 (2021) P05014 and JINST 13 (2018) P06015 as orientation, not a calibrated parametrisation). It cannot recover objects that Delphes misidentifies (e.g. e→γ).
   - The Delphes jet→photon fake rate is a card assumption; the FF band brackets it within a factor of about 2.
3. **Zγγjj uses an on-shell Z.**
   - The off-shell/FSR part is corrected with a 0-jet QCD proxy ratio transferred to jj (EW and QCD). The reference's EW-jj ratio agrees within the assigned uncertainty.
   - The **QCD-type samples needed a generator-mjj correction** (§4) from finite twin samples.
4. **ggZH** is LO loop-induced with shower jets only (×2 nuisance).
5. **LO everywhere.** Theory uncertainties are LO scale ⊕ PDF only; no NLO k-factors; QCD ZHjj is fixed-order ZH+2j.
6. **Double-fake backgrounds** (Z+jets, tt̄) are not in b. They are order-of-magnitude only, as in the reference.
7. **Luminosity scaling:** 3000 fb⁻¹ is scaled at 13.6 TeV, with no pile-up and no HL-LHC detector.
8. **Coupling interpretation (§9):**
   - LO EW ZHjj only.
   - ggZH, tt̄H and tHW are kept at the SM. ggZH depends on κZ (triangle) and κt (box), which is neglected (ggZH is 0.054 events at 500 fb⁻¹).
   - The headline keeps BR(H→γγ) at the SM. The resolved-κγ variant assumes κt = 1 and no BSM loops.
9. **tt̄γ / tWγ** have **zero raw events in the signal region** (N_MC ≥ 4 × σ×BR×3000 fb⁻¹), so they are estimated by factorisation (L2: N(all cuts except VBS, wide mγγ) × ε(VBS | preselection) × f_win; 100 % uncertainty). Replacing them by their direct zero-count 95 % upper limits raises **b at 500 fb⁻¹ from 0.520 to 0.76** (robustness row; μ₉₅ 34.5 → 48.9).
10. **The λWZ sensitivity is modest by construction.** In ZH the SM κW–κZ interference in EW ZHjj is destructive, but flipping the sign of κW raises σ by only a moderate factor: σ(λWZ = −1)/σ(SM) = 2.95 at generator level and 3.8 in the signal region. In addition, λWZ → 0⁻ is almost degenerate with the SM. In VBS/VBF WH, instead, λWZ < 0 breaks the gauge cancellation of the W W → W H amplitude and enhances the high-energy cross section by large factors, which both CMS and ATLAS exploit.
11. **The c_A sensitivity is dominated by the unclipped high-energy tail**, where the validity of the dimension-6 EFT is questionable. With clipping at m(ℓℓγγ) < 500 GeV, the expected 95 % interval at 3000 fb⁻¹ widens from [-0.70, +0.80] to [-3.80, +3.80].


## 9. VH coupling interpretation: λWZ = κW/κZ, κZ, CP-odd (E)

**Motivation and comparison.**
- The sign of λWZ is the target of the recent CMS (PLB 860 (2025) 139202, arXiv:2405.16566) and ATLAS (PRL 133 (2024) 141801, arXiv:2402.00426) analyses. Both use WH/VBF-WH with H→bb̄, and both exclude λWZ < 0 with very high significance in their channels.
- Our channel is ZH with Z→ℓℓ and H→γγ, with VBS-like jets. The EW ZHjj amplitude contains both the WW-fusion (κW) and ZZ-fusion/Higgsstrahlung (κZ) diagrams, so the kinematics and the rate depend on λWZ through the κW–κZ interference, which is destructive in the SM.
- The two experiments have far larger signal rates, so this channel is complementary in final state and production mode, not competitive.

**Model.**
- The official Higgs Characterisation UFO HC_NLO_X0 (FeynRules model database, README model version 1.3; zip sha256 b91d8788…, fetched 2026-11-03) has a single SM-like κSM shared by X0WW and X0ZZ.
- A minimal documented patch (`scripts/models/make_hc_kvv.sh`) adds κ factors `kSMW` and `kSMZ` multiplying κSM in exactly those two couplings. The resulting model is HC_NLO_X0_kVV.
- Effective X0γγ/X0Zγ/X0gg and dim-5 couplings are switched off to match the SM tree level, and the CKM matrix is diagonal.

**Samples.**
- Direct samples at λWZ ∈ {−1, −0.5, 0, 0.5, 1, 1.5} (κZ = 1) and CP-odd c_A = ±2 (Λ = 1 TeV, cos α·κSM = 1). Each has 25 × 2000 events through the identical Pythia8 (forced H→γγ) → slim Delphes chain and selection (mmjj > 400 GeV, safe for EW-type samples, §4).
- **No MG5 reweighting is used.** Because the amplitude is κZ·A_Z + κW·A_W, the yield in every bin is exactly κZ²(a + bλ + cλ²).
- a, b and c are fitted per bin to the six direct points. Closure tests are below.

| point | sample | σ [fb] | N_MC | jobs | σ closure | raw events in SR | s in SR at 500 fb⁻¹ |
|---|---|---|---|---|---|---|---|
| lam_m100 | K_EW_ZHjj_lam_m100 | 2.382 | 50000 | 25 | -1.79 % | 6168 | 0.3263 |
| lam_m050 | K_EW_ZHjj_lam_m050 | 1.201 | 50000 | 25 | -0.00 % | 6381 | 0.1702 |
| lam_p000 | K_EW_ZHjj_lam_p000 | 0.5655 | 50000 | 25 | -0.58 % | 6158 | 0.0773 |
| lam_p050 | K_EW_ZHjj_lam_p050 | 0.4289 | 50000 | 25 | -0.13 % | 5258 | 0.0501 |
| lam_p100 | K_EW_ZHjj_lam_p100 | 0.8067 | 50000 | 25 | -0.47 % | 4838 | 0.0867 |
| lam_p150 | K_EW_ZHjj_lam_p150 | 1.693 | 50000 | 25 | -0.59 % | 5012 | 0.1884 |
| cpo_m2 | K_EW_ZHjj_cpo_m2 | 29.79 | 48000 | 24 | -0.47 % | 4270 | 2.9426 |
| cpo_p2 | K_EW_ZHjj_cpo_p2 | 29.68 | 50000 | 25 | +0.14 % | 4310 | 2.8408 |

| closure test | prediction | direct | ratio | direct MC stat | shape |
|---|---|---|---|---|---|
| mllgg|leave-out lam_m100 | 0.0006516 | 0.0006526 | 0.999 | ±1.3 % | χ² = 9.0 / 7 |
| mllgg|leave-out lam_p150 | 0.0003752 | 0.0003769 | 0.996 | ±1.4 % | χ² = 5.6 / 7 |
| mllgg|leave-out lam_p000 | 0.0001557 | 0.0001547 | 1.007 | ±1.3 % | χ² = 7.2 / 7 |
| ptgg|leave-out lam_m100 | 0.0006528 | 0.0006526 | 1.000 | ±1.3 % | χ² = 18.0 / 7 |
| ptgg|leave-out lam_p150 | 0.0003758 | 0.0003769 | 0.997 | ±1.4 % | χ² = 5.7 / 7 |
| ptgg|leave-out lam_p000 | 0.0001557 | 0.0001547 | 1.007 | ±1.3 % | χ² = 4.4 / 7 |
| HC lambda=1 vs SM Tier-1 signal (full selection, per fb^-1) | 0.0001733 | 0.0001758 | 0.986 | ±1.7 % | — |

**Statistics.**
- The observable is a binned Poisson likelihood of mllgg inside the signal region (all optimum cuts including the mγγ window). It was chosen by expected sensitivity to λWZ = −1 at 3000 fb⁻¹; the −2Δln L values are mllgg: 1.1, ptgg: 0.9.
- Data are Asimov at the SM. All nuisances of the SM result are profiled (signal theory included).
- The background bin fractions come from each process's Delphes distribution, at all cuts except the window, or looser if fewer than 10 raw events remain.
- QCD ZHjj (def. b) scales with κZ².

Intervals are the expected (Asimov SM) ranges where −2Δln L < 1 (68 %) or < 3.84 (95 %); `*` marks an end at the scan boundary (λWZ ∈ [−2, 2], κZ ∈ [0, 3], c_A ∈ [−4, 4]), i.e. no constraint there.

| parameter | L [fb⁻¹] | expected 68 % CL | expected 95 % CL | Z(exclude all λWZ < 0) (exclude λWZ = −1) |
|---|---|---|---|---|
| λWZ (κZ = 1), BR(H→γγ) SM | 500 | [-2.00*, +2.00*] | [-2.00*, +2.00*] | 0.14 (λWZ = −1: 0.43) |
| λWZ, resolved κγ(κW), Γ_H | 500 | [-1.10, +2.00*] | [-1.75, +2.00*] | 0.09 (λWZ = −1: 0.81) |
| λWZ, def. (b) (QCD ZHjj ∝ κZ²) | 500 | [-2.00*, +2.00*] | [-2.00*, +2.00*] | 0.14 |
| λWZ (κZ = 1), BR(H→γγ) SM | 1000 | [-1.65, +2.00*] | [-2.00*, +2.00*] | 0.19 (λWZ = −1: 0.61) |
| λWZ, resolved κγ(κW), Γ_H | 1000 | [-0.90, +1.80] | [-1.35, +2.00*] | 0.13 (λWZ = −1: 1.15) |
| λWZ, def. (b) (QCD ZHjj ∝ κZ²) | 1000 | [-1.65, +2.00*] | [-2.00*, +2.00*] | 0.19 |
| λWZ (κZ = 1), BR(H→γγ) SM | 3000 | [-0.90, +2.00*] | [-1.90, +2.00*] | 0.33 (λWZ = −1: 1.05) |
| λWZ, resolved κγ(κW), Γ_H | 3000 | [-0.65, +1.55] | [-0.95, +1.85] | 0.22 (λWZ = −1: 1.98) |
| λWZ, def. (b) (QCD ZHjj ∝ κZ²) | 3000 | [-0.90, +2.00*] | [-1.90, +2.00*] | 0.33 |
| κZ (λWZ = 1) | 500 | [+0.00*, +3.00*] | [+0.00*, +3.00*] | — |
| κZ (λWZ = 1) | 1000 | [+0.00*, +3.00*] | [+0.00*, +3.00*] | — |
| κZ (λWZ = 1) | 3000 | [+0.00*, +2.30] | [+0.00*, +3.00*] | — |
| CP-odd c_A (Λ = 1 TeV), no clipping | 500 | [-0.90, +1.00] | [-1.70, +1.80] | — |
| c_A, clipped m(ℓℓγγ) < 500 GeV | 500 | [-4.00*, +4.00*] | [-4.00*, +4.00*] | — |
| CP-odd c_A (Λ = 1 TeV), no clipping | 1000 | [-0.70, +0.70] | [-1.30, +1.30] | — |
| c_A, clipped m(ℓℓγγ) < 500 GeV | 1000 | [-3.50, +3.50] | [-4.00*, +4.00*] | — |
| CP-odd c_A (Λ = 1 TeV), no clipping | 3000 | [-0.40, +0.40] | [-0.70, +0.80] | — |
| c_A, clipped m(ℓℓγγ) < 500 GeV | 3000 | [-2.40, +2.40] | [-3.80, +3.80] | — |

**Notes on the results.**
- The 1D intervals can be disjoint, because the quadratic yield allows a second solution with the SM rate.
- The **headline** is the BR(H→γγ)-fixed row: a production-only interpretation in which κγ is a free effective coupling constrained by inclusive H→γγ.
- In the **resolved** variant, κγ² = 1.59κW² + 0.07 − 0.67κW (κt = 1). λWZ = −1 then multiplies BR(H→γγ) by about 2.3, a constraint dominated by the inclusive H→γγ rate.
- The CP-odd interpretation is linear + quadratic in c_A, with and without an energy clipping m(ℓℓγγ) < 500 GeV. The rate is dominated by the quadratic term (0.018 = |linear/quadratic| at c_A = ±2), so clipping mainly shows how much of the sensitivity comes from high energies, where the EFT validity is questionable.
**Comparison with experiment (closeout item 4).** This study is complementary, not competitive: it has an independent final state (Z→ℓℓ, H→γγ) and an independent production mode (EW ZHjj).

| analysis | process, decays | √s, L | 95 % CL limit on the SM signal strength (obs. / exp.) | λWZ < 0 |
|---|---|---|---|---|
| CMS, PLB 860 (2025) 139202, arXiv:2405.16566 | VBS WH, W→ℓν, H→bb̄ | 13 TeV, 138 fb⁻¹ | 14.3 / 9.9 (VBS WH) | excluded beyond 5σ (all scenarios consistent with current measurements) |
| ATLAS, PRL 133 (2024) 141801, arXiv:2402.00426 | VBF WH, W→ℓν, H→bb̄ | 13 TeV, 140 fb⁻¹ | 9.0 / 8.7 (VBF WH) | excluded at ≫ 5σ |
| **this study (expected)** | EW ZHjj, Z→ee/μμ, H→γγ | 13.6 TeV, 500 / 3000 fb⁻¹ | — / 34.5 (500), 10.4 (3000) | Z(all λWZ < 0) = 0.14 / 0.33; Z(λWZ = −1) = 0.43 / 1.05 |

Quantitative reasons for the gap:
- **Higgs decay:** BR(H→γγ)/BR(H→bb̄) = 0.00227/0.5809 ≈ 1/256.
- **Vector-boson decay:** BR(Z→ee+μμ)/BR(W→eν+μν) = 0.0673/0.214 ≈ 0.31.
- **Interference structure:** σ(λWZ = −1)/σ(SM) = 3.0 in EW ZHjj (limitation 10). In VBS/VBF WH the λWZ < 0 enhancement grows with energy.
- **Luminosity:** the experiments use 138–140 fb⁻¹ of observed data at 13 TeV. Our expected numbers need 500–3000 fb⁻¹ to reach μ₉₅ ≈ 35–10, and λWZ = −1 still reaches only Z ≈ 1 at 3000 fb⁻¹.
- **CP-odd:** published HVV CP limits are quoted as f_a3, defined in the H→ZZ decay (JHU convention, with the a₃ normalised to the H→ZZ*→4ℓ cross section). Our c_A = sin α·κ_AVV with Λ = 1 TeV is defined in the HC UFO for production in EW ZHjj, with κ_AZZ = κ_AWW.
  - A reliable conversion needs σ₃/σ₁ for H→ZZ*→4ℓ in the HC normalisation, which was not computed here.
  - **We therefore make no numerical comparison with published f_a3 limits.** Only the convention difference is stated.
- Figures: `lambdaWZ_scan`, `kappaZ_lambdaWZ_500/3000`, `lambdaWZ_dist_{mllgg,ptgg,mjj,detajj}` (SM vs λWZ = −1 and 0), `cA_scan`.

## 10. Figures (`figures/`, PDF + PNG)

- **Distributions:** `m_gg`, `m_ll`, `m_jj`, `deta_jj`, `photon1_pt`, `photon2_pt`, `zeppenfeld`.
  - 3000 fb⁻¹, all optimum cuts except the VBS cuts and the window.
  - The QCD-type samples are drawn from their no-mjj-cut twins.
- **Significance scans:**
  - `scan_mjj_deta_500`, `scan_mjj_deta_3000` (reference Fig. 4 style);
  - `z_vs_mjj`, `z_vs_deta` (A1).
- **Coupling:** `lambdaWZ_scan`, `kappaZ_lambdaWZ_500`, `kappaZ_lambdaWZ_3000`, `lambdaWZ_dist_*`, `cA_scan`.

## 11. Checks

- **σ closure:** < 1 % for every final sample; < 1.8 % for the coupling samples.
- **Ntuples:** event counts equal the verified job totals.
- **BR ledger and N_MC ≥ σ×BR×3000 fb⁻¹:** asserted in code (§2, §3).
- **ggZH decay closure:** 98.4 % of events have a prompt ee/μμ pair, with no ττ.
- **Coupling morphing closure:** §9.
- **Re-optimisation:** Z_syst at the optimum minus Z_syst at the reference-like baseline = +0.017 at 500 fb⁻¹ **[γ pT 25 vs 20 GeV]**.
