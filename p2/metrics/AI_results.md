# AI results: single-agent vs multi-agent (p2, WH H→γγ VBS study), G4

Written by the multi_r1 orchestrator on 2026-11-16 under D48 (G4 (b), (c)).
- **Machine-readable sources:**
  - `metrics/g4/ai_metrics.json` (script `metrics/g4/ai_metrics.py`);
  - `metrics/g4/g4a_results.json`, `metrics/g4/blind/`;
  - `metrics/g4/condor_core_hours.json`;
  - `metrics/usage_events_p2.csv` (per message, from `metrics/parse_usage.py --events`);
  - `metrics/ledger.csv`, `metrics/prompts/*.csv`, `metrics/review_log.csv`.
- **Cost:** cost-equivalent USD from `metrics/prices.json` (list prices per model, cache read and write priced separately).
- **Active time:** the union of inter-message gaps under 10 min.
- **Wall time:** first event → gate.

**Design reminder (HANDOFF §2, SPEC §1):** 3 multi-agent repeats (multi_r1–r3) vs 3 single-agent repeats (single_r1–r3), all on WH Phase 01–03 from the same SPEC_G0.
- **multi_r1:**
  - It also ran HH (stopped by amendment A1; excluded from the WH comparison).
  - It ran the ZH erratum (reported separately).
  - It continued WH to the final result with its own production (wh-prod-v1/v1.1/v1.2) and the joint VH combination.
- **single_r1** continued to the final WH result on the *frozen* multi_r1 production samples (amendment A2). It did no production of its own except one H_ggF_jj_nomjj gridpack.
- **The end-to-end comparison is n = 1 per arm and covers different scopes;** see §2.

## 0. Exclusions (not counted in any run's totals)

| item | run | cost-eq | tokens | active | human msgs | treatment |
|---|---|---|---|---|---|---|
| single_r1 launched twice (~2026-11-08T20:15Z); both sessions stopped by the human (sessions e11a5b3e*, ffcf95fa*) | single_r1 | $4.25 | 6.87 M | 0.14 h | 4 | human error; outputs in p2/_to_delete/ |
| multi_r2 start prompt pasted into the multi_r1 session (2026-11-08T20:14:43–20:29:58Z) | multi_r1 | $3.12 | 11.97 M | 0.25 h | 1 | human error; not acted on |
| G4 evaluation (blind-audit reviewers, metrics scripts, this file) | multi_r1 | ≥ $0.92 at the last parse (still growing; final value in ai_metrics.json `excluded.multi_r1:g4_eval`) | — | — | — | evaluation, not analysis work |
| Pause 2026-11-04T13:40Z → 2026-11-06T12:57Z (credit limit) | multi_r1 | — | — | — | 1 (pause order) | wall time only; active-time metric unaffected |
| single_r1 idle 2026-11-09T13:56Z → 2026-11-13T18:08Z (background waiter reaped by Claude Code; session idle until a human "continue") | single_r1 | — | — | — | 1 (continue) | inside the P01–03 wall window; see H4 |
| multi_r1 session interruptions (2026-11-03 17:45–21:26Z restart; 2026-11-04 API usage-limit stop; 2026-11-13 session end) | multi_r1 | — | — | — | 3 (continue) | wall only |

## 1. Hypotheses H1–H4 (WH Phase 01–03, 3 vs 3 repeats)

### H1, correctness
**Claim tested:** the multi-agent arm reaches each gate with fewer unresolved severity-1 physics issues.

**Method (G4 (a)):**
- The six G1-state Phase 01–03 reports were stripped of arm and run identifiers (seed run indices, paths, model and role names masked) and labelled A–F with a random key (seed 20261115, `g4/blind_key.json`).
- One fresh opus reviewer per report applied one fixed rubric (`g4/blind/RUBRIC.md`, fixed before any audit ran).

| run | label | unresolved sev-1 | flagged-open sev-1 |
|---|---|---|---|
| multi_r1 | B | 1 | 8 |
| multi_r2 | E | 3 | 8 |
| multi_r3 | F | 3 | 8 |
| single_r1 | D | 2 | 7 |
| single_r2 | A | 1 | 9 |
| single_r3 | C | 0 | 9 |
| **multi mean ± sd** | | **2.33 ± 1.15** | 8.0 ± 0 |
| **single mean ± sd** | | **1.00 ± 1.00** | 8.3 ± 1.2 |

