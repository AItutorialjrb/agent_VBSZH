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
**G1 revision (D1 / D-WH-1, binding for all new seeds):** `seed = 1 000 000 × P + 100 000 × R + idx`, P = 2 (WH) / 3 (HH), R = 1..6 for multi_r1, multi_r2, multi_r3, single_r1, single_r2, single_r3; idx = 1000 × sample index + J (sample index < 100, J < 1000, so idx < 100 000; orchestrator reading of "idx"). Seeds already used in multi_r1 (old formula, R=11) are kept and listed in `<proc>/config/seeds_used_preG1.txt`; the uniqueness assertion includes that list. Original text (superseded):
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
| D1 | 2026-11-03T22:00Z | orch | SPEC §3.4 seed formula collides across runs for sample idx>=10 (my error) | adopt seed=1e7*P+1e5*R+1000*idx+J before r2/single runs start; multi_r1 test seeds unchanged / other | D-WH-1 "Accept: seed = base + 1e5*R + idx, R = 1..6 for multi_r1..r3, single_r1..r3. Already-produced multi_r1 samples keep their seeds; record the mapping." → §3.4 (G1 revision) | 2026-11-03 (G1 prompt) |
| D2 | 2026-11-03T22:00Z | executor-hh (D-HH-1) | software/install/MG5_aMC_v3.6.3/HEPTools (15 MB) written into shared ZH install | human: rm -rf it (deny rules block agents) + accept ZH-install integrity note | D-HH-1 "Leave the shared HEPTools dir in place (no deletion). Record its listing, size and sha256 in SPEC section 7 as a deviation; the constraint violation stays on the ledger. Any further installs go under p2/software only." | 2026-11-03 (G1 prompt) |
| D3 | 2026-11-03T22:00Z | executor-wh (D-WH-0) | WH signal = light-flavour external partons only; top-resonant b class excluded (+108%), non-top b +5% as syst | accept / include b-initiated classes | D-WH-0 "Accept. The top-resonant b class (tHq/tHW-like) enters as a resonant background; check that it is in the matrix." | 2026-11-03 (G1 prompt) |
| D4 | 2026-11-03T22:00Z | executor-wh (D-WH-2,7) | N>=σ·BR·3000 infeasible: W+jets 2-fake ~1e10, tt̄ 1ℓ ~4e8, F_QCD_Wajj_nomjj 1.6e7 | extend an effective-N/bound policy to WH (handoff deviation) / VBS-biased samples / other | D-WH-2 "Accept VBS-biased W+jets and tt 1l with probability (fake-factor) weighting using the Delphes j->gamma rate, N_eff >= 10 in the SR. Use only biasing cuts shown safe by a twin test (loss <= 5% within stat at reco SR)." | 2026-11-03 (G1 prompt) |
| D5 | 2026-11-03T22:00Z | executor-wh (D-WH-3) | frozen ZH samples below 50k: ggZH 20000, ttH 42000, ZH→ττ 6565 | top up / accept with N_eff | D-WH-3 "Top up ggZH, ttH dilep and ZH->tautau to >= 50k as new samples under p2/production. Never modify ZH files." | 2026-11-03 (G1 prompt) |
| D6 | 2026-11-03T22:00Z | executor-wh (D-WH-4,5) | non-prompt-lepton (γγ+jj 0.07/0.25/2.5 ev) and WZγ/WWγ/ZZγ (e→γ) unquantified | dedicated samples / approve f_lepton range / bound | D-WH-4 "Accept a parametrised f_lepton range, taken from published CMS tight-ID fake rates (cite them). Report both ends." D-WH-5 "Accept batch generation with group_subprocesses False, after one successful test job." (orchestrator reading: WZγ/WWγ/ZZγ get dedicated batch samples, group_subprocesses False, after one successful test job) | 2026-11-03 (G1 prompt) |
| D7 | 2026-11-03T22:00Z | executor-wh (D-WH-6) | B_EW_Waajj_vbs gridpack 884456.3 running >5 h | wait / condor_rm + split by initial state / close Phase 03 without EW test | D-WH-6 "Info, noted." (orchestrator reading: wait for 884456.3; no condor_rm) | 2026-11-03 (G1 prompt) |
| D8 | 2026-11-03T22:00Z | executor-wh (D-WH-7) + reviewer WH-G1-2 | mmjj>400 generator cut unsafe for QCD-type (37–48% loss); frozen ZH samples affected; EW twins missing | regenerate with looser cut / apply C=1/(1-f) with syst / EW twins first | "Twin result (generator mjj>400 unsafe for QCD-type, 47.6% / 37% loss): no generator mjj cut on QCD-type samples. Nominal = no-mjj samples, or a looser cut shown safe by twin (<= 5%). If N is infeasible, use the ZH twin-correction method (stat + full-difference syst) and log it as a deviation." | 2026-11-03 (G1 prompt) |
| D9 | 2026-11-03T22:00Z | executor-wh (D-WH-8) | τ: W→τν signal-like part kept in b; background cards e/μ only (+18.8% lepton uplift not applied) | keep τ in b + add τ to bkg cards / treat as signal (deviation) | RESUME: "accept your recorded defaults for D9 and D10" → τ default adopted (S_EW_WHjj_taunu in b; r_τ uplift ±100 %) [G1 text: not answered at G1 (D-WH-8; reviewer WH-G1-8 sev-2, binding before G2). Orchestrator default pending G2 confirmation: handoff signal = W→eν/μν, so S_EW_WHjj_taunu stays in b (no deviation); τ feed-down into W-decaying backgrounds quantified at reco SR (τ in production cards, or uplift measured on the τ sample with ±100 % unc.)] | 2026-11-06T12:57:29Z (resume prompt) |
| D10 | 2026-11-03T22:00Z | executor-wh (D-WH-9) | 11/20 WH sample types untested; tt̄γγ vs tt̄γ double counting 0.554 fb | test all before G2 (recommended) / accept subset | RESUME: "accept your recorded defaults for D9 and D10" → every type tested before production; tt̄γ/tt̄γγ overlap bounded/removed [G1 text: not answered at G1 (D-WH-9; reviewer WH-G1-4,9 sev-2, binding). Orchestrator default: one test job per sample type before G2 (Phase 03 requirement); tt̄γ/tt̄γγ overlap bounded after b-veto at reco or removed as ZH; I_WHjj BR ledger fixed] | 2026-11-06T12:57:29Z (resume prompt) |
| D11 | 2026-11-03T22:00Z | executor-hh (D-HH-2) | ggF HH+2j at LO, K-factor, EW×loop interference not covered (~½ SM signal in SR) | limitation / HEFT ggF HHjj sample | D-HH-2 "ggF HH: LO loop-induced gg->HH + PS (existing install), normalised to the LHC HWG NNLO cross section at 13.6 TeV (cite it), 30% extra uncertainty in the VBF region. EW-loop interference neglected and stated. Reword 01:62(c)." — **CLOSED by A1 (2026-11-06): not pursued** | 2026-11-03 (G1 prompt) |
| D12 | 2026-11-03T22:00Z | executor-hh (D-HH-3,7) | tt̄ VBS topology and ME jet multiplicity (Z/W+3j, VH+2j, ggH+jj) | ttjj ME+filter vs MLM; higher-multiplicity samples vs PS-modelling unc. | D-HH-3 "Nominal: validated MLM tt+0,1,2j. Use ttjj ME+filter only if N_eff fails." D-HH-7 "Rule: add an ME+jets sample (Z/W+3j, VH+2j, ggH+jj) only if that background's PS-based yield is > 10% of total background in the SR. Otherwise apply a 100% PS-modelling uncertainty." — **CLOSED by A1 (2026-11-06): not pursued** | 2026-11-03 (G1 prompt) |
| D13 | 2026-11-03T22:00Z | executor-hh (D-HH-4) | QCD multijet: 6-parton MEs infeasible (82k–139k diagrams) | accept 4j+bbjj VBS-filtered + PS + truth-tag with large unc. / other | D-HH-4 "Accept 4j + bbjj + PS + truth-tag. Give the class-resolved N_eff estimate (review item 6) and use a b-enriched / PS g->bb strategy. Multijet normalisation +-100%, results also shown with multijet x0.5 and x2." — **CLOSED by A1 (2026-11-06): not pursued** | 2026-11-03 (G1 prompt) |
| D14 | 2026-11-03T22:00Z | executor-hh (D-HH-5,8,9) | SM HH boosted ~0.07 [0.009,0.25] ev @500/fb → deliverable κ2V≠1; pT thresholds 300/450 provisional; m(HH) clip value; trigger 450 + 500/550 variation | confirm / specify | D-HH-5 "Accept the kappa2V != 1 deliverable. 300/450 thresholds are provisional, fixed by expected-only optimisation in Phase 06. Quote SM 0.07 with its Poisson interval." D-HH-8 "Primary result unclipped (as in published kappa2V results). Variation clipped at m(HH) < 1.5 TeV, plus a 1.0 TeV check. Both fixed now, a priori." D-HH-9 "Accept 450 GeV baseline with pre-declared 500/550 variations. Define the m_SD window on the Delphes peak with a +-5% mass-scale variation." — **CLOSED by A1 (2026-11-06): not pursued** | 2026-11-03 (G1 prompt) |
| D15 | 2026-11-03T22:00Z | executor-hh (D-HH-6,10,11) | bkg twins + N_eff≥10 before G2; tagging class definition (bb_nonH rate); extra bkgs tW/ttZ/ttW/EW Zjj/QCD ZZ bounds | approve plan / dedicated samples | D-HH-6 "Accept: background twins and N_eff >= 10 before G2. Storage <= 150 GB after checking the EOS quota." D-HH-10 "Accept the class definition in review item 1." D-HH-11 "Bound each background. Make a dedicated sample only if its 95% UL is > 10% of total SR background." — **CLOSED by A1 (2026-11-06): not pursued** | 2026-11-03 (G1 prompt) |
| D16 | 2026-11-03T22:00Z | executor-hh (D-HH-12) | full N instead of effective-N for ggF HH, ZH, ZZjj, ttH (~3.5 GB, ~15 CPU-h) | full N (recommended by executor and reviewer) / effective-N | D-HH-12 "Accept full N (3.5 GB, 15 CPU-h)." — **CLOSED by A1 (2026-11-06): not pursued** | 2026-11-03 (G1 prompt) |
| D17 | 2026-11-03T22:00Z | orch | assisted flag of prompt 1 | — | "prompt 1 in metrics/prompts/multi_r1.csv is assisted=yes (drafted with the chat assistant)" | 2026-11-03 (G1 prompt) |
| D18 | G1 | human | comparability of repeat runs | — | "freeze SPEC.md as SPEC_G0.md = state at multi_r1 start + the seed fix (D-WH-1) only. All repeat runs (multi_r2/r3, single_r1-r3) use SPEC_G0.md for Phase 01-03 and must not read multi_r1 outputs. Decisions below apply to multi_r1 from Phase 04 onward (and to pre-G2 fixes). Record as a known environment difference that repeats start with HEPTools already present." → p2/SPEC_G0.md | 2026-11-03 (G1 prompt) |
| D19 | G1 | human | role briefs (from Phase 04 onward only; repeat Phase 01-03 keep the multi_r1 protocol) | — | "(a) role briefs: the orchestrator writes brief_wh.md / brief_hh.md (<= 150 lines) and executors read the brief instead of the full handoff" → runs/multi_r1/brief_{wh,hh}.md | 2026-11-03 (G1 prompt) |
| D20 | G1 | human | gate auto-pass (from Phase 04 onward only) | — | "(b) gate auto-pass: if the reviewer reports no severity-1 issue and no decision is needed, proceed without waiting, and log the auto-pass on the ledger." | 2026-11-03 (G1 prompt) |
| D21 | G1 | human | role-spawn protocol for repeats | — | "multi_r2/r3 must spawn roles the same way [general-purpose + explicit model override + role prompt], for comparability; log this in SPEC section 7." | 2026-11-03 (G1 prompt) |
| D22 | G1 | human | reviewer conditions | — | "Reviewer conditions in reviews/wh_01-03.md and reviews/hh_01-03.md are binding before G2." Then: "do the pre-G2 fixes and WH Phase 03 completion. Stop at G2, or earlier if a new human decision is needed." | 2026-11-03 (G1 prompt) |
| D23 | 2026-11-04 | executor-hh (D-HH-13) + reviewer hh_G2 3 | κλ/κV secondary result: Delphes closure T3 has no power, κλ morphing MC error ≥34 % (up to 195 %) at planned N | direct samples (1,1,0),(1,1,2) + (1,1,5) closure (reviewer recommends) / high-yield T3 (κV=1.5) / no κλ claim | CLOSED by A1 | 2026-11-06T12:57:29Z (resume prompt) |
| D24 | 2026-11-04 | executor-hh (D-HH-14) + reviewer hh_G2 1 (sev-1) | QCD multijet (~97 % of SR bkg) generator filter: nominal loses 25/29 %, looser filter residual loss unmeasured; also impact-level twin criterion for sub-dominant bkgs; bound-only if 95 % UL < 1 % of SR bkg | (a) further-loosened twin ~1e6 ev (~40 wall-h) / particle-level fat-jet filter; (b),(c) accept / reject | CLOSED by A1 | 2026-11-06T12:57:29Z (resume prompt) |
| D25 | 2026-11-04 | reviewer hh_G2 2 | 2.19 M pre-G2 pilot events (~56 wall-h, ~14 GB) generated without G2 approval, ~41 % of the HH total | reuse as production (after sha256 card/gridpack match) / declare validation-only and regenerate | CLOSED by A1 (pilots kept on disk, not used) | 2026-11-06T12:57:29Z (resume prompt) |
| D26 | 2026-11-04 | reviewer hh_G2 4 | D-HH-2 premise changed: ggF HH (LO+PS, NNLO-normalised) 0.923 SR events vs SM EW 0.047 (≈20×, was "~½" at G1); K(κλ) taken at κλ=1 for all κλ | keep D-HH-2 (30 % VBF-region unc.) / larger unc. or κλ-dependent K | CLOSED by A1 | 2026-11-06T12:57:29Z (resume prompt) |
| D27 | 2026-11-04 | executor-wh (D-WH-10) | W+jets double fake and tt̄ two-fake: ME W+4j (F_Wjjjj) and tt̄jj (T_ttjj_1l) with fake-factor weights, N from N_eff ≥ 10 in SR, no generator bias cut (none shown safe) | confirm / other | RESUME: "accept ... your recommendations for D-WH-10" → unbiased ME W+4j / tt̄jj with fake-factor weights, N_eff ≥ 10 in SR (+ reviewer wh_G2 12: αs⁴ scale envelope, 2-fake f-scenarios ×{0.09,1,9}) | 2026-11-06T12:57:29Z (resume prompt) |
| D28 | 2026-11-04 | executor-wh (D-WH-11, blocks D-WH-4) | no citable numeric table of CMS tight-ID lepton fake rates found (2103.04956 gives figures only); f_lepton range still the ZH assumption, non-prompt numbers labelled ESTIMATES | human supplies reference / accept digitised figure values / keep assumption range as stated | RESUME D-WH-11: "take numeric jet->lepton fake rates from HEPData tables of published CMS (or ATLAS) papers, citing the record. If none exist, bracket f_lepton over a cited range and report both ends." | 2026-11-06T12:57:29Z (resume prompt) |
| D29 | 2026-11-04 | executor-wh (D-WH-12) | WZγ/WWγ/ZZγ (D-WH-5) generated without ME jets (7–8-body jj samples not generated); VBS jets from PS | accept + PS-modelling unc. (analogue of D-HH-7 rule) / generate Vγ+jj | RESUME D-WH-12: "add ME-jet samples only if that background's PS-based yield is > 10% of total background in the SR; otherwise 100% PS-modelling uncertainty." | 2026-11-06T12:57:29Z (resume prompt) |
| D30 | 2026-11-04 | executor-wh (D-WH-13) | F_QCD_Wajj_nomjj full N = 1.64e7 events (corrected by reviewer wh_G2 6: 894 core-h, 42.7 GB; executor first quoted ~520 core-h) vs mmjj>400 + twin C (deviation) | full N (executor + reviewer recommend) / twin-correction | RESUME: "your recommendations for ... D-WH-13 (full N accepted within the 200 GB budget)" → F_QCD_Wajj_nomjj full N | 2026-11-06T12:57:29Z (resume prompt) |
| D31 | 2026-11-04 | reviewer wh_G2 1 (sev-1) | non-prompt-lepton class (QCD γγ+jj 0.07/0.25/2.5 ev, VBF/ggF H 0.13/0.05 vs ~0.9 signal) has no MC; assumed-ε estimates proved 36× low for tt̄ | add Q_aajj + VBF/ggF H→γγjj with per-jet f_ℓ weights, N_eff ≥ 10 (executor preparing gridpacks/tests now) / enter ESTIMATE in b as conservative variant | RESUME: not answered explicitly; "N rule unchanged" → orchestrator reading: Q_aajj / H+jj non-prompt-lepton samples at full N = max(50k, σ·k·3000) if within the 200 GB budget; otherwise new human decision | 2026-11-06T12:57:29Z (resume prompt) |
| A1 | 2026-11-06T12:57:29Z | human | **Protocol amendment A1 (human decision, 2026-11-06, before any HH physics result): stop the HH stream for resource reasons.** | — | verbatim: "stop the HH stream for resource reasons. Record A1 with timestamp and reason in the SPEC.md decision log and SPEC section 7. Keep all HH files; no deletion, no HH jobs. HH Phase 01-03 becomes an exploratory appendix case (multi only, n=1, no hypothesis test). D-HH-2..12 closed as not pursued. H1-H4 unchanged." | 2026-11-06T12:57:29Z (resume prompt) |
| A2 | 2026-11-06T12:57:29Z | human | **Amendment A2 (single-agent full analysis)** | — | verbatim: "repeats stay WH Phase 01-03 as pre-registered (multi_r2/r3, single_r1-r3). In addition, single_r1 continues from Phase 04 to the final result using only the frozen multi_r1 production samples (read-only ntuples + sigma/N table, no multi_r1 reports or code). This is the end-to-end single vs multi comparison on identical samples. When WH production is complete and validated, tag it wh-prod-v1, write single_r1 access instructions, and stop so I can launch the repeat runs." | 2026-11-06T12:57:29Z (resume prompt) |
| D32 | 2026-11-06T12:57:29Z | human | WH final-result scope (multi_r1, Delphes level, N rule unchanged) | — | items 1-6 of the resume prompt (backgrounds incl. three separated non-prompt classes with lower/upper bounds; cut-based then BDT/DNN k-fold adopted only if >10 % gain and stable; Eq.1 + exact-Poisson CLs mu95 at 500/1000/3000 + mγγ PL fit, defs (a),(b); couplings λWZ, (κW,κZ) from direct samples, per-bin quadratic + leave-one-out, λWZ<0 and λWZ=−1 significance, c_A if cheap, binning optimised; VH combination with frozen ZH; comparison with CMS PLB 860 (2025) 139202 and ATLAS PRL 133 (2024) 141801). Copied in runs/multi_r1/brief_wh.md §5. Stop only for a human decision or at wh-prod-v1. | 2026-11-06T12:57:29Z (resume prompt) |

