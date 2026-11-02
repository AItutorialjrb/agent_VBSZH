# Phase 03 — generator smoke tests and cross-section consistency (M5)

Date UTC: 2026-11-02. **Status: PASS for S_EW_ZHjj, H_QCD_ZHjj (fixed order), I_ZHjj, H_ttH (σ + 500-event chain); continuum llγγ: NOT passed interactively (timeout), moved to batch gridpacks, §3.**
Stack: [03_stack.md](03_stack.md). Cards: `cards/phase03_smoke/` (run cards = the `set run_card` lines inside each `.mg5`). Runner: `scripts/mg5_smoke.sh <card> <seed>` (MG5 in node-local /tmp, small outputs staged to `work/m5/<card>/`: `mg5.log`, `status.txt`, `Cards/`, banner, LHE or gridpack). All runs interactive on lxplus9109, `nb_core=4`, wall ≤ 100 s except §3.
Common: √s = 13.6 TeV, NNPDF31_nnlo_as_0118 (303600), α_s(m_Z) from PDF, `sm-no_b_mass` 5F, maxjetflavor 5, `use_syst=True` (7-point scale + PDF weights in LHE).

## 1. Cross sections (LO, MG5 integration error)
| Sample (card) | Seed | Gen. cuts | σ [fb] | Scale (7-pt) | PDF | Notes |
|---|---|---|---|---|---|---|
| EW ZHjj, H & Z undecayed (`ew_zhjj_nodecay`) | 13600501 | p_T(j)>20, \|η(j)\|<5, ΔR(jj)>0.4 | **18.64 ± 0.19** | +5.0 / −4.5 % | ±1.0 % | scale-scheme envelope (choices 1–4): −11.7 % |
| EW ZHjj, Z→ee/μμ (`ew_zhjj_zll`, gridpack) | 13600502 | same, `cut_decays=F` | **1.298 ± 0.008** | — | — | gridpack re-run (seed 13600601, 1000 ev): 1.286 ± 0.015 |
| EW×QCD interference (`int_zhjj_nodecay`) | 13600503 | same | **−0.114 ± 0.007** | — | — | −0.61 ± 0.04 % of EW |
| QCD ZHjj (2,2), Z→ll (`qcd_zhjj_zll`, gridpack) | 13600504 | same | **10.25 ± 0.03** | — | — | gridpack 1k ev (seed 13600602): 10.10 ± 0.08 |
| ttH, t→b ℓν both (ℓ=e,μ) (`ttH_dilep`) | 13600507 | none on jets | **17.98 ± 0.20** | +29.7 / −21.3 % | ±1.2 % | includes eμ; MG5 tree W BR |

Ratio QCD/EW (both Z→ll): 10.25/1.298 = 7.9 at generator level.

## 2. Decay and normalisation closure
- **Z→ll (executed):** σ(Z→ll)/σ(undecayed) = 0.06964 ± 0.00083; analytic MG5 tree 2Γ_ll/Γ_Z = 0.06878 (Γ_ll = 83.965 MeV, Γ_Z = 2.441404 GeV, s_W² = 0.22225) → pull 1.0, **PASS**. PDG rescale factors 0.9779 (ee), 0.9788 (μμ).
- **H→γγ (executed):** Pythia 8.317 forced decay; generator record: 1000/1000 (EW), 1000/1000 (QCD), 500/500 (ttH) last-copy H → γγ, 0 other. **PASS.**
- **Weight/σ closure through PY8:** σ_PY8 = 1.290 fb vs LHE 1.286–1.292 fb (EW); 10.13 vs 10.10 fb (QCD); 18.00 vs 17.98 fb (ttH). Pythia does **not** fold BR(H→γγ) into σ → physical B_γγ = 0.002270 applied once, externally. **PASS.**
- **Ledger:** σ_phys(EW ZHjj → ℓℓγγjj) = 1.298 fb × 0.9783 × 0.002270 = **2.88 × 10⁻³ fb** (cross-check: 18.64 × 0.067294 × 0.002270 = 2.85 × 10⁻³ fb, agree within MC error). At 500 fb⁻¹: **1.44 events before any acceptance** (LO; scale ±5 %).

## 3. Continuum llγγ smoke tests
**Status: not passed interactively. Moved to batch (gridpack creation).** Both runs reached the 1500 s timeout (rc = 124; `work/m5/{ew_llaajj,qcd_llaa_mlm02}/status.txt`). No orphaned MG5 processes remained afterwards (checked with `ps`).

