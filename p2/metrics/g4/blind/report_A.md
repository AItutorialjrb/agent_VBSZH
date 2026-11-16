# WH Phase 01-03 reports, analysis A


<!-- ===== Phase report 01_signal_definition ===== -->

# WH Phase 01 — signal definition (EW W±Hjj, W→eν/μν, H→γγ)

- **Status: PASS with open decisions D-WH-1…D-WH-3** (defaults applied and labelled; a human answer can change the signal normalisation by the amounts quoted). The HTCondor results for the off-shell and 5F no-top samples were added on 2026-11-09 (§3, §9).
- **Scope:** generator level only: amplitudes, subprocesses, cross sections, BR bookkeeping. No yield in this report is a final result. The illustrative Delphes numbers are in 03.

## 1. Inputs, versions, seeds
| item | value |
|---|---|
| stack | `p2/lib/scripts/setup_stack.sh` (unchanged): LCG_110 x86_64-el9-gcc13-opt, MG5_aMC 3.6.3 upstream (`software/install`, frozen ZH install), Pythia 8.317, Delphes 3.5.1, NNPDF31_nnlo_as_0118 (LHAID 303600) |
| model | `sm-no_b_mass` (MG5 3.6.3). Inputs: aEWM1 = 132.507, G_F = 1.16639e-5, M_Z = 91.188 → M_W = 80.419 GeV, s_W² = 0.22225. Widths: Γ_W = 2.0476, Γ_t = 1.4915, Γ_H = 6.382e-3 GeV |
| beams / PDF | 6800 + 6800 GeV; LHAPDF 303600; α_s from the PDF |
| generator cuts (signal-type) | p_T(j) > 20 GeV, \|η(j)\| < 5, ΔR(jj) > 0.4; `cut_decays = False` (no cuts on W decay products); scale = `dynamical_scale_choice 3` (½ Σ m_T), as ZH |
| seeds | SPEC_G0 §3.4: seed = 2 000 000 + 500 000 + 1000·idx + J. Registry: `wh/config/samples.yaml`; helper `wh/scripts/seeds.py` asserts uniqueness, P = 2, R = x |
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
| EW W±Hjj, 4F | 2x02000 | **62.43 ± 0.45** | +5.4 / −4.9 % | ±1.05 % | −12.6 % (√ŝ) |
| EW W±Hjj, 5F | 2x03000 | 126.9 ± 1.4 | +0.5 / −1.2 % | ±1.14 % | −5.2 % |
| EW W±Hjj, 4F, W→eν/μν (MG5 chain) | 2x01000 | **13.76 ± 0.03** | (gridpack mode; no systematics run) | | |
| QCD W±Hjj, 4F | 2x07000 | **261.1 ± 1.6** | +24.9 / −18.7 % | ±0.87 % | −27.1 % |
| QCD W±Hjj, 4F, W→eν/μν | 2x04000 | **58.83 ± 0.15** | | | |
| EW × QCD interference, 4F | 2x05000 | **−0.256 ± 0.013** | | | |
| EW ℓνHjj (0,5) off-shell, no chain, MG5 default lepton cuts (p_T > 10, \|η\| < 2.5, ΔR_jℓ > 0.4) | 2x06000 | 11.49 ± 0.09 | | | |
| 5F `$$ t t~` (diagnostic, not gauge invariant) | 2x08000 | 144.6 ± 1.0 | | | |

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

Git commit: see `reports/INDEX.md`. Pending items are listed in 03 §6, and the review is in `reports/G1_self_review.md`.


<!-- ===== Phase report 02_background_overlap ===== -->

# WH Phase 02 — background matrix and overlap ledger

- **Date (UTC):** 2026-11-09. **Run:** `RUN`.
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
  - F_Wjj and F_aajj: 1000 events each, through the local PY8 + Delphes slim_v1 chain, seeds 2x14010 / 2x25010.
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


<!-- ===== Phase report 03_generation_validation ===== -->

# WH Phase 03 — generation validation (smoke tests, σ/BR closure, Delphes objects, condor test jobs)

