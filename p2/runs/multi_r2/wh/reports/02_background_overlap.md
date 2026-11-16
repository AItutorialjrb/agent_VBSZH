# WH Phase 02 — background and overlap ledger (multi_r2, executor-wh)

Date UTC: 2026-11-09. **Status: PASS with open numbered decisions D-WH-3..D-WH-8 (non-blocking for Phase 03 smoke tests; D-WH-4 and D-WH-5 block Phase 04 production).** Git commit: none (orchestrator commits). All sigma values here are LO MG5 validation numbers (short runs, 500 events, req_acc 0.05, 4 cores on a shared login node), not yields. Earlier decisions: D-WH-1 stays at its default (keep dynamical scale 3, document). **D-WH-2 resolved: separate W->tau nu feed-down samples** (S_EW_WHjj_Wtau, H_QCD_WHjj_Wtau), reported separately from S, never added silently.

## Goal
Background/overlap ledger for pp -> W±Hjj(EW), H->gg, W->e/mu nu (+tau feed-down): one row per sample with definition, validated MG5 syntax, BR ledger entry (BR once), N_MC plan against max(50k, sigma*BR*3000 fb^-1), seed index, overlap rule, and generator-cut safety (twin design). Frozen ZH samples reused only where coverage is demonstrated.

## Inputs, versions, seeds
Stack as Phase 01 (LCG_110, MG5 3.6.3 upstream, model sm-no_b_mass, NNPDF31_nnlo_as_0118, 13.6 TeV, dynamical_scale_choice 3). Seeds: SPEC_G0 3.4, P=2, R=2: seed = 2 200 000 + 1000*idx + J. Index map in `config/sample_registry.json` (1-29 and 60-61 production-intent, 30-58 interactive validation `VAL02_*`, 80-99 Phase 01 validation); uniqueness asserted in `scripts/seeds.py` (an earlier batch with duplicate seed indices aborted at start and was moved to `work/p02/aborted_badseed_start`, never used). Frozen ZH inputs read-only: `production/final/*` GenTruth ntuples + json, `cards/production_final|production_v2|coupling`, `reports/ZH_self_review.md`, `reports/FINAL_report.md`.

## Commands and paths
`scripts/make_cards_p02.py` (cards `cards/phase02/{prod,parse,val}/<name>.mg5`, table `config/phase02_cards.json`); `scripts/run_parse_p02.sh <name>` (logs `work/p02/parse/`, summary `parse_summary.txt`); `scripts/run_val_p02.sh <name> [timeout]` (-> `mg5_run_p02.sh`, outputs `work/p02/val/<name>/`); `scripts/br_ledger.py` -> `config/br_ledger.json`; `scripts/p02_numbers.py`; `scripts/build_ledger02.py` -> `config/phase02_ledger.json` (the sample registry with sigma, k, N_req, seeds); `scripts/zh_lostlepton_coverage.py` -> `work/p02/zh_coverage.json`; `scripts/fake_bounds.py`, `scripts/aajj_bound.py`. No condor submission, no bulk generation.

## 1. Sample ledger (definition, process, cuts: `config/phase02_ledger.json`; cards: `cards/phase02/prod/`)
Class / role / overlap rule:
- **Resonant (peak in m_gg, fitted with signal shape)**: S_EW_WHjj_Wlnu (signal), S_EW_WHjj_Wtau (feed-down), H_QCD_WHjj_Wlnu/Wtau (QCD W±Hjj, def. a background), I_EW_QCD_WHjj (signed), H_ttH_1l (semilep + dilep), H_tHq_1l, H_tHW_1l, H_QCD_ZHjj_ll and H_QCD_ZHjj_tautau (Z->ll lost lepton / Z->tautau->l), H_VBF_Hjj (only as shape/bound for fake-lepton), ZH EW and ggZH from frozen ZH (section 3).
- **Prompt continuum**: B_EW/QCD_Wggjj (W gamma gamma jj, ISR photons in ME) plus B_EW/QCD_WggjjFSR (one ME photon + W -> l nu gamma in the decay chain).
- **One fake photon**: F_QCD/EW_Wgjj (2j), F_QCD_Wgjjj (3j topology), F_QCD_Zgjj_ll (Z gamma jj, lost lepton).
- **Two fake photons**: F_Wjets_4j, T_tt_1l, T_ttjj_1l (bound/decision D-WH-4).
- **Top with prompt photons**: T_tta_1l, T_ttaa_1l, T_tWa_1l (DR via `$$ t~`/`$$ t`).
- **Non-prompt lepton**: Q_aajj_nplep (bound).
Jets/matching: fixed-order 2j (3j for F_QCD_Wgjjj, 4j for W+4j, ttjj) + PY8 shower, no MLM merging in Phase 02 (as the ZH final choice); resonant top and V samples are 0j + PS.

