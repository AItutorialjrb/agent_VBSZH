# WH Phase 01-03 reports, analysis E


<!-- ===== Phase report 01_signal_definition ===== -->

# WH Phase 01 — signal definition (RUN, analyst)

Date UTC: 2026-11-09 (work started 2026-11-08T20:3x Z). **Status: PASS** (two non-blocking decisions raised with defaults: D-WH-1, D-WH-2). Git commit: none (analyst commits). All numbers here are LO MG5 validation cross sections (labelled validation only, not yields).

## Goal
Define gauge-invariant EW pp -> W±Hjj at sqrt(s)=13.6 TeV, (QCD,QED)=(0,4) amplitude order, both charges; W->e nu / mu nu decayed in MG5 (BR ledger + W-width factor WF); H->gamma gamma forced in Pythia8, SM BR applied once; QCD W±Hjj as resonant background (def. a) and inclusive-signal variant (def. b); interference statement. Validate MG5 syntax by diagram/subprocess lists and short LO runs.

## Inputs, versions, seeds
- Stack: `p2/lib/scripts/setup_stack.sh` (LCG_110 x86_64-el9-gcc13-opt, MG5_aMC 3.6.3 upstream tag, Pythia 8.317, Delphes 3.5.1, PDF NNPDF31_nnlo_as_0118 / LHAID 303600), model `sm-no_b_mass` (5F, massless b, diagonal CKM), as ZH.
- Seeds: SPEC_G0 3.4 with P=2, R=x: `seed = 2x00000 + 1000*sample_index + J`; registry `config/sample_registry.json`, uniqueness asserted in `scripts/seeds.py` (validation samples use indices 80-99, never enter s or b). Seed per run in `work/p01/phase01_numbers.md`.
- Reused lib code: `lib/scripts/setup_stack.sh` (as is), `lib/scripts/mg5_smoke.sh` (patch 001), `lib/scripts/run_py8_delphes.sh` (002, hand transcription), `lib/cards/phase03_smoke/py8_common_CP5.cmnd` (as is), ZH card pattern `ew_zhjj_zll.mg5`. See `patches/README.md`.
- Run-card pins (as ZH): 6800+6800 GeV, lhaid 303600, maxjetflavor 5, asrwgtflavor 5, ptj 20, |eta_j|<5, drjj 0.4, `dynamical_scale_choice 3` (sum m_T/2), cut_decays False (no lepton cuts), use_syst True.

## Signal definition
Signal S = complete tree-level EW amplitude pp -> W± H j j at order (QCD,QED)=(0,4), summed coherently over all diagrams and all partonic channels (both charges), W on-shell decayed with spin correlations in the MG5 decay chain to e nu or mu nu, H undecayed in the LHE (decays in Pythia8). It contains VBF-like (W/Z exchange, VBS WW->WH-type), Higgsstrahlung-like (s-channel W*->WH with extra EW radiation/hadronic V->jj, i.e. WVH with V->qq) and crossed/identical-quark diagrams, with their same-order interference inside S. "VBS/VBF-like" is only a later fiducial region (m_jj, Delta eta_jj), not a diagram subset: diagram labels are not gauge invariant. Internal top lines appear through diagonal-CKM b-quark diagrams (b in the 5F proton/jets); 4F/heavy-Yukawa/CKM completeness is a documented later systematic (as ZH D2).
Not included: loop-induced contributions, off-shell l nu H j j (computed only as control), W->tau nu feed-down (D-WH-2), W->jj.

