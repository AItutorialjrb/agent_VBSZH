# Brief v3: executor-wh, multi_r1, final analysis from wh-prod-v1 to the VH combination (orchestrator, 2026-11-08; D19)

Read this brief, not the full handoff. Binding sources, in this order:
1. p2/SPEC.md §1, §4 and §6, especially D4, D9, D27–D29, D31–D38, A1 and A2.
2. This brief.
3. reviews/wh_prod_validation.md and reviews/wh_G2_recheck.md, whose conditions stay binding.
4. wh/reports/04_production_plan.md §18–21.
5. p2/production/wh/FORMAT.md and SAMPLES.csv.

**Write locations.**
- You write in p2/runs/multi_r1/wh/ and in p2/combination/ (the VH files only; ZH_erratum.md belongs to the separate ZH-erratum executor).
- Production data in p2/production/wh/ is read-only. The only exception is the H_ggF_jj v1.1 rows (§1).
- The ZH tree, p2/lib and software/ are read-only. Reuse frozen ZH code from p2/lib; put patches in wh/patches/.
- Never touch hh/, other run directories (multi_r2, multi_r3, single_r*) or ~/.codex.
- **Git:** the orchestrator commits. You do not run git.

## 0. Binding rules
- Use Delphes-level yields only. Apply the BR once. Normalisation follows SAMPLES.csv `normalisation_formula` × L.
- Every yield carries its source, selection, raw N, weighted MC uncertainty and cutflow. A nominal 0 from missing MC support is never proof that a background is negligible: give a Poisson 95 % UL scaled by the per-event weight.
- **Blinded style.**
  - Optimise on expected yields only, with sidebands and the signal window reserved.
  - Choose cuts by pre-declared criteria, not by maximising a noisy scan.
  - Fix the selection in a report section before computing the final significance.
- Use only the frozen samples. If a method needs a new sample (for example the 2j F_QCD row under D34), raise a decision in STATUS and continue the other work. Any new production needs a test job, the N rule and seeds under SPEC §3.4 (J ≥ 600).
- Condor jobs go to schedd bigbird103.cern.ch. Use scripts/fix_memory_holds.sh and D33 for held jobs. Nothing heavy runs on the login node: anything over about 10 min of CPU goes to condor.

## 1. H_ggF_jj (D38), handled first in the background
- When 893012 finishes, run the test job, the pilot, the plan row and the submit under the N rule.
- When the samples are delivered and validated, add v1.1 rows to SAMPLES.csv and SHA256SUMS. Record the new manifest for the orchestrator.
- If 893012 fails (D-WH-14), bound H_ggF_jj with a 95 % UL from the available ggF H samples (state which and how). Log it in STATUS for SPEC §7.

## 2. Background model (D32 item 1, with D34 and D35)
**(a) Fake photons (D34 = option a′).**
- Nominal method: the fake factor with the lepton-decontaminated per-jet j→γ rate, built from genuine in-jet photons only (π⁰/η, matched to a GenTruth photon carrying most of the reco energy).
- Delphes energy-flow artefact photons are excluded from the rate and from the nominal. Define the veto with GenTruth: a reco photon with no gen photon of pT > 10 within ΔR < 0.1, or with E_gen/E_reco below a stated cut. Validate the veto on the *_full.root test files, including the reviewer's test of summed true E of Photon.Particles against reco E.
- Calibrate the rate to a published CMS non-prompt-photon fraction in a comparable final state (for example the CMS Wγγ/Zγγ measurements). Verify the record (DOI, HEPData, table) and cite it. The difference between the calibrated and uncalibrated rate is a systematic.
- The direct count, artefact included, is an upper variation only.
- Decide whether the method needs the 2j F_QCD row. It does only if the in-jet fake topology needs a 2-parton sample: the fake photon consumes a jet, so the 3j row may already cover it. State the argument. If the row is needed, raise D-WH-17 with its cost and stop that branch.
- Two-fake rows: use the fake factor squared with the decontaminated rate, cross-checked against the direct-count Poisson UL.

