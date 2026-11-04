# Phase 04 (pre-G2) — Production plan and Phase-03 completion (boosted VBF HH → bb̄bb̄)

- **Date UTC:** 2026-11-03/04 (log: PROGRESS.md)
- **Status: APPROVE-with-conditions at G2 (reviews/hh_G2.md); this version = G2-FIX.** Phase 03 PASS. Blocks 1–2 of the production (signal, ggF HH, tt̄/ttH/ZH/WH/ZZjj) are ready but **nothing is submitted**; the QCD block is **HELD** (sev-1: residual generator-filter loss unmeasured). Open decisions: D-HH-13, D-HH-14a/b/c, D-HH-15 (pilot reuse), D-HH-16 (ggF HH premise).
- **Goal:** implement all G1 decisions D-HH-1…12 and the binding G1 reviewer conditions; deliver the production plan for G2.
- **Inputs / versions:** MG5_aMC 3.6.3 (per-job private copy of the install tarball; no write into `software/`), Pythia 8.317 (CP5, NNPDF3.1 NNLO, lhaid 303600), Delphes 3.5.1 slim_hh card (patch 002), LCG_110; seeds: SPEC §3.4 G1 revision (`seed = 3 000 000 + 100 000 + 1000·idx + J`; J=3 gridpack, 4 test, 5 closure/twin, 10+k production job k) + pre-G1 list `config/seeds_used_preG1.txt` (old formula, unchanged); uniqueness asserted in `scripts/hh_samples.py` and `scripts/check_seed_uniq.py` (177 registry seeds, 536 job seeds, OK). git commit: recorded by orchestrator.
- **Everything below is validation/planning at Delphes level on pilot samples; it is NOT a result.** SR yields are quoted for the plan only.

## 1. Summary
1. **Phase 03 complete**: all handoff sample types have a gridpack and a verified test job (§2). New: W±H, ggH+jj (HEFT), W+jets (QCD, W±), QCD 4b, tt̄+0,1,2j MLM (replaces the ttjj ME+filter, D-HH-3). σ closure (gridpack / LHE / PY8): ratios 0.977–1.017 over all 2000-event tests and pilots; every deviation is within the MG5 gridpack integration error (0.2–1.5 %) — the worst, S (1.5,0,0) = 0.977 (PY8 0.1163 ± 0.0001 pb vs MG5 0.1190 ± 0.0015 pb), is −1.8σ of the MG5 error (PY8 statistical error 0.1 %); no normalisation problem is indicated, but the band is 0.977–1.017, not '0.98–1.02'.
2. **Pilots (2.19 M events, `p2/production/hh/<sample>/`)** were run to measure N_eff, twins and closure: signal 20 k per point (not 50 k: pilots are part of the later production, same seeds scheme), ggF HH 10 k per κλ, main backgrounds 30–100 k, twins 20–200 k, bound samples 20 k. They are counted in N_planned.
3. **Physics outcome of the pilots (planning level):** the QCD multijet (Q_4j + Q_bbjj, nominal tagging, 500 fb⁻¹) is ≈ 97 % of the SR background (≈ 2×10³ events vs SM EW HH ≈ 0.05 events; κ2V = 0, κV = 1.5 ≈ 220 events before background). Sensitivity is therefore dominated by the multijet normalisation (±100 %, ×0.5/×2 pre-declared).
4. **Twin finding and HOLD (G2 sev-1):** the nominal QCD generator filters (ihtmin 500, VBS 3.0/400) lose **+25 ± 5 % (Q_4j) and +29 ± 6 % (Q_bbjj)** of the reco VBS-stage rate (+27 ± 5 / +32 ± 6 % tag-weighted) relative to the looser twin (ihtmin 350, VBS 2.0/200). The twin filter is the planned production filter, but its *own* residual loss is **unmeasured**, so the QCD block (217 jobs, ≈ 76 wall-h) is **held** until D-HH-14a is answered. Both options are prepared (§17): (1) further-loosened twins ≈ 1.5 M events ≈ 53 wall-h (files `scripts/condor/HELD_do_not_submit/g2_{gp,prod}_D14a_twin2.sub`); (2) a particle-level fat-jet filter: feasible only with a custom driver (§17), not ready.
5. **Morphing:** the **validated deliverable is κ2V at κV = κλ = 1** (closure T1, T2 at Delphes level, pulls ≤ 1.1; MC error ≤ 15 % at planned N). The third closure point (κV ≠ 1, κλ ≠ 1) has no power (prediction error > prediction), so κλ and κV results are **not validated** and depend on D-HH-13 (direct (1,1,0), (1,1,2) samples recommended) or carry no claim; κλ-only scans have up to 195 % MC error at planned N.
6. Cost (blocks 1–3, **wall-clock** not CPU): see §4 totals; **3.45 M new events, 345 jobs × 10 k, ≈ 135 wall-clock h, 19.2 GB** (incl. pilots) vs the 150 GB internal budget; block 1 (signal + ggF HH) 62 jobs, block 2 (tt̄, ttH, ZH, WH, ZZjj) 66 jobs, block 3 QCD (held) 217 jobs. Sizing now uses the **measured** pilot N_eff (§4).
7. **ggF HH premise changed (D-HH-16):** in the pilot SR ggF HH (LO+PS, K = 2.333) is 0.92 events at 500 fb⁻¹ vs the SM EW signal 0.047, **≈ 20× the SM signal** (D-HH-2 was decided on "about half"). Negligible for κ2V (< 0.1 % of the background) but it dominates any SM-HH statement; the 30 % VBF-region allowance and the K(κλ) reuse are raised separately as D-HH-16.
8. **Pilot reuse (D-HH-15):** the 2.19 M pilot events (≈ 41 % of the planned total) are a logged brief violation; all pilot jobs used exactly the MANIFEST gridpacks (sha256 table §17).

## 2. Phase 03: every handoff sample type has a verified test job
Test jobs: gridpack → LHE → PY8 → Delphes → slim, 2000 events, EOS stage-out, exit 0 (verified with `condor_history`), N_LHE = N_Delphes. Clusters: 884462 (S SM, VBF H, ZH, ttH, tt̄ PS, Z+jets, ZZjj), 884464 (Q_bbjj), 884466 (ggF HH), 884577 (Q_4j), **new: 884941 (W±H), 884943 (ggH+jj, W+jets, QCD 4b), 884945 (tt̄ MLM)**. Gridpacks for the new types and twins: clusters 884937 (20), 884944 (3), 884946 (1) in `p2/production/hh/gridpacks/` (sha256 in `production/hh/MANIFEST.tsv`). Pilots: 884938, 884942, 884947, 884948, 884949 (all jobs exit 0, none held/failed). Types: signal EW HHjj, ggF HH, VBF H, ZH, **WH**, ttH, **ggH+jj**, Z+jets, **W+jets**, ZZjj (EW VBS), tt̄ (**MLM+PS-only**), QCD 4j, bbjj, **4b**. Note on multi-process cards (`add process`): the LHE `<init>` block has one line per subprocess; `sigma_closure.py` now sums them (first-line-only gave 0.65 for W±H, a bookkeeping artefact, not a normalisation error).
| sample | test seed | N_req | N_LHE | N_Delphes | σ gridpack [pb] | σ LHE-init [pb] | σ PY8 [pb] | LHE/gridpack | PY8/LHE |
|---|---|---|---|---|---|---|---|---|---|
| G_ggHH_loop_kl1 | 3120001 | 2000 | 2000 | 2000 | 0.01441 | 0.014371 | 0.01437 | 0.997 | 1.000 |
| H_VBFH_bb | 3150001 | 2000 | 2000 | 2000 | 2.461 | 2.5031 | 2.505 | 1.017 | 1.001 |
| H_WH_Wqq_bb | 3142004 | 2000 | 2000 | 2000 | 0.1525 | 0.15412 | 0.1539 | 1.011 | 0.999 |
| H_ZH_Zqq_bb | 3151001 | 2000 | 2000 | 2000 | 0.08438 | 0.08465 | 0.08444 | 1.003 | 0.998 |
| H_ggH_jj_heft | 3145004 | 2000 | 2000 | 2000 | 2.642 | 2.6373 | 2.634 | 0.998 | 0.999 |
| H_ttH_bb | 3154001 | 2000 | 2000 | 2000 | 0.248 | 0.25082 | 0.2507 | 1.011 | 1.000 |
| Q_4b_ht | 3122004 | 2000 | 2000 | 2000 | 4.138 | 4.0979 | 4.095 | 0.990 | 0.999 |
| Q_4j_vbs | 3130001 | 2000 | 2000 | 2000 | 37660 | 37548 | 37580 | 0.997 | 1.001 |
| Q_bbjj_vbs | 3131001 | 2000 | 2000 | 2000 | 725.4 | 720.8 | 721.2 | 0.994 | 1.001 |
| S_HHjj_kV1_k2V1_kl1 | 3111001 | 2000 | 2000 | 2000 | 0.001153 | 0.001135 | 0.001136 | 0.984 | 1.001 |
| T_ttbar_boost | 3140001 | 2000 | 2000 | 2000 | 30.83 | 30.77 | 30.8 | 0.998 | 1.001 |
| T_ttbar_mlm | 3131004 | 2000 | 2000 | 616 | 180.3 | 181.41 | 56.07 | 1.006 | 0.309 |
| V_Wjj_QCD_vbs | 3151004 | 2000 | 2000 | 2000 | 839 | 848.06 | 846.4 | 1.011 | 0.998 |
| V_ZZjj_EW | 3163001 | 2000 | 2000 | 2000 | 0.0765 | 0.076688 | 0.07643 | 1.002 | 0.997 |
| V_Zjj_QCD_vbs | 3160001 | 2000 | 2000 | 2000 | 270 | 269.05 | 269.8 | 0.996 | 1.003 |

Pilot-level σ closure and cost per event (all production directories): 
| sample | jobs | N_LHE | N_Delphes | σ_PY8 [pb] | σ_ref [pb] | PY8/ref | s/event | kB/event |
|---|---|---|---|---|---|---|---|---|
| G_ggHH_loop_kl0 | 1 | 10000 | 10000 | 0.03023 | 0.03009 | 1.005 | 0.104 | 3.45 |
| G_ggHH_loop_kl1 | 1 | 10000 | 10000 | 0.01442 | 0.01441 | 1.001 | 0.103 | 3.64 |
| G_ggHH_loop_kl2 | 1 | 10000 | 10000 | 0.00682 | 0.006802 | 1.003 | 0.123 | 3.79 |
| G_ggHH_loop_kl5 | 1 | 10000 | 10000 | 0.03345 | 0.03344 | 1.000 | 0.111 | 3.05 |
| H_VBFH_bb | 5 | 50000 | 50000 | 2.5034 | 2.461 | 1.017 | 0.081 | 2.35 |
| H_VBFH_bb_twin | 5 | 50000 | 50000 | 2.716 | 2.728 | 0.996 | 0.066 | 2.36 |
| H_WH_Wqq_bb | 5 | 50000 | 50000 | 0.15414 | 0.1525 | 1.011 | 0.070 | 3.52 |
| H_WH_Wqq_bb_twin | 5 | 50000 | 50000 | 0.3689 | 0.3684 | 1.001 | 0.086 | 2.87 |
| H_ZH_Zqq_bb | 5 | 50000 | 50000 | 0.08451 | 0.08438 | 1.002 | 0.076 | 3.46 |
| H_ZH_Zqq_bb_twin | 5 | 50000 | 50000 | 0.20448 | 0.2051 | 0.997 | 0.069 | 2.85 |
| H_ggH_jj_heft | 5 | 50000 | 50000 | 2.636 | 2.642 | 0.998 | 0.070 | 2.63 |
| H_ggH_jj_heft_twin | 5 | 50000 | 50000 | 3.9018 | 3.925 | 0.994 | 0.071 | 2.65 |
| H_ttH_bb | 5 | 50000 | 50000 | 0.24948 | 0.248 | 1.006 | 0.075 | 4.59 |
| H_ttH_bb_twin | 5 | 50000 | 50000 | 0.3319 | 0.3319 | 1.000 | 0.071 | 4.29 |
| Q_4b_ht | 5 | 50000 | 50000 | 4.124 | 4.138 | 0.997 | 0.088 | 4.89 |
| Q_4j_vbs | 10 | 100000 | 100000 | 37558 | 37660 | 0.997 | 0.171 | 5.21 |
| Q_4j_vbs_twin | 20 | 200000 | 200000 | 2.6754e+05 | 2.663e+05 | 1.005 | 0.137 | 3.89 |
| Q_bbjj_vbs | 10 | 100000 | 100000 | 722.57 | 725.4 | 0.996 | 0.138 | 5.00 |
| Q_bbjj_vbs_twin | 15 | 150000 | 150000 | 5965.8 | 5976 | 0.998 | 0.091 | 3.75 |
| S_HHjj_SM_twin_loose | 3 | 30000 | 30000 | 0.0016107 | 0.001591 | 1.012 | 0.097 | 3.14 |
| S_HHjj_kV0p5_k2V2_kl0 | 2 | 20000 | 20000 | 0.03131 | 0.03115 | 1.005 | 0.099 | 4.28 |
| S_HHjj_kV1_k2V0_kl1 | 2 | 20000 | 20000 | 0.01669 | 0.01668 | 1.001 | 0.098 | 3.85 |
| S_HHjj_kV1_k2V0_kl1_twin | 2 | 20000 | 20000 | 0.017555 | 0.01747 | 1.005 | 0.066 | 3.83 |
| S_HHjj_kV1_k2V0_kl2 | 2 | 20000 | 20000 | 0.01207 | 0.01199 | 1.007 | 0.088 | 4.02 |
| S_HHjj_kV1_k2V1_kl1 | 2 | 20000 | 20000 | 0.001134 | 0.001153 | 0.984 | 0.075 | 2.88 |
| S_HHjj_kV1_k2V2_kl1 | 2 | 20000 | 20000 | 0.0084055 | 0.008425 | 0.998 | 0.096 | 4.47 |
| S_HHjj_kV1_k2V2_klm1 | 2 | 20000 | 20000 | 0.0050595 | 0.005038 | 1.004 | 0.062 | 4.77 |
| S_HHjj_kV1p25_k2V1p5_kl2 | 2 | 20000 | 20000 | 0.0021965 | 0.002201 | 0.998 | 0.094 | 3.06 |
| S_HHjj_kV1p5_k2V0_kl0 | 2 | 20000 | 20000 | 0.1163 | 0.119 | 0.977 | 0.089 | 3.67 |
| S_HHjj_kV1p5_k2V0_kl1 | 2 | 20000 | 20000 | 0.09436 | 0.09505 | 0.993 | 0.075 | 3.79 |
| T_ttbar_boost | 5 | 50000 | 50000 | 30.734 | 30.83 | 0.997 | 0.107 | 5.07 |
| T_ttbar_boost_twin | 5 | 50000 | 50000 | 134.58 | 134.3 | 1.002 | 0.068 | 3.85 |
| T_ttbar_mlm | 10 | 100000 | 30056 | 54.02 | 54.191 | 0.997 | 0.070 | 1.28 |
| T_ttbar_mlm_twin | 10 | 100000 | 33087 | 184.38 | 184.46 | 1.000 | 0.061 | 1.00 |
| T_ttbar_mlm_xq20 | 3 | 30000 | 6455 | 56.97 | 57.213 | 0.996 | 0.070 | 0.92 |
| T_ttbar_mlm_xq45 | 3 | 30000 | 12128 | 51.22 | 50.938 | 1.006 | 0.067 | 1.71 |
| V_Wjj_QCD_vbs | 5 | 50000 | 50000 | 839.38 | 839 | 1.000 | 0.075 | 2.77 |
| V_Wjj_QCD_vbs_twin | 5 | 50000 | 50000 | 2393.4 | 2414 | 0.991 | 0.074 | 2.67 |
| V_ZZjj_EW | 5 | 50000 | 50000 | 0.076896 | 0.0765 | 1.005 | 0.069 | 3.63 |
| V_ZZjj_EW_twin | 5 | 50000 | 50000 | 0.087914 | 0.08692 | 1.011 | 0.071 | 3.70 |
| V_Zjj_QCD_vbs | 5 | 50000 | 50000 | 270.04 | 270 | 1.000 | 0.101 | 2.82 |
| V_Zjj_QCD_vbs_twin | 5 | 50000 | 50000 | 788 | 786.3 | 1.002 | 0.075 | 2.71 |
| X_WZ_QCD_boost | 2 | 20000 | 20000 | 0.16315 | 0.163 | 1.001 | 0.073 | 4.95 |
| X_Wjj_EW_vbs | 2 | 20000 | 20000 | 90.815 | 90.04 | 1.009 | 0.075 | 2.32 |
| X_ZZ_QCD_boost | 2 | 20000 | 20000 | 0.0857 | 0.08632 | 0.993 | 0.082 | 4.98 |
| X_Zjj_EW_vbs | 2 | 20000 | 20000 | 8.7975 | 8.779 | 1.002 | 0.070 | 2.58 |
| X_ggZH_loop | 2 | 20000 | 20000 | 0.02136 | 0.02128 | 1.004 | 0.177 | 3.90 |
| X_tW_boost | 2 | 20000 | 20000 | 1.841 | 1.831 | 1.005 | 0.070 | 4.88 |
| X_ttW_boost | 2 | 20000 | 20000 | 0.1028 | 0.1041 | 0.988 | 0.076 | 5.14 |
| X_ttZ_boost | 2 | 20000 | 20000 | 0.1622 | 0.1624 | 0.999 | 0.078 | 5.40 |

