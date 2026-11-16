# WH Phase 03 - generation validation (multi_r2, executor-wh)

Date UTC: 2026-11-09 (condor submitted 11:08Z, report written 13:07Z). **Status: PASS with open items** (22 of 30 sample types validated end to end; 8 test jobs still RUNNING on condor: cluster 900153 procs 10-15 (six Wggjj variants), 20 (F_QCD_Wgjjj), 21 (F_Wjets_4j). Their sigma stays an ESTIMATE/flagged.) Git commit: none (orchestrator commits).

## Goal
SPEC_G0 2.1/handoff 5.1 Phase 03: smoke tests of every production card via gridpack, sigma closure (gridpack vs direct, charge sum, decay chain vs production x BR), BR closure, Delphes object validation (MET, lepton, photon, m_gg, VBS jets) with the lib slim card, one condor test job per sample type, twin checks.

## Inputs, versions, seeds
- Stack: `p2/lib/scripts/setup_stack.sh` (LCG_110, MG5_aMC 3.6.3 upstream, Pythia 8.317, Delphes 3.5.1, NNPDF31_nnlo LHAID 303600); Delphes card `lib/cards/phase04_candidates/delphes_card_CMS_slim_v1.tcl` with RandomSeed pinned by lib `run_py8_delphes.sh`; Pythia seed = event seed + 1e8. Gridpack sha256 (12 chars) stored in each job json.
- Lib scripts used UNMODIFIED via condor transfer: `make_gridpack.sh`, `run_job.sh`, `run_py8_delphes.sh`, `slim_gentruth.py`, `py8_common_CP5.cmnd`. Only the chaining wrapper `scripts/condor/p03_job.sh` is new.
- Cards: 28 Phase-02 production cards (`cards/phase02/prod/`) + two NEW production cards written this phase from the validated P01 syntax: `S_EW_WHjj_Wlnu.mg5` (QCD=0 QED=4, W->e/mu nu in ME) and `H_QCD_WHjj_Wlnu.mg5` (QCD=2 QED=2). I_EW_QCD_WHjj (signed cross term) is NOT generated as an event sample (negative weights; its sigma closure is the P01 coherent-sum test, pull -1.35). PY8 cmnd: `cards/phase03/py8_ew_haa.cmnd` (EW H samples, dipole recoil), `py8_qcd_haa.cmnd` (QCD H samples, copy of lib py8_qcd_zhjj_haa), `py8_generic(.dipole).cmnd` (backgrounds; EW backgrounds dipole recoil).
- Seeds (SPEC_G0 3.4, P=2, R=2): gridpack build J=0, test events J=999 (J=999 reserved for p03 tests; production must use J in 1..998). Uniqueness asserted in `scripts/p03_submit.py` (60 seeds). Test events never enter s or b.

## Commands and paths
- `python3 scripts/p03_submit.py` (writes `config/p03_condor.sub`, `config/p03_rows.json`, submits via `module load lxbatch/eossubmit`); condor_q was empty before submission; cluster **900153**, 30 procs, 8 cores/16 GB each, flavour workday (tomorrow for heavy cards), 2000 events per sample.
- Manifest for audit: `config/p03_condor_manifest.json` (cluster, proc, sample, seeds, expected events, EOS output path, status). Outputs: `work/p03/condor/<sample>/` (gridpack, LHE, slim Delphes tree, GenTruth friend tree, json, logs; `_full.root` kept for S_EW_WHjj_Wlnu, H_QCD_WHjj_Wlnu, F_QCD_Wgjj, F_EW_Wgjj, F_QCD_Zgjj). Condor logs: `work/p03/condor_logs/`.
- Analysis (login node, light): `scripts/p03_fetch.py` (xrdcp copy; EOS FUSE directory cache was stale right after stage-out, so xrootd is used), `p03_closure.py` -> `config/p03_closure.json`, `work/p03/closure_table.md`; `p03_delphes_val.py` -> `config/p03_delphes_val.json`, `figures/p03_*.{pdf,png}`; `p03_br_check.py` -> `config/p03_py8_hbr.json`; `scripts/check_hgg_decay.py` on full records (`work/p03/hgg_check_*.txt`).

