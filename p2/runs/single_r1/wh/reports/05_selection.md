# 05 — Baseline selection, background estimation, optimisation (single_r1, WH)

**Date:** 2026-11-14 10:53 UTC. **Status: PASS** (all background sources have a Delphes-level yield or a 95 % UL in the SR; three non-prompt/mis-ID methods estimated separately with closure tests; cut-based optimum and k-fold BDT on expected quantities; BDT adopted by the pre-declared rule, with the marginal-stability caveat in §6).
**Goal:** event selection for EW W±Hjj (W→eν/μν, H→γγ) at Delphes level on the frozen canonical package `p2/production/wh` (tag wh-prod-v1, v1.1 rows), read-only; every background source with a yield or UL; non-prompt photons, non-prompt leptons and e→γ separately; cut-based optimisation, then BDT with k-fold, adopted only if the gain is > 10 % and stable.

## 1. Inputs, versions, integrity
- Package: `p2/production/wh/` (SAMPLES.csv, FORMAT.md, V1.1_NOTES.md read first). **SHA256: 2900 production files hashed inside the ntuple jobs and compared with `SHA256SUMS`: 0 mismatches.** Frozen ZH directories used as WH backgrounds (`production/final/*`, `production/v1/*`, read-only) have no reference list: their 1120 files' hashes are recorded in the ntuples (`M_sha`), not verified.
- Σ Event.Weight and N_Delphes per sample reproduce SAMPLES.csv exactly for every package row (`inventory_bad` = []).
- Own sample (A2: "extra samples only under runs/single_r1, R=4 seeds"): **`H_ggF_jj_nomjj`** (idx 42, HEFT `p p > h j j`, ptj>20, |ηj|<5, ΔRjj>0.4, **no m_jj cut**), gridpack seed 2442000 (cluster 913309, σ = 7.141 ± 0.026 pb), test job 2442001 (913310: 2000/2000 events, σ_PY8 = 7.059 pb), production 30 jobs seeds 2442002–2442031 (913321, all exit 0): **N = 59 945 ≥ N_req = max(50k, σ·BGG·3000 fb⁻¹ = 48.4k)**; replaces the missing `H_ggF_jj` row (D-WH-5).
- Stack: LCG_110 (MG5 3.6.3, Pythia 8.317 CP5, Delphes 3.5.1 slim card), uproot 5.7.1, awkward 2.9.0, numpy 2.4.4, scipy 1.17.1, xgboost 2.1.3, scikit-learn 1.9.0.
- Commands: `python3 -P wh/scripts/p05/make_nt_jobs.py` → `condor_submit wh/scripts/condor/p05_nt.sub` (cluster 913320, 999 jobs; first attempt 913314 removed: condor split comma arguments) ; `python3 -P wh/scripts/p05/p05_run.py` ; `p05_bdt.py` ; `p07_stats.py` ; `make_figs.py` ; `make_reports.py` (all from `wh/scripts/p05`, with `source p2/lib/scripts/setup_stack.sh` and `PYTHONPATH=wh/scripts/p05`). Ntuples: `wh/work/nt/<sample>/*.npz` (git-ignored); results `wh/work/p05/{p05,bdt,p07}.json` (copied to `reports/evidence/`).

