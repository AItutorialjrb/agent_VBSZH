# single_r1 / WH — report index
| Phase | Report | Status | Updated (UTC) |
|---|---|---|---|
| 01 | [01_signal_definition.md](01_signal_definition.md) | PASS (D-WH-1 open) | 2026-11-09 |
| 02 | [02_background_overlap.md](02_background_overlap.md) | PASS as ledger; S1 caveats (fake-sample design, fake-ℓ size); D-WH-2/3/4 open | 2026-11-09 |
| 03 | [03_generation_validation.md](03_generation_validation.md) | PASS for 16/21 sample types; heavy continuum pending | 2026-11-09 |
| G1 | [../../reviews/wh_01-03_self_review.md](../../reviews/wh_01-03_self_review.md) | self-review (referee mode) | 2026-11-09 |

Evidence: `wh/work/p03/{xsec.json,xsec_table.md,delphes_validation.json,egamma_pilot.json,bounds_table.md,test_audit.md}`, `wh/figures/p03_signal_validation.{png,pdf}`, `wh/config/samples.yaml`, `wh/cards/`, `wh/patches/`. Work outputs (`wh/work/`) are git-ignored (p2/.gitignore), so the md/json evidence files are copied to `wh/reports/evidence/` at each commit.
Git commits: listed in `wh/PROGRESS.md`.