- **Date (UTC):** 2026-11-09. **Run:** `RUN`.
- **Status: PASS for the signal, the resonant QCD W±Hjj, the top-resonant (tt̄H) and the 1-fake-photon (Wγjj) sample types. Overall phase status: BLOCKED (partial).** Continuum Wγγjj: NOT passed.** Its σ integration was still running on HTCondor (cluster 899738.0–2), so it has no gridpack and no test job yet. This is the same situation as the ZH continuum in ZH 03 §3, and it is listed as pending, not as zero.
- **Stack:** `p2/lib/scripts/setup_stack.sh` (LCG_110 + MG5 3.6.3 upstream, Pythia 8.317, Delphes 3.5.1).
  - Pythia: common CP5 card `lib/cards/phase03_smoke/py8_common_CP5.cmnd` + `wh/cards/py8/py8_wh_haa.cmnd` (forced H→γγ) or `py8_wh_noh.cmnd`.
  - Delphes: `lib/cards/phase04_candidates/delphes_card_CMS_slim_v1.tcl` with the seed pinned.

## 1. Commands
```bash
cd RUNDIR/wh
scripts/mg5_smoke_wh.sh cards/phase01/<card>.mg5 <sample> 0 1500        # interactive MG5 (01 samples)
bash -lc 'module load lxbatch/eossubmit; condor_submit scripts/condor/mg5_jobs.sub'   # 02 integrations (cluster 899738; wrapper test 899735)
scripts/local_chain.sh <sample> 10 1000 py8_wh_haa.cmnd                  # gridpack -> LHE -> PY8 + Delphes, 1000 ev, local
bash -lc 'module load lxbatch/eossubmit; condor_submit scripts/condor/test_jobs_A.sub'  # signal + QCD WHjj test jobs (899741)
bash -lc 'module load lxbatch/eossubmit; condor_submit scripts/condor/test_jobs_B.sub'  # ttH 1l + QCD Wajj test jobs (899823)
python3 -P scripts/validate_delphes_wh.py <full.root> <sigma_fb> <out_prefix> <label>
python3 scripts/xsec_br_ledger.py                                         # sigma + BR ledger, assertions
```
- The test jobs use `p2/lib/scripts/condor/run_job.sh` **unchanged**: gridpack → PY8 → Delphes slim → `slim_gentruth.py` → xrdcp with no overwrite, `keep_lhe=1`, `keep_full=1`.
- Outputs are in `wh/work/condor_test/<sample>/`; logs in `wh/work/condor/`.

## 2. Cross sections and closure
- All MG5 cross sections are in the 01/02 tables and in `config/xsec_br_ledger.json`. Every card ran with rc = 0, and its process list and diagram count were recorded.
- Wall times: 30 s – 70 min. The heavy ones are F_EW_Wajj (4156 s on 8 cores) and F_QCD_Wajj_nomjj (2524 s).

| check | result | verdict |
|---|---|---|
| W→ℓν BR closure (EW): σ_chain/σ_undecayed vs MG5-LO 0.22227 | 0.2204 ± 0.0017 (pull −1.1) | PASS |
| W→ℓν BR closure (QCD) | 0.2253 ± 0.0015 (pull +2.1) | PASS (< 3σ; ±1.4 % chain-normalisation systematic, 01 §4) |
| Γ_W(MG5-LO, 9 channels) vs param card | 2.04808 vs 2.0476 GeV | consistent |
| pole approximation: off-shell ℓνHjj (0,5) vs chain with identical lepton cuts (p_T > 10, \|η\| < 2.5, ΔR(j,ℓ) > 0.4) | R = 11.49/(13.76 × 0.819) = **1.020 ± 0.017** | PASS (NWA at 2 %) |
| W→τν / W→(e+μ)ν | 0.495 | PASS |
| gridpack re-run vs integration (EW, 1000 ev, local) | 13.63 ± 0.12 vs 13.76 ± 0.03 fb | PASS (−1.1σ) |
| PY8 σ vs LHE (EW, test job 2000 ev) | 13.79 fb (sum line) vs integration 13.76 fb | PASS (+0.2 %) |
| PY8 σ vs LHE (QCD, test job) | 58.36 vs 58.83 fb | PASS (−0.8 %, gridpack-run MC error ≈ 0.8 %) |
| H→γγ forced (truth, last-copy H) | EW 1000/1000 (local) + 2000/2000 (condor); QCD 1000/1000 + 2000/2000; 0 other decays | PASS |
| Pythia does not fold B_γγ into σ | σ_PY8 = σ_LHE, all events accepted | PASS → B_γγ applied once, externally |
| SLHA: Pythia ignores the MG5 DECAY 25 table (no BRs) and uses its own H width/BRs, then forces γγ | log: "ignoring empty DECAY tables for id = {6,25}" | as intended (physical BR applied in the ledger) |
| W charge (truth) | EW: W⁺ 1265 / W⁻ 735 (63 %); QCD: 61 % W⁺; LHE σ split 62 % | consistent |
| lepton flavour (truth) | EW e 979 / μ 1021; QCD e 1003 / μ 997 | consistent with 50/50 |

