# STATUS hh (multi_r1) — updated 2026-11-03 UTC (after G1 review, PASS-with-conditions)
Done: 01 PASS; 02 PASS (review item 1 fixed: explicit tag classes top/Hbb/bb_nonH/b/c/l, 02 §8 restated for 3 scenarios with 95% intervals/ULs; SM 0.070 [0.009,0.25] ev @500/fb);
 03 PASS for the 10 types with gridpack+test job; NOT met: W±H, ggH+jj, W+jets, QCD 4b, ttjj (planned only). Pre-G2 plan: reports/03 §13. Extra bkg sigma-only gridpacks (cluster 884857, done) ledgered in 02 §9b.
Running: none.  Verifier: not requested for the G1-fix edits (docs/scripts only; matrix re-rendered, nmc_check passes).
Decisions (no implementation):
 D-HH-1 HEPTools dir in frozen software/ (human rm -rf).
 D-HH-2 ggF HH+2j / K-factor / EW-loop interference (ggF HH ~ half of SM signal in anchor SR).
 D-HH-3 ttbar VBS topology: ttjj ME+filter vs validated MLM.
 D-HH-4 QCD multijet: 6-parton MEs infeasible; accept 4j+bbjj+PS+truth-tag, large residual unc.?
 D-HH-5 SM boosted acceptance ~2.5% -> deliverable = kappa2V!=1; thresholds 300/450 provisional.
 D-HH-6 background twins + N_eff>=10 before G2; HH storage <=150 GB.
 D-HH-7 ME jet multiplicity: Z/W+3j, VH+2j, ggH+jj (or PS-modelling unc.).
 D-HH-8 m(HH) clipping value.
 D-HH-9 trigger 450 GeV baseline + pre-declared 500/550 variation (+ no fat-jet JES in m_SD window).
 D-HH-10 tagging class definition (bb_nonH rate = b/g->bb column).
 D-HH-11 extra backgrounds tW/ttZ/ttW/EWZjj/QCD ZZ (sigma 1.83/0.162/0.104/8.78/0.086 pb): bounds+plan in 02 §9b; accept or dedicated samples.
 D-HH-12 full N instead of effective-N for ggF HH/ZH/ZZjj/ttH: cost ~3.5 GB, ~15 CPU-h (recommended).
W-width factor: none needed (no MG5 decays in yields), 01 §7. mg5priv diff + sha256: config/mg5priv_diff.md (03 §14).
Next action: await human answers D-HH-1..12 and G2 plan (03 §13).
