# WH Phase 01-03 reports, analysis C


<!-- ===== Phase report 01_signal_definition ===== -->

# WH Phase 01 — signal definition (EW W±Hjj, W→eν/μν, H→γγ), RUN

- **Date UTC:** 2026-11-08 20:20 → 2026-11-09 00:10 (incl. a usage-limit interruption ~20:45–23:59).
- **Status: PASS with decisions open (D-WH-1 flavour scheme, D-WH-2 W normalisation convention).** The numbers below hold under the recommended defaults. No number here is a yield. All are generator- or validation-level and are labelled as such.
- **Git:** base commit `e681d9b`; this run's files are **uncommitted** (no commit without a human instruction, see D-WH-9).
- **Inputs/versions:** stack `LCG_110/x86_64-el9-gcc13-opt + MG5_aMC_v3.6.3 (upstream)`, sourced from `p2/lib/scripts/setup_stack.sh`; Pythia 8.317 with CP5; Delphes 3.5.1 with the slim CMS card from `p2/lib`; NNPDF31_nnlo_as_0118 (LHAID 303600); model `sm-no_b_mass`; dynamical scale choice 3 (HT/2), as in ZH.
- **Seeds:** SPEC_G0 §3.4 with P=2, R=x: `seed = 2x00000 + 1000·idx + J`, from the registry `wh/config/samples.yaml`. J=0 for interactive runs, J=900 for gridpack builds, J≥1 for condor jobs. Uniqueness is asserted by `wh/scripts/seeds.py`, plus a check over all 58 planned seeds.

## 1. Goal
Define the gauge-invariant EW W±Hjj signal and its order bookkeeping, the QCD W±Hjj component (definitions a/b) and the interference. Fix the W branching-ratio ledger (WF) and the H→γγ treatment, and validate each by executed diagram, cross-section and closure checks.

## 2. Definition
- **Signal:** the complete tree amplitude at amplitude order (QCD, QED) = (0, 4) for pp → W± H j j. All diagrams are summed coherently, including VBF/VBS-like, Higgsstrahlung-like (W V H with V→qq̄) and crossed or identical-quark terms, with both charges.
  - External partons j, p ∈ {g, u, d, s, c} and their antiquarks, with a 5-flavour PDF.
  - **No external b (D-WH-1).**
  - W→eν/μν is done in an MG5 decay chain (spin correlations kept). H→γγ is forced in Pythia8.
- **Model content (executed check):** `sm-no_b_mass` has MC = MB = 0, ymc = ymb = 0 and diagonal CKM (`restrict_no_b_mass.dat`). In the no-b set, every Higgs coupling is therefore HWW or HZZ: there are no Yukawa or top lines. This is what makes the sample a λWZ = κW/κZ probe.
- **VBF-like is a region of the full amplitude, not a diagram subset.** No diagram is removed. Observable-bin fractions at parton level (LHE, 1000 events, `work/m5/lhe_kin_phase01.json`): 62 % have m_jj > 500 GeV and |Δη| > 2.5, while 20 % have 60 < m_jj < 110 GeV (the V→jj region where Higgsstrahlung-like diagrams dominate). The corresponding QCD fraction in the VBF-like region is 4.5 %.

| Component | MG5 syntax (cards `wh/cards/smoke/`) | Diagrams | σ (LO, gen. cuts) |
|---|---|---|---|
| EW W±Hjj, undecayed, no-b | `p p > w+ h j j QCD=0 QED=4` + w− | 80 proc. / 1456 | **61.87 ± 0.44 fb** |
| EW W±Hjj, undecayed, 5F (b in p, j) | same with b | 104 / 1792 | 127.1 ± 1.4 fb |
| b-complement (≥1 external b), undecayed | `bq j5 > …`, `q4 bq > …`, `q4 q4 > w h bq j5` (6 lines) | 40 / 560 | 65.98 ± 0.51 fb |
| **Signal production**, W→ℓν chain (ℓ=e,μ) | `p p > w+ h j j QCD=0 QED=4, w+ > l+ vl` + w− | 2 groups / 1460 | 13.62 ± 0.09 fb (interactive); **13.79 ± 0.03 fb** (gridpack build, seed 2x03900) |
| W+ only: undecayed / chain | | 40/728, 1/730 | 38.56 ± 0.58 / 8.359 ± 0.085 fb |
| QCD W±Hjj (2,2), undecayed, no-b / 5F | `QCD=2 QED=2` | 96/352, 120/400 | 263.6 ± 1.6 / 263.9 ± 1.4 fb |
| QCD W±Hjj, W→ℓν chain (def. a background) | | 2 / 356 | 58.26 ± 0.33 fb; 58.6 ± 0.19 fb (gridpack) |
| EW×QCD interference, undecayed, no-b | `QCD^2==2 QED^2==6` | 80 / 1680 | **−0.238 ± 0.012 fb** |
| EW (0,5) ℓνHjj, no chain, default lepton cuts | `p p > l+ vl h j j QCD=0 QED=5` | 160 / 4032 | 11.33 ± 0.12 fb (lepton acceptance applied; not like-for-like) |
| same, lepton cuts removed (`ptl 0, etal −1, drjl 0`) | | | **13.61 ± 0.11 fb** |
| EW W±Hjj, W→τν (background, τ in PY8) | chain `w+ > ta+ vt` | 2 / 1458 | 6.81 ± 0.04 fb |

