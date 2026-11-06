# Review WH G2-RECHECK (04_production_plan.md, regenerated 2026-11-06T14:52Z), multi_r1. Reviewer (opus), 2026-11-06 UTC. Read-only.
Paths are relative to p2/runs/multi_r1/. Numbers, exit codes and seeds are left to the verifier. Severity: 1 = changes a result or breaks a binding rule; 2 = fix before Phase 05 yields; 3 = minor.

## Severity 1
1. [1] **Q_aajj breaks the binding N rule, and the code hides it.** D31 (SPEC.md:137) and brief_wh.md:13 require full N = 1.13e7 if it fits. It does: about 27 GB and 265 core-h (wh/reports/04:166), against 58 of 200 GB planned (04:68). The plan has 331k (04:47). make_plan.py:123 drops Q_aajj, H_VBFH_jj and H_ggF_jj from nmc_check. Yet 04:71 prints "PASS (30 rows)" and 04:78 says "Exceptions: none besides D-WH-2". 04:166 still carries option A, which no human approved. This is the silent relaxation that SPEC.md:20 (§1.5) forbids. Fix: plan Q_aajj at full N and put the three rows back into nmc_check. No human is needed, because D-WH-15 applies only if full N is infeasible.
2. [1] **Every sample where one reco jet is converted needs a third jet that the ME does not provide.** In both pilots, one jet becomes the photon or the lepton, and the two tag jets come from the remaining jets (wh/scripts/fakefactor_pilot_w.py:69-81, fakelep_pilot.py:29-31). F_QCD_Wajj_nomjj, F_EW_Wajj_nomjj, Q_aajj and VBF H are 2-parton LO MEs (04:36-38, 04:47-49). So every weighted SR event contains at least one parton-shower jet.
   - The PS uncertainty in §6b (±15-45 %, 04:134) comes from twins selected without the converted jet (04:38), so it understates the effect.
   - F_QCD_Wajj is the largest background at test level, 3.0 events against 0.9 signal (04:140), and costs 894 core-h and 43 GB. The 2-fake classes already use ME jets (D27), so the treatment is inconsistent.
   - Condition: apply the D29 rule (SPEC.md:135) to these rows. Use an ME+1-jet model (Wγ+3j or MLM Wγ+2,3j; γγ+3j for Q_aajj), or a 100 % PS uncertainty on the whole yield for rows below 10 % of the background. Hold bulk production of F_QCD_Wajj_nomjj, F_EW_Wajj_nomjj and Q_aajj until this is fixed. tt̄γ (≥4 ME partons) is unaffected.

## Severity 2
3. [2] **Stale "decisions needed" text reads as open decisions under D20.** 04:14 says D-WH-4 is BLOCKED and 04:18 says D9 is "to be confirmed". 04:157-168 lists D-WH-10/11/12/13, D9 and D31 option A as open. 04:3 and 04:64 list gridpacks as pending although they have finished. This conflicts with 04:194 (D28 closed) and with STATUS ("none"). Regenerate.
4. [2] **The fake-photon rate is called "Delphes-calibrated" (04:12, config/sample_matrix.yaml:628), but the code uses an assumed fixed form,** F0·(pT/50)^-0.5 ×2 in the endcap (fakefactor_pilot_w.py:18,47). Label it as an assumption. Measure the direct Delphes j→γ rate and put it in FORMAT.md (brief_wh.md:50). Under A2, single_r1 sees only FORMAT.md, so the D32 direct-fake cross-check depends on this.
5. [2] **Non-prompt leptons.**
   - fakelep_pilot.py:27 vetoes every real lepton with pT > 10, so the direct Delphes non-prompt component is thrown away, not kept as the D32 cross-check.
   - It is not stated whether one f_ℓ covers e+μ or each flavour; this is a factor 2 on the nominal.
   - The cited ATLAS 1110.3174 covers electrons only (04:188). Muons and heavy flavour rest on an order-of-magnitude check (04:193).
6. [2] **H_ggF_jj is LO loop-induced with no K-factor (04:143).** Pre-declare a normalisation uncertainty. The fallback D-WH-14 (04:203) becomes a human decision if it triggers. The row must not block the others.
7. [2] **wh_G2 item 2 is only half done.** ZH_Zajj_eFake still uses C = 1.866 with a syst of about 87 %, from 200k events of the frozen F_QCD_llajj_nomjj (04:87; wh/work/ratioC_ZH_Zajj_QCD.json). The plan never states that sample's full N against about 2.6M. If its N is sufficient, use it as nominal.

## Severity 3
8. [3] **Coupling fits.** The κ scaling of the H-bearing backgrounds is not declared (H_QCD_WH, ZH lost-lepton, ggZH κ_t-κ_Z, VBF H; 04:171-178). c_A has 3 points for 3 parameters, so there is no leave-one-out closure (04:177).
9. [3] **I/S is given at LHE parton-VBS level (04:78), not at the SR proxy (wh_G2 8).** This is acceptable as a signed systematic.
10. [3] **Stale labels:** "cluster ?" at 04:47-59, "not computed here" at 04:83-85, "previous design target (30)" at 04:183.