## 3. Delphes object validation (condor test-job outputs; `work/validation/<sample>_s<seed>.json`, figures `figures/03_delphes_validation_*.png`)
| quantity | EW W±Hjj (2000 ev) | QCD W±Hjj (2000 ev) | comment |
|---|---|---|---|
| ≥ 2 photons (p_T > 20, \|η\| < 2.5, no crack) | 885 (44 %) | 693 (35 %) | |
| m_γγ Gaussian core μ / σ | 124.93 / **2.06 GeV** | 125.10 / 2.16 GeV | ZH: 124.98 / 2.07 GeV ✓; 91 % / 92 % within 120–130 GeV |
| MET resolution σ68(MET_x,reco − MET_x,gen) | **16.2 GeV** (y: 17.0) | 16.4 GeV | RMS 22 GeV (tails); reco − gen median +3.5 GeV |
| MET relative resolution (GenMET > 50 GeV) | σ68 = 21 % | 19 % | |
| GenMissingET = Σ status-1 ν p_T | median \|Δ\| < 10⁻⁵ GeV | 0 | closure of the truth MET definition |
| isolated e/μ reco efficiency given a generator lepton in acceptance (p_T > 15, \|η\| < 2.5) | **0.70** | 0.65 | low: ZH found the same (isolation in busy H/VBS events, photon priority in UniqueObjectFinder); e 471 vs μ 669 reco → **electron deficit**, carried to Phase 04 (as ZH D11) |
| ≥ 2 jets (p_T > 25, \|η\| < 4.7) | 94 % | 90 % | |
| m_jj median; frac m_jj > 500; frac \|Δη\| > 2.5 | 507 GeV; 0.50; 0.61 | 182 GeV; 0.11; 0.20 | VBS discrimination as expected |
| frac with ≥ 1 b-tag (\|η\| < 2.5) | 6.8 % | 9.7 % | signal loss from the b-veto ≈ 7 % |
| \|Δη_jj\| shape | bimodal: Higgsstrahlung-like (V→jj, 17.6 % of events) + VBF-like | single low-Δη peak | supports the 01 §3.2 statement |
| GenTruth friend | 2000 entries; N_prompt_γ = 0/1/2/3: 78/543/1351/28 | | `slim_gentruth.py` works for WH; caveat: its "last-copy W" is the highest-index \|pid\| = 24, which can be an s-channel W→jj (0 % QCD, ≈ 17 % EW). Phase 04 must patch this to select the leptonic W |
| slim output size | 2.29 kB/event (Delphes 4.34 MB + GenTruth 0.23 MB per 2000) | | full record 86 kB/event, test jobs only |

## 4. Illustrative smoke cutflow (local 1000 events; σ in fb before WF·B_γγ; NOT an optimised selection, never to be tuned on)
| step | EW W±Hjj | QCD W±Hjj |
|---|---|---|
| all | 13.57 | 59.10 |
| ≥ 2 γ | 6.31 ± 0.29 | 20.63 ± 1.10 |
| + exactly 1 ℓ (p_T > 15) | 3.43 ± 0.22 | 12.06 ± 0.84 |
| + lead ℓ p_T > 25 | 3.05 ± 0.20 | 10.93 ± 0.80 |
| + MET > 30 | 2.14 ± 0.17 | 8.39 ± 0.70 |
| + ≥ 2 jets | 1.93 ± 0.16 | 6.74 ± 0.63 |
| + b-veto | 1.80 ± 0.16 | 6.26 ± 0.61 |
| + m_jj > 500, \|Δη\| > 2.5 | 0.99 ± 0.12 (73 ev) | 0.53 ± 0.18 (9 ev) |
| + 120 < m_γγ < 130 | **0.92 ± 0.11** (68 ev) | 0.41 ± 0.16 (7 ev) |
| × WF·B_γγ·500 fb⁻¹ | **1.02 ± 0.12 events** | 0.46 ± 0.17 events |