Validation samples `V_HHjj_SM_noSchanV`, `V_ZHH`, `V_WHH` (diagram-class, Phase 01) are unchanged and never enter yields.

## 3. Normalisation (D-HH-2 and others)
- **ggF HH:** LO loop-induced (MG5 loop_sm_kl, σ_LO(κλ=1) = 14.41 fb) + PY8, normalised to the LHC HWG recommendation **σ = 33.62 fb at 13.6 TeV** (σ_NNLO-FTapprox 34.01 fb × K3 1.0308 × K_EW 0.959; scale +2.07/−4.85 %, PDF+αs 2.43 %, mt-scheme +5/−16 %): LHCHWG-2026-010 (CDS 2969777), TWiki LHCPhysics/LHCHWGHHRecommendations r3 (2026-09-29), fetched 2026-11-03. K = 2.333 is computed at **κλ = 1** and **reused for all κλ points as an assumption**: the HWG K-factor depends on κλ and on m(HH); no κλ-dependent K is available here and its size is not estimated — the ±30 % VBF-region uncertainty is the only allowance and is **not known to cover the κλ dependence** (raised as D-HH-16, not part of the filter decision D-HH-14). **Extra 30 % uncertainty in the VBF region**; EW×loop interference is **neglected**; ggF HH+2j not simulated.
- Signal EW HHjj: MG5 LO, no K (not requested). All other samples: LO σ at the generator cuts, K = 1; the normalisation uncertainties (placeholder 30 % for V+jets, tt̄ and single-H; ±100 % multijet) are Phase-06 nuisances, stated here as an assumption. BR ledger once per sample (`nmc_check_hh` asserts it).
- SM expectation (pilot, 20 k events, k = 17 raw SR events): **0.047 events at 500 fb⁻¹ (nominal tagging); pessimistic 0.027, optimistic 0.073; Garwood 95 % interval on k: ×[0.58, 1.60] → [0.027, 0.075] (nominal)**. (The 2000-event estimate 0.07 [0.009, 0.25] of the G1 reports is superseded.)

