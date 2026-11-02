# VBS-enriched ZH, H → γγ — Claude execution handoff

**Handoff date:** 2026-11-02 UTC  
**Project:** `pp -> ZHjj`, `Z -> e+e- / mu+mu-`, `H -> gamma gamma`  
**Primary authoritative working tree:** `/eos/home-r/rjiang/vbs_zh_codex_starter` on CERN lxplus  
**Read this document first. Continue existing work; do not restart it.**

## 0. Instructions to the receiving Claude agent

You are joining an **existing** independent HEP feasibility study, not starting a new project. The original work was performed by a single Codex session. Your task is to continue from the real files and verified status on EOS. **The state described below is a handoff snapshot, not evidence that files currently exist on your machine.** Inspect the CERN project tree before acting. Do not re-run completed stages, reproduce the entire paper, or regenerate samples merely to reacquire context.

**First execution:** read `reports/01_signal_process.md`, `reports/01_source_control.md`, `reports/INDEX.md`, `AGENTS.md`, and `PROJECT_BRIEF.md` on EOS; inspect only the relevant candidate cards and reports. Verify present files and their status; then continue **only missing/unvalidated Phase 01 gates and Phase 02**. If a gate cannot be resolved reliably, mark it BLOCKED with exact evidence and continue independent safe work. Never fabricate generator validation or simulated yields.

Be rigorous, concise, and quota-aware. Prefer a single well-scoped execution with short reports and command/evidence references, not repetitive prose, full re-audits, or unnecessary loops. Do not re-read the entire reference PDF if `reports/00_environment.md` already contains the needed extracts; open specific pages only for unresolved issues. Preserve all completed work.

**Claude compatibility:** Claude is a separate assistant from Codex and cannot literally be the same model or the same Codex conversation. **Do not change or damage the existing Codex CLI, model, session, login, or files.** Claude may work on the same EOS working tree via an authorized terminal/Claude Code. A web-only Claude chat with no remote shell access must not pretend to have inspected or executed anything on lxplus: ask for targeted files/command output instead. Do not use Claude and Codex to write to the same files concurrently.

## 1. Non-negotiable configuration and file policy

- Persistent project root: `/eos/home-r/rjiang/vbs_zh_codex_starter` — **do not move, rename, erase, or replace it**.
- All persistent source code, Git metadata, downloads, installed research software, cards, simulation products, logs, reports and checkpoints: within that project root or another **explicitly approved EOS directory**. **No AFS** for any project artifact. An old `README.md` inside the starter bundle suggests AFS for small files; **that advice is superseded by this policy**.
- `/tmp` on lxplus: allowed only for necessary ephemeral state (SQLite/socket, temporary execution workspace); never the only copy of irreplaceable results. On HTCondor worker nodes, transient job scratch may be used with reliable EOS output staging. Avoid massive workloads on interactive lxplus nodes.
- Existing Codex installation: CLI `0.158.0`; the user requires the original **`GPT-6-Astra default`** setting, original reasoning mode and existing Codex session to remain unchanged. **No Codex update, model switch, new Codex subagents, or reinstallation.** A Codex update banner to 0.166.0 was shown and deliberately ignored.
- Existing Codex binary: `/eos/home-r/rjiang/bin/codex`; current Codex state home observed at `/eos/home-r/rjiang/.codex` (outside project but already exists — **do not migrate or modify without permission**). Login `codex login status` was successful (`Logged in using ChatGPT`). Never display or copy auth tokens.
- Run Codex with `CODEX_SQLITE_HOME=/tmp/${USER}/codex-sqlite` and `--no-daemon` because SQLite state under EOS raised `locking protocol (code: 15)`; background daemon also failed to create its Unix socket under EOS. `/tmp` is **node-local** (lxplus host changes), so session resumption must be checked rather than assumed.
- Project Git: `git rev-parse --show-toplevel` previously resolved to **parent** `/eos/home-r/rjiang`, not the project. Its HEAD was `6ea6cb9462533bbc1b209f7d4b4b67fd49b4d737` during Phase 00. **Never** change parent `.git`, run broad parent `git add .`, reset or commit unrelated content. A nested project-only Git repository has been *proposed*, not yet initialized as of the latest user-shared output; inspect `reports/01_source_control.md`, then implement only if proven safe and approved by project rules.
- Security: stay in workspace/approval mode; no destructive shell commands, unverified downloads, unchecked external scripts, or global credentials/config edits.

