# WH selection (05), focused review (reviewer, opus, read-only; 2026-11-09; recorded by orchestrator)
**Verdict: HOLD on adopting the MVA as primary.** The cut-based selection may proceed to statistics with conditions.

1. [sev-1] **m_gg leaks into the BDT.** pt1, pt2, ptgg and drgg rebuild m_gg exactly (median error 2e-5 GeV). The BDT sculpts the background m_gg: background efficiency is 0.10-0.15 in 120-128 against ≈0.06-0.10 in the sidebands. This breaks the sideband/m_gg PL fit and pre-declaration item 10.
   - Fix: use pT/m_gg ratios or drop the redundant input; retrain; show the sideband shape is flat versus score.
2. [sev-2] **Threshold optimism is small but must be built into the method.**
   - Nested check (threshold on 4 folds, applied to the 5th): Z = 0.615 vs 0.619.
   - The optimism is MC-stat driven: b N_eff 139, ±8.5 %.
   - Implement the nested procedure in sel_mva.py/sel_final.py and quote its Z.
3. [sev-2] **Reading "stable" as RMS is post-hoc.** §0 says "spread < 10 %" and the fold range is 19 %. Log it as a deviation and replace it with a metric fixed in advance.
4. [sev-2] **The |Δη| grid edge binds.** Δη>4.5 gives Z 0.457, so the cut-based reference is under-optimised by ≥5 % and the MVA gain is ≈+35 %, not +42 %. State this.
5. [sev-2] **Cut-based b = 1.793 has N_eff 134** (MC stat 8.6 %); the 10 largest weights carry 19 % of the MVA b. Barlow-Beeston is mandatory in 07.
6. [sev-2] **Silent missing or zero-support rows.**
   - H_ggF_jj is skipped without a log line.
   - Heavy flavour enters at 0 raw (use the factorised nominal).
   - V_WWa UL 0.467.
   Carry all of these as variants and name them in §2.
7. [sev-2] **Weights match 05a v2.1 VBS** (b 66.28). One unexplained difference: non-prompt 0.803 vs 0.8433.
8. [sev-2] **The loose v1.1 sample and H_ggF_jj will change the training mix** (eFake QCD part is 17.4 of 66.3). Pre-declare now:
   - models and cuts frozen, re-evaluated only;
   - a retraining trigger (e.g. >30 % change in the lost-lepton or non-prompt share of b), retraining only with nested CV;
   - whether the primary is re-decided at that point.
9. [sev-2] **Pre-declaration integrity cannot be verified.**
   - §0 time equals the scan-script mtime; the files are untracked.
   - 05a:3 contradicts the logs.
   - The selection ran on v2.1 before its recheck.
   Commit now, and state that §0 was not committed before the scan. Blinding is fine.
10. [sev-3] Small issues:
    - fold N_eff quoted as 19-67 vs 19-63;
    - 05a still quotes C 0.958 while the code uses 1.016;
    - |w| training on negative weights is unstated;
    - the fold hash reduces to evt mod 5.

**Human questions:**
- (a) Does "stable" in D32 mean fold RMS, fold range, or MC-stat compatibility?
- (b) Is retraining allowed after the loose and H_ggF_jj samples arrive?
