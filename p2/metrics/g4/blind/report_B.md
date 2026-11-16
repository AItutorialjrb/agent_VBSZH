# WH Phase 01-03 reports, analysis B


<!-- ===== Phase report 01_signal_definition ===== -->

# Phase 01 — signal definition: EW W±Hjj, W→ℓν (ℓ=e,μ), H→γγ, √s = 13.6 TeV (WH, RUN)

Date UTC: 2026-11-03 (start 16:14 UTC, end see PROGRESS.md). **Status: PASS with open decisions (see STATUS.md D-WH-0…9)** (D-WH-1 seed-range overlap; none blocks Phase 02/03; see STATUS.md).
Author: analyst (MODEL), run RUN. Process dir: `/eos/home-r/rjiang/vbs_zh_codex_starter/RUNDIR/wh`. Frozen-ZH methodology: `reports/01_signal_process.md`, `03_generation_validation.md` (read-only).
All numbers below are LO MG5 cross sections with the MG5 integration error, **validation quantities, not yields**. No yield after selection is quoted in Phases 01-03.

## 1. Goal
Define the gauge-invariant EW W±Hjj signal (both charges), its decay implementation and BR ledger, the QCD W±Hjj resonant background (definition a) / inclusive variant (definition b), the interference statement, and separate VBF-like kinematics from diagram labels. Validate orders by MG5 diagram counts, subprocess lists and cross sections.

## 2. Inputs, versions, seeds
Stack as ZH (`lib/scripts/setup_stack.sh`): LCG_110 view, MG5_aMC 3.6.3 (upstream tarball, "UNKNOWN DEVELOPMENT VERSION" banner is a packaging marker, as in ZH 03_stack.md), Pythia 8.317 (CP5, dipole recoil on for EW samples), Delphes 3.5.1 slim CMS card (`delphes_card_CMS_slim_v1.tcl`), model `sm-no_b_mass` (5F, massless b/light quarks, diagonal CKM, no light Yukawas), PDF NNPDF31_nnlo_as_0118 (LHAID 303600), beams 6800+6800 GeV, scale choice 3 (½ Σ m_T), `use_syst` on. Jet generation cuts as ZH signal: pT(j)>20, |η(j)|<5, ΔR(jj)>0.4, ΔR(jℓ)>0.4, `cut_decays=False` (no cuts on W-decay leptons). Parameter card (generated): MW = 80.419 GeV (derived), MZ = 91.188, Gf = 1.16639e-5, 1/α = 132.507, WW = 2.0476 GeV (fixed), MH = 125, WH(MG5) = 6.38e-3 GeV (not used), MT = 173.
Seeds (SPEC 3.4): smoke runs P=2, R=x1, sample index 0 → 2x10001…2x10029 (listed per card in `scripts/run_smoke_batch{1,2}.sh`); PY8 validation seeds 2x10101-2x10103 (W⁺, W⁻, τν) (Delphes `RandomSeed` pinned by `run_py8_delphes.sh`). Git commit: recorded by analyst.

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
Diagnostic: the same W⁻ chain with `bwcutoff=1000` (seed 2x10029) gives 0.2989 ± 0.0051 (+37 %): this is *not* a closure test (it admits the off-shell W tail, non-resonant ℓνHjj) but shows the decay-chain σ depends on the Breit-Wigner cut. The default `bwcutoff=15` removes events with |m_ℓν − M_W| > 15 Γ_W (30 GeV); the analytic Breit-Wigner tail beyond that is ≈ 2/(π·30) = 2.1 %, i.e. the same size as the observed deficit (combined −0.8 %, W⁻ −2.0 %).
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


<!-- ===== Phase report 02_background_overlap ===== -->

# Phase 02 — background matrix and overlap ledger (WH, RUN)

Date UTC: 2026-11-03. **Status: PASS-with-conditions (ledger complete; B_EW_Waajj_vbs σ pending; G1 review items applied 2026-11-03). Open decisions D-WH-2 (infeasible N for double-fake samples), D-WH-3 (frozen ZH samples below the 50k floor), D-WH-4 (non-prompt-lepton backgrounds not negligible by arithmetic), D-WH-5 (WZγ-type e→γ/lost-lepton components unquantified), D-WH-7 (mmjj>400 generator cut on every VBS-biased sample incl. frozen ones; EW twins missing), D-WH-8 (τ treatment), D-WH-9 (untested sample types, tt̄γγ double counting).** Several gridpack cross sections were still being computed when this report was written; the table is regenerated by `python3 scripts/build_sample_matrix.py` (reads `work/smoke`, `work/gridpacks`) and the live version is `config/sample_matrix.yaml`.
Inputs: Phase 01 (`01_signal_definition.md`), frozen ZH `reports/02_background_overlap.md`, `FINAL_report.md`, `lib/config/sample_matrix_phase02.yaml`, `lib/cards/production_{v2,final}`. Versions/seeds as Phase 01 (stack unchanged). Git commit: recorded by analyst.

## 1. Final state and measurement definition
Reco target: one isolated e/μ (W→ℓν), MET, ≥2 isolated photons with m_γγ in the Higgs window (sidebands reserved, Phase 06), ≥2 VBS tag jets, b-veto (top). **Signal = EW (0,4) W±Hjj (light external flavours, W→e/μ in ME, plus the τ feed-down as a separate signal-like component).** Everything with a resonant m_γγ peak that is not EW W±Hjj is a *resonant background* and is fitted with the signal shape; continuum (prompt γγ, fake γ) is constrained by m_γγ sidebands.