### Parse audits (executed, `work/p02/parse/*.log`, all rc=0; `Total: N processes with M diagrams`)
```
B_EW_Wggjj_biased | 2 processes with 38310 diagrams | 136 | rc=0
B_EW_WggjjFSR_biased | 2 processes with 5052 diagrams | 136 | rc=0
B_EW_Wggjj_nomjj | 2 processes with 38310 diagrams | 136 | rc=0
B_QCD_Wggjj_biased | 2 processes with 15350 diagrams | 204 | rc=0
B_QCD_WggjjFSR_biased | 2 processes with 2252 diagrams | 204 | rc=0
B_QCD_Wggjj_nomjj | 2 processes with 15350 diagrams | 204 | rc=0
F_EW_Wgjj_biased | 2 processes with 5046 diagrams | 136 | rc=0
F_EW_Wgjj_nomjj | 2 processes with 5046 diagrams | 136 | rc=0
F_QCD_Wgjj_biased | 2 processes with 2246 diagrams | 204 | rc=0
F_QCD_Wgjjj | 2 processes with 23286 diagrams | 348 | rc=0
F_QCD_Wgjj_nomjj | 2 processes with 2246 diagrams | 204 | rc=0
F_QCD_Zgjj_ll_biased | 1 processes with 2402 diagrams | 155 | rc=0
F_QCD_Zgjj_ll_nomjj | 1 processes with 2402 diagrams | 155 | rc=0
F_Wjets_4j | 2 processes with 396666 diagrams | 1512 | rc=0
H_QCD_WHjj_Wtau | 2 processes with 402 diagrams | 204 | rc=0
H_QCD_ZHjj_ll | 1 processes with 522 diagrams | 155 | rc=0
H_tHq_1l | 2 processes with 24 diagrams | 8 | rc=0
H_tHW_1l | 4 processes with 44 diagrams | 4 | rc=0
H_ttH_1l | 3 processes with 76 diagrams | 15 | rc=0
Q_aajj_nplep | 95 processes with 2400 diagrams | 155 | rc=0
S_EW_WHjj_Wtau | 2 processes with 1794 diagrams | 180 | rc=0
T_tt_1l | 2 processes with 30 diagrams | 10 | rc=0
T_tta_1l | 3 processes with 106 diagrams | 15 | rc=0
T_ttaa_1l | 3 processes with 412 diagrams | 15 | rc=0
T_tWa_1l | 4 processes with 56 diagrams | 4 | rc=0
```
Notes: off-diagonal W->l nu flavour combinations (e vm, ...) are rejected by MG5 (`w+ > lt+ vlt` yields e ve, mu vm, ta vt only, `lt=e,mu,ta`); decay chain with extra photon `w+ > lt+ vlt a` parses (2252 diagrams QCD, 5052 EW, both charges); `QCD=n QED=m` orders are upper bounds in chains (squared-order `==` forbidden in chains, as P01). 4F (no b) is used for EW Wgg jj, Wg jj and VBF-H as in ZH (b-initiated EW contributions need b-veto anyway; documented systematic). tHq (`p p > t h j $$ w+ w-`) 12 diagrams per charge, tHW (`p p > t w- h $$ t~`) 11 per process.

