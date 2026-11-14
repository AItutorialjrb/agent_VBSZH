# FINAL report — EW W±Hjj (W→eν/μν, H→γγ), √s = 13.6 TeV — single-agent arm, run single_r1

**Date:** 2026-11-14 10:56 UTC. **Status: FINAL (expected results; Delphes level; LO MC).** Phases 01–03 (G1, accepted 2026-11-14 with the declared defaults) and 05–07 (amendment A2) of this run; Phase 04 (production) is the canonical frozen package `p2/production/wh` (wh-prod-v1 + v1.1 rows, read-only) plus one own sample.
Reports: `01_signal_definition.md`, `02_background_overlap.md`, `03_generation_validation.md` (+ addendum), `05_selection.md`, `06_systematics.md`, `07_sensitivity.md`; machine-readable `final.json`; self-reviews `../reviews/wh_01-03_self_review.md`, `../reviews/wh_05-07_self_review.md`.

## 1. Result
Signal definition (a): EW W±Hjj at (QCD, QED) = (0, 4), 4F jets, W→eν/μν, H→γγ (BR applied once); QCD W±H(+jets) is a resonant background. Definition (b): signal = EW + QCD W±H.
Final selection: one lepton (pT>25, veto on a 2nd lepton >10 GeV), two photons (pT/m_γγ > 1/3, 1/4), 2 jets pT>30, b-veto, m_eγ Z-veto, m_jj > 300, |Δη_jj| > 2.0, **BDT > 0.88** (xgboost, 5-fold, m_γγ not an input), window 120.9–129.0 GeV (±2σ of the Delphes peak, σ = 2.03 GeV).

| L [fb⁻¹] | def | s | b | σ_b | **Z Eq. 1 (stat) ± MC** | Z with σ_b | μ95 CLs exact Poisson (syst) | μ95 (stat) | Z m_γγ fit (syst) | μ95 fit (syst) |
|---|---|---|---|---|---|---|---|---|---|---|
| 500 | a | 1.19 | 1.26 | 0.26 | **0.94 ± 0.01** | 0.91 | 3.50 | 3.37 | 0.90 | 3.11 |
| 1000 | a | 2.38 | 2.53 | 0.53 | **1.33 ± 0.02** | 1.24 | 2.03 | 1.93 | 1.27 | 1.94 |
| 3000 | a | 7.15 | 7.58 | 1.58 | **2.30 ± 0.04** | 1.93 | 1.06 | 0.95 | 2.15 | 0.99 |
| 500 | b | 1.27 | 1.18 | 0.25 | **1.02 ± 0.02** | 0.99 | 3.30 | 3.18 | 0.98 | 2.85 |
| 1000 | b | 2.54 | 2.37 | 0.50 | **1.44 ± 0.03** | 1.35 | 1.93 | 1.84 | 1.38 | 1.78 |
| 3000 | b | 7.62 | 7.10 | 1.49 | **2.50 ± 0.04** | 2.11 | 1.02 | 0.92 | 2.35 | 0.89 |

**Cut-based selection (no BDT; reported alongside because the BDT stability is marginal):**

| L [fb⁻¹] | def | s | b | σ_b | Z Eq. 1 ± MC | Z with σ_b | μ95 (syst) | μ95 (stat) |
|---|---|---|---|---|---|---|---|---|
| 500 | a | 0.81 | 1.73 | 0.66 | **0.58 ± 0.01** | 0.51 | 5.07 | 6.10 |
| 1000 | a | 1.63 | 3.46 | 1.32 | **0.82 ± 0.02** | 0.65 | 3.56 | 3.19 |
| 3000 | a | 4.88 | 10.38 | 3.95 | **1.41 ± 0.03** | 0.86 | 2.12 | 1.61 |
| 500 | b | 0.87 | 1.67 | 0.64 | **0.62 ± 0.01** | 0.55 | 4.75 | 4.48 |
| 1000 | b | 1.74 | 3.35 | 1.27 | **0.88 ± 0.02** | 0.71 | 3.34 | 3.01 |
| 3000 | b | 5.21 | 10.05 | 3.82 | **1.53 ± 0.03** | 0.93 | 1.82 | 1.55 |