## 2. Objects and normalisation
Electrons pT>10 |η|<2.5, muons pT>10 |η|<2.4 (Delphes isolated); photons pT>15, |η|<2.5 outside 1.4442–1.566, ΔR(γ,ℓ)>0.4; jets anti-kT 0.4 pT>20 |η|<4.7, ΔR>0.4 to leptons and photons; b-tag = BTag bit 0, |η|<2.5, pT>25. Truth flags from GenTruth: prompt lepton/photon (ΔR<0.1 to a prompt generator object), photon from a prompt electron (ΔR<0.2). σ×BR per set of events = 10³·k·ΣEvent.Weight/N_generated (FORMAT §4); k from the SAMPLES.csv factor string, re-multiplied from named factors and asserted equal (BR applied once; `whana.py` R/kfac).
**Object efficiencies (D-WH-4 default, G1): CMS-like reweighting** ε_CMS/ε_Delphes per prompt lepton and prompt photon, ε_CMS from the ZH final analysis (`lib/scripts/analysis/final_analysis.py`), ε_Delphes measured here from gen-matched prompt objects in the signal and Wγγjj samples:
| object | |η| bin | ε_Delphes (pT bins: 10/20–20/30–30/50–50+; γ: 20–30–40–60–∞) | ε_CMS |
|---|---|---|---|
| e | 0 | 0.39 / 0.47 / 0.58 / 0.71 | 0.70 / 0.80 / 0.88 / 0.92 |
| e | 1 | 0.28 / 0.35 / 0.44 / 0.55 | 0.65 / 0.75 / 0.83 / 0.88 |
| m | 0 | 0.59 / 0.71 / 0.79 / 0.86 | 0.93 / 0.96 / 0.96 / 0.96 |
| m | 1 | 0.58 / 0.69 / 0.80 / 0.86 | 0.93 / 0.96 / 0.96 / 0.96 |
| g | 0 | 0.61 / 0.69 / 0.78 / 0.89 | 0.85 / 0.88 / 0.92 / 0.92 |
| g | 1 | 0.53 / 0.60 / 0.69 / 0.80 | 0.80 / 0.83 / 0.88 / 0.88 |

Stock Delphes efficiencies are a robustness variant (07).

## 3. Baseline (pre-declared at G1) and cutflow
Peak from the Delphes EW signal: μ = 124.99 GeV, σ_core = 2.03 ± 0.02 GeV, σ_eff(68 %) = 2.08 GeV; 120–130 GeV contains 97.5 % of the loose-selection signal.
Baseline: exactly one lepton pT>25 (2nd lepton pT>10 vetoed), ≥2 photons with pT/m_γγ>1/3, 1/4, 105<m_γγ<160, MET>30, ≥2 jets pT>30, m_jj>500, |Δη_jj|>2.5, b-veto, window 120–130. **At 500 fb⁻¹: s = 1.48, b = 17.16, Z(Eq. 1) = 0.35.**
Final-selection cutflow (500 fb⁻¹, expected events; raw MC rows in parentheses; continuum groups after the window use the m_γγ-shape estimate):
| step | EW W±Hjj (signal) | QCD W±H (+jets, MLM) | EW W→τν feed-down | EW Wγγjj | QCD Wγγjj | Wγ+jets, 1 non-prompt γ | W+jets, 2 non-prompt γ | top: tt̄γγ, tt̄γ, tWγ, tt̄jj | tt̄H, tHq, tHW | ZH (EW, QCD, gg, ττ), lost ℓ | Zγγjj, lost ℓ | e→γ: Zγjj, WWγ/WZγ/ZZγ | non-prompt ℓ: γγ+3j, VBF H, ggF H |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 ℓ (pT>25), ≥2 γ, ≥2 jets (pT>25) | 4.54 (37250) | 15.5 (6021) | 0.356 (2662) | 52.1 (11000) | 492 (8524) | 126 (354307) | 32.1 (1250920) | 278 (182918) | 37.8 (70516) | 7.01 (92380) | 71.3 (49832) | 734 (30885) | 94.1 (472279) |
| + 2nd-ℓ veto, pT/m_γγ>1/3,1/4, 105<m_γγ<160 | 3.79 (32105) | 13.1 (5234) | 0.3 (2312) | 30.3 (6681) | 298 (5362) | 76.1 (251842) | 19.6 (925050) | 128 (142237) | 29.1 (56583) | 3.59 (43012) | 24.6 (16238) | 374 (22034) | 45.4 (348743) |
| + 2 jets pT>30, b-veto, m_eγ Z-veto (e channel) | 2.92 (25153) | 7.47 (3058) | 0.223 (1761) | 23.9 (5342) | 214 (3926) | 58 (195273) | 14.8 (740532) | 22.8 (48313) | 4.68 (11566) | 2.46 (31872) | 17.5 (12129) | 141 (2889) | 31.3 (285542) |
| + m_jj>300, Δη_jj (abs)>2.0 (BDT preselection) | 2.2 (18936) | 1.18 (483) | 0.168 (1333) | 17.3 (3883) | 50.5 (936) | 37.3 (137276) | 10.7 (569089) | 7.78 (34906) | 0.96 (2800) | 0.577 (15043) | 5.27 (5956) | 46.5 (2155) | 16.2 (226267) |
| + BDT > 0.88 | 1.27 (11180) | 0.0842 (37) | 0.0859 (708) | 2.96 (681) | 0.684 (14) | 0.517 (2870) | 0.107 (11120) | 0.0716 (433) | 0.142 (544) | 0.0654 (4273) | 0.187 (343) | 0.563 (183) | 0.141 (3869) |
| + m_γγ window 120.9–129.0 (final) | 1.19 (10548) | 0.0786 (35) | 0.0807 (667) | 0.483 (99) | 0.112 (3) | 0.109 (450) | 0.0178 (1807) | 0.00977 (62) | 0.13 (518) | 0.0613 (4042) | 0.0307 (55) | 0.0899 (25) | 0.059 (1406) |


