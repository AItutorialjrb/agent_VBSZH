# Brief — executor-hh, multi_r1, pre-G2 and Phase 04+ (orchestrator, G1 decision D19)
Read this brief, not the full handoff. Binding sources, in order: p2/SPEC.md §1, §4.3 and §6 (decision log), this
brief, reviews/hh_01-03.md, your reports/03 §13 (pre-G2 plan).
Your directory: p2/runs/multi_r1/hh/. Shared canonical samples: p2/production/hh/<sample>/ (create it). Never write
elsewhere. ZH tree, p2/lib and software/ are read-only. **Do not run MG5 commands that install into the shared
software/ tree** (D-HH-1). New installs only under p2/software/ (and record checksums).

## 0. Rules that stay binding
- Signal and the D-HH-12 samples: N_MC ≥ max(50k, σ×BR×3000 fb⁻¹). Other backgrounds: effective-N policy (SPEC §4.3),
  enforced by nmc_check_hh (fails loudly).
- BR applied once; Delphes-level yields only; test job before bulk; no duplicate submissions.
- **No bulk production before G2.** Allowed now: gridpacks, test jobs, twin samples, N_eff pilots at validation size
  (state the size and why).
- Seeds (SPEC §3.4, G1 revision): seed = 3 000 000 + 100 000×1 + 1000×sample_idx + J. Write the seeds already used,
  config/seeds_used_preG1.txt (old formula, kept, unchanged), and make the uniqueness assertion cover them.

## 1. Human decisions at G1 (verbatim in SPEC §6). Implement them.
- D-HH-1 HEPTools stays (human). No action except the rule above.
- D-HH-2 ggF HH: LO loop-induced gg→HH + PS (existing install, no new install in software/). Normalise to the LHC HWG
  NNLO (FTapprox or the current recommendation) σ at 13.6 TeV. Cite the CERN Yellow Report/TWiki value and the version.
  Add 30 % extra uncertainty in the VBF region. State that EW–loop interference is neglected. Reword 01:62(c).
- D-HH-3 tt̄ nominal: validated MLM tt̄+0,1,2j (DJR / matching-scale check). ttjj ME+filter only if N_eff fails.
- D-HH-4 QCD multijet: 4j + bbjj + PS + truth-tag. Give the class-resolved N_eff estimate (review 6) and use a
  b-enriched / PS g→bb strategy. Normalisation ±100 %; results also with multijet ×0.5 and ×2 (pre-declare now).
- D-HH-5 Deliverable κ2V ≠ 1. 300/450 thresholds provisional, fixed by expected-only optimisation in Phase 06. Quote SM
  0.07 events with its Poisson interval.
- D-HH-6 Background twins (ihtmin, VBS filter 3.0/400, ptheavy) and N_eff ≥ 10 projections before G2. Storage ≤ 150 GB
  after checking the EOS quota. (`eos quota /eos/home-r/rjiang` returned "no quota for path /eos/user/r/rjiang/". Try
  `eos root://eosuser.cern.ch quota /eos/user/r/rjiang/` or `eos quota -m`; record the command and the result.)
- D-HH-7 Rule: add an ME+jets sample (Z/W+3j, VH+2j, ggH+jj) only if that background's PS-based yield is > 10 % of the
  total SR background. Otherwise apply a 100 % PS-modelling uncertainty. Show the computation per background.
- D-HH-8 Primary result unclipped. Variation m(HH) < 1.5 TeV plus a 1.0 TeV check. Both fixed now (write into config).
- D-HH-9 Trigger 450 GeV baseline; pre-declared 500/550 variations. m_SD window defined on the Delphes peak, with a
  ±5 % mass-scale variation.
- D-HH-10 Tag-class definition of review item 1 accepted (already implemented; keep it).
- D-HH-11 Bound each extra background (tW, tt̄Z, tt̄W, EW Zjj, QCD ZZ/WZ, gg→ZH, EW Wjj): a 95 % UL in the SR. Make a
  dedicated sample only if its UL > 10 % of the total SR background.
- D-HH-12 Full N (max(50k, σ×BR×3000)) for ggF HH, ZH, ZZjj, tt̄H.

## 2. Reviewer conditions (reviews/hh_01-03.md), binding before G2
- 2: covered by D-HH-7.
- 3: morphing: one closure point with κV ≠ 1 and κλ ≠ 1; a Delphes-level SR closure; Σ|c_i| / MC-stat amplification
  over the intended κ2V and κλ scan ranges; fix the citation 01:90.
- 4: covered by D-HH-12.
- 5: nmc_check_hh must check how ul_fb was derived (Poisson 95 % with the weight scale) and that the conservative
  variant is actually produced. Fails loudly otherwise.
- 6: covered by D-HH-4.
- 7: gridpacks and test jobs for W±H, ggH+jj, W+jets, QCD 4b, tt̄+0,1,2j MLM. Correct the stale status lines
  (INDEX:6, 03:4).
- 8: covered by D-HH-6.
- 9: (b), (c) are logged in SPEC §7 by the orchestrator. For (a), justify the absence of a W factor in 01.
- 11: done. 12: covered by D-HH-11. 13: covered by D-HH-9.
- 14: make the decision lists consistent everywhere (01, 02 §9, 03, STATUS).

## 3. Deliverable for G2 — `reports/04_production_plan.md` + INDEX update
The G2 reviewer judges this file. For each sample entering s or b, a table row with:
sample | class | σ (fb) and source (+ K-factor and normalisation) | BR applied once | generator filters and twin
evidence (loss ± stat at reco SR) | rule (full N / effective-N) | N_required or N_eff target | N_planned | projected
N_eff in SR per tagging scenario (class-resolved) | seeds | jobs × events | CPU-h | storage (GB) | test job (cluster,
exit 0, verified).
Plus: morphing-closure evidence (item 3), the D-HH-7 and D-HH-11 rule outcomes, the pre-declared variations (×0.5/×2
multijet, trigger 500/550, m_SD ±5 %, m(HH) clips), the storage total against the quota, the CPU-h total, the
`nmc_check_hh` output on the planned table (must pass), the deviation list, and the condor submission plan.
Phase 03 PASS only when every handoff sample type has a verified test job.

## 4. Working protocol
- Verifier: for every new finished test job, gridpack, twin or closure result, write VERIFY_REQUEST.md (paths,
  cluster IDs, expected σ/BR/N) and say so in STATUS.
- STATUS.md ≤ 25 lines (done; running clusters; blockers; decisions needed D-HH-N; next action). Your final reply is
  a pointer to STATUS.md only.
- If a new human-level decision is needed (not covered here), raise D-HH-13+ in STATUS, stop that branch, and continue
  the rest.
- Long waits: do not idle-poll. If only condor jobs remain, set STATUS "waiting on clusters X" and return; you will be
  resumed.
- Prefix the first line of your work log with ROLE=executor-hh PHASE=PRE-G2.