| Card | Seed | Subprocesses / diagrams | Progress at timeout | Implication |
|---|---|---|---|---|
| `ew_llaajj` (`l+ l- a a j j QCD=0 QED=6`, ref. cuts, 90<m_γγ<190) | 13600505 | 174 / **282 144** | compile ~15 min, survey 0/1057 channels | needs ≥ 8 cores × O(day) → `scripts/condor/gridpacks_llaa.sub` (testmatch) |
| `qcd_llaa_mlm02` (llγγ + 0,1,2j MLM, xqcut 10) | 13600506 | 230 / **109 600** | survey 1/448 channels after 16 min | same |

The process generation itself succeeded (diagram counts above; the MG5 `QED=6`/MLM syntax is accepted), so the cards are syntactically validated. No σ is available yet, and no zero or placeholder value is used anywhere.

## 4. Pythia8 + Delphes (CMS card, stock) on 1k signal events
Command: `scripts/run_py8_delphes.sh <lhe.gz> cards/phase03_smoke/py8_ew_zhjj_haa.cmnd 1000 13600701 <out.root>` (CP5, NNPDF3.1 NNLO via LHAPDF6, dipole recoil on). 31 s wall for 1000 events. Analysis: `python3 -P scripts/smoke_analysis.py` → `work/m5/<sample>/delphes_smoke/{smoke_summary.json,smoke_validation.png}`.

| Check | EW ZHjj | QCD ZHjj | ttH |
|---|---|---|---|
| m_γγ median (110–140) / 68 % half-width | 125.05 / 2.13 GeV | 124.87 / 2.08 GeV | — |
| fraction of ≥2γ events with 120<m_γγ<130 | 0.88 | 0.87 | — |
| OSSF ee / μμ pairs (of 1000) | 127 / 236 | 127 / 204 | — |
| m_jj median (≥2 jets) | 422 GeV | 202 GeV | — |
| frac m_jj>500 / 60<m_jj<110 (≥2 jets) | 0.46 / 0.11 | 0.12 / 0.16 | — |

Smoke cutflow (σ in fb **before B_γγ**, weighted MC error; photons p_T>20, |η|<2.5 excl. 1.4442–1.566; leptons p_T>15; 70<m_ll<110; jets p_T>25, |η|<4.7; last row illustrative only, **not an optimised selection**):

| Step | EW ZHjj | QCD ZHjj | ttH |
|---|---|---|---|
| all | 1.290 | 10.25 | 17.98 |
| ≥2 γ | 0.577 ± 0.027 | 3.48 ± 0.19 | 6.33 ± 0.48 |
| + OSSF ℓℓ | 0.203 ± 0.016 | 1.23 ± 0.11 | 0.79 ± 0.17 |
| + m_ll window | 0.200 ± 0.016 | 1.20 ± 0.11 | 0.14 ± 0.07 |
| + ≥2 jets | 0.180 ± 0.015 | 0.95 ± 0.10 | 0.14 ± 0.07 |
| + m_jj>500, \|Δη_jj\|>2.5 | **0.106 ± 0.012** (82 ev) | **0.103 ± 0.032** (10 ev) | 0.036 ± 0.036 (1 ev) |

Times B_γγ·(PDG/MG Z factor) = 2.22 × 10⁻³ and 500 fb⁻¹: EW ZHjj ≈ **0.12 events** after the illustrative selection (0.20 after ≥2 jets).

**Detector-model findings (feed Phase 04, decision D11):**
1. Electron deficit: of events with ≥2 generator electrons (p_T>15, |η|<2.5), only 128/362 = 35 % have ≥2 reco electrons, vs 239/376 = 64 % for muons. 72 of 1479 reco photons lie within ΔR<0.1 of a generator electron (collinear FSR or e→γ; not yet distinguished). **Tested hypothesis:** the stock `UniqueObjectFinder` gives photons priority over electrons (card lines 765–771). Variant `cards/phase04_candidates/delphes_card_CMS_vbszh_v0.tcl` (electron priority; same LHE and seeds) raises OSSF ee pairs only from 127 to 141, with μμ 236→234 and m_γγ unchanged (median 124.87 GeV, half-width 2.10 GeV), illustrative-selection σ 0.096 ± 0.011 fb. So the ordering is a **minor** cause. Leading remaining hypothesis: electron relative isolation (`PTRatioMax 0.12`, ΔR<0.5, vs 0.25 for muons) fails because of FSR/H photons in the cone. Phase 04 item.
2. Output size: 106 MB per 1000 events (GenParticle/Tower/EFlow stored), too large for production → slim TreeWriter.
3. Muon pair efficiency of 64 % for in-acceptance pairs is also lower than naive (≈0.9); isolation in busy H/VBS events is the suspect. To be checked in Phase 04.

