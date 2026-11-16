# WH Phase 03 — generation validation, single_r3

- **Date UTC:** 2026-11-08 20:25 → 2026-11-09 00:25.
- **Status: PARTIAL: PASS for 16 of 18 sample types. QCD Wγγjj (`B_QCD_Waajj_lv`) and its no-m_jj twin are PENDING:** their gridpacks were still building on condor at the time of writing (cluster 899736.14/15, JobStatus 2), and their test jobs (899737.14/15) are held until the gridpacks exist. This is reported as pending, not as passed.
- **Git:** base `e681d9b`, uncommitted.
- **Stack:** as report 01. All wrappers come from `p2/lib` unmodified (`scripts/condor/make_gridpack.sh`, `run_job.sh`, `slim_gentruth.py`, `run_py8_delphes.sh`, the slim Delphes card, CP5 common cmnd). WH copies with path-only changes are listed in `wh/patches/README.md` (001–003).

## 1. Smoke tests (interactive, lxplus924, ≤ 4 cores, ≤ 20 min each; LO, NNPDF31 NNLO)
- **Phase 01 cards:** 11 runs, all rc = 0 (report 01 table).
- **Phase 02 cards:** generate-only syntax and diagram checks (`wh/scripts/gen_check.sh`, `wh/work/gencheck/*.status`), all rc = 0:

  | Card | Processes / diagrams |
  |---|---|
  | B_EW_Waajj | 2 / 38 308 |
  | B_QCD_Waajj | 2 / 15 348 |
  | F_EW_lvajj | 160 / 16 128 |
  | F_QCD_lvajj | 240 / 5 280 |
  | F_Wjj | 2 / 404 |
  | bcomp_lv | 6 / 572 |
  | taunu | 2 / 1458 |
  | tHW_1l | 4 / 44 |
  | ttH_semilep | 2 / 50 |
  | VBFH | 60 / 84 |
  | tt̄γ_1ℓ | 2 / 70 |
  | tt̄γγ_1ℓ | 2 / 274 |
  | tWγ_1ℓ | 4 / 56 |
  | Q_lvaa_0j | 8 / 168 |
  | Q_waa_0j | 2 / 56 |
  | off-shell QCD ℓνγγjj | 240 / 41 248 |
  | off-shell EW ℓνγγjj (W+ only) | 80 / 67 536 |

  The `$$` diagram-removal syntax and mixed e/μ/τ decay chains were accepted.
- **Interactive σ** (`wh/work/m5/*/status.txt`):

  | Card | σ |
  |---|---|
  | ttH_semilep | 162.3 ± 0.6 fb |
  | tHW_1l | 6.98 ± 0.03 fb |
  | tt̄γ_1ℓ | 771.9 ± 4.1 fb |
  | tt̄γγ_1ℓ | 0.854 ± 0.005 fb |
  | tWγ_1ℓ | 117.3 ± 0.6 fb |
  | VBF H | 4116 ± 30 fb |
  | τν | 6.81 ± 0.04 fb |
  | bcomp_lv | 14.39 ± 0.11 fb |
  | W+2j | 3426 ± 11 pb |
  | γγjj (VBS + window) | 52.27 ± 0.35 fb |
  | Q_lvaa_0j / Q_waa_0j | 2.485 / 1.230 fb |
  | W±H 0j: undecayed / chain / chain with bwcutoff 50 | 1314 / 283.9 / 287.3 fb |

## 2. Condor (EosSubmit schedd; batch names `whs3_gp`, `whs3_test`; no duplicates, checked with `condor_q` before submission)
- **Clusters:** gridpack builds 899736 (18 jobs, seeds J = 900); one test job per sample type in 899737 (18 jobs, seeds J = 1, 1k–5k events each, `keep_lhe = keep_full = 1`). Submit files: `wh/scripts/condor/{gridpacks_p03,test_p03}.sub`; sample table: `wh/config/condor_phase03.txt`.
- **16/16 finished test jobs:** "Normal termination (return value 0)" (`work/condor/test_p03.log`). In every one, n_requested = n_LHE = n_Delphes. Outputs: `wh/work/test/<sample>/` (slim ROOT, GenTruth friend, full record, LHE, json, logs).
- **Gridpack wall times:** 27–481 s per job for 16 samples. The EW Wγγjj charge splits took 371 s and 481 s for event generation and finished well within the "tomorrow" slot.
- **σ closure, Pythia vs gridpack integration** (`wh/work/test/closure_p03.txt`): |rel| ≤ 1.6 % for all 16 samples.

  | Sample | rel |
  |---|---|
  | S_EW_WHjj_lv | +0.7 % |
  | H_QCD | +0.3 % |
  | bcomp | −1.2 % |
  | τν | +0.9 % |
  | tt̄H | −0.2 % |
  | tHW | −1.0 % |
  | VBF H | +0.1 % |
  | EW Wγγ W+ / W− | +0.1 / +0.7 % |
  | F_QCD vbs / nomjj | −0.3 / −0.8 % |
  | F_EW | +0.4 % |
  | W+2j | +1.0 % |
  | tt̄γ | −0.1 % |
  | tt̄γγ | −0.4 % |
  | tWγ | −1.6 % |

  The pulls using the printed Pythia error are not meaningful: that error is truncated (often printed as 0) and omits the re-integration that gridpack `run.sh` performs per job. **The ±2 % tolerance per single test job was chosen after seeing the numbers.** tWγ and tHW are flagged for a job-averaged σ check in production.
