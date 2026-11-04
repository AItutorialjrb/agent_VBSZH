# Phase 02 — Background and overlap ledger (boosted VBF HH → bb̄bb̄)

- **Date UTC:** 2026-11-03 (start in PROGRESS.md)
- **Status: PASS with flagged infeasibilities** — the matrix, overlap rules, object audit, tagging/trigger scenarios and the effective-N machinery are in place; brute-force N ≥ σ·BR·L is **impossible** for QCD multijet, tt̄, Z+jets, VBF H and is handled only through the pre-declared effective-N policy; open decisions D-HH-2 … D-HH-12 in `STATUS.md` (listed in §9). No yield here is a result.
- **git commit:** recorded by orchestrator

## 1. Goal
Define every background class with σ source, BR, generator cuts/filters and N_MC policy; audit overlap between samples; check the Delphes card for large-R jets and substructure; pre-declare H→bb̄ tagging scenarios and the trigger assumption; extend `nmc_check()`; estimate storage.

## 2. Inputs / versions / seeds
As Phase 01 (stack LCG_110, MG5 3.6.3, PY8 8.317, Delphes 3.5.1, NNPDF31_nnlo_as_0118). Registry and seeds: `scripts/hh_samples.py` → `config/sample_matrix.yaml` (σ from MG5 status files) and `config/seeds.yaml` (90 unique seeds, `3 110 000 + 1000·idx + J`). Tagging/trigger: `config/tagging_scenarios.yaml`.

## 3. Sample matrix
All σ are **MG5 LO gridpack integration results** (`work/gridpacks*/…_status.txt`) at the stated generator cuts; the final-state BR ledger factor is applied once (`config/sample_matrix.yaml`). "brute force N" = σ·BR·3000 fb⁻¹, shown to document infeasibility, not a plan. K-factors are **not** applied (LO, flagged).

@@MATRIX@@

Notes: `ptheavy` = minimum pT for at least one heavy final-state particle (top, V, H); `ihtmin` = parton-level HT; the any-pair VBS filter requires an existing jet pair with y1y2<0, |Δy|>3.0, mjj>400 GeV for backgrounds (2.5/200 for EW processes), looser than the preliminary anchor (|Δη|>3.5, mjj>500). Z/W hadronic decays and H→bb̄ are forced in Pythia8 (conditional BR = 1) and the PDG/YR4 BR enters once from the ledger; tt̄ decays are inclusive in PY8 (BR = 1).

**Decay/generation modelling choices.** (i) QCD multijet is generated with j = g,u,d,s,c,b including b, so b/c content comes from the ME (initial/final b) *and* from g→bb̄/cc̄ in the parton shower; there is no merging with 5j (fixed-order exclusive 4-parton + PS, flagged). (ii) Higgs bosons from VBF H, VH, ttH are decayed in PY8; ggH + jets (HEFT) is listed as planned (idx 45) and is not a Phase-03 type. (iii) QCD ZZjj, QCD W/Z+jets with W, EW Zjj/Wjj are planned additions (idx 51, 54…) to be added at G2 if the stat budget allows.