## 2. Ledger (full machine-readable version: `config/sample_matrix.yaml`; N rule N_req = max(50k, σ·k·3000 fb⁻¹), SPEC 4.2)
| ID | role | σ_MG [fb] (source) | k = ext. BR factors | σ·k [fb] | N_required | N planned / avail. | flag / generator-cut C |
|---|---|---|---|---|---|---|---|
| S_EW_WHjj | signal (def a: EW only) | 13.77 (gridpack init sigma) | WF×BGG=0.0021794 | 0.03001 | 50000 | 200000 |  |
| S_EW_WHjj_taunu | signal-like feed-down (W->tau nu->l nu nu) | 6.71 (SMOKE RUN) | WFTAU×BGG=0.0023244 | 0.0156 | 50000 | 100000 |  |
| H_QCD_WH_mlm | resonant bkg (def a) / signal component of d | 302.3 (condor test job H_QCD_WH_mlm_s2113) | WF×BGG=0.0021794 | 0.6588 | 50000 | 1000000 |  |
| H_QCD_WHjj_fixed | cross-check only (VBS-region efficiency) | 57.81 (SMOKE RUN) | WF×BGG=0.0021794 | 0.126 | 50000 | 100000 |  |
| I_WHjj | signed EW x QCD interference (def b); sigma  | -0.2644 (SMOKE RUN) | BR_WLL×BGG=0.00048442 | -0.0001281 | 50000 | 50000 |  |
| H_ttH_1l | resonant bkg | 107.8 (gridpack init sigma) | WF×WHAD×BGG=0.0022032 | 0.2375 | 50000 | 200000 |  |
| H_tHq_lep | resonant bkg | 14.88 (SMOKE RUN) | WF×BGG=0.0021794 | 0.03243 | 50000 | 100000 |  |
| H_tHW_1l | resonant bkg | 4.668 (SMOKE RUN) | WF×WHAD×BGG=0.0022032 | 0.01028 | 50000 | 100000 |  |
| T_tta_1l | 1 fake gamma (+ prompt gamma) | 511.2 (SMOKE RUN) | WF×WHAD=0.97056 | 496.1 | 1488444 |  |  |
| T_ttaa_1l | irreducible prompt | 0.5709 (SMOKE RUN) | WF×WHAD=0.97056 | 0.5541 | 50000 |  |  |
| T_tWa_1l | 1 fake gamma | 77.87 (SMOKE RUN) | WF×WHAD=0.97056 | 75.58 | 226731 |  |  |
| T_tt_1l | 2 fake gammas (bound) | 1.417e+05 (SMOKE RUN) | WF×WHAD=0.97056 | 1.375e+05 | 412583100 |  | D-WH-2 (N>feasible) |
| B_EW_Waajj_vbs | irreducible continuum (EW) | pending (gridpack init sigma if available e) | WF=0.96008 | pending | pending |  | C unquantified |
| B_QCD_Waajj_vbs | irreducible continuum (QCD) | 0.6327 (gridpack init sigma) | WF=0.96008 | 0.6074 | 50000 |  | C=1.91 |
| B_QCD_Waajj_nomjj | aux twin (ratio C only) | 3.582 (gridpack init sigma) | WF=0.96008 | 3.439 | 50000 |  |  |
| F_EW_Wajj_vbs | 1 fake gamma (EW) | 89.63 (gridpack init sigma) | WF=0.96008 | 86.05 | 258155 |  | C unquantified |
| F_QCD_Wajj_vbs | 1 fake gamma (QCD) | 712.4 (gridpack init sigma) | WF=0.96008 | 684 | 2051875 |  | C=1.59 |
| F_QCD_Wajj_nomjj | aux twin (ratio C only) | 5683 (gridpack init sigma) | WF=0.96008 | 5456 | 16368344 |  |  |
| F_Wjj_pilot | 2 fake gammas (bound) pilot | 3.435e+06 (gridpack init sigma) | WF=0.96008 | 3.298e+06 | 9893588253 |  | D-WH-2 (N>feasible) |
| F_Wajj_pilot | 1 fake gamma pilot | 9878 (gridpack init sigma) | WF=0.96008 | 9484 | 28450907 |  | D-WH-2 (N>feasible) |
| ZH_EW_ZHjj_lostlep | ZHjj EW, Z->ll, 1 lepton lost | 1.295 (FINAL_report.md table) | ZF×BGG=0.0022207 | 0.002876 | 50000 | 200000 |  |
| ZH_QCD_ZHjj_lostlep | ZHjj QCD (2,2), Z->ll, 1 lepton lost | 10.21 (FINAL_report.md table) | ZF×BGG=0.0022207 | 0.02267 | 50000 | 100000 |  |
| ZH_ggZH_lostlep | ggZH loop, Z->ee/mumu (PY8), 1 lepton lost | 74.33 (FINAL_report.md table) | BR_ZLL×BGG=0.00015276 | 0.01135 | 50000 | 20000 | D-WH-3 |
| ZH_ttH_dilep_lostlep | ttH dilepton, 1 lepton lost | 18.11 (FINAL_report.md table) | WF×WF×BGG=0.0020924 | 0.03789 | 50000 | 42000 | D-WH-3 |
| ZH_Zaajj_EW_lostlep | Zgg jj EW (on-shell Z->ll), 1 lepton lost | 0.0393 (FINAL_report.md table) | ZF=0.9783 | 0.03845 | 50000 | 60000 | C unquantified |
| ZH_Zaajj_QCD_lostlep | Zgg jj QCD (on-shell Z->ll), 1 lepton lost | 0.0356 (FINAL_report.md table) | ZF=0.9783 | 0.03483 | 50000 | 100000 | C=1.91 |
| ZH_Zajj_eFake | Z(ll)gamma jj with e->gamma (QCD+EW), lepton | 80.51 (FINAL_report.md table) | one=1 | 80.51 | 241530 | 6489548 | C=1.59 |

σ_MG = generator σ after the decay in the ME (fb, LO, before external BR); k = factors applied once externally (WF = 0.96008, WFτ = 1.0240, WHAD = 1.0109, B_γγ = 0.002270, ZF = 0.9783; `scripts/br_ledger.py`, asserts single application). Rows prefixed `ZH_` are frozen zh-final-v1.1 samples (read-only reuse, Delphes-level, paths in the YAML). Planned N values are the Phase-04 proposal (≥ N_req); estimates are labelled ESTIMATE and never used as yields.

