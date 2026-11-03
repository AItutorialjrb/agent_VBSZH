# Phase 03 — generator smoke tests, σ/BR closure, Delphes validation, condor test jobs (WH, multi_r1)

Date UTC: 2026-11-03. **Status: IN-PROGRESS (interactive validation PASS; 8 of the 20 registered samples have a finished test job (test-job coverage is therefore NOT "one per sample type"), namely S_EW_WHjj, H_ttH_1l, H_QCD_WH_mlm, F_Wjj_pilot, F_Wajj_pilot, F_QCD_Wajj_nomjj, B_QCD_Waajj_vbs, B_QCD_Waajj_nomjj. **Untested sample types (no test job, G1 item 9):** T_tta_1l, T_ttaa_1l, T_tWa_1l, T_tt_1l, H_tHq_lep, H_tHW_1l, S_EW_WHjj_taunu, F_EW_Wajj_vbs, F_QCD_Wajj_vbs, H_QCD_WHjj_fixed, I_WHjj (σ-only; no events needed); their cards ran as σ-only smoke tests (rc 0) and F_*_Wajj_vbs/F gridpacks built, but the PY8+Delphes chain is exercised only through the tested types (top-type: H_ttH_1l is the representative). Decision D-WH-9. MISSING for PASS: the EW Wγγjj gridpack B_EW_Waajj_vbs (cluster 884456.3, running ≈ 5 h; sibling QCD gridpacks needed 4.6-4.8 h with 6984 diagrams, EW has 20520) and its test job 884457.3; an EW-type twin; verifier audit of the new jobs).** Git commit: recorded by orchestrator.
Stack, versions, model, PDFs: as Phase 01 (LCG_110, MG5 3.6.3 upstream, Pythia 8.317 CP5, Delphes 3.5.1 slim CMS card, NNPDF31_nnlo_as_0118). Seeds: SPEC 3.4 (P=2, R=11): smoke = sample index 0 (2110001-2110031), gridpacks J=0, test jobs J=1, with 1000×idx from `config/sample_registry.yaml`; uniqueness asserted in `scripts/make_condor.py` (print of all seeds in the run log). **D-WH-1:** the SPEC formula J+1000·idx exceeds the R spacing (10⁴) for idx ≥ 10 (max here 20001), so seed *numbers* of multi_r1 can coincide with those of multi_r2/r3 (different samples, hence not a physics problem, but not unique across runs); uniqueness is asserted only within this run. Proposed fix: R spacing 10⁵.

