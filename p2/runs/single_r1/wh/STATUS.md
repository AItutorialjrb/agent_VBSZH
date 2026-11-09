# single_r1 WH STATUS (≤ 25 lines) — 2026-11-09
Done: P01 signal definition (4F-jet EW W±Hjj (0,4); orders/diagrams closed; W BR WF = 0.9601 closed, pull −0.5; σ(signal) = 13.83 fb → 0.0301 fb after WF·BGG).
Done: P02 ledger (23 components + 4 frozen-ZH reuses with coverage proof; overlap contract; fake scenarios; pilot bounds = LOWER bounds).
Done: P03 for 16/21 sample types: σ closure (hp, pull 0.8), PY8/LHE closure, BR closure, Delphes object validation, 16 clean test jobs.
Running: condor 900134.4/.5 (EW W±γγjj gridpacks, ETA ~6–10 h), .6/.7 (QCD Wγγjj + twin, ~1 h), .12 (tt̄γγ); tests 900136.4–7, .12 held until gridpacks.
Blockers: none technical; Phase 03 final needs the heavy samples.
Decisions needed:
 D-WH-1 signal jet flavour: 4F jets (rec.) vs 5F with $ t t~ vs 5F full (5F = 2.08 × 4F, resonant tHq).
 D-WH-2 N_MC rule for parametrised-fake samples (W+jj 7.5e8, tt̄ 8e8 needed): adopt HH effective-N / truth-weighting policy for WH fakes?
 D-WH-3 frozen ZH samples below N_req (ggZH, ZH→ττ, EW Zγγjj splits): extend in canonical production vs MC-stat nuisance.
 D-WH-4 electron efficiency (stock Delphes 0.63/0.50): adopt the ZH-final CMS-like object efficiencies for VH consistency?
Self-review: reviews/wh_01-03_self_review.md (6 sev-1, 7 sev-2, 5 sev-3).
Next: finish heavy samples → update 02/03 → G1.
