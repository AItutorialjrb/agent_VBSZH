# VBS-enriched pp -> ZHjj, H -> gamma gamma: project charter

## Fixed scenario
- pp at 13.6 TeV; projected 500 fb^-1 (matching the attached reference; NOT strictly a delivered Run 3 luminosity claim).
- Z -> e+ e- or mu+ mu-. H -> gamma gamma. Two VBS tagging jets.
- LO MG5 + Pythia8 + Delphes CMS detector card as INITIAL reference workflow; version and physics-quality upgrades must be explicitly motivated and documented.
- Reference study: Ding et al., *Prospects for measuring electroweak production of Zgamma gamma and 2 jets at the LHC*, arXiv:2512.07689v1 (Dec 2025), locally available as `reference_ZGammaGamma.pdf`.
- Reference generator setup: MG5_aMC 3.6.3 LO; sqrt(s)=13.6 TeV; pT lepton >10 GeV, pT gamma >15 GeV, pT jet >20 GeV; |eta lepton,photon|<2.5, |eta jet|<5, DeltaR>0.4, mll>50 GeV; Pythia8; Delphes 3.5; CMS card; QCD Zgamma and Zgammagamma samples 0,1,2 jet MLM matched/merged.
- Reference reconstruction baseline: >=2 good photons, OS-SF lepton pair, >=2 jets; pT lepton>15, gamma>20, jet>25 GeV, |eta lepton,photon|<2.5, |eta jet|<5. Reference paper used mll between 70 and 120 GeV and optimized mjj/deltaeta; **do not automatically copy its final optimum** (mjj>700, |deltaeta|>2).

## Signal definition issues to resolve BEFORE production
1. Gauge-invariant LO EW pp -> ZHjj, perturbative-order bookkeeping; include all required diagrams and interference. Isolate VBS-enriched fiducial phase space rather than call a hand-selected diagram subset 'VBS signal'.
2. Correct H->gamma gamma decay model, loop-induced BR and spin/kinematic treatment; total rate and normalization checks.
3. Z decay with lepton-flavour completeness, off-shell Z/gamma* effects where appropriate.
4. Define other ZH production mechanisms (QCD-induced, gg-initiated if relevant) as irreducible Higgs resonant components or separate categories; check overlap.

## Starting background ledger (hypotheses; NOT established ordering)
- Prompt continuum Zgamma gamma + >=2 jets QCD-induced and EW-induced, their possible interference.
- Zgamma + jets with 1 jet->gamma fake; Z + jets with double fakes; consider electron->gamma and nonprompt leptons if applicable.
- ttbar gamma gamma, ttbar gamma, single-top gamma( gamma), diboson + photons with jets as justified.
- Resonant H->gamma gamma from other Higgs production associated with Z / other leptonic processes; classify by measurement definition.
- Photon FSR/ISR, parton-shower photon overlap and merged samples; explicit veto/phase-space partition, not ad hoc truth-parent classification alone.

## Minimum plots
mgg (broad sidebands and zoom at 125), mll, mjj, delta_eta_jj, leading/trailing photon pT, diphoton pT, Z pT, Zeppenfeld centrality, jet multiplicity, b-tag multiplicity, MET. Include weighted yields and MC errors.

## Essential decision gates
- Phase 01 sign off signal definition and decay chain with test evidence.
- Phase 02 sign off mutually exclusive sample phase-space ledger.
- Phase 03 show generator-level sanity and xsec*BR bookkeeping tests.
- Phase 04 inspect Delphes photons, mass resolution, fake modeling limitations.
- Phase 07 issue no evidence-of-observability claim without uncertainty/sensitivity analysis.
