# WH Phase 02 — background matrix and overlap ledger

- **Date (UTC):** 2026-11-09. **Run:** `single_r2`.
- **Status: PASS as a design ledger, with three open quantitative items.** All items are raised as decisions; none was relaxed silently.
  1. The prompt Wγγjj continuum cross sections were still integrating on HTCondor (cluster 899738, procs 0–2; > 3.5 h on 8 cores).
  2. Several backgrounds are comparable to the signal and need dedicated production statistics, which go to G2 (D-WH-5, D-WH-6).
  3. The on-shell-W Wγγ treatment misses about half of the prompt rate (D-WH-4).
- **Inputs:** cards `wh/cards/phase02/*.mg5`; registry `wh/config/samples.yaml`; σ/BR ledger `wh/config/xsec_br_ledger.json` (`scripts/xsec_br_ledger.py`); estimates in `wh/work/validation/*.json`. Seeds per SPEC_G0 §3.4 (J = 0 integration, J = 10 local pilots).
- **Not final yields:** the relevance column uses an *illustrative, non-optimised* Delphes selection. That selection is identical for every row:
  - ≥ 2 photons with p_T > 20 GeV, |η| < 2.5 outside the barrel–endcap crack;
  - exactly 1 lepton (p_T > 15 GeV), with leading p_T > 25 GeV;
  - MET > 30 GeV, ≥ 2 jets, b-veto;
  - m_jj > 500 GeV and |Δη_jj| > 2.5;
  - 120 < m_γγ < 130 GeV.

  On this selection the signal is **s ≈ 1.02 ± 0.12 events at 500 fb⁻¹** (03 §4, 1000 events; definition (a)). These numbers only rank the backgrounds and decide what Phase 04 must produce.

## 1. Final state and measurement definition
- **Reconstructed target:** one isolated e/μ, MET, ≥ 2 isolated photons with m_γγ in a Higgs window, two VBS tag jets, and a b-veto. m_γγ sidebands are reserved and the window is never optimised on the signal region (Phase 06).
- **Signal:** EW (0,4) W±Hjj, 4F (01; D-WH-1).
- **Categories:**
  - *resonant backgrounds:* anything with H → γγ that is not the signal; they peak with the signal shape;
  - *continuum backgrounds:* smooth in m_γγ, constrained by the sidebands;
  - *reducible backgrounds:* fake photons or fake/non-prompt leptons, quoted per scenario and never labelled data-driven.

