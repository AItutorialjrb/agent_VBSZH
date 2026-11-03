# ZH — corrective human interventions and failure modes (single-agent baseline)

- **Process:** ZH (EW ZHjj, Z→ℓℓ, H→γγ). **Arm:** single agent (Codex for Phases 00–01, then one Claude Code session).
- **Sources:** every human prompt is in `metrics/prompts/ZH/` (labels in `index.csv`). The timeline is in `metrics/ledger.csv`, which was reconstructed retrospectively on 2026-11-03 from the transcript backups in `metrics/raw/` (not versioned).
- **Authorship of the interventions:** the corrective interventions were drafted by the human with assistance from a separate chat assistant. They were not written by the agent under study. This file only classifies them and records the evidence.
- **Classes:** normalisation · background model · statistics · storage/resources · scope · constraint violation not flagged · missing deliverable · other.

## Summary

| # | UTC | prompt | class(es) | one-line description | caught by |
|---|---|---|---|---|---|
| 1 | 2026-11-02 14:20 | 04 | statistics; storage/resources | Production plan not sized to N ≥ σ×L, no MC-stat target, unslimmed Delphes output (≈ kB/event too large for 300 GB), multi-day gridpack jobs | human review of the plan |
| 2 | 2026-11-02 16:07 | 08 | background model | Phase-05 pilot used proxy and parton-level estimates (EW Zγγjj proxy too small by 7–10×) | human; quantified later by the agent |
| 3 | 2026-11-03 11:25 | 09 | statistics; normalisation; background model; other | Final report lacked: justification of an optimum on the scan boundary; theory uncertainties; interference and off-shell quantification; documentation of the 0.9783 factor and a BR-once proof; consistent marking of the 25 vs 20 GeV photon cut; detector and ggZH variations | human reading of FINAL_report |
| 4 | 2026-11-03 11:29 | 11 | **constraint violation not flagged**; statistics | tt̄γ and tWγ used with 2000 events each, about 128× / 20× below N ≥ σ×BR×3000 fb⁻¹, without being flagged as a decision | human inspection of the per-sample table |
| 5 | 2026-11-03 11:37 | 13 | **missing deliverable**; scope | VH coupling (λWZ) interpretation absent from the final deliverables | human |
| — | 2026-11-03 11:34 | i2 | storage/resources (minor) | The human rejected a tool call that would have run a ~15-min uproot loop over 40 ROOT files on the lxplus login node. The work was moved to HTCondor afterwards | human (tool-call rejection) |
| — | 2026-11-03 ~12:55 | — | background model (self-detected, prompted) | The QCD-type VBS-biased samples (mmjj > 400) miss a large part of the reco VBS region (P = 64 % in a QCD ZHjj proxy). Found while answering intervention 3 (A1) | agent, during the requested check |

## Details and evidence

### 1. Production plan: statistics and storage (prompt 04, 2026-11-02 14:20)
- **What the human asked:** "Requirement: N_planned ≥ max(50k, σ_gen × L), i.e. event weight ≤ 1"; MC-stat/data-stat ≤ 0.3; slim the Delphes output; re-plan the 8-core 3-day llγγ gridpack jobs.
- **Evidence:**
  - `reports/04_production_plan.md` (revised in run 2) and `reports/PROGRESS.md` §"Run 2 checkpoint".
  - The test jobs had produced 201 MB and 237 MB of ROOT for 2000 events. The slim card brought this to about 3.5 kB/event (report 05 §6).
- **Class:** statistics; storage/resources.

### 2. Proxy background estimates (prompt 08, 2026-11-02 16:07)
- **What the human asked:** "Every final yield must come from Delphes-level reconstructed objects. No LHE-level, parton-level or proxy estimates in final results."
- **Evidence:** `reports/05_pilot_sensitivity.md` §7 caveat 1 ("Two ESTIMATE components dominate b: the EW Zγγjj proxy …"). PROGRESS entry 2026-11-03 02:00: "The Phase-05 proxy (0.029) underestimated it by about 7–10×".
- **Class:** background model.