## 4. Background estimation (three non-prompt / mis-ID classes separately)
**Estimation hierarchy per (sample, component)** (`whana.component`, adapted from the ZH final analysis): L0 direct window count for m_γγ-resonant samples with N_eff ≥ 10; L1 m_γγ shape for continuum samples (fit-range yield × window fraction of an unbinned exponential MLE of the same component) when N_eff(fit range) ≥ 10; otherwise L2 VBS-factorised (yield without the m_jj/Δη/BDT cuts × their efficiency in a loose object-level region) with 100 % uncertainty; zero support everywhere: central 1.14 w̄ (100 %), 95 % UL = 3 w̄ (w̄ = mean per-event weight in the loose region). The direct-event category that a weighted method replaces is removed from the direct count (no double counting): non-prompt photons (F1/F2 samples), photons from electrons (EG samples), non-prompt leptons (FL samples, max rule).
**(a) Non-prompt photons (j→γ).** Per-jet weighting of pseudo-events (jet → photon with pT = x·pT(GenJet), x ~ N(0.85, 0.10) truncated to [0.5, 1]): one fake in Wγ+jets (`F_QCD_Wajjj_nomjj`, `F_EW_Wajj_nomjj`), tt̄γ, tWγ (n_prompt_photons ≤ 1 overlap rule for Wγ); two fakes in W+4j and tt̄jj (n_prompt_photons = 0). Rate = declared scenario f = 10⁻³(pT/50)^−0.5 (×2 endcap) × {0.3, 1, 3}. *Closure* at the one-fake level (lepton pT>25), Delphes direct non-prompt photons vs weighting:
| sample | Delphes direct [fb] | raw | frac. ΔR(γ, GenJet)>0.4 | weighting × Delphes rate (FORMAT 6a) [fb] | weighting × nominal scenario [fb] | nominal / direct |
|---|---|---|---|---|---|---|
| `F_Wjjjj` | 151.117 | 7120 | 0.78 | 29.902 | 611.953 | 4.0 |
| `T_ttjj_1l` | 37.581 | 193 | 0.67 | 9.619 | 211.464 | 5.6 |
| `F_QCD_Wajjj_nomjj` | 1.122 | 3564 | 0.78 | 0.209 | 4.030 | 3.6 |
| `F_EW_Wajj_nomjj` | 0.083 | 285 | 0.68 | 0.009 | 0.159 | 1.9 |
| `T_tta_1l` | 0.196 | 627 | 0.78 | 0.036 | 0.818 | 4.2 |
| `T_tWa_1l` | 0.031 | 794 | 0.78 | 0.005 | 0.115 | 3.7 |