### Cross sections, BR ledger entry, N plan (BR applied once; k = product of listed factors; k in `config/br_ledger.json`)
BR factors: WF_em 0.9601 (P01), WF_emt (W->e,mu,tau chain) 0.98161, WF_tau 1.0247, WF_had 1.0109, WF_semilep 0.99233 (WF_emt*WF_had; dilepton component would be 0.96356, difference -2.9% treated as systematic on tt-type samples), ZF 0.9783 (e,mu), ZF_TAU 0.98196, BGG 0.00227; the PDG-like W/Z BRs carry the same unverified-against-RPP caveat as P01. Samples with H carry BGG exactly once (PY8 forces H->gg, conditional BR 1, no BR folded by PY8, shown in P01). Tau leptonic BR is PY8's and not folded. H_ttH/T_tt* use W3F/Whad on the whole sample (semilep + dilep components mixed).
Validation runs only; "ESTIMATE" rows are NOT measurements: the run timed out at 2400 s (survey progress at timeout: QCD Wggjj 380/1713 survey jobs after 32 min, EW Wggjj 237/3254 after 28 min, EW FSR 405/2619 after 37 min => projected 2.4 h, >6.5 h, ~4 h integration on 4 shared cores) and sigma is the frozen ZH Zgg sigma times the measured W/Z ratio of Vgamma jj (sigma_W/sigma_Z = 17.2 nomjj, 22.3 biased); FSR rows scaled by an assumed 0.3, EW nomjj by an assumed 1.8 (to be replaced by Phase 03 gridpack measurement). F_Wjets_4j: no sigma (396 666 diagrams, survey not finished; lite variant F_Wjets_4j_lite also did not finish within its timeout). T_ttjj_1l sigma is the MG5 integration estimate (event unweighting hit my own 1500 s timeout).
N_plan = min(N_req, 1e6) where 1e6 ~ largest per-sample ZH production (T_tta 1.04M); N_req = max(50k, sigma*k*3000).

