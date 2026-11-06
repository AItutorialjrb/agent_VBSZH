# Brief v2 — executor-wh, multi_r1: from G2 to wh-prod-v1 (orchestrator, 2026-11-06; D19)
Read this brief, not the full handoff. Binding sources, in order:
1. p2/SPEC.md §1 and §6 (D1–D10, D27–D32, A1, A2);
2. this brief;
3. reviews/wh_G2.md (its conditions are binding);
4. your STATUS.md and reports/04_production_plan.md.

Your directory is p2/runs/multi_r1/wh/. Canonical samples go to p2/production/wh/<sample>/. ZH tree, p2/lib and software/ are read-only. Reuse frozen ZH code from p2/lib (patches in wh/patches/). New installs go only under p2/software/.
The HH stream is stopped (A1): never touch hh/ or HH jobs.

## 0. Binding rules (unchanged)
- **N rule:** N_MC ≥ max(50k, σ×BR×3000 fb⁻¹), enforced loudly by code. The only exceptions are the human-approved weighted samples W+4j and tt̄jj (D4/D27: fake-factor weights, N_eff ≥ 10 in the SR, code-enforced).
  - **Non-prompt-lepton samples** (Q_aajj, H_VBFH_jj, H_ggF_jj; D31): full N within the 200 GB WH budget. If that is impossible, raise D-WH-15 and stop that row.
- **BR and yields:** BR applied once. Final yields at Delphes level only.
- **Condor:** test job before bulk; no duplicate submissions; seeds per SPEC §3.4 and checked by seeds.check on every submit file. Jobs run on schedd bigbird103.cern.ch.
- **Storage:** WH ≤ 200 GB in total, slim Delphes output.

## 1. Human answers at resume (SPEC §6)
- **D9 (τ):** S_EW_WHjj_taunu stays in b; the r_τ uplift carries ±100 %, stated per sample, including the V_*, H_ggZH_wh and frozen lost-lepton rows (wh_G2 11).
- **D10:** every sample type gets a verified test job before bulk production.
- **D27 / D-WH-10:** unbiased ME W+4j and tt̄jj with fake-factor weights. Add the LO αs⁴ scale envelope, and pre-declare the 2-fake f-scenarios ×{0.09, 1, 9} (wh_G2 12).
- **D28 / D-WH-11:** numeric jet→lepton fake rates from HEPData tables of published CMS (or ATLAS) papers, citing the record (DOI or ins number, table). If no per-jet table exists, bracket f_ℓ over a cited range and report both ends. Mind wh_G2 9: a tight-to-loose ratio is not a per-jet rate, so state the conversion explicitly.
- **D29 / D-WH-12:** an ME-jet sample only if the background's PS-based yield is > 10 % of the total SR background; otherwise 100 % PS-modelling uncertainty. Pre-declare the rule now and evaluate it on production.
- **D30 / D-WH-13:** F_QCD_Wajj_nomjj at full N (893.7 core-h, 42.7 GB).

## 2. Work to wh-prod-v1, in order
1. **Collect** the finished gridpacks, tests and twins from the resume audit (the orchestrator relays it). Finish the pending rows under the wh_G2 conditions:
   - B_EW_Waajj_nomjj: σ, N, test with LHE = Delphes count, EW twin ≤ 5 %, C for ZH_Zaajj_EW;
   - V_ZZa_WH;
   - H_ggF_jj;
   - the F_QCD_llajj_loose coverage bound;
   - fallbacks as stated in wh_G2.
2. **Coupling samples**, needed for the final scope (D32 item 4): direct samples at λWZ ∈ {−1, −0.5, 0, 0.5, 1, 1.5} and a (κW, κZ) grid, using the ZH framework (HC_NLO_X0_kVV patched model; reuse ZH cards and code from p2/lib).
   - Add the CP-odd c_A only if cheap; state the cost and the choice.
   - Each needs a gridpack, a verified test job and a plan row (N rule as for the signal).
   - Size the grid so that the per-bin quadratic fit and the leave-one-out closure are possible in every candidate binning (m_jj, pT(γγ), m(Wγγ)).
3. **Production for the final analysis** (D32): keep direct-Delphes fake photons in the fake-photon samples (no prompt-photon generator filter), so that a direct-fake cross-check of the fake-factor method is possible.
   - BDT k-fold needs disjoint training and evaluation halves. State in 04 whether the planned N supports this (N_eff per fold), and top up if not.
4. **Update 04_production_plan.md:** all rows, totals, `nmc_check` (non-empty and loud), N_eff gates, pre-declared rules (D29, f-scenarios, f_ℓ ends), and the fake-model definitions for the three non-prompt classes:
   - (a) fake photons;
   - (b) non-prompt leptons;
   - (c) e→γ and lost-lepton.
   Then write VERIFY_REQUEST and set STATUS to "READY FOR G2-RECHECK" and return. The orchestrator runs the verifier and a G2 recheck by the reviewer. Under D20 the recheck auto-passes if it has no sev-1 and no open decision.
5. **After the orchestrator says "G2 passed":** submit bulk production, one cluster per sample, no duplicates.
   - Validate it with exit codes, counts, σ closure, seeds, and a post-production `nmc_check` with measured N_eff; resubmit failures with fresh seeds.
   - Write VERIFY_REQUEST and return.
6. **Production package for wh-prod-v1** (A2: single_r1 will read only this, never your reports or code):
   - p2/production/wh/<sample>/: the slim Delphes ROOT files only (plus LHE if kept); no scripts.
   - p2/production/wh/SAMPLES.csv, one row per sample: sample, process class, s/b role, σ_pb (pre-decay) and source, BR×k factors (applied once), N_generated, N_Delphes, sum of weights, weight convention, generator cuts, seeds range, files glob, sha256 list path.
   - p2/production/wh/FORMAT.md: branch list, weight semantics, units, fake-factor inputs (the Delphes j→γ rate as data, not code), the f_ℓ range with citations, luminosities. Physics conventions only, no analysis recipe.
   - p2/production/wh/SHA256SUMS.
   - Set STATUS "PRODUCTION COMPLETE" and return. The orchestrator verifies, tags wh-prod-v1, and stops.

## 3. Not now
The final analysis (D32 items 1–6: selection, BDT, statistics, couplings, VH combination, comparison) starts only after the orchestrator relaunches you after wh-prod-v1. Design the production so that it serves those items, but do not run them.

## 4. Protocol
- **Verifier:** write VERIFY_REQUEST.md for every finished set of jobs. The orchestrator runs the verifier and relays the result.
- **STATUS.md:** ≤ 25 lines: done; running clusters (with schedd); held jobs; decisions needed (D-WH-14+); next action. Your final reply is a pointer to STATUS.md only.
- **Human decisions:** if one is needed, raise it in STATUS, stop that branch, and continue the others.
- **Waiting:** no idle polling. When only condor remains, set STATUS "waiting on clusters X (schedd)" and return; you will be resumed.
- First line of your work log: ROLE=executor-wh PHASE=PROD.
