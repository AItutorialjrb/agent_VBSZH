# WH multi_r3 STATUS (executor-wh) 2026-11-09
Done: P01 PASS, P02 PASS (ledger; Waajj sigma/fake N_MC open), P03 PASS (signal machinery). Reports + INDEX in reports/. Stopped before Phase 04.
Running clusters: none (899739 gridpacks, 899740 test jobs: all 8 exit 0, no resubmission).
Decisions (recommendation first):
- D-WH-1 W normalisation: chain sigma/undecayed = 0.215-0.217 vs analytic 0.2223 (BW-cutoff dependent). Rec: sigma_chain x WF(0.96008) x B_gg, +-3.3% norm syst.
- D-WH-2 N_MC: tt gamma(1l) needs 1.21M ev; F_Wgamma jj 2.4e7, F_Wjj 6.9e9 by brute force. Rec: extend effective-N policy (handoff 5.3) to WH fakes + twin-validated VBS-biased generation.
- D-WH-3 photon gen cut pT>20 (ref) vs 25 (ZH forced). Rec: 20.
- D-WH-4 pilots (lower bounds, N_eff<10): W+2j 2 fakes 1.7 ev, Wgamma 2j 6.4 ev, Z(ee)gamma e->gamma 2.4 ev (f=2%) in PEAK at 500/fb vs signal-like ~0.6: reducible bkgs dominate; prioritise in Phase 04.
- D-WH-5 off-shell (0,5) lvHjj = 0.89 x on-shell chain (both scales), unexplained. Rec: quote >=11% pole-approx syst, investigate in Phase 04.
Incidents: compute_widths rewrote auto-generated software/.../models/sm/param_card.dat (not in tarball, regenerated on import; not restored). A ps listing exposed other runs' command lines; not used.
VERIFY requests: (1) clusters 899739/899740 exit codes+event counts; (2) sum ALL init rows of work/test/*/*.lhe.gz vs reports (wrapper JSON records one row only); (3) PY8 vs LHE sigma closure; (4) br_ledger.json N_req table + single-occurrence of WF/B_gg; (5) seed uniqueness in config/sample_registry.py vs scripts/condor/*.sub.
Not done: W gamma gamma jj sigma (timeouts), W+4j sigma, tHq/tHW/tt_1l cards, overlap/twin validation.
Next: Phase 04 only after gate G1 decisions.
