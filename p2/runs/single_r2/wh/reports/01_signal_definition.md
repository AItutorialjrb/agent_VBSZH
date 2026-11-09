# WH Phase 01 — signal definition (EW W±Hjj, W→eν/μν, H→γγ)

- **Date (UTC):** 2026-11-08. **Run:** `single_r2` (single-agent arm, one Claude Code session, Opus 5.5, no subagents). **Spec:** `p2/SPEC_G0.md` (read in place of `p2/SPEC.md`), handoff §5.1.
- **Status: PASS with open decisions D-WH-1…D-WH-3** (defaults applied and labelled; a human answer can change the signal normalisation by the amounts quoted). The HTCondor results for the off-shell and 5F no-top samples were added on 2026-11-09 (§3, §9).
- **Scope:** generator level only: amplitudes, subprocesses, cross sections, BR bookkeeping. No yield in this report is a final result. The illustrative Delphes numbers are in 03.

## 1. Inputs, versions, seeds
| item | value |
|---|---|
| stack | `p2/lib/scripts/setup_stack.sh` (unchanged): LCG_110 x86_64-el9-gcc13-opt, MG5_aMC 3.6.3 upstream (`software/install`, frozen ZH install), Pythia 8.317, Delphes 3.5.1, NNPDF31_nnlo_as_0118 (LHAID 303600) |
| model | `sm-no_b_mass` (MG5 3.6.3). Inputs: aEWM1 = 132.507, G_F = 1.16639e-5, M_Z = 91.188 → M_W = 80.419 GeV, s_W² = 0.22225. Widths: Γ_W = 2.0476, Γ_t = 1.4915, Γ_H = 6.382e-3 GeV |
| beams / PDF | 6800 + 6800 GeV; LHAPDF 303600; α_s from the PDF |
| generator cuts (signal-type) | p_T(j) > 20 GeV, \|η(j)\| < 5, ΔR(jj) > 0.4; `cut_decays = False` (no cuts on W decay products); scale = `dynamical_scale_choice 3` (½ Σ m_T), as ZH |
| seeds | SPEC_G0 §3.4: seed = 2 000 000 + 500 000 + 1000·idx + J. Registry: `wh/config/samples.yaml`; helper `wh/scripts/seeds.py` asserts uniqueness, P = 2, R = 5 |
| cards | `wh/cards/phase01/*.mg5` (OUTDIR/SEED substituted by the runner) |
| runner | `wh/scripts/mg5_smoke_wh.sh <card> <sample> [J] [timeout]` (patch 001 of `lib/scripts/mg5_smoke.sh`, see `wh/patches/README.md`); outputs in `wh/work/smoke/<sample>_s<seed>/` (status.txt, mg5.log, processes.txt, Cards/, banner) |
| host | lxplus924 (interactive, nb_core 4, every run ≤ 3 min); heavier runs went to HTCondor (03 §6) |

## 2. Gauge-invariant signal definition
**Signal (definition a):** the complete tree-level electroweak amplitude for pp → W⁺Hjj and pp → W⁻Hjj at amplitude order (QCD, QED) = (0, 4). Every Feynman diagram at this order is included, and all of them interfere coherently. MG5 syntax: `generate p p > w+ h j j QCD=0 QED=4, w+ > l+ vl` + `add process p p > w- h j j QCD=0 QED=4, w- > l- vl~`, with ℓ = e, μ.
- **No topology filter is used:** no required s/t-channel bosons, no `$`/`/` diagram vetoes. "VBF-like" / "VBS" refer to *fiducial regions* (large m_jj and |Δη_jj|) of this single gauge-invariant amplitude. They are never diagram subsets.
- **Flavour scheme (D-WH-1, default applied): 4-flavour external states.** p = j = {g, u, c, d, s} and their antiquarks; no b, massless quarks, diagonal CKM.
  - Removing a whole external-flavour class is gauge invariant. A diagram veto is not.
  - Why: with b quarks in p/j, the (0, 4) W±Hjj amplitude contains resonant t → Wb diagrams. For example q b → q′ t H with t → W b is exactly tHq.
  - Measured: **σ(5F) = 126.9 ± 1.4 fb vs σ(4F) = 62.43 ± 0.45 fb.** The b-containing external states therefore add +103 % of the 4F rate.
  - This excess matches the tHq rate: σ(tHq, t→bℓν) = 15.40 fb corresponds to ≈ 69 fb before the top/W decay (02 §3.5).
  - The `$$ t t~` diagnostic gives **144.6 ± 1.0 fb, i.e. more than the full 5F result**. Removing the s-channel top breaks the gauge cancellations, so the non-top b-initiated piece **cannot be isolated this way**. The number is not interpretable and is shown only to document why diagram removal is unsafe.
  - In the 4F definition, tHq and tHW are *separate resonant backgrounds* (02), suppressed by a b-veto. A 5F signal would instead absorb tHq into "signal", which is not the VBS/VBF WH physics targeted.
  - Inconsistency, stated: the PDF is a 5-flavour set (as everywhere in ZH). The non-top b-initiated EW W±Hjj piece (b as spectator) is dropped from the signal; its size is a signal-definition uncertainty to be quoted from the diagnostic run.