| Component (physics) | Treatment | Why |
|---|---|---|
| EW/QCD Wγγjj (prompt, irreducible) | B_EW_Waajj_vbs, B_QCD_Waajj_vbs (+ twin nomjj), on-shell W→ℓν chain, ZH-final-style VBS-biased cuts | same recipe as ZH final (Zγγjj) |
| Wγ+jets, jet→γ fake | F_EW_Wajj_vbs, F_QCD_Wajj_vbs (+ twin), direct Delphes photon objects **and** parametrised f(j→γ) scenarios (ZH: Delphes fakes are reported, not trusted) | |
| W+jets, two fakes | bound from fake-factor pilot F_Wjj_pilot (Phase 03, 5000 events) | σ(W+2j) = 3.4×10⁶ fb: N ≥ σ·L infeasible, D-WH-2 |
| tt̄γ, tt̄γγ, tWγ (single-lepton) | T_tta_1l, T_ttaa_1l, T_tWa_1l (ZH closeout convention: tt̄γ/tWγ not overlap-removed, bound by T_ttaa_1l) | N for T_tta_1l ≈ 1.5M (feasible, as ZH 1.04M) |
| tt̄ (single lepton, two fakes) | T_tt_1l σ = 1.4×10⁵ fb. **No pilot was run: unquantified**; arithmetic ESTIMATE in §5 (≈ 0.01 events nominal, 0.001-0.09 over the f scenarios, ε assumed). Needs a pilot or approval of the estimate: D-WH-2 | |
| tt̄H, tHq, tHW | H_ttH_1l, H_tHq_lep, H_tHW_1l (single-lepton configurations, W decays in ME); frozen ZH_ttH_dilep_lostlep for the dilepton lost-lepton part | |
| ZHjj / ggZH with one lost lepton | frozen ZH EW/QCD ZHjj, ggZH | coverage checked in §3 |
| Zγγjj with one lost lepton | frozen ZH B_EW/B_QCD Zaajj | coverage checked in §3 |
| Zγjj with e→γ | frozen F_*_llajj_vbs (partial, §3) | |
| W→τν H feed-down | S_EW_WHjj_taunu | in signal definition (Phase 01) |
| QCD W±H+jets (def a bkg) | H_QCD_WH_mlm (+ fixed-order cross-check) | |
| EW×QCD interference | I_WHjj σ only, **negative (computed sign, not structural)**: σ_I = −0.264 ± 0.013 fb undecayed (both charges; −0.43 ± 0.02 % of EW). Enters s/b only as a signed signal-model systematic (±|I|/S on the signal, never as events in b); revisited with VBS cuts in Phase 04 (if |I|/S > 10 % ask the human) | |
| QCD γγ+jets, non-prompt lepton; ggF/VBF H with non-prompt lepton | **bound, §5; D-WH-4** | |
| WZγ/WWγ/ZZγ (lost lepton, e→γ) | **unquantified, D-WH-5** | ZH attempts at WZγ/ZZγ failed at generation (setcuts grouping error, compile time) |

## 3. Reuse of frozen ZH samples: coverage of the generation phase space (checked explicitly)
Cards read from `lib/cards/` and, for Zγγjj, the run_card inside the production gridpack (`madevent/Cards/run_card.dat` of `B_EW_zaajj_vbs_is2_gridpack_s1363800.tar.gz`).
- **ZHjj EW and QCD (Tier-1 v1; cards `phase03_smoke/{ew,qcd}_zhjj_zll.mg5`)**: Z→ℓℓ in the ME with `cut_decays=False`; only jet cuts (pT>20, |η|<5, ΔR(jj)>0.4) apply, **no cuts on the leptons**: a lost lepton (acceptance, ID, isolation) is fully covered. Both leptons are in the final-state record at Delphes level. Covered. N = 200k (EW), 100k (QCD).
- **ggZH (final/H_ggZH_py8dec)**: Z and H decayed in PY8, ptj>0: covered; N = 20000 < 50k floor → D-WH-3.
- **ttH dilepton (final/H_ttH + test_v2)**: t→bℓν both in ME, `cut_decays=False`, no jet cuts: covered (lost lepton); N = 42000 < 50k → D-WH-3. Ledger difference: the ZH analysis used k = B_γγ (MG tree W BR, "one"); applying the physical W BR needs WF² = 0.9218 (−7.8 %); here the WH ledger uses WF²·B_γγ (documented, not silent).
- **Zγγjj EW/QCD (final/B_*_zaajj_vbs, on-shell Z→ℓℓ chain)**: run_card: `cut_decays=False` (so ptl/etal/mmll do **not** act on the decay leptons → lost leptons covered), but **pta>25, |η_γ|<2.5, 100<m_γγ<170, mmjj>400, ptj>20, |η_j|<5, ΔR>0.4 do apply**. These are binding constraints on the WH baseline: photon pT>25 (offline, with margin for resolution), reco m_γγ window ⊂ [100,170], reco m_jj well above 400 (ZH found the m_jj>500 cut safe at 1.4 % for EW-type and unsafe, 64 %, for QCD-type samples; the twin-sample demonstration for W is in Phase 03 §5 and must be repeated with the final cuts). N = 3×20k (EW), 100k (QCD).
- **Zγ+jets with e→γ (F_*_llajj_vbs; ℓℓ in ME)**: ptl>10, |η_ℓ|<2.5, mmll>50 apply to both leptons ⇒ a lepton outside the acceptance is **not** covered: partial coverage only (documented; e→γ with the lepton in acceptance is covered; N = 6.49M).
- **Z→ττ, Z→νν H(+jets)**: Z→νν has no lepton (needs a non-prompt lepton: ESTIMATE in §5, ≈ 6×10⁻⁵ events nominal, 6×10⁻⁴ high; assumed ε); ZH(Z→ττ) lost-lepton feed-down is covered by frozen `H_ZH_tautau` (N = 6565 = final + test_v2 per FINAL_report, <50k, D-WH-3 if it survives selection).
**Generator-cut correction (G1 item 2).** All frozen VBS-biased samples (Zγγjj, Zγjj) were generated with mmjj>400, which is not safe at the WH working point for QCD-type samples (twins, 03 §7: 47.6 ± 5.5 % / 37 ± 9 % of reco-selected events lost). They therefore **cannot** be used as generated: the QCD-type ones carry a yield multiplier C = 1/(1−f): `ZH_Zaajj_QCD_lostlep` C = 1.91 (+0.24/−0.20) and the QCD part of `ZH_Zajj_eFake` C = 1.59 (+0.30/−0.20), both **proxies from the W twins** (ZH needed C = 2.37 at its own selection) to be re-derived with a twin at the final WH selection; own samples `B_QCD_Waajj_vbs` C = 1.91, `F_QCD_Wajj_vbs` C = 1.59. EW-type samples (`ZH_Zaajj_EW_lostlep`, `B_EW_Waajj_vbs`, `F_EW_Wajj_vbs`): **no twin for W exists, C unquantified** (ZH: 1.4 % at its selection, placeholder only). C and its source are columns of `config/sample_matrix.yaml` (`c_gen_cut`) and of the table in §2. No yield is quoted here; the multiplier must be applied in Phase 05, and the missing twins generated: **D-WH-7**. The remaining coverage statements (lepton cuts) above stand. Otherwise frozen samples enter b only through the Delphes-level WH selection applied to their reco objects, so no re-generation is needed where coverage is "covered", N ≥ N_req and C is applied.

