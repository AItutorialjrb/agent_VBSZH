# STATUS wh multi_r2 (executor-wh) - Phase 03
Phase 03: PASS with open items (reports/03_generation_validation.md; INDEX, PROGRESS updated; manifest config/p03_condor_manifest.json).
Done: 30 condor test jobs (gridpack+2000 ev+PY8+slim Delphes); 22 finished and validated: sigma closure (gridpack/direct 0.2-4%, LHE/PY8 <=0.3%), charge sum, W decay chain, forced H->gg 2000/2000, PY8 BR(gg)=0.002297 vs YR4 0.002270, Delphes MET/lepton/photon/mgg(2.17 GeV)/VBS jets, twins; ttjj sigma measured (92.15 pb).
Running cluster IDs: 900153 procs 10-15 (six Wggjj), 20 (F_QCD_Wgjjj), 21 (F_Wjets_4j) - still integrating; their sigma stays ESTIMATE/unmeasured. Re-run p03_fetch/p03_closure/p03_delphes_val when done.
Blockers: none for G1; D-WH-4/D-WH-5 still block Phase 04.
Decisions needed:
- D-WH-1, D-WH-3..D-WH-8: open, defaults kept (see report 02).
- D-WH-9: QCD Wgjj/Zgjj twins fail (2-5 sigma) for reco mjj<~800; EW twin passes. Default: biased samples only with reco mjj>~1000 + nomjj cross-check/systematic; alternative lower mmjj or merged samples.
- D-WH-10: W->lnu chain sigma 1-2% below prod x B_MG5; default no correction, +-2% norm. syst.
- D-WH-11: seed convention J=0 gridpack build, J=999 tests, production J=1..998.
Next: collect the 8 running jobs; G1 decisions; Phase 04 planning on go.