## 2. Ledger (σ at the generator cuts of each card, LO, MG5 integration error; k = BR ledger factor; ev₅₀₀ = σ·k·500 fb⁻¹ before any cut)
| ID | role | MG5 process / order | gen cuts | σ [fb] | k | ev₅₀₀ pre-cut | overlap rule | relevance after illustrative selection (500 fb⁻¹) |
|---|---|---|---|---|---|---|---|---|
| S_EW_WHjj | signal | `w± h j j` (0,4), 4F, W→eν/μν chain | p_T(j) > 20 GeV | 13.76 ± 0.03 | WF·BGG | 15.3 | order-exclusive vs QCD | **1.02 ± 0.12** |
| H_QCD_WHjj | resonant (def. a) | `w± h j j` (2,2), 4F | same | 58.83 ± 0.15 | WF·BGG | 65.5 | order-exclusive; I term separate | **0.46 ± 0.17** (7 raw) |
| I_WHjj | signed | `QCD^2==2 QED^2==6`, undecayed | same | −0.256 ± 0.013 (undecayed) | — | — | never as positive events | −0.4 % of EW (loose cuts) |
| H_EW_WHjj_tau | resonant | as signal, W→τν, τ in PY8 | same | 6.814 ± 0.049 | WF·BGG | 7.6 | distinct W decay | Phase 04 (≲ 0.1 expected: τ→ℓ BR 0.35 and a softer lepton) |
| H_tHq | resonant | `t h j` (0,3) 5F, t→bℓν | none | 15.40 ± 0.14 | TF·WF·BGG | 17.0 | **same external states as 5F W±Hjj**: never combined with a 5F signal | Phase 04; b-veto discriminant |
| H_tHW | resonant | `g b > t w- h $$ t~` (DR), 1ℓ | none | 2.335 ± 0.015 | TF·WF·HF·BGG | 2.6 | DR; DS as systematic | Phase 04 |
| H_ttH_1l / _2l | resonant | `t t~ h` 1ℓ / 2ℓ chains | none | 108.2 ± 0.3 / 18.02 ± 0.17 | see ledger | 120.7 / 19.4 | external tops | Phase 04; b-veto, VBS |
| R_ZHjj_lostlep | resonant | **frozen ZH** S_EW_ZHjj + H_QCD_ZHjj (v1) | no lepton generator cuts (`cut_decays=False`), so **coverage is complete** | ZH ledger | ZF·BGG | — | distinct process (Z) | EW **0.0287 ± 0.0007**, QCD **0.0252 ± 0.0019** (80k events each) |
| H_ggZH_lostlep | resonant | frozen ZH H_ggZH_py8dec | Z decayed in PY8 | ZH ledger | BR_ZLL·BGG | — | distinct | Phase 04 (no WH-selection support yet; in ZH its σ×BR was 0.5× that of QCD ZHjj before cuts) |
| B_EW_Waajj | continuum | `w± a a j j` (0,5), on-shell W chain, 4F, VBS-biased (m_jj > 400) | p_T(γ) > 25 GeV, 100 < m_γγ < 170 GeV | **pending** (899738.0) | WF | — | ≥ 2 prompt γ region | — |
| B_QCD_Waajj (+ _vbs twin) | continuum | (2,3), no generator m_jj cut (+ twin with m_jj > 400) | same | **pending** (899738.1/2) | WF | — | ≥ 2 prompt γ | — |
| R_Zaajj_lostlep | continuum | **frozen ZH** B_QCD_zaajj_vbs, B_EW_zaajj_vbs_is1–3 | `cut_decays=False`, so leptons are uncut; p_T(γ) > 25, m_jj > 400, 100 < m_γγ < 170 GeV | ZH ledger | ZF·1.128 | — | distinct process | QCD **0.038 ± 0.003** (×C = 2.37 generator-m_jj correction → 0.089); EW is2 0.058 ± 0.005 (is1–3 together ≈ 0.14, scaled by σ) |
| F_QCD_Wajj (+ _nomjj twin) | 1 fake γ | `l ν a j j` (2,3), full off-shell | p_T(γ) > 25, ℓ p_T > 10, m_jj > 400 (twin: none) | 687.5 ± 1.2 (twin: 6308 ± 8) | WF | 3.4 × 10⁵ | **keep N_prompt γ = 1** | Phase 04, direct Delphes. Test job submitted (899823.1) |
| F_EW_Wajj | 1 fake γ | (0,5) | as F_QCD | 82.11 ± 0.15 | WF | 4.0 × 10⁴ | N_prompt γ = 1 | Phase 04 |
| F_Wjj | 2 fake γ | `l ν j j` (2,2), m_jj > 400 | ℓ p_T > 10 | 1.710 × 10⁵ ± 1.0 × 10³ (pilot normalised to the PY8 value 1.708 × 10⁵) | WF | 8.4 × 10⁷ | **keep N_prompt γ = 0** | **0.31** (N_eff 2.4; band 0.03–2.8 for f × {0.3, 1, 3}); VBS region 17.1 (N_eff 27) — **lower bound** (2 ME partons) |
| T_tta_1l / _2l | top + 1 prompt γ | `t t~ a` chains | p_T(γ) > 15 GeV | 514.6 ± 3.2 / 84.53 ± 0.88 | TF²·WF·HF / TF²·WF² | 2.5 × 10⁵ / 4.0 × 10⁴ | **not** overlap-removed against tt̄γγ (ZH A9 lesson: conservative, follows the reference) | Phase 04; b-veto + VBS |
| T_ttaa_1l | top + 2 prompt γ | `t t~ a a` 1ℓ | p_T(γ) > 20, 90 < m_γγ < 190 GeV | 0.4685 ± 0.0032 | TF²·WF·HF | 230 | double counting with tt̄γ bounded by its full yield | Phase 04 |
| T_tWa_1l | top + 1 prompt γ | `t w a $$ t~` (DR), 1ℓ | p_T(γ) > 15 GeV | 78.31 ± 0.52 | TF·WF·HF | 3.9 × 10⁴ | DR (DS as systematic) | Phase 04 |
| F_aajj | non-prompt ℓ | `a a j j` (2,2), m_jj > 400 | p_T(γ) > 25, 100 < m_γγ < 170 GeV | 279.5 ± 1.3 | 1 (× f_ℓ) | — | no prompt lepton | **0.14** at f_ℓ = 10⁻⁴ (band **0.04–1.4** for f_ℓ = 3·10⁻⁵–10⁻³); 6 raw events, lower bound |
| V_e→γ (Zγjj) | e→γ fake | **frozen ZH** F_QCD/EW_llajj_vbs (direct Delphes) | ZH | 69.46 (×C 2.05) / 11.05 | 1 (× f_e) | — | the ZH event is the source; the photon is the misidentified electron | f_e = 2 %: 0.30 + 0.19 events without a Z-veto; **0.12 + 0.02 with \|m(ℓ,γ) − m_Z\| > 10 GeV** (band 0.07–0.36 for f_e = 1–5 %) |
| ggF/VBF H + fake ℓ | resonant | — | — | — | — | — | — | bound in Phase 04 via the f_ℓ scenario. VBF H has the signal-like jets, so it is not dismissed |

