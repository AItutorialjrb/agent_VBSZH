# Phase 04 (pre-G2) — production plan, WH (multi_r1) — G2 deliverable

Date UTC: 2026-11-04T09:16Z. **Status: PARTIAL / WAITING ON CONDOR** — the plan is complete in structure and all sample types have gridpack + test job submitted (clusters 884934/884935/884936, plus 884456.3/884457.3 for B_EW_Waajj_vbs); rows whose σ or N is "PENDING" are filled automatically by `scripts/make_plan.py` when the gridpacks/test jobs finish. **No bulk production has been submitted** (rule: none before G2). Nothing below is a yield. Git commit: recorded by the orchestrator.
Inputs: `config/sample_matrix.yaml` (σ, k, ledger; built by `scripts/build_sample_matrix.py`), test-job jsons `work/xrd/`, `work/test/<sample>/`, SPEC §1/§3.4/§4/§6, `reviews/wh_01-03.md`, brief_wh.md. Stack unchanged (LCG_110, MG5 3.6.3 upstream, Pythia 8.317 CP5, Delphes 3.5.1 slim CMS card, NNPDF31_nnlo_as_0118).
Commands: `python3 scripts/build_sample_matrix.py`; `scripts/envrun.sh python3 -P scripts/make_plan.py`; `python3 scripts/make_condor_g2.py`; `scripts/envrun.sh python3 -P scripts/make_prod_sub.py` (writes `work/condor/prod/prod_<sample>.sub`, not submitted); `python3 scripts/assemble_reports.py`.

## 1. G1 decisions implemented
| decision | implementation |
|---|---|
| D-WH-0 | light-flavour signal; top-resonant b class = resonant background: `H_ttH_1l`, `H_tHq_lep`, `H_tHW_1l` in the matrix, each with gridpack + test job; non-top b +5 %/−0 % systematic on S (01 §3) |
| D-WH-1 / D1 | seed = 2 000 000 + 100 000·R + 1000·idx + J (R = 1), J = 100/101/110-119/≥200; `scripts/seeds.py` asserts uniqueness incl. `config/seeds_used_preG1.txt` (120 old seeds kept); mapping `config/seed_mapping_old_to_new.txt` |
| D-WH-2 | `F_Wjjjj` (W+4j ME, 2 jets → photons, 2 ME VBS jets) and `T_ttjj_1l` (tt̄jj ME, b-veto in selection), fake-factor probability weights from the Delphes-calibrated j→γ rate; N set by N_eff ≥ 10 in the SR (target ×3 safety). No biasing generator cut was shown safe, so none is used (see D-WH-10) |
| D-WH-3 | new samples `H_ggZH_wh`, `H_ttH_dilep_wh`, `H_ZH_tautau_wh` (ZH gridpacks read from `production/gridpacks`, never modified; new seeds; output under `p2/production/wh/`); frozen samples of those processes are superseded, not mixed |
| D-WH-4 | f_lepton range: **BLOCKED on a citable table, D-WH-11** (CMS H→ZZ→4ℓ, arXiv:2103.04956 Sec. 7.2 gives f_e, f_μ only graphically); non-prompt result is labelled ESTIMATE (02 §5) |
| D-WH-5 | `V_WZa_WH`, `V_WWa_WH`, `V_ZZa_WH` with `group_subprocesses False`, gridpack + test job; no ME jets (D-WH-12) |
| D-WH-6 | 884456.3 not removed; 884457.3 (held test) releases automatically when the gridpack appears |
| D8 | no generator mmjj cut on nominal samples (`*_nomjj`); mmjj>400 samples only as test-job cross-checks; frozen QCD-type ZH samples carry the twin C at the WH SR proxy (§4) |
| D9 | τ: uplift method (02 §6b), S_EW_WHjj_taunu stays in b — to be confirmed at G2 |
| D10 | one test job per sample type (§2 last column); tt̄γ/tt̄γγ overlap: events with ≥2 prompt photons removed from T_tta/T_tWa, reco-level size in §6; `I_WHjj` is σ-only (k = BR_WLL×B_γγ applied for the σ ratio only; no events enter s or b) |

