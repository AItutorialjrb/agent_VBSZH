# WH single_r2 — STATUS at G1 (2026-11-09T00:15Z)
Done: Phase 01 PASS (D-WH-1..3 defaults); Phase 02 PASS as design ledger (3 open quantitative items); Phase 03 BLOCKED(partial): signal,
  QCD WHjj, ttH(1l), QCD Wajj test jobs PASS; prompt Wgg continuum pending. Self-review: reports/G1_self_review.md (4 sev-1, 7 sev-2).
Key numbers: sigma(EW WHjj, W->e/mu nu, 4F) = 13.76 +- 0.03 fb; x WF x Bgg = 0.0305 fb = 15.3 ev @500/fb pre-cut;
  illustrative Delphes selection s ~ 1.02 +- 0.12 ev @500/fb (QCD WHjj 0.46). I/EW = -0.41 %. 5F = 2.0 x 4F (tHq).
  Off-shell/on-shell: signal 1.020 +- 0.017; prompt W(gg) continuum 2.01 +- 0.05 (!).
Running: condor 899738.0-2 (B_EW_Waajj, B_QCD_Waajj, B_QCD_Waajj_vbs integrations, 8 cores, flavour tomorrow).
Blockers: continuum sigma/gridpack (running); decisions below.
Decisions needed: D-WH-1 flavour scheme (4F+tHq bkg default); D-WH-2 WF universal vs non-universal; D-WH-3 WF on l-nu-in-ME;
  D-WH-4 off-shell Wgg continuum generation; D-WH-5 aux twins below N rule; D-WH-6 W+jets 2-fake effective-N deviation from SPEC_G0 §1.5.
Next: on answers + continuum sigma -> continuum test job, then G2 production plan (Phase 04 of canonical arm is not this run).
