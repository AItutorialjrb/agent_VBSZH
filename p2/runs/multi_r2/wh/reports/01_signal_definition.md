# WH Phase 01 — signal definition (multi_r2, executor-wh)

Date UTC: 2026-11-09 (work started 2026-11-08T20:3x Z). **Status: PASS** (two non-blocking decisions raised with defaults: D-WH-1, D-WH-2). Git commit: none (orchestrator commits). All numbers here are LO MG5 validation cross sections (labelled validation only, not yields).

## Goal
Define gauge-invariant EW pp -> W±Hjj at sqrt(s)=13.6 TeV, (QCD,QED)=(0,4) amplitude order, both charges; W->e nu / mu nu decayed in MG5 (BR ledger + W-width factor WF); H->gamma gamma forced in Pythia8, SM BR applied once; QCD W±Hjj as resonant background (def. a) and inclusive-signal variant (def. b); interference statement. Validate MG5 syntax by diagram/subprocess lists and short LO runs.

## Inputs, versions, seeds
- Stack: `p2/lib/scripts/setup_stack.sh` (LCG_110 x86_64-el9-gcc13-opt, MG5_aMC 3.6.3 upstream tag, Pythia 8.317, Delphes 3.5.1, PDF NNPDF31_nnlo_as_0118 / LHAID 303600), model `sm-no_b_mass` (5F, massless b, diagonal CKM), as ZH.
- Seeds: SPEC_G0 3.4 with P=2, R=2: `seed = 2 200 000 + 1000*sample_index + J`; registry `config/sample_registry.json`, uniqueness asserted in `scripts/seeds.py` (validation samples use indices 80-99, never enter s or b). Seed per run in `work/p01/phase01_numbers.md`.
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
- MG5 widths from `compute_widths w+ z` (cards/phase01/widths_w.mg5; work/p01/widths/pc_in.dat, a copy of restrict_no_b_mass.dat): Gamma(W->l nu) = 0.2275641 GeV per flavour, Gamma_W(computed LO) = 2.04791 GeV, Gamma_W(param card used in decay chains) = 2.0476 GeV; BR_ll(Z) cross-check reproduces ZF denominators (Gamma_ee 83.965 MeV).
- B_MG5(W->e nu + mu nu) = 2 x 0.2275641 / 2.0476 = 0.222274.
- Reference: B(W->e nu)=0.1071 +- 0.0016, B(W->mu nu)=0.1063 +- 0.0015 (sum 0.2134 +- 0.0022). Caveat: numbers confirmed by a web search against arXiv:2202.14015 (which quotes them), PDG attribution not independently verified; re-check against current RPP.
- **WF = 0.2134/0.222274 = 0.9601 +- 0.0099** (per flavour: e 0.9637, mu 0.9565). Applies only to samples with W->l nu decayed in the MG5 matrix element (analogue of ZF = 0.9783).
- H->gamma gamma: B_gg = 0.002270 (LHCHXSWG YR4, mH=125; as ZH), applied once in the analysis ledger; Pythia forces `25:onIfMatch = 22 22` with conditional BR = 1.
- Sample factor: **k(S_EW_WHjj_Wlnu) = WF x B_gg = 2.1794e-3** (factors listed: WF, BGG; asserted no duplicates in later ledger code). sigma x k = 28.10 x 2.179e-3 = 0.0612 fb. N_MC = max(50 000, 0.0612 fb x 3000 fb^-1 = 184) = 50 000 (sigma x BR x 3000 binds nowhere).
- Same k for QCD W±Hjj (decayed in ME). Cross section stage separation: sigma_prod (undecayed) -> sigma_dec = sigma_prod x B_MG5 -> x WF x B_gg (before cuts) -> after cuts (Phase 05); not mixed.

### W->l nu closure (executed)
sigma_dec/sigma_prod vs analytic 0.2223: W- dynamical scale 0.2200 +- 0.0019 (pull -1.2); W+ dynamical scale 0.2149 +- 0.0018 and 0.2174 +- 0.0022 (pulls -4.2, -2.3; ratios 0.967, 0.978); W+ **fixed mu = 125 GeV** 0.2199 +- 0.0019 (pull -1.3, ratio 0.989). Interpretation: with `dynamical_scale_choice 3` the decay-chain event scale is computed from the full final state including the lepton transverse masses, which differs from the undecayed (W on-shell) scale; with a fixed scale the closure holds within errors. The ~1-3% shift is a scale-definition effect inside the scale uncertainty, not a BR error. WF is applied to the decay-chain sigma itself, so no further correction is made; D-WH-1 asks whether to keep scale 3 or to fix the decayed-sample scale convention. (ZH showed no such shift: pull 1.0.)

## H -> gamma gamma route (executed)
`cards/phase01/py8_ew_whjj_haa.cmnd` (ZH settings) + CP5 common card, LHE of the W+ decayed validation sample, 300 events through DelphesPythia8 (`work/p01/py8check/`, seed 2299000): 300/300 last-copy H decay to gamma gamma (`scripts/check_hgg_decay.py`); Pythia sigma_gen = 1.791e-11 mb = 17.91 fb = LHE sigma 17.91 fb (init block 1.791e-2 pb) -> Pythia does not fold any BR into the cross section for LHE input; SLHA DECAY tables ignored by Pythia. The loop-induced decay is not attempted in MG5.

## Checks / caveats
- Checks passed: syntax (11 cards), no external gluon at (0,4), 896+200=1096 union, coherent-sum closure, H->gamma gamma forcing, no hidden BR, seed uniqueness assert.
- Caveats: MG5 sigma errors are integrator errors from 2000-event runs (second seeds suggest ~1-2% fluctuations beyond quoted error in W+ decayed runs); LO only; 5F massless-b/diagonal CKM; no off-shell/pole comparison (planned Phase 03b as ZH); W->tau nu->l excluded (D-WH-2); lib file copies of `run_py8_delphes.sh` and `py8_ew_zhjj_haa.cmnd` were blocked by a permission deny rule, so those two were re-typed from earlier read output (documented in patches/README.md).
- Decisions: **D-WH-1** scale convention for decay-chain samples (default adopted: keep scale 3 as ZH; document closure at fixed scale; alternative: fixed/undecayed-W scale). **D-WH-2** W->tau nu (->e/mu nu nu, ~+19% of the e/mu signal-like events before cuts, softer leptons) is outside the specified signal; default: separate feed-down sample reported separately, decided in Phase 02.

## Commands
`scripts/run_parse.sh <card>`; `scripts/run_validation_batch.sh <sample...>` (calls `scripts/mg5_run_wh.sh <card> <seed> 3000`, scratch in session scratchpad, 3 parallel on a login node, tiny validation only); `scripts/run_py8_wh.sh work/p01/V_ew_wp_wlnu/unweighted_events.lhe.gz cards/phase01/py8_ew_whjj_haa.cmnd 300 2299000 <out.root>`; `scripts/phase01_numbers.py`. No condor submission.

## Next actions
Phase 02: background/overlap ledger (Wgg, Wg+jets, W+jets fakes, ttg(g), tWg, ttH/tH, ZHjj/Zggjj lost lepton from frozen ZH samples, QCD gg+jets with non-prompt lepton, photon overlap removal, twin samples) incl. W->tau nu feed-down; then Phase 03 smoke/closure per sample type and one condor test job.
