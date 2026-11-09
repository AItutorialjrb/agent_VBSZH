# Patches against p2/lib (ZH tag zh-final-v1.1); lib itself is never modified
| # | file | lib source | rationale |
|---|---|---|---|
| 001 | scripts/mg5_smoke_wh.sh | lib/scripts/mg5_smoke.sh | write into this run's wh/work (not frozen ZH work/), registry seeds, record process list + diagram counts, clean /tmp scratch |
| 002 | scripts/run_py8_delphes_wh.sh | lib/scripts/run_py8_delphes.sh | paths from p2/lib instead of frozen root; sample cmnd + Delphes card explicit (default slim_v1); physics unchanged |
| 003 | scripts/condor/mg5_job_wh.sh | lib/scripts/condor/make_gridpack.sh | stage to run's wh/work/gp_condor, keep process list/banner/LHE, success = σ in log; same MG5 tarball + stack |
| 004 | scripts/fakefactor_pilot_wh.py | lib/scripts/fakefactor_pilot.py | W selection (==1 lepton, lead pT>25, MET>30) replaces the Z window; fake model/regions unchanged |