**(b) Non-prompt leptons (D35, which supersedes the D28 bracket).**
- Heavy-flavour non-prompt leptons come directly from Delphes MC.
- Light-hadron misID uses a per-jet parametrisation applied to each process's own jets. The nominal is the tight working point matching the Delphes lepton efficiencies: 2×10⁻⁵ for electrons from the cited table, and a separately cited value for muons.
- 2×10⁻³ is not an upper bound.
- Calibrate to a published CMS non-prompt-lepton fraction in a comparable final state if one exists, and cite it. If none exists, say so.

**(c) e→γ and lost-lepton.** Use the measured Delphes e→γ rate from FORMAT.md, plus the lost-lepton rows (including the frozen ZH rows in SAMPLES.csv).

**All classes.** Give lower and upper bounds for each class. The τ uplift is ±100 % (D9).

## 3. Selection (D32 item 2)
- Start with a cut-based selection, using pre-declared criteria and expected yields.
- Then try a BDT or DNN with K = 5 k-fold, using disjoint training and evaluation sets. Check the N_eff per fold.
- Adopt the MVA only if it gains more than 10 % in expected significance and is stable across folds and seeds. Report both.

## 4. Statistics (D32 item 3, D36)
- Eq. 1 significance and exact-Poisson CLs μ95 at 500, 1000 and 3000 fb⁻¹.
- An mγγ profile-likelihood fit with nuisances, including per-bin MC-stat (Barlow-Beeston).
- Signal definitions (a) and (b).
- A with/without-MC-stat impact.
- **D36:** significance, μ95 and the λWZ < 0 exclusion as a function of the non-prompt normalisation, ×0.3 to ×3, with fake photons and non-prompt leptons scanned separately.

## 5. Couplings (D32 item 4)
- λWZ and (κW, κZ) from the direct coupling samples: a per-bin quadratic and a leave-one-out closure.
- The significance of λWZ < 0 and of λWZ = −1.
- c_A only if cheap; state the cost and the choice.
- Optimise the binning over mjj, pT(γγ) and m(Wγγ).

## 6. VH combination (D32 item 5, D37)
- Combine with the frozen ZH (zh-final-v1.1) and correlate the nuisances: luminosity, theory per process class, photon and lepton efficiency scenarios.
- Report the combined μ95 and λWZ at 500, 1000 and 3000 fb⁻¹.
- Use the corrected ZH numbers from p2/combination/ZH_erratum.md where they differ. The orchestrator relays them when ready. Build the combination so that the ZH inputs are a swappable table.
- Write p2/combination/VH_combination.md plus tables (json/csv).

## 7. Comparison (D32 item 6)
Compare with CMS PLB 860 (2025) 139202 and ATLAS PRL 133 (2024) 141801. Verify the numbers from the papers and cite tables or figures.

## 8. Reports and protocol
- **Phase reports:** wh/reports/05_selection.md, 06_systematics.md, 07_sensitivity.md, 08_reproducibility.md, FINAL_report.md, final.json, and figures (PDF+PNG). Each report states date, PASS/FAIL, inputs, commands, checks, caveats and next steps (AGENTS.md).
- **VERIFY_REQUEST:**
  - Write one for each finished block: background model, selection, statistics, couplings, combination.
  - The orchestrator runs the verifier.
  - The reviewer runs once at the final result (G3, D20 auto-pass if there is no sev-1 and no open decision).
  - The orchestrator may also ask for one focused review after the background model, which is the riskiest block.
- **STATUS.md:** at most 25 lines. Give done items, running clusters (with schedd), decisions needed (D-WH-17+), and the next action. Your reply to the orchestrator is a pointer to STATUS.md only.
- **Human decisions:** raise them in STATUS, stop that branch, and continue the rest.
- **Waiting:** no idle polling. When only condor remains, set STATUS "waiting on clusters X" and return.
- The first line of your work log is ROLE=executor-wh PHASE=FINAL.