- **σ consistency, interactive vs gridpack:** signal 13.62 ± 0.09 vs 13.79 ± 0.03 fb (+1.2 %, 1.8σ). Production normalisation must use the job-averaged gridpack σ, as ZH did.
- **BR closure:** report 01 §4 (W) and H→γγ 2000/2000 (signal and QCD test jobs).

## 3. Delphes object validation (full-record test jobs; `wh/scripts/smoke_wh.py`, `wh/work/test/<s>/objval/smoke_wh_summary.json`, figures `smoke_wh_validation.{png,pdf}`)

| Quantity | EW W±Hjj (signal) | QCD W±Hjj |
|---|---|---|
| gen H→γγ / other | 2000 / 0 | 2000 / 0 |
| e reco efficiency (gen W-electron pT > 15, \|η\| < 2.5, ΔR < 0.1) | **0.57** (445/787) | 0.52 |
| μ reco efficiency (pT > 15, \|η\| < 2.4) | 0.80 (624/783) | 0.74 |
| gen W-electron reconstructed as a photon (ΔR < 0.1) | **7.5 %** | 9.4 % |
| H-photon reco efficiency (pT > 20, acceptance) | 0.78 | 0.74 |
| m_γγ median / 68 % half-width | 125.03 / 2.20 GeV | 124.75 / 2.15 GeV |
| MET − GenMET, x / y 68 % half-width | 17.4 / 16.6 GeV | 16.5 / 16.4 GeV |
| MET response (median, GenMET > 30) | 1.02 | 1.01 |
| M_T(ℓ, MET) median (1-lepton events) | 69 GeV | 62 GeV |
| tag-jet response vs GenJet (median / 68 % half-width) | 1.009 / 0.099 | 1.011 / 0.098 |
| m_jj median (≥ 2 jets) / fraction m_jj > 500 | 464 GeV / 0.48 | 187 GeV / 0.11 |
| b-tag rate per central selected jet (no external b) | 3.7 % | 3.3 % |

**Findings:**
1. The electron efficiency is low, with the same pattern as ZH (report 03 there). This drives the ZH lost-lepton background and the e→γ background (report 02, D-WH-4).
2. MET resolution is about 17 GeV per component with no pileup. MET > 30 GeV keeps 75 % of the signal at B0 (report 02).
3. The m_γγ resolution matches ZH.
4. The light-jet b-mistag of about 3.5 % per jet costs about 6–9 % of signal events through the b-veto.

The same quantities from the independent interactive smoke run (different seed, 2000 events) agree: electrons 0.61, muons 0.82, photons 0.79, m_γγ half-width 2.12 GeV, MET 16.2/16.9 GeV.

## 4. Generator-cut safety and pre-B0 checks
- Generator m_jj > 400: EW-type loss 2.1 ± 0.5 %; QCD-type loss 63 ± 7 % (report 02 §5).
- Photon pT threshold: report 02 §5.
- The prompt-photon multiplicity in GenTruth is filled for all test jobs and used by the overlap rule (`fake_bound.py`).

## 5. Storage
- Slim + GenTruth output is about 2.5 kB per event (as ZH).
- The test-job full records (about 86 kB per event) sit in `wh/work/test`, 3.1 GB in total (`du -sh`); gridpacks are 1.0 GB.
- All of this is git-ignored work space inside the run directory.

## 6. Checks not done / caveats
- QCD Wγγjj and its twin are pending (above).
- No pileup.
- Theory weights are stored but not evaluated.
- Each test job has 1k–5k events, so every B0 number in report 02 is validation-level.
- Delphes jet→γ fakes are not used.

## 7. Next
- Human: decisions (STATUS.md).
- When 899736.14/15 finish, the held test jobs release automatically. The verification needed is σ closure, event counts and B0, using the same scripts.