## MG5 syntax validation (executed parse audits, `work/p01/parse/*.log`, cards `cards/phase01/parse_*.mg5`)
| Card | Result | Subprocesses / diagrams |
|---|---|---|
| `p p > w+ h j j QCD=0 QED=4` | parses | 52 / 896; 0 gluon-containing subprocesses; 12 with b-quark legs |
| same, w- | parses | 52 / 896; 0 gluons |
| w+ and w- via add process | parses | 104 / 1792 |
| `...QCD==2 QED==2` (QCD W+Hjj) | parses | 60 / 200 (8 with gluons) ; W- same |
| `...QCD^2==2 QED^2==6` (cross term) | parses | 52 / 1032 |
| `...QCD<=2 QED<=4` (coherent total) | parses | 60 / 1096 = 896 + 200 (union, no extra sector) |
| decay chain `QED=4, w+ > l+ vl` (vl = ve vm) | parses | decays listed: `w+ > e+ ve`, `w+ > mu+ vm` only (flavour-off-diagonal combinations are rejected by MG5) |
| explicit two-chain variant | parses | same two decays |
| decay chain with `QED==4` | **fails**: "Decay processes cannot specify squared orders constraints" | as ZH: use `QED=4` (with QCD=0 equivalent to ==4 for 2->4 tree) |
| `w+ > ta+ vt` chain | parses | control only |
| off-shell `p p > l+ vl h j j QCD=0 QED=5` | parses | 104 / 2472 (control; not in signal) |
Conclusion: orders syntax `QCD=0 QED=4` for the production + `QED=4` (upper bound) in chains is validated; `==` only for undecayed processes.

## Cross sections (MG5 LO, fb, generator cuts above, 2000 unweighted events/run, MC error = MG5 integration error)
Full table with seeds: `work/p01/phase01_numbers.md` (produced by `scripts/phase01_numbers.py`).
| Process | sigma [fb] |
|---|---|
| EW W+Hjj (undecayed, 2 seeds averaged) | 83.18 +- 0.33 |
| EW W-Hjj | 46.04 +- 0.29 |
| EW W±Hjj total | 129.22 +- 0.44 |
| QCD W+Hjj (2,2) (2 seeds) / W-Hjj | 165.17 +- 0.63 / 101.30 +- 0.52 |
| EW x QCD cross term W+ / W- | -0.128 +- 0.008 / -0.124 +- 0.006 |
| coherent (QCD<=2,QED<=4) W+ vs EW+QCD+cross | 246.59 +- 0.97 vs 248.22 +- 0.71 (pull -1.35) -> closure PASS |
| EW W±Hjj with W->e nu/mu nu in ME (W+ 17.97, W- 10.13) | 28.10 +- 0.10 |

Interference statement: the signed EW-QCD cross term is -0.15% (W+) and -0.27% (W-) of sigma_EW under generation cuts (ZH: -0.6%); closure of the coherent sum holds within 1.4 sigma. Treat as signal-model systematic (and quote after selection in Phase 05/06); it is not a separate sample. Higgs-pole vs continuum l nu gamma gamma jj interference (loop-induced decay) is not computed here (forced PY8 decay cannot); to be carried as a Phase 06 mass-shape caveat, not transferred from the reference paper.
Definitions: (a) baseline: S = EW only; QCD W±Hjj (sigma ~ 1.9-2.2 x EW before VBS cuts) is a resonant background, separate sample (`H_QCD_WHjj`). (b) inclusive-signal variant: S+QCD+cross term (coherent sum = def. a sum within MC precision), reported as an alternative signal definition in sensitivity; selection power of the VBS region (Phase 05) decides the practical difference.