## 4. Overlap-removal contract (hard/soft photons), generator-cut safety
Same partition-of-phase-space rule as ZH (02 §3), with the GenTruth `n_prompt_photons` (status-1 photon with no hadron in its ancestry, pT>15, |η|<2.5, ΔR>0.4 to prompt leptons pT>10 / other prompt photons) produced in-job by the reused `slim_gentruth.py`:
1. W+jets-type samples (F_Wjj) keep N_prompt = 0; Wγ(+jets) keeps N_prompt ≤ 1 (≥2 → covered by B_*Waajj); Wγγ keeps N_prompt ≥ 2. Residual migration in 15<pT<25 GeV (the B samples are generated with pta>25) is measured on the twins in Phase 04 (as ZH).
2. Shower QED emission on in all samples (PY8 default). Fake-photon pT = x·pT(jet), x~N(0.85,0.10) (unchanged from ZH).
3. tt̄γ/tWγ: **no** overlap removal (ZH closeout: the second "prompt" photon is mostly radiated by top-decay products that the decay-chain tt̄γγ ME lacks; removal discarded 87 % of the selection). Double counting with T_ttaa_1l is bounded by the full T_ttaa_1l yield: σ_MG = 0.571 fb, σ·k = 0.554 fb, i.e. **≈ 19× the signal σ_phys (0.0297 fb) before selection — not negligible a priori**; its size after lepton/γγ/VBS/b-veto selection is not yet computed (Phase 05; needs T_ttaa_1l and T_tta_1l test/production events) and a human choice between "no removal, bound by T_ttaa_1l" and a removal scheme is open: D-WH-9.
4. EW vs QCD by coupling order (diagram counts Phase 01 §4); interference separate and signed.
5. Generator-level cut safety by **twin samples** (as ZH A1): `B_QCD_Waajj_nomjj`/`F_QCD_Wajj_nomjj` (mmjj=0) vs the `*_vbs` samples (mmjj=400); safety = fraction of reco-selected (m_jj>500, Δη>2.5 + γγ + lepton) twin events whose generator m_jj < 400. Gridpacks and one test job per twin are in flight (clusters in STATUS.md); the first numbers are in `03_generation_validation.md` §5; the conclusion is deferred to Phase 04/05 with production-size twins (as in ZH: EW-type safe, QCD-type not safe and corrected by the ratio C with its MC-stat uncertainty).

## 5. Quantitative ESTIMATES for components without MC support (never "zero"; assumed efficiencies, not rigorous bounds)
Parameterised, **not data-driven**: jet→γ f = 10⁻³(pT/50)^−0.5 (×2 endcap) × {0.3, 1, 3}; e→γ 1–5 %; non-prompt lepton per jet {3×10⁻⁵, 10⁻⁴, 10⁻³} (ZH `fake_scenarios`, ranges unchanged; the data-driven range is a Phase 06 systematic).
- **W+jets, 2 jet→γ fakes and Wγ+jets, 1 fake**: the pilot fake-factor analysis (`scripts/fakefactor_pilot_w.py`, patch 001) on 5000 events of F_Wjj_pilot/F_Wajj_pilot is reported in `03_generation_validation.md` §6; lower bounds because only 2 partons are in the ME.
- **Non-prompt lepton backgrounds** (`scripts/bounds.py`, `work/bounds.txt`; arithmetic with stated assumptions, not MC):
```
component                                                        sigma_fid[fb]       low   nominal      high
QCD gamma gamma + jj (LO MG5, pTg>25, 100<mgg<170, ptj>20)                3542    0.0744     0.248      2.48   | smoke Q_aajj_smoke: 3.542 pb (LO, no K-factor, fixed 2 jets)
ggF H->gg (+jets)   [YR4 13 TeV 48.58 pb x1.1 = 53.4 pb]                 121.2   0.00164   0.00545    0.0545   | YR4 x 1.1 scaling (as ZH); eps_VBS from ggF+2j fraction (assumed 1e-2)
ZH, Z->nunu, H->gg [LO ZH 704 fb (ZH zh_0j 48.45 fb / 0.06878) x B(inv)=0.200 x B_gg]        0.3196  1.73e-05  5.75e-05  0.000575   | LO sigma from the ZH smoke run; eps_VBS assumed 1e-2; genuine MET (eps_MET 0.8)
VBF H->gg           [YR4 13 TeV 3.78 pb x1.1 = 4.16 pb]                  9.443   0.00382    0.0127     0.127   | YR4 x 1.1 scaling; extra (non-tag) jet fraction 0.3 assumed
ttbar 1l, 2 jet->gamma fakes (15 jet pairs, f0=1e-3, eps_pT .5, window .02, VBS .01, b-veto .1)     1.375e+05  0.000928    0.0103    0.0928   | f scenarios x{0.3,1,3} per photon -> x{0.09,1,9}; sigma = smoke T_tt_1l_smoke 141.7 pb x k; eps ASSUMED
```
 The QCD γγ+jj estimate (0.07 / 0.25 / 2.5 events at 500 fb⁻¹ in the m_γγ peak window after the illustrative VBS+MET cuts; **the efficiency factors ε_VBS (0.10/0.01…), ε_MET = 0.2, ε_window = 0.14 and the extra-jet fractions are assumptions, not validated by MC**; "high" = f ×10 over nominal and is not an envelope) is of the same order as the expected signal (σ_phys 0.0297 fb = 14.9 events before acceptance; ZH-like acceptance ≈ 6 % gives ≈ 0.9 events) in the nominal and exceeds it in the high scenario; ggF/VBF H are smaller but not <10⁻² in the high scenario. **Therefore these components cannot be declared negligible (unlike ZH, where the Z-mass window removes them): D-WH-4.** Proposed remedy (needs human approval of compute and the f_ℓ range): dedicated γγ+jets (VBS-biased) and VBF/ggF H+jets samples with parametrised non-prompt-lepton weights on reco jets, N_eff ≥ 10 in the SR, or report the Phase-05 sensitivity with the bound as an explicit extra background (conservative variant).
- **tt̄ (1ℓ) with two jet→γ fakes and Z→νν H**: rows in the table above (ESTIMATES, assumed ε; no MC). tt̄ ≈ 0.01 events nominal (0.001-0.09); ZH(Z→νν) ≈ 6×10⁻⁵ (nominal), negligible only under these assumptions. The tt̄ row stays **unquantified** until a pilot is run (D-WH-2).
- **WZγ/WWγ/ZZγ and W/Z γγ with e→γ**: cross sections not available (ZH could not integrate `wza`/`zza`); no bound is claimed. D-WH-5: generate with `group_subprocesses False` on batch in Phase 04 or provide an analytic bound.

