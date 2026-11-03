# VBS/VBF Higgs programme, phase 2 — WH and boosted VBF HH→4b with a multi-agent system
**Pre-registered experiment design + execution handoff**

**Handoff date:** 2026-11-03 UTC
**Owner:** Ruobing Jiang (human PI)
**Repository:** `/eos/home-r/rjiang/vbs_zh_codex_starter` (git remote `git@github.com:AItutorialjrb/agent_VBSZH.git`)
**Frozen baseline:** ZH study at tag `zh-final-v1.1`. Read-only from now on.
**Standard:** every deliverable, physics and AI, is held to the PRX Intelligence standard.

Read this document completely before acting. It is both the physics specification and the pre-registered protocol of an AI experiment. Deviations from the protocol must be logged, never silent.

---

## 0. Context and purpose

This work produces one AI-led paper: *an agentic system that executes end-to-end, auditable LHC phenomenology feasibility studies*. Three physics tasks form a ladder of increasing novelty.

| Task | Status | Role in the paper | Agent arm |
|---|---|---|---|
| EW ZHjj, Z→ee/μμ, H→γγ | **done**, tag `zh-final-v1.1` | observational single-agent pilot; source of failure modes | single (Codex → Claude handoff) |
| EW WHjj, W→eν/μν, H→γγ | to do | **reuse + extension** task; controlled single- vs multi-agent comparison | multi (canonical) + single (control) |
| Boosted VBF HHjj, HH→bb̄bb̄ | to do | **new-structure** task (no photons, multijet, b-tagging, boosted jets, κ₂V) | multi |

Physics theme: **electroweak VBS/VBF production of Higgs bosons with two tagging jets, probing the HVV (λWZ = κW/κZ) and HHVV (κ₂V) couplings.** VH is combined (ZH+WH) at the end.

Highlights the paper must be able to defend with data:
1. correctness and honesty of agent-produced physics, at Delphes level;
2. the failure modes of a single agent, and which ones the multi-agent design removes;
3. **token, cost and prompt economy**: tokens per role and phase, human prompts per phase, versus the single-agent arm and the ZH baseline.

---

## 1. Non-negotiable policies (inherited from ZH, still binding)

- All persistent artifacts on EOS under the repository root. No AFS. `/tmp` only for transient state.
- Never touch the parent Git repository at `/eos/home-r/rjiang/.git`. Never touch Codex or `~/.codex`.
- **ZH is frozen.** Never modify files reachable from tag `zh-final-v1.1` under `reports/`, `cards/`, `config/`, `scripts/`, `work/`, `production/`, `figures/`. Reuse ZH code only through the read-only library copy in §4.
- All final yields at Delphes level. No LHE-level, parton-level or proxy numbers in final results.
- MC statistics: N_MC ≥ max(50k, σ×BR×3000 fb⁻¹) for every sample entering s or b, enforced by code that fails loudly (reuse `nmc_check()`). Exceptions only through the HH effective-N policy in §5.3, declared in advance.
- BR applied exactly once per sample, with the per-sample BR ledger asserted in code (reuse the ZH ledger, including the documented 0.9783 MG5-LO→PDG Z-width factor where applicable; derive the analogous W factor).
- Bulk HTCondor only after a successful test job; no duplicate submissions; EOS stage-out; seeds unique per (process, run_id, job).
- Storage budget for phase 2: ≤ 400 GB logical in total. Slim Delphes output only (reuse `delphes_card_CMS_slim_v1.tcl`, extended for HH objects).
- Every constraint above that an agent cannot satisfy must be raised as a numbered decision, never relaxed silently. (ZH failure mode: tt̄γ/tWγ produced with 2000 events, violating N ≥ σL without flagging.)

---

## 2. Pre-registered hypotheses and metrics

### 2.1 Hypotheses (fixed now; not to be edited after the first run starts)
- **H1 (correctness):** the multi-agent arm reaches each gate with fewer unresolved severity-1 physics issues than the single-agent arm.
- **H2 (human load):** the multi-agent arm needs fewer corrective human interventions per phase.
- **H3 (economy):** the multi-agent arm uses fewer cost-equivalent tokens per completed phase, because high-volume work runs on cheaper models and logs never enter the orchestrator context.
- **H4 (time):** wall time per phase is not worse than the single-agent arm by more than 20 %.