## 1. Smoke tests: σ (all interactive, ≤ 12 min wall, 4 cores, no bulk)
All cards in `cards/smoke/` (`scripts/make_smoke_cards.sh`, `scripts/make_prod_cards.sh`), runner `scripts/mg5_run_smoke.sh` (patch 000), logs/banners/LHE under `work/smoke/<card>/`. Gen cuts: WH/ZH-like jets pT>20, |η|<5, ΔR(jj)>0.4, `cut_decays=False`; photons as listed in the YAML. LO MG5 σ in fb with the integration error:
| card | seed | σ [fb] (MG5 LO, integration err) | wall [s] |
|---|---|---|---|
| F_Wajj_pilot_smoke | 2110022 | 9616 ± 63 | 202 |
| F_Wjj_pilot_smoke | 2110021 | 3.411e+06 ± 2.6e+04 | 174 |
| H_QCD_WH_0j_smoke | 2110028 | 280.3 ± 2 | 65 |
| H_QCD_WH_mlm_smoke | 2110023 | 862.1 ± 9.3 | 185 |
| H_QCD_WHjj_fixed_smoke | 2110024 | 57.81 ± 0.5 | 144 |
| H_tHW_1l_smoke | 2110016 | 4.668 ± 0.035 | 89 |
| H_tHq_lep_smoke | 2110015 | 14.88 ± 0.15 | 85 |
| H_ttH_1l_smoke | 2110014 | 108.3 ± 0.5 | 81 |
| I_WHjj_smoke | 2110025 | -0.2644 ± 0.013 | 120 |
| Q_aa_0j_smoke | 2110030 | 4774 ± 48 | 64 |
| Q_aajj_smoke | 2110031 | 3542 ± 29 | 99 |
| S_EW_WHjj_smoke | 2110012 | 13.63 ± 0.18 | 121 |
| S_EW_WHjj_taunu_smoke | 2110013 | 6.71 ± 0.11 | 141 |
| T_tWa_1l_smoke | 2110019 | 77.87 ± 0.61 | 82 |
| T_tt_1l_smoke | 2110020 | 1.417e+05 ± 9.9e+02 | 86 |
| T_tta_1l_smoke | 2110017 | 511.2 ± 3.4 | 154 |
| T_ttaa_1l_smoke | 2110018 | 0.5709 ± 0.0047 | 398 |
| wm_light_nodec | 2110002 | 23.66 ± 0.16 | 112 |
| wm_light_nodec_rep | 2110027 | 23.59 ± 0.35 | 109 |
| wm_light_wdec | 2110006 | 5.15 ± 0.03 | 119 |
| wm_light_wdec_bw | 2110029 | 7.069 ± 0.11 | 681 |
| wm_light_wdec_rep | 2110026 | 5.152 ± 0.033 | 101 |
| wp_b_nodec | 2110003 | 82.75 ± 0.46 | 136 |
| wp_bnot_nodec | 2110004 | 178.6 ± 1.4 | 738 |
| wp_int_nodec | 2110009 | -0.1253 ± 0.0083 | 88 |
| wp_light_nodec | 2110001 | 38.4 ± 0.2 | 101 |
| wp_light_wdec | 2110005 | 8.538 ± 0.043 | 120 |
| wp_qcd_nodec | 2110007 | 165.2 ± 0.84 | 98 |

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
| quantity | W⁺→ℓν (1000 ev, seed 2110101) | W⁻→ℓν (1000, 2110102) | S_EW_WHjj condor test (2000, seed 2111001) |
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
| B_QCD_Waajj_nomjj | 2125001 | 2000 / 2000 / 2000 | 1.631 ± 0.011 (1st proc.) | 3.582 ± 0.0064 | 3.558 | -0.7 % | 318/188/8 | 2.68 | b9p17p0675 |
| B_QCD_Waajj_vbs | 2124001 | 2000 / 2000 / 2000 | 0.2657 ± 0.0021 (1st proc.) | 0.6327 ± 0.0011 | 0.6317 | -0.2 % | 394/155/10 | 2.85 | b9p20p9077 |
| F_QCD_Wajj_nomjj | 2128001 | 2000 / 2000 / 2000 | 2625 ± 21 (1st proc.) | 5683 ± 10 | 5735 | +0.9 % | 129/229/13 | 2.46 | b9p16p0159 |
| F_Wajj_pilot | 2130001 | 5000 / 5000 / 5000 | 4545 ± 23 (1st proc.) | 9878 ± 19 | 9838 | -0.4 % | 160/358/12 | 2.44 | b9p26p4110 |
| F_Wjj_pilot | 2129001 | 5000 / 5000 / 5000 | 1.982e+06 ± 1.2e+04 (1st proc.) | 3.435e+06 ± 7.6e+03 | 3.413e+06 | -0.6 % | 63/505/15 | 2.22 | b9p16p0146 |
| H_QCD_WH_mlm | 2113001 | 4000 / 4000 / 1386 | 294.2 ± 1.6 (1st proc.) | 879.6 ± 4.2 | 302.3 | -65.6 % | 70/230/8 | 2.02 | b9g03p0004 |
| H_ttH_1l | 2116001 | 2000 / 2000 / 2000 | 54.24 ± 0.56 (1st proc.) | 107.8 ± 0.31 | 107.8 | +0.0 % | 30/169/12 | 3.11 | b9p26p6528 |
| S_EW_WHjj | 2111001 | 2000 / 2000 / 2000 | 5.137 ± 0.055 (1st proc.) | 13.77 ± 0.037 | 13.68 | -0.7 % | 68/157/12 | 2.29 | b9g03p3647 |

Slim output 2.0-3.1 kB/event (ZH: 1.5-2.8); LHE+PY8+Delphes+slim ≈ 3-4 min per 2000 events. The MLM test shows the expected 34.6 % matching efficiency: the Delphes entry count is the accepted-event count, which must be used in N_MC.
Status of the remaining jobs and the verifier request: `VERIFY_REQUEST.md`, `STATUS.md`.