Generator cuts for all of the above: pT(j) > 20 GeV, |η(j)| < 5, ΔR(jj) > 0.4, `cut_decays False`. Evidence: `wh/work/m5/<card>/{mg5.log,status.txt,subproc.mg,diagrams.txt}`.

- **QED=4 vs QED==4.** For a (0,4) process, `QED=4` (upper bound) with `QCD=0` selects the minimal order. The diagram counts and the decomposition closure below confirm that no extra orders entered.

## 3. Findings and decisions
- **D-WH-1, external-b flavour scheme (physics decision).**
  - The 5F (0,4) set contains resonant **tHq with t→Wb**. 54 % of 5F events have an external b, and 93 % of those have m(W,b) within 15 GeV of m_t (`lhe_kin_phase01.json`).
  - The b-component (65.98 fb) is larger than the no-b signal itself, and it involves the top Yukawa, so it is not a pure HVV probe.
  - **Partition closure:** σ(no-b) + σ(b-complement) = 127.85 ± 0.67 fb against σ(5F) = 127.1 ± 1.4 fb, a pull of +0.5. The partition by external flavour is exhaustive and has no double counting.
  - **Recommended:** signal = no-b set. The b-complement (W→ℓν, 14.54 ± 0.07 fb) becomes a resonant background (`H_EW_WHjj_bcomp_lv`) that contains tHq and is suppressed by the b-veto (Phase 02).
  - **Alternative:** a 5F signal, which would mix the κt dependence into the λWZ interpretation.
  - In QCD (2,2) the b-component is negligible: 1.1 % of 5F events, and σ(5F) − σ(no-b) = 0.3 ± 2.1 fb.
- **Definition (a)/(b).** In (a), QCD W±Hjj is a resonant background fitted with the signal shape. In (b), signal = EW + QCD + I.
- **Interference.** σ_I/σ_EW = −0.38 ± 0.02 % inclusive. In the parton-level VBS region (m_jj > 500, |Δη| > 2.5) it is −0.11 ± 0.07 % (signed LHE weights, `I_WHjj_nodecay_nob/vbs_fraction.txt`). It is negligible relative to every other uncertainty and is quoted, not added. The signed sample is σ-only and is never used as positive events.
- **Negative weights.** 11 of 2000 signal LHE events (0.55 %) carry negative weights, presumably from negative NNPDF3.1 NNLO PDF values at large x. ZH reported none for its samples. All yields must use signed weights, Σw and Σw², as `wh_baseline.py` already does.

## 4. Branching ratios and the normalisation ledger
- **B(H→γγ) = 0.002270** (LHCHWG YR4, m_H = 125 GeV, as ZH). It is applied **once**, externally. Pythia forces H→γγ with conditional BR 1.
  - Generator closure: 2000/2000 last-copy H→γγ in the signal smoke run, the signal test job and the QCD test job.
  - Pythia σ equals LHE σ (13.56 vs 13.62 fb interactive; 13.89 vs 13.79 fb in the test job), so Pythia does not fold in BR(γγ).
- **W factor WF.** The MG5 model inputs (aEWM1 = 132.507, G_F, M_Z, giving M_W = 80.419 GeV and s_W² = 0.22225) give tree Γ(W→ℓν) = 227.56 MeV. The param-card Γ_W is 2.0476 GeV; the tree sum over 3ℓ + 6q is 2.0481 GeV. Hence B_MG(ℓν) = 0.11114 per flavour.
  - PDG 2025 (`wh/sources/pdg_w/`, sha256 `4e23549b…`): B(eν) = 10.71 ± 0.16 %, B(μν) = 10.63 ± 0.15 %, B(τν) = 11.38 ± 0.21 %, B(had) = 67.41 ± 0.27 %.
  - **WF = 0.2134/0.22227 = 0.9601.** Also WF_τ = 1.0240, WF3 (e,μ,τ) = 0.9814, WF_had = 1.0109, and WF² = 0.9217 for dileptonic W pairs.
  - The lepton-universality alternative (2 × 10.86 %) gives 0.9772 (+1.8 %), carried as a systematic.
- **Closure tests (executed).**

  | Test | Measured | Expectation | Verdict |
  |---|---|---|---|
  | σ(W±Hjj chain)/σ(undecayed) | 0.2201 ± 0.0021 | 2·B_MG = 0.22227 | −1.0σ |
  | W+ only | 0.2168 ± 0.0040 | 0.22227 | −1.4σ |
  | High-statistics W±H, 0 jets (bwcutoff 15) | **0.21606 ± 0.00028** = 0.9721·2B_MG | BW fraction (2/π)atan(30) = 0.9788 | resolved |
  | same, bwcutoff 50 | 0.21865 ± 0.00030 = 0.9837·2B_MG | (2/π)atan(100) = 0.9936 | resolved |
  | Off-shell ℓνHjj (no chain, no lepton cuts) / on-shell chain | **1.000 ± 0.010** | 1 | PASS |

  The chain therefore does not equal σ_prod × B_MG exactly: Breit-Wigner truncation and off-shell production cost about 2.8 % at 0 jets. However, the full off-shell (0,5) calculation agrees with the chain to 1 % at the Hjj level.