The m_jj shape of the Delphes fakes is reproduced by the weighting (W+4j fractions in m_jj bins 0–200/200–500/500–1000/>1000: direct 0.446 / 0.397 / 0.124 / 0.033, weighted 0.470 / 0.378 / 0.120 / 0.032; `figures/p05_closure_jg_mjj.png`). The normalisation does not close against Delphes: the FORMAT-6a per-jet rate (ΔR<0.2 matched) under-predicts Delphes by ≈ 5× because most Delphes non-prompt photons are not aligned with a GenJet, and the nominal scenario is ≈ 4× the Delphes rate (conservative; the low scenario ≈ Delphes). Uncertainty: 100 % (one fake), 150 % (two fakes), 100 % correlated within each class; Delphes-rate variant in the robustness table.
**(b) Non-prompt leptons (j→ℓ).** Per-jet weighting (jet → lepton, x as above, e/μ 50/50) in events without a reco lepton, rate {3·10⁻⁵, 2·10⁻⁴, 10⁻³} per jet, on `Q_aajjj` (γγ+3 partons), `H_VBFH_jj`, `H_ggF_jj_nomjj` (own); `Q_aajj` is a cross-check. Max rule: nominal = max(parametrised, Delphes direct non-prompt leptons). *Closure / cross-check:* Delphes direct per-jet rate f_eff = 1.05e-05 (`Q_aajjj`, 55 raw leptons / 5229184 jets), 1.21e-05 (`Q_aajj`), 0 in VBF/ggF H (31684 / 45155 jets) — below the tight scenario, so the parametrised value is used everywhere. Uncertainty 100 % (scenario range ×0.15–×5 in robustness); PS-modelling 100 % for VBF/ggF H (third jet from the shower).
**(c) e→γ.** Per-electron weighting (reco prompt electron → photon) in events with ≥2 reco leptons, weight = P(e→γ | gen e)/ε_Delphes(e) with P = {1, 2, 5} %, on `F_QCD_llajj_loose`, frozen `F_EW_llajj_vbs`, `V_WWa/WZa/ZZa_WH`. *Closure* in a relaxed region (no VBS/MET/b cuts, fit range): Delphes direct e→γ vs weighting × FORMAT-6b Delphes rate:
| sample | direct [fb] | raw | weighted × 6b [fb] | C = direct/weighted | applied |
|---|---|---|---|---|---|
| `F_QCD_llajj_loose` | 1.7139 | 3093 | 0.4241 | 4.04 | yes |
| `ZH_F_EW_llajj_vbs` | 0.0691 | 1835 | 0.0675 | 1.02 | yes |
| `V_WWa_WH` | 0.0074 | 15 | 0.0008 | 9.04 | yes |
| `V_WZa_WH` | 0.0010 | 7 | 0.0003 | — | no (raw < 10) |
| `V_ZZa_WH` | 0.0011 | 31 | 9.3e-05 | 11.33 | yes |

The method closes for the EW sample (C ≈ 1.02) and fails by ≈ 4× for the loose QCD ℓℓγjj sample (soft/collinear γ*→ee configurations; ≈ 17 % of the direct e-photons are themselves prompt FSR photons). The measured C is applied as a closure correction (D-WH-13), uncertainty 100 % on the class.
**Prompt sources:** Wγγjj (EW, QCD; no generator m_jj cut), tt̄γγ, tt̄γ/tWγ prompt-prompt (kept as in ZH), Zγγjj/ZHjj lost lepton (frozen ZH; EW Zγγjj with generator m_jj>400, C = 0.958 ± 0.061), tt̄H, tHq, tHW, ggZH, ZH→ττ, QCD WH (MLM), W→τν feed-down: direct.

## 5. Cut-based optimisation (expected quantities, 500 fb⁻¹, def. a, Z with σ_b)
Coordinate scan (window, pT/m_γγ, MET, m_T, Zeppenfeld, m_eγ veto, j2 pT, pT^γγ, (m_jj, Δη) grid), choice = highest s among points within 3 % of the best Z (avoid chasing noise), iterated to convergence (3 passes). Optimisation-level σ_b: 10 % prompt, 100 % (150 %) one (two) fakes, 100 % L2 and zero-support, 2.5 % luminosity, MC stat.
**Cut-based optimum:** m_jj > 700, |Δη_jj| > 4.0, pT^γγ > 120, MET > 0, m_T > 0, pT/m_γγ > 0.333/0.250, m_eγ veto ±10 GeV, j2 pT > 30, window 120.93–129.05 GeV (±2σ_core), b-veto, Zeppenfeld none. s = 0.813, b = 1.731 → Z(Eq. 1) = 0.577, Z(σ_b) = 0.562. Stability (Z(σ_b) at ±1 grid step): ratio: 0.562, 0.562; met: 0.562, 0.555; mtw: 0.562, 0.557; zgg: 0.562, 0.565; meg: 0.488, 0.562; j2pt: 0.562, 0.496; ptgg: 0.529, 0.562; mjj: 0.557, 0.562, 0.562; deta: 0.521, 0.562, 0.576. pT^γγ sits at the largest grid value (120; 80 → 120 gains 6 %); not extended further.