**Coupling interpretation (rate only, BR(H→γγ) fixed to SM, κ_Z = 1 for λ_WZ):**

| L [fb⁻¹] | Z excl. λ_WZ = −1 | Z excl. λ_WZ < 0 | λ_WZ 68 % | λ_WZ 95 % |
|---|---|---|---|---|
| 500 | 4.2 | 1.21 | [0.07, 1.48] | [-0.27, 1.82] |
| 1000 | 5.9 | 1.70 | [0.19, 1.37] | [-0.07, 1.63] |
| 3000 | 10.1 | 2.88 | [0.31, 1.24] | [0.14, 1.42] |

(κ_W, κ_Z): quadratic yield Y = 3.956 κ_W² -6.262 κ_W κ_Z + 3.511 κ_Z² events at 500 fb⁻¹ (fit to six λ points; closure on the two κ points and the SM sample within 2σ); contours `figures/p07_kappa_contours.png`.

**In words.** At 500 fb⁻¹ the expected EW W±Hjj significance is below 1σ (Eq. 1: 0.94; cut-based 0.58); at 3000 fb⁻¹ (luminosity scaling of the Run-3-like detector, not an HL-LHC prediction) it reaches 2.3σ stat-only and 1.9σ with systematics (cut-based 1.4 / 0.9). The expected 95 % CL limit on μ is 3.5 × SM at 500 fb⁻¹ and ≈ 1.1 × SM at 3000 fb⁻¹. The sign-flipped coupling λ_WZ = −1 (5× the SM rate) is excluded at 4.2σ already at 500 fb⁻¹; excluding all λ_WZ < 0 by rate is limited by λ → 0⁻ (1.2σ / 2.9σ at 500 / 3000 fb⁻¹).

## 2. Background composition (final selection, 500 fb⁻¹, def. a; every source in 05 §7)
EW Wγγjj 0.48, tHq 0.13, QCD Wγγjj 0.11, Wγ+jets (1 non-prompt γ) 0.11, W→τν feed-down 0.08, QCD WH 0.08, ZH lost-ℓ 0.06, e→γ 0.09, non-prompt ℓ 0.059, W+jets 2 fakes 0.018, Zγγjj lost-ℓ 0.031, top 0.010, tt̄H/tHW 0.003 events. Non-prompt photons, non-prompt leptons and e→γ are estimated separately by per-object weighting with declared rate scenarios, each with a closure test against Delphes (05 §4) and its own uncertainty (06).

## 3. Robustness (500 fb⁻¹, def. a; full table 07 §2)
- nominal: Z Eq. 1 = 0.94, Z(σ_b) = 0.91, μ95 = 3.50
- j->gamma x0.3 (low): Z Eq. 1 = 0.96, Z(σ_b) = 0.93, μ95 = 3.53
- j->gamma x3 (high): Z Eq. 1 = 0.85, Z(σ_b) = 0.79, μ95 = 3.44
- j->gamma Delphes-measured rate (FORMAT 6a): Z Eq. 1 = 0.97, Z(σ_b) = 0.94, μ95 = 3.53
- e->gamma 1 % (low): Z Eq. 1 = 0.94, Z(σ_b) = 0.91, μ95 = 3.51
- e->gamma 5 % (high): Z Eq. 1 = 0.92, Z(σ_b) = 0.89, μ95 = 3.49
- e->gamma Delphes-measured rate (FORMAT 6b): Z Eq. 1 = 0.91, Z(σ_b) = 0.88, μ95 = 3.48
- j->lepton 3e-5 (low): Z Eq. 1 = 0.95, Z(σ_b) = 0.92, μ95 = 3.51
- j->lepton 1e-3 (high): Z Eq. 1 = 0.89, Z(σ_b) = 0.84, μ95 = 3.47
- all fake/mis-ID rates high: Z Eq. 1 = 0.80, Z(σ_b) = 0.73, μ95 = 4.35
- stock Delphes object efficiencies (no CMS-like reweighting): Z Eq. 1 = 0.76, Z(σ_b) = 0.75, μ95 = 5.48
- conservative: N_eff<10 sources at max(value, 3 w̄), zero-support at 3 w̄: Z Eq. 1 = 0.79, Z(σ_b) = 0.70, μ95 = 4.37
- QCD WH x2 (def. a background): Z Eq. 1 = 0.92, Z(σ_b) = 0.88, μ95 = 3.48
- cut-based selection (no BDT): Z Eq. 1 = 0.58, Z(σ_b) = 0.54, μ95 = 6.41