- **D-WH-2, recommended convention:** normalise the chain σ by WF only, as ZH did with ZF. This is equivalent to the off-shell calculation rescaled to the PDG BR within 1 %. Add a ±1 % W-lineshape normalisation uncertainty (the precision of the test) and the +1.8 % universality alternative. The off-shell (0,5) sample is a systematic cross-check and is never added to the signal.
- **Ledger code:** `wh/scripts/ledger.py` (patch 003 of lib `final_analysis.py`).
  - It asserts that each decay factor appears at most once per sample, including the W factors.
  - `nmc_check` enforces N ≥ **max(50k, σ×BR×3000 fb⁻¹)**. The lib version lacked the 50k floor.
  - Self-tests pass (`python3 -P wh/scripts/ledger.py`).
- **Signal physics normalisation, before any acceptance:** σ×WF×B_γγ = 13.79 × 0.9601 × 0.002270 = **0.0301 fb**, i.e. 15.0 events at 500 fb⁻¹ (ZH: 1.44).
- **Observation for the frozen ZH study (reported, not modified):** the ZH ledger applies B_γγ only to samples whose top-decay W's were decayed in MG5 (tt̄H, tt̄γ, tWγ, tt̄γγ). The PDG/MG5 rescale WF² = 0.9217 is missing there, so those ZH backgrounds are high by about 8.5 %. Impact on the ZH result is expected to be small, since these backgrounds are minor.

## 5. Checks
- Diagram counts and subprocess lists were saved for every card.
- σ decomposition closure: no-b + b-complement = 5F (pull 0.5).
- W BR closure (above) and H→γγ closure (2000/2000).
- Pythia σ = LHE σ.
- Seed uniqueness was asserted.
- Charge split: W+ = 62 % of W± undecayed (38.56/61.87).

## 6. Caveats
- LO only, with no K-factors. Theory uncertainties (7-point scale ⊕ PDF from the `use_syst` weights) are stored but not yet evaluated (Phase 04/05).
- The τ-mass effect on B_MG(τν), about 10⁻³, is neglected.
- No heavy-quark Yukawa or CKM-mixing study was done beyond the b partition.
- The interference was evaluated at parton level only; it will be re-checked after selection if the selection changes the region.

## 7. Next actions
Phase 02 ledger (done, report 02) and Phase 03 validation (report 03). Human: answer D-WH-1 and D-WH-2.


<!-- ===== Phase report 02_background_overlap ===== -->

# WH Phase 02 — background matrix and overlap ledger, RUN

- **Date UTC:** 2026-11-08 20:30 → 2026-11-09 00:20.
- **Status: PASS as a ledger with quantitative first estimates; four physics decisions open (D-WH-3 … D-WH-6).**
- **Git:** base commit `e681d9b`, uncommitted.
- **Inputs:** report 01, test-job samples (report 03), frozen ZH samples under `production/{v1,final}` (read-only), the PDG/YR4 inputs of report 01 §4. Seeds as in report 01.
- **Scope note:** every number below is a validation-level estimate at a **pre-declared, non-optimised baseline B0**, computed at 500 fb⁻¹ from 1k–5k-event test jobs or from frozen ZH samples. None of them is a final yield. A zero MC count is never read as a zero background.

## 1. Final state and baseline B0
- **Reco target:** exactly one isolated e/μ, MET, two photons with m_γγ near 125 GeV, two VBS tag jets, and a b-veto.
- **B0** (`wh/scripts/wh_baseline.py`, fixed before any background was examined; evaluated at Delphes level):
  - leptons: e pT > 15, |η| < 2.5; μ pT > 15, |η| < 2.4; veto on a second lepton with pT > 10;
  - photons: ≥ 2 with pT > 20, |η| < 2.5 excluding the crack, ΔR(γ,ℓ) > 0.4; 100 < m_γγ < 180 GeV;
  - jets: ≥ 2 with pT > 25, |η| < 4.7, cleaned against the lepton and photons;
  - MET > 30 GeV; 0 b-tags (|η| < 2.5);
  - VBS: m_jj > 500 GeV, |Δη_jj| > 2.5; window 120 < m_γγ < 130 GeV.
- **Sidebands:** 105–120 and 130–165 GeV are reserved for Phase 06. No cut was tuned here.
- **Signal at B0 (signal test job, 2000 events):** **1.17** events in the window at 500 fb⁻¹ (155 raw), and 1.28 ± 0.10 in the interactive smoke run. Validation only.

## 2. Ledger
Columns: window yield at B0 and 500 fb⁻¹ (raw MC count in brackets) and the method. Machine-readable version: `wh/config/sample_matrix_wh.yaml`.