| sample (idx) | sigma_MG5 [fb] | source | k | sigma*k*3000 | N_req | N_plan | shortfall | seed (J=0) |
|---|---|---|---|---|---|---|---|---|
| B_EW_WggjjFSR_biased (14) | 0.2617 +- n/a | ESTIMATE (run timed out at 2400 s) | 0.9816 | 770.5 | 5e+04 | 5e+04 | no | 2214000 |
| B_EW_Wggjj_biased (10) | 0.8722 +- n/a | ESTIMATE (run timed out at 2400 s) | 0.9816 | 2568 | 5e+04 | 5e+04 | no | 2210000 |
| B_EW_Wggjj_nomjj (11) | 1.57 +- n/a | ESTIMATE (run timed out at 2400 s) | 0.9816 | 4623 | 5e+04 | 5e+04 | no | 2211000 |
| B_QCD_WggjjFSR_biased (15) | 0.2376 +- n/a | ESTIMATE (run timed out at 2400 s) | 0.9816 | 699.7 | 5e+04 | 5e+04 | no | 2215000 |
| B_QCD_Wggjj_biased (12) | 0.792 +- n/a | ESTIMATE (run timed out at 2400 s) | 0.9816 | 2332 | 5e+04 | 5e+04 | no | 2212000 |
| B_QCD_Wggjj_nomjj (13) | 4.687 +- n/a | ESTIMATE (run timed out at 2400 s) | 0.9816 | 1.38e+04 | 5e+04 | 5e+04 | no | 2213000 |
| F_EW_Wgjj_biased (18) | 134.4 +- 0.43 | short LO run (validation, 500 ev) | 0.9816 | 3.958e+05 | 3.96e+05 | 3.96e+05 | no | 2218000 |
| F_EW_Wgjj_nomjj (19) | 241.2 +- 1.6 | short LO run (validation, 500 ev) | 0.9816 | 7.103e+05 | 7.1e+05 | 7.1e+05 | no | 2219000 |
| F_QCD_Wgjj_biased (16) | 1084 +- 2.9 | short LO run (validation, 500 ev) | 0.9816 | 3.192e+06 | 3.19e+06 | 1e+06 | YES | 2216000 |
| F_QCD_Wgjj_nomjj (17) | 8428 +- 43 | short LO run (validation, 500 ev) | 0.9816 | 2.482e+07 | 2.48e+07 | 1e+06 | YES | 2217000 |
| F_QCD_Wgjjj (20) | 2819 +- 11 | short LO run (validation, 500 ev) | 0.9816 | 8.301e+06 | 8.3e+06 | 1e+06 | YES | 2220000 |
| F_QCD_Zgjj_ll_biased (27) | 48.67 +- 0.23 | short LO run (validation, 500 ev) | 0.9783 | 1.428e+05 | 1.43e+05 | 1.43e+05 | no | 2227000 |
| F_QCD_Zgjj_ll_nomjj (28) | 490.5 +- 3.6 | short LO run (validation, 500 ev) | 0.9783 | 1.44e+06 | 1.44e+06 | 1e+06 | YES | 2228000 |
| F_Wjets_4j (21) | n/a +- n/a | NOT AVAILABLE (run timed out / not run) | 0.9816 | n/a | n/a | n/a | no | None |
| H_QCD_WHjj_Wtau (5) | 29.21 +- 0.25 | short LO run (validation, 500 ev) | 0.002326 | 203.8 | 5e+04 | 5e+04 | no | 2205000 |
| H_QCD_ZHjj_ll (9) | 10.24 +- 0.079 | short LO run (validation, 500 ev) | 0.002221 | 68.22 | 5e+04 | 5e+04 | no | 2209000 |
| H_QCD_ZHjj_tautau (61) | 5.074 +- 0.038 | short LO run (validation, 500 ev) | 0.002229 | 33.93 | 5e+04 | 5e+04 | no | 2261000 |
| H_VBF_Hjj (29) | 4099 +- 36 | short LO run (validation, 500 ev) | 0.00227 | 2.791e+04 | 5e+04 | 5e+04 | no | 2229000 |
| H_tHW_1l (8) | 7.045 +- 0.037 | short LO run (validation, 500 ev) | 0.002253 | 47.61 | 5e+04 | 5e+04 | no | 2208000 |
| H_tHq_1l (7) | 20.46 +- 0.23 | short LO run (validation, 500 ev) | 0.002228 | 136.8 | 5e+04 | 5e+04 | no | 2207000 |
| H_ttH_1l (6) | 202.9 +- 0.67 | short LO run (validation, 500 ev) | 0.002253 | 1371 | 5e+04 | 5e+04 | no | 2206000 |
| Q_aajj_nplep (26) | 283.6 +- 1.3 | short LO run (validation, 500 ev) | 1 | 8.508e+05 | 8.51e+05 | 8.51e+05 | no | 2226000 |
| S_EW_WHjj_Wtau (4) | 13.65 +- 0.27 | short LO run (validation, 500 ev) | 0.002326 | 95.25 | 5e+04 | 5e+04 | no | 2204000 |
| T_tWa_1l (24) | 117.5 +- 0.63 | short LO run (validation, 500 ev) | 0.9923 | 3.498e+05 | 3.5e+05 | 3.5e+05 | no | 2224000 |
| T_tt_1l (25) | 2.13e+05 +- 9.8e+02 | short LO run (validation, 500 ev) | 0.9923 | 6.341e+08 | 6.34e+08 | 1e+06 | YES | 2225000 |
| T_tta_1l (22) | 960.4 +- 4.4 | short LO run (validation, 500 ev) | 0.9923 | 2.859e+06 | 2.86e+06 | 1e+06 | YES | 2222000 |
| T_ttaa_1l (23) | 1.079 +- 0.0059 | short LO run (validation, 500 ev) | 0.9923 | 3212 | 5e+04 | 5e+04 | no | 2223000 |
| T_ttjj_1l (60) | 9.044e+04 +- 3.8e+02 | MG5 'Current estimate of cross-section' (integration finished, event unweighting/combine hit my 1500 s timeout); no LHE | 0.9923 | 2.693e+08 | 2.69e+08 | 1e+06 | YES | 2260000 |