- **D33 (human, 2026-11-07): held/failed production chunks.** Release a held job once with more memory. If a chunk fails again, drop it only if the sample still meets the N rule (max(50k, σ×BR×3000 fb⁻¹) and N_eff ≥ 10); log every dropped chunk in §7. Do not wait on them otherwise.

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
| 2026-11-03 (G1) | shared software | D2 / D-HH-1: `software/install/MG5_aMC_v3.6.3/HEPTools` left in place by human decision. Created 2026-11-03 17:28–17:30 CET by executor-hh (MG5 loop_sm output). 537 entries (471 files, dirs bin, HEPToolsInstallers, include, lib, ninja, oneloop), 15 388 533 bytes. Listing `p2/metrics/heptools_listing.txt`; per-file sha256 `p2/metrics/heptools_sha256.txt` (sha256 of that list a343bcbe…2b42). Further installs only under `p2/software/`. Ledger constraint_violation line kept. | agent action, human decision | **known environment difference: all repeat runs start with HEPTools present** (multi_r1 Phase 01–03 started without it) |
| 2026-11-03 (G1) | multi_r1 | Role-spawn record from transcripts (`metrics/raw/claude/multi_r1/*/subagents/`, assistant-message models): before the restart, 6 spawns were general-purpose with explicit model override + role prompt + ROLE= tag: executor-wh and executor-hh (sonnet), verifier ×3 (haiku), reviewer ×1 (opus). After the restart (21:50Z) 2 spawns used the native types: verifier (haiku), reviewer (opus). Every verifier message ran on claude-haiku-5-5 and every reviewer message on claude-opus-5-5. | session restart | G1 reviews: one general-purpose, one native. tools: restriction applied only to native spawns |
| 2026-11-03 (G1) | multi_r2, multi_r3 | D21: roles are spawned as general-purpose subagents with explicit model override + verbatim role prompt (the agent-definition body) + ROLE=/PHASE= tags, i.e. tool restrictions not enforced, matching multi_r1 Phase 01–03. multi_r1 itself keeps native types from now on. | comparability with multi_r1 | a residual multi_r1 difference: 2 native spawns at G1 (row above) |
| 2026-11-03 (G1) | repeat runs | D18: repeats use `p2/SPEC_G0.md` (SPEC at multi_r1 start, commit a57ced5, plus the D1 seed revision only) and must not read multi_r1 outputs. multi_r1 settings deny Edit of other runs' `.claude/settings.json`, so the extra repeat deny rules (Read of `p2/SPEC.md`, `p2/production/**`, `p2/metrics/review_log.csv`) are prepared as `p2/metrics/g1_repeat_isolation.py` for the human to run. | isolation design | not enforced until the human runs the script; `ledger.csv` notes stay readable by repeats (minor leak, notes are terse) |
| 2026-11-03 (G1) | ZH tree (human) | The 19 ZH `figures/*.pdf` were deleted by the human (to limit scp) and restored from zh-final-v1.1. Not an agent violation; logged as a human action (ledger event human_intervention). | human action | none (restored from tag) |
| 2026-11-04 | multi_r1/hh | executor-hh generated 2.19 M pilot events (219 jobs, ~56 wall-h, ~14 GB) in p2/production/hh before G2 and counts them toward production N; brief allowed validation-size samples only | twin tests need ≥1e2 QCD tail events (executor justification) | constraint_violation on ledger; reuse decision D25 |
| 2026-11-04 | multi_r1/hh | executor-hh stopped by the API 5-hour usage limit (~01:50Z), resumed 08:59Z after human "continue" | account rate limit | wall-time gap; no work lost |
| 2026-11-06T12:57:29Z | multi_r1/hh | **Amendment A1**: HH stream stopped (human decision, 2026-11-06, resource reasons), before any HH physics result. All HH files kept (no deletion), no HH jobs; HH Phase 01–03 = exploratory appendix case (multi only, n=1, no hypothesis test); D-HH-2..12 and D23–D26 closed as not pursued; H1–H4 unchanged. | human resource decision | HH 04 plan, QCD held block, 2.19 M pilots remain on disk unused |
| 2026-11-06T12:57:29Z | single_r1 | **Amendment A2**: single_r1 continues past G1 from Phase 04 to the final WH result on the frozen multi_r1 production samples (read-only ntuples + σ/N table only; no multi_r1 reports or code). Requires a second-stage isolation change for single_r1 (Read allowed on the production data only) at wh-prod-v1. | human design decision | adds an end-to-end single-vs-multi comparison on identical samples |
| 2026-11-06T12:57:29Z | multi_r1 | Pause 2026-11-04T13:40Z → 2026-11-06 (credit limit); no condor action during pause | human | wall-time gap |
| 2026-11-06T22:53Z | multi_r1/wh | **D29 supersedes D30 for F_QCD_Wajj_nomjj**: D29 triggered (3j PEAK yield ≥40 % of SR background), so the human-sanctioned full-N 2j row (D30) is replaced by the ME+1j sample F_QCD_Wajjj_nomjj (8.72M, unmerged, used only in regions requiring ≥3 reco jets); the 2j test + twins become a cross-check outside s and b. σ_MC ≤ 0.1·S not met for this row (0.19 events): treated as an MC-stat nuisance; D-WH-15 contingent (reviews/wh_G2_recheck.md Recheck 3) | D29 rule vs D30 | row replaced; ≈−18 GB vs plan |
| 2026-11-07 | multi_r1/wh | **D33 dropped chunks**: F_Wjjjj top-up 893633.14, .19, .120 (41 000 events each, 123 000 total) were released once at 12000 MB, then removed by wall time; dropped under D33, F_Wjjjj N = 18 714 998 still meets the rule. Q_aajj 893632.204/.205/.211/.212 not dropped (resubmitted as 893876). Also: all pre-production Delphes j→γ rate tables were lepton-contaminated (98.8 %); top-up sizing (893633/893634) and the pre-production D29 fractions used them, so those outputs are superseded (kept in wh/work/postprod_v1_contaminated/), samples kept | D33 / executor bug | +0 GB; review wh_prod_validation.md |