| ID | Role | Generator / order (card) | BR ledger k | Overlap rule | σ_gen [fb] | B0 window [ev] | Method / note |
|---|---|---|---|---|---|---|---|
| S_EW_WHjj_lv | signal | MG5 (0,4) no-b, W→ℓν chain | WF·B_γγ | order-exclusive vs QCD; flavour-exclusive vs bcomp | 13.79 | **1.17** (155) | direct |
| H_QCD_WHjj_lv | resonant (def. a) / signal (def. b) | (2,2) no-b, W→ℓν chain | WF·B_γγ | — | 58.6 | 0.58 (18) | direct; fixed order, MLM alternative open (D-WH-7) |
| I_WHjj | signed | `QCD^2==2 QED^2==6` | — | separate signed term | −0.238 | −0.11 % of EW (parton VBS) | quoted, not added |
| H_EW_WHjj_bcomp_lv | resonant (tHq-like) | (0,4) with ≥1 external b | WF·B_γγ | flavour partition (report 01) | 14.54 | 0.33 (41) | direct; b-veto keeps 36 %, so the b-veto matters (Phase 05) |
| H_EW_WHjj_taunu | resonant (τ feed-down) | (0,4) W→τν, τ in PY8 | WF_τ·B_γγ | distinct W decay | 6.83 | 0.14 (34) | direct |
| H_ttH_semilep | resonant | tt̄H, one t→bℓν (e,μ,τ) | WF3·WF_had·B_γγ | distinct external tops | 161.8 | 0 (0 of 2000; w_evt 0.09) | **no MC support**. Need production N; upper value 3.0·w_evt = 0.27 |
| ZH:H_ttH (dilep, lost ℓ) | resonant | frozen ZH final | WF²·B_γγ | dilep vs semilep exclusive by decay | 18.09 | 0.031 (65) | direct, reused |
| H_tHW_1l | resonant | tHW (DR), one leptonic W | WF3·WF_had·B_γγ | DR vs tt̄H | 7.04 | 0.012 (3) | direct, low statistics |
| ZH:S_EW_ZHjj (lost ℓ) | resonant | frozen ZH v1, 200k | ZF·B_γγ | Z vs W exclusive by final state | 1.295 | 0.032 (4406) | direct, reused; coverage verified (§4) |
| ZH:H_QCD_ZHjj (lost ℓ) | resonant | frozen ZH v1, 100k | ZF·B_γγ | — | 10.21 | 0.026 (234) | direct, reused |
| ZH:H_ggZH (lost ℓ) | resonant | frozen ZH final | BR_ZLL·B_γγ | — | 75.0 | 0.023 (80) | direct, reused |
| ZH:H_ZH_tautau | resonant | frozen ZH final (MLM) | B_γγ | — | 25.0 | 0.011 (2) | direct, low statistics |
| H_VBFH_nolep | resonant + non-prompt ℓ | (0,3) Hjj | B_γγ | requires 0 reco leptons | 4152 | 0.006 (f_ℓ = 1e-4; ×0.3–10) | parametrised f_ℓ (fl mode) |
| ggF H+jj | resonant + non-prompt ℓ | not generated | — | — | (ranking: ~σ_ggF·B_γγ·10⁻²) | bound pending | heft sample needed (D-WH-6) |
| B_EW_Waajj_wp/wm | continuum | (0,5) Wγγjj, on-shell W chain, VBS-biased | WF | n_prompt ≥ 2 | 0.129 / 0.0737 | **2.67** (58) | direct; **misses ℓ→γ radiation**: D-WH-3 |
| B_QCD_Waajj_lv (+nomjj twin) | continuum | (2,3), chain, VBS-biased | WF | n_prompt ≥ 2; twin for generator-m_jj correction | gridpacks building | — | Phase 03 pending |
| ZH:Zγγjj EW (is1h/2/3), lost ℓ | continuum | frozen ZH final | ZF | — | 0.0392 | 0.140 (440) | direct, reused |
| ZH:Zγγjj QCD, lost ℓ | continuum | frozen ZH final, VBS-biased | ZF | twin C (ZH: 2.37) | 0.0356 | 0.033 (187) × C | direct, reused |
| T_ttaa_semilep | continuum | tt̄γγ 1ℓ | WF3·WF_had | — | 0.869 | 0 (0; w_evt 0.21) | no MC support; production N |
| ZH:T_ttaa (dilep) | continuum | frozen ZH | WF² | — | 0.097 | 0.013 (6) | direct, reused |
| F_QCD_lvajj_vbs (+nomjj) | 1 fake γ | (2,3) ℓνγjj, VBS-biased | 1 | n_prompt ≤ 1 | 696 / 6381 | **1.61 ± 0.63** (vbs); 10.3 ± 4.8 (nomjj twin) | fake factor, f×{0.3,1,3}; **C ≈ 4.3 at VBS level** |
| F_EW_lvajj_vbs | 1 fake γ | (0,5) | 1 | n_prompt ≤ 1 | 81.9 | 0.30 ± 0.15 | fake factor |
| F_Wjj_pilot | 2 fake γ | W(→ℓν)+2 partons, fixed order | WF | n_prompt = 0 | 3.45·10⁶ | **1.51 ± 0.95** (3 combinations); f²×{0.09,1,9} | fake factor; lower bound (jets beyond 2 come from the shower) |
| T_tta_semilep | 1 fake γ | tt̄γ 1ℓ | WF3·WF_had | none (ZH lesson) | 773 | 0 combinations in window; 0.66 at VBS | fake factor; bound from production N |
| T_tWa_1l | 1 fake γ | tWγ 1ℓ (DR) | WF3·WF_had | none | 118 | 0 in window; 0.25 at VBS | fake factor |
| ZH:T_tWa (dilep) | 1 fake γ / lost ℓ | frozen ZH | WF² | — | 13.07 | 0.038 (1) | direct Delphes |
| ZH:T_tta (dilep) | | frozen ZH | WF² | — | 85.6 | pending (job still running at writing) | direct Delphes |
| tt̄ semileptonic, 2 fakes | 2 fake γ | not generated | WF3·WF_had | n_prompt = 0 | ~4·10⁵ (ranking) | bound pending | f²·b-veto; pilot needed |
| **ZH:Zγjj EW, e→γ + "lost" e** | e→γ fake | frozen ZH final, 500k | 1 | — | 11.05 | **1.71 ± 0.14** (156) | **direct Delphes e→γ (stock card, no pixel veto)** |
| **ZH:Zγjj QCD, e→γ** | e→γ fake | frozen ZH final, 600k of 6M | 1 | — | 69.46 | **1.39 ± 0.28** (24) × C | as above; D-WH-4 |
| γγjj + non-prompt ℓ | non-prompt ℓ | QCD (2,2) γγjj, VBS + 115–135 window (Q_aajj_vbs, 1k events through PY8+Delphes) | 1 | requires 0 reco leptons | 52.3 | 0.050 ± 0.011 (f_ℓ = 1e-4; ×0.3–10) | parametrised f_ℓ |
| W/γ+jets + non-prompt ℓ, multijet | | not generated | | | | f³ or f_ℓ·f², ranked negligible at order of magnitude | order-of-magnitude statement only |