### Raw MC support of the frozen-ZH and pilot estimates
- **Frozen-ZH rows:** files `production/v1/*` and `production/final/*`, read only. Script: `scripts/lostlep_frozen_zh.py` → `work/validation/lostlep_frozen_zh.json` (raw counts at each cut). The off-shell factor 1.128 for Zγγ comes from the ZH ledger.
- **Pilot rows:**
  - `scripts/fakefactor_pilot_wh.py` (patch 004) → `work/validation/fakefactor_F_Wjj.json`
  - `scripts/fakelep_bound.py` → `work/validation/fakelep_bound_F_aajj.json`
  - `scripts/efake_frozen_zh.py` → `work/validation/efake_frozen_zh.json`
- **Inputs to the pilots:**
  - F_Wjj and F_aajj: 1000 events each, through the local PY8 + Delphes slim_v1 chain, seeds 2514010 / 2525010.
  - Fake model: f(j→γ) = 10⁻³ (p_T/50)^−0.5, ×2 in the endcap, with p_T(γ) = x·p_T(j) and x ~ N(0.85, 0.10). These are the ZH 02 §4 scenarios, not data-driven.
- **No zero is used as negligible:** rows marked "Phase 04" have no Delphes support yet. They are not zero.

## 3. Findings that change the background model (vs ZH)
1. **Off-shell/FSR of the prompt continuum is a factor of ~2, not ~1.13.**
   - The 0-jet proxy pair `Q_W_aa_0j_offshell` (ℓνγγ, full (0,4)) vs `Q_W_aa_0j_onshell` (W(→ℓν)γγ chain) has the same photon cuts. The on-shell LHE gets the same lepton cuts (p_T > 10, |η| < 2.5, ΔR(ℓ,γ) > 0.4).
   - Result: **R = 2.49 / (1.751 × 0.708) = 2.01 ± 0.05** (`work/validation/offshell_fsr_ratio_0j.json`).
   - Reason: photons radiated in the W decay (radiative W → ℓνγ) cannot be removed by a mass window, because m_ℓν is not reconstructible. ZH had the m_ℓℓ window instead.
   - Consequence: on-shell-W Wγγjj samples alone (the ZH-final strategy) would **underestimate the continuum by about 50 %**. → **D-WH-4.**
