# Project rules — VBS-enriched ZH, H -> gamma gamma (Run 3 projection)

## Mission
Produce an auditable feasibility study for pp -> ZHjj (EW-induced) with Z -> e+e-/mu+mu- and H -> gamma gamma at sqrt(s)=13.6 TeV, L=500 fb^-1. Treat this as **unknown research**. Do not assume positive significance or invent any yield.

## Single Codex agent / reproducibility
Use ONE primary interactive Codex conversation throughout. Do not spawn Codex subagents, switch models, or upgrade the Codex CLI during the project. At start log `codex --version` and `/status` (model + reasoning effort) in reports/00_environment.md; keep them unchanged. Pin MG5, PY8, Delphes, Python, ROOT, PDFs, seed, cards and git commit hashes separately. If a version cannot be pinned, report it as a blocker. Resume same Codex session when returning.

## Computational environment
Operate from CERN lxplus, but DO NOT launch bulk generation on login nodes. Inspect local availability, AFS/EOS permissions, CVMFS tools, HTCondor, quotas, and network first. Use short validation tasks interactively, submit heavier jobs to batch under CERN policies. Never overwrite other user/project data. Never place API tokens in git, EOS shared paths or logs.

## Physics safety and scientific integrity
- The reference paper `reference_ZGammaGamma.pdf` is a starting point for methodology and backgrounds, NOT an answer to this process. Extract and cite its numerical setup accurately.
- Define the target gauge-invariant EW ZHjj final state and all diagrams; explicitly separate VBF-like kinematics from diagram-by-diagram (potentially non-gauge-invariant) labels. Investigate Higgsstrahlung-like contributions and interference.
- Validate MadGraph orders by output diagrams, subprocess lists and cross sections. No unverified generator syntax in production.
- H->gamma gamma is loop induced in SM; do NOT assume a tree-level `h > a a` MG5 decay-chain works. Select and validate a consistent decay implementation (e.g. PY8/MadSpin with supported decay data or validated external decay tool). Verify physical SM BR, decay flags, and event-weight normalization.
- Distinguish irreducible prompt backgrounds, reducible mis-ID backgrounds, other Higgs production modes and interference/overlap. Explicitly audit Zgamma and Zgammagamma shower overlap; choose validated matching/merging or exclusive sample definitions.
- Delphes jet->photon fake predictions are not automatically trustworthy. Use parameterized fake-rate scenarios with justified uncertainty ranges; do not label them data-driven without data.
- Keep cross sections before branching, after decay, after cuts distinct; include both Z lepton flavours and H diphoton BR exactly once.
- Every yield must come with source, selection, generator sample count, weighted MC uncertainty, and event cutflow. No reporting nominal 0 from missing Monte Carlo support as proof of negligibility.
- Reserve photon-mass sidebands / signal window, perform blinded-style selection optimization using expected yields, and report dependence on mass resolution and systematics. Avoid selecting cuts merely to maximize a noisy scan.
- Use properly tested significance methods; show Asimov stat-only as illustrative, profile-likelihood with nuisance parameters where practical, and MC-stat effects.
- Never claim an analysis result until independently reproduced by code and validated by checks.

## Required phase gates and reporting
After EACH completed phase write `reports/NN_<phase>.md` with: date UTC, status PASS/FAIL/BLOCKED, goal, inputs/version/seeds, exact commands and paths, calculations/evidence, plots/tables, checks, caveats, next actions, git commit. Also update `reports/INDEX.md` and stop at any blocked physics decision requiring human input.
Phases: 00 environment & reference audit; 01 signal/process definition; 02 background matrix & overlap; 03 generator smoke tests and cross-section consistency; 04 PS/Delphes validation; 05 baseline selection and cutflows; 06 mass-window/sideband and systematic models; 07 sensitivity and robustness; 08 reproducibility and final summary.

## First task NOW
Read `PROJECT_BRIEF.md` and reference paper, inspect current lxplus environment, write Phase 00 report, and prepare (not bulk-run) validated process cards and the background accounting plan. Do not launch extensive MC until phase-01/02 physics audits pass. Document any missing dependencies and give executable, non-destructive remedies.