- **W decay:** in the MG5 decay chain (narrow width, `bwcutoff` = 15). This keeps the W spin correlations and the lepton–neutrino kinematics in the matrix element.
- **H decay:** H is undecayed in the LHE and forced to γγ in Pythia8 (§4).

### 2.1 Subprocesses and diagrams (from `processes.txt` and `mg5.log` in each `work/smoke/<sample>/`)
| sample | partonic subprocesses | P-directories | diagrams (MG5 "Total") | notes |
|---|---|---|---|---|
| S_EW_WHjj_nodecay (4F) | 80 (40 per charge) | 2 | 1456 (728 per charge) | gg-initiated W±Hqq̄ is tried but has 0 diagrams at QCD = 0 (correct: no gluon couples in a pure-EW amplitude) |
| S_EW_WHjj (4F, W→ℓν) | 80 production | 2 | 1460 = 1456 + 2 decay diagrams (W→eν_e, W→μν_μ; W→eν_μ correctly has none) | discrepancy of 2 explained |
| S_EW_WHjj_5F_nodecay | 104 | 2 | 1792 | +24 b-containing subprocesses (e.g. `b b~ > w+ h d u~`, `b c~ > w- h b s~`) |
| H_QCD_WHjj_nodecay (4F, (2,2)) | 96 | 8 | 352 | includes gg, qg and qq initial states |
| I_WHjj (`QCD^2==2 QED^2==6`) | 80 | 2 | 1680 | **closure:** in the uniquely generated processes, I = EW + QCD-four-quark diagrams exactly (360 = 312 + 48); there are no gluon-initiated I processes, as required |

## 3. Cross sections (LO, MG5 integration error; undecayed unless stated)
| sample | seed | σ [fb] | scale 7-pt | PDF | scale-choice envelope (1–4) |
|---|---|---|---|---|---|
| EW W±Hjj, 4F | 2502000 | **62.43 ± 0.45** | +5.4 / −4.9 % | ±1.05 % | −12.6 % (√ŝ) |
| EW W±Hjj, 5F | 2503000 | 126.9 ± 1.4 | +0.5 / −1.2 % | ±1.14 % | −5.2 % |
| EW W±Hjj, 4F, W→eν/μν (MG5 chain) | 2501000 | **13.76 ± 0.03** | (gridpack mode; no systematics run) | | |
| QCD W±Hjj, 4F | 2507000 | **261.1 ± 1.6** | +24.9 / −18.7 % | ±0.87 % | −27.1 % |
| QCD W±Hjj, 4F, W→eν/μν | 2504000 | **58.83 ± 0.15** | | | |
| EW × QCD interference, 4F | 2505000 | **−0.256 ± 0.013** | | | |
| EW ℓνHjj (0,5) off-shell, no chain, MG5 default lepton cuts (p_T > 10, \|η\| < 2.5, ΔR_jℓ > 0.4) | 2506000 | 11.49 ± 0.09 | | | |
| 5F `$$ t t~` (diagnostic, not gauge invariant) | 2508000 | 144.6 ± 1.0 | | | |

- **Charge split** (gridpack re-run of S_EW_WHjj, LHE `<init>`): W⁺ 8.48 fb, W⁻ 5.15 fb (62 % W⁺); QCD: 36.3 / 22.7 fb.
- **Ratios at loose cuts:** QCD/EW = 4.18 (undecayed), 4.28 (W→ℓν).
  - Interference: σ_I/σ_EW = **−0.41 ± 0.02 %**; σ_I/(σ_EW + σ_QCD) = −0.08 %.
  - VBS-region interference: not evaluated yet. It needs a signed-weight Delphes sample in Phase 04 (ZH: −0.20 % in the VBS region).