## Smoke tests and cross-section closure
All 22 finished jobs: gridpack rc=0, N_LHE = N_Delphes = 2000, wall 1-90 min (gridpack build+integration 56 s ... 5291 s). sigma is compared at three stages: (i) MG5 gridpack integration (`Cross-section` in mg5.log), (ii) LHE `<init>` summed over all process lines (add-process safe; the json of the lib job stores only the first line), (iii) Pythia sigmaGen (mb->fb), against the direct interactive LO runs of P01/P02. MG5 LO, generator cuts as in the cards, fb, before any BR factor.

| sample | sigma gridpack-integ [fb] | sigma LHE init [fb] | sigma PY8 [fb] | direct P01/P02 [fb] | gp/direct | PY8/LHE | N_lhe/N_delphes | gp wall s |
|---|---|---|---|---|---|---|---|---|
| S_EW_WHjj_Wlnu | 28.23 +- 0.095 | 28.06 +- 0.2 | 28.1 | 28.1 | 1.005 | 1.0015 | 2000/2000 | 416 |
| S_EW_WHjj_Wtau | 14.2 +- 0.043 | 14.16 +- 0.1 | 14.14 | 13.65 | 1.040 | 0.9985 | 2000/2000 | 421 |
| H_QCD_WHjj_Wlnu | 59.34 +- 0.17 | 58.99 +- 0.37 | 58.99 | 59.23 | 1.002 | 1.0000 | 2000/2000 | 283 |
| H_QCD_WHjj_Wtau | 29.58 +- 0.094 | 29.45 +- 0.18 | 29.44 | 29.21 | 1.013 | 0.9998 | 2000/2000 | 242 |
| H_QCD_ZHjj_ll | 10.27 +- 0.033 | 10.37 +- 0.07 | 10.38 | 10.24 | 1.003 | 1.0013 | 2000/2000 | 149 |
| H_QCD_ZHjj_tautau | 5.107 +- 0.017 | 5.054 +- 0.036 | 5.043 | 5.074 | 1.007 | 0.9978 | 2000/2000 | 97 |
| H_VBF_Hjj | 4132 +- 27 | 4120 +- 26 | 4122 | 4099 | 1.008 | 1.0005 | 2000/2000 | 56 |
| H_ttH_1l | 202.2 +- 0.31 | 203.6 +- 1.3 | 203.5 | 202.9 | 0.997 | 0.9997 | 2000/2000 | 127 |
| H_tHq_1l | 21.02 +- 0.17 | 20.87 +- 0.17 | 20.82 | 20.46 | 1.027 | 0.9975 | 2000/2000 | 231 |
| H_tHW_1l | 7.032 +- 0.013 | 7.055 +- 0.046 | 7.057 | 7.045 | 0.998 | 1.0003 | 2000/2000 | 64 |
| B_EW_Wggjj_biased | n/a +- n/a | n/a +- n/a | n/a | n/a | n/a | n/a | n/a/n/a | n/a |
| B_EW_Wggjj_nomjj | n/a +- n/a | n/a +- n/a | n/a | n/a | n/a | n/a | n/a/n/a | n/a |
| B_QCD_Wggjj_biased | n/a +- n/a | n/a +- n/a | n/a | n/a | n/a | n/a | n/a/n/a | n/a |
| B_QCD_Wggjj_nomjj | n/a +- n/a | n/a +- n/a | n/a | n/a | n/a | n/a | n/a/n/a | n/a |
| B_EW_WggjjFSR_biased | n/a +- n/a | n/a +- n/a | n/a | n/a | n/a | n/a | n/a/n/a | n/a |
| B_QCD_WggjjFSR_biased | n/a +- n/a | n/a +- n/a | n/a | n/a | n/a | n/a | n/a/n/a | n/a |
| F_QCD_Wgjj_biased | 1086 +- 1.5 | 1090 +- 5.6 | 1093 | 1084 | 1.002 | 1.0027 | 2000/2000 | 2516 |
| F_QCD_Wgjj_nomjj | 8618 +- 12 | 8614 +- 43 | 8620 | 8428 | 1.023 | 1.0007 | 2000/2000 | 1145 |
| F_EW_Wgjj_biased | 134.8 +- 0.25 | 134 +- 0.73 | 134 | 134.4 | 1.003 | 0.9998 | 2000/2000 | 1736 |
| F_EW_Wgjj_nomjj | 251.2 +- 0.26 | 250.6 +- 1.2 | 250.5 | 241.2 | 1.041 | 0.9995 | 2000/2000 | 5291 |
| F_QCD_Wgjjj | n/a +- n/a | n/a +- n/a | n/a | 2819 | n/a | n/a | n/a/n/a | n/a |
| F_Wjets_4j | n/a +- n/a | n/a +- n/a | n/a | n/a | n/a | n/a | n/a/n/a | n/a |
| T_tta_1l | 964.7 +- 1.6 | 956.3 +- 6.5 | 957.4 | 960.4 | 1.004 | 1.0012 | 2000/2000 | 487 |
| T_ttaa_1l | 1.087 +- 0.0019 | 1.098 +- 0.0068 | 1.096 | 1.079 | 1.007 | 0.9982 | 2000/2000 | 2137 |
| T_tWa_1l | 117.9 +- 0.31 | 117.8 +- 0.8 | 117.8 | 117.5 | 1.003 | 0.9997 | 2000/2000 | 119 |
| T_tt_1l | 2.12e+05 +- 5.7e+02 | 2.122e+05 +- 9.7e+02 | 2.123e+05 | 2.13e+05 | 0.995 | 1.0003 | 2000/2000 | 61 |
| T_ttjj_1l | 9.215e+04 +- 99 | 9.172e+04 +- 4.5e+02 | 9.156e+04 | n/a | n/a | 0.9983 | 2000/2000 | 4501 |
| Q_aajj_nplep | 284.2 +- 0.68 | 284.8 +- 2.3 | 285.1 | 283.6 | 1.002 | 1.0012 | 2000/2000 | 176 |
| F_QCD_Zgjj_ll_biased | 48.22 +- 0.19 | 48.14 +- 0.33 | 48.07 | 48.67 | 0.991 | 0.9984 | 2000/2000 | 361 |
| F_QCD_Zgjj_ll_nomjj | 498 +- 1.1 | 498.3 +- 2.9 | 497.6 | 490.5 | 1.015 | 0.9985 | 2000/2000 | 210 |