## 2. Generator-level cut safety and twin design
Generation box (reco selection of Phase 05 must stay inside it, asserted in code): photons pT>25, |eta|<2.5, DeltaR(a,a)>0.4, DeltaR(a,j)>0.4, DeltaR(a,l)>0.4 (ME level only), m_gg in [100,170] for Wgg/Qagg, jets pT>20 (25 for 3j/4j/ttjj), |eta_j|<5, DeltaR(jj)>0.4, no lepton cuts (cut_decays False) except the FSR samples (cut_decays True: pT_l>10, |eta_l|<2.5, DeltaR(a,l)>0.4). Reco constraints implied: pT_gamma/m_gg thresholds with m_gg>=105 give pT>=26; mjj_reco >= 500 vs generator mmjj>400.
**Twin pairs** (biased = mmjj>400, twin = mmjj 0; correction C = Y_twin/Y_biased measured at Delphes level after the full selection, uncertainty propagated, accepted as auxiliary ratio samples as in ZH D-flag): (B_QCD_Wggjj_biased, _nomjj), (B_EW_Wggjj_biased, _nomjj), (F_QCD_Wgjj_biased, _nomjj), (F_EW_Wgjj_biased, _nomjj), (F_QCD_Zgjj_ll_biased, _nomjj); frozen pair (B_QCD_zaajj_vbs, B_QCD_zaajj_nomjj) is reused as is. ZH prior evidence (not re-derived): P(parton mjj<400 | reco mjj>500, |deta|>3.5) = 1.4% (EW ZHjj) but 64% (QCD ZHjj, tag jets from the shower) -> QCD-type samples cannot be used biased without C; H_QCD_ZHjj_*, F_QCD_Wgjjj and F_Wjets_4j therefore carry no mmjj cut (a ME-level all-pair mmjj cut would also remove the fake-photon jet pair). A second twin type is planned for Phase 03/04: pta 25 vs 20 and mmaa 100-170 vs 90-190 on B_QCD_Wggjj (stability of the stitched sum).
Executed (interactive, LO, `work/p02/p02_numbers.md`): sigma(biased)/sigma(no cut): QCD Wgjj 0.1286 +- 0.0007, EW Wgjj 0.5572 +- 0.0042, QCD Zgjj (lost lepton) 0.0992 +- 0.0009; frozen ZH QCD Zgg 0.130 (0.03556/0.2728 fb). The QCD biased samples retain only ~10-13% of the inclusive LO cross section, so the shower-level safety (C) is not a negligible correction. Wgg twins: sigma ratio unavailable (timeouts). Shower+Delphes twin comparison is Phase 03/04 work (not done here).

## 3. Lost-lepton backgrounds from frozen ZH samples: coverage demonstration
Frozen cards audited: `K_EW_ZHjj_lam_p000` (HC model, SM point, `z x0 j j QCD=0, z > l+ l-`, cut_decays False, mmjj>400, ptj 20), `B_EW_zaajj_vbs_is*`, `B_QCD_zaajj_vbs/nomjj` (Z in decay chain, cut_decays default False so the ptl/etal/mmll lines in the run card act on no lepton; Zgg: pta>25, mmaa 100-170, mmjj>400 or 0), `H_ggZH_py8dec` (Z decayed in PY8, no lepton cuts). Not reusable: `F_*_llajj` (leptons in the ME with ptl>10, |eta|<2.5, mmll>50: the lost-lepton region is cut away). Not reusable for QCD ZHjj: no frozen QCD ZHjj sample was produced (card only) -> new samples H_QCD_ZHjj_ll/_tautau; sigma(H_QCD_ZHjj_ll) = 10.24 +- 0.08 fb reproduces the ZH 10.25 fb (closure).
Evidence (`scripts/zh_lostlepton_coverage.py`, generator-level e/mu pT>5 stored in the frozen GenTruth; T1 = exactly one prompt lepton pT>25,|eta|<2.5 and no second prompt lepton pT>10,|eta|<2.5):
| frozen ZH sample | N_gen | sigma_gen [fb] | k | N(T1) raw | f_T1 | f_T1 && nph>=2 | 2nd lepton lost via eta>2.5 / pT 5-10 / absent (of T1) | N_T1 x sigma k L(500), pre-photon-window |
|---|---|---|---|---|---|---|---|---|
| K_EW_ZHjj_lam_p000 | 50000 | 0.5624 | 0.002221 | 6194 | 0.1239 | 0.0949 | 4295 / 1393 / 522 | 0.0774 |
| B_EW_zaajj_vbs_is1h | 20000 | 0.01663 | 0.9783 | 2605 | 0.1303 | 0.1144 | 1635 / 716 / 264 | 1.06 |
| B_EW_zaajj_vbs_is2 | 20000 | 0.01576 | 0.9783 | 2710 | 0.1355 | 0.1184 | 1670 / 751 / 296 | 1.04 |
| B_EW_zaajj_vbs_is3 | 20000 | 0.00677 | 0.9783 | 2634 | 0.1317 | 0.1158 | 1602 / 751 / 285 | 0.436 |
| B_QCD_zaajj_vbs | 100000 | 0.03556 | 0.9783 | 16541 | 0.1654 | 0.1253 | 11225 / 3932 / 1430 | 2.88 |
| B_QCD_zaajj_nomjj | 100000 | 0.2728 | 0.9783 | 17215 | 0.1721 | 0.1347 | 12121 / 3830 / 1339 | 23 |
| H_ggZH_py8dec | 20000 | 75 | 0.0001527 | 2672 | 0.1336 | 0.0972 | 1529 / 870 / 282 | 0.765 |
| H_ZH_tautau | 5248 | 24.87 | 0.00227 | 790 | 0.1505 | 0.0958 | 17 / 81 / 692 | 4.25 |

