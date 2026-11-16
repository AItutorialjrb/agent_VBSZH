# verify_R4 (haiku verifier, FINAL-R2 R4, 2026-11-16) — saved by the orchestrator
VERDICT: FAIL (single cause: pre-R4 headline in two captions; all numerical checks pass)
PASS: C1 LLQ window content 0.121227 in WH/VH workspaces (upper 0.67543, lower 0.003069; preR4 0.2551 = 2.10 Y0, factor 0.47514). C2 pyhf WH joint 0.455539, VH 0.473376, ZH 0.130998; stand-alone WH rebuilt 0.445111; sources newer than 06:35 rebuild. C3 49/49 R4 rows match; T4, T4c, T7, T10, csvs, paper_numbers; missing []; exact Poisson 8.082. C4 toys_agg rerun 0 diffs; WH 0.4248, VH 0.4607, ZH 0; μ95 7.124±0.301, 6.819±0.576, 33.51±1.84; λ=-1 tails WH 0.0470/0.0108/0.0012, VH 0.0390/0.0130/0.0024; 160 q0 s+b files (914157); coupling outputs cmp-identical to preR4.
[sev-1] T5_systematics_WH.tex:28 and T6_nonprompt_scans.tex:30 captions state stand-alone WH 0.428/6.81 (pre-R4); bodies 0.445/6.58.
[sev-2] final.json:140,~160 Z_lambda_m1 "primary" 3.764024 / kW 6.197320 from WH-only couplings_kzneg_v12.json (Nov 14); headline 3.7659 (joint). Regenerate or relabel.
[sev-2] VH μ95 toy grid changed preR4 5 pts × 480 → R4 4 pts × 240, undisclosed; 6.41±0.35 → 6.82±0.58 mixes workspace and grid effects.
[sev-3] pl_140_a_v12.json pre-rebuild, not labelled _preR4 (used only as a gate).
[sev-3] counting_v12, couplings_* older than rebuild (workspace-independent; state it).
[sev-3] ZH q0 reruns differ from preR4 by ≤2.6e-5 (fit noise).
[sev-3] VH_combination.json lacks D49 ends/toys/map2d (md/csv only).
[sev-3] compile not re-run by verifier.