## 4. Production plan table (main requirement of G2)
Columns as required by the brief. "Twin evidence" = loss of the nominal filter at the reco VBS stage (2 fat jets, lead ≥ 450, VBS pair), nominal vs looser twin, with k_nominal/k_twin raw counts. Class-resolved top contributors: class pair, share of E[Σw], N_eff of that class (projected at planned N, nominal). Samples marked "bound" are not produced further. `T_ttbar_boost`, `Q_4b_ht`, `Q_4j_vbs`, `Q_bbjj_vbs` (nominal-filter pilots) are cross-check/bound-and-shape rows, never summed.
| sample | class | σ_LO [fb] ⇒ K ⇒ σ [fb] (source) | BR (applied once) | generator filters; twin evidence | rule | N required / N_eff target | N_planned (pilot done) | projected N_eff in SR p / n / o (class-resolved top) | seeds | jobs × events | wall-clock h | storage [GB] | test job |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S_HHjj_kV1_k2V1_kl1 | signal | 1.15 ⇒ 1 ⇒ 1.15 (MG5 LO gridpack (EW, QCD=0), no K) | B_bb@H1×B_bb@H2 = 0.3392 | deltaeta=2.5, xetamin=200; signal twin (S_HHjj_SM/k2V0 twins): ok | full-N | N ≥ 50,000 | 50,000 (20,000) | 34.2 / 33.5 / 33.2 (Hbb-Hbb 99%, 33; b-Hbb 0%, 1) | 3101012–3101014 | 3 × 10k | 0.9 | 0.14 | 884462 |
| S_HHjj_kV1p5_k2V0_kl1 | signal | 95 ⇒ 1 ⇒ 95 (MG5 LO gridpack (EW, QCD=0), no K) | B_bb@H1×B_bb@H2 = 0.3392 | deltaeta=2.5, xetamin=200; signal twin (S_HHjj_SM/k2V0 twins): ok | full-N | N ≥ 96,720 | 100,000 (20,000) | 3.83e+03 / 3.79e+03 / 3.78e+03 (Hbb-Hbb 100%, 3771.7; bb_nonH-Hbb 0%, 98.6) | 3102012–3102019 | 8 × 10k | 2.3 | 0.38 | σ-closure LHE job 884463 + pilot |
| S_HHjj_kV1p5_k2V0_kl0 | signal | 119 ⇒ 1 ⇒ 119 (MG5 LO gridpack (EW, QCD=0), no K) | B_bb@H1×B_bb@H2 = 0.3392 | deltaeta=2.5, xetamin=200; signal twin (S_HHjj_SM/k2V0 twins): ok | full-N | N ≥ 121,091 | 130,000 (20,000) | 4.02e+03 / 3.99e+03 / 3.98e+03 (Hbb-Hbb 100%, 3975.9; bb_nonH-Hbb 0%, 63.8) | 3103012–3103022 | 11 × 10k | 3.6 | 0.48 | σ-closure LHE job 884463 + pilot |
| S_HHjj_kV0p5_k2V2_kl0 | signal | 31.2 ⇒ 1 ⇒ 31.2 (MG5 LO gridpack (EW, QCD=0), no K) | B_bb@H1×B_bb@H2 = 0.3392 | deltaeta=2.5, xetamin=200; signal twin (S_HHjj_SM/k2V0 twins): ok | full-N | N ≥ 50,000 | 50,000 (20,000) | 3.28e+03 / 3.26e+03 / 3.25e+03 (Hbb-Hbb 100%, 3243.8; bb_nonH-Hbb 0%, 64.3) | 3104012–3104014 | 3 × 10k | 1.1 | 0.21 | σ-closure LHE job 884463 + pilot |
| S_HHjj_kV1_k2V0_kl2 | signal | 12 ⇒ 1 ⇒ 12 (MG5 LO gridpack (EW, QCD=0), no K) | B_bb@H1×B_bb@H2 = 0.3392 | deltaeta=2.5, xetamin=200; signal twin (S_HHjj_SM/k2V0 twins): ok | full-N | N ≥ 50,000 | 50,000 (20,000) | 2.65e+03 / 2.63e+03 / 2.62e+03 (Hbb-Hbb 100%, 2614.5; bb_nonH-Hbb 0%, 55) | 3105012–3105014 | 3 × 10k | 1.0 | 0.20 | σ-closure LHE job 884463 + pilot |
| S_HHjj_kV1_k2V2_klm1 | signal | 5.04 ⇒ 1 ⇒ 5.04 (MG5 LO gridpack (EW, QCD=0), no K) | B_bb@H1×B_bb@H2 = 0.3392 | deltaeta=2.5, xetamin=200; signal twin (S_HHjj_SM/k2V0 twins): ok | full-N | N ≥ 50,000 | 50,000 (20,000) | 5.49e+03 / 5.45e+03 / 5.44e+03 (Hbb-Hbb 100%, 5429.9; bb_nonH-Hbb 0%, 89.9) | 3106012–3106014 | 3 × 10k | 0.8 | 0.24 | σ-closure LHE job 884463 + pilot |
| S_HHjj_kV1_k2V0_kl1 | signal | 16.7 ⇒ 1 ⇒ 16.7 (MG5 LO gridpack (EW, QCD=0), no K) | B_bb@H1×B_bb@H2 = 0.3392 | deltaeta=2.5, xetamin=200; signal twin (S_HHjj_SM/k2V0 twins): ok | full-N | N ≥ 50,000 | 50,000 (20,000) | 2.14e+03 / 2.13e+03 / 2.12e+03 (Hbb-Hbb 100%, 2119.3; bb_nonH-Hbb 0%, 33.3) | 3107012–3107014 | 3 × 10k | 1.1 | 0.19 | σ-closure LHE job 884463 + pilot |
| S_HHjj_kV1_k2V2_kl1 | signal | 8.43 ⇒ 1 ⇒ 8.43 (MG5 LO gridpack (EW, QCD=0), no K) | B_bb@H1×B_bb@H2 = 0.3392 | deltaeta=2.5, xetamin=200; signal twin (S_HHjj_SM/k2V0 twins): ok | full-N | N ≥ 50,000 | 50,000 (20,000) | 3.71e+03 / 3.69e+03 / 3.68e+03 (Hbb-Hbb 100%, 3671.5; bb_nonH-Hbb 0%, 78.6) | 3108012–3108014 | 3 × 10k | 1.1 | 0.22 | σ-closure LHE job 884463 + pilot |
| S_HHjj_kV1p25_k2V1p5_kl2 | signal | 2.2 ⇒ 1 ⇒ 2.2 (MG5 LO gridpack (EW, QCD=0), no K) | B_bb@H1×B_bb@H2 = 0.3392 | deltaeta=2.5, xetamin=200; signal twin (S_HHjj_SM/k2V0 twins): ok | full-N | N ≥ 50,000 | 50,000 (20,000) | 81.8 / 80.2 / 79.6 (Hbb-Hbb 99%, 79.2; b-Hbb 0%, 3.3) | 3114012–3114014 | 3 × 10k | 1.0 | 0.15 | σ-closure LHE job 884463 + pilot |
| G_ggHH_loop_kl1 | ggF_HH | 14.4 ⇒ 2.33 ⇒ 33.6 (MG5 LO loop × K (HWG 33.62 fb @13.6 TeV)) | B_bb@H1×B_bb@H2 = 0.3392 | ; n/a (no generator filter beyond ptj/eta): ok | full-N | N ≥ 50,000 | 50,000 (10,000) | 25.5 / 23.2 / 22.3 (Hbb-Hbb 97%, 21.8; b-Hbb 2%, 4.5) | 3110011–3110014 | 4 × 10k | 1.5 | 0.18 | 884466 |
| G_ggHH_loop_kl0 | ggF_HH | 30.1 ⇒ 2.33 ⇒ 70.2 (MG5 LO loop × K (HWG 33.62 fb @13.6 TeV)) | B_bb@H1×B_bb@H2 = 0.3392 | ; n/a (no generator filter beyond ptj/eta): ok | full-N | N ≥ 71,437 | 80,000 (10,000) | 38.7 / 35.6 / 34.4 (Hbb-Hbb 97%, 33.6; b-Hbb 2%, 9.6) | 3111011–3111017 | 7 × 10k | 2.6 | 0.28 | pilot job (10k) |
| G_ggHH_loop_kl2 | ggF_HH | 6.8 ⇒ 2.33 ⇒ 15.9 (MG5 LO loop × K (HWG 33.62 fb @13.6 TeV)) | B_bb@H1×B_bb@H2 = 0.3392 | ; n/a (no generator filter beyond ptj/eta): ok | full-N | N ≥ 50,000 | 50,000 (10,000) | 24.3 / 20.4 / 18.9 (Hbb-Hbb 93%, 17.9; b-Hbb 3%, 7.7) | 3112011–3112014 | 4 × 10k | 1.7 | 0.19 | pilot job (10k) |
| G_ggHH_loop_kl5 | ggF_HH | 33.4 ⇒ 2.33 ⇒ 78 (MG5 LO loop × K (HWG 33.62 fb @13.6 TeV)) | B_bb@H1×B_bb@H2 = 0.3392 | ; n/a (no generator filter beyond ptj/eta): ok | full-N | N ≥ 79,390 | 80,000 (10,000) | 14.4 / 13.8 / 13.6 (Hbb-Hbb 99%, 13.5; b-Hbb 1%, 0.9) | 3113011–3113017 | 7 × 10k | 2.7 | 0.24 | pilot job (10k) |
| Q_4j_vbs_twin | QCD_multijet | 2.66e+08 ⇒ 1 ⇒ 2.66e+08 (MG5 LO gridpack at the generator cuts; K = 1 (LO; normalisation unc. in 06)) | one = 1 | deltaeta=2.0, xetamin=200, ihtmin=350; production uses the looser filter of the twin; nominal-filter loss at reco VBS stage +25±5 % (k=854/322) (residual loss of the looser filter assumed <= nominal loss (added as syst, D-HH-14)) | effective-N | N_eff ≥ 30 | 1,900,000 (200,000) | 51.5 / 51.5 / 51.5 (l-l 29%, 76.4; l-c 24%, 32.2) | 3180030–3180199 | 170 × 10k | 78.6 | 7.40 | pilot job (10k) |
| Q_bbjj_vbs_twin | QCD_multijet | 5.98e+06 ⇒ 1 ⇒ 5.98e+06 (MG5 LO gridpack at the generator cuts; K = 1 (LO; normalisation unc. in 06)) | one = 1 | deltaeta=2.0, xetamin=200, ihtmin=350; production uses the looser filter of the twin; nominal-filter loss at reco VBS stage +29±6 % (k=700/180) (residual loss of the looser filter assumed <= nominal loss (added as syst, D-HH-14)) | effective-N | N_eff ≥ 10 | 620,000 (150,000) | 17.9 / 17.9 / 17.9 (b-b 28%, 3.4; bb_nonH-bb_nonH 14%, 1.7) | 3181025–3181071 | 47 × 10k | 15.9 | 2.32 | pilot job (10k) |
| T_ttbar_mlm | ttbar | 1.8e+05 ⇒ 1 ⇒ 1.8e+05 (MG5 LO gridpack at the generator cuts; K = 1 (LO; normalisation unc. in 06)) | one = 1 | use_syst=False, ickkw=1, ptheavy=250, xqcut=30; T_ttbar_mlm_twin: loss +7±11 % (k=291/101); ok (sample-level (VBS and tag-weighted stages): loss-1.645 err <= 5 %) | effective-N | N_eff ≥ 10 | 110,000 (100,000) | 29.4 / 29.4 / 29.4 (b-b 68%, 16.4; l-b 10%, 11.4) | 3131020–3131020 | 1 × 10k | 0.3 | 0.14 | 884945 |
| H_VBFH_bb | single_H | 2.46e+03 ⇒ 1 ⇒ 2.46e+03 (MG5 LO gridpack at the generator cuts; K = 1 (LO; normalisation unc. in 06)) | B_bb = 0.5824 | deltaeta=2.5, xetamin=200; H_VBFH_bb_twin: loss +3±36 % (k=15/14); ok (impact-level: share x UL95(loss) <= 5 % of total SR background and share < 10 %) | effective-N via bound (UL < 1 % of total SR bkg) | N_eff ≥ 10 | 50,000 (50,000) | 0.433 / 0.425 / 0.421 (l-Hbb 71%, 0.6; b-Hbb 28%, 0.1) | pilot only | 0 | 0.0 | 0.12 | 884462 |
| H_ZH_Zqq_bb | single_H | 84.4 ⇒ 1 ⇒ 84.4 (MG5 LO gridpack at the generator cuts; K = 1 (LO; normalisation unc. in 06)) | B_Zqq×B_bb = 0.4072 | ptheavy=150; H_ZH_Zqq_bb_twin: loss +3±24 % (k=54/23); ok (impact-level: share x UL95(loss) <= 5 % of total SR background and share < 10 %) | full-N (D-HH-12) | N ≥ 103,068 | 110,000 (50,000) | 20.3 / 19.8 / 19.6 (l-Hbb 59%, 26.4; bb_nonH-Hbb 28%, 2.5) | 3141015–3141020 | 6 × 10k | 1.8 | 0.38 | 884462 |
| H_WH_Wqq_bb | single_H | 152 ⇒ 1 ⇒ 152 (MG5 LO gridpack at the generator cuts; K = 1 (LO; normalisation unc. in 06)) | B_Wqq×B_bb = 0.3926 | ptheavy=150; H_WH_Wqq_bb_twin: loss -22±34 % (k=50/17); ok (impact-level: share x UL95(loss) <= 5 % of total SR background and share < 10 %) | full-N (D-HH-12) | N ≥ 179,613 | 180,000 (50,000) | 12.8 / 12.6 / 12.6 (c-Hbb 70%, 7.5; l-Hbb 30%, 6.4) | 3142015–3142027 | 13 × 10k | 3.6 | 0.63 | 884941 |
| H_ttH_bb | single_H | 248 ⇒ 1 ⇒ 248 (MG5 LO gridpack at the generator cuts; K = 1 (LO; normalisation unc. in 06)) | B_bb = 0.5824 | ptheavy=150; H_ttH_bb_twin: loss -0±8 % (k=340/253); ok (impact-level: share x UL95(loss) <= 5 % of total SR background and share < 10 %) | full-N (D-HH-12) | N ≥ 433,306 | 440,000 (50,000) | 311 / 230 / 199 (b-Hbb 71%, 134.3; b-b 6%, 141.9) | 3144015–3144053 | 39 × 10k | 11.4 | 2.02 | 884462 |
| H_ggH_jj_heft | single_H | 2.64e+03 ⇒ 1 ⇒ 2.64e+03 (MG5 LO gridpack at the generator cuts; K = 1 (LO; normalisation unc. in 06)) | B_bb = 0.5824 | deltaeta=3.0, xetamin=400; H_ggH_jj_heft_twin: loss +9±21 % (k=46/34); ok (impact-level: share x UL95(loss) <= 5 % of total SR background and share < 10 %) | effective-N via bound (UL < 1 % of total SR bkg) | N_eff ≥ 10 | 50,000 (50,000) | 2.76 / 2.73 / 2.72 (l-Hbb 73%, 2.5; c-Hbb 27%, 0.5) | pilot only | 0 | 0.0 | 0.13 | 884943 |
| V_Zjj_QCD_vbs | V+jets | 2.7e+05 ⇒ 1 ⇒ 2.7e+05 (MG5 LO gridpack at the generator cuts; K = 1 (LO; normalisation unc. in 06)) | B_Zqq = 0.6991 | deltaeta=3.0, xetamin=400; V_Zjj_QCD_vbs_twin: loss +20±25 % (k=35/15); ok (impact-level: share x UL95(loss) <= 5 % of total SR background and share < 10 %) | effective-N via bound (UL < 1 % of total SR bkg) | N_eff ≥ 10 | 50,000 (50,000) | 0.996 / 0.996 / 0.996 (c-b 39%, 0.2; l-c 19%, 0.5) | pilot only | 0 | 0.0 | 0.14 | 884462 |
| V_Wjj_QCD_vbs | V+jets | 8.39e+05 ⇒ 1 ⇒ 8.39e+05 (MG5 LO gridpack at the generator cuts; K = 1 (LO; normalisation unc. in 06)) | B_Wqq = 0.6741 | deltaeta=3.0, xetamin=400; V_Wjj_QCD_vbs_twin: loss +36±23 % (k=22/12); ok (impact-level: share x UL95(loss) <= 5 % of total SR background and share < 10 %) | effective-N via bound (UL < 1 % of total SR bkg) | N_eff ≥ 10 | 50,000 (50,000) | 0.316 / 0.316 / 0.316 (c-b 41%, 0.1; l-c 26%, 0.2) | pilot only | 0 | 0.0 | 0.14 | 884943 |
| V_ZZjj_EW | VBS_VV | 76.5 ⇒ 1 ⇒ 76.5 (MG5 LO gridpack at the generator cuts; K = 1 (LO; normalisation unc. in 06)) | B_Zqq@Z1×B_Zqq@Z2 = 0.4887 | deltaeta=2.5, xetamin=200; V_ZZjj_EW_twin: loss +2±6 % (k=555/499); ok (sample-level (VBS and tag-weighted stages): loss-1.645 err <= 5 %) | full-N (D-HH-12) | N ≥ 112,167 | 120,000 (50,000) | 54.1 / 54.1 / 54.1 (l-bb_nonH 26%, 22.4; c-bb_nonH 18%, 7.8) | 3153015–3153021 | 7 × 10k | 1.9 | 0.44 | 884462 |
| T_ttbar_boost | ttbar | 3.08e+04 ⇒ 1 ⇒ 3.08e+04 (MG5 LO gridpack at the generator cuts; K = 1 (LO; normalisation unc. in 06)) | one = 1 | ptheavy=250; T_ttbar_boost_twin: loss +22±8 % (k=385/113); NOT ok (FAILED) | effective-N | cross-check / bound | 50,000 (50,000) | 50.9 / 50.9 / 50.9 (b-b 77%, 34.9; b-top 6%, 4.8) | pilot only | 0 | 0.0 | 0.25 | 884462 |
| Q_4b_ht | QCD_multijet | 4.14e+03 ⇒ 1 ⇒ 4.14e+03 (MG5 LO gridpack at the generator cuts; K = 1 (LO; normalisation unc. in 06)) | one = 1 | ihtmin=500; inherited from Q_4j_vbs: NOT ok | effective-N | cross-check / bound | 50,000 (50,000) | 11 / 11 / 11 (b-bb_nonH 44%, 4.8; bb_nonH-bb_nonH 42%, 4.6) | pilot only | 0 | 0.0 | 0.24 | 884943 |
| Q_4j_vbs | QCD_multijet | 3.77e+07 ⇒ 1 ⇒ 3.77e+07 (MG5 LO gridpack at the generator cuts; K = 1 (LO; normalisation unc. in 06)) | one = 1 | deltaeta=3.0, xetamin=400, ihtmin=500; Q_4j_vbs_twin: loss +25±5 % (k=854/322); NOT ok (FAILED) | effective-N | cross-check / bound | 100,000 (100,000) | 11.5 / 11.5 / 11.5 (l-l 29%, 18.6; l-c 25%, 7.9) | pilot only | 0 | 0.0 | 0.52 | 884577 |
| Q_bbjj_vbs | QCD_multijet | 7.25e+05 ⇒ 1 ⇒ 7.25e+05 (MG5 LO gridpack at the generator cuts; K = 1 (LO; normalisation unc. in 06)) | one = 1 | deltaeta=3.0, xetamin=400, ihtmin=500; Q_bbjj_vbs_twin: loss +29±6 % (k=700/180); NOT ok (FAILED) | effective-N | cross-check / bound | 100,000 (100,000) | 12.5 / 12.5 / 12.5 (b-b 32%, 2.7; l-bb_nonH 15%, 6.5) | pilot only | 0 | 0.0 | 0.50 | 884464 |
| X_tW_boost | extra_bkg | 1.83e+03 ⇒ 1 ⇒ 1.83e+03 (MG5 LO gridpack at the generator cuts; K = 1 (LO; normalisation unc. in 06)) | one = 1 | ptheavy=250; inherited from T_ttbar_mlm: ok | bound (D-HH-11) | N_eff ≥ 10 | 20,000 (20,000) | 8.88 / 8.88 / 8.88 (b-b 45%, 2.5; c-b 27%, 3.8) | pilot only | 0 | 0.0 | 0.10 | pilot job (10k) |
| X_ttZ_boost | extra_bkg | 162 ⇒ 1 ⇒ 162 (MG5 LO gridpack at the generator cuts; K = 1 (LO; normalisation unc. in 06)) | one = 1 | ptheavy=250; inherited from T_ttbar_mlm: ok | bound (D-HH-11) | N_eff ≥ 10 | 20,000 (20,000) | 32.2 / 32.2 / 32.2 (b-b 39%, 9; b-bb_nonH 18%, 4.1) | pilot only | 0 | 0.0 | 0.11 | pilot job (10k) |
| X_ttW_boost | extra_bkg | 104 ⇒ 1 ⇒ 104 (MG5 LO gridpack at the generator cuts; K = 1 (LO; normalisation unc. in 06)) | one = 1 | ptheavy=250; inherited from T_ttbar_mlm: ok | bound (D-HH-11) | N_eff ≥ 10 | 20,000 (20,000) | 10.9 / 10.9 / 10.9 (b-b 71%, 6.5; c-b 11%, 2.5) | pilot only | 0 | 0.0 | 0.10 | pilot job (10k) |
| X_Zjj_EW_vbs | extra_bkg | 8.78e+03 ⇒ 1 ⇒ 8.78e+03 (MG5 LO gridpack at the generator cuts; K = 1 (LO; normalisation unc. in 06)) | B_Zqq = 0.6991 | deltaeta=2.5, xetamin=200; inherited from V_ZZjj_EW: ok | bound (D-HH-11) | N_eff ≥ 10 | 20,000 (20,000) | 0.404 / 0.404 / 0.404 (l-bb_nonH 57%, 0.3; c-b 28%, 0.1) | pilot only | 0 | 0.0 | 0.05 | pilot job (10k) |
| X_Wjj_EW_vbs | extra_bkg | 9e+04 ⇒ 1 ⇒ 9e+04 (MG5 LO gridpack at the generator cuts; K = 1 (LO; normalisation unc. in 06)) | B_Wqq = 0.6741 | deltaeta=2.5, xetamin=200; inherited from V_ZZjj_EW: ok | bound (D-HH-11) | N_eff ≥ 10 | 20,000 (20,000) | 0.0878 / 0.0878 / 0.0878 (l-c 64%, 0; l-l 36%, 0.1) **cap exceeded → bound** | pilot only | 0 | 0.0 | 0.05 | pilot job (10k) |
| X_ZZ_QCD_boost | extra_bkg | 86.3 ⇒ 1 ⇒ 86.3 (MG5 LO gridpack at the generator cuts; K = 1 (LO; normalisation unc. in 06)) | B_Zqq@Z1×B_Zqq@Z2 = 0.4887 | ptheavy=250; inherited from T_ttbar_mlm: ok | bound (D-HH-11) | N_eff ≥ 10 | 20,000 (20,000) | 7.23 / 7.23 / 7.23 (l-bb_nonH 33%, 2.6; c-bb_nonH 32%, 1.3) | pilot only | 0 | 0.0 | 0.10 | pilot job (10k) |
| X_WZ_QCD_boost | extra_bkg | 163 ⇒ 1 ⇒ 163 (MG5 LO gridpack at the generator cuts; K = 1 (LO; normalisation unc. in 06)) | B_Wqq×B_Zqq = 0.4713 | ptheavy=250; inherited from T_ttbar_mlm: ok | bound (D-HH-11) | N_eff ≥ 10 | 20,000 (20,000) | 4.04 / 4.04 / 4.04 (l-bb_nonH 38%, 1.9; l-c 21%, 2.6) | pilot only | 0 | 0.0 | 0.10 | pilot job (10k) |
| X_ggZH_loop | extra_bkg | 21.3 ⇒ 1 ⇒ 21.3 (MG5 LO gridpack at the generator cuts; K = 1 (LO; normalisation unc. in 06)) | B_Zqq×B_bb = 0.4072 | ptheavy=150; inherited from H_ZH_Zqq_bb: ok | bound (D-HH-11) | N_eff ≥ 10 | 20,000 (20,000) | 9.28 / 8.61 / 8.34 (l-Hbb 40%, 8.5; bb_nonH-Hbb 27%, 1.1) | pilot only | 0 | 0.0 | 0.08 | pilot job (10k) |