## 4. Overlap ledger
| # | Pair | Overlap mechanism | Rule |
|---|---|---|---|
| O1 | `Q_4j_vbs` ⊃ `Q_bbjj_vbs` ⊃ `Q_4b_ht` | 4j with j ∋ b contains every b b̄ + 2-parton ME of `p p > b b~ j j`, which contains `b b~ b b~` | **Flavour partition on the hard-process record** (status-23 partons, stored as `g_nhard_b`, `g_nhard_bbar` by `slim_hh_truth.py`): events of `Q_4j` with both a b and a b̄ in the hard final state are removed and replaced by `Q_bbjj` (enriched statistics). `Q_4b_ht` is used only as a bound/shape sample, never summed. Partition equality validated at G2-FIX (04 §17.2: ratio 0.986 nominal, 0.992 twin) (σ of the b b̄-containing subset of `Q_4j` must equal σ(`Q_bbjj`) within errors) |
| O2 | `T_ttbar_mlm` (tt̄+0,1,2j MLM, nominal, D-HH-3) vs `T_ttbar_boost` (PS-only, 0 ME jets) | PS jets vs ME jets for the VBS pair | the MLM sample is the nominal; the PS-only sample is a cross-check, never summed; the ttjj ME+filter option of the first draft is superseded (needed only if N_eff failed; it did not) |
| O3 | `H_VBFH_bb` (`p p > h j j QCD=0`) vs `H_ZH_Zqq_bb`, W±H | EW pp→Hjj contains s-channel V→jj H diagrams | generator filter mjj>200 excludes the resonant region (m(jj)≈mV); parton-level evidence of the same mechanism for HHjj: −2 ± 2 % effect of s-channel diagrams inside VBS acceptance (01 report §3.1) → VBF H and VH samples are summed; for H_ZH/H_WH only the boosted-V topology (pT(V)>150) is generated |
| O4 | EW `S_HHjj` vs ggF HH (`G_ggHH_loop`) | different initial states/orders | separate samples; interference neglected (01 §4); ggF HH+2j missing (D-HH-2) |
| O5 | SM VBF HH vs κ2V scan | SM HH is signal for the SM μ, part of the background for κ2V≠1 | statistical model fixed in Phase 07; SM point is directly generated and also reproduced by morphing |
| O6 | QCD V+jets (QED=1) vs EW Vjj (QCD=0) | different amplitude orders; EW×QCD interference of order αs·α³ | EW Vjj planned as a separate sample; interference neglected, flagged |
| O7 | EW ZZjj (`V_ZZjj_EW`) vs ZH Z→bb̄ | different Higgs content | none |
| O8 | Any sample vs 3000 fb⁻¹ luminosity scaling | — | 3000 fb⁻¹ is luminosity scaling with the Run-3 card, not HL-LHC (SPEC) |

## 5. Objects: Delphes card audit
- Stock CMS card (`delphes_card_CMS_slim_v1.tcl`, lib) **contains** `FatJetFinder` (anti-kT R = 0.8 on EFlow, pT > 200, `ComputeNsubjettiness` (τ1…τ5, β = 1), trimming (R_trim 0.2, f 0.05), pruning (z 0.1, R_cut 0.5), soft-drop (β = 0, z_cut 0.1, R0 0.8)) in the ExecutionPath, but its TreeWriter branch was **removed** in slim_v1.
- Limitations found: no JES applied to fat jets (stock card: only AK5 `JetEnergyScale`); no b-tagging or flavour association for fat jets; no subjet b-tag; leptons/photons are not removed from fat jets; Delphes has **no** jet-substructure tagger such as DeepAK8/ParticleNet.
- Patch 002 (`cards/delphes/delphes_card_CMS_slim_hh_v1.tcl`, sha256 `e7ac2638…`): re-enable `FatJet` branch and add a particle-level `GenFatJetFinder` + `GenFatJet` branch; detector physics unchanged. Validation in the 03 report (soft-drop mass peak 116 GeV for contained H→bb̄; τ21 median 0.29).
- Truth labels per fat jet (`slim_hh_truth.py`): nB, nC, nHb (b quarks from H), nVq (V daughters not from top), nWq, ntb (top), plus last-copy H/t kinematics and hard-process b/c counts.

## 6. H→bb̄ tagging scenarios and trigger (declared in `config/tagging_scenarios.yaml`)
| Scenario | ε(H→bb̄, contained) | mistag g/light | mistag b / g→bb̄ | mistag c | mistag top |
|---|---|---|---|---|---|
| pessimistic | 0.45 | 2.0 % | 10 % | 4 % | 6 % |
| nominal | 0.60 | 1.0 % | 5 % | 2 % | 3 % |
| optimistic | 0.75 | 0.5 % | 2.5 % | 1 % | 1.5 % |

