# Phase 00 — initial study design (prepared outside lxplus)
Status: DESIGN ONLY — LXPLUS NOT CONNECTED, NO MC GENERATED.
Date: 2026-10-31.

## Paper facts copied with attribution
Ding et al., arXiv:2512.07689v1, attached reference pp. 4–6: 13.6 TeV, 500/fb projected, MG5 3.6.3 LO, Pythia8, Delphes 3.5 CMS card, 0/1/2-jet MLM for QCD Zgamma and Zgammagamma. pp. 9–11: final m_jj >700 GeV and |delta eta_jj| >2.0 were optimized for *EW Zgammagammajj*, not ZHjj. Their 4.50 sigma must not be carried into this study.

## Current results
No signal cross section, cross section times BR, background yield, detector efficiency, or significance for ZHjj has been computed. Any such numbers are pending validation.

## Open physics decisions
- gauge-invariant ZHjj perturbative-order definition / Higgsstrahlung and interference;
- one-loop H->gamma gamma decay and exact branching normalization;
- overlap of EW/QCD continuum and Zgamma fake contributions;
- resonant ZH and other Higgs background treatment;
- fake-rate calibration scenarios and systematics;
- mass resolution and 125 GeV mass-window policy.

## First lxplus actions
1. collect OS/CVMFS/scheduler/software environment;
2. check Codex version and current model; lock both;
3. extract reference figures/tables and selection choices;
4. prepare and SMOKE-TEST MG5 process definitions only, before bulk MC.