## BR and width ledger (BR applied exactly once)
- MG5 widths from `compute_widths w+ z` (cards/phase01/widths_w.mg5; work/p01/widths/pc_in.dat, a copy of restrict_no_b_mass.dat): Gamma(W->l nu) = 0.2x75641 GeV per flavour, Gamma_W(computed LO) = 2.04791 GeV, Gamma_W(param card used in decay chains) = 2.0476 GeV; BR_ll(Z) cross-check reproduces ZF denominators (Gamma_ee 83.965 MeV).
- B_MG5(W->e nu + mu nu) = 2 x 0.2x75641 / 2.0476 = 0.222274.
- Reference: B(W->e nu)=0.1071 +- 0.0016, B(W->mu nu)=0.1063 +- 0.0015 (sum 0.2134 +- 0.0022). Caveat: numbers confirmed by a web search against arXiv:2202.14015 (which quotes them), PDG attribution not independently verified; re-check against current RPP.
- **WF = 0.2134/0.222274 = 0.9601 +- 0.0099** (per flavour: e 0.9637, mu 0.9565). Applies only to samples with W->l nu decayed in the MG5 matrix element (analogue of ZF = 0.9783).
- H->gamma gamma: B_gg = 0.002270 (LHCHXSWG YR4, mH=125; as ZH), applied once in the analysis ledger; Pythia forces `25:onIfMatch = 22 22` with conditional BR = 1.
- Sample factor: **k(S_EW_WHjj_Wlnu) = WF x B_gg = 2.1794e-3** (factors listed: WF, BGG; asserted no duplicates in later ledger code). sigma x k = 28.10 x 2.179e-3 = 0.0612 fb. N_MC = max(50 000, 0.0612 fb x 3000 fb^-1 = 184) = 50 000 (sigma x BR x 3000 binds nowhere).
- Same k for QCD W±Hjj (decayed in ME). Cross section stage separation: sigma_prod (undecayed) -> sigma_dec = sigma_prod x B_MG5 -> x WF x B_gg (before cuts) -> after cuts (Phase 05); not mixed.

### W->l nu closure (executed)
sigma_dec/sigma_prod vs analytic 0.2223: W- dynamical scale 0.2200 +- 0.0019 (pull -1.2); W+ dynamical scale 0.2149 +- 0.0018 and 0.2174 +- 0.0022 (pulls -4.2, -2.3; ratios 0.967, 0.978); W+ **fixed mu = 125 GeV** 0.2199 +- 0.0019 (pull -1.3, ratio 0.989). Interpretation: with `dynamical_scale_choice 3` the decay-chain event scale is computed from the full final state including the lepton transverse masses, which differs from the undecayed (W on-shell) scale; with a fixed scale the closure holds within errors. The ~1-3% shift is a scale-definition effect inside the scale uncertainty, not a BR error. WF is applied to the decay-chain sigma itself, so no further correction is made; D-WH-1 asks whether to keep scale 3 or to fix the decayed-sample scale convention. (ZH showed no such shift: pull 1.0.)

## H -> gamma gamma route (executed)
`cards/phase01/py8_ew_whjj_haa.cmnd` (ZH settings) + CP5 common card, LHE of the W+ decayed validation sample, 300 events through DelphesPythia8 (`work/p01/py8check/`, seed 2x99000): 300/300 last-copy H decay to gamma gamma (`scripts/check_hgg_decay.py`); Pythia sigma_gen = 1.791e-11 mb = 17.91 fb = LHE sigma 17.91 fb (init block 1.791e-2 pb) -> Pythia does not fold any BR into the cross section for LHE input; SLHA DECAY tables ignored by Pythia. The loop-induced decay is not attempted in MG5.

## Checks / caveats
- Checks passed: syntax (11 cards), no external gluon at (0,4), 896+200=1096 union, coherent-sum closure, H->gamma gamma forcing, no hidden BR, seed uniqueness assert.
- Caveats: MG5 sigma errors are integrator errors from 2000-event runs (second seeds suggest ~1-2% fluctuations beyond quoted error in W+ decayed runs); LO only; 5F massless-b/diagonal CKM; no off-shell/pole comparison (planned Phase 03b as ZH); W->tau nu->l excluded (D-WH-2); lib file copies of `run_py8_delphes.sh` and `py8_ew_zhjj_haa.cmnd` were blocked by a permission deny rule, so those two were re-typed from earlier read output (documented in patches/README.md).
- Decisions: **D-WH-1** scale convention for decay-chain samples (default adopted: keep scale 3 as ZH; document closure at fixed scale; alternative: fixed/undecayed-W scale). **D-WH-2** W->tau nu (->e/mu nu nu, ~+19% of the e/mu signal-like events before cuts, softer leptons) is outside the specified signal; default: separate feed-down sample reported separately, decided in Phase 02.