**Truth class of a selected fat jet (explicit; first match wins; resolves G1 review item 1; same text in the yaml):** top (nWq = 2 and ntb = 1) → mistag_top; **Hbb** (nHb = 2: both b quarks of one Higgs within ΔR < 0.8) → ε(H→bb̄, contained); **bb_nonH** (nB ≥ 2, not Hbb: g→bb̄ from the shower or ME, Z→bb̄, ...) → `mistag_bb_nonH` (declared equal to the b/g→bb̄ column: 10 / 5 / 2.5 %; Z→bb̄ is further suppressed by the m_SD window); b (nB = 1) → mistag b; c (nC ≥ 1, nB = 0) → mistag c; l (otherwise) → mistag g/light. Earlier drafts of `sr_feasibility.py` gave every nB ≥ 2 jet the Higgs efficiency; that was wrong and is fixed.

Applied by **truth-tag weighting** (product of the two leading fat-jet probabilities, class from truth, m_SD window and pT ≥ 300, |η| < 2.4). Justification: ranges bracket published Run-2 CMS taggers (JINST 15 (2020) P06005, arXiv:2004.08262; ParticleNet note CMS-DP-2020/002); **these numbers are assumptions, not measurements, not data-driven; exact working-point values are to be checked against the cited references in Phase 04 (not done here)**. Trigger: offline leading large-R pT ≥ 450 GeV (alternative: AK4 HT ≥ 1000 GeV) on the plateau, efficiency 1, **stated as an assumption**; the 450 GeV value is probably below the Run-3 single-AK8 plateau, so the variations **500 and 550 GeV are pre-declared now** (all reported in Phase 07, D-HH-9). Soft-drop masses carry no JES (peak at 116 GeV): the Phase-06 window must account for this.

## 7. Effective-N machinery (`scripts/nmc_check_hh.py`, patch 006)
Signals (registry roles `sig`/`basis`/`closure`; twin/validation/ggF-HH-closure samples are not signal): N_gen ≥ max(50 000, σ·BR·3000 fb⁻¹). The BR ledger uses labelled entries (`B_bb@H1`, `B_bb@H2`, `B_Zqq@Z1`, `B_Zqq@Z2`: one factor per distinct decaying particle; a repeated identical label is rejected), br_total is stored at full precision and compared at 1e-9 relative tolerance; `python3 scripts/nmc_check_hh.py config/sample_matrix.yaml` additionally runs the BR-once and signal-N rule on the real registry (passes). Backgrounds: (1) generator filters looser than the reco anchor with a twin-sample proof (`twin_ok`), (2) truth-tag weights, (3) N_eff = (Σw)²/Σw² ≥ 10 in the SR or a direct upper bound + conservative variant. The function raises `SystemExit` listing **all** violations; its self-test (`python3 -P scripts/nmc_check_hh.py`) passes the good registry and raises on a bad one (basis and closure signal with N too low, twin missing, N_eff < 10 without bound, BR label applied twice, br_total off by 1e-7 relative). Twin sample status in Phase 03: signal VBS filter **proven safe at parton level** (03 report §6); background twins (e.g. ihtmin 350 vs 500, VBS 3.0/400 vs none) are **not yet generated** and are required before G2.

## 8. Feasibility from the Phase-03 test samples (2000 events each, **illustrative, not a result**)
Preliminary anchor: two fat jets pT ≥ 300 (lead ≥ 450), VBS pair (any opposite-hemisphere non-overlapping AK5 pair, mjj > 500, |Δη| > 3.5), both m_SD ∈ [90,150]. Expected-event numbers use σ·BR·L·(Σw/N_gen); they have **no** meaningful uncertainty at these counts.

@@FEAS@@

After the explicit class definition the table is **unchanged in value** for the rows that have window events (their selected jets are classes top, Hbb or light; no nB ≥ 2 non-Higgs jet populated the window), but the weights are now unambiguous for every scenario. Intervals are 95 % Garwood (Poisson) limits on the raw SR count k applied to the weighted expectation; a row with k = 0 is shown as a **95 % upper limit** = 3.0 raw events × (σ·BR·L/N_gen) × ε_H² (the largest possible weight), i.e. never as zero.