## 2. Physics scope and reference

Study the feasibility of measuring **electroweak `pp -> ZHjj` in a VBS-enriched region** at **13.6 TeV** with **projected** integrated luminosity **500 fb⁻¹**, `Z -> ee / μμ`, `H -> γγ`. The signal definition and expected sensitivity are **unknown and must be determined**; the requested 500 fb⁻¹ is a projection matched to the reference, **not an assertion of collected Run 3 luminosity**.

Reference local file: `reference_ZGammaGamma.pdf`, Ding et al., *Prospects for measuring electroweak production of Zγγ and 2 jets at the LHC*, arXiv:2512.07689v1 (2025). Its studied process is **EW Zγγjj continuum**, **not ZHjj**. Reuse its methodological lessons and backgrounds critically, never its signal yields or 4.50σ significance.

Reference facts already extracted in Phase 00: LO MG5_aMC 3.6.3, 13.6 TeV; Pythia8; Delphes 3.5 CMS card; generator cuts `pT(l)>10 GeV`, `pT(γ)>15 GeV`, `pT(j)>20 GeV`, `|η(l,γ)|<2.5`, `|η(j)|<5`, `ΔR>0.4`, `m(ll)>50 GeV`. QCD Zγ and Zγγ samples up to two matrix-element jets, MLM merged. Reco baseline `pT(l)>15`, `pT(γ)>20`, `pT(j)>25 GeV`, two photons + OS-SF dilepton + two jets. Reference VBS cuts `mjj>700 GeV`, `|Δηjj|>2` are **not** optimized or validated for new signal. Consult `reports/00_environment.md` for precise numerical provenance.

### Essential unresolved physics

1. **Gauge-invariant signal definition:** complete EW `ZHjj` at suitable coupling orders and all diagrams/interference; VBF-like kinematics must not be confused with an individually gauge-invariant diagram subset. Account for Higgsstrahlung-like contributions, QCD-induced `ZHjj` and possible production-mode overlap. Specify on-shell Z versus off-shell `ll`/`γ*`, consistent widths, lepton flavours, flavour scheme, PDF, coupling powers and order restrictions.
2. **Higgs decay:** `H -> γγ` is loop-induced in the SM. Do not assume a standard tree-level `h > a a` MG5 decay chain works. Select a supported Pythia8/MadSpin/external decay implementation only after checking its actual capabilities. Account for physical `BR(H→γγ)` and `BR(Z→ee, μμ)` **exactly once**, record whether sample cross sections include each decay, validate decay-filter efficiency and weighted event closure. Phase 01 static arithmetic reported `BR(Z→ee or μμ) × BR(H→γγ) = 0.00015275738`, **not a yield or universally endorsed BR choice**; inspect its assumptions and original values in `reports/01_signal_process.md` before using.
3. **Backgrounds and overlap:** irreducible prompt QCD/EW `Zγγ+jets`; continuum interference where relevant; `Zγ+jets` with one jet→γ fake; `Z+jets` double fakes; electron→γ and nonprompt leptons if justified; `tt̄γγ`, `tt̄γ`, `tWγ(γ)`, diboson+photons; **resonant** H→γγ from other Higgs production modes, not necessarily continuum background. Explicit and non-overlapping phase-space partitions/merging for `Zγ`, `Zγγ` and photon shower emissions. Fast-sim jet fake rates cannot be presented as reliable data-driven predictions.
4. **Detector & statistics:** CMS-like Pythia8→Delphes chain, validate photons, diphoton mass peak/resolution, tagging jets, jet/photon separation, b-tags, lepton selections, MET, pileup assumptions. Preserve broad `mγγ` sidebands and a properly chosen Higgs peak window, optimize using expected quantities rather than observed signal region. Include MC statistical errors, fake-rate/systematic scenarios, likelihood nuisances where feasible, and robust significance (not only ideal Asimov stat-only).

Suggested core observables: `mγγ` (full range + peak), `mll`, `mjj`, `|Δηjj|`, photon pT, diphoton pT, Z pT, centrality/Zeppenfeld variables, jet and b-jet multiplicities, MET. Every cross section and yield must identify sample definition, coupling/decay convention, branching ratio treatment, luminosity, cutflow and weighted MC uncertainty.

