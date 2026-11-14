Computed by `wh/scripts/my_usage.py` from this session's transcript (deduplicated by message id; prices `p2/metrics/prices.json`; cost-equivalent, not billed cost). Segments from the ledger times. Computed shortly before the final commit; the last few calls are not included.

| segment | model | API calls | input | output | cache write | cache read | cost-eq. USD | first → last call (UTC) |
|---|---|---|---|---|---|---|---|---|
| setup / G0 (before P01) | claude-opus-5-5 | 11 | 22 | 6,007 | 89,445 | 591,961 | 0.95 | 20:32:18 → 10:33:50 |
| P01–P03 → G1 | <synthetic> | 1 | 0 | 0 | 0 | 0 | 0.00 | 13:56:17 → 13:56:17 |
| P01–P03 → G1 | claude-opus-5-5 | 116 | 236 | 170,813 | 921,174 | 27,181,826 | 16.22 | 10:34:08 → 18:13:58 |
| idle at G1 (stale notifications) | claude-opus-5-5 | 2 | 6 | 2,829 | 1,375 | 738,354 | 0.22 | 18:14:18 → 18:32:03 |
| P05–P07 → FINAL (A2) | claude-opus-5-5 | 115 | 232 | 213,487 | 417,476 | 28,994,991 | 13.41 | 09:48:40 → 10:56:01 |
| **total** | | | | | | | **30.80** | |
wall (first→last transcript record): 134.40 h; active (gaps capped at 5 min): 2.77 h

transcript records with usage (dedup): 245; sidechain records: 0; first/last timestamp: 2026-11-08T20:32:16.044Z / 2026-11-14T10:56:03.478Z