## wh_G2 items and pending rows
**Resolved:**
- Items 3, 4, 5 (+105 %, 04:137), 6, 8, 9 (04:188, 04:194), 10, 11 (04:189) and 12 (04:190).
- B_EW_Waajj_nomjj (twin 1.56 ± 0.20 %, C = 1.026; 04:202) and V_ZZa_WH (04:200-201), including the EW twin result.
- The coupling samples: effective couplings are 0, the λ = 1 closure is +0.7 %, and the quadratic closure holds (04:197-199).

**Partly resolved:** item 1 (see 1 and 2), item 2 (see 7), item 7 (see 2) and item 13 (see 10).

**Verdict: APPROVE-with-conditions, not auto-passable under D20 (sev-1 items 1 and 2).** Bulk production may start for all rows except F_QCD_Wajj_nomjj, F_EW_Wajj_nomjj, Q_aajj and H_ggF_jj (pending). Items 1 and 2 need executor fixes and a reviewer check, not a human decision. A human is needed only if the ME+1-jet samples exceed 200 GB or D-WH-14 triggers.

## Recheck 2 (2026-11-06 UTC, focused: 04 §15 + measured j→γ rate; numbers left to VERIFY #15)
1. [1] **The fake rows are now dominant, but they are still sized for a subleading background.** F_Wjjjj gives 24.8 of 56.8 PEAK events at N = 59 000, with projected N_eff 92 (50 at the 95 % lower bound; 04:39, 04:73). That is about 0.27 events per effective event against S ≈ 0.9 (04:§15(3)). After the Phase 05/07 cuts and K = 5 folds, the MC statistics of B will exceed S. The 10·K rule (04:74) was set when these rows were 1.15 events. Fix before Phase 05: size F_Wjjjj and T_ttjj_1l (12.9 events, N_eff 197) so that σ_MC(B) in the tightest pre-declared region is well below S. This is cheap: F_Wjjjj costs 5.6 core-h per 59k events. Add a top-up with new seeds; nothing already produced is lost.
2. [1, unverified] **The measured rate may double-count real photons.** The numerator is any reco Photon within ΔR<0.2 of a GenJet, in events with n_prompt_photons==0, "incl. FSR in jets" (scripts/jet_to_photon_rate.py:3,24-34). If GenTruth does not count quark-FSR photons as prompt, the rate contains real photons that the Wγjj/Wγγjj ME rows already model. That inflates the dominant background. Check the parent ID of the matched photons (hadron decay vs parton FSR) before the rate is used in Phase 05. I could not read the GenTruth definition, which lies outside this run.
3. [2] **The rate is pooled across processes, but the dominant rows are W+jets.** W/tt̄ differs by 1.1-3.0× (04:§15(3)), yet only the half-difference is carried (jet_to_photon_rate.py:39). The W rate is up to 1.6× the pooled one, which becomes 2.5× for the 2-fake F_Wjjjj. Use the class-specific rate as nominal, or the full difference, squared for 2-fake rows.
4. [2] **The rate is binned in GenJet pT but applied to reco Jet pT** (jet_to_photon_rate.py:22-27 vs fakefactor_pilot_w.py:29,94). Some bins have 14-29 counts. Declare the jet-scale effect.
5. [2] **The direct-fake closure is in-sample.** The rate comes from the F_Wjjjj/T_ttjj_1l/F_Wjj_pilot/T_tt_1l test files (work/jgamma_rate.json), the same files as the pilots. Pre-declare a disjoint split of the production files: measure on one half, close on the other in a loose region with enough direct fakes. Do this before any re-measurement (04:§15(3) "re-measured on the production files").
6. [2] **The Q_aajj D29 outcome is fragile.** The upper-bracket value of 3.6 events comes from 3 raw events; its 95 % upper bound of about 7.6 is 13 % of 56.8. The denominator includes F_QCD 15.0 from 1 raw event (04:201-203). Re-run D29 on the production yields. Use the γγ+3j test (893599) as the comparison and switch to ME+1j if the fraction exceeds 10 %.
7. [3] **Stale text.** 04:3 says "No bulk production has been submitted". §6d still quotes the assumed-rate yields (3.0/0.15/1.15 events, f0 = 10⁻³). Regenerate.
**Recheck-1 items:** 1 is resolved (04:47, 04:71). Item 2 is resolved by the D29 evaluation (04:§15(2)). Item 7 is answered; C stays, with an 87 % systematic (04:§15(5)).
**Verdicts:** F_EW_Wajj_nomjj **APPROVE** (0.89 events, ≤ 3 % even at the 95 % upper bound; 100 % PS). Q_aajj **APPROVE-with-conditions** (item 6; the full-N 2-jet sample is needed either way). F_QCD_Wajj_nomjj **HOLD** until the ME+1j comparison exists. Items 1-2 are new sev-1s for production design, fixable by the executor; no human decision is needed unless the item-1 top-up pushes storage above 200 GB.