Null results are reported as such.

### 2.2 Controlled comparison (WH only)
- **Arms:** `single` = one Claude Code session, Opus, no subagents (same configuration as the ZH baseline). `multi` = the architecture in §3.
- **Repeats:** Phase 01–03 of WH (§5.1), run **3 times per arm** (`r1`, `r2`, `r3`), each from the identical start state and identical first prompt.
- **Canonical run:** `multi/r1` continues to production and final results. Fixed in advance; no cherry-picking.
- **Single-arm continuation:** `single/r1` continues through analysis and statistics (Phase 05–07) on the **frozen canonical WH samples**, without producing its own bulk MC. Its sample-matrix design is still recorded and diffed against the canonical one.
- **Isolation:** each run works only in its own directory (§4), may read only `lib/`, `SPEC.md` and its own directory, and never reads another run's outputs. Enforce with Claude Code permission deny rules where supported (verify the rule syntax with `/permissions` before the first run); log any access violation.

### 2.3 Metrics (definitions are binding)
| Metric | Definition | Source |
|---|---|---|
| tokens by class | input / output / cache-write / cache-read per model, per role, per phase, per run | Claude Code `.jsonl` incl. subagent sidechains, parsed by `parse_usage.py` |
| cost-equivalent | Σ tokens × public API list price per model and token class at run date (prices recorded in `metrics/prices.json`) | computed |
| human prompts | number of human messages per phase, split into task / decision / corrective-intervention / continue | `metrics/prompts/` |
| severity-1 issues at gate | physics or normalisation errors that would change a result or violate §1, found by the gate review | reviewer reports + human gate check |
| errors caught by reviewer | issues raised and later confirmed | `metrics/review_log.csv` |
| wall / active time | from ledger timestamps; active = time with agent activity | ledger + transcripts |
| condor core-hours | per phase | `condor_history` |
| constraint violations | any breach of §1, flagged or not | ledger |
| reproducibility | a phase restarted from `PROGRESS.md` completes without redoing verified work (yes/no) | ledger |

Human assistance from a separate chat assistant is allowed for drafting gate prompts, but every use is logged as `assisted=yes` on the ledger line.

---

## 3. Multi-agent architecture (token-economy design)

One orchestrating Claude Code session spawns subagents through the Agent tool. **All coordination goes through files, never through chat relay.**

| Role | Model | Reads | Writes | Returns to orchestrator |
|---|---|---|---|---|
| `orchestrator` (main session) | opus | `SPEC.md`, each executor's `STATUS.md`, reviewer/verifier summaries | `SPEC.md` (only via decision log), `metrics/ledger.csv`, gate notes | — |
| `executor-wh`, `executor-hh` | sonnet | `lib/`, `SPEC.md`, own process directory | own process directory only | ≤ 25-line `STATUS.md` summary |
| `verifier` | haiku | logs, outputs, condor state of a named cluster or sample | nothing (read-only) | ≤ 30-line pass/fail table with file paths |
| `reviewer` | opus | one phase report + its evidence files | `reviews/<process>_<phase>.md` | numbered issue list by severity, ≤ 40 lines |

Token-economy rules (binding for every role):
1. The orchestrator never reads logs, ROOT dumps or full reports; it reads `STATUS.md` and review summaries only.
2. Executors read targeted line ranges, tail logs, and never paste outputs into their final message.
3. All high-volume checking (job audits, closure checks, N-checks) goes to `verifier`.
4. `reviewer` runs once per gate (G1–G3), with fresh context, not continuously.
5. Code is reused from `lib/` (ZH tag) rather than regenerated; changes go into the process directory as patches with a one-line rationale.
6. Standard prompts (§7) are used verbatim; free-form human prompts are counted as interventions.
7. `/compact` is run by the human at every gate before the gate prompt.
8. Each phase has a soft token budget recorded in `SPEC.md` after `multi/r1` Phase 01; overruns are flagged, not hidden.

Agent definition files to create in `<run_dir>/.claude/agents/` (multi arm only):