2. **W+jets with two fake photons, the γγ+jets non-prompt lepton, and e→γ from Zγjj are each O(10–30 %) of the signal or more** under nominal scenarios (§2).
   - All three rest on lower-bound pilots (fixed-order 2 partons) or parametrised rates.
   - Their scenario bands reach or exceed the signal. They are mandatory in Phase 04 and cannot be dropped.
3. **ZHjj with a lost lepton:** 0.054 events, i.e. 5 % of the signal. Small but kept, from the frozen samples. Their generation covers lost leptons fully, since no lepton cuts were active.
4. **Zγγjj with a lost lepton:** ≈ 0.09 (QCD, C-corrected) + ≈ 0.14 (EW) events. This is comparable to the expected Wγγ continuum scale. It is reused from frozen ZH, with full lepton coverage; the photon (p_T > 25 GeV), m_jj (> 400 GeV) and m_γγ (100–170 GeV) generator cuts constrain the WH selection to stay inside them.
5. **tHq ≈ 5F excess:** the undecayed tHq rate implied by 15.40 fb is ≈ 15.40/(0.2223 × 1.0026) ≈ 69 fb. This matches the 5F − 4F W±Hjj difference (64.5 ± 1.5 fb) within the cuts difference.
   - This confirms that the b-containing part of 5F W±Hjj is essentially tHq. Hence the 4F signal + tHq background (D-WH-1).
   - The `$$ t t~` diagnostic gives σ = 144.6 fb, *larger* than the full 5F 126.9 fb. Removing the s-channel top breaks gauge cancellations, so that number is **not interpretable**. It is shown only as a demonstration of why diagram removal is unsafe.

## 4. Overlap-removal contract (as ZH 02 §3, adapted)
1. **Prompt photons:** defined once at particle level by `lib/scripts/slim_gentruth.py`, unchanged (prompt = no hadron ancestor; p_T > 15 GeV, |η| < 2.5, ΔR > 0.4 to prompt leptons, other photons and GenJets).
   - W+jets keeps N_pγ = 0, Wγ+jets keeps N_pγ = 1, Wγγ+jets keeps N_pγ ≥ 2.
   - The same rule applies to the frozen Z samples that enter as lost-lepton backgrounds.
   - Top samples are **not** photon-count overlap-removed (ZH A9 finding: the second photon often comes from the top decays, which the tt̄γγ ME lacks). This is conservative.
2. **QED shower ON** everywhere (common CP5 card).
3. **Stitching validation (Phase 04):** continuity of p_T(γ) and ΔR(γ,ℓ) at the 15 GeV / 0.4 boundaries, and threshold variation 15 → 20 GeV.
4. **EW vs QCD:** separated by coupling order. Interference is carried as signed separate terms.
5. **Resonant vs continuum:** there is no tree Hγγ vertex, so H-pole/continuum interference is absent. Quoted as a caveat.
6. **Lost-lepton Z samples vs W samples:** there is no double counting, since the external bosons are distinct. A Z → ℓℓ event with one lepton out of acceptance is not in any W sample.

## 5. Generator-level cut safety (twins, as ZH A1)
- **EW-type samples:** m_jj > 400 GeV at generator level. ZH measured the loss in the reco VBS region to be 1.4 %; it is re-measured for W in Phase 04 with the signal (generated without an m_jj cut).
- **QCD-type samples:** either generated without the m_jj cut (`B_QCD_Waajj`), or VBS-biased with a no-m_jj twin (`F_QCD_Wajj` + `F_QCD_Wajj_nomjj`; `B_QCD_Waajj_vbs` + `B_QCD_Waajj`).
  - C = Y(twin)/Y(biased) is measured at Delphes level, with its MC-stat uncertainty as a nuisance.
  - The no-m_jj twin of Wγjj needs 1.85 × 10⁷ events to satisfy N ≥ σ×BR×3000 itself. As in ZH, it is used **only as an auxiliary ratio sample**, flagged and not exempted silently (D-WH-5).