## 3. Completed work — do not repeat

### Phase 00 — environment and reference audit (executed; overall BLOCKED for production)

**Real EOS report:** `reports/00_environment.md` (created 2026-11-02; verified nonempty by the user). Supporting evidence: `reports/00_environment_audit.txt`, `reports/00_preflight_output.txt`, `reports/00_report_verification.txt`, `reports/00_initial_design.md`, `reports/INDEX.md` (check exact names on EOS). No simulations/jobs were launched and no software installed.

Observed: lxplus924 (earlier lxplus937/9109), RHEL9.8; Python runtime 3.9.25; ROOT 6.40.04 functioning; GCC/GFortran 11.5.0; CMake 3.31.8; `condor_submit` available, HTCondor 25.0.14; EOS CLI 5.4.9; CVMFS readable. MG5/Pythia8/Delphes executables **not on PATH**; this does not imply absent everywhere. Candidate LCG_108 stack manifests, **not validated**: `madgraph5amc 3.5.9.atlas13`, `pythia8 315`, `delphes 3.5.1pre12`, `lhapdf 6.5.5`, Python 3.12.11 and ROOT 6.36.02 in that stack. Do not silently use a patched MG5 or prerelease Delphes. AFS home was 99% full (~76 MiB free) and is off-limits for this project. EOS user quota response showed ~780 GB used and an indicated 2 TB capacity-type field; avoid confusing the mount's petabyte free-space figure with personal quota. Codex `/status` was inspected interactively and showed `GPT-6-Astra default`; `reports/00_environment.md` notes the agent's shell could not independently capture live `/status`.

### Phase 01 — **report written; BLOCKED, not signed off**

The user completed a **37m 19s** Codex run ending approximately 2026-11-02 14:01 (as reported by its interface). Codex's completion summary said:

> Created `reports/01_signal_process.md`, untested candidate cards (`cards/phase01_candidates/README.md`), and updated `reports/INDEX.md`. Phase 01 remains BLOCKED pending stack selection, flavour/width decisions, generator validation, and decay-weight closure. Static checks and branching-product arithmetic passed; no MC generated. Git isolation proposal (`reports/01_source_control.md`) recommends a nested project repository. Parent Git metadata untouched; no repository initialized. All persistent outputs on EOS. Codex CLI 0.158.0, original configuration unchanged; no subagents.

It also reported **six MG5 candidate cards**, a decay fragment, and static-only guard checks (including `cards/phase01_candidates/ew_offshell_ll.mg5` and `ew_on_shell.mg5`). Static syntax guard checks are **not successful MG5 generation or physical validation**. **Important:** the full Phase 01 files have **not** been supplied to this handoff author. The Codex completion summary above is the only evidence of their detailed contents. Claude **must read the actual EOS report/cards, not infer their exact contents from the summary**.

**No Phase 02 result, process validation, cross sections, simulated events, cutflows, backgrounds, significance or final research result has been established.** Preserve Phase 00/01 files verbatim unless a specific, documented correction is needed.

## 4. Safe lxplus shell commands (from a fresh terminal)

```bash
# Connect from your own computer, using the existing working CERN account:
ssh rjiang@lxplus.cern.ch

# Once on lxplus:
set -o pipefail
export PROJECT=/eos/home-r/rjiang/vbs_zh_codex_starter
cd "$PROJECT" || exit 1
pwd

# Show state: read-only and concise
ls -lh AGENTS.md PROJECT_BRIEF.md reference_ZGammaGamma.pdf
ls -lh reports/00_environment.md reports/01_signal_process.md reports/01_source_control.md reports/INDEX.md
find cards/phase01_candidates -maxdepth 2 -type f -print | sort
sed -n '1,220p' reports/01_signal_process.md
sed -n '1,180p' reports/01_source_control.md
sed -n '1,160p' reports/INDEX.md

# Git isolation read-only verification; do not touch parent Git metadata:
git rev-parse --show-toplevel 2>&1 || true
test -d "$PROJECT/.git" && echo 'project Git exists' || echo 'no project-local Git directory'
git status --short -- "$PROJECT" 2>&1 | head -80

# Check existing production and batch outputs before any submission:
find reports cards config scripts -maxdepth 3 -type f -printf '%p\n' 2>/dev/null | sort | head -180
condor_q -name bigbird26.cern.ch rjiang -totals 2>&1
```