- **Interference statement:** the EW–QCD cross term exists only in four-quark channels; it is colour-suppressed and small at loose cuts. It is kept as a **separate signed component**, never as positive events. In definition (a) it is a ±0.4 % systematic on the signal unless the VBS-region value comes out larger.

### 3.1 Definitions (a) and (b)
| def. | signal | resonant WHjj background | σ(W→eν/μν) at generator cuts |
|---|---|---|---|
| (a) | EW (0,4) only | QCD (2,2) W±Hjj, separate sample; signed I term as systematic | s: 13.76 fb; b_res: 58.83 fb |
| (b) inclusive | EW + QCD + I (all W±Hjj at O(α_s⁰⁻²)) | none from W±Hjj | 13.76 + 58.83 + I(≈ −0.056, scaled by the measured W BR closure) ≈ 72.5 fb |

Definition (b) is reported alongside (a) in later phases, as in ZH. The VBS selection is the discriminant between EW and QCD.
- Parton level (`work/validation/*_lhe.json`): m_jj > 500 GeV and |Δη| > 2.5 hold for 61.4 % of EW events, against 5.7 % of QCD events.

### 3.2 Higgsstrahlung-like and VBF-like content (parton level, EW, 1000 events, `scripts/lhe_summary.py`)
- 17.6 % of EW events contain an MG5-written s-channel W/Z → qq̄ resonance (W V H "triboson-like" configuration). Independently, 17.6 % have a parton m_jj in 60–110 GeV.
- These configurations are part of the gauge-invariant signal. **No separate WWH/WZH (V→jj) sample may be added** (double counting). A resonance-region m_jj bin is an observable, not a diagram label.
- VBF-like region (m_jj > 500, |Δη| > 2.5): 61.4 % of EW events, against 5.7 % for QCD.

## 4. Decays and the BR ledger (BR applied exactly once, asserted in `wh/scripts/xsec_br_ledger.py`)
- **H → γγ:** in Pythia8, `25:onMode = off`, `25:onIfMatch = 22 22` (card `wh/cards/py8/py8_wh_haa.cmnd`, identical to the validated ZH card).
  - Pythia does **not** fold the BR into σ: σ_PY8 = 13.57 fb vs LHE 13.63 ± 0.12 fb, with 1000/1000 events accepted.
  - The physical B_γγ = 0.002270 (LHCHWG YR4, m_H = 125 GeV, as ZH) is applied **once**, externally.
  - Truth: 1000/1000 last-copy H → γγ in EW and in QCD (03 §3).
- **W → ℓν: the factor WF.**
  - MG5-LO computes Γ(W→ℓν) = e²M_W/(48π s_W²) = 0.22756 GeV per flavour. With Γ_W = 2.0476 GeV this gives B_MG5 = 0.111137 per flavour, i.e. 0.222274 for e + μ.
  - Closure: σ(W→ℓν)/σ(undecayed) = 13.76/62.43 = **0.2204 ± 0.0017** (EW, pull −1.1). For QCD it is 58.83/261.1 = 0.2253 ± 0.0015 (pull +2.1).
    - Agreement is within ≈ 1.4 % in both cases, at the level expected from the Breit–Wigner truncation and the off-shell kinematic dependence of the decay chain (ZH Z→ℓℓ: +1.2 %).
    - **PASS** with tolerance |pull| < 3. This tolerance was fixed when writing this report; it is the ZH convention.
    - The ±1.4 % is quoted as a decay-chain normalisation systematic.
  - PDG 2025 (`wh/config/sources/pdg2025_w.pdf`, sha256 `4e23549b…3e848`; text lines 413–417): B(eν) = 10.71 ± 0.16 %, B(μν) = 10.63 ± 0.15 %, B(τν) = 11.38 ± 0.21 %, lepton-universal B(ℓν) = 10.86 ± 0.09 %, B(hadrons) = 67.41 ± 0.27 %.
  - **Nominal (D-WH-2): WF = 0.1086/0.111137 = 0.97717**, applied once per leptonic W whose decay is computed by MG5.
    - Alternative: the non-universal e + μ fit gives WF = 0.96008 (−1.75 %), quoted as a BR systematic.