New events beyond the pilots: **3,450,000** in **345** jobs; new CPU **135 wall-h**; storage of all planned samples (pilot + new) **19.2 GB** (new: 13.4 GB).

**Rules used** (declared in `g2_plan.py`, all derived from the G1 decisions): full-N = max(50 k, σ·BR·3000 fb⁻¹) rounded up to 10 k for signal, closure, ggF HH (σ with K), ZH, **WH (added to D-HH-12 by the same cost argument)**, ZZjj, ttH. Effective-N backgrounds: N such that the projected N_eff in the SR ≥ target (10; 30 for a background with > 10 % share) in **all three** tagging scenarios, ×1.5 safety, capped at 3 M events/sample; if the nominal 95 % UL on the SR yield is < 1 % of the total SR background the sample is bound-only (structured Poisson-95 % record + conservative variant, SPEC §4.3(3)), no further events.

## 5. Generator-filter twins (D-HH-6, review item 8)
Delphes level, in the boosted tail (stages: ≥2 fat jets pT ≥ 300; + lead ≥ 450; + VBS pair [reco SR before the window]; + both m_SD in [90,150]; `tagw` = nominal-tag-weighted VBS stage). Loss = 1 − rate(nominal)/rate(twin); `twin_ok` = loss − 1.645·err ≤ 5 % at the VBS stage **and at the tag-weighted stage** (G2 item 5: SR yields are tag-weighted); "stat-limited" if err > 10 %. For sub-dominant backgrounds an impact-level criterion (share × UL95(loss) ≤ 5 % of the total SR background, share < 10 %) is also used (**D-HH-14**). Twin loosening: QCD ihtmin 500→350 and VBS 3.0/400→2.0/200; tt̄ ptheavy 250→150; VBF H / ZZjj VBS 2.5/200→1.5/100; ZH, WH, ttH ptheavy 150→100; Z/W+jets, ggH+jj VBS 3.0/400→2.0/200; signal: no VBS filter. Boosted-tail evidence for the signal (κ2V = 0 twin: loss −2.2 ± 3.7 % at the VBS stage, −5.5 ± 5.4 % in the raw SR) shows the signal generator filter is safe; the SM twin is statistics-limited (+26 ± 14 %, 47/69 events).
| nominal (N) | twin (N) | stage | k_nom | k_twin | loss ± stat | loss UL95 | twin_ok / stat-limited |
|---|---|---|---|---|---|---|---|
| Q_4j_vbs (100000) | Q_4j_vbs_twin (200000) | two | 7791 | 3860 | +42.9 ± 1.1 % | +44.8 % |  |
| Q_4j_vbs (100000) | Q_4j_vbs_twin (200000) | lead | 2829 | 1396 | +42.7 ± 1.9 % | +45.8 % |  |
| Q_4j_vbs (100000) | Q_4j_vbs_twin (200000) | vbs | 854 | 322 | +25.0 ± 4.9 % | +33.1 % | False / False |
| Q_4j_vbs (100000) | Q_4j_vbs_twin (200000) | win | 26 | 6 | -22.6 ± 55.5 % | +68.8 % |  |
| Q_4j_vbs (100000) | Q_4j_vbs_twin (200000) | tagw | 854 | 322 | +26.9 ± 4.8 % | +34.7 % |  |
| Q_bbjj_vbs (100000) | Q_bbjj_vbs_twin (150000) | two | 6885 | 2327 | +46.1 ± 1.3 % | +48.3 % |  |
| Q_bbjj_vbs (100000) | Q_bbjj_vbs_twin (150000) | lead | 2393 | 758 | +42.5 ± 2.4 % | +46.5 % |  |
| Q_bbjj_vbs (100000) | Q_bbjj_vbs_twin (150000) | vbs | 700 | 180 | +29.2 ± 5.9 % | +38.9 % | False / False |
| Q_bbjj_vbs (100000) | Q_bbjj_vbs_twin (150000) | win | 22 | 6 | +33.2 ± 30.7 % | +83.8 % |  |
| Q_bbjj_vbs (100000) | Q_bbjj_vbs_twin (150000) | tagw | 700 | 180 | +31.7 ± 5.7 % | +41.1 % |  |
| T_ttbar_mlm (100000) | T_ttbar_mlm_twin (100000) | two | 4736 | 1542 | +0.7 ± 2.9 % | +5.5 % |  |
| T_ttbar_mlm (100000) | T_ttbar_mlm_twin (100000) | lead | 2386 | 759 | -1.7 ± 4.2 % | +5.3 % |  |
| T_ttbar_mlm (100000) | T_ttbar_mlm_twin (100000) | vbs | 291 | 101 | +6.8 ± 10.8 % | +24.5 % | True / True |
| T_ttbar_mlm (100000) | T_ttbar_mlm_twin (100000) | win | 22 | 1 | -611.5 ± 727.5 % | +585.2 % |  |
| T_ttbar_mlm (100000) | T_ttbar_mlm_twin (100000) | tagw | 291 | 101 | +16.6 ± 9.6 % | +32.4 % |  |
| T_ttbar_boost (50000) | T_ttbar_boost_twin (50000) | two | 8073 | 2074 | +10.6 ± 2.2 % | +14.3 % |  |
| T_ttbar_boost (50000) | T_ttbar_boost_twin (50000) | lead | 3467 | 940 | +15.3 ± 3.1 % | +20.5 % |  |
| T_ttbar_boost (50000) | T_ttbar_boost_twin (50000) | vbs | 385 | 113 | +21.8 ± 8.4 % | +35.6 % | False / False |
| T_ttbar_boost (50000) | T_ttbar_boost_twin (50000) | win | 41 | 10 | +5.9 ± 33.2 % | +60.5 % |  |
| T_ttbar_boost (50000) | T_ttbar_boost_twin (50000) | tagw | 385 | 113 | +16.6 ± 8.9 % | +31.2 % |  |
| H_VBFH_bb (50000) | H_VBFH_bb_twin (50000) | two | 255 | 278 | +17.3 ± 7.2 % | +29.1 % |  |
| H_VBFH_bb (50000) | H_VBFH_bb_twin (50000) | lead | 102 | 100 | +8.0 ± 12.9 % | +29.3 % |  |
| H_VBFH_bb (50000) | H_VBFH_bb_twin (50000) | vbs | 15 | 14 | +3.3 ± 35.9 % | +62.4 % | True / True |
| H_VBFH_bb (50000) | H_VBFH_bb_twin (50000) | win | 1 | 2 | +54.9 ± 55.2 % | +145.8 % |  |
| H_VBFH_bb (50000) | H_VBFH_bb_twin (50000) | tagw | 15 | 14 | -38.3 ± 51.4 % | +46.2 % |  |
| H_ZH_Zqq_bb (50000) | H_ZH_Zqq_bb_twin (50000) | two | 4013 | 1678 | +1.6 ± 2.9 % | +6.3 % |  |
| H_ZH_Zqq_bb (50000) | H_ZH_Zqq_bb_twin (50000) | lead | 1621 | 667 | +0.0 ± 4.6 % | +7.6 % |  |
| H_ZH_Zqq_bb (50000) | H_ZH_Zqq_bb_twin (50000) | vbs | 54 | 23 | +3.4 ± 24.1 % | +43.0 % | True / True |
| H_ZH_Zqq_bb (50000) | H_ZH_Zqq_bb_twin (50000) | win | 10 | 5 | +17.7 ± 45.1 % | +91.9 % |  |
| H_ZH_Zqq_bb (50000) | H_ZH_Zqq_bb_twin (50000) | tagw | 54 | 23 | +28.6 ± 17.8 % | +57.8 % |  |
| H_ttH_bb (50000) | H_ttH_bb_twin (50000) | two | 4248 | 3232 | +1.8 ± 2.3 % | +5.6 % |  |
| H_ttH_bb (50000) | H_ttH_bb_twin (50000) | lead | 2297 | 1722 | +0.3 ± 3.2 % | +5.6 % |  |
| H_ttH_bb (50000) | H_ttH_bb_twin (50000) | vbs | 340 | 253 | -0.4 ± 8.3 % | +13.3 % | True / False |
| H_ttH_bb (50000) | H_ttH_bb_twin (50000) | win | 52 | 24 | -61.9 ± 40.0 % | +3.8 % |  |
| H_ttH_bb (50000) | H_ttH_bb_twin (50000) | tagw | 340 | 253 | +19.0 ± 6.7 % | +30.1 % |  |
| V_Zjj_QCD_vbs (50000) | V_Zjj_QCD_vbs_twin (50000) | two | 331 | 234 | +51.4 ± 4.1 % | +58.3 % |  |
| V_Zjj_QCD_vbs (50000) | V_Zjj_QCD_vbs_twin (50000) | lead | 131 | 95 | +52.6 ± 6.4 % | +63.1 % |  |
| V_Zjj_QCD_vbs (50000) | V_Zjj_QCD_vbs_twin (50000) | vbs | 35 | 15 | +19.9 ± 24.7 % | +60.6 % | True / True |
| V_Zjj_QCD_vbs (50000) | V_Zjj_QCD_vbs_twin (50000) | win | 3 | 0 | n/a | n/a | |
| V_Zjj_QCD_vbs (50000) | V_Zjj_QCD_vbs_twin (50000) | tagw | 35 | 15 | +48.8 ± 15.8 % | +74.8 % |  |
| V_ZZjj_EW (50000) | V_ZZjj_EW_twin (50000) | two | 3490 | 4166 | +26.3 ± 1.7 % | +29.1 % |  |
| V_ZZjj_EW (50000) | V_ZZjj_EW_twin (50000) | lead | 1959 | 2434 | +29.2 ± 2.2 % | +32.7 % |  |
| V_ZZjj_EW (50000) | V_ZZjj_EW_twin (50000) | vbs | 555 | 499 | +2.1 ± 6.0 % | +12.0 % | True / False |
| V_ZZjj_EW (50000) | V_ZZjj_EW_twin (50000) | win | 59 | 46 | -12.9 ± 22.2 % | +23.6 % |  |
| V_ZZjj_EW (50000) | V_ZZjj_EW_twin (50000) | tagw | 555 | 499 | +13.5 ± 5.3 % | +22.2 % |  |
| H_ggH_jj_heft (50000) | H_ggH_jj_heft_twin (50000) | two | 546 | 511 | +28.1 ± 4.4 % | +35.4 % |  |
| H_ggH_jj_heft (50000) | H_ggH_jj_heft_twin (50000) | lead | 249 | 236 | +29.0 ± 6.5 % | +39.6 % |  |
| H_ggH_jj_heft (50000) | H_ggH_jj_heft_twin (50000) | vbs | 46 | 34 | +8.9 ± 20.6 % | +42.8 % | True / True |
| H_ggH_jj_heft (50000) | H_ggH_jj_heft_twin (50000) | win | 3 | 4 | +49.5 ± 38.6 % | +112.9 % |  |
| H_ggH_jj_heft (50000) | H_ggH_jj_heft_twin (50000) | tagw | 46 | 34 | +26.4 ± 16.6 % | +53.8 % |  |
| H_WH_Wqq_bb (50000) | H_WH_Wqq_bb_twin (50000) | two | 4122 | 1778 | +4.0 ± 2.7 % | +8.5 % |  |
| H_WH_Wqq_bb (50000) | H_WH_Wqq_bb_twin (50000) | lead | 1660 | 703 | +2.3 ± 4.4 % | +9.5 % |  |
| H_WH_Wqq_bb (50000) | H_WH_Wqq_bb_twin (50000) | vbs | 50 | 17 | -21.8 ± 34.2 % | +34.5 % | True / True |
| H_WH_Wqq_bb (50000) | H_WH_Wqq_bb_twin (50000) | win | 2 | 2 | +58.6 ± 41.4 % | +126.7 % |  |
| H_WH_Wqq_bb (50000) | H_WH_Wqq_bb_twin (50000) | tagw | 50 | 17 | -27.9 ± 35.9 % | +31.2 % |  |
| V_Wjj_QCD_vbs (50000) | V_Wjj_QCD_vbs_twin (50000) | two | 243 | 195 | +56.7 ± 4.2 % | +63.5 % |  |
| V_Wjj_QCD_vbs (50000) | V_Wjj_QCD_vbs_twin (50000) | lead | 84 | 73 | +60.0 ± 6.4 % | +70.5 % |  |
| V_Wjj_QCD_vbs (50000) | V_Wjj_QCD_vbs_twin (50000) | vbs | 22 | 12 | +36.3 ± 22.9 % | +73.9 % | False / True |
| V_Wjj_QCD_vbs (50000) | V_Wjj_QCD_vbs_twin (50000) | win | 0 | 0 | n/a | n/a | |
| V_Wjj_QCD_vbs (50000) | V_Wjj_QCD_vbs_twin (50000) | tagw | 22 | 12 | +40.6 ± 21.3 % | +75.7 % |  |
| S_HHjj_kV1_k2V1_kl1 (20000) | S_HHjj_SM_twin_loose (30000) | two | 279 | 1044 | +70.9 ± 2.0 % | +74.2 % |  |
| S_HHjj_kV1_k2V1_kl1 (20000) | S_HHjj_SM_twin_loose (30000) | lead | 140 | 529 | +71.2 ± 2.7 % | +75.7 % |  |
| S_HHjj_kV1_k2V1_kl1 (20000) | S_HHjj_SM_twin_loose (30000) | vbs | 47 | 69 | +26.0 ± 14.0 % | +49.0 % | False / True |
| S_HHjj_kV1_k2V1_kl1 (20000) | S_HHjj_SM_twin_loose (30000) | win | 17 | 18 | -2.7 ± 34.7 % | +54.5 % |  |
| S_HHjj_kV1_k2V1_kl1 (20000) | S_HHjj_SM_twin_loose (30000) | tagw | 47 | 69 | +7.8 ± 17.4 % | +36.5 % |  |
| S_HHjj_kV1_k2V0_kl1 (20000) | S_HHjj_kV1_k2V0_kl1_twin (20000) | two | 3815 | 3659 | +0.5 ± 2.3 % | +4.2 % |  |
| S_HHjj_kV1_k2V0_kl1 (20000) | S_HHjj_kV1_k2V0_kl1_twin (20000) | lead | 2658 | 2516 | -0.9 ± 2.8 % | +3.7 % |  |
| S_HHjj_kV1_k2V0_kl1 (20000) | S_HHjj_kV1_k2V0_kl1_twin (20000) | vbs | 1573 | 1470 | -2.2 ± 3.7 % | +3.9 % | True / False |
| S_HHjj_kV1_k2V0_kl1 (20000) | S_HHjj_kV1_k2V0_kl1_twin (20000) | win | 791 | 716 | -5.5 ± 5.4 % | +3.5 % |  |
| S_HHjj_kV1_k2V0_kl1 (20000) | S_HHjj_kV1_k2V0_kl1_twin (20000) | tagw | 1573 | 1470 | -3.6 ± 3.8 % | +2.6 % |  |

