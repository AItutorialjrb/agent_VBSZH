# multi_r1 PROGRESS (orchestrator)
- [x] 2026-11-03 §8 step 1 setup: p2 layout, lib export (zh-final-v1.1 = 5785329), SPEC.md, agent files (multi_r1-3), isolation settings (all 6 runs), metrics (ledger, prices, prompts, review_log, parse_usage.py), ENFORCEMENT.md
- [ ] WH Phase 01–03 (executor-wh)
- [ ] HH Phase 01–03 (executor-hh)
- [ ] verifier audits of condor test jobs
- [ ] G1 reviewer (wh, hh)
- 2026-11-03T17:22Z verifier WH audit #1: finished tests PASS; FAIL items: matrix σ (I_WHjj negative, F_Wajj_pilot, H_ttH_1l), F_Wjj fake-factor σ input, SPEC §3.4 seed formula collides across runs for sample idx ≥ 10 (orchestrator error -> decision D1). Sent to executor-wh.
- 2026-11-03T17:35Z executor-hh returned: 01 PASS, 02 PASS (D-HH-2..6), 03 9/10 types; incident D-HH-1 (HEPTools written in shared software/ install; flagged, cleanup left to human).
- 2026-11-03T17:31Z verifier HH audit #1: tests/closure/seeds/N PASS; FAIL: BR rounding vs strict tol, repeated-factor false positive (ZZ), role wiring sig vs basis/closure (strict N rule not applied to HH signal), gridpack provenance, exit-code hygiene. Sent to executor-hh with Q_4j test job.
- 2026-11-03T21:33Z executor-hh G1 fixes: sev-1 tagging class fixed, 02 §8 restated; D-HH-1..12; σ-only gridpacks 884857 for extra bkgs; 5 handoff sample types still lack gridpack/test (stated).
- 2026-11-03T21:50Z executor-wh: 10/11 gridpacks; 8 test types done; B_EW_Waajj_vbs gridpack still running (D-WH-6); twin test: mmjj>400 gen cut UNSAFE for QCD-type (47.6±5.5% loss Waajj, 37±9% Wajj).
- 2026-11-03T21:55Z verifier WH #3 (native type): all finished jobs/σ/N/seeds/twin numbers PASS; FAIL F-1 twin_safety.py not reproducible in pinned env (uproot/zstandard); docs F-2,F-4,F-5. Note: verifier wrote a recheck script + 2 json into the orchestrator scratchpad (/tmp), not the run tree — role says never write; logged.

## 2026-11-03T22:24:19Z — G1 decisions received
- Answers recorded in SPEC §6. D9 (τ) and D10 (untested types) were not answered, so orchestrator defaults are in the briefs, for confirmation at G2. Protocol decisions are D17–D22. SPEC_G0.md is frozen, and the repeat-isolation script is prepared for the human. Commit b77d5cd.
- No severity-1 WH review item is uncovered: item 1 is fixed, and item 2 is covered by the twin decision.
- Native executor-wh and executor-hh were spawned with brief_{wh,hh}.md (PRE-G2). Next steps: the verifier on each VERIFY_REQUEST, then the reviewer on 04_production_plan.md at G2.

## 2026-11-04T13:40:56Z — PAUSE (human order: credit limit, resume next week)
No condor job was submitted, released or removed by the pause. All subagents are stopped. Executor-wh wrote STATUS.md at 13:40Z. Executor-hh had already finished; its STATUS.md (10:58Z) is current. The VERIFY #9 audit was stopped unfinished (read-only, no state).
**Done**
- G1 decisions are recorded (SPEC §6 D1–D22), SPEC_G0.md is frozen, and the briefs are written.
- HH: Phase 03 is complete (every type tested). 04_production_plan is at G2 and the reviewer verdict is APPROVE-with-conditions (reviews/hh_G2.md). All non-decision conditions are fixed and verified. The QCD block is HELD in hh/scripts/condor/HELD_do_not_submit/.
- WH: 28 of 30 types are tested. 04_production_plan (581 jobs, ~1019 core-h, ~53 GB) is at G2, with the reviewer verdict APPROVE-with-conditions (reviews/wh_G2.md). G2-FIX items 1–8 and 13 are done. VERIFY #4–#8 fixes are applied; #9 is not yet audited.
- Open decisions for the human: D9, D23–D31 (SPEC §6).
**Running clusters** (schedd bigbird103.cern.ch; the default schedd shows none):
- 884934.13: B_EW_Waajj_nomjj gridpack.
- 885044.0: V_ZZa_WH gridpack.
- 885122.2: H_ggF_jj gridpack.
- 885124.0: F_QCD_llajj_loose gridpack. It was no longer in the queue at 13:40Z, so check its outcome.
**Held jobs to release on resume:** none in condor. The HH QCD block-3 and D14a twin2 submit files are deliberately unsubmitted and await D24.
**Next action per stream**
- WH: on resume, check the 4 gridpacks (exit_codes.py). Then run scripts/followup_after_gridpacks.sh test, followup_g3.sh and twinB, fakelep_pilot.py on H_ggF_jj, and twin_safety2.py on the B_EW twin. Rebuild the builder, plan, prod-subs and assemble. Then the verifier audits VERIFY_REQUEST #9 (and #10 for the gridpack follow-ups), and the WH G2 rows for the pending gridpacks get a verifier sign-off.
- HH: idle at G2. Next is the human answers to D23–D26. After that, submit block 1 (62 jobs) and block 2 (66) per 04 §14; the QCD block waits for D24.
- Orchestrator: G2 report to the human (both reviews, D9 and D23–D31, token/time table). Bulk production only after human approval.

## 2026-11-07T19:49:15Z — WH production tagged wh-prod-v1; STOP for human (A2)
- **Done:**
  - WH production delivered: 128 GB, 2688 ROOT files, 43-row SAMPLES.csv (incl. read-only frozen ZH rows).
  - Measured-N check: 39 PASS + 2 human-exempt (F_Wjjjj, T_ttjj_1l).
  - Q_aajjj replaces Q_aajj (pre-declared D29 rule).
  - F_QCD_Wajjj_nomjj (ME+1j) replaces the withdrawn 2j row (D29 supersedes D30).
  - D33: 3 F_Wjjjj chunks dropped, N rule holds.
- **Reviews:** wh_G2_recheck.md Recheck 3; wh_prod_validation.md (HOLD → recheck APPROVE-with-conditions, conditions met). Verifier #19–#25.
- **Key findings:**
  - The pre-production j→γ tables were lepton-contaminated; the corrected rate is 3.6e-5–1.5e-4 per jet.
  - The fake-factor direct closure fails ×5: 12/16 traced non-prompt photons are a probable Delphes ECal-tail artefact (untested).
- **Tag:** package metadata snapshot in metrics/wh-prod-v1/ (MANIFEST.sha256); access instructions in metrics/single_r1_access_wh-prod-v1.md.
- **Open human decision H1** (one-fake nominal method; reviews/wh_prod_validation.md Recheck): options (a)/(b)/(b'), reviewer recommends (b').
- **Pending v1.1:** H_ggF_jj (gridpack 893012 still running; D-WH-14 if it fails); the 2j row only if H1 = (b).
- **Next (on human go):**
  - H1 answer;
  - repeat runs launched by the human;
  - multi_r1 final analysis D32 after relaunch;
  - H_ggF_jj v1.1.