**Do not run** `git init`, install software, launch MC generation, or modify existing reports merely to do this inspection. Before writing new artifacts, make sure the active shell/agent is on lxplus with the CERN-mounted EOS path and adequate permissions. Protect secrets in command output.

### Existing Codex session (only if the user chooses to return to Codex)

```bash
export PROJECT=/eos/home-r/rjiang/vbs_zh_codex_starter
cd "$PROJECT" || exit 1
export CODEX_SQLITE_HOME="/tmp/${USER}/codex-sqlite"
mkdir -p "$CODEX_SQLITE_HOME"
chmod 700 "$CODEX_SQLITE_HOME"
/eos/home-r/rjiang/bin/codex --version       # Expected 0.158.0; do not update
/eos/home-r/rjiang/bin/codex --no-daemon resume
```

Select the **original** session if available and confirm `GPT-6-Astra default` without altering it. The original session may not appear automatically after a host change because `/tmp` is local. Do not create a substitute Codex conversation before inspecting persisted session data. **For Claude, do not invoke Codex or attempt to use Codex authentication; use Claude's own authorized terminal tooling to inspect EOS.**

## 5. What Claude should do next, in order

### Step A — establish a no-duplication checkpoint (small, safe)

1. Read the **latest existing** `reports/01_signal_process.md`, `reports/01_source_control.md`, `reports/INDEX.md`, `AGENTS.md`, `PROJECT_BRIEF.md`, and candidate-card README. Inspect timestamps, actual file content and any existing progress/checkpoint file. Avoid overwriting prior scientific records.
2. Identify validated, static-only, incomplete and blocked items. Check whether any Phase 02 files, test runs, external program installations or Git isolation have appeared since the handoff; **reuse if valid**.
3. Create/update **`reports/PROGRESS.md`** on EOS, concisely recording current phase and status, verified completed outputs, hashes or source commit when available, remaining subtasks, exact next command, blocker/decision, and last UTC update. Treat it as a fast resume index, not a replacement for reports. Only write it after inspecting the real tree. Do not duplicate entire earlier reports.
4. Check the source-control proposal for nested project Git. Do not change the parent repo. If nested Git on EOS is safe and consistent with the existing proposal, document a minimal **project-only** workflow; leave potentially risky initialization for explicit approval.

### Step B — close feasible Phase 01 gaps without unnecessary reruns

Review the **actual six candidate MG5 cards** and decay fragment. Determine which are physically meaningful hypotheses, what syntax/order restrictions are supported, and what is still unverified. Select an explicit tested generator stack **only after checking availability/compatibility**, without blindly accepting an `atlas13` patch or pre-release Delphes. If tools are not ready, create validated installation/activation and minimal smoke-test scripts for future execution rather than pretending cards ran. Avoid changing previous Phase 01 claims without evidence.

Resolve flavour and on-/off-shell Z/γ* and widths as far as science allows. Flag decisions requiring the user. Verify the BR convention, numerical inputs, normalization closure plan and gauge-invariant perturbative-order definition. Clearly separate **documentation/static audit** from **executed physics validation**. If Phase 01 remains BLOCKED, preserve its status and create a focused addendum; do not spend quota rewriting the entire report.

### Step C — proceed with Phase 02 background & overlap accounting (the main next deliverable)

Build a **process ledger**, not a speculative ranking. For each background/component document physics role (irreducible/fake/resonant), intended generator order, expected photon/lepton source, inclusive/exclusive jet definition, decay/BR factors, phase-space matching/merging, overlap and interference risks, phase-space validation, uncertainties and required checks. Cover at minimum:

- prompt EW and QCD `Zγγ + jets` and possible interference;
- `Zγ + jets` one jet→γ fake and `Z + jets` two photon fakes, both with an explicit parametrized fake-rate/uncertainty strategy;
- top (`tt̄γγ`, `tt̄γ`, single top), dibosons and any additional prompt/fake processes materially relevant to the final state;
- resonant `H→γγ` from other production modes / `ZHjj` production orders (clear measurement-dependent classification);
- photon FSR/ISR, ME–shower overlap, parton-jet multiplicity binning, matching/merging, lepton and object misidentification.