- **Exact permutation test** (20 relabellings, one-sided for multi < single): p = 0.95.
- **Verdict: H1 not supported.** The direction is opposite to the hypothesis. With n = 3 + 3 the difference is not significant either way (two-sided p = 0.30; p(multi ≥ single by this much) = 0.15).
- **Issues found across both arms** (`g4/blind/audit_*.md`):
  - resonant tHq / top contamination in the 5-flavour signal definition;
  - a missing lepton-FSR (W→ℓνγ) photon class;
  - gaps in the lost-lepton background.
- **Blinding limitations** (recorded by the reviewers, not counted):
  - report E had one number corrupted by seed masking (a Γ(W→ℓν) digit), which the reviewer flagged and did not count;
  - report A kept 9-digit seed strings, which could in principle identify a run but do not identify the arm.
- **The audit is of the G1 *report state*, not of the code:**
  - Multi arms ran their own opus reviewer at G1. The issues that review raised were fixed or raised as decisions *after* G1, so they do not show up here.
  - The single arm's self-review is part of its report state.

### H2, human load
**Claim tested:** fewer corrective human interventions per phase.

| run | human msgs P01–03 | of which corrective | what they were |
|---|---|---|---|
| multi_r1 | 2 | 0 | start prompt; "continue" after a session restart |
| multi_r2 | 1 | 0 | start prompt |
| multi_r3 | 1 | 0 | start prompt |
| single_r1 | 2 | 0 | start prompt; "continue" after the waiter was reaped |
| single_r2 | 1 | 0 | start prompt |
| single_r3 | 1 | 0 | start prompt |

- **Corrective interventions per phase: 0 in both arms** (0/3 phases × 3 repeats each).
- **Verdict: H2 not testable at this sample size.** No corrective intervention was needed in either arm in Phase 01–03, so both arms score 0. Both arms improve on the ZH single-agent baseline: 5 corrective interventions over its whole run, of which 0 in Phase 00–01 (§3).
- **G1 gate prompts (not counted as P01–03):**
  - multi_r1's G1 gate prompt answered D-WH-0..6 and D-HH-1..12 and contained metrics corrections, so it is classified "gate + corrective-intervention" in `prompts/multi_r1.csv`.
  - single_r1's G1 prompt accepted the declared defaults.
  - The repeats r2/r3 stopped at G1 by design.

### H3, economy
**Claim tested:** fewer cost-equivalent tokens per completed phase. Scope: WH roles only; multi_r1 executor-hh is excluded.

| run | cost-eq | per phase (÷3) | tokens (in + cache + out) | output tokens | API msgs |
|---|---|---|---|---|---|
| multi_r1 | $17.88 | $5.96 | 63.3 M | 457 k | 379 |
| multi_r2 | $11.32 | $3.77 | 32.6 M | 281 k | 287 |
| multi_r3 | $6.86 | $2.29 | 18.3 M | 171 k | 151 |
| single_r1 | $17.08 | $5.69 | 28.6 M | 176 k | 126 |
| single_r2 | $10.99 | $3.66 | 21.5 M | 143 k | 108 |
| single_r3 | $11.77 | $3.92 | 21.9 M | 160 k | 107 |
| **multi mean ± sd** | **$12.02 ± 5.54** | $4.01 | 38.1 ± 23.0 M | | |
| **single mean ± sd** | **$13.28 ± 3.31** | $4.43 | 24.0 ± 4.0 M | | |

- **Cost ratio multi/single:** 0.91 on the mean, 0.96 on the median. Permutation p(multi ≤ single) = 0.45.
- **Verdict: H3 not supported.** The cost is equal within the spread. The multi arm uses about 1.6× more tokens, but they are cheaper:
  - multi_r1 P01–03 WH: executor (sonnet) $8.12, orchestrator (opus) $6.86, reviewer (opus) $2.71, verifier (haiku) $0.20.
  - The single arm runs everything on opus with fewer messages.
