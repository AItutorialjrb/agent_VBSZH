# WH background model (05a), focused review (reviewer, opus, read-only; 2026-11-09; recorded by orchestrator)
**Verdict: HOLD.** Items 1-3 are sev-1 and executor-fixable.

## Sev-1
1. **Multi-directory frozen ZH rows are normalised wrongly.** bgmodel.py:14,22 groups N_gen by dirname, but skim.py:147 stores bare filenames, so each directory is normalised by the combined N.
   - ZH_Zajj_eFake EW part: 13× low. ZH_Zaajj_EW_lostlep: 3× low.
   - Corrected PEAK: eFake 1.137 → 2.41; Zaajj_EW 0.040 → 0.119. PRE eFake 15.8 → 27.4.
   - Check: corrected Σw/N = 0.0804 pb vs SAMPLES 0.0805.
2. **Missing C factors are an error, not a caveat.**
   - C = 1.866 (Zajj QCD) and 0.958 (Zaajj EW) were measured at the WH reco-SR proxy (mjj>500, |Δη|>2.5), the same phase space as VBS/PEAK, and are pre-declared in 04:89 and §15(7).
   - Lost-lepton/e→γ at PEAK: 1.33 → ≈2.79 (normalisation fix) → ≈3.84 (+C), with ≈±1.8 from the 87 % C systematic.
   - PEAK b: ≈7.6 → ≈10.1.
   - PRE needs its own twin ratio or a stated bound.
3. **D35 is violated.** The light-misID high bound uses the loose 2e-3 (bg_yields.py:8,23-24), which D35 says is not an upper bound (PEAK high 7.87). The deviation is not logged.
   - Use ×3 (D36) for the high bound and ×0.3 for the low bound. Electron-only is not a lower bound.
   - 2e-4 and 2e-3 survive only as labelled robustness variants. The ×100 scan must be labelled as beyond D36.

## Sev-2
4. **Fake-photon non-closure is significant.** PRE: 6 raw vs 15.3 expected (P = 0.006). VBS: 3 vs 7.4 (P = 0.06). Ratio ≈0.39 (0.24-0.63). Add a one-sided ≈−60 % non-closure systematic (≈2 % of PEAK b; the overprediction is conservative).
5. **The D39 ±20 % floor is not in the bounds.** It must be a declared nuisance. c = 1 is acceptable while D39 is open.
6. **"No 2j row" holds for the nominal only.**
   - The 3j generator-cut safety for the converted jet is asserted, not shown.
   - Artefacts lie outside jets, so the 3j-only direct count is a lower limit on the upper variation; label it.
7. **HF direct at PEAK: 0 raw, UL 0.474 + 0.283 vs nominal 0.079.** Add a factorised variant (≈0.05 ± 100 %) and keep the UL as the conservative variant.
8. **f_μ = 2e-5 (D40) is only a flagged interim default.** Delphes has no hadron→μ fakes. The Q_aajjj D29 trigger was evaluated at f = 2e-3; at the D35 nominal it would not fire. Harmless, but log it.
9. **Deferred items:** the D29 100 % PS uncertainty on V_* (PEAK UL sum 0.65), the D27 two-fake ×{0.09,1,9} and the C systematic must be pre-declared in 05 before the yields are fixed. H_ggF_jj must enter (v1.1 or D38 UL) before statistics.

## Sev-3
10. Fixes needed:
    - zero-support ULs are dropped from the direct-count variation (bg_yields.py:84);
    - r_τ (W) is applied to Z lost-lepton rows without comment;
    - 05a:3 gives no commit hash.
    The veto validation is adequate (0/123, UL95 2.4 %).
11. **Correct:** BR applied once; raw N, N_eff and MC stat per row; the 2.996 × weight UL; τ [1, 1+2r_τ]; the two-fake UL cross-check.

**Conditions to lift the HOLD:** fix 1-3; re-run and reissue 05a; log 3 and 8 in SPEC §7; pre-declare 4, 5 and 9 as nuisances.

**Human questions:**
- (a) D35 high bound: ×3 (D36) or medium WP 2e-4?
- (b) D40 cited muon value, or accept the placeholder with a wider scan?
- (c) PRE: replace C by the 2.4M ZH_Zajj nomjj top-up (≈125 core-h)?

## Recheck (05a v2; reviewer, opus, read-only; 2026-11-09; recorded by orchestrator)
**Verdict: APPROVE-with-conditions.** PEAK b = 10.0 vs S = 0.99. Sev-1 items 1-3 are resolved.

**Earlier items:**
- 4. The ×0.4 on the LOW bound is the right direction; state in §2 that the nominal is deliberately high (~2.5×).
- 5. Minor: the two-fake ±20 % should follow c² (−36 %/+44 %).
- 7. Use the factorised HF 0.055 as the PEAK nominal (no nominal 0 from zero MC support).
- 2. The PRE C high bound max(1,C) is not shown to be an upper bound; label it a stated bound (D42).
- 10. r_τ on the Z rows is not justified in §5; commit hash still missing.

**New findings:**
- N1 [sev-1 for statistics]: two systematics declared in 04 are missing from the nuisance list:
  - +105 % one-sided lepton-acceptance coverage on the lost-lepton part of ZH_Zajj_eFake (04:139, :181);
  - 100 % PS-jet-fraction (~±45 % of yield) on the QCD-type rows: B_QCD_Waajj, the eFake QCD part, ZH_Zaajj_QCD, T_tta, Q_aajj (04:136).
  State the overlap/correlation with the C systematic.
- N2 [sev-3]: the eFake EW part uses C = 1 (not measured; the W proxy gives ≈1.025), and Zaajj EW uses C = 0.958 < 1 (unphysical for a nomjj ⊃ vbs; its twin loss of 1.56 % gives ≈1.016). Harmonise the EW parts to C ≥ 1 from the loss fractions.

**Conditions before statistics:**
- (a) N1;
- (b) H_ggF_jj via v1.1 or the D38 UL;
- (c) D39-D43 answered, or their defaults run as switches;
- (d) PRE C label, r_τ justification, commit hash;
- (e) block regions redone on the final selection, with the sidebands blind;
- (f) the PEAK UL sums (V_* 0.65, non-prompt 0.76, direct 0.97) as sensitivity variants.

**New question:** does the +105 % eFake lepton-coverage bound trigger the pre-declared 04:139 rule (>10 % of SR background → dedicated loose-cut sample)? Split eFake into its e→γ and lost-lepton parts first.
