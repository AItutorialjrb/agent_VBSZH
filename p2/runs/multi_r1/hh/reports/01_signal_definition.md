# Phase 01 — Signal definition: EW pp → HHjj (boosted VBF HH → bb̄bb̄), κV / κ2V / κλ

- **Date UTC:** 2026-11-03 (start 16:15Z, end see PROGRESS.md)
- **Status: PASS** (open decisions D-HH-1 … D-HH-12 in STATUS.md; none blocks Phase 01; the G1 review conditions are tracked in 03 §13)
- **Run:** multi_r1 (canonical), process directory `p2/runs/multi_r1/hh/`
- **git commit:** recorded by orchestrator

## 1. Goal
Define the target gauge-invariant EW final state pp → HHjj (QCD = 0) at √s = 13.6 TeV with a UFO model that exposes κV, κ2V, κλ separately; validate orders by diagrams, subprocess lists and cross sections; fix the H → bb̄ treatment and the BR ledger; fix the six-point morphing basis with closure on ≥ 2 independent points; separate VBF-like kinematics from diagram labels; state the treatment of ggF HH, VHH-like (Higgsstrahlung) contributions and interference. All σ here are **parton-level (LHE / gridpack) validation numbers**, not results.

## 2. Inputs, versions, seeds
| Item | Value |
|---|---|
| Stack | ZH stack `source p2/lib/scripts/setup_stack.sh`: LCG_110 (gcc13), MG5_aMC 3.6.3 upstream, Pythia 8.317, Delphes 3.5.1, NNPDF31_nnlo_as_0118 (LHAID 303600), seeds below |
| UFO (signal) | `sm_kVk2VkL` = MG5 v3.6.3 built-in `sm` UFO + **one patch** (`scripts/make_hh_model.sh`; tarball sha256 in `config/ufo_checksums.txt`); restriction `-no_b_mass` (5F, massless b, y_b = 0) |
| UFO (ggF HH) | `loop_sm_kl` = built-in `loop_sm` + one patch (`scripts/make_loop_model.sh`): kl × GC_30 (HHH) |
| MG5 source | upstream tarball sha256 `2bb0d085a37b704ef956e8e8ed468bdcfef13e638c82ed3f1c4e968a090ebd98` (ZH install; no network fetch of any model needed) |
| Seeds (SPEC §3.4) | `seed = 3 110 000 + 1000·idx + J`; J = 0 gridpack, 1 test job, 2 LHE-closure job; 90 seeds asserted unique in `scripts/hh_samples.py` (`config/seeds.yaml`) |
| Cards | `cards/S_HHjj_*.mg5`, `cards/V_*HH*.mg5`, generated from `scripts/hh_samples.py` |

### 2.1 The model patch (what exactly changes)
Three real external parameters in block `KAPPAS` (codes 1, 2, 3 = kV, k2V, kl) multiply exactly five couplings of the SM UFO: GC_72 (HWW), GC_81 (HZZ) × kV; GC_34 (HHWW), GC_65 (HHZZ) × k2V; GC_69 (HHH) × kl. HHHH (GC_33) does not enter at this order. Nothing else is modified.

**Two pitfalls found and fixed during validation (kept in the record because both silently gave wrong physics):**
1. Restrict-card defaults equal to 1 are *fixed* by MG5 and removed from the param card (`DEBUG: fix parameter value: mdl_kV`) → first gridpacks gave σ ≈ 1.13 fb at every (κV,κ2V,κλ). Detected because σ was identical at seven different points.
2. After changing defaults to a common value, MG5 *merged the three externals into one card entry* (`set of param: 1*kv,1*k2v,1*kl`) → all `set` commands wrote the same entry. Defaults are now mutually distinct (1.11, 1.22, 1.33; `scripts/make_hh_model.sh`); every card sets kV, k2V, kl explicitly; the param card is verified to contain three separate entries (`proc_new/Cards/param_card.dat`, `INFO: modify param_card … id (1,)/(2,)/(3,)`). All numbers in this report come from the corrected rerun (`work/gridpacks_v2/`); the faulty gridpacks were moved to `work/gridpacks_bad_*` and are not used.

## 3. Process definition and diagram audit
Target: `generate p p > h h j j QCD=0 QED=4` with `p, j = g u c d s b u~ c~ d~ s~ b~`.