- **The mechanism the hypothesis names does operate** (high-volume work on cheaper models; logs kept out of the orchestrator context). It is offset by:
  - opus reviewer and orchestrator overhead;
  - each executor re-reading context, since cache reads dominate the token count.
- **multi_r1 all roles, including HH:** $26.58 for P01–03.

### H4, time
**Claim tested:** wall time per phase is not worse than single by more than 20 %.

| run | wall P01–03 | active P01–03 |
|---|---|---|
| multi_r1 | 6.44 h | 2.19 h |
| multi_r2 | 16.74 h | 2.81 h |
| multi_r3 | 4.15 h | 0.85 h |
| single_r1 | 117.69 h raw; 17.5 h without the 100.2 h idle (§0) | 0.93 h |
| single_r2 | 3.95 h | 0.63 h |
| single_r3 | 3.92 h | 0.60 h |
| **multi median (mean ± sd)** | **6.44 h** (9.11 ± 6.71) | 2.19 h (1.95 ± 1.00) |
| **single median (mean ± sd)** | **3.95 h** (8.5 ± 7.8 with the idle removed) | 0.63 h (0.72 ± 0.18) |

- **Ratio multi/single:** wall 1.63 on the median; active 3.5 on the median, 2.7 on the mean.
- **Verdict: H4 not supported.** The multi arm is more than 20 % slower on the median wall and active time.
  - **Wall time** is dominated by condor gridpack and test-job waits. That is why multi_r2 (one 847 core-h cluster) took 16.7 h.
  - **Active time** is the cleaner measure of agent work, and the multi arm spends about 3× more, mostly in orchestrator↔executor round trips and gate reviews.
  - **The raw mean** (multi 9.1 h vs single 41.9 h) would favour multi only because of the single_r1 idle period, which is a tool failure. It is not used.

### Summary
| | H1 correctness | H2 human load | H3 economy | H4 time |
|---|---|---|---|---|
| multi (mean ± sd) | 2.33 ± 1.15 unresolved sev-1 | 0 corrective | $12.0 ± 5.5 | 6.4 h median wall, 2.2 h active |
| single (mean ± sd) | 1.00 ± 1.00 | 0 corrective | $13.3 ± 3.3 | 4.0 h median wall, 0.6 h active |
| verdict | not supported (p = 0.95) | not testable (both 0) | not supported (equal within spread) | not supported (×1.6 wall, ×3.5 active) |

**Caveat that applies to all four:** n = 3 per arm; each run is one stochastic trajectory. The HEPTools environment difference (multi_r1 started without it, all repeats with it; SPEC §7) and multi_r1's partly non-native role spawns before its restart are documented confounders.

## 2. End-to-end: single_r1 vs multi_r1 (n = 1 each, unequal scope)

### Scope
| | single_r1 | multi_r1 |
|---|---|---|
| phases | 01–03, 05–07 (no 04: used frozen wh-prod-v1/v1.1) | 01–08, own production v1/v1.1/v1.2, 05a background model, joint VH combination with ZH, toys, paper package |
| production | one gridpack (H_ggF_jj_nomjj) | 2688+ ROOT files, 128 GB (v1) + v1.1 + v1.2 rows |
| independent review | self-review only | haiku verifier on every job/number; opus reviewer per gate |

### Results (500 fb⁻¹, signal def (a) unless stated)
**WH at 500 fb⁻¹** (sources: single_r1 `runs/single_r1/wh/reports/final.json`; multi_r1 `runs/multi_r1/wh/reports/final.json` and `combination/VH_combination.json`/`_mu95.csv`, R2 regeneration):