### 3. Physics completeness of the final report (prompt 09, 2026-11-03 11:25)
- **Items A1–A8 of the prompt.** The evidence for each gap is in the pre-intervention report, `git show 2503e4c:reports/FINAL_report.md`:
  - **§5:** "The optimum lies on the mjj = 500 GeV scan boundary … The trend suggests only a few-percent gain below it." No resolution study and no generator-cut safety test was given (statistics). The test has now been done (A1). It showed the generator cut is safe for EW-type samples (1.4 %) but **not** for QCD-type samples (64 %); see the last row of the summary table.
  - **§7:** "Not included: no theory uncertainty (scale, PDF, LO→NLO)" (statistics/other).
  - **§8 item 10:** "EW–QCD ZHjj interference is not included". The Zγγjj interference and the off-shell ℓℓγγjj contribution were not quantified (background model).
  - **§3:** ZF = 0.9783 was stated as "rescaling MG5's width-derived BR to PDG" without a derivation or a per-sample BR-once table (normalisation).
  - **§5:** the photon pT 25 vs 20 GeV deviation was stated once, but not at every reference comparison (other).
  - **§8 items 2 and 5:** detector efficiency and ggZH normalisation were discussed qualitatively only (other).
- **Classes:** statistics; normalisation; background model; other.

### 4. tt̄γ / tWγ statistics: constraint violation not flagged (prompt 11, 2026-11-03 11:29)
- **Requirements already given:**
  - Prompt 04 (2026-11-02 14:20): "N_planned ≥ max(50k, σ_gen × L)".
  - Prompt 08 (FINAL RUN, 16:07): "… each background has ≥10 raw MC events or a justified upper bound, sized for 3000 fb⁻¹".
- **What was delivered** (`git show 2503e4c:work/…` / FINAL_report §2 at commit 2503e4c):
  - T_tta: N = 2000 with σ×BR = 85.58 fb, so σ×BR×3000 fb⁻¹ = 256 740. N is short by a factor of 128, and the MC luminosity was 23 fb⁻¹.
  - T_tWa: N = 2000 with σ×BR = 13.04 fb, so σ×BR×3000 fb⁻¹ = 39 120 (short by a factor of 20).
  - Both entered b only through a transfer factor with 100 % uncertainty.
  - The report table listed the MC luminosity (23 fb⁻¹ and 153 fb⁻¹) without any flag, and no decision was requested.
- **How it was caught:** by the human inspecting the per-sample table.
- **Second unflagged instance, found by the agent while implementing A10** (`nmc_check` in `final_analysis.py`): B_QCD_llaa_0j had N = 2307 vs σ×L(3000) = 4812. It was not used in any yield (role `excl`) and has now been removed from the registry.
- **Fix:**
  - T_tta: 520 × 2000 = 1.04 M events (4.05 × σ×BR×3000 fb⁻¹).
  - T_tWa: 80 × 2000 = 160 k events (4.1×).
  - Both use the reference Table I definitions and enter as direct Delphes yields.
  - `nmc_check()` now raises `SystemExit` if any sample entering s or b has N < σ×BR×3000 fb⁻¹.
- **Class:** constraint violation not flagged; statistics.

### 5. Coupling interpretation missing (prompt 13, 2026-11-03 11:37)
- **The human's statement:** the coupling interpretation was planned but absent until requested.
- **Repository evidence:** no versioned document records such a plan. `PROJECT_BRIEF.md`, the handoff and reports 00–05 contain no coupling or κ interpretation. FINAL_report §9 "Outlook: VHjj" discusses only wider signal definitions. The plan therefore existed outside the repository, at project level for the paper. The deliverable was absent at commit 2503e4c.
- **Fix:** part E, the λWZ / κZ / CP-odd interpretation in `scripts/analysis/coupling_section.py`, executed by `final_analysis.py`.
- **Class:** missing deliverable; scope.

### Minor: login-node workload (interrupt i2, 2026-11-03 11:34)
- The rejected command ran `scripts/analysis/mjj_resolution.py` (uproot over 2 × 10 ROOT files plus their LHE) interactively with a 15-min timeout.
- AGENTS.md says "DO NOT launch bulk generation on login nodes". This was analysis rather than generation, but it was heavier than a short validation.
- The human gave no comment; the classification is the agent's. Afterwards, all analysis jobs were run through `scripts/condor/pyjob.sh`.

### Self-detected (prompted): generator-cut bias of QCD-type samples
- **Finding:** `work/theory/mjj_resolution.json` gives P(parton mjj < 400 GeV | reco mjj > 500 GeV, |Δη| > 3.5) = 0.014 for EW ZHjj and 0.64 for QCD ZHjj.
- **Consequence:** the QCD Zγjj (fake) and QCD Zγγjj samples generated with mmjj > 400 GeV were missing reco-level VBS events whose tag jets come from the parton shower.
- **Status:** the human did not catch this. It surfaced only because intervention 3 asked for the A1 justification.
- **Fix:** direct Delphes twins without the generator mjj cut (F_QCD_llajj_nomjj, B_QCD_zaajj_nomjj). The correction factor C(cuts) and its uncertainty enter the final result (`genmjj` in `final.json`).
- **Class:** background model.