`executor-wh.md` / `executor-hh.md`
```markdown
---
name: executor-wh            # executor-hh for HH
description: Executes the WH (HH) physics phases defined in SPEC.md inside its own process directory.
model: sonnet
tools: Read, Write, Edit, Grep, Glob, Bash
---
Follow SPEC.md and the handoff. Work only in your process directory; read lib/ and SPEC.md read-only. Never modify ZH-frozen paths. Update PROGRESS.md after every item and STATUS.md (≤ 25 lines: done, running cluster IDs, blockers, decisions needed D1…, next action) before returning. Raise any constraint you cannot meet as a numbered decision. Token economy: targeted reads, tail logs, no dumps, no pasted outputs in your reply.
```

`verifier.md`
```markdown
---
name: verifier
description: Read-only audit of condor jobs, outputs, σ/BR closure and N-checks. Use for all job and log verification.
model: haiku
tools: Read, Grep, Glob, Bash
---
Audit only; never write or delete. For the named cluster/sample: exit codes, event counts vs expected, σ closure vs gridpack, BR ledger consistency, N_MC vs σ×BR×3000 fb⁻¹ (or the effective-N rule for HH), missing or duplicate outputs. Read tails and targeted lines only. Return ≤ 30 lines: one table + failures with file paths.
```

`reviewer.md`
```markdown
---
name: reviewer
description: Independent referee at a gate. Use only on a finished phase report.
model: opus
tools: Read, Grep, Glob, Bash
---
You did not produce this work. Read-only except reviews/. Check the named report against its evidence as a PRX Intelligence referee would: every number traceable; Delphes-level only; BR once; N/effective-N policy met; overlap removal; statistics valid at low counts; no overclaims; limitations stated; deviations from SPEC.md logged. Write reviews/<process>_<phase>.md and return a numbered issue list by severity (1 = changes a result), ≤ 40 lines, with file:line evidence. No rewrites.
```

The single arm uses none of these files.

---

## 4. Directory layout

```
vbs_zh_codex_starter/
  (ZH, frozen at zh-final-v1.1)
  p2/
    SPEC.md                     shared conventions + decision log (orchestrator owns)
    lib/                        read-only export of ZH code at zh-final-v1.1 (scripts/, cards/, config/)
    metrics/                    ledger.csv, prices.json, prompts/, review_log.csv, raw/ (git-ignored)
    runs/
      multi_r1/  (canonical)    .claude/agents/, wh/, hh/, reviews/, PROGRESS.md
      multi_r2/  multi_r3/      wh/ Phase 01–03 only
      single_r1/                wh/ Phase 01–03, then 05–07 on frozen samples
      single_r2/ single_r3/     wh/ Phase 01–03 only
    combination/                VH (ZH+WH) combination, final tables, figures
    production/                 canonical WH and HH samples (multi_r1 only)
```
Create `lib/` with `git archive zh-final-v1.1 scripts cards config | tar -x -C p2/lib` and make it read-only (`chmod -R a-w p2/lib`). Commit `p2/` on `main`; transcripts and `metrics/raw/` stay git-ignored.

---

## 5. Physics specification

Common to both processes: √s = 13.6 TeV; L = 500, 1000, 3000 fb⁻¹ (3000 fb⁻¹ = luminosity scaling with the Run-3-like Delphes card, not an HL-LHC prediction); LO MG5_aMC v3.6.3 (upstream) + Pythia8 (LCG_110) + slim Delphes CMS card, exactly as in ZH; theory uncertainties (7-point scale ⊕ PDF from MG5 weights); expected results only, from Asimov or expected counts; never optimise on an observed signal region.

### 5.1 WH (EW W±Hjj, W→eν/μν, H→γγ)

**Phases for the controlled comparison (01–03):**
- **01 Signal definition:** gauge-invariant EW W±Hjj at (QCD, QED) = (0, 4) amplitude order, both charges, W decayed in MG5 (BR ledger, W-width factor), H→γγ forced in Pythia8 with SM BR applied once. QCD W±Hjj as resonant background (definition a) and in an inclusive-signal variant (definition b). Interference statement.
- **02 Background and overlap ledger:** at minimum EW/QCD Wγγjj; Wγ+jets (j→γ fake, direct Delphes); W+jets double fake (quantitative bound); tt̄γ(γ) and tWγ in single-lepton configurations; tt̄H, tHq/tHW; **ZHjj and Zγγjj with one lost lepton, reusing the frozen ZH samples where the generation phase space covers it**; QCD γγ+jets with a non-prompt lepton (bound); hard/soft photon overlap removal as in ZH; generator-level cut safety demonstrated with twin samples as in ZH.
- **03 Generation validation:** smoke tests, σ closure, BR closure, Delphes object validation (MET resolution, lepton, photon, mγγ, VBS jets), one condor test job per sample type.