| Check | Command (card in `cards/diag/`) | Result |
|---|---|---|
| Full EW | `p p > h h j j QCD=0 QED=4` (also without orders) | 87 processes, **456 diagrams**; single subprocess group `qq_hhqq` (31 distinct matrix elements, 172 diagrams after crossing reuse); no gluon-initiated process |
| QCD-order amplitudes | `QCD==1`, `QCD==2` with `QED==4` | **NoDiagramException** (no tree-level amplitude with gluon exchange): the EW amplitude is the only tree-level amplitude for this final state (massless quarks, y_b = 0) |
| Wrong QED orders | `QED==2`, `QED==3` | NoDiagramException |
| No s-channel V | `… $$ w+ w- z` | 324 diagrams, i.e. **132 of 456 diagrams contain an s-channel W/Z** (crossing-dependent label) |
| ZHH-like | `p p > z h h QCD=0, z > j j` | 1 process, 25 diagrams |
| W±HH-like | `p p > w+ h h QCD=0, w+ > j j` (and w−) | 10 diagrams each |

Note on labels: "s-channel V" vs "t-channel V" is a property of a diagram in a given crossing and gauge (unitary gauge here); it is **not** gauge-invariant and is used only as a bookkeeping label. The gauge-invariant object is the full EW amplitude of order QED⁴ (QCD⁰).

### 3.1 VBF-like kinematics vs diagram labels (evidence, parton level, SM point)
Same generator cuts for all three (ptj 20, |ηj| < 5, ΔRjj > 0.4, any jet pair with y1·y2 < 0, |Δy| > 2.5, mjj > 200 GeV; see §6):

| Sample | σ [fb] | σ after anchor (mjj > 500 GeV, \|Δη\| > 3.5) [fb] |
|---|---|---|
| Full EW (`S_HHjj_kV1_k2V1_kl1`) | 1.132 ± 0.02 (LHE init, 5k ev) / 1.153 ± 0.018 (gridpack) | 0.951 ± 0.015 |
| No s-channel V diagrams (`V_HHjj_SM_noSchanV`) | 1.127 ± 0.015 (gridpack) | 0.955 ± 0.015 |
| Full EW, **no** VBS filter, twin (`S_HHjj_SM_twin_loose`) | 1.591 ± 0.026 | **0.943 ± 0.017** |

Source: `work/twin_check.txt` (from `scripts/morph_closure.py::read_lhe`, 5000 LHE events each). Conclusions: (i) within the VBS acceptance the s-channel-V diagrams (132/456) change σ by (−2 ± 2) %, i.e. consistent with zero: the selected phase space is VBF-like and the diagram label is irrelevant there; (ii) the generator VBS filter is looser than the preliminary reco anchor and does not change the anchor-level σ (0.951 ± 0.015 vs 0.943 ± 0.017 fb) — cut safety demonstrated at parton level (validation only).

## 4. VHH-like (Higgsstrahlung-type) contributions and interference
| Process (parton level, validation only) | σ [fb] | Comment |
|---|---|---|
| ZHH, Z → jj in MG5 (includes MG5 BR(Z→jj)) | 0.204 ± 0.001 | no VBS filter; jj pair has m ≈ mZ |
| W+HH, W+ → jj | 0.200 ± 0.001 | W− by charge symmetry up to PDFs (not generated) |
| EW HHjj, SM, same ptj/η cuts, no VBS filter | 1.591 ± 0.026 | for scale |

The resonant VHH, V → jj component is ≈ 0.4 fb per boson pair before any VBS requirement; since m(jj) ≈ m_V < 200 GeV, it is removed by the VBS pair requirement (mjj > 500 GeV in the anchor, > 200 GeV at generator level). It is **part of the full EW amplitude** (the 132 s-channel diagrams) and interferes with the t-channel diagrams in the full-amplitude σ; the table of §3.1 shows the interference/resonant effect in VBS acceptance is (−2 ± 2) %. **Treatment:** the signal is the full EW pp → HHjj amplitude (QCD = 0), no separate VHH sample enters the yields; `V_ZHH_Zjj_SM`/`V_WHH_Wjj_SM` are validation-only. The V → qq̄ + HH final state with a boosted V and two Higgs fat jets is a different topology (3 fat jets), outside the 2-fat-jet + 2-VBS-jet category.

**Interference statement.** (a) EW × QCD at tree level: identically zero (no QCD-order tree amplitude, §3). (b) EW HHjj × loop-induced ggF HH + jets: different initial-state colour structure and loop order; **not computed, neglected, flagged as limitation** (D-HH-2). (c) ggF HH (loop, LO, no K-factor) is treated as a separate background sample, not as part of the signal. It is **not** negligible in the boosted SR: in the Phase-03 test sample it retains about half of the SM-signal expectation in the preliminary anchor SR (02 §8, 1 raw event, wide interval); the generated 0-jet + PS sample under-populates the genuine VBS-jet topology and ggF HH + 2 jets is missing (D-HH-2). (d) The nonlinear κ-dependence is included exactly in the EW amplitude through the morphing basis of §5.

## 5. Six-point basis and morphing
The EW HHjj cross section is a homogeneous quartic in the couplings; its independent monomials in (κV, κ2V, κλ) are

`σ = Σ_j a_j m_j`, `m = (κV⁴, κ2V², κV²κλ², κV³κλ, κVκ2Vκλ, κV²κ2V)`