- **Hadronic W in MG5 chains (top samples):** HF = 0.6741/(6·0.22756/2.0476) = 1.01092 per W → jj.
- **Top in MG5 chains:** Γ_MG5(t→bW) = 1.49541 GeV vs Γ_t = 1.4915 GeV, so TF = 0.99739 per top (physical B(t→Wb) = 1).
- **Off-shell ℓν in the ME (no chain, e.g. Wγjj):** the rate carries the same MG5-LO W→ℓν coupling, so WF is applied as well. This is D-WH-3, and it differs from ZH, which applied no factor to ℓℓ in the ME because of γ*/Z interference. W has no such interference. The non-resonant part makes this a ±2.3 % scheme systematic.
- **Signal ledger:** k = WF × BGG = 0.97717 × 0.002270 = **2.2182 × 10⁻³**.
  - σ×k = 13.76 × 2.2182e-3 = **0.03052 fb**, i.e. **15.3 events at 500 fb⁻¹ before any acceptance** (LO, scale +5/−5 %).
  - Cross-check from the undecayed σ: 62.43 × 0.2172 × 0.002270 = 0.03078 fb (+0.9 %, consistent with the closure).
  - The machine-readable ledger is `wh/config/xsec_br_ledger.json`, regenerated by `python3 wh/scripts/xsec_br_ledger.py`. The script aborts if BGG appears more than once, if WF/HF/TF counts differ from the number of MG5-decayed W/t, or if a Z factor appears in a W sample.
- **N_MC requirement** for the signal: max(50k, 0.03052 × 3000 = 92) = **50 000** events. QCD W±Hjj: max(50k, 0.1305 × 3000 = 392) = 50 000.

## 5. Other same-final-state Higgs components (assigned in 02)
- W → τν with τ → ℓνν: a separate sample, `H_EW_WHjj_tau` (and its QCD analogue). It is not part of the ℓ = e, μ signal.
- tHq/tHW: resonant backgrounds (see D-WH-1).
- ZHjj with a lost lepton: reused from the frozen ZH samples.
- ggF/VBF H + fake lepton: bounds.
- H-pole vs continuum ℓνγγjj interference: absent from generated samples (no tree Hγγ vertex). Quoted as a caveat, as ZH 02 §3.6.

## 6. Checks
1. Order separation verified by diagram counts and the interference closure (§2.1).
2. gg → W±Hqq̄ has 0 EW diagrams.
3. Lepton-flavour-violating decay chains have no diagrams.
4. W BR closure: PASS (§4).
5. Pythia σ = LHE σ; H → γγ forced, 1000/1000.
6. Seeds are unique (registry assertion).

## 7. Caveats
- LO only.
- 4F external states with a 5F PDF.
- NWA for W. Verified: the off-shell ℓνHjj result over the decay chain with identical lepton cuts gives R = 1.020 ± 0.017 (03 §2), so the pole approximation holds at ≈ 2 %. This is quoted as a systematic.
- The scale-scheme envelope (−12.6 % EW) is larger than the 7-point band. Report both.
- Pure-EW Born: a small scale band does not bound missing EW corrections.

## 8. Decisions raised (the human may override; defaults in force)
- **D-WH-1** (flavour scheme): 4F signal + tHq/tHW as separate b-vetoed backgrounds [default]; alternatives: 5F signal including tHq-like amplitudes, or 4F + an additive non-top b-initiated correction from the diagnostic.
- **D-WH-2** (W BR): WF from the lepton-universal PDG fit (0.97717) [default] vs the non-universal e/μ values (0.96008).
- **D-WH-3** (ℓν in the ME without a chain): apply WF [default] vs no factor (the ZH ℓℓ convention).

## 9. Next actions
- Done: off-shell and 5F-no-top results (§3).
- Open: quantify the non-top b-initiated EW part some other way, e.g. a 5F sample with a b-tag-vetoed fiducial comparison at Delphes level (Phase 04).
- VBS-region interference at Delphes level (Phase 04).

Git commit: see `reports/INDEX.md`. Pending items are listed in 03 §6, and the self-review is in `reports/G1_self_review.md`.
