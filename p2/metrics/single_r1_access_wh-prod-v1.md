# single_r1 access to wh-prod-v1 (A2): instructions for the human

Written by the multi_r1 orchestrator on 2026-11-07, at tag `wh-prod-v1`.

## What single_r1 may read
- `p2/production/wh/<sample>/*.root`: slim Delphes ntuples (TTree `Delphes`) and GenTruth (RNTuple). Read-only.
- `p2/production/wh/SAMPLES.csv`: one row per sample, with these columns:
  - role, σ and its source, BR×k, N_generated, N_Delphes, signed Σw;
  - normalisation formula, generator cuts, seeds range, files glob.
  
  The frozen ZH rows are read-only pointers to the ZH production.
- `p2/production/wh/FORMAT.md`: branches, weight semantics (including the WeightLHEF index map), units, generator facts, the Delphes j→γ / e→γ rate tables as data, the f_ℓ range with citations, versions.
- `p2/production/wh/SHA256SUMS`: integrity list of the ROOT files. Check it with `cd p2/production/wh && sha256sum -c SHA256SUMS`.
- A git-tracked copy of the three metadata files is in `p2/metrics/wh-prod-v1/`, with the sha256 of each (`MANIFEST.sha256`). If the copy in `p2/production/wh/` differs, the tagged copy is authoritative for v1.

## What single_r1 must NOT read
- `p2/runs/multi_r1/**`: reports, code, reviews, STATUS, briefs.
- `p2/SPEC.md`: it contains multi_r1 decisions. single_r1 uses `p2/SPEC_G0.md`, plus the human amendments A1/A2 and the resume decisions as given to it by the human.
- `p2/production/hh/**`.
- `p2/metrics/review_log.csv`, `usage_p2.*` and `heptools_*`.

## Steps (human)
1. Let single_r1 finish its WH Phase 01-03 and G1, as pre-registered and without production access.
2. After its G1, run the second isolation stage:
   `python3 p2/metrics/g1_repeat_isolation.py --single-r1-prod` (use `--dry-run` first).
   This lifts the production/** read deny for single_r1 only. It keeps production/wh/** edit-denied and production/hh/** read- and edit-denied.
   (Stage 1, without the flag, must already have been run for all repeat runs before they start.)
3. Commit the settings change: `git add p2/runs/single_r1/.claude && git commit`.
4. Tell single_r1 (in its prompt):
   - The WH samples are frozen at tag `wh-prod-v1` in `p2/production/wh/`. Read SAMPLES.csv and FORMAT.md first, and verify SHA256SUMS.
   - Use the samples read-only. If single_r1 needs extra samples, it generates them under its own `p2/runs/single_r1/` with seeds R=4 (SPEC_G0 §3.4), never in `p2/production/`.
   - v1.1 will add rows: H_ggF_jj (gridpack still running), and possibly a 2-jet F_QCD_Wajj row, depending on the human decision H1. Its background list must therefore not assume v1 is complete, and the H_ggF_jj yield must not be assumed negligible.
5. Optional: make the frozen files immutable on disk with `chmod -R a-w p2/production/wh/*/`. Undo it before v1.1 adds rows.

## Known facts single_r1 should not need multi_r1 for
All the needed physics conventions are in FORMAT.md, which contains no analysis recipe or nominal method (A2).