**Phases 04–07 (canonical arm; single arm 05–07 on frozen samples):** production with N ≥ max(50k, σ×BR×3000 fb⁻¹); selection (one isolated lepton, MET, two photons with pT/mγγ cuts, two VBS jets, mγγ window from the Delphes peak, b-veto against top); optimisation on expected quantities; Eq. 1 counting significance (primary, stat-only ± MC stat), profile-likelihood fit in mγγ (supplementary), μ95 with exact Poisson CLs; robustness table as in ZH.

**Coupling interpretation (canonical arm):** identical framework to ZH (HC_NLO_X0_kVV patched model, direct samples at λWZ ∈ {−1, −0.5, 0, 0.5, 1, 1.5}, per-bin quadratic in λWZ, leave-one-out closure). Results: expected exclusion of λWZ < 0, 1D λWZ scan, 2D (κZ, λWZ); compare with CMS PLB 860 (2025) 139202 and ATLAS PRL 133 (2024) 141801 (both H→bb).

### 5.2 Boosted VBF HH→bb̄bb̄ (κ₂V focus)

Methodological reference: UCL MSc thesis on particle-level VBF HH→bb̄bb̄ at 14 TeV. Reuse its ideas (VBF tagging-jet variables, top-veto concept, jet-radius reasoning); **do not reuse its numbers or its significance**, which rest on a BDT with very low MC statistics, particle-level objects and s/√b.

- **Scope:** boosted category only — two large-radius H→bb̄ candidates plus two VBS tagging jets, high m(HH). Resolved category only as outlook.
- **Signal:** EW pp → HHjj (QCD = 0), H→bb̄ in Pythia8 (BR once). Coupling dependence via the standard **six-point basis in (κV, κ₂V, κλ)** with linear combination (morphing); validate closure on at least two independent points. Primary parameter κ₂V; secondary κλ.
- **Backgrounds:** QCD multijet (bb̄bb̄ and bb̄ + light/c with mistags); tt̄ (all-hadronic and semi-leptonic); ggF HH (κλ-dependent); single Higgs (tt̄H, VBF H, ZH/WH with V→bb̄/qq̄, ggH+jets); Z/W(→qq̄)+jets; VBS/VBF ZZ, ZH with Z→bb̄.
- **Objects:** check the Delphes CMS card for large-R jets with groomed mass and substructure; if absent, extend the slim card from `lib/` and document it. **H→bb̄ tagging:** parametrised efficiencies in three pre-declared scenarios (pessimistic / nominal / optimistic signal efficiency and QCD/top mistag), with results reported for all three. Trigger: emulate a Run-3-like plateau with an offline requirement on the leading large-R jet pT or HT; state it as an assumption.
- **Statistics:** Eq. 1 counting significance and μ95 for SM VBF HH; κ₂V 1D intervals and the expected significance of excluding κ₂V = 0; (κ₂V, κλ) 2D contours; with and without an m(HH) clipping cut. No MVA unless trained and validated on statistically adequate, independent samples; if used, report the cut-based result alongside.
- **Comparison:** qualitative comparison with the published CMS boosted VBF HH→4b κ₂V result, with citation.

### 5.3 Effective-N policy for HH (declared in advance)
Brute-force N ≥ σ×L is impossible for QCD multijet. HH backgrounds instead use, in this order: (1) generator-level filters looser than the reco baseline, demonstrated safe with twin samples; (2) truth-tag weighting (every event weighted by the product of per-jet tag probabilities instead of cutting on tags); (3) the requirement that in the final signal region each background has an effective N_eff = (Σw)²/Σw² ≥ 10, or a direct upper bound with the conservative variant shown in the robustness table. `nmc_check()` is extended to apply this rule to HH backgrounds and still fails loudly on violation.

### 5.4 Combination
VH = ZH (frozen inputs from `zh-final-v1.1`) + WH: correlated nuisances (luminosity, theory per process class, photon/lepton efficiency scenarios), combined μ95 and combined λWZ results at 500/1000/3000 fb⁻¹.

---

## 6. Gates and human protocol