Reading: (i) SM EW signal: 0.070 expected events at 500 fb⁻¹ (nominal) from k = 2 raw events, 95 % interval **[0.009, 0.25]**; even the upper end is ≪ 1 event, so the a-priori negligible SM sensitivity of the boosted category (and the κ2V ≠ 1 framing, κ2V = 0 has σ ≈ 14× SM) is supported, not an overclaim; (ii) ggF HH (LO, no K-factor, 0 ME jets + PS) retains about half of that (0.037 [0.001, 0.20], k = 1): it is a first-order background (D-HH-2); (iii) tt̄ and ttH populate the SR with k = 1–2 raw events out of 2000, QCD (Q_4j, Q_bbjj), Z+jets, VBF H, ZH and ZZjj with k = 0: all N_eff ≲ 2, the upper limits in the table are **limits of the test statistics, not estimates, and the corresponding backgrounds must not be read as negligible**; (iv) a class-resolved N_eff estimate for QCD and tt̄ (weights span ≈ 10⁻⁴ for light-light to 0.36 for Hbb-Hbb, so N_eff is set by the rare shower g→bb̄ and Higgs-like fraction, not by raw counts) replaces the naive "10⁵–10⁶ events" scaling and is pre-G2 work (03 §13).

## 9. Infeasibilities and decisions (never relaxed silently) — status after G1
Common numbering D-HH-1 … D-HH-12 (identical in 01, 02, 03, STATUS.md and `04_production_plan.md`); human answers are quoted verbatim in `p2/SPEC.md` §6 (D2, D11–D16). Implementation of every answer is documented in **04**.
| ID | topic | G1 answer (SPEC §6) | implemented in |
|---|---|---|---|
| D-HH-1 | partial HEPTools install in the shared MG5 tree | leave in place; listing/sha256 in SPEC §7 (D2); further installs only under `p2/software/` | no action; all new MG5 runs on batch (private copy per job) or `work/mg5priv` |
| D-HH-2 | ggF HH normalisation | LO loop-induced + PS, normalised to LHC HWG NNLO at 13.6 TeV, +30 % in the VBF region, EW-loop interference neglected | 04 §3, `config/g2_predeclared.yaml`, 01 §4(c) |
| D-HH-3 | tt̄ VBS topology | nominal MLM tt̄+0,1,2j validated by matching-scale variation; ttjj ME+filter only if N_eff fails | `T_ttbar_mlm*`, 04 §9 |
| D-HH-4 | QCD multijet | 4j + bb̄jj + PS + truth tag; class-resolved N_eff; b-enriched; ±100 %, ×0.5/×2 | 04 §6, §10 |
| D-HH-5 | SM acceptance / deliverable | κ2V ≠ 1; 300/450 provisional; SM 0.07 with Poisson interval | 04 §8, §10 |
| D-HH-6 | background twins, N_eff ≥ 10, storage ≤ 150 GB | accepted | 04 §5, §6, §11 |
| D-HH-7 | ME jet multiplicity (Z/W+3j, VH+2j, ggH+jj) | ME sample only if PS-based yield > 10 % of the SR background | 04 §7 |
| D-HH-8 | m(HH) clip | primary unclipped; clipped < 1.5 TeV variation + 1.0 TeV check | `config/g2_predeclared.yaml`, 04 §10 |
| D-HH-9 | trigger, m_SD | 450 baseline; 500/550 pre-declared; m_SD window on the Delphes peak, ±5 % scale | `config/g2_predeclared.yaml`, 04 §10 |
| D-HH-10 | tag-class definition | accepted (item 1 of the G1 review) | §6 (unchanged) |
| D-HH-11 | extra backgrounds | 95 % UL in the SR; dedicated sample only if UL > 10 % of the SR background | 04 §7 |
| D-HH-12 | full N for ggF HH, ZH, ZZjj, ttH | accepted | 04 §4 (WH added by the same cost argument) |
New numbered items raised after G1 are listed in `STATUS.md` (D-HH-13 …).