| quantity | single_r1 | multi_r1 |
|---|---|---|
| primary selection | BDT (cut-based alongside) | cut-based (MVA on HOLD at 05; frozen) |
| s / b (window) | 1.19 / 1.26 | 0.612 / 1.747 |
| Z (Eq. 1) | 0.94 (cut-based 0.58) | 0.440 |
| Z0 (profile likelihood) | — (counting / fit / CLs) | 0.445 stand-alone (stat-only 0.458); joint workspace 0.456, toy 0.425 |
| μ95 median | 3.50 exact Poisson (cut-based 5.07) | 8.08 exact Poisson; PL 6.58 stand-alone, 6.41 joint workspace; toy 7.12 ± 0.30 (+2.4σ_fit above asymptotic; asymptotic likely low by 10–25 %, not validated) |
| λWZ = −1 exclusion | 4.2σ, rate-only, BR fixed to SM | 3.77σ (κZ-sign, R_BR included; convention-independent primary); 6.20σ in the κW-sign convention; median-q toy 3.92σ (SM pseudo-data); λ=−1 thrown toys follow χ²₁ to p ≈ 0.001, the 3.8σ tail itself is not toy-resolved |
| lost-lepton QCD row | — | D49 option 4: 0.121 [0.003, 0.68] in the m_γγ window (PL template normalised to it after the final-review fix R4). At the upper end, Z0 0.379, μ95 7.82; λ=−1 unchanged (3.77σ) |

**multi_r1 only, VH combination at 500 fb⁻¹, def (a):**

| channel | Z0 | μ95 median |
|---|---|---|
| WH | 0.456 | 6.41 |
| ZH (corrected) | 0.131 | 32.3 |
| VH | 0.473 | 6.01 (±1σ band 3.87–9.66) |

- Toys: VH Z0 0.461, μ95 6.82 ± 0.58 (fit error understated: seeds reused across μ points).
- λ = −1 for VH: 3.78σ (κZ-sign), 6.24σ (κW-sign).
- Def (b): VH Z0 0.56, μ95 5.03.
- At 3000 fb⁻¹: VH Z0 1.10, μ95 2.06.
- Channel compatibility: the SM Asimov point has p = 1 by construction. Expected sensitivity is p = 0.03 at (μ_WH, μ_ZH) = (1, 32) at 500 fb⁻¹.

**Reading:**
- The single_r1 Z is about 2× multi_r1's. This comes from the BDT (single_r1's own cut-based Z of 0.58 is closer) and from a lower b, since single_r1's j→γ parametrisation under-predicts Delphes by about 5× (S2-8, open).
- The two results are not independent: they share the samples.

### Issues
| | single_r1 | multi_r1 |
|---|---|---|
| G1 blind audit (unresolved sev-1) | 2 | 1 |
| own review sev-1 at final | 3 (self-review 05–07: S1-9 BDT stability marginal, S1-10 e→γ non-closure ×4, S1-11 jet-modelling nuisance) plus S2-8 (j→γ parametrisation under-predicts Delphes ~5×) | 0 open at the G3 final (one sev-1 relabel fixed; D20 auto-pass); final round: all verifier sev-1 fixed (§3) |
| independent sev-1 caught by reviewers (WH) | — (no independent reviewer) | ≈ 18 over G1, G2, G2 recheck, production validation, 05a, 05, G3 (§3) |
| constraint violations on the ledger | 0 | 4 (2 HH, 2 WH/shared; all flagged by the agents themselves) |
| interrupts (ledger) | 1 | 18 |

### Cost, tokens, time, prompts (exclusions in §0 applied)
| | single_r1 E2E | multi_r1 WH E2E to first final (2026-11-13T18:25Z) | multi_r1 FINAL-R2 round | multi_r1 HH (stopped) | multi_r1 ZH erratum |
|---|---|---|---|---|---|
| cost-eq | $30.94 | $145.39 | E2E_R2_COST | $19.31 | $2.90 |
| tokens | 59.8 M | 557.1 M | E2E_R2_TOK | 89.5 M | 10.9 M |
| output tokens | 0.39 M | 3.24 M | E2E_R2_OUT | 0.47 M | 0.04 M |
| active | 1.90 h | 14.77 h | E2E_R2_ACT | 3.48 h | 0.86 h |
| wall | 134.4 h (incl. 100.2 h idle) | 242.9 h (incl. the 47 h pause) | E2E_R2_WALL | | |
| human msgs | 3 (start, continue, G1 accept) | 14 | E2E_R2_HUM | | |
| condor core-h (since 2026-11-03; lower bound) | 379 | 7791 (WH) + 28 (combination) | | 145 | in "ZH tree" 1959 |