## 2. Per-sample production plan (generated; PENDING = not yet known, never invented)
| sample | role (s/b class) | σ (fb), source | BR / k (applied once) | generator cuts; twin evidence | N_required | N_planned (accepted) [LHE gen.] | weighting | projected N_eff in SR | seeds | jobs x ev/job (flavour) | CPU-h | storage GB | test job |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S_EW_WHjj | signal (def a: EW only) | 13.77 (gridpack init sigma (smoke run gave 13.63 +- 0.18 fb)) | WFxBGG = 0.0021794 | ptj>20,|etaj|<5,drjj>0.4,drjl>0.4, cut_decays=False (no cuts on decay leptons), scale choi; no generator mjj cut / not applicable | 50000 | 200000 [200000]  | none (unit weights) | 149/2000 in SR proxy (ng=2) -> 14900 sel. events (unweighted => N_eff = N_sel) | 2101200-2101209 | 10 x 20000 (microcentury) | 6.6 | 0.46 | cluster 884457.0, exit 0, LHE=2000, Delphes=2000 (executor-checked; verifier pending) |
| S_EW_WHjj_taunu | signal-like feed-down (W->tau nu->l nu nu) | 6.884 (gridpack init sigma (smoke run gave 6.71 +- 0.11 fb)) | WFTAUxBGG = 0.0023244 | ptj>20,|etaj|<5,drjj>0.4,drjl>0.4, cut_decays=False (no cuts on decay leptons), scale choi; no generator mjj cut / not applicable | 50000 | 100000 [100000]  | none (unit weights) | 24/2000 in SR proxy (ng=2) -> 1200 sel. events (unweighted => N_eff = N_sel) | 2102200-2102209 | 10 x 10000 (microcentury) | 2.3 | 0.22 | cluster 884935.0, exit 0, LHE=2000, Delphes=2000 (executor-checked; verifier pending) |
| H_QCD_WH_mlm | resonant bkg (def a) / signal component of def b | 302.3 (condor test job H_QCD_WH_mlm_s2113001: PY8 sigma after MLM m) | WFxBGG = 0.0021794 | xqcut=10, ptj>10, scale -1; no generator mjj cut / not applicable | 50000 | 200000 [578000]  | none (unit weights); MLM matched, N = accepted | 1/1386 in SR proxy (ng=2) -> 144 sel. events (unweighted => N_eff = N_sel) | 2103200-2103211 | 12 x 50000 (longlunch) | 12.4 | 0.40 | cluster 884457.1, exit 0, LHE=4000, Delphes=1386 (executor-checked; verifier pending) |
| H_QCD_WHjj_fixed | cross-check only (VBS-region efficiency) | 58.61 (gridpack init sigma (smoke run gave 57.81 +- 0.5 fb)) | WFxBGG = 0.0021794 | ptj>20,|etaj|<5,drjj>0.4,drjl>0.4, cut_decays=False (no cuts on decay leptons), scale choi; no generator mjj cut / not applicable | 50000 | 100000 [100000]  | none (unit weights) | 12/2000 in SR proxy (ng=2) -> 600 sel. events (unweighted => N_eff = N_sel) | 2104200-2104209 | 10 x 10000 (microcentury) | 2.5 | 0.26 | cluster 884935.1, exit 0, LHE=2000, Delphes=2000 (executor-checked; verifier pending) |
| I_WHjj | signed EW x QCD interference (def b); sigma is NEGATIVE (computed sign, not structural) (-0.264 +- 0.013 fb undecayed = -0.43 % of EW); enters s/b only as a signed signal-model systematic, never as events | -0.2503 (gridpack init sigma (smoke run gave -0.2644 +- 0.013 fb)) | BR_WLLxBGG = 0.00048442 | ptj>20,|etaj|<5,drjj>0.4,drjl>0.4, cut_decays=False (no cuts on decay leptons), scale choi; no generator mjj cut / not applicable | 50000 | 50000 [50000]  | none (unit weights) | 10/2000 in SR proxy (ng=2) -> 250 sel. events (unweighted => N_eff = N_sel) | 2105200-2105209 | 10 x 5000 (espresso) | 1.3 | 0.09 | cluster 884935.2, exit 0, LHE=2000, Delphes=2000 (executor-checked; verifier pending) |
| H_ttH_1l | resonant bkg | 107.8 (gridpack init sigma (smoke run gave 108.3 +- 0.5 fb)) | WFxWHADxBGG = 0.0022032 | no jet cuts, scale 3; no generator mjj cut / not applicable | 50000 | 200000 [200000]  | none (unit weights) | 3/2000 in SR proxy (ng=2) -> 300 sel. events (unweighted => N_eff = N_sel) | 2106200-2106209 | 10 x 20000 (microcentury) | 5.9 | 0.62 | cluster 884457.2, exit 0, LHE=2000, Delphes=2000 (executor-checked; verifier pending) |
| H_tHq_lep | resonant bkg | 15.63 (gridpack init sigma (smoke run gave 14.88 +- 0.15 fb)) | WFxBGG = 0.0021794 | no jet cuts; no generator mjj cut / not applicable | 50000 | 100000 [100000]  | none (unit weights) | 28/2000 in SR proxy (ng=2) -> 1400 sel. events (unweighted => N_eff = N_sel) | 2107200-2107209 | 10 x 10000 (microcentury) | 2.3 | 0.25 | cluster 884935.3, exit 0, LHE=2000, Delphes=2000 (executor-checked; verifier pending) |
| H_tHW_1l | resonant bkg | 4.679 (gridpack init sigma (smoke run gave 4.668 +- 0.035 fb)) | WFxWHADxBGG = 0.0022032 | no jet cuts; no generator mjj cut / not applicable | 50000 | 100000 [100000]  | none (unit weights) | 4/2000 in SR proxy (ng=2) -> 200 sel. events (unweighted => N_eff = N_sel) | 2108200-2108209 | 10 x 10000 (microcentury) | 2.8 | 0.29 | cluster 884935.4, exit 0, LHE=2000, Delphes=2000 (executor-checked; verifier pending) |
| T_tta_1l | 1 fake gamma (+ prompt gamma) | 512 (gridpack init sigma (smoke run gave 511.2 +- 3.4 fb)) | WFxWHAD = 0.97056 | pta>15,|etaa|<2.5, no jet cuts; no generator mjj cut / not applicable | 1490773 | 1491000 [1491000]  | none (unit weights) | 4/2000 in SR proxy (ng=1) -> 2982 sel. events (unweighted => N_eff = N_sel) | 2109200-2109229 | 30 x 50000 (longlunch) | 34.8 | 4.34 | cluster 884935.5, exit 0, LHE=2000, Delphes=2000 (executor-checked; verifier pending) |
| T_ttaa_1l | irreducible prompt | 0.5816 (gridpack init sigma (smoke run gave 0.5709 +- 0.0047 fb)) | WFxWHAD = 0.97056 | pta>15,|etaa|<2.5, 90<maa<190; no generator mjj cut / not applicable | 50000 | 50000 [50000]  | none (unit weights) | 6/2000 in SR proxy (ng=1) -> 150 sel. events (unweighted => N_eff = N_sel) | 2110200-2110209 | 10 x 5000 (espresso) | 1.8 | 0.15 | cluster 884935.6, exit 0, LHE=2000, Delphes=2000 (executor-checked; verifier pending) |
| T_tWa_1l | 1 fake gamma | 78.6 (gridpack init sigma (smoke run gave 77.87 +- 0.61 fb)) | WFxWHAD = 0.97056 | pta>15,|etaa|<2.5; no generator mjj cut / not applicable | 228857 | 229000 [229000]  | none (unit weights) | 8/2000 in SR proxy (ng=1) -> 916 sel. events (unweighted => N_eff = N_sel) | 2111200-2111209 | 10 x 23000 (microcentury) | 5.7 | 0.61 | cluster 884935.7, exit 0, LHE=2000, Delphes=2000 (executor-checked; verifier pending) |
| B_EW_Waajj_nomjj | irreducible continuum (EW), NOMINAL (no generator mjj cut) | PENDING (gridpack init sigma (pending: 884934.13)) | WF = 0.96008 | pta>25,|etaa|<2.5,100<maa<170,ptj>20,|etaj|<5,dR>0.4,cut_decays=False, mmjj 0; none (nominal); EW twin = this sample vs B_EW_Waajj_vbs (pending) | PENDING | PENDING [PENDING]  | none (unit weights) | PENDING (no test job yet) | PENDING | PENDING (-) | PENDING | PENDING | PENDING |
| B_QCD_Waajj_nomjj | irreducible continuum (QCD), NOMINAL (no generator mjj cut) | 3.582 (gridpack init sigma (smoke run gave 3.582 +- 0.0064 fb)) | WF = 0.96008 | pta>25,|etaa|<2.5,100<maa<170,ptj>20,|etaj|<5,dR>0.4,cut_decays=False, mmjj 0; none (nominal = no mjj cut). Twin 2000 ev: mmjj>400 loses 47.6 +- 5.5 % (loose sel.); 40k twin: no cut >=100 GeV safe (loss 15-45 +- 2 %, 518 sel. events) | 50000 | 50000 [50000]  | none (unit weights) | 23/2000 in SR proxy (ng=2) -> 575 sel. events (unweighted => N_eff = N_sel) | 2115200-2115209 | 10 x 5000 (microcentury) | 3.6 | 0.13 | cluster 884460.0, exit 0, LHE=2000, Delphes=2000 (executor-checked; verifier pending) |
| F_EW_Wajj_nomjj | 1 fake gamma (EW), NOMINAL (no generator mjj cut) | 167.7 (gridpack init sigma (smoke run gave 167.7 +- 0.19 fb)) | WF = 0.96008 | pta>25,ptj>20,..., mmjj 0; none (nominal); EW twin vs F_EW_Wajj_vbs (pending) | 483014 | 484000 [484000]  | none (unit weights) | 207/2000 in SR proxy (ng=1) -> 50094 sel. events (unweighted => N_eff = N_sel) | 2122200-2122209 | 10 x 49000 (workday) | 15.6 | 1.06 | cluster 884935.13, exit 0, LHE=2000, Delphes=2000 (executor-checked; verifier pending) |
| F_QCD_Wajj_nomjj | 1 fake gamma (QCD), NOMINAL (no generator mjj cut) | 5683 (gridpack init sigma (smoke run gave 5683 +- 10 fb)) | WF = 0.96008 | pta>25,ptj>20,..., mmjj 0; none (nominal). Twin 2000 ev: mmjj>400 loses 37 +- 9 %; 40k twin: loss 14-42 +- 2 % for 100-400 GeV (531 sel. events) | 16368344 | 16369000 [16369000]  | none (unit weights) | 13/2000 in SR proxy (ng=1) -> 106398 sel. events (unweighted => N_eff = N_sel) | 2118200-2118527 | 328 x 50000 (workday) | 843.5 | 40.32 | cluster 884460.1, exit 0, LHE=2000, Delphes=2000 (executor-checked; verifier pending) |
| F_Wjjjj | 2 fake gammas (weighted; replaces the W+2j pilot) | 4.147e+05 (gridpack init sigma (smoke run gave 4.147e+05 +- 4.1e+02 fb)) | WF = 0.96008 | ptj>20,|etaj|<5,dR>0.4, no bias cut (no safe bias cut established); no generator mjj cut / not applicable | 1194431164 | PENDING [PENDING] **flag D-WH-2 (N_eff rule, N set in report 04)** | fake-factor (probability) weights | fake-factor weighting; N_planned from N_eff>=10 projection: PENDING (test job + scripts/fakefactor_pilot_w.py) | PENDING | PENDING (-) | PENDING | PENDING | PENDING |
| T_ttjj_1l | tt 1l, 2 fake gammas (weighted) | 8.579e+04 (gridpack init sigma (smoke run gave 85790 +- 1.5e+02 fb)) | WFxWHAD = 0.97056 | ptj>20,|etaj|<5,dR>0.4, no bias cut; no generator mjj cut / not applicable | 249791843 | 50000 [50000] **flag D-WH-2 (N_eff rule, N set in report 04)** | fake-factor (probability) weights | fake-factor weighting; test job (5000 ev): PEAK(final-SR-like)-region n_events=40, N_eff=29.27 -> N_eff/event = 5.85e-03; planned N gives projected N_eff = 292.7 (target >= 10, x3 safety) | 2127200-2127209 | 10 x 5000 (espresso) | 1.8 | 0.16 | cluster 884935.9, exit 0, LHE=5000, Delphes=5000 (executor-checked; verifier pending) |
| V_WZa_WH | WZ gamma -> l l l nu gamma, lost lepton / e->gamma | 5.128 (gridpack init sigma (smoke run gave 5.128 +- 0.0058 fb)) | one = 1 | ptl>5,|etal|<3.5,mmll>10,dRll>0.1,pta>15,|etaa|<2.5; NO ME jets (jets from PS only); no generator mjj cut / not applicable | 50000 | 50000 [50000]  | none (unit weights) | 1/2000 in SR proxy (ng=2) -> 25 sel. events (unweighted => N_eff = N_sel) | 2123200-2123209 | 10 x 5000 (microcentury) | 3.3 | 0.10 | cluster 884935.15, exit 0, LHE=2000, Delphes=2000 (executor-checked; verifier pending) |
| V_WWa_WH | WW gamma / ZZ(llnunu) gamma -> l nu l nu gamma | 28.09 (gridpack init sigma (smoke run gave 28.09 +- 0.038 fb)) | one = 1 | ptl>5,|etal|<3.5,mmll>10,dRll>0.1,pta>15,|etaa|<2.5; NO ME jets (jets from PS only); no generator mjj cut / not applicable | 84270 | 85000 [85000]  | none (unit weights) | 0/2000 in SR proxy (ng=2); 95% UL on SR fraction 1.5e-03 -> N_sel < 128 | 2124200-2124209 | 10 x 9000 (microcentury) | 5.2 | 0.16 | cluster 884935.16, exit 0, LHE=2000, Delphes=2000 (executor-checked; verifier pending) |
| V_ZZa_WH | ZZ gamma -> 4l gamma, 3 leptons lost | PENDING (gridpack init sigma (pending: 884934.12)) | one = 1 | ptl>5,|etal|<3.5,mmll>10,dRll>0.1,pta>15,|etaa|<2.5; NO ME jets (jets from PS only); no generator mjj cut / not applicable | PENDING | PENDING [PENDING]  | none (unit weights) | PENDING (no test job yet) | PENDING | PENDING (-) | PENDING | PENDING | PENDING |
| H_ggZH_wh | ggZH loop, Z->ee/mumu (PY8), 1 lepton lost (D-WH-3 top-up) | 74.33 (SMOKE RUN (no gridpack sigma yet): ZH FINAL_report table (sa) | BR_ZLLxBGG = 0.00015276 | none (PY8 decay, no cuts); no generator mjj cut / not applicable | 50000 | 50000 [50000]  | none (unit weights) | 5/2000 in SR proxy (ng=2) -> 125 sel. events (unweighted => N_eff = N_sel) | 2128200-2128209 | 10 x 5000 (microcentury) | 2.7 | 0.12 | cluster 884935.18, exit 0, LHE=2000, Delphes=2000 (executor-checked; verifier pending) |
| H_ttH_dilep_wh | ttH dilepton, 1 lepton lost (D-WH-3 top-up) | 18.11 (SMOKE RUN (no gridpack sigma yet): ZH FINAL_report table (sa) | WFxWFxBGG = 0.0020924 | no jet cuts, scale 3; no generator mjj cut / not applicable | 50000 | 50000 [50000]  | none (unit weights) | 3/2000 in SR proxy (ng=2) -> 75 sel. events (unweighted => N_eff = N_sel) | 2129200-2129209 | 10 x 5000 (espresso) | 1.8 | 0.14 | cluster 884935.19, exit 0, LHE=2000, Delphes=2000 (executor-checked; verifier pending) |
| H_ZH_tautau_wh | ZH, Z->tautau (MLM 0-2j), tau->l feed-down (D-WH-3 top-up) | 24.97 (SMOKE RUN (no gridpack sigma yet): ZH FINAL_report table (si) | BGG = 0.00227 | xqcut as ZH; no generator mjj cut / not applicable | 50000 | 50000 [151000]  | none (unit weights); MLM matched, N = accepted | 0/1333 in SR proxy (ng=2); 95% UL on SR fraction 2.3e-03 -> N_sel < 113 | 2130200-2130209 | 10 x 16000 (microcentury) | 4.6 | 0.10 | cluster 884935.20, exit 0, LHE=4000, Delphes=1333 (executor-checked; verifier pending) |


Notes. σ = LO MG5 (gridpack init σ preferred; smoke σ or frozen ZH σ otherwise, as stated per row). "N_planned" = accepted (Delphes-level) events; "[LHE gen.]" divides by the MLM/accept fraction of the test job. "Projected N_eff in SR" = test-job selected events in the **SR proxy** of `scripts/srsel.py` (not the final Phase 05 baseline) scaled to N_planned (unit weights ⇒ N_eff = N_sel); for 1-fake samples (ng = 1) it ignores the weight of the second (fake) photon, so it is an upper projection of the raw MC support. With 2000-event tests a low count carries a large Poisson error. CPU/storage use the per-sample test cost (s/event, kB/event) where a test exists, defaults 0.13 s/ev and 2.8 kB/ev otherwise.

## 3. Totals and N-rule check
planned new production (rows with known N): jobs=540, CPU-h=960, storage=50.0 GB (budget WH <= 200 GB)

```
nmc_check on 19 planned rows (br_ledger.nmc_check, N >= max(50k, sigma*k*3000)): PASS
PENDING (sigma or N not yet known): B_EW_Waajj_nomjj, F_Wjjjj, V_ZZa_WH
weighted rows (N_eff>=10 rule in the PEAK region, NOT sigma*L): F_Wjjjj: PENDING (no pilot json); T_ttjj_1l: nt = 5.85e-03; planned N gives projected N_eff = 292.7 (target >= 10, x3 safety)

```
Samples not entering s or b (test job only, no production): `B_EW_Waajj_vbs`, `B_QCD_Waajj_vbs`, `F_EW_Wajj_vbs`, `F_QCD_Wajj_vbs` (mmjj>400 twin cross-checks), `F_Wjj_pilot`, `F_Wajj_pilot` (exploratory pilots), `T_tt_1l` (check; superseded by `T_ttjj_1l`), `H_QCD_WHjj_fixed` (cross-check of the VBS-region efficiency, never added to H_QCD_WH_mlm; N_planned in the table follows the 100k plan), `I_WHjj` (σ-only). Exceptions to the N rule: none besides D-WH-2 weighted rows (N_eff rule). The nmc_check line names every row that is evaluated and every row pending.

## 4. Frozen ZH samples reused as WH background (read-only)
| frozen ZH sample (read-only reuse) | role | σ (fb), source | k | N available | N_required | generator cuts; correction | status |
|---|---|---|---|---|---|---|---|
| ZH_EW_ZHjj_lostlep | ZHjj EW, Z->ll, 1 lepton lost | 1.295, FINAL_report.md table (ZH, LO MG5 init) | 0.0022207 | 200000 | 50000 | ptj>20,|etaj|<5,drjj>0.4; none | N OK |
| ZH_QCD_ZHjj_lostlep | ZHjj QCD (2,2), Z->ll, 1 lepton lost | 10.21, FINAL_report.md table (ZH, LO MG5 init) | 0.0022207 | 100000 | 50000 | ptj>20,|etaj|<5,drjj>0.4; none | N OK |
| ZH_Zaajj_EW_lostlep | Zgg jj EW (on-shell Z->ll), 1 lepton lost | 0.0393, FINAL_report.md table (ZH, LO MG5 init) | 0.9783 | 60000 | 50000 | pta>25,etaa<2.5,100<maa<170,mjj>400; C PENDING: EW part: ZH measured 1.4 % loss at the ZH selection; W EW twin (B_EW_Waajj_nomjj vs _vbs) pending as proxy; sy | N OK |
| ZH_Zaajj_QCD_lostlep | Zgg jj QCD (on-shell Z->ll), 1 lepton lost | 0.0356, FINAL_report.md table (ZH, LO MG5 init) | 0.9783 | 100000 | 50000 | pta>25,etaa<2.5,100<maa<170,mjj>400; C = 1.955 (stat 7 %, syst = full difference 0.955); frozen ZH twin pair B_QCD_zaajj_nomjj/_vbs (100k+100k ev) at the WH SR proxy, ng=2 | N OK |
| ZH_Zajj_eFake | Z(ll)gamma jj with e->gamma (QCD+EW), lepton+photon pairs | 80.51, FINAL_report.md table (ZH, LO MG5 init) | 1 | 6489548 | 241530 | ptl>10,mmll>50,mjj>400,pta>25; C = 1.866 (stat 5 %, syst = full difference 0.866); frozen ZH twin pair F_QCD_llajj_nomjj/_vbs (first 200k ev each), ng=1; QCD part only, EW p | N OK |

Correction C = nomjj/vbs reco-SR-proxy yield ratio measured on the frozen ZH twin pairs (`scripts/ratio_C.py`, `work/ratioC_*.json`); uncertainty = MC stat ⊕ full difference (C − 1) (ZH method). Deviation logged (§8).

## 5. Seeds, duplicate check and condor submission plan
Seeds: formula and J-ranges in §1; G2-prep seeds `config/seeds_g2.txt` (57 incl. EW twins), production seeds `scripts/make_prod_sub.py` (uniqueness asserted). **Submitted so far (pre-G2 allowed):** gridpacks cluster **884934** (16 procs, one per new sample), test jobs cluster **884935** (21 procs, hold-and-release until the gridpack exists), QCD twin jobs cluster **884936** (10 procs: 5 × 8000 ev for each of B_QCD_Waajj_nomjj, F_QCD_Wajj_nomjj, LHE kept), earlier clusters 884456 (gridpacks, 884456.3 running), 884457 (tests), 884460, 884860. `condor_q` was checked before each submission (no existing job of the same name). The EW twin production jobs (`work/condor/g2_twins_ew.sub`, 2 × 5 × 8000 ev) are prepared and will be submitted after their EW test jobs succeed. **After G2:** one cluster per sample from `work/condor/prod/prod_<sample>.sub` (generated for every sample with known N; the rest after their σ is known), each preceded by a `condor_q` duplicate check, stage-out to `p2/production/wh/<sample>/`, the wrapper skips existing outputs and never overwrites (no duplicates by construction).

## 6. tt̄γ / tWγ vs tt̄γγ overlap after the b-veto (G1 item 4)
```
{
 "T_tta_1l": {
  "N": 2000,
  "sigma_k_fb": 496.92436375648833,
  "frac_ge2_prompt_photons": 0.013,
  "n_SRproxy_all": 0,
  "n_SRproxy_ge2prompt": 0,
  "yield_all_500": 0.0,
  "yield_ge2prompt_500": 0.0,
  "err_ge2prompt_500": 124.23109093912208,
  "note": "Poisson error; 0 events => UL 3 events: 373"
 },
 "T_tWa_1l": {
  "N": 2000,
  "sigma_k_fb": 76.28565427980466,
  "frac_ge2_prompt_photons": 0.0145,
  "n_SRproxy_all": 0,
  "n_SRproxy_ge2prompt": 0,
  "yield_all_500": 0.0,
  "yield_ge2prompt_500": 0.0,
  "err_ge2prompt_500": 19.071413569951165,
  "note": "Poisson error; 0 events => UL 3 events: 57.2"
 },
 "T_ttaa_1l": {
  "N": 2000,
  "sigma_k_fb": 0.564475019454636,
  "frac_ge2_prompt_photons": 0.6425,
  "n_SRproxy_all": 0,
  "n_SRproxy_ge2prompt": 0,
  "yield_all_500": 0.0,
  "yield_ge2prompt_500": 0.0,
  "err_ge2prompt_500": 0.141118754863659,
  "note": "Poisson error; 0 events => UL 3 events: 0.423"
 }
}```
Reading: zero MC events pass the SR proxy in the 2000-event tests. **Zero is not a bound.** The 95 % CL upper limits on the removed (≥2-prompt-photon) yield after the b-veto and SR-proxy selection, at 500 fb⁻¹, are **< 373 events (T_tta_1l), < 57 events (T_tWa_1l)**, and < 0.42 events for the full T_ttaa_1l (3-event Poisson limits ×σ·k·L/N); they are uninformative and the overlap is **not** declared negligible. Measured: the ≥2-prompt-photon fraction is 1.3 % (T_tta_1l) and 1.45 % (T_tWa_1l); the removed part has σ·k ≈ 6.5 fb and 1.1 fb before selection versus 0.564 fb for T_ttaa_1l. The removal is applied (as in ZH). **How to get a usable bound:** a limit below 1 event needs N > 3·σ·k·L = 7.5×10⁵ (T_tta_1l) and 1.1×10⁵ (T_tWa_1l) events; the planned production samples (T_tta_1l 1.49×10⁶, T_tWa_1l 2.3×10⁵) reach this, so the bound is computed from the ≥2-prompt-photon subset of those samples in Phase 05 (no extra generation), with the T_ttaa_1l yield as the comparison; if it is not small, a 100 % systematic on the T_tta_1l 2-photon component is carried.

## 7. Verification status of the test jobs
Executor audit: `scripts/audit_test_jobs.py` (LHE = Delphes entries, σ_LHE vs gridpack vs PY8, wall, kB/event) → `work/test_summary.md`; independent verification: `VERIFY_REQUEST.md` (for each finished job and gridpack). σ note: `H_tHq_lep` gridpack σ = 15.63 ± 0.07 fb vs smoke 14.88 fb (+5 %): different MG5 seeds/integration; the gridpack value is used.

## 8. Deviations (to be logged by the orchestrator in SPEC §7)
1. **D-WH-2:** the HH effective-N policy is extended to two WH backgrounds (fake-weighted `F_Wjjjj`, `T_ttjj_1l`); N from N_eff ≥ 10 in the SR proxy, not σ·k·L.
2. **D8:** frozen ZH QCD-type samples with mmjj>400 used with twin C (stat ⊕ full-difference); EW-type C from the W EW twin (proxy).
3. The twin/N_eff projections use the SR **proxy** of `scripts/srsel.py` (Phase 05 baseline not yet fixed); to be redone at Phase 05.
4. `V_*_WH` samples have no ME jets (VBS jets from PS): lower-bound-like, D-WH-12; ZH-frozen `ZH_Zajj_eFake` has partial lepton-acceptance coverage.
5. ZH gridpacks are read (not modified) for the D-WH-3 top-ups; all outputs and seeds are new.
6. `H_QCD_WH_mlm` N_planned counts accepted MLM events; ttH dilepton k uses WF² (ZH used B_γγ only).
7. `F_QCD_Wajj_nomjj` is planned at full N = 1.64×10⁷ (≈ 520 core-h, ≈ 40 GB); the cheaper alternative is mmjj>400 + C (a deviation); full N chosen as the D8-preferred option (confirm: D-WH-13).

## 9. Decisions needed (for the human, via the orchestrator)
- **D-WH-10** (informational/confirm): D-WH-2 needs ME-level W+4j and tt̄jj (pilots had PS VBS jets); no safe biasing cut found, so weighted unbiased samples; CPU/storage in §2 once their σ and N_eff are known.
- **D-WH-11** (blocker for D-WH-4): supply a citable numeric table (paper + table/HEPData id) for the CMS tight-ID lepton fake rate; until then the per-jet range is the unvalidated ZH assumption.
- **D-WH-12**: WZγjj/ZZγjj with ME jets (7-8 bodies) not generated; accept the no-ME-jet V samples with the stated limitation, or approve long-running ME gridpacks.
- **D-WH-13**: confirm full N for `F_QCD_Wajj_nomjj` (D8 option 1) vs mmjj>400 + C.
- **D9**: confirm the τ default (S_EW_WHjj_taunu in b; uplift r_τ ±100 %).