If evidence supports a negligible component, **justify it**; do not equate zero generated events with zero physics. Specify robust but cost-conscious MC-statistics planning. Do **not** claim measured fake rates from Delphes alone. Avoid production until the sample ledger/generator/decay accounting is validated.

Write **`reports/02_background_overlap.md`** and corresponding concise, explicitly labeled **candidate/unvalidated** generator input cards or machine-readable sample matrix as appropriate. Update `reports/INDEX.md` and `reports/PROGRESS.md`. Each stage report must include UTC date, status PASS/BLOCKED/FAIL, inputs and versions, commands/evidence, checks, scientific decisions, caveats and next actions. Keep main summaries compact; place long raw logs separately only if generated.

### Step D — downstream phases only when gates pass

- **03:** minimal MG5 generation smoke tests, process/coupling-order checks, diagrams, cross sections, decay/BR closure, seeds and MC-stat consistency; move bulk work to HTCondor, never login node.
- **04:** Pythia8 shower/matching and Delphes CMS card; photon ID, mass resolution, physics-object validation, fake-model limitations.
- **05:** reproducible baseline selection, cutflows, weighted distributions and errors; cut definitions chosen with honest MC-stat constraints.
- **06:** Higgs diphoton signal window and sidebands, fit/background-shape and systematic scenarios.
- **07:** statistical sensitivity and robustness, profile likelihood where feasible, nuisance/MC-stat uncertainties, no unjustified observation claims.
- **08:** independent reproducibility audit, final report, exact dependency versions, scripts/cards, checksums, seeds and all limitations.

## 6. Safe resume and resource-efficiency rules

- **Never rerun completed, checked work** merely because the assistant changed. Open existing report and output; verify metadata/hash when needed, then continue only missing pieces.
- If a job/test partially completed, compare input cards, hashes, seeds, IDs, event counts, log exit status and output completeness. Only rerun failed/missing segments. Avoid double-counting resumed datasets or overlapping HTCondor submissions.
- If a model quota/session ends, resumption starts with `reports/PROGRESS.md` and the specific latest phase report, **not a full environment scan or full reference-PDF reread**. Recover actual state from files and the scheduler if progress note is stale.
- At each major successful checkpoint write the **minimal restart instructions** and output list to `reports/PROGRESS.md`. If interruption is abrupt, reconstruct state from EOS files and active job statuses without guessing.
- Use small, reversible checks first; perform detailed validation where it changes a physics result; avoid repetitive near-identical command invocations, verbose full-file dumps and speculative installations.
- Never declare a phase PASS unless its stated acceptance criteria are met with executed evidence. A documented BLOCKED outcome is acceptable.
- Before any HTCondor campaign: require audited process cards, software availability, intended output directory and quota, expected resource needs, seed separation, retry rules, and reliable EOS stage-out. Do not submit duplicate jobs.

## 7. Immediate Claude prompt (copy/paste if the Markdown is provided as a file)

> Continue the **existing** CERN EOS VBS ZH, H→γγ project using this handoff and the real files at `/eos/home-r/rjiang/vbs_zh_codex_starter`. Do not start a new project, disturb Codex, use AFS, change the root directory, redo Phase 00 or regenerate Phase 01. First inspect `reports/01_signal_process.md`, `reports/01_source_control.md`, `reports/INDEX.md`, `AGENTS.md`, `PROJECT_BRIEF.md`, existing candidate cards and any later progress artifacts. Verify completed work and create a concise `reports/PROGRESS.md` checkpoint. Then close only feasible missing Phase 01 audit items and deliver Phase 02's rigorous background/sample-overlap ledger and `reports/02_background_overlap.md`. Preserve scientifically justified blockers; no bulk MC or unsupported generator claims. Use EOS only for persistent outputs, a single authorized execution agent, concise evidence-backed reports, and do not touch the parent Git repository. Continue until the safe scoped work is done; stop only on a material physics/security blocker. If you have no lxplus shell access, say so and request only the specific EOS files or command outputs needed to continue — do not claim work was executed.

---

**Truth boundary:** This handoff includes direct user-shared terminal evidence and Codex's reported completion summary. The detailed contents of Phase 01 artifacts and their current EOS existence must be checked on CERN before making new conclusions. No generated-event physics result has yet been provided to the handoff author.