WH reference (pre-cut): sigma(S_EW_WHjj, W->e/mu in ME) x k x L = 28.10 x 2.179e-3 x 500 = 30.6 events

Coverage holds: ~13-17% of events fall in T1 with the second lepton at |eta|>2.5 (about 2/3 of T1), pT 5-10 (about 1/4) or absent; all samples contain leptons at |eta|>2.5 and pT<10, i.e. no generator lepton cut. Limits: (i) mmjj>400 in the EW ZH sample (safe for reco mjj>500 per ZH 1.4% study); (ii) the Zgg QCD biased sample needs the twin C, nomjj frozen twin has N(T1)=17215 raw; (iii) lepton |eta| and pT recorded only for pT>5; MET from the lost lepton is a Delphes-level quantity, to be validated in Phase 03; (iv) frozen Z->ee/mumu only (the Z->tautau->l topology comes from H_ZH_tautau (MLM, 5248 events < 50k: reuse only as a cross-check, flagged D-WH-7) and the new H_QCD_ZHjj_tautau). Indicative pre-photon-window sizes at 500 fb^-1 (table last column) vs 30.6 signal events before cuts: EW ZHjj lost lepton 0.08, QCD Zgg nomjj 23 (no photon-window/VBS/MET cuts yet), so the Zgg QCD lost-lepton component is not negligible a priori and stays in the ledger; the ggZH, EW ZH components are small but retained with MC support (stats 20k-50k).

