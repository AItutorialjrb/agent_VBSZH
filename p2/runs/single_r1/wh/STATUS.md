# single_r1 WH STATUS (≤ 25 lines) — 2026-11-13
Done: P01 signal definition (4F-jet EW W±Hjj (0,4); orders/diagrams closed; W BR WF = 0.9601 closed (pull −0.5); σ(signal) = 13.83 fb → 0.0301 fb after WF·BGG).
Done: P02 ledger (all classes sampled, reused with coverage proof, or bounded; fake pilots are LOWER bounds).
Done: P03 for 20/21 sample types: σ order closure (hp, pull 0.8), PY8/LHE (20), BR closure, Delphes objects, 20 clean test jobs.
Running: 912997 (EW W⁻γγjj gridpack retry; attempt 1 aborted on a corrupted survey channel), 912998 (its test, held until gridpack).
Pilot (illustrative, 500 fb⁻¹, peak window): signal 1.13; prompt Wγγjj continuum ≈ 1.8 (EW W⁺ + QCD), fakes ≈ 1 nominal.
Blockers: generator-cut safety of m_jj > 400 not demonstrated (twin ratio 0.47 ± 0.17) → production design change (no cut).
Decisions needed:
 D-WH-1 signal jet flavour: 4F jets (rec.) vs 5F with $ t t~ vs 5F full (5F = 2.08 × 4F, resonant tHq).
 D-WH-2 N_MC rule for parametrised-fake samples (W+jj 7.5e8, tt̄ 8e8 needed): adopt HH effective-N / truth-weighting for WH fakes?
 D-WH-3 frozen ZH samples below N_req (ggZH, ZH→ττ, EW Zγγjj splits): extend in canonical production vs MC-stat nuisance.
 D-WH-4 electron efficiency (stock Delphes 0.63/0.50): adopt the ZH-final CMS-like object efficiencies for VH consistency?
Self-review: reviews/wh_01-03_self_review.md (8 sev-1, 7 sev-2, 5 sev-3).
Next: G1 (human). EW W⁻γγjj retry result to be appended when it finishes.