- **Scale:** multi_r1's end-to-end WH work cost about 4.7× more than single_r1 and took about 7.8× more active time.
- **Most of that is scope**, not arm efficiency:
  - full production with N-rule enforcement (the 7791 core-h);
  - the 05a background model with three production rounds;
  - the joint VH workspace.
- **No like-for-like end-to-end cost ratio is possible from n = 1 with different scopes.**

### Human prompts, multi_r1 (14 up to the first final, plus 3 in FINAL-R2; `metrics/prompts/multi_r1.csv`)

| class | count | notes |
|---|---|---|
| task (start) | 1 | |
| continue | 4 | after restarts and usage-limit stops |
| pause | 1 | |
| gate + corrective | 1 | the G1 prompt |
| decision | 3 + 3 | including the FINAL-R2 rounds D39–D48, D49 and D50 |
| corrective (human error) | 1 | wrong-session prompt, excluded |

- Decisions answered by the human: D1–D50 in SPEC §6.
- **Most human load in multi_r1 came from physics decisions the agents raised** (about 50 D-items). In ZH the load came from corrective interventions.

## 3. Failure-mode comparison against the ZH baseline (G4 (c))

**Baseline:** `metrics/ZH_failure_modes.md`. Single agent, 14 human msgs, 666 API msgs, 0.79 M output tokens, 2375.6 core-h (`metrics/usage_by_phase.md`). It had 5 corrective interventions plus 2 minor items.

