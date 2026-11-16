# WH multi_r3 progress (executor-wh)
- 2026-11-08T21:15Z start. Read SPEC_G0, handoff 1/5.1/2.3, frozen ZH reports 01-03 + lib scripts. condor_q clean for rjiang at start.
- Created wh/{reports,cards,scripts,patches,config,figures,work}; config/sample_registry.py (seeds 2 3xx xxx, uniqueness asserted).
- scripts/gen_cards.py -> 26 cards (smoke/ + prod/); scripts/mg5_run.sh (adapted from lib mg5_smoke.sh); scripts/wfactor.py: WF = 0.9601 (analytic, to be closed vs MG5 sigma ratio).
- Launched interactive smoke chains A,B (work/smoke/chain{A,B}.log): EW/QCD/interference W+-Hjj, W+H 0j decay closure, off-shell check.
- (UTC note: the first line above used local CET clock; true start ~20:16Z.) 
- Interactive MG5 sigma (work/smoke/xs_summary.json): EW W+Hjj 83.99, W-Hjj 46.71 fb; QCD 164.6/101.3 fb; interference -0.1435/-0.1146 fb; 52 proc/896 diagrams (EW), 60/200 (QCD), 52/1032 (int); W+H 0j 804.7 fb.
- W->l nu closure: sigma(chain)/sigma(undecayed)=0.2150+-0.0018 (scale choice 3) vs analytic 0.2223 -> -4 sigma; bwcutoff scan (5/15/100: 166.4/173.0/174.5 fb); scale-matched (dyn scale 4) test queued. WF=0.9601 analytic.
- Frozen-ZH reuse coverage test (scripts/zh_lostlepton.py) done for EW/QCD ZHjj, ggZH, ZH->tautau, ttH, tta, tWa, ttaa (work/lostlep/*.json).
- Condor: gridpack cluster 899739, test cluster 899740 submitted (work/condor/clusters.txt).
2026-11-09T00:03:38Z resumed after usage-limit; clusters 899739/899740 finished (all outputs present); no resubmission
- 2026-11-09T00:12:47Z P01-P03 reports, INDEX, STATUS written; pilots (W+2j, Wg+2j, Zg e-fake) done; stopped at end of Phase 03.
