# WH production-validation review before wh-prod-v1 (reviewer, opus, read-only; 2026-11-07; recorded by orchestrator)
**Verdict: HOLD.** Items 1-2 are sev-1 and there is an open human question (H1); D20 auto-pass does not apply.

**Decisions:**
- **Q1 Q_aajj.** The pre-declared rule (04:256, recheck 2/3) tests at f_ℓ = 2×10⁻³; at that point the fraction is 28 %, so (A) is required. (B) would change the rule after the result is known. No human needed: 115 + 13.9 = 129 GB < 200 (D31).
- **Q2 Validity.** No file is invalid; the direct fakes, e→γ objects and non-prompt leptons are all in the Delphes output. The isolated non-prompt photon origin must be diagnosed on the existing files before the tag, because it decides which production row is needed (item 2).
- **Q3 Conflict with D32.** Making direct counts nominal reverses D32 item 1 / D4, so it needs a human (H1). Under A2, FORMAT.md must not state a nominal method.
- **Q4 Package.** Not neutral yet (items 3-6).
- **Q5 Other sev-1s.** None beyond items 1-2.

**Findings:**
1. [1] Submit Q_aajjj (5.24M) under the ≥3-jet condition and keep Q_aajj as a cross-check; add the row; log it in SPEC §7; re-run the N rule. With the fake-factor denominator (~6.4 events) the fraction is still >25 %.
2. [1] Direct-count nominal breaks the basis for withdrawing the 2-jet row.
   - The ≥3-jet rule assumes the fake photon consumes a jet, but 93 % of the direct non-prompt photons are not in a jet (04:273). For those the withdrawn 2j Wγjj (5.68 pb) is the right sample and the 3j row undercounts. "F_QCD_Wajjj at 11 %" holds only under the direct method (2.6 % under the fake factor).
   - Identify the photon origin on existing files before the tag: state whether `Particle` is kept (card :787, not in FORMAT.md:12).
   - 33 % of the photons are >ΔR 1.5 from any GenJet; suspected artefact (GenJet "not dominated by photon" exclusion, Delphes hadron→photon deposit, or a matching/entry-order bug).
3. [2] FORMAT.md states a nominal method and results (A2 forbids).
   - Remove the recipe/result content at :27, :28, :49, :51, :71.
   - Keep the rate tables, the per-event rate and the 7 %-within-ΔR<0.2 fact as data.
   - Human rules only as cited constraints.
4. [2] FORMAT.md:17 "|w| = σ" is false for the matched rows (H_QCD_WH_mlm Σw/N_Delphes 0.879 vs σ 0.3023; H_ZH_tautau_wh 0.0761 vs 0.02535). Σw/(N_gen·σ) = 0.981: state the 1.9 % offset.
5. [2] Missing convention: the WeightLHEF index → (μR, μF)/PDF mapping, needed for the D27 envelopes.
6. [2] The frozen ZH rows are outside the package, but A2 lets single_r1 read only the package, and e→γ is 4-15 % (not 1-5 %). Add these rows (path, σ, k, N, read-only) or state that they are excluded for both runs.
7. [2] The two-fake estimate (per-jet factor squared, ×28) is unsupported. F_Wjjjj direct 0 has a 95 % UL ≈ 32 events against 7.2 total, so the 7.2 denominator is uncertain.
8. [2] H_ggF_jj (a D31 row) is pending. Wait for it, or tag v1 explicitly without it (v1.1 later; D-WH-14 if it fails).
9. [2] The three dropped F_Wjjjj chunks are not in SPEC §7 (now logged by the orchestrator). 04:268 "list (empty)" contradicts 04:271.
10. [3] Small fixes:
    - Poisson intervals for the small direct counts.
    - F_Wjjjj N_eff mismatch (40 522 vs 63 434).
    - Label x~N(0.85, 0.1) as an uncited assumption.
    - Log the (iii)/(vi) deviations.

