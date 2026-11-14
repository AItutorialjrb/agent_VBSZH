# Self-review (referee mode) — single_r1 WH Phase 05–07 (gates after 05, 06, 07)

**Date UTC:** 2026-11-14. **Reviewer:** the same single Opus session that produced the work (single arm, no independent reviewer by design); blind spots shared with the author are not excluded.
**Reviewed:** `wh/reports/05_selection.md`, `06_systematics.md`, `07_sensitivity.md`, `FINAL_report.md`, `final.json` against `wh/work/p05/{p05,bdt,p07}.json` and `wh/scripts/p05/*.py`.
Severity 1 = changes a result or violates a SPEC_G0 §1 policy; 2 = weakens a claim; 3 = presentation/minor. Per the A2 instruction, each gate was passed by taking the declared default and continuing; nothing below blocks the final result, but the severity-1 items qualify it.

## Gate 05 (selection, backgrounds, optimisation)
**S1-9 BDT stability is marginal.** The pre-declared rule (gain > 10 % and a positive gain in every fold, AUC(train) − AUC(test) < 0.02) passes after a genuine bug fix (the e→γ closure factors were not passed to the BDT script). The pre-fix run failed fold 0 (0.56 vs 0.58). The overall gain (+66 % in Z(σ_b) at 500 fb⁻¹) comes largely from regions where the low-statistics backgrounds (QCD Wγγjj: 3 raw events in the window, 50k sample) are estimated by the L1/L2 hierarchy rather than counted. The AUC gap (max 0.019) is close to the limit. *Mitigation done:* the cut-based result is reported alongside in 07 and FINAL. *Not done:* an independent statistically adequate test sample, which would need new background MC.
**S1-10 e→γ method non-closure (factor 4.0 ± 0.1) for the loose QCD ℓℓγjj sample.** The per-electron weighting under-predicts the Delphes direct e→γ in `F_QCD_llajj_loose`, while it closes for the EW sample (1.02). The measured factor is applied as a correction (D-WH-13). The cause is only partly identified: about 17 % of the direct e-photons are prompt FSR photons, and the rest probably comes from collinear/soft γ*→ee configurations where both electrons are not isolated. A correction derived in a relaxed region is assumed to hold in the SR. The impact on b is small (e→γ total 0.11 of 1.26 events at 500 fb⁻¹, with 100 % uncertainty).
**S2-8 j→γ parametrisation does not describe the Delphes mechanism.** About 78 % of the Delphes non-prompt photons are more than 0.4 from any GenJet, so the per-jet ΔR<0.2 rate of FORMAT 6a under-predicts Delphes by about 5×. The weighting reproduces the m_jj shape. The nominal scenario is about 4× Delphes, i.e. conservative. Real-detector fake rates are a scenario in any case (robustness rows ×0.3, ×3 and the Delphes rate).
**S2-9 Optimisation boundary.** The cut-based optimum takes pT^γγ at the largest grid value (120 GeV; the 80 → 120 step gains 6 %). The pick rule (highest s within 3 % of the best Z) limits noise chasing, but the edge was not explored.
**S2-10 N_eff < 10 sources in the SR.** These are QCD Wγγjj fit range (13.6 OK; window 3 raw), F_EW_Wajj (7.6), Q_aajjj (5.5), ℓℓγjj EW (6.4), tt̄γ / tWγ prompt-prompt, V+γ, tt̄H, ZH→ττ. They are handled by the hierarchy (L1/L2 with 100 %) and the zero-support rule. The conservative variant (all at max(value, 3 w̄)) lowers Z(σ_b) at 500 fb⁻¹ from 0.91 to 0.70 (robustness table).
**S2-11 tt̄γ prompt-prompt events kept (ZH convention).** One heavy direct event (0.29 events at 500 fb⁻¹ in the cut-based fit range) is replaced by the L2 factorised estimate. Overlap with tt̄γγ is bounded by the tt̄γγ UL.
**S3-6** The `nraw` column counts unique events per component; pseudo-event tables have several rows per event, so "raw rows" ≠ events for F1/F2/FL/EG.

## Gate 06 (systematics)
**S1-11 Jet-modelling nuisance is statistics-limited and dominant.** The ratio of selection efficiencies, QCD WH MLM vs fixed order, is 0.89 ± 0.19 (35 vs 116 selected rows). The statistical error (19 %) is used as the size, applied 100 % correlated to all background prompt/FL components. It is the largest single b nuisance (0.19 of σ_b = 0.26 events). It is a proxy, not a PS-variation study: no alternative-shower samples exist in the package.
**S2-12 Signal PS 10 % is an assumption.** It is not derived from a variation (recoil scheme / central jet activity in VBF-like topologies is typically O(10 %); no reference number was extracted in this run).
**S2-13 Not modelled:** pile-up, trigger, b-tag scale factors, JES on MET, and the κ-dependence of BR(H→γγ) (07 coupling). The theory for fake classes uses prompt-analogue proxies.

## Gate 07 (sensitivity, couplings)
**S2-14 Exact-Poisson CLs discreteness.** With a median n_obs of 1–2 at 500/1000 fb⁻¹, μ95 is coarse and occasionally non-monotonic (cut-based 500 a: syst 5.07 < stat 6.10; j→γ-high variant 3.44 < nominal 3.50). The fit μ95 (asymptotic CLs, continuous) is given alongside; it is approximate at O(1–10) events.
**S2-15 Coupling interpretation is rate-only with BR(H→γγ) fixed to SM.** The λ_WZ < 0 exclusion is set by the boundary λ → 0⁻. λ_WZ = −1 is excluded by its 5× larger rate (4.2σ at 500 fb⁻¹). Including the W-loop κ_γ dependence would strengthen it further, and was not used. QCD WH scales as κ_W², and other Higgs backgrounds (tHq, tt̄H, ZH) are held fixed. The quadratic form closes on the independent points within 2σ (kap_W15_Z075: 3.83 predicted vs 3.90 ± 0.03).
**S3-7** Asymptotic fit significance and counting Z(σ_b) agree within 0.05 at 500 fb⁻¹ (0.90 vs 0.91, def. a), as expected for a window-dominated fit.

## Process / protocol
**S3-8 Isolation note.** A repository-wide `git status`/`git diff --stat` (run to check this run's changes) printed file *names* of other runs' modified files (multi_r1 reports/scripts, combination/). No content was opened. Later git commands were restricted to `runs/single_r1`.
**S3-9 Batch.** The first ntuple cluster (913314) failed for multi-mode jobs because condor's `queue … from` splits comma arguments; it was removed and resubmitted (913320). The 4 outputs it had written are complete and SHA-verified. The own EW W⁻γγjj validation gridpack retry (912997) failed again on the same survey channel (same seed, deterministic). It was not retried, since the canonical `B_EW_Waajj_nomjj` covers both charges (03 addendum).
**S3-10** The test-job seed 2442001 of `H_ggF_jj_nomjj` is not part of the production sample. N = 59 945 (some gridpack jobs returned fewer than 2000 events) ≥ N_req = 50 000.

## Overclaim check
All results are expected (Asimov) values at Delphes level from LO MC. "PASS" means the phase deliverables exist and the executed checks passed. No observed significance is claimed. The headline significance is BDT-based, with marginal stability (S1-9), and is always paired with the cut-based value.

## Verdict
05 PASS with S1-9/S1-10; 06 PASS with S1-11; 07 PASS (expected results). The final WH result stands, conditional on the BDT stability caveat. A human referee may prefer the cut-based numbers (Z Eq. 1 = 0.58 / 1.41 at 500 / 3000 fb⁻¹, def. a) as the conservative headline.