## 6. N_MC feasibility (SPEC 4.2): flagged items
- Infeasible (σ·k·3000 > 2×10⁷ events, storage ≈ 2.4 kB/event ⇒ >50 GB each): `F_Wjj_pilot` (σ·k·L ≈ 9.8×10⁹), `T_tt_1l` (4.1×10⁸), `F_Wajj_pilot` fixed 2-parton σ (2.8×10⁷; the production Wγ sample is the VBS-biased `F_QCD_Wajj_vbs`, pending σ). **D-WH-2**: use the bound method above (parameterised fake weights on a generator-filtered/VBS-biased sample with N_eff ≥ 10 and the conservative upper-bound variant in the robustness table), as the handoff effective-N policy (§5.3) is declared only for HH; this is an extension of that policy to the WH double-fake backgrounds and needs approval.
- Frozen ZH samples below the 50k floor: `ZH_ggZH_lostlep` (20000), `ZH_ttH_dilep_lostlep` (42000), `H_ZH_tautau` (6565). **D-WH-3**: top up in Phase 04 (cheap: ≈ 30 core-h) or accept with N_eff in the SR.
- All other rows satisfy the rule or are pending a gridpack σ (the floor 50k dominates unless σ·k > 16.7 fb).

## 6b. τ feed-down and radiative W decays (G1 item 8)
`S_EW_WHjj_taunu` (W→τν→ℓ, σ_MG = 6.71 fb, k = 2.324×10⁻³) is, by the handoff definition (W→eν/μν), **not signal**: it is kept as a separate resonant component of b ("other H→γγ"); including it in s would be a deviation to be approved (D-WH-8). Conversely, **all background cards decay W to e/μ only** (B_*, F_*, T_*, H_*): τ feed-down in backgrounds is not generated. Size: B(W→τν)·B(τ→ℓνν)(≈0.352) ≈ 0.0401 vs B(W→e,μ) = 0.2134, i.e. **+18.8 % on the lepton-channel yield of every W-lepton background** (smaller after the lepton pT>25 cut), not applied; options in D-WH-8: apply the ratio as a normalisation uplift with ±100 % uncertainty, or generate τ in the cards. W→ℓνγ radiative photons are excluded from the on-shell chain B/F cards (not in the ME) and are a caveat; PY8 QED shower photons off leptons are included.

## 6c. Combination with ZH (handoff §5.4) — conventions that differ
(i) frozen ZH ttH (dilepton) used k = B_γγ (MG tree W BR) in ZH but WF²·B_γγ here (−7.8 %); (ii) ZH's QCD VH background is fixed-order ZHjj (2,2) (`H_QCD_ZHjj`), WH's is MLM-merged W H+0,1,2j (matched σ 302 fb vs 0j proxy 280 fb); (iii) ZH ledger applied k = 1 to tt̄γ/tWγ. The theory-nuisance correlation groups for the shared samples (ttH, tHW, ggZH) and the choice of one consistent convention must be fixed before the combination (Phase 07/combination); not decided here.

## 7. Checks
Table built by code (`scripts/build_sample_matrix.py`) with the BR ledger assertions (no BR applied twice) and the N rule; frozen coverage verified from actual run cards; diagram counts for the continuum cards (B_EW_Waajj_vbs 44 subprocesses / 20520 diagrams, B_QCD_Waajj_vbs 52/6984, F_EW_Wajj_vbs 44/2700, F_QCD_Wajj_vbs 52/1024; `work/diag/`).

## 8. Caveats and next actions
LO σ (K-factors not applied; shown only for sizing). ESTIMATE-labelled σ (continuum) are replaced by gridpack σ as they arrive. Next: Phase 03 test jobs (one per sample type), check audit, then G1 review of D-WH-2…5 before any Phase-04 production.


<!-- ===== Phase report 03_generation_validation ===== -->

# Phase 03 — generator smoke tests, σ/BR closure, Delphes validation, condor test jobs (WH, RUN)

Date UTC: 2026-11-03. **Status: IN-PROGRESS (interactive validation PASS; 8 of the 20 registered samples have a finished test job (test-job coverage is therefore NOT "one per sample type"), namely S_EW_WHjj, H_ttH_1l, H_QCD_WH_mlm, F_Wjj_pilot, F_Wajj_pilot, F_QCD_Wajj_nomjj, B_QCD_Waajj_vbs, B_QCD_Waajj_nomjj. **Untested sample types (no test job, G1 item 9):** T_tta_1l, T_ttaa_1l, T_tWa_1l, T_tt_1l, H_tHq_lep, H_tHW_1l, S_EW_WHjj_taunu, F_EW_Wajj_vbs, F_QCD_Wajj_vbs, H_QCD_WHjj_fixed, I_WHjj (σ-only; no events needed); their cards ran as σ-only smoke tests (rc 0) and F_*_Wajj_vbs/F gridpacks built, but the PY8+Delphes chain is exercised only through the tested types (top-type: H_ttH_1l is the representative). Decision D-WH-9. MISSING for PASS: the EW Wγγjj gridpack B_EW_Waajj_vbs (cluster 884456.3, running ≈ 5 h; sibling QCD gridpacks needed 4.6-4.8 h with 6984 diagrams, EW has 20520) and its test job 884457.3; an EW-type twin; check audit of the new jobs).** Git commit: recorded by analyst.
Stack, versions, model, PDFs: as Phase 01 (LCG_110, MG5 3.6.3 upstream, Pythia 8.317 CP5, Delphes 3.5.1 slim CMS card, NNPDF31_nnlo_as_0118). Seeds: SPEC 3.4 (P=2, R=x1): smoke = sample index 0 (2x10001-2x10031), gridpacks J=0, test jobs J=1, with 1000×idx from `config/sample_registry.yaml`; uniqueness asserted in `scripts/make_condor.py` (print of all seeds in the run log). **D-WH-1:** the SPEC formula J+1000·idx exceeds the R spacing (10⁴) for idx ≥ 10 (max here 20001), so seed *numbers* of RUN can coincide with those of RUN/r3 (different samples, hence not a physics problem, but not unique across runs); uniqueness is asserted only within this run. Proposed fix: R spacing 10⁵.