(HVV² t-channel, HHVV contact², (HVV·HHH)², HVV²×HHH interference, HHVV×HHH, HVV²×HHVV). Six basis points give `σ(κ) = Σ_i c_i(κ) σ_i` with `c = m(κ)·M⁻¹`, `M_ij = m_j(κ_i)` (`scripts/morph.py`). The same coefficients apply bin-by-bin to any distribution. The basis was selected **before** any σ was inspected by minimising cond(M) over a grid (κV ∈ {0.5,1,1.5}, κ2V ∈ {0,0.5,1,2,3}, κλ ∈ {−1,0,1,2,5}, seed 1, 40 000 random draws; SM forced in the set):

Basis: (κV,κ2V,κλ) = (1,1,1), (1.5,0,1), (1.5,0,0), (0.5,2,0), (1,0,2), (1,2,−1); cond(M) = 8.66.
Closure points (independent of the basis): T1 = (1,0,1), T2 = (1,2,1).

### 5.1 σ table (MG5 LO gridpack integration, VBS filter as §6; `config/sample_matrix.yaml`)
| (κV,κ2V,κλ) | role | σ [fb] | σ·B(HH→4b) [fb] |
|---|---|---|---|
| (1,1,1) | basis (SM) | 1.153 ± 0.018 | 0.391 |
| (1.5,0,1) | basis | 95.05 ± 1.22 | 32.2 |
| (1.5,0,0) | basis | 119.0 ± 1.5 | 40.4 |
| (0.5,2,0) | basis | 31.15 ± 0.20 | 10.6 |
| (1,0,2) | basis | 11.99 ± 0.08 | 4.07 |
| (1,2,−1) | basis | 5.038 ± 0.041 | 1.71 |
| (1,0,1) | closure T1 | 16.68 ± 0.14 | 5.66 |
| (1,2,1) | closure T2 | 8.425 ± 0.043 | 2.86 |

### 5.2 Closure (parton-level validation, `scripts/morph_closure.py`, `work/morph_closure.json`)
- **σ closure (gridpack σ, errors from the MG5 integration):** T1: predicted 16.74 ± 0.28 vs direct 16.68 ± 0.14 fb (ratio 1.004, pull 0.2); T2: 8.32 ± 0.35 vs 8.43 ± 0.04 fb (ratio 0.988, pull −0.3).
- **σ closure (LHE init cross sections, 5000 ev each):** T1 ratio 0.995, T2 ratio 1.019.
- **Distribution closure (5000 LHE events per point; morphed from the 6 basis samples vs the direct sample; 10 bins; statistical errors of all 7 samples):** χ²/ndf — T1: m(HH) 6.5/10, pT(H1) 12.1/10, m(jj) 9.9/10, |Δη(jj)| 12.8/8; T2: 14.1/10, 12.6/10, 5.3/10, 7.7/8. Compatible with closure at this statistics.
- Caveat: errors of the morphed prediction at points far from the basis grow with Σ|c_i| (T2: coefficient 1.85 on the SM point); the production statistics (Phase 04) must be set accordingly; the Σ|c_i| amplification over the intended κ2V and κλ scan range and an SR-level closure at a point with κV≠1 and κλ≠1 are pre-G2 work (03 §13).

Physics note (not a result): σ(κ2V=0)/σ(SM) ≈ 14 at κλ = 1 with the VBS filter; the SM σ·B(4b) = 0.39 fb, i.e. ≈ 195 events at 500 fb⁻¹ before acceptance. The kinematic acceptance of the boosted category for the SM point is small (see 03 report: 2.5 % of SM events have two large-R jets with pT > 250 GeV).

## 6. Generator configuration (signal)
`ebeam1 = ebeam2 = 6800`, `pdlabel lhapdf`, `lhaid 303600`, `maxjetflavor 5`, `use_syst True` (7-point scale + PDF weights), `dynamical_scale_choice 3` (as ZH), `ptj 20`, `etaj 5`, `drjj 0.4`; VBS pair filter (patch 003): exists a jet pair with y1y2 < 0, |Δy| > 2.5, mjj > 200 GeV (uses run-card `deltaeta`, `xetamin` repurposed; the stock WBF cut acts on the two hardest jets, which are the Higgs jets in boosted topologies and is therefore unsuitable). Reco anchor for cut-safety: |Δη| > 3.5, mjj > 500 GeV (provisional, frozen in Phase 05). H is undecayed in the LHE (`h` is stable in the ME; mH = 125, WH = 6.38e-3 GeV in the param card).

