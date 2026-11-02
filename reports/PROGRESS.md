# PROGRESS — fast resume index (not a replacement for phase reports)

Agent: Claude Code (Opus 5.5), single session, started 2026-11-02 13:30 UTC on lxplus9109. Codex installation/session/state untouched. Parent Git (`/eos/home-r/rjiang`, HEAD 6ea6cb9) untouched; **no project Git** exists (git init awaits explicit user approval, see 01_source_control.md).

## M1 checkpoint — 2026-11-02 13:40 UTC

### Phase 01 item classification (evidence: files read on EOS; `sha256sum -c reports/SHA256SUMS_01.txt` → all OK)

| Item | Class | Evidence |
|---|---|---|
| Gauge-invariant EW ZHjj definition (full (QCD,QED)=(0,4) amplitude, no diagram vetoes; VBS = fiducial region) | STATIC-ONLY (documented, sound) | 01_signal_process.md §Scientific definition |
| Order bookkeeping table EW/QCD/interference | STATIC-ONLY | 01_signal_process.md §Coupling |
| 6 MG5 cards + higgs_decay.cmnd | STATIC-ONLY (never parsed by MG5) | cards/phase01_candidates/, 01_report_verification.txt |
| BR product (B_ee+B_μμ)·B_γγ = 0.067294 × 0.002270 = 1.5275738e-4 | VALIDATED (arithmetic only; re-checked) | 01_report_verification.txt |
| BR inputs (YR4 BR_γγ, PDG2025 B_ll) | VALIDATED as sourced inputs | 01_sources/higgs_125_rows.txt, pdg2025_z.txt |
| H→γγ decay route (PY8 forced decay) | STATIC-ONLY; runtime closure MISSING | 01_signal_process.md §H→γγ |
| Generator stack choice | BLOCKED (Phase 00) → addressed in M4 | 00_environment.md |
| PDF / scale / seeds / run cards | MISSING | 01_signal_process.md §run specs |
| Flavour scheme (5F massless vs 4F/heavy Yukawa/CKM) | BLOCKED (decision) → D-decision in M2 | 01_signal_process.md |
| Diagram/subprocess/xsec validation | MISSING → M5 | — |
| Project Git | BLOCKED (needs user approval) | 01_source_control.md |
| Phase 02+ outputs | MISSING (none existed at start) | `ls reports` |

### Verified outputs (sha256)
```
10ef6bca4ae3128241e52377fa9dd3ceef98e3a5fb7023dc4df90c142ba1f3d4  reports/01_signal_process.md
6346d1a08304a62915606ca5d715922bd64f8760b890600a0edda87deff31ac2  reports/01_source_control.md
9e5b3ea1c3dc50863a1f0bac6cbc86c56d98fac2123b27a31940404cdb4d07b0  reports/INDEX.md (pre-append)
52accc3c4de3ec638be0a73e1513fb1c29022704711076c1fbd10c1d64cce1fe  reports/00_environment.md
1b99c2896e9e07192ee91b19333a279939f954406149b5518e6b3aff7b6363ff  cards/phase01_candidates/ew_on_shell.mg5
ec9601ecef34eeec5b661a0a8a2a26e350f7f206a6d20c3d000f45c2a1faadca  cards/phase01_candidates/ew_z_decay.mg5
bfbc5ebb334dbce680f730ffdfbf9e492984bd85502e4edb844e29f6401a5d2b  cards/phase01_candidates/higgs_decay.cmnd
```

### Environment facts newly observed (M1)
- Newest LCG: LCG_110/110a → MG5 only `3.6.4.atlas2` (patched), Pythia8 **8.317**, Delphes **3.5.1 (stable)**, ROOT 6.40.02, Python 3.13.11, LHAPDF 6.5.5, HepMC2 2.06.11, HepMC3 3.3.1, FastJet 3.5.1 (`x86_64-el9-gcc13-opt`).
- Upstream MG5 tags on GitHub up to v3.8.1; v3.6.3 (reference version) downloaded to `software/sources/` (sha256 2bb0d085…ebd98).
- HTCondor: 0 user jobs. /tmp 35 GB free. `eos quota` for /eos/user/r/rjiang returned "no quota for path" (see 03_stack.md).