**ttH is covered only by the impact criterion (D-HH-14b):** its tag-weighted loss is +19.0 ± 6.7 % (loss − 1.645σ = 8 % > 5 %), so it fails the sample-level test; its SR share is 0.04 %. ZZjj (+13.5 ± 5.3 %, 4.8 % after the 1.645σ allowance) passes only marginally; ZH, Z/W+jets, ggH+jj and the SM signal twin show the same positive trend but are statistics-limited (errors 17–50 %).
Reading: (i) **QCD multijet and PS-only tt̄ filters are unsafe** (+25 %, +29 %, +22 % at the VBS stage) → production with the looser QCD filter (§4); the PS-only tt̄ is a cross-check only. (ii) tt̄ MLM (nominal): +6.8 ± 10.8 % (stat-limited, sample-level pass). (iii) Single-H, V+jets, ggH+jj twins are statistics-limited (errors 20–35 %); they enter through the impact criterion (their shares are ≤ 10⁻³ of the SR background), flagged in D-HH-14. The bound samples inherit the filter evidence of the sample type they share it with (stated in the table; not independently tested).

## 6. Class-resolved N_eff projection (review item 6, D-HH-4)
Method (`scripts/neff_project.py`): V = events with 2 fat jets + VBS pair; p_win(class) = fraction of selected fat jets of that class in m_SD [90,150]; hard-window SR statistic has E[Σw] = Σ_V p·w, E[Σw²] = Σ_V p·w², so N_eff,proj = (Σp·w)²/Σp·w², linear in N. Check vs the direct hard-window count in the pilot: e.g. Q_4j (twin config / nominal) 11.5 projected vs 18.3 direct (N_eff of 26 raw events), tt̄ MLM 26.7 vs 13.8, ttH 26.1 vs 23.1 (factorisation approximate; the direct count is stat-limited). The weights span 1e-4 (l,l) … 0.36 (Hbb,Hbb); the rare PS g→bb̄ (bb_nonH) and b classes carry 15–30 % of the weight with class N_eff ≲ 2, so N_eff of the *total* is set by the l-l/l-c classes plus these, hence a target of 30 for the dominant QCD sample. **Sizing (G2 item 9):** the factorised projection overestimates the direct hard-window count by up to 2× (tt̄ 26.7 vs 13.8), so N_planned now uses min(projection, measured pilot N_eff) scaled linearly, ×1.5, target 10 (30 for QCD Q_4j). Top-up rule (pre-declared, `config/g2_predeclared.yaml`): if `nmc_post_production.py` fails, one top-up of 1.2·N_planned·(target/N_eff,meas − 1) events, then bound-only. **b-enrichment strategy:** Q_bbjj (ME b b̄) and Q_4b (ME 4b, bound/shape only) cover the b classes; flavour partition O1 removes bb̄-containing events from Q_4j (1.5 %), replacing them with Q_bbjj; a dedicated PS g→bb̄ filter is not needed if the planned Q_4j events reach the target.
| sample | pilot N | pre-window events V | raw SR | N_eff proj. (pilot, p/n/o) | class pair | share of E[Σw] | N_eff proj. of the class (nominal, at the PILOT N) |
|---|---|---|---|---|---|---|---|
| Q_4j_vbs | 100000 | 854 | 26 | 11.5 / 11.5 / 11.5 | l-l (V=595) | 29 % | 18.6 |
| | | | | | l-c (V=179) | 25 % | 7.91 |
| | | | | | l-bb_nonH (V=44) | 19 % | 2.37 |
| | | | | | c-bb_nonH (V=5) | 6 % | 0.38 |
| Q_bbjj_vbs | 100000 | 700 | 22 | 12.5 / 12.5 / 12.5 | b-b (V=120) | 32 % | 2.7 |
| | | | | | l-bb_nonH (V=114) | 15 % | 6.51 |
| | | | | | l-b (V=324) | 15 % | 6.37 |
| | | | | | bb_nonH-bb_nonH (V=6) | 14 % | 1.14 |
| Q_4b_ht | 50000 | 240 | 9 | 11 / 11 / 11 | b-bb_nonH (V=94) | 44 % | 4.81 |
| | | | | | bb_nonH-bb_nonH (V=23) | 42 % | 4.61 |
| | | | | | b-b (V=107) | 13 % | 1.4 |
| | | | | | l-bb_nonH (V=4) | 0 % | 0.273 |
| T_ttbar_mlm | 100000 | 291 | 22 | 26.7 / 26.7 / 26.7 | b-b (V=63) | 68 % | 14.9 |
| | | | | | l-b (V=97) | 10 % | 10.4 |
| | | | | | c-b (V=29) | 9 % | 4.8 |
| | | | | | b-top (V=18) | 6 % | 2.06 |
| H_ttH_bb | 50000 | 340 | 52 | 35.4 / 26.1 / 22.6 | b-Hbb (V=48) | 71 % | 15.3 |
| | | | | | b-b (V=77) | 6 % | 16.1 |
| | | | | | Hbb-top (V=11) | 5 % | 1.76 |
| | | | | | bb_nonH-Hbb (V=3) | 5 % | 0.979 |
| V_Zjj_QCD_vbs | 50000 | 35 | 3 | 0.996 / 0.996 / 0.996 | c-b (V=2) | 39 % | 0.223 |
| | | | | | l-c (V=7) | 19 % | 0.528 |
| | | | | | l-l (V=22) | 18 % | 1.02 |
| | | | | | l-b (V=2) | 12 % | 0.136 |
| V_Wjj_QCD_vbs | 50000 | 22 | 0 | 0.316 / 0.316 / 0.316 | c-b (V=1) | 41 % | 0.0718 |
| | | | | | l-c (V=6) | 26 % | 0.225 |
| | | | | | l-l (V=14) | 20 % | 0.34 |
| | | | | | l-b (V=1) | 13 % | 0.0466 |
| H_ggH_jj_heft | 50000 | 46 | 3 | 2.76 / 2.73 / 2.72 | l-Hbb (V=28) | 73 % | 2.52 |
| | | | | | c-Hbb (V=5) | 27 % | 0.464 |
| | | | | | l-b (V=8) | 0 % | 0.08 |
| | | | | | l-bb_nonH (V=1) | 0 % | 0.0234 |
| V_ZZjj_EW | 50000 | 555 | 59 | 22.5 / 22.5 / 22.5 | l-bb_nonH (V=90) | 26 % | 9.34 |
| | | | | | c-bb_nonH (V=23) | 18 % | 3.24 |
| | | | | | l-c (V=131) | 14 % | 12.7 |
| | | | | | l-l (V=247) | 10 % | 17.6 |
| H_ZH_Zqq_bb | 50000 | 54 | 10 | 9.2 / 9 / 8.93 | l-Hbb (V=28) | 59 % | 12 |
| | | | | | bb_nonH-Hbb (V=3) | 28 % | 1.15 |
| | | | | | c-Hbb (V=3) | 11 % | 1.15 |
| | | | | | l-bb_nonH (V=3) | 0 % | 0.627 |
| H_WH_Wqq_bb | 50000 | 50 | 2 | 3.56 / 3.51 / 3.49 | c-Hbb (V=14) | 70 % | 2.07 |
| | | | | | l-Hbb (V=13) | 30 % | 1.78 |
| | | | | | l-b (V=13) | 0 % | 0.184 |
| | | | | | l-c (V=5) | 0 % | 0.13 |
| H_VBFH_bb | 50000 | 15 | 1 | 0.433 / 0.425 / 0.421 | l-Hbb (V=12) | 71 % | 0.641 |
| | | | | | b-Hbb (V=1) | 28 % | 0.0513 |
| | | | | | c-bb_nonH (V=1) | 1 % | 0.0364 |
| | | | | | l-b (V=1) | 0 % | 0.00342 |

## 7. D-HH-7 and D-HH-11 outcomes
**D-HH-7** (ME+jets sample only if the PS-based SR yield of that background is > 10 % of the total SR background; nominal tagging, shares also for the other scenarios):
| background | ME+jets sample in question | expected SR events @500 fb⁻¹ (pess/nom/opt, smoothed estimator) | share of total SR bkg (nominal) | > 10 %? | outcome |
|---|---|---|---|---|---|
| V_Zjj_QCD_vbs | Z+3j | 4.28 / 1.07 / 0.267 | 0.052 % (pess 0.052 %, opt 0.052 %) | no | 100 % PS-modelling uncertainty |
| V_Wjj_QCD_vbs | W+3j | 3.94 / 0.985 / 0.246 | 0.048 % (pess 0.048 %, opt 0.047 %) | no | 100 % PS-modelling uncertainty |
| H_ZH_Zqq_bb | VH+2j | 0.0633 / 0.0417 / 0.0259 | 0.002 % (pess 0.00077 %, opt 0.005 %) | no | 100 % PS-modelling uncertainty |
| H_WH_Wqq_bb | VH+2j | 0.0323 / 0.0214 / 0.0133 | 0.001 % (pess 0.00039 %, opt 0.0026 %) | no | 100 % PS-modelling uncertainty |
| H_ggH_jj_heft | ggH+3j | 0.482 / 0.319 / 0.199 | 0.015 % (pess 0.0058 %, opt 0.038 %) | no | 100 % PS-modelling uncertainty |

Total SR background (sum of the main backgrounds, 500 fb⁻¹, smoothed estimator, before the multijet ±100 %): pessimistic 8.26e+03, nominal 2.07e+03, optimistic 518 events.
No background passes: all are ≲ 0.05 % of the SR background (QCD dominates), so **no Z/W+3j, VH+2j or ggH+jj sample; apply a 100 % PS-modelling uncertainty** to these backgrounds. 
**UL definition (G2-FIX):** the bound is the *larger* of (i) the class-aware smoothed-estimator UL and (ii) the direct hard-window proper Poisson 95 % UL, E_direct × Poisson95(k)/k with k the raw SR count (e.g. tW: k = 11, Poisson95(11) = 18.2, E_direct = 0.53 events ⇒ 0.88 events; the class-aware value is 0.82), recomputable by `nmc_check_hh` (methods `poisson95_direct`, `poisson95_classaware`). **D-HH-11** (95 % UL in the SR for each extra background; dedicated sample only if UL > 10 % of the total SR background; gg→ZH, EW Wjj and QCD WZ were added to the original list and now have σ + pilot):
| extra background | pilot N | raw SR count | expected SR @500 fb⁻¹ (nominal, smoothed) | 95 % UL (nominal; class-aware Poisson) | UL / total SR bkg | UL > 10 %? | outcome |
|---|---|---|---|---|---|---|---|
| X_tW_boost | 20000 | 11 | 0.65 | 0.879 (pess 3.52, opt 0.22) | 0.043 % | no | bound only: UL enters as an extra background term in the conservative variant (work/g2/conservative_variant.json) |
| X_ttZ_boost | 20000 | 29 | 0.234 | 0.268 (pess 1.07, opt 0.0669) | 0.013 % | no | bound only: UL enters as an extra background term in the conservative variant (work/g2/conservative_variant.json) |
| X_ttW_boost | 20000 | 7 | 0.0594 | 0.0747 (pess 0.299, opt 0.0187) | 0.0036 % | no | bound only: UL enters as an extra background term in the conservative variant (work/g2/conservative_variant.json) |
| X_Zjj_EW_vbs | 20000 | 0 | 0.0364 | 0.0752 (pess 0.301, opt 0.0188) | 0.0036 % | no | bound only: UL enters as an extra background term in the conservative variant (work/g2/conservative_variant.json) |
| X_Wjj_EW_vbs | 20000 | 0 | 0.0219 | 0.0491 (pess 0.196, opt 0.0123) | 0.0024 % | no | bound only: UL enters as an extra background term in the conservative variant (work/g2/conservative_variant.json) |
| X_ZZ_QCD_boost | 20000 | 10 | 0.00418 | 0.00626 (pess 0.025, opt 0.00157) | 0.0003 % | no | bound only: UL enters as an extra background term in the conservative variant (work/g2/conservative_variant.json) |
| X_WZ_QCD_boost | 20000 | 3 | 0.00474 | 0.0134 (pess 0.0536, opt 0.00335) | 0.00065 % | no | bound only: UL enters as an extra background term in the conservative variant (work/g2/conservative_variant.json) |
| X_ggZH_loop | 20000 | 14 | 0.0277 | 0.0422 (pess 0.067, opt 0.0258) | 0.002 % | no | bound only: UL enters as an extra background term in the conservative variant (work/g2/conservative_variant.json) |
**t-channel single top (G2 item 12, added):** σ_LO(t+t̄, ptheavy 250) = 2.894 ± 0.024 pb (interactive MG5 σ-only run in the private copy `work/mg5priv`, 2 cores, 500 events; retained log `work/g2/tchan/mg5_log_X_tchan_sigma_only.txt` [line "Cross-section : 2.894 +- 0.02351 pb"] and the exact input `work/g2/tchan/run.mg5`, generated from `cards/X_tchan_boost.mg5`; no gridpack/submit file kept since no sample is needed) = 1.58 × σ(tW) (1.831 pb). Bound by σ-ratio: UL ≤ 1.58 × UL(tW) = 1.58 × 0.88 = 1.4 events × an unquantified allowance factor 3 for the forward-jet VBS topology ≈ 4.2 events ≈ 0.2 % of the total SR background < 10 %: **no dedicated sample** (an assumption-based bound; a pilot would replace it if ever needed).
None exceeds 10 % (largest: tW 0.04 %): **no dedicated sample**; the ULs enter the conservative variant (`work/g2/conservative_variant.json`, `conservative_variant_poisson.json`).