**Human question H1 (D32 item 1 / D4).** The per-jet j→γ rate covers only ~7 % of the Delphes non-prompt photons, and the closure is off by ×5. What should the one-fake estimate be?
- (a) Keep the fake factor nominal, with the direct count as a cross-check and the ×5 non-closure as a systematic.
- (b) Direct count nominal (a deviation); restore the 2j F_QCD_Wajj_nomjj at full N (D30, ~43 GB, total ~172 GB) with an exclusive in-jet / not-in-jet split.
- (c) Decide after the origin diagnosis (item 2). **Reviewer recommends (c).**

## Recheck (reviewer, opus, read-only; 2026-11-07; recorded by orchestrator)
**Verdict: APPROVE-with-conditions for wh-prod-v1.** The tag can go ahead now; H1 can be decided after the tag (no option blocks it). Before tagging, fix R1-R4 (docs only, no ROOT change); R5-R7 may follow.

**Items 1-10:** 1, 3, 4, 5, 7 and 10 are resolved (Q_aajjj delivered; SHA256SUMS 2688 = 2688 ROOT files).
- R1 [2] 04 says "no electronic noise in the card". Wrong: the ECal constant term is 0.40 GeV (card :304), log-normal smearing, and the EnergyMin/significance cuts come after smearing.
- R2 [2] 04:274 "direct Delphes count … is the nominal estimate" contradicts "NO CHOICE MADE". Supersede it.
- R3 [2] The frozen ZH rows in SAMPLES.csv point to the ZH report for the weight convention and have empty sum_weights. State the normalisation in the package (A2).
- R4 [2] FORMAT.md lists Photon.Particles but does not say `Particle` is absent from the slim files.
- R5 [3] F_QCD_Wajjj_nomjj / Q_aajjj are not "inclusive": 3 ME partons pT>20 and no 2j+PS component. State it as a generator fact.
- R6 [3] SPEC §7 lacks the Q_aajjj replacement and the (iii)/(vi) deviations (orchestrator).
- R7 [3] Pin the Delphes and Pythia 8 versions in FORMAT.md.

**Neutrality:** OK apart from the above; FORMAT.md:68 "(medium, nominal)" is acceptable only as a D28 quote.

**Diagnosis:**
- 11/16 has a 95 % interval of ~44-86 %: a coarse estimate, mechanism unproven.
- Likely the log-normal ECal tail: 0.01-0.1 GeV towers have P(>25 GeV) ~1-2e-5, so O(1e-4)/event. This fits the flat ME-jet dependence and the back-to-back-with-MET pattern.
- Test: sum the true E of Photon.Particles vs the reco E on *_full.root.
- Not physical: it is Delphes-specific and should be flagged and excluded, or shown as a labelled upper-bound scenario. The HCal has a similar tail (a limitation).
- No new sample is needed before the tag. An analysis-phase GenTruth veto is possible (gph_* within ΔR<0.1).

**H1 (human):** "Should Delphes reco photons with no generator photon (pT>10) within ΔR<0.1 (≈70 % of non-prompt photons, probably a log-normal ECal-tail artefact) count as background, and which one-fake estimate is nominal?"
- (a) Fake factor nominal, direct count as cross-check, ×5.3 non-closure as a systematic. F_QCD PEAK 0.16 (≈0.8 with ×5). 0 GB. Consistent with D32/D4.
- (b) Direct count including the artefact, and restore the 2j row. ≈1.3 events; +42.7 GB (≈171 total), 578-894 core-h. Deviates from D32 item 1 and reverses "D29 supersedes D30".
- (b') Veto the artefact with GenTruth; in-jet direct count nominal (≈0.23 ± 0.10), fake factor as cross-check, 0.79 (UL95 1.66) as an upper-bound scenario. 0 GB (+ optional ~10 core-h / 2 GB diagnostic with Particle kept). Deviation: nominal method of D32 item 1. **Reviewer recommends (b').**

**H_ggF_jj:** tag v1 without it; v1.1 later.
- Tell single_r1 that v1.1 adds rows (H_ggF_jj, and the 2j row if H1=(b)).
- Regenerate SHA256SUMS at v1.1.
- D-WH-14 if the gridpack fails.
- Its yield is not to be assumed negligible meanwhile.
