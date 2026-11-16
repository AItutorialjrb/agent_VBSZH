# verify_R2_paper (haiku verifier, FINAL-R2, 2026-11-16) — saved verbatim by the orchestrator (verifier is read-only)
VERDICT: FAIL (sev-1: 1)
Check 1: 530/530 registry entries traced and matched (395 json key, 90 SAMPLES.csv, 24 kappa extents recomputed, 16 ZH cutflow sums, 6 zh.comp, 8 pub.*, 1 closed form). Toy vs asymptotic present with N toys.
Check 2 missing/partial: (a) VH ranking not delivered and not stated; (b) ZH lepton non-prompt scan/class absent; (c) ZH cutflow frozen only; (d) kappa at 1000 missing; (e) VH Eq.1 column absent; (f) D49 upper end absent.
Check 3: 16/16 compile (recompiled standalone), 0 missing. Check 4: 9 figure pairs valid; regenerate.sh documented (not run). Check 5: only f_mu limitation stated.
1. [sev-1] D50/D49 upper-end Z and mu95 not in package; T3 says "D49 INTERIM (open)" and quotes 68% [0.021,0.40] instead of 95% [0.0031,0.675] — paper/tables/T3_composition_WH.tex
2. [sev-2] VH ranking absence not stated in T5 captions.
3. [sev-2] D47(3) limitations (calibration mismatch, other-Higgs not rescaled, no Zγ+3j in ZH) absent from package.
4. [sev-2] kappa at 1000 fb^-1 missing (make_paper.py loops 500,3000; couplings_vh_L1000_v12.json exists).
5. [sev-2] ZH non-prompt-lepton class absent / "expected negligible" without MC support.
6. [sev-2] ZH cutflow is frozen basis; corrected only for fake rows.
7. [sev-2] T4 WH nominal 0.438/6.64 (joint) vs T5_WH/T6 0.428/6.81 (stand-alone); basis not stated.
8. [sev-2] kW-sign values lack convention next to the number (T9, T10, T7 label).
9. [sev-2] T5_ZH caption "frozen-code" but corrected values; b-uncertainty not Z0/mu95 impact.
10. [sev-3] unregistered literals: 0.5196, 0.4687 (T2_ZH), 0.021/0.40 (T3), 2.45 (T7), f_mu 2e-5, toy counts, cut constants; README claim not literal.
11. [sev-3] T3_WH raw signal 8157 vs selection_v12.json 8158.
12. [sev-3] ZH toy Z0=0 is clipped negative (-0.46), not stated in T10.
13. [sev-3] grid-edge intervals shown as bounded (T7b ZH kZ/kW, T8 c_A clip).
14. [sev-3] Eq.1 undefined in package.
15. [sev-3] T10 WH mu95 toy 8.38±1.11 vs 6.64 (+26 %, ~1.6σ) called "consistent"; CLs non-monotonic.
16. [sev-3] CMS PLB 860 (2025) volume/year not in stored PDF text (DOI is).
17. [sev-3] kappa/lambda figures 500 only.
18. [sev-3] T1 k column factors undefined in table; σ pre-decay not labelled.
19. [sev-3] D46 range (5.1-7.1) not given, 6.20 only.