## 4. Checks performed
SHA256 of all 2900 package files vs SHA256SUMS (0 bad); Σw/N per sample vs SAMPLES.csv; BR ledger asserted in code; N_MC ≥ max(50k, σ·BR·3000 fb⁻¹) enforced (`whana.nmc_check`, fails loudly; D-WH-2 effective-N for the weighted W+jets and tt̄jj two-fake rows, N_eff in the SR 7659 / 165); peak/resolution from Delphes; three closure tests (j→γ, j→ℓ, e→γ); BDT k-fold with held-out scoring and a pre-declared adoption rule; JES variation with BDT rescoring (exact closure at zero shift); quadratic coupling closure on independent samples; fit vs counting consistency (Z 0.90 vs 0.91 at 500 fb⁻¹, def. a).

## 5. Decisions (D-WH-n; G1 defaults accepted by the human 2026-11-14, later ones taken as this run's declared defaults per A2)
| ID | decision | taken |
|---|---|---|
| D-WH-1 | signal jets 4F (no b in j; 5F would include resonant tHq) | G1 default (human: accepted) |
| D-WH-2 | WH fake-weighted rows follow the HH effective-N policy (truth/fake weighting; N_eff ≥ 10 in SR or UL + conservative variant) | G1 default (accepted) |
| D-WH-3 | frozen ZH rows below N_req: accept with MC-stat nuisance; split rows checked as one SAMPLES.csv row (EW Zγγjj 3×20k = 60k ≥ 50k) | G1 default (accepted) |
| D-WH-4 | CMS-like object efficiencies (ZH final table) as nominal; stock Delphes as robustness | G1 default (accepted) |
| D-WH-5 | missing `H_ggF_jj` row → own HEFT sample `H_ggF_jj_nomjj` (no m_jj cut, 59 945 events ≥ 50k), FL weighting, 100 % PS-modelling | A2 default |
| D-WH-6 | fake/mis-ID rates: G1-declared scenarios are nominal (j→γ 10⁻³(pT/50)^−0.5 ×2 endcap ×{0.3,1,3}; e→γ {1,2,5} %; j→ℓ {3·10⁻⁵, 2·10⁻⁴, 10⁻³}); FORMAT-6a/6b Delphes rates only for closure and as variants | A2 default |
| D-WH-7 | non-prompt ℓ nominal = max(parametrised, Delphes direct) | A2 default (02 §5 option) |
| D-WH-8 | W→τν feed-down in the background for (a) and (b); scales with the couplings | A2 default (01 §5) |
| D-WH-9 | coupling interpretation rate-only with BR(H→γγ) fixed to SM; QCD WH ∝ κ_W² | A2 default |
| D-WH-10 | `Q_aajj`, `H_QCD_WHjj_fixed`, frozen `B_QCD_zaajj_vbs` are cross-checks only (SAMPLES.csv roles) | A2 default |
| D-WH-11 | own EW W⁻γγjj validation gridpack (failed twice, deterministic survey-channel error) not retried; canonical `B_EW_Waajj_nomjj` covers W± | A2 default |
| D-WH-12 | ZH-style estimation hierarchy (L0 direct / L1 m_γγ shape / L2 VBS-factorised 100 % / zero-support 1.14 w̄, UL 3 w̄) | A2 default |
| D-WH-13 | e→γ closure factor C = direct/weighted (relaxed region) applied when ≥ 10 raw direct events | A2 default |
| D-WH-14 | jet-modelling nuisance = MLM vs fixed-order QCD WH selection-efficiency ratio (backgrounds); signal PS 10 % (assumption) | A2 default |
| D-WH-15 | BDT adopted by the declared rule (gain > 10 % and positive in every fold, AUC gap < 0.02); cut-based shown alongside | A2 rule |