- **Photon generator cut p_T > 25 GeV:** safe if the reco selection uses p_T(γ₂) ≥ m_γγ/4 ≈ 30 GeV (resolution ~2 %). This constrains Phase 05; using 20 GeV (reference) would need p_T > 15 GeV samples.

## 6. MC-statistics needs (N ≥ max(50k, σ·k·3000 fb⁻¹), from the ledger)
| sample | σ·k [fb] | required N_MC | feasibility |
|---|---|---|---|
| S_EW_WHjj, H_QCD_WHjj, H_tHq, H_tHW, H_ttH_1l/2l, H_EW_WHjj_tau, T_ttaa_1l | ≤ 0.46 | 50 000 each | easy |
| T_tta_2l / T_tWa_1l / F_EW_Wajj | 80 / 77 / 80 | 2.4 × 10⁵ / 2.3 × 10⁵ / 2.4 × 10⁵ | ok |
| T_tta_1l | 506 | 1.5 × 10⁶ | ok (ZH did 1 M) |
| F_QCD_Wajj (m_jj > 400) | 672 | 2.0 × 10⁶ | ok (ZH did 6 M) |
| F_QCD_Wajj_nomjj (twin) | 6164 | 1.85 × 10⁷ | auxiliary ratio only → D-WH-5 |
| F_aajj | 280 (× f_ℓ) | 8.4 × 10⁵ | ok |
| F_Wjj | 1.67 × 10⁵ | **5.0 × 10⁸** | **infeasible**: needs fake-factor weighting (every event weighted, no fake cut) with an N_eff ≥ 10 rule, analogous to the HH effective-N policy → **D-WH-6** |
| B_*_Waajj | pending | pending | — |

## 7. Checks
- Every card parsed and integrated with rc = 0; process lists are in `work/gp_condor/<sample>_s<seed>_processes.txt` and diagram totals in the ledger.
- W→τν / W→(e+μ)ν σ ratio = 6.814/13.76 = 0.495 (expected 0.5).
- tt̄γ 2ℓ/1ℓ = 0.164. Expected (B_ℓ²)/(2 B_ℓ B_had) with MG5 BRs: 0.2223²/(2 × 0.2223 × 0.6668) = 0.167. Agreement ✓.
- BR ledger assertions passed.

## 8. Caveats
- LO.
- The pilots are fixed-order 2-parton samples with 1000 events: they are lower bounds with large MC errors (PEAK N_eff 2.4 for W+jets).
- Fake and non-prompt rates are scenarios, not measurements.
- Frozen-ZH estimates use 40–80 % of the files.
- The m_γγ window is illustrative.

## 9. Decisions raised
- **D-WH-4** (prompt continuum off-shell): default = generate the Wγγjj continuum as **full off-shell ℓνγγjj** for EW and QCD (cost to be measured on batch, possibly with beam-class splits as in ZH). Fallback = the on-shell chain × an R factor measured at Delphes level in the signal region with 0j/1j proxies, ±50 % of (R − 1) as a nuisance.
- **D-WH-5** (QCD-type twin statistics): accept the no-m_jj twins as auxiliary ratio samples below σ·k·3000, with the MC-stat of C as a nuisance [default], vs generating them at full N (1.85 × 10⁷ events for Wγjj).
- **D-WH-6** (W+jets double fake): an N_MC ≥ σ·k·3000 = 5 × 10⁸ requirement is infeasible. Default = a merged W+jets (0–4j MLM) sample with fake-factor weighting of every event and the requirement N_eff ≥ 10 in the final SR, else a direct upper bound and a conservative robustness variant. This is a **deviation from SPEC_G0 §1.5** and needs human approval.

## 10. Next actions
Collect the B_*_Waajj σ (cluster 899738). Then Phase 04 production planning at G2: merged W+jets / Wγ+jets, the off-shell Wγγ cost test, and Delphes-level C factors.

Git commit: see `reports/INDEX.md`.