## Commands
`scripts/run_parse.sh <card>`; `scripts/run_validation_batch.sh <sample...>` (calls `scripts/mg5_run_wh.sh <card> <seed> 3000`, scratch in session scratchpad, 3 parallel on a login node, tiny validation only); `scripts/run_py8_wh.sh work/p01/V_ew_wp_wlnu/unweighted_events.lhe.gz cards/phase01/py8_ew_whjj_haa.cmnd 300 2x99000 <out.root>`; `scripts/phase01_numbers.py`. No condor submission.

## Next actions
Phase 02: background/overlap ledger (Wgg, Wg+jets, W+jets fakes, ttg(g), tWg, ttH/tH, ZHjj/Zggjj lost lepton from frozen ZH samples, QCD gg+jets with non-prompt lepton, photon overlap removal, twin samples) incl. W->tau nu feed-down; then Phase 03 smoke/closure per sample type and one condor test job.


<!-- ===== Phase report 02_background_overlap ===== -->

# WH Phase 02 — background and overlap ledger (RUN, analyst)

Date UTC: 2026-11-09. **Status: PASS with open numbered decisions D-WH-3..D-WH-8 (non-blocking for Phase 03 smoke tests; D-WH-4 and D-WH-5 block Phase 04 production).** Git commit: none (analyst commits). All sigma values here are LO MG5 validation numbers (short runs, 500 events, req_acc 0.05, 4 cores on a shared login node), not yields. Earlier decisions: D-WH-1 stays at its default (keep dynamical scale 3, document). **D-WH-2 resolved: separate W->tau nu feed-down samples** (S_EW_WHjj_Wtau, H_QCD_WHjj_Wtau), reported separately from S, never added silently.

## Goal
Background/overlap ledger for pp -> W±Hjj(EW), H->gg, W->e/mu nu (+tau feed-down): one row per sample with definition, validated MG5 syntax, BR ledger entry (BR once), N_MC plan against max(50k, sigma*BR*3000 fb^-1), seed index, overlap rule, and generator-cut safety (twin design). Frozen ZH samples reused only where coverage is demonstrated.