## 6. BDT (xgboost, 5-fold) — adopted
Training after the preselection m_jj>300, |Δη|>2.0, j pT>30, b-veto, m_eγ veto, MET>0, fit range; signal EW W±Hjj vs all backgrounds with expected weights (each class normalised to equal total); 26 inputs, **m_γγ excluded**; folds by event-number hash (pseudo-events of one event share a fold); each row scored by the model that did not see its fold; models saved (`work/p05/bdt_models/`). AUC train/test per fold: 0.952/0.935, 0.952/0.938, 0.951/0.937, 0.951/0.940, 0.952/0.934. Top inputs: detajj 0.23, j3pt 0.12, ptbal 0.09, drgg 0.09, drgj 0.07, zgg 0.06.
Threshold scan with the **same** estimation hierarchy and σ_b as the cut-based optimum (`figures/p05_bdt_scan.png`): best BDT > 0.88: s = 1.192, b = 1.263, Z(σ_b) = 0.931 vs cut-based 0.562 → **gain 66 %**. Fold-wise check (direct counts in one fold × 5): 0.82 vs 0.58, 0.92 vs 0.31, 0.97 vs 0.53, 1.08 vs 0.64, 0.87 vs 0.33 → gain positive in every fold; max AUC(train) − AUC(test) = 0.019 < 0.02. **Adopted** (rule: gain > 10 % and stable).
*Caveat (referee point, see 07 self-review):* the first BDT run, made before the e→γ closure factor was passed to the BDT script (bug, fixed), had fold 0 at 0.56 vs 0.58 (rule failed); the stability is therefore marginal, and the cut-based result is reported alongside everywhere. The BDT relies on jet-activity variables (j3 pT, n_jets), which are parton-shower sensitive; this is covered by the jet-modelling and signal PS nuisances (06).