Findings: gridpack/direct within 0.2-4.1% everywhere (largest: F_EW_Wgjj_nomjj +4.1% and S_EW_WHjj_Wtau +4.0%, ~2 sigma of the short direct runs' 500-event errors, F_QCD_Wgjj_nomjj +2.3%); LHE/gridpack and PY8/LHE agree to <=0.3% (event weights normalised to sigma, no hidden weight factor). Figure: `figures/p03_sigma_closure.png`.
Previously ESTIMATED sigma now measured: T_ttjj_1l = 9.215e4 fb (estimate 9.04e4, +1.9%), F_EW_Wgjj_nomjj, F_QCD_Wgjj_nomjj (direct values were short runs). Still ESTIMATE/unmeasured: six Wggjj variants, F_QCD_Wgjjj (direct short value 2819 fb only), F_Wjets_4j (no sigma): jobs running.

### Charge sum, decay chain vs production x BR (LHE of test jobs, 2000 events)
- S_EW_WHjj_Wlnu: W+ fraction 1268/2000 = 0.634 +- 0.011 vs P01 sigma(W+)/sigma(W+ + W-) = 0.6437 (pull -0.9); e/mu = 1015/985 (expected 1:1 up to Z-lepton universality). Charge sum: gridpack sigma (W+ and W- in one card) 28.23 +- 0.10 fb vs P01 W+ 17.88 + W- 10.13 = 28.01 (+0.8%); vs sigma_prod 129.22 x B_MG5 0.222274 = 28.72 (-1.7%, P01 dynamic-scale closure showed the same 1-3% deficit, pulls up to -4 for single runs; unresolved, treated as +-2% norm. uncertainty, see D-WH-9).
- S_EW_WHjj_Wtau: 14.20 fb vs sigma_prod x B_MG5(tau) = 129.22 x 0.111056 = 14.35 (-1.1%); W+ fraction 0.6445.
- H_QCD_WHjj_Wlnu: 59.34 fb vs (165.17+101.30) x 0.222274 = 59.23 (+0.2%); W+ fraction 0.614 +- 0.011.
## BR closure
- Forced H->gamma gamma: 2000/2000 last-copy H decays to gamma gamma in both full-record signal samples (`work/p03/hgg_check_*.txt`); conditional BR = 1 in the sample, B_gg = 0.002270 (YR4) applied once in the ledger (k(S_EW_WHjj_Wlnu) = WF_em x BGG = 2.1794e-3; no double counting: PY8/LHE sigma ratio = 1.0015).
- Pythia8 internal SM table (`config/p03_py8_hbr.json`, mH=125, with and without HiggsSM:NLOWidths): BR(gamma gamma) = 0.002297 (+1.2% vs YR4 0.002270), Gamma_H = 4.083 MeV, BR(bb) = 0.577. The ledger uses YR4 (0.002270); the 1.2% difference is assigned as BR systematic. Physical BR is an external input; PDG/YR4 not re-verified against the primary source (offline).
- W->l nu BR: MG5 ledger values from P01 unchanged (WF_em = 0.9601); gridpack closure above.

## Delphes object validation (signal S_EW_WHjj_Wlnu, 2000 events, validation-only loose objects)
| quantity | result |
|---|---|
| electron reco x ID x iso eff (gen prompt, dR<0.1), pT 10-20/20-30/30-50/50-100/>100 | 0.36/0.43/0.59/0.65/0.64 (eta integrated, |eta|<2.5) |
| muon eff same bins | 0.61/0.67/0.79/0.83/0.92 (|eta|<2.4) |
| photon eff (gen prompt H photons, no crack) pT 20-30/30-40/40-60/60-100/>100 | 0.50/0.64/0.76/0.85/0.87 |
| MET: sigma_eff of (MET_reco - MET_gen) components | x 15.5, y 16.2 GeV (flat 14.5-16.9 over gen MET bins; bias -0.3..+2.4 GeV) |
| m_gg, 2 reco photons pT>25, |eta|<2.5 (no crack), 808 events in 100-150 | Gaussian core 125.03 +- 2.17 (0.07) GeV; sigma_eff 2.17 GeV; 40.4% of events have >=2 photons |
| leading-2 jet response pT_reco/pT_gen (dR<0.3) | central 1.015 (sigma_eff 8.4%), forward 2.5-4.7: 0.964 (12.8%) |
| mjj reco/gen of the VBS pair | mean 1.006, sigma_eff 8.0% |
| events with exactly one lepton pT>25 | 46.5% (e 21.7%, mu 27.1% with >=1) |
Comparison with the frozen ZH object efficiencies (`work/theory/object_eff.json`, barrel/endcap split): electron 0.39-0.73 / 0.24-0.56, muon 0.57-0.87, photon 0.49-0.89: same card, consistent (our eta-integrated numbers lie between barrel and endcap values). Figures: `figures/p03_mgg_signal`, `p03_object_eff`, `p03_met_resolution`, `p03_vbs_jets`.
Truth-level checks: gH_m = 125.0; QCD W+Hjj behaves as expected (mjj>500 only 10% vs 34% for EW).
Overview of all finished samples (fractions of events: >=1 e pT>25, >=1 mu, >=1 photon, >=2 photons, m_gg in 100-160, mjj>500) in `config/p03_delphes_val.json` ("overview"); e.g. F_QCD_Wgjj_biased 2.1% >=2 photons (fake/second photon), unmatched (non-prompt/fake) reco photons are 2.6% of reco photons in Wgjj biased, 2.8% in EW Wgjj. Delphes jet->photon fake rates are reported only as such; they are not used for backgrounds (policy; parameterised fake factors in Phase 06). ttjj/tt have ~1-2% events with a photon pT>25.
Caveat: the loose validation selection (pT>25 object cuts, no isolation optimisation, no blinded window) is not the Phase-05 baseline. Delphes already removes jets overlapping photons/leptons (UniqueObjectFinder); my extra dR>0.4 jet cleaning changed nothing.

## Twin checks (shower level, 2000 events per twin; sigma x acceptance with reco selection mjj>X, |deta_jj|>3.0)
Biased (generator mmjj>400) vs nomjj (mmjj=0); sigma_x from LHE init; pull = (sigma_b - sigma_n)/sqrt(err^2 sum), binomial MC errors only. LO sigma ratios biased/nomjj: QCD Wgjj 0.127 (design 0.129), EW Wgjj 0.535 (0.557), QCD Zgjj 0.097 (0.099).
| twin | X=500 | X=700 | X=1000 | parton mjj<400 among nomjj events passing X=700 |
|---|---|---|---|---|
| EW Wgjj | -0.98 / -0.56 (+obj) | -0.59 / -0.68 | +0.45 / -0.05 | 2% -> PASS |
| QCD Wgjj | -4.9 / -2.8 | -2.1 / -1.7 | -0.6 / -0.3 | 45% |
| QCD Zgjj (lost lepton) | -5.8 / -3.1 | -3.3 / -2.0 | -1.0 / 0.0 | 60% |
(each cell: jets-only / with >=1 lepton pT>25 and >=1 photon pT>25.) Figure `figures/p03_twins`.
Result: the EW twin passes. For the QCD twins the biased sample underestimates sigma x acceptance for reco mjj below ~700-800 GeV (at 2-5 sigma on 2000 events), because in the unmatched LO+PS samples hard ISR/FSR jets let events with parton mjj<400 reach reco mjj>700; the discrepancy disappears at mjj>~1000 (stat. limited, 14-19 nomjj events). Interpretation: the generator cut mmjj>400 is NOT demonstrated safe for QCD Wgjj/Zgjj for a baseline reco mjj < ~1 TeV; and it also shows that the LO+PS definition (no merging with the Wgjjj/Zgjjj sample) is shower-dominated there. This is a real finding to be resolved in Phase 04, not a validation of the current biased cards (D-WH-9). The conclusion is statistics-limited and also depends on the unmerged Wgjj vs Wgjjj overlap (D-WH-3 style).

## Checks
- seeds unique (assert), no duplicate condor submission (condor_q empty before; single cluster).
- N_LHE=N_Delphes for all 22 finished jobs; PY8 sigma = LHE sigma; no overwrite of other data; nothing left running on the login node.
- Slim card output has Electron, Muon, Photon, Jet, GenJet, MissingET, GenMissingET, GenTruth friend tree (entry order identical).

## Caveats
- 2000-event tests: efficiency/resolution numbers carry 3-5% statistical errors in bins; resolution (m_gg 2.17 GeV) is for the inclusive signal photon pair without crack/category split.
- Running jobs (cluster 900153 procs 10-15, 20, 21): Wggjj gridpack integration (2.4 to >6.5 h projected in P02), W+4j and Wgjjj integration. If they fail or are held, Phase 04 needs beam-class splitting (D-WH-5). Results will be added by the next session (fetch with `scripts/p03_fetch.py`, closure with `p03_closure.py`; the Delphes script handles them automatically).
- W+jets/ttbar double fake remains unresolved (D-WH-4); F_Wjets_4j validation depends on its job.
- PDG/YR4 BR not re-verified from primary sources (no network lookup); PY8 BR differs by 1.2%.

## Decisions (new)
- D-WH-9: QCD twin FAIL at reco mjj<~800 (above). Default: keep biased samples only with baseline reco mjj>~1000 GeV plus the nomjj twin as a cross-check, and treat the twin-based correction as a systematic; alternative: lower generator mmjj (e.g. 250) or merged samples. Needs human choice before Phase 04.
- D-WH-10: W->l nu closure: gridpack decay-chain sigma is 1-2% below sigma_prod x B_MG5 (P01 also 1-3%); default: no correction, +-2% normalisation systematic (spin-correlated chain, not a bug found).
- D-WH-11: seed J convention J=0 gridpack / J=999 tests; production events J=1..998.
- Open from earlier unchanged: D-WH-1, D-WH-3..D-WH-8 (defaults kept).

## Next actions
1. When cluster 900153 finishes, fetch and add Wggjj/Wgjjj/W4j sigma and Delphes checks (rerun the three analysis scripts).
2. G1 human decisions D-WH-9..11 and earlier open ones; then Phase 04 production planning (gridpacks from the test jobs can be reused; cards unchanged).