## 3. Overlap removal (phase-space partition, as ZH, plus WH additions)
1. Prompt photons are counted from GenTruth (`lib/scripts/slim_gentruth.py`): pT > 15, |η| < 2.5, isolated. Wγγ keeps n_prompt ≥ 2, Wγ+jets keeps n_prompt ≤ 1, W+jets keeps n_prompt = 0.
2. **tt̄γ/tWγ are not overlap-removed** (the ZH A9 lesson: ME photons from top-decay products are missing). Double counting with tt̄γγ is bounded by the tt̄γγ yield.
3. EW/QCD are separated by coupling order. Signal and b-complement are separated by external flavour, with closure shown (report 01).
4. **WH-specific gap (D-WH-3).** On-shell W decay chains miss photons radiated by the W-decay lepton. At 0 jets with Wγγ generator cuts, σ(ℓνγγ)/σ(W(→ℓν)γγ chain) = 2.485/1.230 = **2.02 ± 0.02** (`Q_lvaa_0j`, `Q_waa_0j`, identical lepton and photon cuts). For ZH the analogous after-cut factor was only 1.128, because the m_ℓℓ and m_ℓℓγγ cuts removed FSR. WH has no such handle, so the dominant continuum may be underestimated by up to ×2.
   - The Wγ+jets ME (`l vl a j j`) does contain lepton radiation. Its n_prompt = 2 events (second photon from the shower) are discarded by rule 1, which leaves the configuration covered by neither sample.
   - **Options:**
     - (i) generate ℓνγγjj without the chain: QCD has 41 248 diagrams and looks feasible; EW has 67 536 diagrams for W+ alone and is heavy;
     - (ii) keep the on-shell chain and apply an analysis-level ratio from 0j/1j proxies with a conservative nuisance (the ZH approach);
     - (iii) both, with (i) for QCD.
   - **Recommended:** (iii).
5. **e→γ (D-WH-4).** The stock Delphes CMS card turns 7.5 % (signal) to 9.4 % (QCD WH) of generator electrons into photons (report 03 §3). This makes Z(→ee)γjj a 1ℓ + 2γ background of about 3 events at B0, more than the signal.
   - **Recommended:** (a) replace the intrinsic Delphes e→γ with a parametrised f(e→γ) ∈ {1, 2, 5} % (the ZH scenarios), and (b) add an m(eγ) Z-veto (|m_eγ − m_Z| > 10 GeV) and an M_T cut to the selection in Phase 05. Both are standard in Wγ analyses.