## 1. Smoke tests: σ (all interactive, ≤ 12 min wall, 4 cores, no bulk)
All cards in `cards/smoke/` (`scripts/make_smoke_cards.sh`, `scripts/make_prod_cards.sh`), runner `scripts/mg5_run_smoke.sh` (patch 000), logs/banners/LHE under `work/smoke/<card>/`. Gen cuts: WH/ZH-like jets pT>20, |η|<5, ΔR(jj)>0.4, `cut_decays=False`; photons as listed in the YAML. LO MG5 σ in fb with the integration error:
| card | seed | σ [fb] (MG5 LO, integration err) | wall [s] |
|---|---|---|---|
| F_Wajj_pilot_smoke | 2x10022 | 9616 ± 63 | 202 |
| F_Wjj_pilot_smoke | 2x10021 | 3.411e+06 ± 2.6e+04 | 174 |
| H_QCD_WH_0j_smoke | 2x10028 | 280.3 ± 2 | 65 |
| H_QCD_WH_mlm_smoke | 2x10023 | 862.1 ± 9.3 | 185 |
| H_QCD_WHjj_fixed_smoke | 2x10024 | 57.81 ± 0.5 | 144 |
| H_tHW_1l_smoke | 2x10016 | 4.668 ± 0.035 | 89 |
| H_tHq_lep_smoke | 2x10015 | 14.88 ± 0.15 | 85 |
| H_ttH_1l_smoke | 2x10014 | 108.3 ± 0.5 | 81 |
| I_WHjj_smoke | 2x10025 | -0.2644 ± 0.013 | 120 |
| Q_aa_0j_smoke | 2x10030 | 4774 ± 48 | 64 |
| Q_aajj_smoke | 2x10031 | 3542 ± 29 | 99 |
| S_EW_WHjj_smoke | 2x10012 | 13.63 ± 0.18 | 121 |
| S_EW_WHjj_taunu_smoke | 2x10013 | 6.71 ± 0.11 | 141 |
| T_tWa_1l_smoke | 2x10019 | 77.87 ± 0.61 | 82 |
| T_tt_1l_smoke | 2x10020 | 1.417e+05 ± 9.9e+02 | 86 |
| T_tta_1l_smoke | 2x10017 | 511.2 ± 3.4 | 154 |
| T_ttaa_1l_smoke | 2x10018 | 0.5709 ± 0.0047 | 398 |
| wm_light_nodec | 2x10002 | 23.66 ± 0.16 | 112 |
| wm_light_nodec_rep | 2x10027 | 23.59 ± 0.35 | 109 |
| wm_light_wdec | 2x10006 | 5.15 ± 0.03 | 119 |
| wm_light_wdec_bw | 2x10029 | 7.069 ± 0.11 | 681 |
| wm_light_wdec_rep | 2x10026 | 5.152 ± 0.033 | 101 |
| wp_b_nodec | 2x10003 | 82.75 ± 0.46 | 136 |
| wp_bnot_nodec | 2x10004 | 178.6 ± 1.4 | 738 |
| wp_int_nodec | 2x10009 | -0.1253 ± 0.0083 | 88 |
| wp_light_nodec | 2x10001 | 38.4 ± 0.2 | 101 |
| wp_light_wdec | 2x10005 | 8.538 ± 0.043 | 120 |
| wp_qcd_nodec | 2x10007 | 165.2 ± 0.84 | 98 |

Reading the table: σ(W⁺Hjj EW light) = 38.40, W⁻ = 23.65 fb; b-inclusive and `/ t t~` variants: Phase 01 §3 (gauge-invariance evidence). Q_aa_0j/Q_aajj are used for the non-prompt-lepton bound (Phase 02 §5). `H_QCD_WH_mlm_smoke` (862 fb) is the *pre-matching* sum and is not a physical σ (matched: 302.3 ± 5.3 fb, §4).

## 2. σ closure (smoke vs gridpack vs LHE vs Pythia)
| sample | smoke σ [fb] | gridpack init σ [fb] | LHE (test job) | PY8 σ |
|---|---|---|---|---|
| S_EW_WHjj (W±→ℓν) | 13.63 ± 0.18 | 13.77 ± 0.037 (+1.0 %) | first process line only (multi-process LHE; sum in PY8) | 13.68 (−0.7 % vs gridpack) |
| H_ttH_1l | 108.3 ± 0.50 | 107.8 ± 0.31 (−0.5 %) | | 107.8 (0.0 %) |
| F_Wjj_pilot | 3.411×10⁶ ± 2.6×10⁴ | 3.435×10⁶ ± 7.6×10³ (+0.7 %) | | 3.413×10⁶ (−0.6 %) |
| H_QCD_WH_mlm | 862 ± 9 (pre-matching) | 879.6 ± 4.2 (pre-matching) | | 302.3 ± 5.3 (after MLM; accepted 1386/4000 = 34.6 %, ratio 0.344 consistent) |
Gridpack-vs-smoke closure at ≤ 1 % where both exist (statistical at the error level). Gridpack σ for the continuum cards: see the live matrix. In `config/sample_matrix.yaml` the gridpack init σ is used wherever a gridpack exists (S_EW_WHjj 13.77, H_ttH_1l 107.8, F_Wjj 3.435×10⁶, F_Wajj_pilot 9878 ± 19 fb); smoke-run σ remain, labelled "SMOKE RUN", only where no gridpack σ exists yet; H_QCD_WH_mlm uses the matched PY8 σ.

