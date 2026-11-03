# Phase 01 — signal definition: EW W±Hjj, W→ℓν (ℓ=e,μ), H→γγ, √s = 13.6 TeV (WH, multi_r1)

Date UTC: 2026-11-03 (start 16:14 UTC, end see PROGRESS.md). **Status: PASS with open decisions (see STATUS.md D-WH-0…9)** (D-WH-1 seed-range overlap; none blocks Phase 02/03; see STATUS.md).
Author: executor-wh (Sonnet), run multi_r1. Process dir: `/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh`. Frozen-ZH methodology: `reports/01_signal_process.md`, `03_generation_validation.md` (read-only).
All numbers below are LO MG5 cross sections with the MG5 integration error, **validation quantities, not yields**. No yield after selection is quoted in Phases 01-03.

## 1. Goal
Define the gauge-invariant EW W±Hjj signal (both charges), its decay implementation and BR ledger, the QCD W±Hjj resonant background (definition a) / inclusive variant (definition b), the interference statement, and separate VBF-like kinematics from diagram labels. Validate orders by MG5 diagram counts, subprocess lists and cross sections.

## 2. Inputs, versions, seeds
Stack as ZH (`lib/scripts/setup_stack.sh`): LCG_110 view, MG5_aMC 3.6.3 (upstream tarball, "UNKNOWN DEVELOPMENT VERSION" banner is a packaging marker, as in ZH 03_stack.md), Pythia 8.317 (CP5, dipole recoil on for EW samples), Delphes 3.5.1 slim CMS card (`delphes_card_CMS_slim_v1.tcl`), model `sm-no_b_mass` (5F, massless b/light quarks, diagonal CKM, no light Yukawas), PDF NNPDF31_nnlo_as_0118 (LHAID 303600), beams 6800+6800 GeV, scale choice 3 (½ Σ m_T), `use_syst` on. Jet generation cuts as ZH signal: pT(j)>20, |η(j)|<5, ΔR(jj)>0.4, ΔR(jℓ)>0.4, `cut_decays=False` (no cuts on W-decay leptons). Parameter card (generated): MW = 80.419 GeV (derived), MZ = 91.188, Gf = 1.16639e-5, 1/α = 132.507, WW = 2.0476 GeV (fixed), MH = 125, WH(MG5) = 6.38e-3 GeV (not used), MT = 173.
Seeds (SPEC 3.4): smoke runs P=2, R=11, sample index 0 → 2110001…2110029 (listed per card in `scripts/run_smoke_batch{1,2}.sh`); PY8 validation seeds 2110101-2110103 (W⁺, W⁻, τν) (Delphes `RandomSeed` pinned by `run_py8_delphes.sh`). Git commit: recorded by orchestrator.