## 4. Reducible and bounded components
Fake model (scenarios as ZH, NOT data-driven): f_j->gamma = 1e-3 (pT/50)^-0.5 (x2 |eta|>1.44) x {0.3,1,3}, double fakes scale as f^2; f_l(non-prompt, event level) in {3e-5,1e-4,1e-3}; fake photon pT = x pT_jet, x~N(0.85,0.10). Delphes jet->photon fakes recorded but not trusted.
- **Wgamma+jets (one fake)**: F_QCD_Wgjj / F_EW_Wgjj (2j + PS) are the ZH-style direct samples but in a 2j ME the jet faking the photon removes one VBS tag; the correct topology needs 3 ME jets, hence F_QCD_Wgjjj (sigma 2819 fb, 23 286 diagrams, 2132 s interactive) as the proposed primary with the 2j ones as cross-check (D-WH-3).
- **W+jets double fake**: quantitative bound NOT achieved. F_Wjets_4j (W+4j, 396 666 diagrams) could not be integrated interactively; the lite attempt (u,d,g only, nhel 1) did not finish. Ceiling statement using the T_ttjj sigma and no kinematic efficiency: N <= sigma*k*L*f^2*(6 pair choices)*P(m_gg window ~0.2)*eps_tags(<=0.5) = 9.04e4*0.992*500*1e-6*6*0.2*0.5 = ~27 events (nominal f; x0.09 low, x9 high) for ttbar+2 ME jets, i.e. NOT negligible against ~3 expected signal events after cuts: it must be settled by MC (D-WH-4). For W+4j the corresponding ceiling is of the same order or larger (sigma(W+4j) not measured).
- **tt-bar single lepton with two fakes**: T_tt_1l LHE proxy (parton-level, `scripts/fake_bounds.py`): 0 of 500 events have support (decay products cannot form VBS tags): this is a MISSING-SUPPORT zero, not a bound; the 95% CL ceiling with no efficiency assumption is 0.63 events at nominal f. N_req(T_tt_1l) = 6.3e8 (infeasible). Replaced by T_ttjj_1l (tags are ME jets, sigma 9.04e4 fb, N_req 2.7e8 shortfall) -> D-WH-4.
- **QCD gamma gamma jj + non-prompt lepton**: sigma(VBS-biased, 100<m_gg<170) = 283.6 fb; LHE efficiency for m_gg 120-130 + pT/m_gg + VBS jets mjj>500 |deta|>3: 18/500 = 0.036; N(500 fb^-1) = sigma*eps*L*f_l*eps_MET with eps_MET=0.1 assumed: 0.015 / 0.05 / 0.51 events for f_l = 3e-5/1e-4/1e-3 (`work/p02/aajj_bound.json`). Bound, not yield; at the upper scenario it is ~15% of the expected post-cut signal, so it is retained as a flagged systematic (no MC sample beyond the ledger card; production only if Phase 05 finds eps_MET larger).
- **Other Higgs modes with fake lepton**: VBF H->gg (H_VBF_Hjj sigma 4099 fb, 4F, generator cuts only ptj 20; VBS-jet efficiency from LHE 220/500 = 0.44): N(500) = sigma*B_gg*eps*L*f_l*0.1 = 0.006 / 0.020 / 0.20 events (3e-5/1e-4/1e-3, `work/p02/vbfh_bound.json`). ggF H+jj: analytic ceiling sigma_ggF(13 TeV YR4 48.58 pb, ranking only)*B_gg = 110 fb, N = 5.5e4*f_l*eps_VBS(assumed <=0.01)*0.1 <= 0.055 events at f_l=1e-3 (assumption, no MC; 13.6 TeV values not archived). WH/ZH hadronic V with fake lepton are covered by the same f_l argument and are below VBF. Real-lepton Higgs modes: ttH, tHq, tHW (own samples), WH/ZH QCD (own samples).
- **Wgamma gamma + e->gamma, WZgamma, WWgamma**: not generated; WZ gamma (lost lepton) with an e->gamma fake would be bounded by the Zgg QCD component times (sigma ratio < 0.1) x f_e->gamma(2%); documented bound only, row `V_WZa/V_WWa` to be revisited in Phase 04 (no negligible claim: unquantified).

## 5. Hard/soft photon overlap removal (as in ZH, adapted for W)
1. Prompt photon (particle level after PY8): status-1 photon, no hadron in ancestry, pT>25 (= ME threshold; 15 for the top samples as in ZH), |eta|<2.5, DeltaR>0.4 to other prompt photons, prompt leptons (pT>10) and generator jets (anti-kT 0.4, pT>20); implemented by the frozen `slim_gentruth.py` (`n_prompt_photons`, threshold to be set to the WH ME cuts in Phase 03).
2. Partition by N_p gamma: W/Z+jets keep 0, Wgamma(+jets) exactly 1, Wgamma gamma >= 2, same for ttbar/ttgamma/ttgamma gamma. Photons below the ME threshold from the shower in the higher-multiplicity sample are retained (they fall into N>=2 anyway); migration quantified in Phase 04.
3. W-decay FSR: the decay-chain Wgg sample lacks W->l nu gamma photons; completed by B_*_WggjjFSR (W gamma jj with W->l nu gamma in the chain, cut_decays True, DeltaR(a,l)>0.4, pT_l>10). The decay width ratio Gamma(l nu gamma, cuts)/Gamma_W is built into the chain matrix element; WF_emt applied as for l nu. Overlap with PY8 QED FSR (collinear/soft photons below ME cuts) is removed by N_p gamma counting with DeltaR(gamma,l)>0.4 (so collinear PY8 FSR cannot become a prompt photon). ZH needed a factor 1.128 for the analogous Zgg FSR; for W it cannot be skipped because there is no mll window (D-WH-6).
4. EW vs QCD by coupling order (diagram counts above; interference carried as signed samples as in P01 for the signal; Wgg interference not computed: Phase 03 item).
5. Shower QED emission ON everywhere.