## 4. Lost-lepton coverage of the frozen ZH samples (handoff requirement)
- **Coverage inspected in the gridpack run cards:**
  - ZHjj and Zγγjj use an on-shell Z decay chain with `cut_decays = False`, so no generator lepton cuts apply. In the reused samples, 22–27 % of the 1-lepton events have the extra prompt lepton outside pT > 10 / |η| < 2.5, which shows that this region is populated. **Covered.**
  - Zγjj (`l+ l- a j j`, no chain) applies ptl > 10 and |η_ℓ| < 2.5. It covers only leptons lost through ID or isolation, which are 98 % of its 1-lepton events, and not out-of-acceptance leptons. **Partially covered.** A WH-specific sample would be needed if the out-of-acceptance component matters; in the other samples it is ≤ 27 % of lost-lepton events.
- **Delphes inefficiency dominates the "lost" leptons:** 70–75 % of ZH 1-lepton events have the second lepton in acceptance but not reconstructed (electron 57 %, muon 80 % efficiency in signal-like events, report 03). The ZH lost-lepton background therefore scales roughly with (1 − ε_ℓ) and is model-dependent. It goes into the robustness table (Phase 07).
- **Frozen-ZH constraints on the WH selection:** photon pT > 25 GeV and m_jj > 500 GeV (ZH Zγγ generation cuts pta > 25, mmjj > 400).

## 5. Generator-cut safety (twins, as ZH)
- **EW-type samples:** generator m_jj > 400 removes 2.1 ± 0.5 % of the reco-VBS region (signal, which has no generator m_jj cut; LHE–Delphes 1:1, `work/test/genmjj_safety.txt`). Safe, with a 2 % correction or uncertainty.
- **QCD-type samples:** 63 ± 7 % removed (QCD WHjj). **Unsafe.** Twins without the m_jj cut (`B_QCD_Waajj_nomjj`, `F_QCD_lvajj_nomjj`) provide the correction C = Y(twin)/Y(biased). At test-job statistics C ≈ 4.3 for Wγ+jets at VBS level. ZH found 2.05.
- **Photon pT:** the Wγγ/Wγ samples are generated with pta > 25, so the analysis must use pT(γ) ≥ 25 GeV. B0's 20 GeV is a validation baseline only (D-WH-5, recommended 25 GeV as in ZH).

## 6. MC-statistics requirement (handoff §1; `ledger.nmc_check`, N ≥ max(50k, σ·k·3000 fb⁻¹))
- Most samples need the 50k floor.
- The large requirements are F_QCD_lvajj_vbs 2.1 M, its nomjj twin 19 M (auxiliary), F_EW_lvajj 0.25 M, T_tta_semilep 2.3 M, T_tWa_1l 0.35 M and γγjj 0.16 M.
- **W+jets direct: 9.9·10⁹ events, infeasible (D-WH-6).**
  - **Proposed:** fake-factor weighting (no Delphes fakes) on a VBS-biased W+jets sample (m_jj, H_T generator filters proven with twins), declared as an exception with N_eff ≥ 10 in the SR. This mirrors the HH effective-N policy and would be a deviation from SPEC_G0 §1.5 requiring human approval.
- The the analysis does not produce bulk samples (handoff §2.2). This table is the design record for the diff against the canonical arm.

## 7. Fake-rate parametrisation (NOT data-driven)
- f(j→γ) = 10⁻³ (pT/50)^−0.5, ×2 in the endcap, with fake pT = 0.85·pT(jet); scenarios ×{0.3, 1, 3}, squared for double fakes.
- f_ℓ (jet → isolated lepton) ∈ [3·10⁻⁵, 10⁻³], nominal 10⁻⁴.
- f(e→γ) ∈ {1, 2, 5} %.
- These are the ZH scenarios (ZH report 02 §4). Code: `wh/scripts/fake_bound.py`. Delphes jet→γ fakes are recorded but not used for the estimate.

## 8. Summary of first estimates at B0, 500 fb⁻¹ (validation level)
- Signal: 1.17.
- Prompt EW Wγγjj: 2.67 (×≤2 for D-WH-3).
- Fakes: Wγ+jets 1.6 (twin suggests up to ×4 more), W+jets 1.5, e→γ from Zγjj 3.1.
- Resonant: QCD WHjj 0.58, tHq-like 0.33, other H and lost-lepton ZH ≈ 0.3.
- The continuum and the fakes are smooth in m_γγ and are constrained by sidebands; the resonant terms are not. Feasibility will hinge on the m_γγ resolution (σ ≈ 2.1 GeV), the fake rates and the e→γ suppression. **No significance is claimed.**

## 8b. Photon pT 25 GeV re-evaluation (added at review)
B0 uses photon pT > 20 GeV, below the pta > 25 generator cut of the Wγγ/Wγ/Zγγ samples. Re-running all B0 numbers with pT(γ) > 25 GeV (`GPT=25`, `wh/work/b0_pt20_vs_pt25.txt`) changes the window yields as follows:

| Sample | pT > 20 | pT > 25 |
|---|---|---|
| signal | 1.17 | 1.10 |
| EW Wγγjj | 2.67 | 2.63 |
| QCD WHjj | 0.58 | 0.58 |
| Zγjj e→γ (EW + QCD) | 3.10 | 2.71 |
| frozen ZH lost-lepton | 0.23 | 0.22 |

