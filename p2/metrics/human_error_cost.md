# Human-error cost (excluded from per-run metrics)
Report these separately in AI_results.md. Do not count them in any run's token/time/cost totals.

| utc | run | event | transcripts / sessions | treatment |
|---|---|---|---|---|
| ~2026-11-08T20:15Z | single_r1 | launched twice; both sessions stopped by the human; outputs moved to p2/_to_delete/single_r1_dup_20261108 | the two duplicate single_r1 sessions of ~20:15Z (session IDs to be identified from metrics/raw/claude/single_r1/ by start time when parsing) | excluded from single_r1 metrics; counted here as human-error cost; single_r1 relaunched clean afterwards |
| 2026-11-08T20:29:58Z | multi_r1 (session 2c106b12-2d30-41fb-b453-fd56bc82a4cd) | multi_r2 start prompt pasted into the multi_r1 orchestrator session | one turn in the multi_r1 session (no tool work beyond logging) | not acted on; the turn's tokens are counted as human-error cost, not multi_r1 work, where separable |