## 7. SR yields at the final (BDT) selection, 500 fb⁻¹ (def. a; every source)
| group | sample | class | y | MC stat | raw rows | N_eff | method per component | 95 % UL (zero support) |
|---|---|---|---|---|---|---|---|---|
| EW W±Hjj (signal) | `S_EW_WHjj` | D | 1.192 | 0.012 | 10548 | 10079.9 | D:L0 |  |
| QCD W±H (+jets, MLM) | `H_QCD_WH_mlm` | D | 0.079 | 0.013 | 35 | 34.3 | D:L0 |  |
| EW W→τν feed-down | `S_EW_WHjj_taunu` | D | 0.081 | 0.003 | 667 | 633.2 | D:L0 |  |
| EW Wγγjj | `B_EW_Waajj_nomjj` | D | 0.483 | 0.019 | 99 | 651.5 | D:L1 |  |
| QCD Wγγjj | `B_QCD_Waajj_nomjj` | D | 0.112 | 0.030 | 3 | 13.6 | D:L1 |  |
| Wγ+jets, 1 non-prompt γ | `F_EW_Wajj_nomjj` | F1 | 0.017 | 0.006 | 69 | 7.6 | D:L2,F1:L1 |  |
|  | `F_QCD_Wajjj_nomjj` | F1 | 0.092 | 0.018 | 381 | 27.1 | D:L2,F1:L1 |  |
| W+jets, 2 non-prompt γ | `F_Wjjjj` | F2 | 0.018 | 2.0e-04 | 1807 | 7659.1 | F2:L1 |  |
| top: tt̄γγ, tt̄γ, tWγ, tt̄jj | `T_ttaa_1l` | D | 1.9e-04 | 1.9e-04 | 0 | 1.0 | D:L2 |  |
|  | `T_tta_1l` | F1 | 0.005 | 0.003 | 12 | 2.7 | D:L2,F1:L1 |  |
|  | `T_tWa_1l` | F1 | 0.002 | 0.001 | 19 | 1.9 | D:L2,F1:L1 |  |
|  | `T_ttjj_1l` | F2 | 0.003 | 2.0e-04 | 31 | 165.4 | F2:L1 |  |
| tt̄H, tHq, tHW | `H_ttH_1l` | D | 3.0e-04 | 3.0e-04 | 3 | 1.0 | D:L2 |  |
|  | `H_ttH_dilep_wh` | D | 2.6e-04 | 2.6e-04 | 4 | 1.0 | D:L2 |  |
|  | `H_tHq_lep` | D | 0.127 | 0.006 | 484 | 463.7 | D:L0 |  |
|  | `H_tHW_1l` | D | 0.002 | 3.9e-04 | 27 | 26.2 | D:L0 |  |
| ZH (EW, QCD, gg, ττ), lost ℓ | `ZH_ew_zhjj_zll` | D | 0.041 | 6.7e-04 | 3929 | 3751.5 | D:L0 |  |
|  | `ZH_qcd_zhjj_zll` | D | 0.004 | 8.2e-04 | 22 | 21.2 | D:L0 |  |
|  | `H_ggZH_wh` | D | 0.015 | 0.002 | 88 | 85.7 | D:L0 |  |
|  | `H_ZH_tautau_wh` | D | 0.002 | 0.002 | 3 | 1.0 | D:L2 |  |
| Zγγjj, lost ℓ | `ZH_B_QCD_zaajj_nomjj` | D | 0.004 | 0.001 | 4 | 12.6 | D:L1 |  |
|  | `ZH_B_EW_zaajj_vbs_is1h` | D | 0.011 | 0.001 | 17 | 99.8 | D:L1 |  |
|  | `ZH_B_EW_zaajj_vbs_is2` | D | 0.012 | 0.001 | 21 | 128.1 | D:L1 |  |
|  | `ZH_B_EW_zaajj_vbs_is3` | D | 0.004 | 4.1e-04 | 13 | 88.4 | D:L1 |  |
| e→γ: Zγjj, WWγ/WZγ/ZZγ | `F_QCD_llajj_loose` | EG | 0.025 | 0.019 | 1 | 1.7 | D:L2,EG:L2 |  |
|  | `ZH_F_EW_llajj_vbs` | EG | 0.024 | 0.010 | 24 | 6.4 | D:L2,EG:L1 |  |
|  | `V_WWa_WH` | EG | 0.036 | 0.025 | 0 | 2.0 | D:L2,EG:L2 |  |
|  | `V_WZa_WH` | EG | 0.004 | 0.004 | 0 | 1.1 | D:L2,EG:L2 |  |
|  | `V_ZZa_WH` | EG | 8.6e-04 | 6.5e-04 | 0 | 1.7 | D:L2,EG:L2 |  |
| non-prompt ℓ: γγ+3j, VBF H, ggF H | `Q_aajjj` | FL | 0.033 | 0.014 | 461 | 5.5 | D:L2,FL:L1 |  |
|  | `H_VBFH_jj` | FL | 0.016 | 6.0e-04 | 663 | 748.8 | FL:L0 |  |
|  | `H_ggF_jj_nomjj` | FL | 0.010 | 5.5e-04 | 282 | 314.8 | FL:L0 |  |

Total: **s = 1.192, b = 1.263** (def. a). Sources with N_eff < 10 enter at their estimate with their MC-stat or 100 % L2 uncertainty; the conservative variant (all of them at max(value, 3 w̄)) is in the robustness table (07).

## 8. Checks
SHA256 2900/2900 OK; Σw and N closure per sample; BR ledger asserted; N_MC rule enforced by `whana.nmc_check` (fails loudly; it failed on the first run for the three 20k EW Zγγjj beam splits, now checked as the one SAMPLES.csv row of 60k, D-WH-3); D-WH-2 effective-N for `F_Wjjjj` (N/N_req = 0.016) and `T_ttjj_1l` (0.0017): N_eff in the SR 7659 and 165 ≥ 10. Quadratic coupling closure (07). JES rescoring of the BDT reproduces the stored scores exactly at zero shift.

## 9. Caveats
LO generators; no pile-up; per-jet fake parametrisations are scenarios, not measurements; e→γ needs a closure factor 4 for the loose QCD sample; the W+jets and tt̄ fakes are weighted (D-WH-2); several small sources have N_eff < 10; the optimisation chose pT^γγ at the grid edge; BDT stability marginal (§6).

## 10. Next
06 systematics, 07 sensitivity. **Git:** see `git log -- wh/reports/05_selection.md` (run commit; parent at generation 4689548).
