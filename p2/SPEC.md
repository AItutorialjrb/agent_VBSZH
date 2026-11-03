# p2 SPEC — shared conventions and decision log (WH and boosted VBF HH→4b)

**Owner:** multi_r1 orchestrator (edits only via the decision log below). **Created:** 2026-11-03 UTC (§8 step 1, multi_r1).
**Binding source:** `p2/HANDOFF_VH_HH_multiagent.md` (the handoff). Where this file and the handoff disagree, the handoff wins and the disagreement is a decision item.
**ZH baseline:** tag `zh-final-v1.1` = commit `5785329d651835336af3f23dc8882cc00777384b`, read-only. Code reuse only via `p2/lib/` (read-only `git archive` export; checksums in `p2/lib/SHA256SUMS`).

---

## 1. Non-negotiable policies (from handoff §1)

1. Persistent artifacts on EOS under `/eos/home-r/rjiang/vbs_zh_codex_starter`. No AFS. `/tmp` only for transient state.
2. Never touch `/eos/home-r/rjiang/.git`, Codex, or `~/.codex`.
3. **ZH frozen.** Never modify `reports/ cards/ config/ scripts/ work/ production/ figures/` at the repository root (or anything else reachable from `zh-final-v1.1`). Reading frozen ZH samples/reports is allowed. Never modify `p2/lib/`; changes go into the process directory as patch files with a one-line rationale (`<proc>/patches/NNN_<name>.patch` + entry in `<proc>/patches/README.md`).
4. Final yields at **Delphes level only**. LHE/parton/proxy numbers may appear only as validation, labelled as such.
5. **N_MC ≥ max(50k, σ×BR×3000 fb⁻¹)** for every sample entering s or b, enforced by code that fails loudly (reuse `lib/scripts/analysis/final_analysis.py::nmc_check`). HH backgrounds: effective-N policy (§4.3). Any shortfall is a numbered decision, never a silent relaxation.
6. **BR applied exactly once** per sample, asserted in code by a per-sample BR ledger (reuse ZH ledger incl. ZF = 0.9783 MG5-LO→PDG Z→ℓℓ factor; derive the analogous W factor WF = B_PDG(W→eν+μν)/B_MG5-LO(W→eν+μν) from the model's widths and document it).
7. HTCondor bulk only after a successful test job; no duplicate submissions (check `condor_q` first); EOS stage-out; seeds unique per (process, run_id, job) — seed scheme §3.4.
8. Storage ≤ 400 GB logical for all of phase 2. Slim Delphes output only (`lib/cards/phase04_candidates/delphes_card_CMS_slim_v1.tcl`, extended for HH objects as a patch).
9. Do not launch bulk generation on lxplus login nodes. Short validation tasks interactively; heavier work to batch.
10. No API tokens/secrets in git, EOS shared paths or logs.

## 2. Common physics configuration (handoff §5)

| Item | Value |
|---|---|
| √s | 13.6 TeV |
| Luminosities | 500, 1000, 3000 fb⁻¹ (3000 = luminosity scaling with the Run-3-like Delphes card, not an HL-LHC prediction) |
| Generator | MG5_aMC v3.6.3 (upstream, as installed for ZH under `software/`), LO |
| Shower | Pythia8 from LCG_110 (as ZH) |
| Detector | Delphes, slim CMS card as ZH (`delphes_card_CMS_slim_v1.tcl`) |
| Theory unc. | 7-point scale ⊕ PDF from MG5 weights |
| Results | expected only (Asimov / expected counts); never optimise on an observed SR |
| Stack setup | reuse `lib/scripts/setup_stack.sh`, `lib/scripts/run_py8_delphes.sh`, `lib/scripts/condor/*`; ZH Phase-03 stack record: `reports/03_stack.md` (read-only) |

### 2.1 WH (EW W±Hjj, W→eν/μν, H→γγ) — handoff §5.1
- Phase 01: gauge-invariant EW W±Hjj at amplitude orders (QCD, QED) = (0, 4), both charges, W decayed in MG5 (BR ledger + WF), H→γγ forced in Pythia8 with SM BR applied once; QCD W±Hjj as resonant background (def. a) and inclusive-signal variant (def. b); interference statement.
- Phase 02: background/overlap ledger — at minimum EW/QCD Wγγjj; Wγ+jets (j→γ fake, direct Delphes); W+jets double fake (quantitative bound); tt̄γ(γ), tWγ (single-lepton); tt̄H, tHq/tHW; ZHjj and Zγγjj with one lost lepton reusing frozen ZH samples where phase space covers it; QCD γγ+jets with non-prompt lepton (bound); hard/soft photon overlap removal as ZH; generator-cut safety via twin samples.
- Phase 03: smoke tests, σ closure, BR closure, Delphes object validation (MET resolution, lepton, photon, mγγ, VBS jets), one condor test job per sample type.
- Phases 04–07 per handoff §5.1 (canonical arm). Coupling interpretation (λWZ) per handoff §5.1.

### 2.2 Boosted VBF HH→bb̄bb̄ — handoff §5.2
- Boosted category only (2 large-R H→bb̄ candidates + 2 VBS tagging jets, high m(HH)); resolved = outlook.
- Signal EW pp→HHjj (QCD=0), H→bb̄ in Pythia8 (BR once); six-point (κV, κ₂V, κλ) basis, morphing, closure on ≥2 independent points. Primary κ₂V, secondary κλ.
- Backgrounds: QCD multijet (bb̄bb̄; bb̄+light/c with mistags); tt̄ (all-had, semi-lep); ggF HH (κλ-dep.); single H (tt̄H, VBF H, ZH/WH V→bb̄/qq̄, ggH+jets); Z/W(→qq̄)+jets; VBS/VBF ZZ, ZH Z→bb̄.
- Objects: check Delphes CMS card for large-R jets with groomed mass/substructure; else extend the slim card (patch). H→bb̄ tagging: three pre-declared parametrised scenarios (pessimistic/nominal/optimistic) — all reported. Trigger: offline leading large-R pT or HT plateau, stated as assumption.
- UCL MSc thesis: methodology ideas only; never its numbers or significance.

### 2.3 Phase-01–03 deliverables per process (both)
`<proc>/reports/01_signal_definition.md`, `02_background_overlap.md`, `03_generation_validation.md`, each with: date UTC, status PASS/FAIL/BLOCKED, goal, inputs/versions/seeds, exact commands and paths, evidence, tables, checks, caveats, next actions, git commit. Plus `<proc>/reports/INDEX.md`.

## 3. Run, file and role conventions

### 3.1 Directory per run (`p2/runs/<run_id>/`)
```
.claude/agents/   (multi arm only)    .claude/settings.json  (isolation deny rules)
PROGRESS.md       run-level progress (orchestrator)
reviews/          reviewer output: <process>_<phase>.md (multi arm)
wh/ | hh/         process directory, owned by the executor:
   STATUS.md (≤25 lines)  PROGRESS.md  reports/  cards/  scripts/  patches/  config/  figures/
   work/          heavy/transient outputs (git-ignored); condor logs under work/condor/
```
Canonical production samples (multi_r1 only, Phase 04+): `p2/production/<process>/<sample>/`.

### 3.2 Isolation
A run may read only `p2/lib/`, `p2/SPEC.md`, `p2/HANDOFF_VH_HH_multiagent.md`, its own run directory, and the frozen ZH tree (read-only, for reuse of ZH samples/reports and the installed software). It never reads another run's directory or `p2/metrics/raw/`. Enforcement status: see `p2/metrics/ENFORCEMENT.md`.

### 3.3 Roles (multi arm) — handoff §3
| Role | Model | Writes |
|---|---|---|
| orchestrator | opus | SPEC.md (decision log only), metrics/ledger.csv, run PROGRESS.md, gate notes |
| executor-wh / executor-hh | sonnet | own process dir only |
| verifier | haiku | nothing |
| reviewer | opus | reviews/ only |

Executor return contract: `STATUS.md` ≤ 25 lines: done; running cluster IDs; blockers; decisions needed D<proc>-N; next action. The final reply to the orchestrator is a pointer to STATUS.md, never pasted outputs.

### 3.4 Seeds
`seed = 1 000 000 × P + 10 000 × R + J` with P = process code (WH=2, HH=3), R = run index (multi_r1=11, multi_r2=12, multi_r3=13, single_r1=21, single_r2=22, single_r3=23), J = job index within the sample + 1000 × sample index (sample index from the sample registry in `<proc>/config/`). Executors assert uniqueness in code before any submission. Seeds of frozen ZH samples are not reused.

### 3.5 Decision numbering
Executors raise `D-WH-N` / `D-HH-N` in their STATUS.md; the orchestrator copies open items into §6 as `D<n>` for the human. Answers are recorded in §6 with date and verbatim human text.

## 4. Statistics and MC policies

### 4.1 Significance
Eq. 1 counting significance (Asimov, primary: stat-only ± MC stat), profile-likelihood in mγγ (WH supplementary), μ95 with exact Poisson CLs; robustness table as ZH.
### 4.2 N_MC (WH and HH signal)
N_MC ≥ max(50k, σ×BR×3000 fb⁻¹), checked by `nmc_check()`; failure stops the pipeline.
### 4.3 Effective-N policy (HH backgrounds; declared in advance, handoff §5.3)
In order: (1) generator filters looser than reco baseline, proven safe with twin samples; (2) truth-tag weighting (per-jet tag probability product, no tag cut); (3) in the final SR each background has N_eff = (Σw)²/Σw² ≥ 10, or a direct upper bound with the conservative variant in the robustness table. `nmc_check()` is extended (patch) to apply this rule to HH backgrounds and fails loudly on violation.

## 5. Token budgets per phase (soft; handoff §3 rule 8)
To be filled after multi_r1 Phase 01 from measured usage (`p2/metrics/parse_usage.py`). Overruns are flagged in the ledger, not hidden.

| Phase | WH budget (cost-eq. USD / tokens) | HH budget | Set on |
|---|---|---|---|
| 01 | — | — | — |
| 02 | — | — | — |
| 03 | — | — | — |

## 6. Decision log
(empty at creation; format: `D<n> | raised UTC | by | question | options | human answer (verbatim) | answered UTC`)

| ID | raised | by | question | options | answer | answered |
|---|---|---|---|---|---|---|
| D1 | 2026-11-03T22:00Z | orch | SPEC §3.4 seed formula collides across runs for sample idx>=10 (my error) | adopt seed=1e7*P+1e5*R+1000*idx+J before r2/single runs start; multi_r1 test seeds unchanged / other | open | |
| D2 | 2026-11-03T22:00Z | executor-hh (D-HH-1) | software/install/MG5_aMC_v3.6.3/HEPTools (15 MB) written into shared ZH install | human: rm -rf it (deny rules block agents) + accept ZH-install integrity note | open | |
| D3 | 2026-11-03T22:00Z | executor-wh (D-WH-0) | WH signal = light-flavour external partons only; top-resonant b class excluded (+108%), non-top b +5% as syst | accept / include b-initiated classes | open | |
| D4 | 2026-11-03T22:00Z | executor-wh (D-WH-2,7) | N>=σ·BR·3000 infeasible: W+jets 2-fake ~1e10, tt̄ 1ℓ ~4e8, F_QCD_Wajj_nomjj 1.6e7 | extend an effective-N/bound policy to WH (handoff deviation) / VBS-biased samples / other | open | |
| D5 | 2026-11-03T22:00Z | executor-wh (D-WH-3) | frozen ZH samples below 50k: ggZH 20000, ttH 42000, ZH→ττ 6565 | top up / accept with N_eff | open | |
| D6 | 2026-11-03T22:00Z | executor-wh (D-WH-4,5) | non-prompt-lepton (γγ+jj 0.07/0.25/2.5 ev) and WZγ/WWγ/ZZγ (e→γ) unquantified | dedicated samples / approve f_lepton range / bound | open | |
| D7 | 2026-11-03T22:00Z | executor-wh (D-WH-6) | B_EW_Waajj_vbs gridpack 884456.3 running >5 h | wait / condor_rm + split by initial state / close Phase 03 without EW test | open | |
| D8 | 2026-11-03T22:00Z | executor-wh (D-WH-7) + reviewer WH-G1-2 | mmjj>400 generator cut unsafe for QCD-type (37–48% loss); frozen ZH samples affected; EW twins missing | regenerate with looser cut / apply C=1/(1-f) with syst / EW twins first | open | |
| D9 | 2026-11-03T22:00Z | executor-wh (D-WH-8) | τ: W→τν signal-like part kept in b; background cards e/μ only (+18.8% lepton uplift not applied) | keep τ in b + add τ to bkg cards / treat as signal (deviation) | open | |
| D10 | 2026-11-03T22:00Z | executor-wh (D-WH-9) | 11/20 WH sample types untested; tt̄γγ vs tt̄γ double counting 0.554 fb | test all before G2 (recommended) / accept subset | open | |
| D11 | 2026-11-03T22:00Z | executor-hh (D-HH-2) | ggF HH+2j at LO, K-factor, EW×loop interference not covered (~½ SM signal in SR) | limitation / HEFT ggF HHjj sample | open | |
| D12 | 2026-11-03T22:00Z | executor-hh (D-HH-3,7) | tt̄ VBS topology and ME jet multiplicity (Z/W+3j, VH+2j, ggH+jj) | ttjj ME+filter vs MLM; higher-multiplicity samples vs PS-modelling unc. | open | |
| D13 | 2026-11-03T22:00Z | executor-hh (D-HH-4) | QCD multijet: 6-parton MEs infeasible (82k–139k diagrams) | accept 4j+bbjj VBS-filtered + PS + truth-tag with large unc. / other | open | |
| D14 | 2026-11-03T22:00Z | executor-hh (D-HH-5,8,9) | SM HH boosted ~0.07 [0.009,0.25] ev @500/fb → deliverable κ2V≠1; pT thresholds 300/450 provisional; m(HH) clip value; trigger 450 + 500/550 variation | confirm / specify | open | |
| D15 | 2026-11-03T22:00Z | executor-hh (D-HH-6,10,11) | bkg twins + N_eff≥10 before G2; tagging class definition (bb_nonH rate); extra bkgs tW/ttZ/ttW/EW Zjj/QCD ZZ bounds | approve plan / dedicated samples | open | |
| D16 | 2026-11-03T22:00Z | executor-hh (D-HH-12) | full N instead of effective-N for ggF HH, ZH, ZZjj, ttH (~3.5 GB, ~15 CPU-h) | full N (recommended by executor and reviewer) / effective-N | open | |

## 7. Protocol deviations log
(any deviation from the handoff, logged here and on the ledger)

| UTC | run | deviation | reason | impact |
|---|---|---|---|---|
| 2026-11-03T16:12:55Z | multi_r1 | custom agent types (.claude/agents) not loadable in the running session (no live reload); roles spawned as general-purpose subagents with model override + verbatim definition body + ROLE= tag; tools: restriction not applied | files created after session start | verifier/reviewer technically able to write; audited post hoc (metrics/ENFORCEMENT.md) |
| 2026-11-03T16:12:55Z | multi_r1 | G0 human check skipped: the first human prompt instructed to proceed to Phase 01–03 "without waiting" | human instruction | SPEC.md reviewed by human only at G1 |
| 2026-11-03T16:12:55Z | all | isolation deny rules bypassable by subprocess file access (python open, grep -r from parent) | Claude Code limitation (docs + test) | post-hoc transcript audit |
| 2026-11-03T21:27:06Z | multi_r1/hh | W-width factor not derived for HH (reviewer HH-G1-9) | not applicable to undecayed-V HH samples? to be justified by executor-hh | BR ledger for V→qq̄ samples |
| 2026-11-03T21:27:06Z | multi_r1/hh | interactive MG5 loop_sm output wrote software/install/MG5_aMC_v3.6.3/HEPTools (15 MB) into the shared ZH install (D-HH-1); diagram audits used a private MG5 copy work/mg5priv without recorded checksum | agent action; flagged by agent | ZH install integrity: human cleanup + checksum of ZH-used MG5 files needed |
| 2026-11-03T21:27:06Z | multi_r1 | session interruption 17:45–21:26Z; after restart custom agent types load natively; further spawns use them | Claude Code restart | earlier spawns ran as general-purpose (see first row) |
| 2026-11-03T22:00Z | multi_r1/wh | WH signal restricted to light-flavour external partons (D3); W→τν part in b (D9); effective-N-type bounds proposed for WH (D4, handoff defines it for HH only); SPEC §3.4 seed defect (D1) | physics / orchestrator error | pending human decisions |
| 2026-11-03T22:00Z | multi_r1 | G1 reached with WH Phase 03 IN-PROGRESS (EW gridpack running, 11/20 types untested) and HH Phase 03 missing 5 handoff sample types | long gridpacks / scope | G1 review done on current state; completion before G2 |