## 3. Definition of the signal (gauge-invariant)
**Signal (definition a)** = full tree amplitude of pp → W^± H + 2 partons at amplitude order (QCD,QED) = (0,4), summed coherently over all diagrams and all external-flavour configurations with *light* partons {u,d,s,c} (+ antiquarks) in the initial and final state, both W charges. No diagram vetoes, no required intermediate boson. W decayed in the MG5 matrix element by a decay chain (`w+ > l+ vl`, e,μ) so spin correlations are kept; H left undecayed in the LHE and forced to γγ in Pythia8. Command (validated, `cards/prod/S_EW_WHjj.mg5`):
```
generate p p > w+ h j j QCD=0 QED=4, w+ > l+ vl
add process p p > w- h j j QCD=0 QED=4, w- > l- vl~     (p = j = g u c d s u~ c~ d~ s~ ; no b)
```
**Why light flavours only (decision D-WH-0, taken here, evidence below).** In the 5-flavour model, with b in p/j, the (0,4) amplitude contains W⁺ + b-jet states in which an on-shell top decays t→W⁺b (tHq and tHW topologies: b q → t q' H, t → W b). These are a separate, resonant process (own samples, Phase 02). External-flavour selection is gauge invariant; diagram removal is not.

| W⁺Hjj (0,4), undecayed, LO | σ [fb] | diagrams / subprocesses |
|---|---|---|
| p,j light (u c d s) = **signal** | 38.40 ± 0.20 | 390 / 22 |
| p,j incl. b (5F) | 82.75 ± 0.46 | 474 / 28 |
| p,j incl. b, `/ t t~` (top diagrams removed by hand) | 178.6 ± 1.4 | 456 / 28 |

(a) The b-inclusive sample is 2.2× the light one; an LHE-level classification of its 2000 events (`scripts/lhe_classify.py`, `work/smoke/wp_b_nodec/classes.json`; validation only) gives: no external b: 38.98 fb (≈ the light-only σ, closure 1.5 %); b external with a W⁺b pair within ±25 GeV of m_t (top-resonant): 41.7 fb; b external, not top-resonant: **2.1 ± 0.3 fb (5.4 % of the signal; 3.8 % within the VBS-like region)**. Cross-check: tHq with t→b ℓν (both signs, e/μ), σ = 14.88 fb (`H_tHq_lep_smoke`) corresponds to 14.88/0.2222 ≈ 67 fb for t+t̄ with all W decays; the W⁺b configuration is the *t* (not t̄) share, t:t̄ ≈ 2:1 at the LHC, i.e. ≈ 45 fb, which agrees with the 41.7 fb top-resonant class within the expected size of the remaining tHW-like/non-resonant pieces and MC errors (the earlier equal-split estimate of 33 fb was wrong). (b) Removing the top diagrams by hand (`/ t t~`) raises σ by a factor 2.2 → the diagram subset is not gauge invariant (the gauge cancellations are destroyed), i.e. **top diagrams must not be vetoed; the external-flavour definition is used instead.** (c) Non-top-resonant b-initiated/b-jet pieces (+5 %) are **not** in the signal; this is a documented incompleteness, carried as a **+5 % / −0 %** theory systematic on S in Phase 06 (the excluded piece adds to the signal) (requires human sign-off: D-WH-0 is stated in STATUS as information, not blocking). The same light-flavour rule is applied to QCD W±Hjj and the interference.

**Cross sections (before any BR beyond the ME decay), LO, both charges listed separately**
| | σ(W⁺Hjj) [fb] | σ(W⁻Hjj) [fb] | sum |
|---|---|---|---|
| EW (0,4), W,H undecayed | 38.40 ± 0.20 | 23.65 ± 0.14 (2 seeds, 23.66 ± 0.16, 23.59 ± 0.35) | 62.05 ± 0.25 |
| EW, W→ℓν in ME (e+μ) | 8.538 ± 0.043 | 5.151 ± 0.022 (2 seeds) | one card, both charges: 13.63 ± 0.18 |
| EW, W→τν in ME | | | 6.71 ± 0.11 |
| QCD (2,2), undecayed | 165.2 ± 0.8 | — | QCD/EW = 4.30 (W⁺) |
| EW×QCD interference (QCD²==2, QED²==6), undecayed | −0.1253 ± 0.0083 (−0.33 ± 0.02 % of EW) | | both charges: −0.264 ± 0.013 fb (−0.43 %) |

W⁺/W⁻ = 1.62 (pp initial state). The QCD/EW ratio (4.3) is smaller than for ZH (7.9) at the same loose generator cuts, so the QCD component is the dominant resonant background before VBS cuts, as in ZH.

## 4. Orders validated by diagrams / subprocess lists
Statement of orders (W undecayed, 6 couplings of the 2→4 tree: M_EW ~ g⁴, M_QCD ~ g_s² g²; decay in chain adds no coupling to the production orders, as ZH):
| Card line | subprocesses / diagrams (incl. b) | light only |
|---|---|---|
| `QCD=0 QED=4` (EW) | 28 / 474 | 22 / 390 |
| `QCD=2 QED=2` (QCD) | 20 / 80 | 20 / 80 |
| `QCD^2==2 QED^2==6` (interference) | 28 / 546 | 22 / 450 |
| EW with `w+ > l+ vl` chain, W⁻ | 28 / 474 (W⁻ and chain identical counts) | 22 / 390 |
The EW and QCD sets are disjoint by coupling order (no process line contains both); the interference process contains only diagrams of both orders that interfere (450 < 390+80 because some subprocesses have no colour-allowed overlap). Files: `work/diag/<card>/{mg5.log,proc_list.txt,subproc.mg}`, cards `cards/diag/`. The EW σ(W⁺) is stable between the card with and without the decay chain only through the BR (see 5). MG5 writes intermediate W/Z resonance lines in the LHE of the undecayed sample; they are used in section 6 only as *labels*.

## 5. Decay implementation, BR ledger and closure
**H→γγ.** No tree H→γγ vertex exists in the SM model; a `h > a a` decay chain is **not** used. H is undecayed in the LHE, and Pythia8 forces `25:onMode=off, 25:onIfMatch=22 22` (as ZH, `cards/py8_whjj_haa.cmnd`); the conditional BR is 1 and the physical **B_γγ = 0.002270 (LHCHWG YR4, mH=125.00; same input as ZH) is applied once, externally.** Pythia does not fold the BR into σ: PY8 σ vs LHE init σ: 8.507 ± 0.030 fb vs 8.538 ± 0.043 fb (W⁺→ℓν, 1000 events, −0.4 %); W⁻: 5.166 ± 0.018 fb (LHE 5.151 ± 0.022); τν: 6.749 fb (LHE 6.71 ± 0.11). Generator record: last-copy H → γγ in 1000/1000 (W⁺), 1000/1000 (W⁻), 500/500 (τν) events, 0 other (`work/py8chk/*/validation.json`).

**W→ℓν ledger and WF.** W decayed in the MG5 ME with the model's tree widths. The correction to the PDG physical BR is the analogue of ZF = 0.9783:
Γ(W→ℓν) = G_F M_W³/(6√2 π) = 227.56 MeV (MG5: M_W = 80.419 GeV, G_F = 1.16639e-5), 9 Γ_ℓν = 2.0481 GeV vs the card's WW = 2.0476 GeV (consistent, tree, no QCD correction) ⇒ B_MG(W→ℓν) = 0.11114 per flavour, 0.22227 for e+μ, B_MG(W→hadrons) = 0.66682.
B_PDG (PDG 2025 W boson listing, `config/pdg2025_W.pdf`): B(eν) = 10.71 ± 0.16 %, B(μν) = 10.63 ± 0.15 %, B(τν) = 11.38 ± 0.21 %, B(had) = 67.41 ± 0.27 %.
**WF = B_PDG(eν+μν)/B_MG(eν+μν) = 0.2134/0.22227 = 0.9601 ± 0.0099 (PDG error)**; WFτ = 0.1138/0.11114 = 1.0240; WHAD = 0.6741/0.66682 = 1.0109 (hadronic W in single-lepton top configurations; Phase 02). Derivation and code: `scripts/br_ledger.py` (run it to reproduce; it also asserts that no BR is applied twice and provides `nmc_check`).
Ledger convention for the σ-only interference sample I_WHjj (W undecayed): its σ is multiplied by the physical B_PDG(W→eν+μν) = 0.2134 (not WF×B_MG) and B_γγ, once; it is never showered with a W decay, so there is no second application. If events were ever showered, the W must be decayed in PY8 with forced e/μ (conditional BR 1).
Per-sample ledger for the signal: σ_phys = σ_MG(W→ℓν in ME) × WF × B_γγ, k = 0.96008 × 0.002270 = **2.1794e-3**. Before-BR/after-decay/after-cuts are kept distinct: σ_MG (ME-decayed, "after decay in ME"), σ_phys = ×k ("after BR"), and acceptance only in Phase 05.
With the numbers of this phase: σ_phys(EW W±Hjj→ℓνγγjj, loose gen cuts) = 13.63 fb × 2.179e-3 = **0.0297 fb** → 14.9 events at 500 fb⁻¹ *before any acceptance* (LO; ZH analogue 1.44 events; ratio 10.3). Not a yield.
The W→τν→ℓ feed-down (S_EW_WHjj_taunu, σ_MG = 6.71 ± 0.11 fb, k = WFτ × B_γγ = 2.324e-3) is a separate resonant-signal-like component (Phase 02).

**BR/σ closure (σ_decayed/σ_undecayed vs analytic 0.22227)**, `scripts/closure.py`, `work/closure.txt`:
| | ratio | expected | pull |
|---|---|---|---|
| W⁺→ℓν | 0.2223 ± 0.0016 | 0.2223 | +0.04 |
| W⁻→ℓν (2 independent seeds each) | 0.2178 ± 0.0016 | 0.2223 | −2.76 |
| W⁺ and W⁻ combined | 0.2206 ± 0.0012 | 0.2223 | −1.40 |
| one card, both charges (S_EW_WHjj) | 0.2197 ± 0.0030 | 0.2223 | −0.87 |
| W→τν, both charges | 0.1081 ± 0.0018 | 0.1111 | −1.71 |
Diagnostic: the same W⁻ chain with `bwcutoff=1000` (seed 2110029) gives 0.2989 ± 0.0051 (+37 %): this is *not* a closure test (it admits the off-shell W tail, non-resonant ℓνHjj) but shows the decay-chain σ depends on the Breit-Wigner cut. The default `bwcutoff=15` removes events with |m_ℓν − M_W| > 15 Γ_W (30 GeV); the analytic Breit-Wigner tail beyond that is ≈ 2/(π·30) = 2.1 %, i.e. the same size as the observed deficit (combined −0.8 %, W⁻ −2.0 %).
Result: closure is good for W⁺ and consistent within ≈ 2 % overall; the W⁻ decayed-to-undecayed ratio is 2.0 % low (2.8σ with MG5's own error estimate, which may be underestimated for a 2→4 process). **The cause is not established**: a ≈ 2 % Breit-Wigner-tail truncation by the default `bwcutoff` would affect W⁺ equally, yet W⁺ closes at +0.04σ, so the tail argument is at best a partial explanation and may be a statistical effect. Conclusion: **BR closure PASS at the ±2 % level; the ledger uses the analytic B (narrow-width, no off-shell tail); a ±2 % normalisation uncertainty (narrow-width + bwcutoff) is carried as a nuisance on every ME-decayed W sample; the off-shell/narrow-width comparison (full ℓνHjj, QED=5) is deferred to Phase 04 as for ZH (S_EW_ZHjj_offshell).** ZH Z-closure was 1.0σ at 1.2 %.

## 6. VBF-like kinematics vs diagram labels; Higgsstrahlung-like V→jj
The signal is the complete (0,4) amplitude; "VBS/VBF-like" is a later *fiducial region* in observables (m_jj, Δη_jj, central W/H), not a diagram subset. Higgsstrahlung-like contributions at this order (qq̄' → W* → W H with V → qq̄ radiated or WWH/WZH with hadronic V) are **inside** the (0,4) sample. Evidence (LHE, undecayed light-flavour samples, 2000 events each, `scripts/lhe_vjj.py`): MG5 writes an intermediate hadronic W/Z resonance label in 14.7 % (W⁺) / 21.8 % (W⁻) of events; **288/293 (W⁺) and 433/436 (W⁻) of these have 65 < m_jj < 105 GeV, and 0/293, 0/436 are in the VBS-like region (m_jj > 500, |Δη_jj| > 2.5)**, which contains 1291 (W⁺) / 1100 (W⁻) events (64.6 % / 55 % of the sample at LHE level). So the resonant V→jj-labelled configurations are removed by the *observable* m_jj selection, not by a diagram veto; no separate WWH/WZH hadronic samples are added (they would double count). The VBS-like fraction at reco level after PY8+Delphes: 48 % of events with ≥2 reco jets (W⁺, 1000 ev). The interference/overlap between the V→jj-labelled and VBS-like configurations is inside the coherent sum.

## 7. QCD W±Hjj, definitions (a)/(b), and interference
- **Definition (a)**: signal = EW (0,4) W±Hjj only. QCD-induced W±H(+jets) is a resonant background: merged sample `H_QCD_WH_mlm` (W H + 0,1,2 j MLM, xqcut 10, PY8 qCut 19 as ZH; its 2-jet ME is the (2,2) amplitude, EW order excluded by coupling order) with fixed-order `H_QCD_WHjj_fixed` (σ = 57.81 ± 0.50 fb, W→ℓν both charges) only as VBS-region cross-check, never added. Inclusive LO W(→ℓν)H 0j σ = 280.3 ± 2.0 fb is the proxy for the matched σ (as ZH `zh_0j`; the MLM card's own pre-matching σ = 862 ± 9 fb is *not* the physical normalisation).
- **Definition (b)**: signal = EW + QCD + interference (all W H + 2 partons at tree level): σ_(b)/σ_EW = 1 + 4.30 − 0.0033 for W⁺ at loose cuts. The coherent sum is the sum of the three components (EW, QCD, interference are carried separately; closure by construction of coupling orders; a combined-process check is left to Phase 04).
- **Interference statement**: the signed EW×QCD cross term is −0.33 ± 0.02 % of EW (W⁺; −0.43 % both charges) at loose generator cuts, −0.06 % of EW+QCD. It is carried as a separate signed component (never as positive unweighted events) and assigned to the signal-model uncertainty unless |I|/S > 10 % after the VBS selection (then ask the human), as in ZH (−0.20 % after VBS cuts there). H-pole/γγ-continuum interference: no tree H→γγ vertex exists; the effect (O(1 %), mass shift O(100 MeV) in ggF literature) is a caveat, not modelled, as ZH.
- Other Higgs production modes producing a W: tHq/tHW/ttH are generated in Phase 02 with external tops; no overlap with the light-flavour signal by construction (section 3).

## 8. Commands and artefacts (all under the process dir)
`scripts/make_smoke_cards.sh`, `scripts/mg5_run_smoke.sh <card> <seed>` (σ-only, MG5 in node-local /tmp, staged to `work/smoke/<card>/`; derived from `lib/scripts/mg5_smoke.sh`, paths only), `scripts/run_smoke_batch1.sh`, `scripts/mg5_diag.sh` (generate+output only, counts), `scripts/lhe_classify.py`, `scripts/lhe_vjj.py`, `scripts/closure.py`, `scripts/br_ledger.py`, `scripts/validate_delphes.py` (Phase 03). All interactive runs ≤ 12 min wall, 4 cores, none a bulk generation.

## 9. Checks
Seed uniqueness within the run: asserted in `scripts/make_condor.py`. σ stability: independent seeds W⁻ (±0.3 %), PY8 vs LHE σ (−0.4 %). Cards parse and run (all `cards/smoke/*.mg5` returned rc=0). Orders validated by diagram counts (section 4). BR closure at ±2 % (section 5). Independent reproduction of WF: two code paths (analytic `br_ledger.py` and the MG5 σ ratio of the decayed vs undecayed samples).

## 10. Caveats
LO only; 5F-light external flavours (b-class non-top piece +5 % excluded, bounded); no CKM mixing, no heavy-quark Yukawas (sm-no_b_mass); on-shell W (narrow width, bwcutoff default 15); H→γγ is a forced decay with external BR, so Higgs-pole/continuum interference is not modelled; PDG W BRs include higher-order/QCD corrections absent from the MG5 tree widths and are applied only through the ratio WF; σ closure of the W⁻ chain is 2 % low. The intermediate-V labels are generator conventions.

## 11. Next actions
Phase 02 ledger (done in `02_background_overlap.md`); Phase 04: gridpack σ at higher precision, W⁻ closure repeat, combined-process (b) check, DJR validation of the MLM sample.