The signal is about 10× the ZH illustrative-selection yield (0.12). LO, no pileup, tiny samples, and the cuts are not optimised.

## 5. Condor test jobs (one per sample type available; EosSubmit schedd)
| sample type | sample | cluster.proc | seed (mg / py) | requested / LHE / Delphes | PY8 σ vs gen σ | wall: gridpack / PY8+Delphes | exit |
|---|---|---|---|---|---|---|---|
| wrapper test (MG5 integration) | Q_W_aa_0j_onshell | 899735.0 | 2x32000 | — | σ = 1.751 fb | 72 s | 0 |
| signal | S_EW_WHjj | 899741.0 | 2x01001 / 102501001 | 2000 / 2000 / 2000 | 13.79 vs 13.76 fb | 62 s / 159 s | 0 |
| resonant H (QCD) | H_QCD_WHjj | 899741.1 | 2x04001 / 102504001 | 2000 / 2000 / 2000 | 58.36 vs 58.83 fb | 47 s / 219 s | 0 |
| top-resonant H | H_ttH_1l | 899823.0 | 2x18001 / 102518001 | 2000 / 2000 / 2000 | 108.6 vs 108.2 fb | 47 s / 241 s | 0 |
| 1 fake photon | F_QCD_Wajj | 899823.1 | 2x12001 / 102512001 | 2000 / 2000 / 2000 | 691.5 vs 687.5 fb | 144 s / 211 s | 0 |
| prompt continuum | B_*_Waajj | — | — | **not submitted: gridpack still integrating (899738.0–2)** | | | — |

- No duplicate submissions: `condor_q` was checked before each submit, and the clusters belonging to other runs were not touched.
- The seeds come from the registry (J = 1 for test jobs), and the uniqueness assertion passed.
- MG5 integration clusters: 899735 (1 job) and 899738 (20 jobs; 17 done with rc = 0 at writing time, 3 continuum jobs running).

### 5.1 Second test batch (899823)
- **H_ttH_1l:**
  - Truth: H→γγ 2000/2000. m_γγ core σ = 2.02 GeV. ≥ 1 reco lepton in 950/2000 events.
  - **≥ 1 b-tag in 84 % of events**, so the b-veto is the main handle.
  - Validation file: `work/validation/H_ttH_1l_s2518001.json`.
- **F_QCD_Wajj:**
  - GenTruth N_prompt_γ = 0/1/2 in 313/1655/32 events. The overlap rule (keep exactly 1) retains 82.8 %. The N = 0 events are covered by W+jets and the N = 2 events by Wγγ.
  - Phase 04 validates the stitching with the boundary-continuity test of 02 §4.
  - Reco photons (p_T > 20, |η| < 2.5) per event: 0/1/≥2 in 716/1220/64 events.
- **All four event-level test jobs:** exit 0, N_LHE = N_Delphes = requested, σ closure within 0.8 %, outputs staged with size checks.

## 6. Pending at G1
1. `B_EW_Waajj`, `B_QCD_Waajj`, `B_QCD_Waajj_vbs`: σ integration and gridpack (899738.0–2, flavour "tomorrow"). Afterwards: one test job (prompt-continuum type) with the same submit pattern (`test_jobs_B.sub`).
2. The off-shell continuum (D-WH-4) has no card in production form yet. Its cost has to be measured.

## 7. Caveats
- No pileup.
- Stock CMS Delphes card with the known electron deficit.
- The e→γ fakes have no pixel-seed veto in Delphes; a parametrised f_e is used instead (02).
- Tiny samples: MC errors as shown. Nothing here is a final yield.

Git commit: see `reports/INDEX.md`.
