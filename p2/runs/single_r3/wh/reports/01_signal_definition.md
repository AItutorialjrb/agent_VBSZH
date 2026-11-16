# WH Phase 01 — signal definition (EW W±Hjj, W→eν/μν, H→γγ), single_r3

- **Date UTC:** 2026-11-08 20:20 → 2026-11-09 00:10 (incl. a usage-limit interruption ~20:45–23:59).
- **Status: PASS with decisions open (D-WH-1 flavour scheme, D-WH-2 W normalisation convention).** The numbers below hold under the recommended defaults. No number here is a yield. All are generator- or validation-level and are labelled as such.
- **Agent:** single arm, one Claude Code session (Opus), no subagents. The run reads `SPEC_G0.md` in place of `SPEC.md`.
- **Git:** base commit `e681d9b`; this run's files are **uncommitted** (no commit without a human instruction, see D-WH-9).
- **Inputs/versions:** stack `LCG_110/x86_64-el9-gcc13-opt + MG5_aMC_v3.6.3 (upstream)`, sourced from `p2/lib/scripts/setup_stack.sh`; Pythia 8.317 with CP5; Delphes 3.5.1 with the slim CMS card from `p2/lib`; NNPDF31_nnlo_as_0118 (LHAID 303600); model `sm-no_b_mass`; dynamical scale choice 3 (HT/2), as in ZH.
- **Seeds:** SPEC_G0 §3.4 with P=2, R=6: `seed = 2 600 000 + 1000·idx + J`, from the registry `wh/config/samples.yaml`. J=0 for interactive runs, J=900 for gridpack builds, J≥1 for condor jobs. Uniqueness is asserted by `wh/scripts/seeds.py`, plus a check over all 58 planned seeds.

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
| **Signal production**, W→ℓν chain (ℓ=e,μ) | `p p > w+ h j j QCD=0 QED=4, w+ > l+ vl` + w− | 2 groups / 1460 | 13.62 ± 0.09 fb (interactive); **13.79 ± 0.03 fb** (gridpack build, seed 2603900) |
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