## 8. Morphing: Delphes-level SR closure and amplification (review item 3)
**Deliverable statement: the validated result is κ2V at κV = κλ = 1** (closure points T1 = (1,0,1) and T2 = (1,2,1)). κλ and κV are not validated (D-HH-13). Six-point basis (unchanged). Closure at **Delphes level** (stages: two fat jets / + VBS pair / + m_SD window, plus the m(HH)-proxy histogram before the window), from the 20 k-event pilots; errors from the raw counts of all 7 samples. Closure points: T1 (1,0,1), T2 (1,2,1) and **T3 (1.25, 1.5, 2) with κV ≠ 1 and κλ ≠ 1** (probes κV³κλ, κV²κλ², κVκ2Vκλ).
| closure point (κV, κ2V, κλ) | Σ|c_i| | stage | raw k (direct) | predicted [fb] | direct [fb] | pull |
|---|---|---|---|---|---|---|
| (1, 0, 1) | 0.40 | two | 3815 | 1.049 ± 0.022 | 1.079 ± 0.017 | -1.09 |
| (1, 0, 1) | 0.40 | vbs | 1573 | 0.4379 ± 0.014 | 0.445 ± 0.011 | -0.40 |
| (1, 0, 1) | 0.40 | win | 791 | 0.2272 ± 0.01 | 0.2238 ± 0.008 | +0.27 |
| (1, 0, 1) | | m(HH)-proxy histogram, pre-window region | | | | χ²/ndf = 3.3/7 |
| (1, 2, 1) | 2.93 | two | 6425 | 0.9202 ± 0.034 | 0.918 ± 0.011 | +0.06 |
| (1, 2, 1) | 2.93 | vbs | 2842 | 0.404 ± 0.022 | 0.4061 ± 0.0076 | -0.09 |
| (1, 2, 1) | 2.93 | win | 1422 | 0.2033 ± 0.016 | 0.2032 ± 0.0054 | +0.01 |
| (1, 2, 1) | | m(HH)-proxy histogram, pre-window region | | | | χ²/ndf = 6.8/7 |
| (1.25, 1.5, 2) | 5.65 | two | 570 | -0.0116 ± 0.065 | 0.02128 ± 0.00089 | -0.51 |
| (1.25, 1.5, 2) | 5.65 | vbs | 117 | -0.02087 ± 0.041 | 0.004367 ± 0.0004 | -0.61 |
| (1.25, 1.5, 2) | 5.65 | win | 40 | -0.03424 ± 0.03 | 0.001493 ± 0.00024 | -1.21 |
| (1.25, 1.5, 2) | | m(HH)-proxy histogram, pre-window region | | | | χ²/ndf = 1.6/5 |
T1 and T2 close (pulls ≤ 1.1). **T3 is uninformative and is stated as such:** its prediction error exceeds the quantity predicted — 'two' stage −0.012 ± 0.065 fb vs direct 0.021 fb; VBS stage −0.021 ± 0.041 vs 0.0044 fb; window −0.034 ± 0.030 vs 0.0015 fb (pull −1.2) — so the small pulls only show the test has no power there (Σ|c| = 5.65, direct raw SR count 40). The κV ≠ 1 and κλ ≠ 1 monomials are **not validated at Delphes level**; a test with power needs a closure point with a large yield or much larger basis statistics (D-HH-13).
**Σ|c_i| and MC-stat amplification** over the intended scan ranges (κ2V ∈ [−1,3], κλ ∈ [−5,10], κV ∈ [0.5,1.5]); planned N = full-N of §4; relative error = √(Σ c_i² δY_i²)/|Y| of the morphed raw SR yield; absolute error uses ε_H² = 0.36 for illustration:
| scan | κ | Σ|c_i| | morphed SR yield Y [fb] (raw, no tagging) | rel. MC error at pilot N | rel. MC error at planned N | absolute MC error [events @500 fb⁻¹, ε_H²=0.36] at planned N |
|---|---|---|---|---|---|---|
| κ2V (κV=κλ=1) | (1, -1.0, 1) | 2.6 | 0.884 | 0.025 | 0.013 | 2 |
| κ2V (κV=κλ=1) | (1, 0.0, 1) | 0.4 | 0.227 | 0.044 | 0.02 | 0.8 |
| κ2V (κV=κλ=1) | (1, 0.5, 1) | 0.8 | 0.06 | 0.089 | 0.041 | 0.44 |
| κ2V (κV=κλ=1) | (1, 1.0, 1) | 1.0 | 0.000332 | 0.24 | 0.15 | 0.0092 |
| κ2V (κV=κλ=1) | (1, 1.5, 1) | 1.9 | 0.0481 | 0.14 | 0.075 | 0.65 |
| κ2V (κV=κλ=1) | (1, 2.0, 1) | 2.9 | 0.203 | 0.079 | 0.043 | 1.6 |
| κ2V (κV=κλ=1) | (1, 3.0, 1) | 5.4 | 0.836 | 0.05 | 0.029 | 4.3 |
| κλ (κV=κ2V=1) | (1, 1, -5.0) | 25.1 | -0.452 | 0.79 | 0.34 | 28 |
| κλ (κV=κ2V=1) | (1, 1, -2.0) | 5.3 | -0.0885 | 0.79 | 0.34 | 5.4 |
| κλ (κV=κ2V=1) | (1, 1, 0.0) | 1.3 | 0.00128 | 3.5 | 2 | 0.45 |
| κλ (κV=κ2V=1) | (1, 1, 1.0) | 1.0 | 0.000332 | 0.24 | 0.15 | 0.0092 |
| κλ (κV=κ2V=1) | (1, 1, 2.0) | 3.6 | -0.0312 | 0.85 | 0.38 | 2.1 |
| κλ (κV=κ2V=1) | (1, 1, 5.0) | 20.5 | -0.309 | 0.81 | 0.36 | 20 |
| κλ (κV=κ2V=1) | (1, 1, 10.0) | 78.5 | -1.38 | 0.81 | 0.35 | 88 |
| κV (κ2V=κλ=1) | (0.5, 1, 1) | 1.0 | 0.116 | 0.074 | 0.038 | 0.79 |
| κV (κ2V=κλ=1) | (0.7, 1, 1) | 1.1 | 0.0504 | 0.15 | 0.071 | 0.65 |
| κV (κ2V=κλ=1) | (0.9, 1, 1) | 1.1 | 0.0048 | 0.69 | 0.33 | 0.28 |
| κV (κ2V=κλ=1) | (1.1, 1, 1) | 1.5 | 0.0149 | 0.29 | 0.13 | 0.36 |
| κV (κ2V=κλ=1) | (1.3, 1, 1) | 2.6 | 0.125 | 0.13 | 0.06 | 1.4 |
| κV (κ2V=κλ=1) | (1.5, 1, 1) | 4.0 | 0.388 | 0.085 | 0.04 | 2.8 |
Findings: (i) **κ2V scan: ≤ 15 % relative (≤ ~4 events absolute @500 fb⁻¹, largest at κ2V = 3 where the yield is ≈ 150 events) at planned N, worst near the SM point where the yield itself is tiny** — adequate for the primary deliverable. (ii) **κλ scans at κ2V = 1 (relative MC error up to 195 % at planned N, ≥ 34 % everywhere away from the SM point) and κV scans near 1 (33 % at κV = 0.9) are not usable by morphing**: the morphed yield is ≈ 0 ± 34 % × O(0.3 fb) (even negative) because of cancellations among basis points with 10²× larger yields; the physical SR yield there is ≈ 10⁻³ fb (< 1 event). κλ is a secondary result; a 3-point quadratic κλ line at κV = κ2V = 1 needs only the monomials {1, κλ, κλ²}: (1,1,1) (exists) + (1,1,0), (1,1,2) direct samples (+ (1,1,5) closure). **D-HH-13** below.

## 9. tt̄+0,1,2j MLM validation (D-HH-3)
Nominal ME+PS MLM (ickkw=1, xqcut 30, PY8 qCut 40 [1.3×], nJetMax=2, `JetMatching` hook inside DelphesPythia8; 31 % matching acceptance, the matched σ is the PY8 σ and equals σ_MG5 × accepted/processed within 0.4 %: test job 180.3 × 616/2000 = 55.5 pb (PY8 56.07 pb); 100 k-event pilot 54.2 pb (PY8 54.0 pb), the difference being the 2000-event statistics). Matching-scale variation (Delphes level):
| sample | xqcut / qCut | σ_MG5 [pb] | N_LHE | accepted | matching eff. | σ_matched [pb] | ratio to nominal | stage two / lead / VBS (ratio to nominal, ± stat of the ratio) |
|---|---|---|---|---|---|---|---|---|
| T_ttbar_mlm | 30 / 40 | 180.3 | 100000 | 30056 | 0.301 | 54.19 | 1.000 | — |
| T_ttbar_mlm_xq20 | 20 / 26 | 265.9 | 30000 | 6455 | 0.215 | 57.21 | 1.056 | 1.09±0.04 / 1.12±0.05 / 1.23±0.16 |
| T_ttbar_mlm_xq45 | 45 / 60 | 126 | 30000 | 12128 | 0.404 | 50.94 | 0.940 | 0.94±0.03 / 0.95±0.04 / 1.10±0.11 |
| T_ttbar_boost | PS only (0 ME jets) | 30.83 | 50000 | 50000 | 1.000 | 30.83 | 0.569 | — |

Shape comparison to the nominal (bin-wise, stat. errors only; bins with ≥ 5 events in both samples): T_ttbar_mlm_xq20: nj χ²/ndf 20/8, pt1 χ²/ndf 21/7, pt2 χ²/ndf 16/7, pt3 χ²/ndf 20/6, pt4 χ²/ndf 18/5; T_ttbar_mlm_xq45: nj χ²/ndf 49/8, pt1 χ²/ndf 40/7, pt2 χ²/ndf 36/7, pt3 χ²/ndf 39/7, pt4 χ²/ndf 46/6
Reading: σ_matched is stable to ±6 % for xqcut 20↔45 (matched σ 57.2/54.2/50.9 pb); the rate at the 2-fat-jet / lead stages moves by +9…12 % and −5…−6 %, at the VBS stage by +23 ± 16 % and +10 ± 11 %. Shapes show significant but modest differences (χ²/ndf up to ~7, largely the 6 % normalisation shift with tiny statistical errors). This is a **matching-scale variation check, not a DJR plot**: the slim Delphes files contain no hadron-level particles, so a differential-jet-rate histogram was not produced (deviation §13). Treatment (carried to Phase 06 as the tt̄ modelling systematic: **±(10–20) %**, stat-limited, no DJR; accepted at the 2.4 % tt̄ share): nominal xqcut 30; the xqcut 20/45 spread is a tt̄ modelling systematic (≈ ±10 % at the 2-fat-jet stage, ±(10–20) % at the VBS stage, stat-limited). The PS-only tt̄ is 0.57× the MLM σ in the same filter and has a smaller boosted-VBS rate (MLM/PS ≈ 2 at the VBS stage), i.e. the ME jets matter; ttjj ME+filter is **not needed** (N_eff 27 at 100 k events, planned 100 k).

