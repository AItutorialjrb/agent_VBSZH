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