## 3. BR closure and decay implementation
- **B(H→γγ) inside Pythia8**: the PY8 particle data table (log of every validation job) lists B(25→γγ) = 0.002298 (NLOWidths on) vs the ledger value 0.002270 (YR4): +1.2 %. The forced decay makes the conditional BR 1 and PY8 does not fold it into σ; the ledger value 0.002270 is applied once, externally, and the PY8-internal 0.002298 is **not** used for any normalisation (same as ZH).
- **W→ℓν (MG5 chain)**: σ_dec/σ_undec = 0.2223 ± 0.0016 (W⁺, pull +0.04), 0.2178 ± 0.0016 (W⁻, −2.76σ, two seeds), 0.2206 ± 0.0012 combined (−1.4σ), τν 0.1081 ± 0.0018 vs 0.1111 (−1.7σ); the deficit is the size of the BW tail removed by the default `bwcutoff` (≈2 %) — details, WF = 0.9601, WFτ, WHAD derivation in `01_signal_definition.md` §5 and `scripts/br_ledger.py`. **PASS at ±2 %.**
- **H→γγ (PY8 forced)**: last-copy H→γγ in 1000/1000 (W⁺), 1000/1000 (W⁻), 500/500 (τν), 2000/2000 (condor test S_EW_WHjj) events, 0 other; PY8 σ equals the LHE/gridpack σ (no BR folded in): the physical B_γγ = 0.002270 enters once via the ledger (`k`). **PASS.**
- **Ledger assertion**: `scripts/br_ledger.py` raises on a doubly applied BR and `nmc_check()` implements max(50k, σ·k·3000) (self-test printed in the script's `__main__`).
- W→τν→ℓ: 500/500 last-copy W→τν; 14 % of events have ≥1 reco e/μ (τ→ℓ BR × acceptance).

## 4. Delphes object validation (slim CMS card, 1000-2000 events, validation only; `scripts/validate_delphes.py`, `work/py8chk/*/validation.json`, plots `validation.png`)
| quantity | W⁺→ℓν (1000 ev, seed 2x10101) | W⁻→ℓν (1000, 2x10102) | S_EW_WHjj condor test (2000, seed 2x11001) |
|---|---|---|---|
| gen H→γγ / W→e,μ record | 1000 / (508 e, 492 μ) | 1000 / (501, 499) | 2000 / (1028, 972) |
| muon reco efficiency (gen pT>25, \|η\|<2.5, ΔR<0.2) | 0.809 ± 0.021 | 0.811 | 0.815 ± 0.015 |
| electron reco efficiency (same) | **0.590 ± 0.026** | 0.609 | 0.620 ± 0.018 |
| MET: σ68(Δ_x), σ68(Δ_y) vs GenMissingET [GeV] (gen MET>30) | 15.5, 17.4 | 16.5 | 16.4, 16.3 |
| MET median reco / gen [GeV]; median relative bias | 53.5 / 48.3; +2.8 % | | 53.1 / 47.7; +2.5 % |
| ≥2 reco γ (pT>20, \|η\|<2.5 excl. crack) | 0.457 | | 0.467 |
| m_γγ median / σ68 (100-150) [GeV]; frac. 120-130 | 124.84 / 2.25; 0.91 | 124.94 / 2.27 | 125.02 / 2.05; 0.91 |
| ≥2 jets (pT>25, \|η\|<4.7) | 0.928 | | 0.927 |
| m_jj σ68 of reco/gen−1 (matched leading two, gen m_jj>300) | 7.8 % | 8.9 % | 7.6 % |
| frac. m_jj>500 & Δη_jj>2.5 (≥2 jets) | 0.484 | | 0.463 |
Same Delphes electron deficit as ZH (35 % vs 64 % there for pairs; per-lepton 59-62 % here vs 81 % for muons: the stock card isolation/UniqueObjectFinder ordering; carried to Phase 04 as in ZH D11). m_γγ resolution σ68 ≈ 2.1-2.3 GeV (ZH 2.1) and jet m_jj resolution 8 % (ZH 8.8 %) agree. The lepton efficiency uses the W-daughter lepton before FSR (includes isolation losses).

## 5. HTCondor test jobs (8 of 20 samples, see status line; wrappers `lib/scripts/condor/{make_gridpack.sh,run_job.sh}` reused unmodified; submit files generated by `scripts/make_condor.py`; EOS stage-out; `condor_q` checked for duplicates before each submission)
Submission (cluster 884860: one extra test job for B_QCD_Waajj_vbs, `work/condor/test_wh_bqcd.sub`, submitted after confirming no existing job/output; the continuum type was otherwise only represented by the still-building EW gridpack). Hold/release audit: `work/condor/test_wh.log` shows exactly one termination (005) per test proc (6/6) and 9 start/exit-19 hold cycles for the not-yet-startable procs; outputs are never overwritten (wrapper skips if `<tag>.root` exists, no `xrdcp -f`), so no duplicate test runs. Submission: EosSubmit schedd (`module load lxbatch/eossubmit; condor_submit`), gridpacks cluster **884456** (11 jobs), test jobs cluster **884457** (6 jobs, hold-and-release until the gridpack exists, `exit 19` protocol), twin test jobs cluster **884460** (2 jobs). Outputs: `work/gridpacks/`, `work/test/<sample>/` (`<sample>_s<seed>.{root,_gen.root,json,lhe.gz,_logs.tgz,_full.root}`), logs `work/condor/`.
| sample | seed | n_req / LHE / Delphes entries (MLM: accepted) | σ_LHE init [fb] | σ_gridpack [fb] | σ_PY8 [fb] | LHE vs PY8 | wall gridpack/PY8+Delphes/slim [s] | slim ROOT+gen [kB/ev] | worker |
|---|---|---|---|---|---|---|---|---|---|
| B_QCD_Waajj_nomjj | 2x25001 | 2000 / 2000 / 2000 | 1.631 ± 0.011 (1st proc.) | 3.582 ± 0.0064 | 3.558 | -0.7 % | 318/188/8 | 2.68 | b9p17p0675 |
| B_QCD_Waajj_vbs | 2x24001 | 2000 / 2000 / 2000 | 0.2657 ± 0.0021 (1st proc.) | 0.6327 ± 0.0011 | 0.6317 | -0.2 % | 394/155/10 | 2.85 | b9p20p9077 |
| F_QCD_Wajj_nomjj | 2x28001 | 2000 / 2000 / 2000 | 2625 ± 21 (1st proc.) | 5683 ± 10 | 5735 | +0.9 % | 129/229/13 | 2.46 | b9p16p0159 |
| F_Wajj_pilot | 2x30001 | 5000 / 5000 / 5000 | 4545 ± 23 (1st proc.) | 9878 ± 19 | 9838 | -0.4 % | 160/358/12 | 2.44 | b9p26p4110 |
| F_Wjj_pilot | 2x29001 | 5000 / 5000 / 5000 | 1.982e+06 ± 1.2e+04 (1st proc.) | 3.435e+06 ± 7.6e+03 | 3.413e+06 | -0.6 % | 63/505/15 | 2.22 | b9p16p0146 |
| H_QCD_WH_mlm | 2x13001 | 4000 / 4000 / 1386 | 294.2 ± 1.6 (1st proc.) | 879.6 ± 4.2 | 302.3 | -65.6 % | 70/230/8 | 2.02 | b9g03p0004 |
| H_ttH_1l | 2x16001 | 2000 / 2000 / 2000 | 54.24 ± 0.56 (1st proc.) | 107.8 ± 0.31 | 107.8 | +0.0 % | 30/169/12 | 3.11 | b9p26p6528 |
| S_EW_WHjj | 2x11001 | 2000 / 2000 / 2000 | 5.137 ± 0.055 (1st proc.) | 13.77 ± 0.037 | 13.68 | -0.7 % | 68/157/12 | 2.29 | b9g03p3647 |

Slim output 2.0-3.1 kB/event (ZH: 1.5-2.8); LHE+PY8+Delphes+slim ≈ 3-4 min per 2000 events. The MLM test shows the expected 34.6 % matching efficiency: the Delphes entry count is the accepted-event count, which must be used in N_MC.
Status of the remaining jobs and the check request: `VERIFY_REQUEST.md`, `STATUS.md`.

## 6. Fake-photon pilot (W+jets, two jet→γ fakes; `scripts/fakefactor_pilot_w.py`, patch 001)
5000 events, fixed-order W(→ℓν)+2j (ptj>20, |η|<5, ΔR>0.4), PY8 + slim Delphes, GenTruth N_prompt_photons = 0, parameterised f(j→γ) = 10⁻³(pT/50)^−0.5 (×2 endcap), one lepton pT>25 + MET>30 (illustrative, not optimised), σ input = σ_gridpack·WF = 3.435×10⁶ × 0.96008 = 3.298×10⁶ fb (deliberately WF-corrected; σ_MG = 3.435×10⁶ fb gridpack, PY8 3.413×10⁶ fb; using σ_MG would raise all yields by +4.2 %, i.e. peak 1.5 → 1.6 events, so D-WH-2 conclusions are unchanged), 500 fb⁻¹, `work/xrd/F_Wjj_pilot_fakefactor.json`:
| region | MC events | yield at 500 fb⁻¹ (nominal f) | N_eff | mean weight |
|---|---|---|---|---|
| PRE (1ℓ+MET, ≥2 γ-fakes, ≥2 tag jets pT>30) | 170 | 535 | 80 | 3.1 |
| VBS (+ m_jj>500, \|Δη\|>2.5) | 41 | **44.5** | 20 | 1.1 |
| PEAK (+ 120<m_γγ<130) | 2 | **1.5** | 1.9 | 0.77 |
Scenario scaling: f ×{0.3, 1, 3} per photon → yield ×{0.09, 1, 9} (peak: 0.14 / 1.5 / 14 events). Fraction of the VBS weight lost by a parton-HT filter: 0 % (HT>50), 26 % (>100), 67 % (>150). **Finding: the double-fake W+jets background cannot be shown to be negligible**: the peak-window estimate (1.5 events at nominal f) rests on **2 raw MC events (N_eff = 1.9, i.e. a statistical uncertainty of order ±70 %)**; the signal reference (≈ 0.9 events) is σ_phys × a ZH-like acceptance (≈ 6 %), not this pilot selection (pilot: no b-veto, photons pT>20, 10 GeV window), so the two numbers are *comparable within large uncertainty*. The pilot is plausibly but not demonstrably a lower bound (2-parton fixed order, extra jets only from the shower; the f-model and the x ~ N(0.85,0.1) fake-pT model are assumptions). It cannot be removed by a generator HT filter (loses ≥26 % of the VBS weight at HT>100). Direct production at N ≥ σ·L is impossible (9.8×10⁹ events) → D-WH-2 (human decision needed: accept parameterised-fake bound with a conservative upper variant, or a dedicated VBS-biased W+≥2j sample). **Wγ+2j pilot (one fake, N_prompt = 1; F_Wajj_pilot, 5000 events, seed 2x30001, σ input = 9878 × 0.96008 fb, `work/xrd/F_Wajj_pilot_fakefactor.json`)**: PRE 313 MC events → 1014 events (N_eff 236); VBS 38 → **63.6** (N_eff 26); PEAK 2 raw events → **1.3** (N_eff 2.0) at 500 fb⁻¹, nominal f (×{0.3,1,3} per fake). Same caveats: 2 raw peak events (N_eff 2.0), comparable to the signal within large uncertainty, cannot be shown negligible; its generation phase space (ptj>20, pTγ>15) is looser than the production F_*_Wajj_vbs samples.

## 7. Generator-cut safety (twin samples) — status
Twin gridpacks/test jobs (`B_QCD_Waajj_nomjj`, `F_QCD_Wajj_nomjj`, clusters in §5) are submitted; **Result for the Wγ+jets (QCD) twin** (`F_QCD_Wajj_nomjj`, mmjj = 0, test job seed 2x28001, 2000 events; `scripts/twin_safety.py`, `work/xrd/twin_F_QCD_Wajj.json`): σ(nomjj) = 5683 ± 10 fb vs σ(vbs, mmjj>400) = 712.4 ± 1.5 fb (12.5 %); parton-level m_jj < 400 GeV in 87.6 % of the twin events. Among twin events passing a loose reco VBS-like selection (≥1 lepton pT>25, ≥1 photon pT>25, ≥2 jets pT>30, |Δη_jj|>2.5): m_jj(reco) > 500 → 27 events, 10 of them with parton m_jj < 400 (**37 ± 9 %** would be lost by the mmjj>400 generator cut); m_jj(reco) > 700 → 13 events, 3 lost (23 ± 12 %). Hence, as in ZH, **the mmjj>400 generator cut is NOT safe for QCD-type samples** at the reco m_jj>500 working point (statistically limited: 27 events); the production QCD-type samples need the ratio correction C (twin ratio) with its MC-stat uncertainty, or a looser generator cut, decided in Phase 04. **Wγγjj (QCD) twin** (`B_QCD_Waajj_nomjj`, σ = 3.582 fb vs vbs 0.6327 fb, test seed 2x25001, 2000 events, loose selection with ≥1 photon): parton m_jj < 400 in 82.3 % of events; reco m_jj>500: 82 selected, 39 lost (**47.6 ± 5.5 %**); m_jj>700: 48 selected, 20 lost (41.7 ± 7.1 %) — also NOT safe (ZH: 64 %). The EW-type twin (ZH: 1.4 % loss) is **not yet demonstrated for W**: no EW nomjj twin was planned (the EW Wγγjj gridpack B_EW_Waajj_vbs is still building, D-WH-6); to be generated in Phase 04.


## 8. Checks
Exactly one condor submission per cluster (condor_q checked, 0 duplicates; the `hh` analyst's jobs share the account and were not touched). σ stable across seeds (W⁻ ±0.3 %), gridpack vs smoke ≤ 1 %. PY8 σ = LHE σ. Stage-out size check done in-job by the wrapper. FUSE listing lag on EOS for freshly staged files was bypassed with xrootd listing (`scripts/audit_test_jobs.py`). Job/log audit is the check's task.

## 9. Caveats
Validation samples are small (500-2000 events); no pile-up; LO; the electron deficit is a stock-card feature; MLM matching (xqcut 10 / qCut 19) is not DJR-validated (Phase 04); the fake-factor pilots are parameterised estimates (N_eff ≈ 2 in the peak window), not data-driven; closure at ±2 %. Nothing here is a yield.

## 10. Next actions
Collect remaining gridpacks/test jobs (B_EW_Waajj_vbs, F_Wajj_pilot, twins), update `config/sample_matrix.yaml` (σ), check audit, G1 review of D-WH-1…5 before any Phase-04 production.