## 10. Pre-declared variations and choices (fixed now; `config/g2_predeclared.yaml`)
Primary result: m(HH)-proxy **unclipped**; variation clipped at < 1.5 TeV plus a < 1.0 TeV check; lead fat-jet trigger **450 GeV baseline**, variations **500, 550**; m_SD window [90,150] (provisional; fixed by expected-only optimisation in Phase 06 on the Delphes peak, 116 GeV; no fat-jet JES) with **±5 % mass-scale** variation; fat-jet pT thresholds 300/450 provisional (D-HH-5); multijet (Q_4j, Q_bbjj, Q_4b) ±100 % and results also with **×0.5 and ×2**; tagging scenarios pessimistic/nominal/optimistic; ggF HH +30 % in the VBF region. The variation code is exercised on the pilots (expected SR events relative to baseline, nominal tagging, smoothed estimator; illustration only):
| sample | baseline SR events @500 fb⁻¹ (nominal, smoothed) | trigger 500 | trigger 550 | m_SD ×0.95 | m_SD ×1.05 | m(HH)<1.5 TeV | m(HH)<1.0 TeV |
|---|---|---|---|---|---|---|---|
| S_HHjj_kV1_k2V1_kl1 | 0.0468 | 0.82 | 0.53 | 0.99 | 0.96 | 0.82 | 0.24 |
| S_HHjj_kV1p5_k2V0_kl1 | 220 | 0.84 | 0.68 | 0.94 | 1.00 | 0.66 | 0.15 |
| S_HHjj_kV1_k2V2_kl1 | 37.9 | 0.86 | 0.72 | 0.95 | 1.01 | 0.62 | 0.14 |
| Q_4j_vbs_twin | 1.87e+03 | 0.59 | 0.40 | 0.89 | 1.03 | 0.76 | 0.27 |
| Q_bbjj_vbs_twin | 146 | 0.59 | 0.36 | 0.89 | 1.07 | 0.67 | 0.23 |
| T_ttbar_mlm | 49.1 | 0.70 | 0.49 | 1.01 | 0.96 | 0.83 | 0.30 |
| H_ttH_bb | 0.928 | 0.71 | 0.39 | 1.06 | 0.91 | 0.90 | 0.31 |
| H_ZH_Zqq_bb | 0.0417 | 0.73 | 0.46 | 0.69 | 1.20 | 0.94 | 0.35 |
| V_ZZjj_EW | 0.00675 | 0.70 | 0.47 | 0.57 | 1.45 | 0.65 | 0.28 |
| G_ggHH_loop_kl1 | 0.923 | 0.83 | 0.66 | 0.99 | 0.95 | 0.83 | 0.50 |
**Effective statistics in the variation regions (G2 item 6) — choice: the variations use the smoothed estimator with its MC error quoted** (rule in `g2_predeclared.yaml`); N_eff of the smoothed estimator (effective number of events entering Σp·w) at planned N:
| sample | N_planned | smoothed N_eff at planned N: baseline | trigger 550 | m(HH)<1.0 TeV | m_SD ×0.95 / ×1.05 | note |
|---|---|---|---|---|---|---|
| S_HHjj_kV1_k2V1_kl1 | 50,000 | 43.2 | 22.6 | 10.3 | 43.1 / 43.2 | N_eff ≥ 10 in all variation regions |
| S_HHjj_kV1p5_k2V0_kl1 | 100,000 | 5155.1 | 3492.4 | 772.3 | 5153.3 / 5156.8 | N_eff ≥ 10 in all variation regions |
| S_HHjj_kV1_k2V2_kl1 | 50,000 | 5280.8 | 3785.4 | 730.6 | 5280.6 / 5281.4 | N_eff ≥ 10 in all variation regions |
| Q_4j_vbs_twin | 1,900,000 | 748.8 | 469.7 | 275.0 | 742.4 / 847.6 | N_eff ≥ 10 in all variation regions |
| Q_bbjj_vbs_twin | 620,000 | 221.6 | 64.0 | 103.3 | 229.4 / 229.2 | N_eff ≥ 10 in all variation regions |
| T_ttbar_mlm | 110,000 | 132.6 | 63.2 | 38.2 | 127.0 / 139.5 | N_eff ≥ 10 in all variation regions |
| H_ttH_bb | 440,000 | 743.4 | 314.4 | 228.3 | 733.4 / 759.1 | N_eff ≥ 10 in all variation regions |
| H_ZH_Zqq_bb | 110,000 | 50.1 | 14.9 | 17.8 | 50.9 / 47.9 | N_eff ≥ 10 in all variation regions |
| V_ZZjj_EW | 120,000 | 433.1 | 229.2 | 82.3 | 419.0 / 385.7 | N_eff ≥ 10 in all variation regions |
| G_ggHH_loop_kl1 | 50,000 | 32.0 | 21.1 | 16.0 | 31.9 / 32.0 | N_eff ≥ 10 in all variation regions |
The hard-window N_eff in these regions is lower (e.g. QCD at trigger 550 keeps ≈ 0.4 of the events) and is not required to reach 10. **Tagging scenarios:** all three scale every mistag class by one common factor (pessimistic ×2, optimistic ×0.5; ε_H ×0.75/×1.25), so the light:c:b:bb̄ mistag *ratios* are **not varied**, background N_eff and shapes are identical in p/n/o, and a light-vs-b mistag-ratio variation is not part of the pre-declared set. **Phase 06 anti-tuning guard (declared now, `g2_predeclared.yaml`):** the m_SD window / pT threshold optimisation uses the smoothed estimator or an independent half of each sample, never the raw hard-window count (QCD raw window count is 6 in the 200 k twin).
Signal retention under the m(HH) clip is small for the SM (0.82/0.24 at 1.5/1.0 TeV) and k2V=0 (0.66/0.15): the clip is a strong variation; the unclipped result is primary as decided.

## 11. Storage, quota, CPU
EOS: the project node /eos/user/r/rjiang/ (`eos root://eosuser.cern.ch quota /eos/user/r/rjiang/`; `eos quota /eos/home-r/rjiang` returns "no quota for path") was **43.3 % full at 22:24 UTC (864.9 GB physical = 432.5 GB logical) and 44.69 % full when re-checked after the pilots (893.8 GB physical = 446.9 GB logical)** of 2.00 TB physical = 1.00 TB logical; ≈ 1.00 TB logical free (as quoted by the quota tool), 787 k of 5 M files; the pilots account for ≈ 14 GB. There is no per-directory quota: **150 GB is the internal HH budget (D-HH-6), not a quota**. HH planned total **17.9 GB (pilots included; measured 1.3–5.4 kB per LHE event)** ≤ 150 GB; SPEC §1.8 (400 GB for phase 2) is respected by HH alone. **Compute: ≈ 121 wall-clock hours for the 312 new jobs (per-event wall time of PY8+Delphes+slim+gridpack step, 0.06–0.14 s/event, plus an assumed 5 min/job overhead) — NOT measured CPU time**; the pilots used ≈ 56 wall-clock hours (job JSONs). Measured CPU (RemoteUserCpu) was not retrieved and is not quoted.

## 12. `nmc_check_hh` on the planned table (PROJECTED inputs) and the real check
**Honesty note:** in this planned-table check the effective-N rows are fed the *projected* N_eff (sr_sumw = sr_sumw2 = N_eff,proj at N_planned), so for those rows the pass is **tautological with respect to the N_eff target** (it tests only the plumbing: BR once, full-N rows, twin flags, structure of the bound records). Full-N rows are genuine (N_planned vs max(50k, σ·BR·3000)). **The real check is `scripts/nmc_post_production.py`, to be run after production on the measured hard-window SR Σw, Σw² and N_gen from the job JSONs.** Run now on the pilots it correctly FAILS (`work/g2/nmc_post_production_pilots.txt`): full-N samples are at pilot size, and the measured pilot N_eff is 4.7 (Q_4j_vbs_twin, 200 k), 3.7 (Q_bbjj_vbs_twin, 150 k), 13.8 (T_ttbar_mlm, 100 k). The plan is therefore **verified only by projection until the planned events exist**.
Item 5 fix: a bound is accepted only as a structured record (`poisson95_wmax` or `poisson95_classaware`) that the checker **recomputes**, and only if the conservative variant is a named output file containing that value for the sample; bare numbers, wrong methods/values, missing or inconsistent files fail loudly (self-test: 6 malformed bounds rejected; `python3 scripts/nmc_check_hh.py`). The checker also caught two real inconsistencies of my first plan (integer rounding of the Poisson argument; the unsafe QCD filter). Output of `scripts/g2_plan.py` (`work/g2/plan.txt`): "nmc_check_hh PASSED on the planned table (24 rows)" (projected inputs, see above):
| sample | rule | N | required / N_eff(proj, nominal) | ok |
|---|---|---|---|---|
| S_HHjj_kV1_k2V1_kl1 | N>=max(50k,sigma*BR*L) | 50,000 | 50,000 | True |
| S_HHjj_kV1p5_k2V0_kl1 | N>=max(50k,sigma*BR*L) | 100,000 | 96,719 | True |
| S_HHjj_kV1p5_k2V0_kl0 | N>=max(50k,sigma*BR*L) | 130,000 | 121,090 | True |
| S_HHjj_kV0p5_k2V2_kl0 | N>=max(50k,sigma*BR*L) | 50,000 | 50,000 | True |
| S_HHjj_kV1_k2V0_kl2 | N>=max(50k,sigma*BR*L) | 50,000 | 50,000 | True |
| S_HHjj_kV1_k2V2_klm1 | N>=max(50k,sigma*BR*L) | 50,000 | 50,000 | True |
| S_HHjj_kV1_k2V0_kl1 | N>=max(50k,sigma*BR*L) | 50,000 | 50,000 | True |
| S_HHjj_kV1_k2V2_kl1 | N>=max(50k,sigma*BR*L) | 50,000 | 50,000 | True |
| S_HHjj_kV1p25_k2V1p5_kl2 | N>=max(50k,sigma*BR*L) | 50,000 | 50,000 | True |
| G_ggHH_loop_kl1 | N>=max(50k,sigma*BR*L) | 50,000 | 50,000 | True |
| G_ggHH_loop_kl0 | N>=max(50k,sigma*BR*L) | 80,000 | 71,436 | True |
| G_ggHH_loop_kl2 | N>=max(50k,sigma*BR*L) | 50,000 | 50,000 | True |
| G_ggHH_loop_kl5 | N>=max(50k,sigma*BR*L) | 80,000 | 79,389 | True |
| Q_4j_vbs_twin | effective-N (twin_ok=True) | — | N_eff,proj = 51.5 (UL record: no) | True |
| Q_bbjj_vbs_twin | effective-N (twin_ok=True) | — | N_eff,proj = 17.9 (UL record: no) | True |
| T_ttbar_mlm | effective-N (twin_ok=True) | — | N_eff,proj = 29.4 (UL record: no) | True |
| H_VBFH_bb | effective-N (twin_ok=True) | — | N_eff,proj = 0.0 (UL record: yes) | True |
| H_ZH_Zqq_bb | N>=max(50k,sigma*BR*L) | 110,000 | 103,067 | True |
| H_WH_Wqq_bb | N>=max(50k,sigma*BR*L) | 180,000 | 179,612 | True |
| H_ttH_bb | N>=max(50k,sigma*BR*L) | 440,000 | 433,305 | True |
| H_ggH_jj_heft | effective-N (twin_ok=True) | — | N_eff,proj = 0.0 (UL record: yes) | True |
| V_Zjj_QCD_vbs | effective-N (twin_ok=True) | — | N_eff,proj = 0.0 (UL record: yes) | True |
| V_Wjj_QCD_vbs | effective-N (twin_ok=True) | — | N_eff,proj = 0.0 (UL record: yes) | True |
| V_ZZjj_EW | N>=max(50k,sigma*BR*L) | 120,000 | 112,166 | True |

## 13. Deviations and interpretations (to the ledger)
1. Pilot sizes: 20 k per signal point (closure at Delphes level with the SR raw count 17–2094 per point, not ≥ 50 k), 10 k ggF HH, 20–200 k backgrounds; justified by cost (≈ 56 wall-clock h) and because pilots are part of the plan. 2. D-HH-12 extended to W±H. 3. QCD production with the **looser twin filter** since the nominal one is unsafe (+25/+29 %); residual loss assumed ≤ observed (syst), D-HH-14. 4. Twin acceptance at impact level for sub-dominant backgrounds (D-HH-14); the bound samples inherit twin evidence. 5. N_eff **projected** with a factorised window probability (cross-checked against direct counts; approximate). 6. Bound-only rule (UL < 1 % of the total SR background) and the class-aware Poisson bound method (declared here). 7. MLM validated by matching-scale variation, not DJR. 8. ggF HH K-factor is the SM value for all κλ. 9. K = 1 for all other samples (LO). 10. Test jobs for bound samples and twins are their first 10 k pilot jobs (exit 0) and, for Q twins, the test job of the same card type (884577/884464). 11. EOS "ghost" status files: σ read from the MG5 log fallback (`make_matrix.py`). 12. `python3 -P` is not supported by the system python (3.9); the stack python (LCG_110) is used. 13. ggZH is LO loop-induced with ptheavy 150 and bounded only. 14. Reconstruction objects: no fat-jet JES, no leptons/photon cleaning (unchanged). 15. W-factor absence justified in 01 §7 (item 9a); (b), (c) logged by the orchestrator in SPEC §7.

16. **Pilot size (logged constraint violation).** The brief allowed N_eff pilots at validation size (≤ 100 k per sample unless justified); this run generated **2.19 M pilot events (≈ 56 wall-clock h, ≈ 14 GB) in the canonical `production/hh/` and counted them toward the production N**. Samples above 100 k: Q_4j_vbs_twin 200 k, Q_bbjj_vbs_twin 150 k (the others are ≤ 100 k, but the total is large). Justification: the twin tests need ≳ 10² tail events and the QCD boosted-VBS tail fraction is ~10⁻³, so 150–200 k were needed for ±5–6 % errors; pilots were run as the first production jobs (unique seeds J ≥ 10, same cards) so they are not wasted. It was done without asking first; this is a deviation. **No further production is submitted**; the human may declare the pilots validation-only (then N_planned must be regenerated).

## 14. Condor submission plan (NOT submitted; G2 conditions)
Generated from `work/g2/plan.json` (`make_submit_g2.py prod …`), EosSubmit schedd (`module load lxbatch/eossubmit`), `max_retries=1`, outputs `p2/production/hh/<sample>/`, seeds `3 100 000 + 1000·idx + 10 + k` (k continues after the pilot jobs; `check_seed_uniq.py`). **Block 1** `scripts/condor/g2_prod_G2_block1_signal_ggHH.sub` (62 jobs) and **block 2** `…_block2_tt_ttH_VH_ZZ.sub` (66 jobs) may be submitted after D-HH-13 and D-HH-15 are answered. **Block 3 (QCD twin-config, 217 jobs, ≈ 76 wall-h)** is in `scripts/condor/HELD_do_not_submit/g2_prod_G2_block3_QCD_HELD.sub` and is **held** until D-HH-14a. Before submission: `condor_q` for duplicates and one finished job per batch checked (exit 0, N, σ). Wrappers return exit 30 on a no-op rerun.

## 15. Decisions needed (human)
- **D-HH-13 (κλ/κV validation):** the deliverable is κ2V only unless direct samples are added: (1,1,0), (1,1,2) (+ (1,1,5) closure), ≈ 50–100 k events each (≲ 3 wall-h) — the defensible option (a κλ line at κV = κ2V = 1 needs only the monomials {1, κλ, κλ²}); alternative: a closure point with large yield (e.g. κV = 1.5) with more basis statistics; or no κλ/κV claim.
- **D-HH-14 (generator-filter policy):** (a) **resolve the QCD sev-1 by measurement**: option 1 further-loosened twins (ready, §17, ≈ 53 wall-h) or option 2 particle-level fat-jet filter (§17, needs a custom driver, not ready); (b) accept the impact-level twin criterion for sub-dominant backgrounds (ttH is covered only by it); (c) accept the bound-only rule (UL < 1 % of the SR background).
- **D-HH-15 (pilot reuse):** the 2.19 M pilot events (brief violation, §13.16) enter the production N — accept (gridpack sha256 identical for every pilot job, §17) or declare them validation-only and regenerate N_planned.
- **D-HH-16 (ggF HH premise, raised separately from D-HH-14):** ggF HH (LO+PS) is ≈ 20× the SM EW signal in the pilot SR (0.92 vs 0.047 events at 500 fb⁻¹; N_eff 4.6 at 10 k events, so the number itself is ±50 %), whereas D-HH-2 was decided on "about half". Negligible for κ2V (< 0.1 % of B). Questions: is the +30 % VBF-region allowance still adequate; is the SM-κλ K = 2.333 reused for all κλ acceptable (its κλ dependence is not estimated); is an SM-HH statement wanted at all (then ggF HH + 2 jets is the dominant missing piece).