## 5. Checks
Order separation and diagram closure (01_addendum §A). LHE header σ equals the MG5 result. Seeds are distinct per run and recorded in `status.txt` and banners. No negative weights in unweighted EW/QCD samples. The interference sample is σ-only.

## Caveats
LO only. Tiny samples: the VBS-region numbers carry 10–100 % MC errors and are **not** yields for sensitivity. The stock Delphes card has a known electron→photon artefact. No pileup. The illustrative cuts are not optimised and must not be tuned on these samples.

---
## M6 — HTCondor test-job audit (appended run 2, 2026-11-02 UTC)
Cluster 879052 (EosSubmit schedd), wrapper v1. Sources: `production/test/<s>/<tag>.json`, `<tag>_logs.tgz`, `production/condor_logs/{<tag>.out,test_zhjj.log}`; job status per user report: JobStatus 4, ExitCode 0.

| | EW ZHjj (s13610001) | QCD ZHjj (s13620001) |
|---|---|---|
| events: requested / LHE / Pythia accepted / Delphes entries | 2000 / 2000 / 2000 / 2000 | 2000 / 2000 / 2000 / 2000 |
| σ_gen (LHE init, MG5 MC error), Z→ee/μμ in ME | **1.2964 ± 0.0097 fb** | **10.185 ± 0.071 fb** |
| σ Pythia (sum line) | 1.299 fb | 10.17 fb |
| consistency with M5 (1.298 ± 0.008 / 10.25 ± 0.03 fb) | 0.1σ | 0.9σ |
| BR / decay | Z→ℓℓ in ME (MG tree BR; ×0.9783 PDG rescale); H forced to γγ in PY8 (conditional BR = 1); **×B_γγ = 0.002270 externally, once** | same |
| wall (user) / CPU usr (condor log) | 194 s / 160 s | 231 s / 194 s |
| step times (wrapper log): gridpack / PY8+Delphes | 45 s / 140 s | 43 s / 179 s |
| ROOT (stock card) / LHE.gz | 210.5 MB = **105.3 kB/ev** / 1.2 kB/ev | 247.9 MB = **124.0 kB/ev** / 1.3 kB/ev |
| worker | b9p26p6528 | b9p28p6148 |
| Pythia error summary | 4 events "energy-momentum not conserved" (0.2 %), 1 BeamRemnants failure, 3 "stuck in loop" | 12 "stuck in loop" (warnings) |

**Finding (reproducibility):** the stock CMS card leaves `RandomSeed` unset, so Delphes smearing is clock-seeded. Generator level is reproducible (GenJet and weights bit-identical when re-run with the same Pythia seed), but test-job **reco objects are not**. Fixed in `scripts/run_py8_delphes.sh` (`set RandomSeed <pythia seed mod 9e8 + 1>`): two re-runs are bit-identical. Versus the clock-seeded test job, object counts and mean p_T agree within ≤1.1σ (photons 3007/3024, electrons 1056/1078, muons 1319/1346, jets 6761/6673).

## M6b — run-2 evidence: storage, σ measurements, pilots
### Slim output (validated on the test LHE files, no new MG5 integration)
`cards/phase04_candidates/delphes_card_CMS_slim_v1.tcl` = stock card with identical detector physics. Only the TreeWriter branches Track/Tower/EFlowTrack/EFlowPhoton/EFlowNeutralHadron/FatJet are removed (diff verified). `scripts/slim_gentruth.py` then writes the overlap truth to `<tag>_gen.root` (`GenTruth`: prompt flag by hadron-free M1 ancestry, gen photons/leptons, N_prompt_photons per 02 §3, last-copy H/Z/W/t) and clones `Delphes` without `Particle` (ZSTD-5).