## 6. Fake-photon pilot (W+jets, two jet→γ fakes; `scripts/fakefactor_pilot_w.py`, patch 001)
5000 events, fixed-order W(→ℓν)+2j (ptj>20, |η|<5, ΔR>0.4), PY8 + slim Delphes, GenTruth N_prompt_photons = 0, parameterised f(j→γ) = 10⁻³(pT/50)^−0.5 (×2 endcap), one lepton pT>25 + MET>30 (illustrative, not optimised), σ input = σ_gridpack·WF = 3.435×10⁶ × 0.96008 = 3.298×10⁶ fb (deliberately WF-corrected; σ_MG = 3.435×10⁶ fb gridpack, PY8 3.413×10⁶ fb; using σ_MG would raise all yields by +4.2 %, i.e. peak 1.5 → 1.6 events, so D-WH-2 conclusions are unchanged), 500 fb⁻¹, `work/xrd/F_Wjj_pilot_fakefactor.json`:
| region | MC events | yield at 500 fb⁻¹ (nominal f) | N_eff | mean weight |
|---|---|---|---|---|
| PRE (1ℓ+MET, ≥2 γ-fakes, ≥2 tag jets pT>30) | 170 | 535 | 80 | 3.1 |
| VBS (+ m_jj>500, \|Δη\|>2.5) | 41 | **44.5** | 20 | 1.1 |
| PEAK (+ 120<m_γγ<130) | 2 | **1.5** | 1.9 | 0.77 |
Scenario scaling: f ×{0.3, 1, 3} per photon → yield ×{0.09, 1, 9} (peak: 0.14 / 1.5 / 14 events). Fraction of the VBS weight lost by a parton-HT filter: 0 % (HT>50), 26 % (>100), 67 % (>150). **Finding: the double-fake W+jets background cannot be shown to be negligible**: the peak-window estimate (1.5 events at nominal f) rests on **2 raw MC events (N_eff = 1.9, i.e. a statistical uncertainty of order ±70 %)**; the signal reference (≈ 0.9 events) is σ_phys × a ZH-like acceptance (≈ 6 %), not this pilot selection (pilot: no b-veto, photons pT>20, 10 GeV window), so the two numbers are *comparable within large uncertainty*. The pilot is plausibly but not demonstrably a lower bound (2-parton fixed order, extra jets only from the shower; the f-model and the x ~ N(0.85,0.1) fake-pT model are assumptions). It cannot be removed by a generator HT filter (loses ≥26 % of the VBS weight at HT>100). Direct production at N ≥ σ·L is impossible (9.8×10⁹ events) → D-WH-2 (human decision needed: accept parameterised-fake bound with a conservative upper variant, or a dedicated VBS-biased W+≥2j sample). **Wγ+2j pilot (one fake, N_prompt = 1; F_Wajj_pilot, 5000 events, seed 2130001, σ input = 9878 × 0.96008 fb, `work/xrd/F_Wajj_pilot_fakefactor.json`)**: PRE 313 MC events → 1014 events (N_eff 236); VBS 38 → **63.6** (N_eff 26); PEAK 2 raw events → **1.3** (N_eff 2.0) at 500 fb⁻¹, nominal f (×{0.3,1,3} per fake). Same caveats: 2 raw peak events (N_eff 2.0), comparable to the signal within large uncertainty, cannot be shown negligible; its generation phase space (ptj>20, pTγ>15) is looser than the production F_*_Wajj_vbs samples.

## 7. Generator-cut safety (twin samples) — status
Twin gridpacks/test jobs (`B_QCD_Waajj_nomjj`, `F_QCD_Wajj_nomjj`, clusters in §5) are submitted; **Result for the Wγ+jets (QCD) twin** (`F_QCD_Wajj_nomjj`, mmjj = 0, test job seed 2128001, 2000 events; `scripts/twin_safety.py`, `work/xrd/twin_F_QCD_Wajj.json`): σ(nomjj) = 5683 ± 10 fb vs σ(vbs, mmjj>400) = 712.4 ± 1.5 fb (12.5 %); parton-level m_jj < 400 GeV in 87.6 % of the twin events. Among twin events passing a loose reco VBS-like selection (≥1 lepton pT>25, ≥1 photon pT>25, ≥2 jets pT>30, |Δη_jj|>2.5): m_jj(reco) > 500 → 27 events, 10 of them with parton m_jj < 400 (**37 ± 9 %** would be lost by the mmjj>400 generator cut); m_jj(reco) > 700 → 13 events, 3 lost (23 ± 12 %). Hence, as in ZH, **the mmjj>400 generator cut is NOT safe for QCD-type samples** at the reco m_jj>500 working point (statistically limited: 27 events); the production QCD-type samples need the ratio correction C (twin ratio) with its MC-stat uncertainty, or a looser generator cut, decided in Phase 04. **Wγγjj (QCD) twin** (`B_QCD_Waajj_nomjj`, σ = 3.582 fb vs vbs 0.6327 fb, test seed 2125001, 2000 events, loose selection with ≥1 photon): parton m_jj < 400 in 82.3 % of events; reco m_jj>500: 82 selected, 39 lost (**47.6 ± 5.5 %**); m_jj>700: 48 selected, 20 lost (41.7 ± 7.1 %) — also NOT safe (ZH: 64 %). The EW-type twin (ZH: 1.4 % loss) is **not yet demonstrated for W**: no EW nomjj twin was planned (the EW Wγγjj gridpack B_EW_Waajj_vbs is still building, D-WH-6); to be generated in Phase 04.


## 8. Checks
Exactly one condor submission per cluster (condor_q checked, 0 duplicates; the `hh` executor's jobs share the account and were not touched). σ stable across seeds (W⁻ ±0.3 %), gridpack vs smoke ≤ 1 %. PY8 σ = LHE σ. Stage-out size check done in-job by the wrapper. FUSE listing lag on EOS for freshly staged files was bypassed with xrootd listing (`scripts/audit_test_jobs.py`). Job/log audit is the verifier's task.

## 9. Caveats
Validation samples are small (500-2000 events); no pile-up; LO; the electron deficit is a stock-card feature; MLM matching (xqcut 10 / qCut 19) is not DJR-validated (Phase 04); the fake-factor pilots are parameterised estimates (N_eff ≈ 2 in the peak window), not data-driven; closure at ±2 %. Nothing here is a yield.

## 10. Next actions
Collect remaining gridpacks/test jobs (B_EW_Waajj_vbs, F_Wajj_pilot, twins), update `config/sample_matrix.yaml` (σ), verifier audit, G1 review of D-WH-1…5 before any Phase-04 production.