### 9b. Backgrounds not otherwise in the ledger (G1 review item 12)
LO MG5 σ at the stated generator cuts (σ-only gridpacks, cluster 884857; no events generated); “brute-force N” for reference.

@@EXTRA@@

**Bounds / plans (σ ratios at the same type of generator filter; no event-level bound yet):** tW (1.83 pb) is 6 % of T_ttbar_boost (30.8 pb) with one top: its two-fat-jet + VBS acceptance is bounded by that of tt̄ times this ratio once tt̄ has N_eff ≥ 10; ttZ (0.162 pb) and ttW± (0.104 pb) are 0.65 and 0.42 × σ(ttH, ptheavy>150) (0.248 pb) with the same tt̄-like topology (ttZ with Z→bb̄ is a real bb̄ pair, mass peak at 91 GeV, suppressed by the m_SD window); EW Zjj (8.78 pb) is 3 % of QCD Zjj (270 pb) but has a genuine VBS pair (acceptance higher); QCD ZZ (0.086 pb, 0 ME jets) is comparable to V_ZZjj_EW (0.0765 pb) and needs PS jets for the VBS pair (D-HH-7). All five are generated at the same twin/N_eff standard at G2 if the N_eff of the leading samples (tt̄, Z+jets) does not already bound them (D-HH-11).

Not generated: **gg→ZH (boosted)**: loop-induced (loop_sm), σ(ggZH)/σ(qq̄→ZH) is a ~10 % effect in the literature (not quoted as a number here); plan: loop gridpack at G2 and treat as part of H_ZH; **WZ (QCD)**: analogous to X_ZZ_QCD_boost, plan as ZZ; **EW Wjj**: analogous to X_Zjj_EW_vbs; **QCD ZZ/WZ + 2 jets** (VBS-like): bounded by V_ZZjj_EW × (QCD/EW ratio, to be measured with a dedicated σ-only gridpack at G2); all go through truth-tag weights with the same effective-N rule.

## 10. Storage budget (HH share of the 400 GB)
Measured slim-ROOT size per event on the test jobs: 2.3–4.5 kB (S 2.85, VBF H 2.35, ZH 3.45, ZZjj 3.59, ttH 4.49, Zjj 2.83, Q_4j 5.2); the `Particle`-bearing `_full.root` (≈ 95 kB/event) and LHE are **not** kept in production. Signal: 8 morphing points × (50–121 k events) ≈ 0.5 M events ≈ **1.6 GB**. Backgrounds at ≈ 3×10⁷ generated events in total ≈ **≈ 100 GB**; ggF HH, single H, tt̄ ≈ 10–20 GB. **HH estimate: ≤ 150 GB** (leaving ≥ 250 GB for WH/ZH/combination). The number of background events is the lever and is a G2 decision.

## 11. Exact commands
```
python3 -P scripts/hh_samples.py ; python3 -P scripts/make_matrix.py ; python3 -P scripts/render_table.py
python3 -P scripts/sr_feasibility.py work/test config/sample_matrix.yaml config/tagging_scenarios.yaml work/sr_feasibility.json
python3 -P scripts/nmc_check_hh.py     # self-test
mg5_aMC cards/diag/bg_*.mg5            # diagram counts: work/diag/count_big.txt, bg_*.log
```

## 12. Checks, caveats, next actions
Checks: seeds unique (asserted); BR ledger asserted; diagram counts logged; Delphes card diff in `patches/002`. Caveats: LO σ only; QCD and tt̄ numbers unusable until N_eff is met; tagging numbers are assumptions; Q_4j (σ 3.77e4 pb, test job OK) is in `03_generation_validation.md`. Next: Phase 03 evidence, `VERIFY_REQUEST.md`, G1 decisions.