### Open items
M2 addendum; M3 Phase 02 ledger; M4 stack; M5 smoke tests; M6 condor test; M7 production plan.

### Next command
Continue with M2 (static audit) — see subsequent milestone sections below.

## M2–M4 checkpoint — 2026-11-02 ~14:00 UTC
- M2 PASS: reports/01_addendum_claude.md (6 cards parsed; ew_z_decay.mg5 syntax FAILED and corrected; Z→ll BR closure pull 1.0; H→γγ PY8 closure; decisions D1–D11; D7/D10/D11 need user).
- M3 written, status BLOCKED pending Phase 04 overlap validation: reports/02_background_overlap.md, config/sample_matrix_phase02.yaml, cards/phase02_candidates/.
- M4 PASS: reports/03_stack.md, scripts/setup_stack.sh (LCG_110 + upstream MG5 3.6.3 in software/install).
- Smoke cards: cards/phase03_smoke/*.mg5|*.cmnd; runner scripts/mg5_smoke.sh, scripts/run_py8_delphes.sh, scripts/smoke_analysis.py; outputs work/m5/<sample>/.
- Restart: `source scripts/setup_stack.sh`; smoke reruns refuse to overwrite /tmp/$USER/vbszh_smoke/<card> (node-local; delete or set SMOKE_SCRATCH).

## M5–M7 checkpoint — 2026-11-02 14:10 UTC (end of Claude run 1)
- M5 PASS (EW ZHjj, QCD ZHjj, interference, ttH); llγγ continuum timed out → batch gridpacks. reports/03_generation_validation.md.
- M6 PASS: HTCondor cluster 879052 (EosSubmit schedd), 2 jobs, exit 0; outputs production/test/{ew,qcd}_zhjj_zll/*_s1361x001.*; logs production/condor_logs/.
- M7 PASS (plan): reports/04_production_plan.md; Tier-1 submit file ready, NOT submitted.
- Key number: EW ZHjj→ℓℓγγjj = 2.88e-3 fb (LO) ⇒ ≤1.44 events at 500 fb⁻¹ before acceptance; ~0.12 after illustrative VBS selection.
- Open decisions needing the user: D7 (only if |I|/S>10%), D10 git init, D11(b,c) Delphes detector-model changes, D12 scope before Tier 2.
- Scratch left on node-local lxplus9109:/tmp/rjiang/vbszh_smoke (ephemeral copies only; all results staged to EOS).

### Restart instructions
1. `cd /eos/home-r/rjiang/vbs_zh_codex_starter; source scripts/setup_stack.sh`
2. Check batch state: `bash -lc 'module load lxbatch/eossubmit; condor_q'`
3. Next command (Tier-1 production; requires the user's go-ahead):
   `bash -lc 'module load lxbatch/eossubmit; cd /eos/user/r/rjiang/vbs_zh_codex_starter/scripts/condor; condor_submit production_tier1.sub'`
   In parallel (independent): `… condor_submit gridpacks_llaa.sub`
4. Completeness check: `ls production/v1/<sample>/*.json | wc -l` vs 100 (EW) / 250 (QCD); resubmitting is duplicate-safe.

### sha256 of outputs created in this run
d7d6711877a52b0874e3297015aa13aa1388ca7dcf5abca998d140b47b24f20d  reports/PROGRESS.md (before this section)
2acf40ec3d2a3775aac77a7fb87e2302fbfdafdcbc2f4b3a2d4d1f4eaf7d8740  reports/01_addendum_claude.md
500415cb8b8fa863fb667257e0df76fb55589b96e9f0ae1a409a5c0c9d5fcbf0  reports/02_background_overlap.md
0608fee824f3cad51c3800213d70e0cfd9ab99917655504cdce9db7f00e9d827  reports/03_stack.md
b0b7125bc0938c2358e668c98034007c4953cba332f492c09ad2aaed9ca3e5eb  reports/03_generation_validation.md
a234cca6b02e5028a25b73d411bfb1b480397861588c914fc67d24239fd1d01a  reports/04_production_plan.md
5fae405173c631711ddddb2309d6b9dfb197500ce3810a41233beac5c75150e4  config/sample_matrix_phase02.yaml
85a904327200169cd292a8425bf771c4a67e92b1bab0fae8fbd8f3b70eef7abf  scripts/setup_stack.sh
bb9b5dbc94a8e421bc754bc9042ea51f241f57d1b84d1cd577859c3235b66479  scripts/mg5_smoke.sh
6bc10fa544c937d7adaf34a0ba299e371a76ba9c72db35cb0990f89ccf02b27f  scripts/run_py8_delphes.sh
7febc61263313e4fbf7c3c993338d8f4ea98cd77a62096b0ab23db127dc1f405  scripts/smoke_analysis.py
db8d8d6b4dcb5dbedee1ffe601b541bc08663087029a799e959456fcf95fda8c  scripts/condor/make_gridpack.sh
b92ef2eafd58f97db93162ed269d01ffa5d6700d1465969d9dd74796ea281b55  scripts/condor/run_job.sh
f27918bcd1f76c5e87adfb418e4c77505a6dfebc01202eca930d12dc54baf607  scripts/condor/gridpacks_llaa.sub
77abb638a723cc7eb434c37379ed9f821cc516cf1e072b03fb5706f34508816d  scripts/condor/production_tier1.sub
3144f61181edb9519efedad7f4859788803788b5287c8028875fc2f5d593d0cf  scripts/condor/test_zhjj.sub
39960905384267dcbe67e3fe374e9dcfd2efc4224a066734533ea57437e4fe56  cards/phase03_smoke/ew_llaajj.mg5
c8f4b4e0d6b854993386aeb2928beafd6073fb0568d8d090e0d4060d76be0610  cards/phase03_smoke/ew_zhjj_nodecay.mg5
62027a45ea1cbf94de5ec15176a1b141f7237ba7a66f1dff6f130ca14238ca78  cards/phase03_smoke/ew_zhjj_zll.mg5
46e1b584da26c6d76c8c57b8d582cb5c73ffc7e0f5c399ddea3365881e5e58f3  cards/phase03_smoke/int_zhjj_nodecay.mg5
016d842d1f2651ab46480ccae5bca77331f284ddaaf817225577c4a77740e797  cards/phase03_smoke/py8_common_CP5.cmnd
c2abbfb11488dbfefa4530a6362b6fd295e1d2f5a249333e666c04fa87a0c7a5  cards/phase03_smoke/py8_ew_zhjj_haa.cmnd
92e7f74e0a224189dc8994727a52d063d79a08356f282aaa0868fe1158ffe760  cards/phase03_smoke/py8_qcd_zhjj_haa.cmnd
6275d1708976197be2138cc1e42c1ebcee4fdb06c2a385fd85044512951bd8a6  cards/phase03_smoke/qcd_llaa_mlm02.mg5
c8fbdcede4e60359c9eb68572db146cce80cc295749d4652df44498902aac5be  cards/phase03_smoke/qcd_zhjj_zll.mg5
242841b67936cd020706cd5320ff992d3dfa193d0c4c175e3c132389a06799ab  cards/phase03_smoke/README.md
2772225f4a58f67b8af8cb78ec189cd130fc09a0ac1ce8a1c6c951e22093f558  cards/phase03_smoke/ttH_dilep.mg5
ebd606a1cedc8e1b02c21c93d0e686aec9b3d413e41f1a1cc88b63f89e9a2d73  cards/phase04_candidates/delphes_card_CMS_vbszh_v0.tcl
7edd608fef943ff51f6515d3162e6f554de323615cd3c0e8df4465da5d15b0cb  production/gridpacks/ew_zhjj_zll_v1.tar.gz
b1ee53bacbc7a74da7b649f01132741ea62ee0f8fcf8c33a6371e748f7923810  production/gridpacks/qcd_zhjj_zll_v1.tar.gz

## Run 2 checkpoint — 2026-11-02 15:03 UTC (production-plan revision; no bulk submission, no git writes)
- Stopped the leftover monitoring task (bccauaz3r); no other waiters or orphaned MG5 processes remain.
- M6 audit appended to 03_generation_validation.md. Finding: the stock Delphes card is clock-seeded → `RandomSeed` is now pinned in scripts/run_py8_delphes.sh (bit-reproducible).
- Storage: cards/phase04_candidates/delphes_card_CMS_slim_v1.tcl + scripts/slim_gentruth.py → 1.5–2.8 kB/ev (was 105–124). Validated on the test LHE.
- New σ (11 processes) + Z+2j / Zγ+2j fake-factor pilots (scripts/fakefactor_pilot.py); wza/zza σ still missing (batch).
- Plan v2: reports/04_production_plan.md, reports/04_stats_table.md, config/production_v2.yaml, cards/production_v2/ (31 cards), scripts/plan/{stats_table,make_submit}.py.
- Condor: run_job.sh v2 (slim + GenTruth + optional LHE/full record, staged last-file-wins duplicate guard; tested locally, 200 events), make_gridpack.sh (ncores arg), production_tier1.sub (v2, 150 jobs), gridpacks_v2.sub (29), test_v2.sub (29), production_v2.sub (2461; seeds unique, dry-run OK). gridpacks_llaa.sub and test_zhjj.sub marked SUPERSEDED.
- Budget: ≈29 GB of the 300 GB logical; ≈0.8k core-h expected (≤6k reserved).
- Open decisions: D-P1 fake-rate scenarios, D-P2 jet-multiplicity restriction, D-P3 defer I_llaajj, D-S1 test-output retention, D10 git, D11b/c, D12 scope.

### Restart instructions (run 3)
1. `cd /eos/home-r/rjiang/vbs_zh_codex_starter; source scripts/setup_stack.sh; bash -lc 'module load lxbatch/eossubmit; condor_q'`
2. If the plan changes: edit the tables in scripts/plan/stats_table.py / make_submit.py and rerun both (never hand-edit generated .sub files).
3. Submission order (after user approval), all via `bash -lc 'module load lxbatch/eossubmit; cd /eos/user/r/rjiang/vbs_zh_codex_starter/scripts/condor; condor_submit <file>'`:
   production_tier1.sub → gridpacks_v2.sub → (per passing gridpack) test_v2.sub → production_v2.sub.
4. Completeness: `ls production/<v1|v2>/<sample>/*.json | wc -l` vs the queue count; resubmission is duplicate-safe.

### sha256 (run 2 outputs)
70fdb2adafe3da58498b6438ee1073a0bfb5db165e12e045db36d57e0003519b  reports/04_production_plan.md
d5420db4ad3f5f4d22ec8e8ad98038c2c791b20b4cab9416e2fc99e9192568bd  reports/04_stats_table.md
ab059367624a644c7aceb15a3c85ddc5d65558d9b16710a7b32045b58de85dab  config/production_v2.yaml
c7888f1cbd84623d4e507d3298feb32be54e97c3dd339cc52ba8394e99bc26eb  config/sample_matrix_phase02.yaml
9309a6ba2e386b6b8dd1c4b9608a8e27c0b2d9ba9013f590c56f24c79e47c7e9  cards/phase04_candidates/delphes_card_CMS_slim_v1.tcl
685f87d91ada2b412cbe79f0cf46d97e29a0ca6314b29487cb176d1278fffeaa  scripts/slim_gentruth.py
0cf113618297fe5be452ab45b3d4642e577c1c11de9c48d381da42331b772668  scripts/fakefactor_pilot.py
88741f21624adfe00f60d936e646cb21ae5dc9e1a6383fc119092ee658f580fb  scripts/run_py8_delphes.sh
62e02b0bfffc920d7fe7133366d4f1c9cb03e86136b7252c0930e060139e75a2  scripts/plan/make_submit.py
3e112875f3f3766da8018aebf68dfa1026fa8a9bca0c979f7e153cd34d2498d6  scripts/plan/stats_table.py
83979b390e244864d665c55a435dcb38c8d7dbf5245fb84e3ac36f338fe0bb94  scripts/condor/run_job.sh
d51258707be579e8c9e50912b63127f5d852eb8fbe180034b1f2f97e362e018b  scripts/condor/make_gridpack.sh
93e6b348b0ad6205ea1c0aef49a809c6027cca78168282ffc3169850ca19a946  scripts/condor/production_tier1.sub
ed95d658a8feb9dccc3dabf22f2c2fb9b15e49e0068b2d2773800d91fdb2b0b7  scripts/condor/gridpacks_v2.sub
cc707f65a87e78745333a524eafd2ec292ffe623b7b8b5916a8a875acd4b8059  scripts/condor/test_v2.sub
977c6e78463d3bfb78d3c22c62d989b002c39c9c721e329075c2621fedd79cbd  scripts/condor/production_v2.sub

## Run 3 checkpoint — 2026-11-02 15:55 UTC (submission + Phase 05 pilot)
**Decisions applied**
- D-S1 approved: keep the full-record test outputs until Phase 04 sign-off.
- D10 approved: `git init` in $PROJECT (show-toplevel = $PROJECT verified; parent repo untouched at 6ea6cb9). Commits 777277f and a998b00, plus the run-3 report commit.
  - Remote `origin` = git@github.com:AItutorialjrb/agent_VBSZH.git.
  - **NOT pushed:** `ssh -T git@github.com` returns "Permission denied (publickey)". The user must add an SSH key for lxplus.
- D11 b/c **rejected**: these are detector-model changes, not stock-restoring fixes. The stock CMS card physics is kept.

**Submitted** (EosSubmit schedd)
- Tier-1 `production_tier1.sub` → cluster 879165: 150/150 exit 0; 200k EW + 100k QCD ZHjj in production/v1.
- `gridpacks_v2.sub` → 879166:
  - 13 gridpacks OK.
  - H_ggZH **failed** (MadSpin in gridpack mode).
  - 15 heavy or merged gridpacks still running.
- `test_v2.sub` → 879167:
  - 12 done (production/test_v2).
  - H_ggZH removed (gridpack missing).
  - The rest are held and auto-released every 30 min until their gridpacks exist (exit 19 → on_exit_hold; give up after 200 starts).
- **production_v2.sub is HELD** (D12; recommendation in reports/05 §5: do not run the full campaign).

**Wrapper fix (run 3)**
- Without transfer_output_files, HTCondor copied job scratch files back into scripts/condor/: about 1.1 GB of duplicate LHE, log tarballs, gridpack copies and json. These duplicates are NOT deleted; that needs user approval.
- run_job.sh and make_gridpack.sh now delete top-level scratch files on exit. Jobs already running still return files.
- make_gridpack.sh now overwrites its status/log diagnostics on retry (xrdcp -f); the gridpack itself is never overwritten.

**Phase 05 pilot result (500 fb⁻¹, definition a):** s = 0.067, b = 0.094, Z_syst = 0.20, μ95 = 44.6. At 3000 fb⁻¹: s = 0.40, Z = 0.48, μ95 = 7.4. Details in reports/05_pilot_sensitivity.md.

**Restart**
1. Check jobs:
   `bash -lc 'module load lxbatch/eossubmit; condor_q 879166 879167'`
2. When the test_v2 outputs exist:
   - `source scripts/setup_stack.sh`
   - build `work/m7_analysis/tv2_<id>.npz` with `scripts/analysis/ntuple.py`
   - extend MAP in `scripts/analysis/override_test_v2.py` (B_QCD_llaa_1j/2j_is*, B_EW_llaajj_is*, F_QCD_lla_mlm, F_EW_llajj, F_Zjets_mlm, V_*) to replace the proxies
   - rerun `sensitivity.py` and `tables05.py` (commands in reports/05 §9).
3. Do NOT submit production_v2.sub before D12 is decided.