## Inputs, versions, seeds
Stack as Phase 01 (LCG_110, MG5 3.6.3 upstream, model sm-no_b_mass, NNPDF31_nnlo_as_0118, 13.6 TeV, dynamical_scale_choice 3). Seeds: SPEC_G0 3.4, P=2, R=x: seed = 2x00000 + 1000*idx + J. Index map in `config/sample_registry.json` (1-29 and 60-61 production-intent, 30-58 interactive validation `VAL02_*`, 80-99 Phase 01 validation); uniqueness asserted in `scripts/seeds.py` (an earlier batch with duplicate seed indices aborted at start and was moved to `work/p02/aborted_badseed_start`, never used). Frozen ZH inputs read-only: `production/final/*` GenTruth ntuples + json, `cards/production_final|production_v2|coupling`, `reports/ZH_self_review.md`, `reports/FINAL_report.md`.

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
| B_EW_WggjjFSR_biased (14) | 0.2617 +- n/a | ESTIMATE (run timed out at 2400 s) | 0.9816 | 770.5 | 5e+04 | 5e+04 | no | 2x14000 |
| B_EW_Wggjj_biased (10) | 0.8722 +- n/a | ESTIMATE (run timed out at 2400 s) | 0.9816 | 2568 | 5e+04 | 5e+04 | no | 2x10000 |
| B_EW_Wggjj_nomjj (11) | 1.57 +- n/a | ESTIMATE (run timed out at 2400 s) | 0.9816 | 4623 | 5e+04 | 5e+04 | no | 2x11000 |
| B_QCD_WggjjFSR_biased (15) | 0.2376 +- n/a | ESTIMATE (run timed out at 2400 s) | 0.9816 | 699.7 | 5e+04 | 5e+04 | no | 2x15000 |
| B_QCD_Wggjj_biased (12) | 0.792 +- n/a | ESTIMATE (run timed out at 2400 s) | 0.9816 | 2332 | 5e+04 | 5e+04 | no | 2x12000 |
| B_QCD_Wggjj_nomjj (13) | 4.687 +- n/a | ESTIMATE (run timed out at 2400 s) | 0.9816 | 1.38e+04 | 5e+04 | 5e+04 | no | 2x13000 |
| F_EW_Wgjj_biased (18) | 134.4 +- 0.43 | short LO run (validation, 500 ev) | 0.9816 | 3.958e+05 | 3.96e+05 | 3.96e+05 | no | 2x18000 |
| F_EW_Wgjj_nomjj (19) | 241.2 +- 1.6 | short LO run (validation, 500 ev) | 0.9816 | 7.103e+05 | 7.1e+05 | 7.1e+05 | no | 2x19000 |
| F_QCD_Wgjj_biased (16) | 1084 +- 2.9 | short LO run (validation, 500 ev) | 0.9816 | 3.192e+06 | 3.19e+06 | 1e+06 | YES | 2x16000 |
| F_QCD_Wgjj_nomjj (17) | 8428 +- 43 | short LO run (validation, 500 ev) | 0.9816 | 2.482e+07 | 2.48e+07 | 1e+06 | YES | 2x17000 |
| F_QCD_Wgjjj (20) | 2819 +- 11 | short LO run (validation, 500 ev) | 0.9816 | 8.301e+06 | 8.3e+06 | 1e+06 | YES | 2x20000 |
| F_QCD_Zgjj_ll_biased (27) | 48.67 +- 0.23 | short LO run (validation, 500 ev) | 0.9783 | 1.428e+05 | 1.43e+05 | 1.43e+05 | no | 2x27000 |
| F_QCD_Zgjj_ll_nomjj (28) | 490.5 +- 3.6 | short LO run (validation, 500 ev) | 0.9783 | 1.44e+06 | 1.44e+06 | 1e+06 | YES | 2x28000 |
| F_Wjets_4j (21) | n/a +- n/a | NOT AVAILABLE (run timed out / not run) | 0.9816 | n/a | n/a | n/a | no | None |
| H_QCD_WHjj_Wtau (5) | 29.21 +- 0.25 | short LO run (validation, 500 ev) | 0.002326 | 203.8 | 5e+04 | 5e+04 | no | 2x05000 |
| H_QCD_ZHjj_ll (9) | 10.24 +- 0.079 | short LO run (validation, 500 ev) | 0.002221 | 68.22 | 5e+04 | 5e+04 | no | 2x09000 |
| H_QCD_ZHjj_tautau (61) | 5.074 +- 0.038 | short LO run (validation, 500 ev) | 0.002229 | 33.93 | 5e+04 | 5e+04 | no | 2x61000 |
| H_VBF_Hjj (29) | 4099 +- 36 | short LO run (validation, 500 ev) | 0.00227 | 2.791e+04 | 5e+04 | 5e+04 | no | 2x29000 |
| H_tHW_1l (8) | 7.045 +- 0.037 | short LO run (validation, 500 ev) | 0.002253 | 47.61 | 5e+04 | 5e+04 | no | 2x08000 |
| H_tHq_1l (7) | 20.46 +- 0.23 | short LO run (validation, 500 ev) | 0.002228 | 136.8 | 5e+04 | 5e+04 | no | 2x07000 |
| H_ttH_1l (6) | 202.9 +- 0.67 | short LO run (validation, 500 ev) | 0.002253 | 1371 | 5e+04 | 5e+04 | no | 2x06000 |
| Q_aajj_nplep (26) | 283.6 +- 1.3 | short LO run (validation, 500 ev) | 1 | 8.508e+05 | 8.51e+05 | 8.51e+05 | no | 2x26000 |
| S_EW_WHjj_Wtau (4) | 13.65 +- 0.27 | short LO run (validation, 500 ev) | 0.002326 | 95.25 | 5e+04 | 5e+04 | no | 2x04000 |
| T_tWa_1l (24) | 117.5 +- 0.63 | short LO run (validation, 500 ev) | 0.9923 | 3.498e+05 | 3.5e+05 | 3.5e+05 | no | 2x24000 |
| T_tt_1l (25) | 2.13e+05 +- 9.8e+02 | short LO run (validation, 500 ev) | 0.9923 | 6.341e+08 | 6.34e+08 | 1e+06 | YES | 2x25000 |
| T_tta_1l (22) | 960.4 +- 4.4 | short LO run (validation, 500 ev) | 0.9923 | 2.859e+06 | 2.86e+06 | 1e+06 | YES | 2x22000 |
| T_ttaa_1l (23) | 1.079 +- 0.0059 | short LO run (validation, 500 ev) | 0.9923 | 3212 | 5e+04 | 5e+04 | no | 2x23000 |
| T_ttjj_1l (60) | 9.044e+04 +- 3.8e+02 | MG5 'Current estimate of cross-section' (integration finished, event unweighting/combine hit my 1500 s timeout); no LHE | 0.9923 | 2.693e+08 | 2.69e+08 | 1e+06 | YES | 2x60000 |


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


