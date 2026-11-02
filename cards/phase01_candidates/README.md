# Phase 01 candidates — UNTESTED

These cards express proposed orders, not validated generator behavior. No generator was run. Read [the audit](../../reports/01_signal_process.md) before use. No output, launch, download or installation commands are included.

The explicit five-flavour parton lists and `sm-no_b_mass` are a massless-bottom, zero-light-Yukawa, diagonal-CKM approximation for audit. Heavy-flavour and CKM completion must be signed off before calling the result complete SM EW ZHjj. Gluon channels are available to the QCD controls; pure EW tree amplitudes cannot attach an external gluon at QCD=0.

All cards are separate alternative calculations. Never add the combined sample to its EW/QCD/interference components; never add on-shell and off-shell alternatives. The Z decay card explicitly includes exactly ee and mumu. H remains undecayed until the validated Pythia step.

Run-card specification, not a tested run card: proton beams, ebeam1=ebeam2=6800 GeV; mH=125 GeV; no event count or production seed assigned. Proposed baseline audit seed 13600501 (not used). PDF, scale implementation, widths, cuts and shower interface remain blocking pins. Initial jet cuts for later convergence tests: pT>20 GeV, |eta|<5, DeltaRjj>0.4; no final mjj or Deltaeta requirement. For the off-shell comparison require mll>50 GeV and align lepton cuts in both alternatives. Photon cuts belong after the Higgs decay, not to the undecayed production card.
