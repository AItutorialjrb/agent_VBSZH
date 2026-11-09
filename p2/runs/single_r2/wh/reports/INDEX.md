# WH reports — run single_r2 (single-agent arm)
| phase | report | status | date UTC |
|---|---|---|---|
| 01 signal definition | [01_signal_definition.md](01_signal_definition.md) | PASS (decisions D-WH-1..3 open, defaults applied) | 2026-11-08/09 |
| 02 background & overlap ledger | [02_background_overlap.md](02_background_overlap.md) | PASS as design; open: continuum sigma, D-WH-4..6 | 2026-11-09 |
| 03 generation validation | [03_generation_validation.md](03_generation_validation.md) | BLOCKED (partial): continuum pending; 4 sample types PASS | 2026-11-09 |
| G1 self-review | [G1_self_review.md](G1_self_review.md) | not ready for G2 (4 sev-1) | 2026-11-09 |
Evidence: ../config/xsec_br_ledger.json, ../work/{smoke,gp_condor,condor_test,validation} (work/ is git-ignored, on EOS), ../figures/.
Git commit: the commit that adds this file (`git log -- p2/runs/single_r2/wh/reports/INDEX.md`).