| Gate | When | Reviewer | Human action |
|---|---|---|---|
| G0 | setup done (§8 step 1) | — | check `SPEC.md`, approve start |
| G1 | Phase 01–03 done (each run) | reviewer on 01–03 report (multi arm) / self-review (single arm) | answer decisions D… only |
| G2 | before bulk production | reviewer on production plan + N/effective-N table | approve or return |
| G3 | final results | reviewer on final report | approve or return |
| G4 | freeze | — | tag and push |

Human rules: at each gate the human runs `/compact`, then sends the standard prompt (§7) plus only the decision answers. Any other content is logged as `corrective-intervention` with a reason. If the human uses the separate chat assistant to draft content, mark `assisted=yes`.

---

## 7. Standard prompts (use verbatim)

**S-start (multi arm, first message in `runs/multi_r1`):**
> Read ../../HANDOFF_VH_HH_multiagent.md (this file, copied to p2/) and ../../SPEC.md. You are the orchestrator of the multi arm, run multi_r1 (canonical). Perform §8 step 1 if not done, then run WH Phase 01–03 via executor-wh and HH Phase 01–03 via executor-hh in parallel, verifier for all job audits, and reviewer at G1. Append ledger lines at every phase boundary. Stop at G1 and report only: STATUS of each executor, reviewer issue lists, decisions D… needed, token/time table so far.

**S-start-repeat (multi arm r2, r3):**
> Read ../../HANDOFF_VH_HH_multiagent.md and ../../SPEC.md. You are the orchestrator of run multi_rN. Run WH Phase 01–03 only, via executor-wh, verifier and reviewer at G1, in this run directory only. Stop at G1 and report STATUS, reviewer issues, decisions D…, token/time table.

**S-start-single (single arm r1–r3):**
> Read ../../HANDOFF_VH_HH_multiagent.md and ../../SPEC.md. You are the single-agent arm, run single_rN. No subagents. Run WH Phase 01–03 in this run directory only, then self-review the 01–03 report as a referee would. Stop at G1 and report STATUS, self-review issues, decisions D…, token/time table.

**S-continue (after an interruption):**
> continue

**S-gate (G1–G3):**
> Gate <G#>. Decisions: <D1: …; D2: …>. Proceed to the next phase per the handoff; stop at the next gate with the same report format.

---

## 8. Execution order

1. **Setup (multi_r1 orchestrator, once):** create `p2/` layout (§4), `lib/` export, `SPEC.md` (conventions from §1 and §5, empty decision log, phase token budgets to be filled after Phase 01), agent files in each multi run, permission deny rules for isolation, `metrics/` with ledger schema `utc, process, arm, run_id, role, model, phase, event[start|end|gate|human_intervention|compaction|interrupt], assisted, session_id, note`, `prices.json`, extend `parse_usage.py` for per-model/per-role/per-run aggregation. Commit and push. → G0.
2. **WH Phase 01–03:** six runs (multi r1–r3, single r1–r3) from the identical start state. Runs may be parallel in separate tmux windows; record start/end in the ledger. HH Phase 01–03 runs in multi_r1 in parallel. → G1 for each run.
3. **Canonical production:** multi_r1 WH and HH (G2 before bulk submission).
4. **Final physics:** multi_r1 WH, HH, coupling interpretations; single_r1 WH Phase 05–07 on frozen samples. → G3.
5. **Combination and paper tables:** VH combination; experiment-comparison tables; the AI-metrics tables (H1–H4) with all six WH runs, the HH run and the ZH baseline. → G4: tag `p2-final-v1`, push.

---

## 9. Deliverables

- Per process: `<run>/wh|hh/reports/*` phase reports, `FINAL_report.md`, `08_reproducibility.md`, figures (PDF+PNG), `final.json`, N/effective-N table, robustness table, coupling tables.
- `combination/`: VH combination report and tables.
- `p2/metrics/`: ledger, prompts, review log, parsed token/time/cost tables per role, phase, run and arm; `AI_results.md` evaluating H1–H4 with numbers and uncertainties across repeats, and the failure-mode comparison against `metrics/ZH_failure_modes.md`.
- All limitations stated: LO, fast simulation, parametrised H→bb̄ tagging, multijet modelling, 3000 fb⁻¹ = luminosity scaling, n = 3 repeats.

**Truth boundary:** nothing in this document is evidence that any phase-2 file or result exists. Agents must inspect the tree and report only what they produced or verified.