| ZH failure class (# in ZH_failure_modes.md) | ZH: caught by | multi_r1 WH | single_r1 WH |
|---|---|---|---|
| 1. statistics/storage: production not sized to N ≥ σ×L, unslimmed output | human | **prevented by design:** N rule in SPEC §1.5; slim cards; plan reviewed at G2; `nmc_check` fails loudly. Two reviewer sev-1 catches where the code silently dropped rows from the check (G1 I_WHjj N = 20k; G2-recheck Q_aajj "PASS" hiding 3 rows) | used frozen production; N check passed (2900/2900 SHA, D-WH-2/3) |
| 2. background model: proxy / parton-level estimates in a final yield | human | reviewer sev-1 at G2 (non-prompt-lepton class only an ε-assumption estimate; tt̄ off by 36×) → Q_aajj / Q_aajjj / H samples produced; 05a sev-1 (light-misID bound, ZH rows 13× mis-normalised, C factors not applied) caught by the reviewer before use | self-review S1-10 (e→γ non-closure ×4) and S2-8 (j→γ parametrisation ×5) flagged by the agent itself, left open |
| 3. statistics/normalisation completeness of the final report (boundary optimum, theory unc., interference, BR-once proof) | human | BR-once ledger and theory uncertainties in the SPEC from G0; statistics errors (q0 factor 2, Asimov bias) self-found by the executor before use; final-round verifier caught toy seeds unused, a ZH Z0 threshold artefact, a μ95 grid plateau and an undeclared POI; G3 reviewer sev-1 on labelling | own systematics model (theory from own weights, JES with BDT rescoring); BDT stability marginal (S1-9), self-flagged |
| 4. **constraint violation not flagged** (N rule) | human | flagged violations: 4 on the ledger (HH pilots before G2; HEPTools install; two WH). One N-rule *hiding* caught by the reviewer (G2 recheck), not by a human | none recorded |
| 5. **missing deliverable** (coupling interpretation) | human | prevented: λWZ, (κW, κZ) and c_A in the SPEC deliverables from G0; delivered for WH, ZH, VH | delivered (λWZ, κW, κZ; rate-only, BR fixed to SM: a scope difference) |
| minor: login-node workload | human (tool rejection) | 0 human rejections; all > 10 min work on condor per brief; executor-hh's interactive MG5 loop_sm write into the shared install was self-flagged (constraint violation, D-HH-1) | 0 |
| self-detected: generator-cut bias of QCD samples (mjj > 400) | agent, prompted | built in: D8 (no generator mjj cut on QCD samples) plus `_nomjj` twins. D49 deviation for the lost-lepton QCD row, a human decision; resolved as the one-event estimate (option 4, D50) | inherited the frozen twins |

**Reading of the comparison:**
1. **ZH needed 5 corrective interventions; the multi arm needed none of those classes.** All five ZH classes were either written into SPEC_G0 as rules (N rule, BR-once, coupling deliverables, no proxy yields) or caught by the opus reviewer or haiku verifier before a human saw them.
   - **Confound:** the SPEC itself was written *after* ZH. Part of the gain is the lessons-learned SPEC, not the arm. The single-agent repeats had the same SPEC_G0 and also needed 0 corrective interventions in Phase 01–03 (H2).
2. **New failure modes in the multi arm that ZH did not show:**
   - **code silently relaxing a rule:** `nmc_check` exclusions, and a fold-RMS stability criterion chosen after seeing the folds;
   - **leakage between pipeline stages:** m_γγ rebuilt from BDT inputs; a lepton-contaminated j→γ rate table used to size top-ups;
   - **scope expansion before a gate:** HH pilots counted toward production.
   - All were caught by the reviewer or verifier, not by a human. They cost reruns (the contaminated-rate top-ups were kept but re-justified) and extra rounds: 05a HOLD → v2, 05 MVA HOLD, G3 HOLD → relabel.
3. **Single-arm residuals (single_r1):** the same physics weak points (non-prompt photon calibration, e→γ closure, BDT stability) are present and *flagged* by its self-review but not fixed. With no independent check, nothing forces a fix. Its headline Z (0.94, BDT) is about 2× the multi_r1 WH Z (0.44 Eq. 1; PL 0.445). This is consistent with the open S1-9/S1-10 items, but it is not proven by them.
4. **Remaining human load in multi_r1 is decisions, not corrections.**
   - The agents raised about 50 D-items.
   - The human answered about 10 with non-default choices: H1 fake-factor nominal, A1 stop HH, A2, D29/D30, D42, D46, D49, D50.
   - This matches the ZH "missing deliverable / scope" class turning into explicit decision requests.

**Reviewer/verifier sev-1 catches, multi_r1 WH** (from `runs/multi_r1/reviews/wh_*.md`):

| gate | sev-1 catches |
|---|---|
| G1 | 2 |
| G2 | 1 |
| G2 recheck | 4 |
| production validation | 2 |
| 05a | 4 |
| 05 | 1 (plus 2 protocol items in SPEC §7) |
| G3 | 1 |
| **total** | **≈ 15–18** |

Final-round verifier sev-1 catches:

| block | sev-1 catches |
|---|---|
| Part B | 2 |
| v1.2 (became D49) | 1 |
| workspace | 5 |
| toys | 4 |
| paper | ≥ 4 |
| R2 recheck (workspace/toys: stale VH headline; production and paper: D49 option 4 not shown) | 3 |
| final-package review (opus): LLQ PL template normalised over 100–180 GeV, not to the D49 window yield (≈2.1 Y0 in the window; upper end ≈2.1× too high) | 1 |

None reached a human as a correction.

The final-review catch is the clearest example of the gate structure working. Three haiku verifier passes had checked every number against its source key, and all of them passed this inconsistency. It was a mismatch between the decision's definition (a window yield) and how the code implemented the template. Only the opus physics review caught it.

It changed the WH stand-alone headline from 0.428 / 6.81 to 0.445 / 6.58, and the D49 upper end from 0.309 / 10.9 to 0.379 / 7.82.

## 4. Totals and compute
- **Condor core-h since 2026-11-03** (`g4/condor_core_hours.json`; lower bounds, history retention):

  | directory | core-h |
  |---|---|
  | multi_r1/wh | 7791 |
  | multi_r1/hh | 145 |
  | combination | 28 |
  | multi_r2 | 847 |
  | multi_r3 | 1.3 |
  | single_r1 | 379 |
  | single_r2 | 283 |
  | single_r3 | 226 |
  | ZH tree (erratum checks + earlier) | 1959 |

- **G4 evaluation cost (excluded):** G4_EVAL_COST.
