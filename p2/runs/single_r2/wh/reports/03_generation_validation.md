# WH Phase 03 — generation validation (smoke tests, σ/BR closure, Delphes objects, condor test jobs)

- **Date (UTC):** 2026-11-09. **Run:** `single_r2`.
- **Status: PASS for the signal, the resonant QCD W±Hjj, the top-resonant (tt̄H) and the 1-fake-photon (Wγjj) sample types. Overall phase status: BLOCKED (partial).** Continuum Wγγjj: NOT passed.** Its σ integration was still running on HTCondor (cluster 899738.0–2), so it has no gridpack and no test job yet. This is the same situation as the ZH continuum in ZH 03 §3, and it is listed as pending, not as zero.
- **Stack:** `p2/lib/scripts/setup_stack.sh` (LCG_110 + MG5 3.6.3 upstream, Pythia 8.317, Delphes 3.5.1).
  - Pythia: common CP5 card `lib/cards/phase03_smoke/py8_common_CP5.cmnd` + `wh/cards/py8/py8_wh_haa.cmnd` (forced H→γγ) or `py8_wh_noh.cmnd`.
  - Delphes: `lib/cards/phase04_candidates/delphes_card_CMS_slim_v1.tcl` with the seed pinned.

## 1. Commands
```bash
cd p2/runs/single_r2/wh
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
| wrapper test (MG5 integration) | Q_W_aa_0j_onshell | 899735.0 | 2532000 | — | σ = 1.751 fb | 72 s | 0 |
| signal | S_EW_WHjj | 899741.0 | 2501001 / 102501001 | 2000 / 2000 / 2000 | 13.79 vs 13.76 fb | 62 s / 159 s | 0 |
| resonant H (QCD) | H_QCD_WHjj | 899741.1 | 2504001 / 102504001 | 2000 / 2000 / 2000 | 58.36 vs 58.83 fb | 47 s / 219 s | 0 |
| top-resonant H | H_ttH_1l | 899823.0 | 2518001 / 102518001 | 2000 / 2000 / 2000 | 108.6 vs 108.2 fb | 47 s / 241 s | 0 |
| 1 fake photon | F_QCD_Wajj | 899823.1 | 2512001 / 102512001 | 2000 / 2000 / 2000 | 691.5 vs 687.5 fb | 144 s / 211 s | 0 |
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