## 16. Exact commands
```
source p2/lib/scripts/setup_stack.sh ; cd p2/runs/multi_r1/hh
python3 -P scripts/hh_samples.py ; python3 -P scripts/make_matrix.py            # registry, cards (new seeds), matrix
python3 -P scripts/make_submit_g2.py gp|test|prod <tag> …                         # clusters 884937/44/46 (gp), 884941/43/45 (test), 884938/42/47/48/49 (pilots)
bash scripts/run_g2_analysis.sh                                                    # pilot_check, neff_project, twin_check_hh, morph_delphes, mlm_check, variations, g2_plan
python3 -P scripts/render_04.py ; python3 -P scripts/manifest.py ; python3 -P scripts/check_seed_uniq.py
```
Evidence: `work/g2/*.json|md|txt`, `config/g2_predeclared.yaml`, `production/hh/MANIFEST.tsv`. Next: G2 review; after approval submit `g2_prod_G2.sub`; Phase 04 (PS/Delphes validation) follows.

## 17. G2-FIX material
**17.1 QCD residual filter loss — the two options (D-HH-14a), nothing submitted.** The nominal→twin loss is large at the two-fat-jet stage already (ihtmin 500: 43–46 %) although the reco SR needs ΣpT(fat jets) ≥ 750 GeV, i.e. the SR multijet is largely populated by shower jets, and the twin cuts (350, 2.0/200) may lose a comparable fraction.
- *Option 1 — further-loosened twins* (`Q_4j_vbs_twin2`, `Q_bbjj_vbs_twin2`: ihtmin 250, VBS 1.5/100; idx 92/93; cards `cards/Q_*_twin2.mg5`; the only copies are `scripts/condor/HELD_do_not_submit/g2_gp_D14a_twin2.sub` and `…/g2_prod_D14a_twin2.sub` (copy to `scripts/condor/` and submit together only on the human's choice) — jobs hold with exit 19 until their gridpack exists and are auto-released): Q_4j 1.0 M events (100 jobs × 10 k) ≈ 38 wall-h, Q_bbjj 0.5 M events (50 jobs) ≈ 13 wall-h, gridpacks ≈ 2 wall-h: **≈ 53 wall-h, ≈ 6 GB, 150 jobs**; expected ≈ 400 tail events at the VBS stage ⇒ loss error ≈ 7 % (the twin2 σ is unknown until the gridpack exists, so this is an estimate). Analysis: `twin_check_hh.py … Q_4j_vbs_twin:Q_4j_vbs_twin2 Q_bbjj_vbs_twin:Q_bbjj_vbs_twin2`. If the loss twin1→twin2 is ≤ 5 % the production filter is proven safe; otherwise production switches to twin2 (and the QCD plan is re-sized).
- *Option 2 — particle-level fat-jet filter:* tested in the installed stack (Pythia 8.317 python module, LCG_110). A python `UserHooks` subclass with a `SlowJet` anti-kT R = 0.8 veto after the parton shower (≥ 2 jets pT > 250, |η| < 2.4) runs: on 2000 Q_4j LHE events 359 pass (18 %) at 0.0087 s/event (vs 0.14 s/event for the full PY8+Delphes chain), so hadronisation and Delphes are saved for 82 % of events. **But it cannot be delivered to Delphes with the stock tools**: `DelphesPythia8` accepts only settings (matching hooks are compiled in, no user hook), the python module has no HepMC3 writer (`import HepMC3`/`pyhepmc` fail), and a rerun-by-index is not valid (different random streams). A custom C++ driver (Pythia8 + Delphes classes; headers exist under `$DELPHES_DIR/include`) would be required: estimated effort 1–2 days plus validation against the standard chain. A particle-level filter also does not remove the *LHE-level* bias by itself; it makes an unfiltered (or much looser) LHE affordable: with a pass rate ~10⁻⁴ for the SR-like tail one needs ~10⁷ LHE events (≈ 25 wall-h of showering) for ~10³ tail events. Status: feasible, **not ready-to-submit**; prototype hook `scripts/py8_fatjet_filter_proto.py`.
**17.2 O1 flavour partition (G2 item 10), checked on the nominal pilots and the twins:** σ(Q_4j)·f(b b̄ in the hard final state) vs σ(Q_bbjj): nominal 715 ± 16 vs 725.4 ± 1.6 pb (ratio 0.986, pull −0.6); twin 5927 ± 90 vs 5976 ± 12 pb (0.992, pull −0.5): the partition is validated before Q_bbjj is scaled. `work/g2/o1_partition.txt`.
Q_4j_vbs N=100000 k=1899 f=0.0190  sigma_4j*f = 715.16 +- 16 pb  vs sigma_bbjj(Q_bbjj_vbs) = 725.4 +- 1.6 pb  ratio 0.986 pull -0.6
Q_4j_vbs_twin N=200000 k=4451 f=0.0223  sigma_4j*f = 5926.5 +- 90 pb  vs sigma_bbjj(Q_bbjj_vbs_twin) = 5976 +- 12 pb  ratio 0.992 pull -0.5

**17.3 Pilot reuse audit (G2 item 2):** every pilot job JSON records the sha256 of the gridpack it used; all equal the sha256 in `production/hh/MANIFEST.tsv` (gridpacks) — the binding evidence of identical production configuration. Cards are regenerated deterministically by `hh_samples.py` (so their mtime is not informative; their sha256 is listed). Table (`work/g2/sha_check_pilots.md`):
| sample | jobs | gridpack sha256 (MANIFEST, 12) | jobs with identical gridpack sha | card sha256 (cards/*.mg5) | py8 cmnd sha256 | card older than first job |
|---|---|---|---|---|---|---|
| S_HHjj_kV1_k2V1_kl1 | 2 | 66ddd908b5db | 2/2 | 06b5c6d2df4b | c54ae6a384e0 | yes |
| S_HHjj_kV1p5_k2V0_kl1 | 2 | 9682536b7f06 | 2/2 | 04def1fa858b | c54ae6a384e0 | yes |
| S_HHjj_kV1p5_k2V0_kl0 | 2 | 385922c3dda0 | 2/2 | 3d3ee7bc66f6 | c54ae6a384e0 | yes |
| S_HHjj_kV0p5_k2V2_kl0 | 2 | 40e0e948ddab | 2/2 | c4f461d005c5 | c54ae6a384e0 | yes |
| S_HHjj_kV1_k2V0_kl2 | 2 | 95482fdfc0cd | 2/2 | 76ed7005d1aa | c54ae6a384e0 | yes |
| S_HHjj_kV1_k2V2_klm1 | 2 | ae622e2ab148 | 2/2 | 5c8f15fd7d3f | c54ae6a384e0 | yes |
| S_HHjj_kV1_k2V0_kl1 | 2 | cd838f75f43c | 2/2 | 24698c431139 | c54ae6a384e0 | yes |
| S_HHjj_kV1_k2V2_kl1 | 2 | 303508828507 | 2/2 | fad00c8c988f | c54ae6a384e0 | yes |
| S_HHjj_SM_twin_loose | 3 | 65ec29fb42d7 | 3/3 | 12e2dbfb0acd | c54ae6a384e0 | yes |
| G_ggHH_loop_kl1 | 1 | 40afcef5e77e | 1/1 | f37c125f5088 | c54ae6a384e0 | yes |
| G_ggHH_loop_kl0 | 1 | 40313e1d046a | 1/1 | 94d022014e6b | c54ae6a384e0 | yes |
| G_ggHH_loop_kl2 | 1 | a034490849bc | 1/1 | 38a4dce84d98 | c54ae6a384e0 | yes |
| G_ggHH_loop_kl5 | 1 | f8b5bafc765e | 1/1 | d092b51fa504 | c54ae6a384e0 | yes |
| Q_4j_vbs | 10 | 0b4e3c1cdb3f | 10/10 | f0f28a3a05ba | a070126d3758 | yes |
| Q_bbjj_vbs | 10 | 94f8e31d293d | 10/10 | 338b71a120aa | a070126d3758 | yes |
| T_ttbar_boost | 5 | 0eca6e302946 | 5/5 | 182a03a59c90 | 2fc0f5fd8885 | yes |
| H_VBFH_bb | 5 | 9daaf6d00ce4 | 5/5 | f15f003e6a4a | c54ae6a384e0 | yes |
| H_ZH_Zqq_bb | 5 | b44542fd698c | 5/5 | 9111b2acca96 | 1990ca0ee158 | yes |
| H_ttH_bb | 5 | 9a176992ddd3 | 5/5 | cdf467465b8a | c54ae6a384e0 | yes |
| V_Zjj_QCD_vbs | 5 | 3ed04e2bebc6 | 5/5 | b94a62368693 | 1990ca0ee158 | yes |
| V_ZZjj_EW | 5 | 111d8844acad | 5/5 | a656c49a9c98 | 1990ca0ee158 | yes |
| X_tW_boost | 2 | f26468bb8a36 | 2/2 | 80b4d24526b8 | 2fc0f5fd8885 | yes |
| X_ttZ_boost | 2 | 443e77bf951d | 2/2 | 38d429e68c74 | 2fc0f5fd8885 | yes |
| X_ttW_boost | 2 | 9023b4292b01 | 2/2 | c60fb2b74d13 | 2fc0f5fd8885 | yes |
| X_Zjj_EW_vbs | 2 | 1434068f36b6 | 2/2 | 37feb17d4671 | 1990ca0ee158 | yes |
| X_ZZ_QCD_boost | 2 | 79cbeaac032d | 2/2 | 6e4eb0a7cd46 | 1990ca0ee158 | yes |
| H_WH_Wqq_bb | 5 | a120dd61a630 | 5/5 | 4b6aa5ef4442 | 1990ca0ee158 | no/unknown |
| H_ggH_jj_heft | 5 | bd57b5b9046e | 5/5 | 03a0a250262d | c54ae6a384e0 | no/unknown |
| V_Wjj_QCD_vbs | 5 | f920ee7ee195 | 5/5 | 94e369c89352 | 1990ca0ee158 | no/unknown |
| Q_4b_ht | 5 | 8efc1d11c762 | 5/5 | 90699d94de25 | a070126d3758 | no/unknown |
| T_ttbar_mlm | 10 | ff2335327427 | 10/10 | 86392c889d70 | 4b830f6f3808 | no/unknown |
| T_ttbar_mlm_xq20 | 3 | e02e27d4e08d | 3/3 | 70dc01dac2ae | 1bac53f15e7c | no/unknown |
| T_ttbar_mlm_xq45 | 3 | b7f8b0219b8a | 3/3 | ff28c4495734 | 53d79d90f9d5 | no/unknown |
| X_ggZH_loop | 2 | 9ddb5eefaa36 | 2/2 | 715448f82124 | 1990ca0ee158 | no/unknown |
| X_Wjj_EW_vbs | 2 | 4f7dd0f96d71 | 2/2 | 3cc61659f866 | 1990ca0ee158 | no/unknown |
| X_WZ_QCD_boost | 2 | 8c535f27d106 | 2/2 | e4ef2be7f77a | 1990ca0ee158 | no/unknown |
| S_HHjj_kV1p25_k2V1p5_kl2 | 2 | b58f0f17ea98 | 2/2 | 8389af94d47a | c54ae6a384e0 | no/unknown |
| S_HHjj_kV1_k2V0_kl1_twin | 2 | 06c68ec4e250 | 2/2 | c0591ffb8c8c | c54ae6a384e0 | no/unknown |
| Q_4j_vbs_twin | 20 | 8ffc8c828a8f | 20/20 | f7d1e7757e18 | a070126d3758 | no/unknown |
| Q_bbjj_vbs_twin | 15 | b27a20e2145c | 15/15 | e7190049b273 | a070126d3758 | no/unknown |
| T_ttbar_boost_twin | 5 | 599fdc5bb015 | 5/5 | 738f1e6fcdef | 2fc0f5fd8885 | no/unknown |
| H_VBFH_bb_twin | 5 | 61b5ec64de43 | 5/5 | 853624179ba4 | c54ae6a384e0 | no/unknown |
| H_ZH_Zqq_bb_twin | 5 | f24f0610d863 | 5/5 | e49d93937a0f | 1990ca0ee158 | no/unknown |
| H_ttH_bb_twin | 5 | 2a80b4996a39 | 5/5 | f5187ad28e87 | c54ae6a384e0 | no/unknown |
| V_Zjj_QCD_vbs_twin | 5 | 32fe841c20ba | 5/5 | 2cd9da0f0d34 | 1990ca0ee158 | no/unknown |
| V_ZZjj_EW_twin | 5 | b531f457b4b8 | 5/5 | 6862dd3d1104 | 1990ca0ee158 | no/unknown |
| H_ggH_jj_heft_twin | 5 | d004326791ed | 5/5 | a3cc763443fb | c54ae6a384e0 | no/unknown |
| H_WH_Wqq_bb_twin | 5 | 0430dceecc69 | 5/5 | 3b10751daa52 | 1990ca0ee158 | no/unknown |
| V_Wjj_QCD_vbs_twin | 5 | cda4dacc320c | 5/5 | f192c8c0ead7 | 1990ca0ee158 | no/unknown |
| T_ttbar_mlm_twin | 10 | bbe8e0427a61 | 10/10 | 21c1f2a2d248 | 4b830f6f3808 | no/unknown |

ALL pilot jobs use the MANIFEST gridpack: True

**17.4 Status of G2 conditions:** item 1 prepared (held), 2 table done + D-HH-15 raised, 3 stated, 4 01:62(c) fixed + D-HH-16, 5 tagw twin test applied, 6 variations use the smoothed estimator (N_eff tabulated), 7 guard pre-declared, 8 headers fixed, 9 measured sizing + top-up rule, 10 O1 done, 11 stale text fixed, 12 t-channel bound added, 13 mistag-ratio statement, 14 MLM ±(10–20) % carried.
