# single_r1 / WH — progress log (resume point for a restart)

Spec: `p2/SPEC_G0.md` (repeat runs read it in place of SPEC.md). Arm: single, no subagents. Seeds: 2 400 000 + 1000·idx + J.

| UTC | item | state | evidence |
|---|---|---|---|
| 2026-11-09T10:30 | orphan cleanup (excluded dup run) | done (human-approved) | metrics/ledger.csv |
| 10:34 | start P01 | — | ledger |
| 10:40 | registry + 27→32 cards (`scripts/make_cards.py`), patches 001/002 | done | `config/samples.yaml`, `patches/` |
| 10:41 | generate-only order audit (light cards) | done, all rc=0 | `work/genonly/*.summary` |
| 10:43 | condor 900134 (17 gridpacks), 900135 (6 σ-only), 900136 (17 tests) | 900134: 12/17 done; heavy 5 running | `work/condor/submit_p03.log` |
| 10:47 | added fake-ℓ / Higgs samples idx 33–36: 900142/143/144 | done | |
| 10:50 | order-closure precision repeat idx 37–40: 900148 | done, closure PASS | `work/p03/xsec.json` |
| 10:51 | tt̄ double-fake idx 41: 900149/900150 | done | |
| 11:0x | 01 report written | done | `reports/01_signal_definition.md` |
| 11:1x | Delphes validation + fake pilots (`validate_delphes.py`, `egamma_pilot.py`) | done for 16 test jobs | `work/p03/*.json`, `figures/p03_signal_validation.*` |
| 11:2x | 02 report written | done | `reports/02_background_overlap.md` |
| — | PENDING: gridpacks B_EW_wpaajj, B_EW_wmaajj, B_QCD_lvaajj(+_nomjj), T_ttaa_1l and their test jobs (900136.4–7, .12, held until gridpack) | running | `condor_q 900134 900136` |

Restart recipe: `source p2/lib/scripts/setup_stack.sh`; check `condor_q`; when the pending gridpacks finish, run `condor_release` on the held tests (or wait ≤ 30 min), then `python3 -P scripts/xsec_table.py; python3 -P scripts/validate_delphes.py` (cached per sample) `; python3 -P scripts/test_audit.py`, then update 03 report §1/§4/§5 and 02 report §2/§5.
| 2026-11-14T09:48 | G1 accepted (human, defaults D-WH-1..4); amendment A2: Phase 05–07 on frozen wh-prod-v1 | logged | metrics/ledger.csv |
| 09:57 | own H_ggF_jj_nomjj: gridpack 913309, test 913310, production 913321 (30 × 2000) | done | 05 §1, 03 addendum |
| 10:10 | ntuples: 913314 (removed, comma-arg split), 913320 (999 jobs) + 2 local ggF chunks | done | wh/work/nt |
| 10:25 | p05_run.py (inventory, SHA, N check, closures, optimisation) | done | work/p05/p05.json |
| 10:35 | p05_bdt.py (k-fold, adopted), p07_stats.py, figures, reports 05/06/07, FINAL, final.json | done | reports/ |
| — | W⁻γγjj own gridpack retry 912997 failed again (deterministic); not retried (D-WH-11) | closed | 03 addendum |

Restart recipe (Phase 05–07): see FINAL_report.md §6.