The photons from a 125 GeV decay are hard, so the conclusions of §8 are unchanged. The fake bounds already used 25 GeV.

## 9. Caveats and next actions
- The test-job statistics are small (several components have ≤ 5 raw events or combinations). The ttH and tt̄γ semileptonic samples have no window support.
- The ggF H+jets and tt̄-double-fake bounds are not yet computed.
- `wh_baseline.py` does not apply the n_prompt overlap rule. The reused ZH Zγjj numbers may therefore double count events with two prompt photons, which belong to Zγγ; this is ≤ the Zγγ yield (0.17). The ZH Zγjj direct-Delphes numbers mix Delphes-intrinsic e→γ and j→γ, both untrusted, and the QCD-type generator-m_jj correction C is not applied to them.
- The QCD Wγγjj σ is pending (Phase 03).
- **Next:** human answers D-WH-3 … D-WH-7; then Phase 04 (canonical arm only).


<!-- ===== Phase report 03_generation_validation ===== -->

# WH Phase 03 — generation validation, RUN

- **Date UTC:** 2026-11-08 20:25 → 2026-11-09 00:25.
- **Status: PARTIAL: PASS for 16 of 18 sample types. QCD Wγγjj (`B_QCD_Waajj_lv`) and its no-m_jj twin are PENDING:** their gridpacks were still building on condor at the time of writing (cluster 899736.14/15, JobStatus 2), and their test jobs (899737.14/15) are held until the gridpacks exist. This is reported as pending, not as passed.
- **Git:** base `e681d9b`, uncommitted.
- **Stack:** as report 01. All wrappers come from `p2/lib` unmodified (`scripts/condor/make_gridpack.sh`, `run_job.sh`, `slim_gentruth.py`, `run_py8_delphes.sh`, the slim Delphes card, CP5 common cmnd). WH copies with path-only changes are listed in `wh/patches/README.md` (001–003).

## 1. Smoke tests (interactive, lxplus924, ≤ 4 cores, ≤ 20 min each; LO, NNPDF31 NNLO)
- **Phase 01 cards:** 11 runs, all rc = 0 (report 01 table).
- **Phase 02 cards:** generate-only syntax and diagram checks (`wh/scripts/gen_check.sh`, `wh/work/gencheck/*.status`), all rc = 0:

  | Card | Processes / diagrams |
  |---|---|
  | B_EW_Waajj | 2 / 38 308 |
  | B_QCD_Waajj | 2 / 15 348 |
  | F_EW_lvajj | 160 / 16 128 |
  | F_QCD_lvajj | 240 / 5 280 |
  | F_Wjj | 2 / 404 |
  | bcomp_lv | 6 / 572 |
  | taunu | 2 / 1458 |
  | tHW_1l | 4 / 44 |
  | ttH_semilep | 2 / 50 |
  | VBFH | 60 / 84 |
  | tt̄γ_1ℓ | 2 / 70 |
  | tt̄γγ_1ℓ | 2 / 274 |
  | tWγ_1ℓ | 4 / 56 |
  | Q_lvaa_0j | 8 / 168 |
  | Q_waa_0j | 2 / 56 |
  | off-shell QCD ℓνγγjj | 240 / 41 248 |
  | off-shell EW ℓνγγjj (W+ only) | 80 / 67 536 |

  The `$$` diagram-removal syntax and mixed e/μ/τ decay chains were accepted.

  | Card | σ |
  |---|---|
  | ttH_semilep | 162.3 ± 0.6 fb |
  | tHW_1l | 6.98 ± 0.03 fb |
  | tt̄γ_1ℓ | 771.9 ± 4.1 fb |
  | tt̄γγ_1ℓ | 0.854 ± 0.005 fb |
  | tWγ_1ℓ | 117.3 ± 0.6 fb |
  | VBF H | 4116 ± 30 fb |
  | τν | 6.81 ± 0.04 fb |
  | bcomp_lv | 14.39 ± 0.11 fb |
  | W+2j | 3426 ± 11 pb |
  | γγjj (VBS + window) | 52.27 ± 0.35 fb |
  | Q_lvaa_0j / Q_waa_0j | 2.485 / 1.230 fb |
  | W±H 0j: undecayed / chain / chain with bwcutoff 50 | 1314 / 283.9 / 287.3 fb |