## 6. Checks
Parse audits 28/28 rc=0 (25 batch + 3 added cards); closure of H_QCD_ZHjj_ll vs frozen ZH (10.24 vs 10.25 fb); W/Z ratios consistent (17.2 nomjj, 22.3 biased: W includes e,mu,tau); BR ledger WF_em reproduces P01 0.96008; seed uniqueness asserted; frozen-ZH coverage T1 counts. Not done: N_eff-level shower twin checks, Wgg cross sections, W+4j, tt-bar jets bound, H->gg PY8 check for the new H samples (same cmnd as P01).

## 7. Decisions (numbered; defaults adopted unless noted)
- **D-WH-3 (N shortfall, fake-type QCD)**: N_req > 1e6 for F_QCD_Wgjj_biased (3.2e6), F_QCD_Wgjj_nomjj (2.5e7), F_QCD_Wgjjj (8.3e6), F_QCD_Zgjj_ll_nomjj (1.4e6), T_tta_1l (2.9e6). Default: ZH precedent (flag, N_plan 1e6 / 2e5-1e6 depending on cost, twin ratio C and fake weights as nuisances; effective-N >= 10 in the final region as the criterion, direct upper bound otherwise). Needs human OK before Phase 04.
- **D-WH-4 (double-fake W+jets and ttbar)**: N_req 6e8 (tt 0j), 2.7e8 (ttjj), unmeasurable for W+4j; ceiling ~27 events (nominal f) for ttjj, so not negligible. Options: (a) filtered/biased production (ME-level tags mjj>500, fake-source jets pT>30) with fake weights and effective-N criterion; (b) parametrised bound only. Default: (a) for T_ttjj_1l and F_Wjets_4j prepared as gridpack-split samples in Phase 03/04. BLOCKS Phase 04 sign-off.
- **D-WH-5 (Wgg integration cost)**: no Wgg sigma measured; projected survey 2.4 h (QCD) to >6.5 h (EW) on 4 shared cores; ZH precedent: beam-class split (is1-3) and nhel-1 variant on condor. Default: split by beam-1 parton class, gridpacks on condor in Phase 04; sigma and C measured there. Estimates in the table are provisional.
- **D-WH-6 (W-decay FSR photon)**: adopt B_*_WggjjFSR as part of the Wgg background (alternative: full off-shell l nu a a j j ME, too heavy). The sum rule Wgg_total = ISR-ISR + ISR-FSR carries a narrow-width approximation; systematic to be sized in Phase 03/04.
- **D-WH-7 (ZH lost lepton / tau)**: reuse frozen EW ZHjj, ggZH, Zgg (coverage shown); QCD ZHjj -> new samples (ee/mumu and tautau); frozen H_ZH_tautau only 5248 events (< 50k): cross-check only. Default adopted.
- **D-WH-8 (primary one-fake topology)**: use F_QCD_Wgjjj (3j) as primary and the ZH-style 2j samples as cross-check (default), or the reverse? Human choice (affects stats and twin design).
D-WH-1 default unchanged; D-WH-2 resolved (see top).

## Caveats
LO sigma from 500-event validation runs (errors are integrator errors); estimates flagged ESTIMATE; PDG W/Z BRs not re-verified against RPP; 13 TeV YR4 numbers used only for ranking; the fake models and bounds are scenarios, not data-driven; MG5 `req_acc` 0.05 on validation only.

## Next actions
Phase 03: gridpack + one condor test job per sample type (resolve D-WH-3..8 first), shower-level twin pairs, PY8 H->gg check on the new H samples, Delphes object validation, Wgg sigma/C measurement.
