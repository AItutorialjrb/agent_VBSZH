# verify_R2_workspace_toys (haiku verifier, FINAL-R2, 2026-11-16) — saved by the orchestrator (verifier read-only)
VERDICT: FAIL (sev-1: 1)
PASS: 40 λ-chunk copies byte-identical to toys_prefix; toy medians/bands reproduce toys_summary_v12.json (λ=-1 kZ WH 3.920 VH 3.965 ZH 0.815; kW WH 6.329 ZH 1.126 VH 6.368); Z0 toys (WH 0.4056, VH 0.4056, ZH 0) and mu95 CLs fits (8.375±1.106, 34.287±1.929, 6.407±0.347) reproduce; all R2 table numbers match source json; compat p-value and λ=-1 kZ curves reproduce exactly; correlation scheme 13 shared = 13 declared correlated, 57 entries match.
1. [sev-1] VH def-a 500 headline (Z0 0.4474, mu95 6.512) not reproduced by committed VH_workspace.json: pyhf reload gives Z0 0.45668 (WH 0.43812, ZH 0.13100, VH defb 0.54061 reproduce exactly); coarse mu95 ~6.1-6.2. Source vh_z0mu_500_a_both_v12.json (mtime 11-14 16:13) predates VH_workspace.json (20:26). Also stale: vh_z0mu_1000_b_both, 3000_a_both, 3000_b_both. Fix: rerun vh_run.py z0mu on committed workspaces.
2. [sev-2] stat_lib.py RESONANT edit (W1) dated 11-15 00:10, after all workspace JSONs (11-14 20:26); no workspace rebuilt after W1.
3. [sev-2] λ-toy provenance by reproduction: kZ seed 1, 20, kW seed 1 bit-identical with current vh_coup.py; seeds 1-20 recorded, distinct; λ path seeds via default_rng(SD), unaffected by the toys.py seeding fix. No code hash in json.
4. [sev-2] WH λ=-1 kZ q reproduced (Z 3.765929); ZH 0.289631, VH 3.776356 match.
5. [sev-2] ZH λ=-1 toy 0.82 vs Asimov 0.29 not comparable (median q 0.665 vs 0.084; 91 % toys q<1): label "not comparable" (VH_combination.md:75). n_distinct_q 2170 vs 2107 stored (sev-3).
6. [sev-2] VH_combination.md:91 "agrees within toy stat error": WH 6.64 vs 8.38±1.11 is 1.6σ; CLs non-monotone; unweighted fit 8.06; "interp 9.00" = grid end.
7. [sev-2] mu95 toys reuse the same seeds at every mu point (b toys identical; sb seeds reused) → fit errors understated (not quantified).
8. [sev-2] def a: SR zhjj_qcd has no normfactor while correlation_scheme "tau" says both ZHjj lost-lepton rows are signal-like; text must state QCD ZHjj is background in def a.
9. [sev-3] (PASS) correlation scheme.
10. [sev-3] ZH toy Z0 clipped (unclipped -0.46, p_mid 0.677); "0.000 (0.000-0.000)" artefact; WH/VH "toy err" = ±0.5σ quantile bracket on the s+b median, not null MC error.
11. [sev-3] q0 chunk reproduction not bit-identical (null max |Δq| 2.2e-6 > 1e-6 tie width for a few toys).
12. [sev-3] seed reuse across channel families → WH/ZH/VH toy sets correlated; kZ and kW λ toys share pseudo-data.
13. [sev-3] finish_toys.log: make_verify_requests.py KeyError 'mu95_toy'; toy VERIFY table numbers still match.
14. [sev-3] full mu95 rerun exceeded 10-min budget; finding 1's mu95 estimate indicative.