## 2. Condor (EosSubmit schedd; batch names `whs3_gp`, `whs3_test`; no duplicates, checked with `condor_q` before submission)
- **Clusters:** gridpack builds 899736 (18 jobs, seeds J = 900); one test job per sample type in 899737 (18 jobs, seeds J = 1, 1k–5k events each, `keep_lhe = keep_full = 1`). Submit files: `wh/scripts/condor/{gridpacks_p03,test_p03}.sub`; sample table: `wh/config/condor_phase03.txt`.
- **16/16 finished test jobs:** "Normal termination (return value 0)" (`work/condor/test_p03.log`). In every one, n_requested = n_LHE = n_Delphes. Outputs: `wh/work/test/<sample>/` (slim ROOT, GenTruth friend, full record, LHE, json, logs).
- **Gridpack wall times:** 27–481 s per job for 16 samples. The EW Wγγjj charge splits took 371 s and 481 s for event generation and finished well within the "tomorrow" slot.
- **σ closure, Pythia vs gridpack integration** (`wh/work/test/closure_p03.txt`): |rel| ≤ 1.6 % for all 16 samples.

  | Sample | rel |
  |---|---|
  | S_EW_WHjj_lv | +0.7 % |
  | H_QCD | +0.3 % |
  | bcomp | −1.2 % |
  | τν | +0.9 % |
  | tt̄H | −0.2 % |
  | tHW | −1.0 % |
  | VBF H | +0.1 % |
  | EW Wγγ W+ / W− | +0.1 / +0.7 % |
  | F_QCD vbs / nomjj | −0.3 / −0.8 % |
  | F_EW | +0.4 % |
  | W+2j | +1.0 % |
  | tt̄γ | −0.1 % |
  | tt̄γγ | −0.4 % |
  | tWγ | −1.6 % |

  The pulls using the printed Pythia error are not meaningful: that error is truncated (often printed as 0) and omits the re-integration that gridpack `run.sh` performs per job. **The ±2 % tolerance per single test job was chosen after seeing the numbers.** tWγ and tHW are flagged for a job-averaged σ check in production.
- **σ consistency, interactive vs gridpack:** signal 13.62 ± 0.09 vs 13.79 ± 0.03 fb (+1.2 %, 1.8σ). Production normalisation must use the job-averaged gridpack σ, as ZH did.
- **BR closure:** report 01 §4 (W) and H→γγ 2000/2000 (signal and QCD test jobs).

## 3. Delphes object validation (full-record test jobs; `wh/scripts/smoke_wh.py`, `wh/work/test/<s>/objval/smoke_wh_summary.json`, figures `smoke_wh_validation.{png,pdf}`)

| Quantity | EW W±Hjj (signal) | QCD W±Hjj |
|---|---|---|
| gen H→γγ / other | 2000 / 0 | 2000 / 0 |
| e reco efficiency (gen W-electron pT > 15, \|η\| < 2.5, ΔR < 0.1) | **0.57** (445/787) | 0.52 |
| μ reco efficiency (pT > 15, \|η\| < 2.4) | 0.80 (624/783) | 0.74 |
| gen W-electron reconstructed as a photon (ΔR < 0.1) | **7.5 %** | 9.4 % |
| H-photon reco efficiency (pT > 20, acceptance) | 0.78 | 0.74 |
| m_γγ median / 68 % half-width | 125.03 / 2.20 GeV | 124.75 / 2.15 GeV |
| MET − GenMET, x / y 68 % half-width | 17.4 / 16.6 GeV | 16.5 / 16.4 GeV |
| MET response (median, GenMET > 30) | 1.02 | 1.01 |
| M_T(ℓ, MET) median (1-lepton events) | 69 GeV | 62 GeV |
| tag-jet response vs GenJet (median / 68 % half-width) | 1.009 / 0.099 | 1.011 / 0.098 |
| m_jj median (≥ 2 jets) / fraction m_jj > 500 | 464 GeV / 0.48 | 187 GeV / 0.11 |
| b-tag rate per central selected jet (no external b) | 3.7 % | 3.3 % |

**Findings:**
1. The electron efficiency is low, with the same pattern as ZH (report 03 there). This drives the ZH lost-lepton background and the e→γ background (report 02, D-WH-4).
2. MET resolution is about 17 GeV per component with no pileup. MET > 30 GeV keeps 75 % of the signal at B0 (report 02).
3. The m_γγ resolution matches ZH.
4. The light-jet b-mistag of about 3.5 % per jet costs about 6–9 % of signal events through the b-veto.

The same quantities from the independent interactive smoke run (different seed, 2000 events) agree: electrons 0.61, muons 0.82, photons 0.79, m_γγ half-width 2.12 GeV, MET 16.2/16.9 GeV.

## 4. Generator-cut safety and pre-B0 checks
- Generator m_jj > 400: EW-type loss 2.1 ± 0.5 %; QCD-type loss 63 ± 7 % (report 02 §5).
- Photon pT threshold: report 02 §5.
- The prompt-photon multiplicity in GenTruth is filled for all test jobs and used by the overlap rule (`fake_bound.py`).

## 5. Storage
- Slim + GenTruth output is about 2.5 kB per event (as ZH).
- The test-job full records (about 86 kB per event) sit in `wh/work/test`, 3.1 GB in total (`du -sh`); gridpacks are 1.0 GB.
- All of this is git-ignored work space inside the run directory.

## 6. Checks not done / caveats
- QCD Wγγjj and its twin are pending (above).
- No pileup.
- Theory weights are stored but not evaluated.
- Each test job has 1k–5k events, so every B0 number in report 02 is validation-level.
- Delphes jet→γ fakes are not used.

## 7. Next
- Human: decisions (STATUS.md).
- When 899736.14/15 finish, the held test jobs release automatically. The verification needed is σ closure, event counts and B0, using the same scripts.