<!-- ===== Phase report 03_generation_validation ===== -->

# WH Phase 03 - generation validation (RUN, analyst)

Date UTC: 2026-11-09 (condor submitted 11:08Z, report written 13:07Z). **Status: PASS with open items** (22 of 30 sample types validated end to end; 8 test jobs still RUNNING on condor: cluster 900153 procs 10-15 (six Wggjj variants), 20 (F_QCD_Wgjjj), 21 (F_Wjets_4j). Their sigma stays an ESTIMATE/flagged.) Git commit: none (analyst commits).

## Goal
SPEC_G0 2.1/handoff 5.1 Phase 03: smoke tests of every production card via gridpack, sigma closure (gridpack vs direct, charge sum, decay chain vs production x BR), BR closure, Delphes object validation (MET, lepton, photon, m_gg, VBS jets) with the lib slim card, one condor test job per sample type, twin checks.

## Inputs, versions, seeds
- Stack: `p2/lib/scripts/setup_stack.sh` (LCG_110, MG5_aMC 3.6.3 upstream, Pythia 8.317, Delphes 3.5.1, NNPDF31_nnlo LHAID 303600); Delphes card `lib/cards/phase04_candidates/delphes_card_CMS_slim_v1.tcl` with RandomSeed pinned by lib `run_py8_delphes.sh`; Pythia seed = event seed + 1e8. Gridpack sha256 (12 chars) stored in each job json.
- Lib scripts used UNMODIFIED via condor transfer: `make_gridpack.sh`, `run_job.sh`, `run_py8_delphes.sh`, `slim_gentruth.py`, `py8_common_CP5.cmnd`. Only the chaining wrapper `scripts/condor/p03_job.sh` is new.
- Cards: 28 Phase-02 production cards (`cards/phase02/prod/`) + two NEW production cards written this phase from the validated P01 syntax: `S_EW_WHjj_Wlnu.mg5` (QCD=0 QED=4, W->e/mu nu in ME) and `H_QCD_WHjj_Wlnu.mg5` (QCD=2 QED=2). I_EW_QCD_WHjj (signed cross term) is NOT generated as an event sample (negative weights; its sigma closure is the P01 coherent-sum test, pull -1.35). PY8 cmnd: `cards/phase03/py8_ew_haa.cmnd` (EW H samples, dipole recoil), `py8_qcd_haa.cmnd` (QCD H samples, copy of lib py8_qcd_zhjj_haa), `py8_generic(.dipole).cmnd` (backgrounds; EW backgrounds dipole recoil).
- Seeds (SPEC_G0 3.4, P=2, R=x): gridpack build J=0, test events J=999 (J=999 reserved for p03 tests; production must use J in 1..998). Uniqueness asserted in `scripts/p03_submit.py` (60 seeds). Test events never enter s or b.

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