## 6. Reproducibility (08-equivalent)
Run commit: see `git log -- p2/runs/single_r1/wh/reports/FINAL_report.md`. Commands (from `p2/runs/single_r1/wh`, after `source ../../../lib/scripts/setup_stack.sh; export PYTHONPATH=$PWD/scripts/p05:$PYTHONPATH`):
1. own sample: `python3 -P scripts/make_cards.py; python3 -P scripts/make_submit.py 42 _p05`; `condor_submit scripts/condor/p03_gridpacks_p05.sub`, `p03_test_p05.sub`, `p05_prod_ggF.sub` (EosSubmit).
2. ntuples: `python3 -P scripts/p05/make_nt_jobs.py; condor_submit scripts/condor/p05_nt.sub` (+ `p05_nt_H_ggF_jj_nomjj.list`, run with `scripts/condor/p05_nt_job.sh <list> <line>`).
3. `python3 -P scripts/p05/p05_run.py && python3 -P scripts/p05/p05_bdt.py && python3 -P scripts/p05/p07_stats.py && python3 -P scripts/p05/make_figs.py && python3 -P scripts/p05/make_reports.py && python3 -P scripts/p05/make_final.py`.
Seeds: own MC 2442000–2442031 (SPEC_G0 §3.4, R = 4); ntuple x-draws 90000 + job index; BDT folds random_state 2400000 + fold. Stack: LCG_110 (MG5 3.6.3, Pythia 8.317, Delphes 3.5.1), xgboost 2.1.3, scikit-learn 1.9.0, uproot 5.7.1.

## 7. Caveats (main)
LO generators throughout; no pile-up; fake/mis-ID rates are scenarios; e→γ closure factor 4 for the loose QCD ℓℓγjj sample; the BDT stability is marginal (first run failed one fold before a bug fix); the jet-modelling nuisance is statistics-limited and the largest b uncertainty; signal PS uncertainty assumed; the asymptotic fit is approximate at O(1–10) events and the exact-Poisson μ95 is discrete; the coupling result ignores the κ-dependence of BR(H→γγ); no VH combination in this run.

## 8. Token / time (this run, from its own transcript)
Computed by `wh/scripts/my_usage.py` from this session's transcript (deduplicated by message id; prices `p2/metrics/prices.json`; cost-equivalent, not billed cost). Segments from the ledger times. Computed shortly before the final commit; the last few calls are not included.

| segment | model | API calls | input | output | cache write | cache read | cost-eq. USD | first → last call (UTC) |
|---|---|---|---|---|---|---|---|---|
| setup / G0 (before P01) | claude-opus-5-5 | 11 | 22 | 6,007 | 89,445 | 591,961 | 0.95 | 20:32:18 → 10:33:50 |
| P01–P03 → G1 | <synthetic> | 1 | 0 | 0 | 0 | 0 | 0.00 | 13:56:17 → 13:56:17 |
| P01–P03 → G1 | claude-opus-5-5 | 116 | 236 | 170,813 | 921,174 | 27,181,826 | 16.22 | 10:34:08 → 18:13:58 |
| idle at G1 (stale notifications) | claude-opus-5-5 | 2 | 6 | 2,829 | 1,375 | 738,354 | 0.22 | 18:14:18 → 18:32:03 |
| P05–P07 → FINAL (A2) | claude-opus-5-5 | 115 | 232 | 213,487 | 417,476 | 28,994,991 | 13.41 | 09:48:40 → 10:56:01 |
| **total** | | | | | | | **30.80** | |
wall (first→last transcript record): 134.40 h; active (gaps capped at 5 min): 2.77 h

transcript records with usage (dedup): 245; sidechain records: 0; first/last timestamp: 2026-11-08T20:32:16.044Z / 2026-11-14T10:56:03.478Z