| | EW ZHjj | QCD ZHjj | Z+2j pilot | Zγ+2j pilot |
|---|---|---|---|---|
| slim Delphes + GenTruth | 4.55 + 0.26 MB / 2000 = **2.40 kB/ev** | 5.30 + 0.25 MB = **2.77 kB/ev** | **1.50 kB/ev** | **1.63 kB/ev** |
| reduction vs stock | ×44 | ×45 | — | — |
| slim + truth CPU | 7 s / 2000 ev | 6 s | — | — |

Branches kept: Event, EventLHEF, Weight, WeightLHEF (145 scale/PDF weights), Photon, Electron, Muon, Jet (incl. BTag), MissingET, ScalarHT, GenJet, GenMissingET, plus the GenTruth friend (same entry count, 2000 = 2000). GenTruth on the signal: N_prompt_photons = 0/1/2/3 in 80/580/1301/39 events. The full record is kept only in one test job per sample (`keep_full=1`).
Local end-to-end wrapper-v2 test (200 events, v1 gridpack, seed 13619999): 200 LHE = 200 Delphes; stage-out with size check OK; rerun → "output exists → skip". Output in `production/test_v2_wrapper/`.

### σ measurements (interactive LO, NNPDF31_nnlo_as_0118, gen cuts in the YAML; `work/m5/<card>/status.txt`)
| Card | σ [fb] | Card | σ [fb] |
|---|---|---|---|
| zll_0j (ℓℓ, m_ℓℓ>50, p_T^ℓ>10, \|η\|<2.5) | 1 500 000 ± 12 900 | tt_dilep (e/μ) | 23 470 ± 240 |
| lla_0j (ref. cuts) | 10 080 ± 217 | tta_dilep (p_T^γ>15) | 85.67 ± 1.00 |
| llaa_0j (ref. cuts, 90<m_γγ<190) | 2.893 ± 0.027 | ttaa_dilep (90<m_γγ<190) | 0.0949 ± 0.0013 |
| zh_0j (Z→ℓℓ) | 48.45 ± 0.37 | twa_dilep (DR) | 13.07 ± 0.16 |
| zll_jj_pilot (p_T^j>20) | 211 500 ± 919 | ew_llajj (QED=5, ref. cuts) | 35.6 ± 0.31 |
| llajj_pilot (QCD) | 1 775 ± 6 | wza, zza | **failed / timeout** (see below) |

`wza`/`zza`: the first attempt failed with "grouping of subprocesses not consistent with setcuts.f". With `group_subprocesses False` both timed out at 600 s during compilation, so they are moved to batch. No σ exists; the table uses labelled estimates.

### Initial-state split closure (Z+2j, beam-1 classes g | u c | d s b | antiquarks)
87.16 + 35.72 + 38.60 + 47.11 = **208.6 ± 1.0 pb** vs full 211.5 ± 0.9 pb: −1.4 %, pull −2.1. There is no mirror double-counting (that would be ×2), but the deficit is not yet explained. Status **PLAUSIBLE, not PASS**: repeat at 0.2 % precision (batch) before using split gridpacks.

### Fake-factor pilots (5000 events each, fixed-order 2 partons, slim card; `scripts/fakefactor_pilot.py`, `work/m5/<pilot>/fakefactor.json`)
f(j→γ) = 10⁻³·(p_T/50)^−0.5 (×2 endcap), x ~ N(0.85, 0.10). Overlap rule: N_prompt_photons = 0 (Z+jets) / = 1 (Zγ+jets). Values are events at 500 fb⁻¹.

| Pilot | PRE (≥2γ, Z, ≥2 tags) | VBS (m_jj>500, \|Δη\|>2.5) | PEAK (+120<m_γγ<130) | ⟨w⟩ VBS | lost by HT_parton>50 / >100 GeV (VBS) |
|---|---|---|---|---|---|
| Z+2j, 2 fakes | 36.7 (N_eff 123) | **3.06** (N_eff 32) | **0.19** (N_eff 4.1) | 0.060 | 0 % / 16 % |
| Zγ+2j, 1 fake | 94.9 (N_eff 130) | **5.91** (N_eff 11) | 0 MC events (**not** a zero yield) | 0.33 | 3.1 % / 18 % |

These are lower bounds: fixed-order 2-parton samples obtain the extra jets only from the shower. The fake backgrounds alone exceed the illustrative-selection signal (0.12 events) by ×25–50 in the VBS region and are of comparable order in the peak window.
