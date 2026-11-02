# Phase report index

Updated UTC: 2026-11-02.

- [00_environment.md](00_environment.md) — **BLOCKED**: environment/reference audit executed; production stack, live session status and project commit pins unresolved. No MC generated.
- [00_environment_audit.txt](00_environment_audit.txt) — exact fresh commands and outputs.
- [00_report_verification.txt](00_report_verification.txt) — report/index verification and checksums.
- [00_preflight_output.txt](00_preflight_output.txt) — original 2026-10-31 preflight, retained unchanged and checked.
- [00_initial_design.md](00_initial_design.md) — preliminary design, historical context only.
- [01_signal_process.md](01_signal_process.md) — **BLOCKED**: scientific signal definition and untested candidate cards documented; stack, flavour/width, amplitude and decay-normalization checks unresolved.
- [01_source_control.md](01_source_control.md) — safe nested EOS repository proposal; no Git mutation performed.
- [01_environment_evidence.txt](01_environment_evidence.txt), [01_capabilities_evidence.txt](01_capabilities_evidence.txt), [01_sources/manifest.txt](01_sources/manifest.txt) — exact probes and archived source provenance.
- [01_report_verification.txt](01_report_verification.txt), [SHA256SUMS_01.txt](SHA256SUMS_01.txt) — static checks and artifact hashes.
- 02_background_overlap.md — pending; not passed.
- 03_generator_tests.md — pending.
- 04_detector_validation.md — pending.
- 05_cutflows.md — pending.
- 06_mass_systematics.md — pending.
- 07_sensitivity.md — pending.
- 08_final_audit.md — pending.

Stopped after Phase 01 for human review. Phase 00 blockers remain unresolved; neither Phase 01 nor Phase 02 has passed. No production authorization follows from this audit. All new persistent artifacts are project-local on EOS.

## Appended 2026-11-02 UTC — Claude Code session (M1–M7)
- [PROGRESS.md](PROGRESS.md) — fast resume index (start here).
- [01_addendum_claude.md](01_addendum_claude.md) — **PASS (LO signal definition & decay accounting)**: executed parse of the 6 cards (ew_z_decay syntax fixed), Z→ll BR closure, PY8 H→γγ closure, decisions D1–D11.
- [02_background_overlap.md](02_background_overlap.md) + `config/sample_matrix_phase02.yaml` + `cards/phase02_candidates/` — **BLOCKED**: ledger complete, overlap/merging validation pending (Phase 04).
- [03_stack.md](03_stack.md) — **PASS**: LCG_110 + upstream MG5 3.6.3.
- [03_generation_validation.md](03_generation_validation.md) — **PASS** for EW/QCD ZHjj, interference, ttH; continuum llγγ moved to batch gridpacks.
- [04_production_plan.md](04_production_plan.md) — Tier-1 plan ready (not submitted); Tier 2 BLOCKED on D11/D12. (The Phase 04 detector-validation report keeps its planned name, 04_detector_validation.md.)

## Appended 2026-11-02 UTC — Claude Code run 2 (production-plan revision)
- [03_generation_validation.md](03_generation_validation.md) — appended **M6 test-job audit** (2×2000 events, σ consistent, 105/124 kB/ev stock; Delphes clock-seed reproducibility finding fixed) and **M6b** (slim storage 1.5–2.8 kB/ev validated; 11 new σ; fake-factor pilots; split-gridpack closure −1.4 %, PLAUSIBLE).
- [04_production_plan.md](04_production_plan.md) — **v2** (replaces v1): per-sample σ/N/weight/storage/CPU table ([04_stats_table.md](04_stats_table.md), `config/production_v2.yaml`); ≈29 GB of the 300 GB budget; ≈0.8k core-h expected; bulk BLOCKED pending decisions.
- [eos_quota_2026-11-02.txt](eos_quota_2026-11-02.txt) — user-supplied quota record (supersedes the Phase 00 quota estimate).

## Appended 2026-11-02 UTC — Claude Code run 3 (submission + pilot sensitivity)
- [05_pilot_sensitivity.md](05_pilot_sensitivity.md) — **PASS (pilot)**: normalisation/BR-once evidence, exit-code-2 root cause, reference-aligned background model (proxies and fake-factor band labelled), optimisation on expected yields, results at 500/1000/3000 fb⁻¹, and the D12 recommendation (do not run the full production_v2; reduced campaign). s < 1 at all luminosities.
- Project-only git repository initialised in $PROJECT (D10); see PROGRESS.md for commits and push status.