## 7. H → bb̄ and BR ledger
Pythia8: `25:onMode = off`, `25:onIfMatch = 5 -5` (conditional BR = 1 per Higgs); the physical branching fraction is applied **once** via the ledger (`config/sample_matrix.yaml: br_inputs, br_ledger`): B(H→bb̄) = 0.5824 (LHC Higgs WG Yellow Report 4 SM prediction at mH = 125.0 GeV, i.e. the mass used in the model; not the 125.09 GeV value; PDG gives only a measured value so no PDG SM cross-check exists — closed; the BR uncertainty is carried as a nuisance in Phase 06), HH → bb̄bb̄ factor = 0.5824² = 0.33919 (the ledger lists `B_bb` twice by construction, one per Higgs; `scripts/nmc_check_hh.py` verifies br_total = product of the ledger entries and fails loudly otherwise). **W-width factor:** none of the HH samples decays a W or Z inside MG5 (all V and top decays are done in Pythia8 with PDG branching fractions or inclusively, BR ledger = PDG value, once); there is therefore no MG5-LO→PDG width factor (ZF/WF analogue) to derive for HH. The only samples with an MG5 decay chain are the validation-only V_ZHH/V_WHH (σ includes the MG5 BR(V→jj), never used in yields). Z/W hadronic decays (backgrounds) are forced in PY8 and use the PDG hadronic BR directly (B(Z→had) = 0.6991, B(W→had) = 0.6741); no MG5 width is involved (SPEC §1.6: WF applies only where W decays are done in MG5, which is never the case for HH yields). Tops decay inclusively in PY8 (BR = 1, includes all-hadronic + semileptonic + dilepton in one sample).

**BR closure (generator record of the Phase-03 test jobs, `scripts/br_closure.py`, 2000 events each):** fraction of last-copy Higgs bosons with a b b̄ pair = 1.000 (S, VBF H, ZH, ttH); Z → qq̄ = 1.000 with Z → bb̄/hadronic = 0.2115 (ZH), 0.2185 (ZZjj), 0.2135 (Zjj) vs PDG 0.1512/0.6991 = 0.216 (consistent); ttH inclusive W → qq̄ = 0.6845 ± 0.0073 (stat) vs PDG 0.6741.

## 8. ggF HH
`loop_sm_kl` (LO, loop-induced, full top mass): `generate g g > h h [noborn=QCD]`; κλ enters only the triangle: σ(κλ) = A + Bκλ + Cκλ² (three-point morphing, κλ ∈ {1, 0, 2}, closure point κλ = 5: predicted 32.4 ± 1.6 fb vs direct 33.44 ± 0.14 fb, pull −0.6; σ(κλ=0,1,2) = 30.09, 14.41, 6.80 fb). MG5 LO σ(κλ = 1) = 14.41 ± 0.09 fb (gridpack; LO, no K-factor, **not** the NNLO-FTapprox value; K-factor handling is a Phase 04/05 decision, D-HH-2). The sample is a background, not part of the signal; ggF HH + 2 jets (VBS-like topology) is not available at LO full-theory in practice and is raised as D-HH-2. The MadLoop run in the gridpack worked without ninja/collier (CutTools path); an accidental interactive `output` of a loop process attempted to install HEPTools inside the frozen ZH install (incident, D-HH-1).

## 9. Exact commands and paths
```
source p2/lib/scripts/setup_stack.sh
bash p2/runs/multi_r1/hh/scripts/make_hh_model.sh ; bash .../make_loop_model.sh          # UFOs -> work/models
mg5_aMC cards/diag/d_*.mg5                                                              # diagram audit (work/diag/*.log)
python3 -P scripts/hh_samples.py ; python3 -P scripts/make_submit_hh.py                 # cards, registry, seeds, submit files
condor_submit scripts/condor/gridpacks_hh_rerun2.sub   (cluster 884461, EosSubmit schedd)   # signal/validation gridpacks, work/gridpacks_v2
condor_submit scripts/condor/lhe_closure.sub           (cluster 884463)                      # 5000-event LHE per closure point, work/lhe
python3 -P scripts/morph_closure.py work/lhe work/morph_closure.json
```
Evidence files: `work/gridpacks_v2/*_status.txt`, `work/diag/*.log`, `work/morph_closure.json`, `work/twin_check.txt`, `work/br_closure.json`, `config/sample_matrix.yaml`.

## 10. Caveats
LO only, fast simulation; κ ≠ SM points violate unitarity at high m(HH) (standard EFT-like parametrisation, mitigated by the planned m(HH) clipping cut); VBS generator filter repurposes two run-card parameters (documented, patch 003); closure is parton-level with 5k events per point; σ errors are MG5 integration errors; no theory uncertainties evaluated yet (weights are stored). Pitfalls of §2.1 show that σ values must always be inspected for κ-dependence before use.

## 11. Next actions
Phase 02 background/overlap ledger; production planning at G2 with N ≥ max(50k, σ·B·3000 fb⁻¹): 121k events at (1.5,0,0), 97k at (1.5,0,1), 50k elsewhere.
