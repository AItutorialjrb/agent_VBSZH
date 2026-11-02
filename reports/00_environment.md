# Phase 00 — environment and reference audit

Date UTC: 2026-11-02. Status: **BLOCKED** (audit executed; production readiness and reproducibility gates remain blocked).

## Goal and scope
Audit the actual lxplus environment and the supplied reference for an unknown-research feasibility study of EW pp -> ZHjj, Z -> ee/mumu, H -> gamma gamma at 13.6 TeV and 500 fb^-1. No ZHjj cross section, yield, efficiency or significance has been calculated. No software was installed, no generator was launched and no batch job was submitted. Stop after Phase 00; phases 01/02 have not passed.

Read AGENTS.md, PROJECT_BRIEF.md, START_CODEX_PROMPT.md, reports/00_initial_design.md, reports/00_preflight_output.txt and all 14 pages of reference_ZGammaGamma.pdf via pdftotext. Inputs and hashes are recorded in the command transcript. Working directory: /eos/home-r/rjiang/vbs_zh_codex_starter.

## Evidence and exact commands
[00_environment_audit.txt](00_environment_audit.txt) contains literal commands, stdout/stderr and exit codes for fresh probes starting 2026-11-02T12:17:55Z. Grouped shell commands report the final command's status; intermediate failures are retained and must not be interpreted as successes. Commands had 15–25 second timeouts. No full environment or authentication files were dumped.

PDF extraction commands:
```bash
pdfinfo reference_ZGammaGamma.pdf
pdftotext -layout reference_ZGammaGamma.pdf /tmp/rjiang_reference_ZGammaGamma.txt
cat /tmp/rjiang_reference_ZGammaGamma.txt
```
PDF metadata: 14 pages, 528338 bytes, PDF 1.7, unencrypted. SHA256: `3a456511c4b1faa69397394895f42ea4b76d466580b1c30d51d58154804fcd0a`.

The sandbox failed before commands ran with `bwrap: Can't create file /eos/home-r/rjiang/vbs_zh_codex_starter/.git: Permission denied`. Probes and report writes therefore used the explicit escalation mechanism; this does not show an ordinary EOS write failure. Actual report writes succeeded.

## Session and source-control provenance
`codex --version` returned `codex-cli 0.158.0`; binary is `/eos/home-r/rjiang/bin/codex`. No upgrade, model/configuration change, new conversation or subagent was requested or launched.

The user's stated session model is GPT-6-Astra default, with current reasoning configuration to be preserved. **Live `/status` output is not available through this shell/tool interface.** It was not fabricated or replaced with a new CLI session. `codex --help` exposes no status subcommand; a narrowly filtered inspection of the base config returned no model/reasoning settings. Consequently the active model and exact reasoning effort are not independently verified: this is a reproducibility blocker. Next action: capture `/status` in this same existing interactive conversation and append its model and effort verbatim, without changing settings.

`git rev-parse --show-toplevel` returned `/eos/home-r/rjiang`, and HEAD was `6ea6cb9462533bbc1b209f7d4b4b67fd49b4d737`. `git status --short -- .` returned `?? ./`. This is a parent-repository commit, **not a committed snapshot of this project**. No parent files were changed or committed. A project-only tracked snapshot is required before production; input SHA256 values provide interim provenance.

## Fresh environment findings

| Component | Observed evidence | Interpretation |
|---|---|---|
| Host / OS | lxplus924.cern.ch; RHEL 9.8; kernel 5.14.0-687.59.1.el9_8.x86_64 | Login node; bulk simulation prohibited by project rules |
| Identity | rjiang, UID 155524, group zh | Project and AFS access tests succeeded |
| Python | runtime 3.9.25, GCC 11.5.0; system package python3-3.9.25-7.el9_8.3 | PATH points to CMS CVMFS directory labelled 3.9.6; directory name is not runtime version |
| ROOT | root-config and a ROOT batch expression both returned 6.40.04; prefix /usr | Runtime works; RPM root-core-6.40.04-4.el9.x86_64 |
| Compilers | GCC/GFortran 11.5.0; CMake 3.31.8 | Present; full simulation ABI compatibility untested |
| MG5 | mg5_aMC absent from PATH; nearby MadGraph5_aMCatNLO contains examples/production, no targeted executable/version match | No validated local installation identified; not a machine-wide absence claim |
| Pythia8 / Delphes / LHAPDF | config/executable probes absent from PATH | Production runtime and PDF data unpinned |
| CVMFS | CMS, SFT, LCG views readable | Candidate releases accessible; no setup script sourced |
| HTCondor | 25.0.14; SCHEDD_HOST bigbird26.cern.ch | Direct scheduler query succeeded with zero user jobs; submission/worker access not tested |
| EOS client | 5.4.9; RPM 5.4.9-1.rh9.cern | Project write access and report creation succeeded |
| Network | EOS and arxiv DNS resolved; arxiv HTTPS HEAD returned HTTP/2 200 | Limited endpoint evidence, not unrestricted network validation |

The broad Condor submitter query failed (`Collector has no record of schedd/submitter`); `condor_q -name bigbird26.cern.ch rjiang -totals` succeeded. A missing lxbatch.cern.ch DNS line is not evidence that the configured scheduler is unavailable.

CVMFS LCG_108 x86_64-el9-gcc13-opt manifests identify candidate MG5 **3.5.9.atlas13 / ebc2d**, Pythia8 **315 / 4b2bb**, LHAPDF **6.5.5 / fc9c9**, Delphes **3.5.1pre12 / ae61c**, Python **3.12.11 / 531c6**, ROOT **6.36.02 / c35af**. These are manifest versions/build identifiers, not git hashes or validated project pins. They differ from the paper's MG5 3.6.3 and Delphes 3.5. No 3.6.3 entry matched the inspected common MG5 directory. Delphes was found under LCG_108/delphes after the MCGenerators/delphes location failed. Do not silently adopt an ATLAS-patched MG5 or prerelease Delphes.

## Storage, permissions and preflight comparison
AFS ACL grants rjiang rlidwka. AFS quota: 10,485,760 KiB, used 10,407,773 KiB (99%); remaining 77,987 KiB, about 76.2 MiB. This is unsuitable for sizeable builds or event files. EOS mount-level df reports 4.0P total / 2.0P available; **these are not personal quotas**. Local /tmp has 44G filesystem availability; local quota reports 103G limit, 6808K used, 24 files, 6882k file limit. Scratch capacity is host-local and transient.

EOS quota syntax/path corrections were necessary: `quota -u rjiang` printed usage, and `quota /eos/home-r/rjiang/` reported no quota. The successful `eos root://eoshome-r.cern.ch quota` returned canonical quota node `/eos/user/r/rjiang/`, group `project`, used bytes 780.39 GB, logical bytes 390.19 GB, used files 737.31 K, displayed aval bytes 2.00 TB / aval logib 1.00 TB / aval files 5.00 M, filled 39.02%, statuses ok. These columns are recorded literally; do not equate displayed “aval” to free space without checking semantics. Canonical-node association with the mounted project should be checked before allocating production storage.

The original preflight remains unchanged (SHA256 `d0c4ae590aeac98e44f72bb4c53d48389cf801123766558851a303dcebdec1c5`). It was captured 2026-10-31T17:16:30Z on lxplus937, whereas this audit ran on lxplus924. Codex 0.158.0, Python 3.9.25, ROOT 6.40.04, active tool paths and missing generator PATH entries agree. The old df output did not establish user quota or batch functionality; fresh probes add those checks. Its Python path label also must not be treated as a version pin.

## Reference-paper audit
Source: Ding et al., *Prospects for measuring electroweak production of Z gamma gamma and 2 jets at the LHC*, supplied PDF arXiv:2512.07689v1 (arXiv stamp 8 December 2025; manuscript dated 9 December 2025). Page numbers below are printed PDF pages. This is a continuum EW Zgamma gamma jj study, not a ZHjj result.

| Item | Verified paper setting / location |
|---|---|
| Definition | Full EW component, VBS-enriched phase space; on-shell Z decay and inclusive ee/mumu final-state alternatives, pp. 2–4 |
| Generation | MG5_aMC 3.6.3, LO, 13.6 TeV, pp. 4–5 |
| Generator cuts | pT(l)>10, pT(gamma)>15, pT(j)>20 GeV; abs eta(l,gamma)<2.5, abs eta(j)<5; DeltaR>0.4; mll>50 GeV, pp. 4–5 |
| Shower/detector | Pythia8 default models; Delphes 3.5 built-in CMS card, p. 5 |
| Merging | QCD Zgamma and Zgamma gamma with 0,1,2 ME jets, MLM, p. 5 |
| Baseline | At least two good photons, OS-SF lepton pair, two good jets; pT(l,gamma,j)>15,20,25 GeV; eta limits 2.5,2.5,5, p. 6 |
| Object choice | Two highest-pT jets/photons; lepton pair nearest mZ=91.2 GeV, p. 6 |
| Additional cuts | m(ll gamma gamma)>100 GeV; 70<mll<120 GeV, p. 8 |
| Scan | mjj lower cut 200–800 GeV by 100; abs Deltaeta lower cut 0–4 by 0.5, p. 8 |
| Chosen region | mjj>700 GeV, abs Deltaeta>2.0; scan peak at (700,2.5), pp. 8–10 |
| Statistics | Z=sqrt(2*((s+b)*ln(1+s/b)-s)); inclusive signal; 500 fb^-1, Eq. 1 p. 8 |

Table I p. 5 lists EW/QCD Zgamma gamma, EW/QCD Zgamma, ttbar gamma and tW gamma. Z+jets double fakes are neglected in the paper (p. 4); this is not a justified omission for our study. Its overlap prescription rejects Zgamma events with at least two reconstructed photons classified by ancestry as hard (quark/boson origin), p. 6. This needs a phase-space/shower validation and cannot be assumed exclusive for this project. Jet-to-photon misidentification in detector simulation is not data-driven.

Table II p. 6 quotes cross sections in fb: on-shell EW signal 0.263, inclusive EW 0.426, QCD Zgamma gamma 23.0, interference 0.0244; paper interference syntax is `QCD^2==2` (p. 5). These are paper results with its final-state/cut definitions, not pre-decay ZHjj cross sections. The ratio 0.0244/0.263 is about 9.3%; its neglect cannot be transferred to ZHjj.

Table IV p. 11 at 500 fb^-1 quotes inclusive signal 17.55 +/- 0.46 and total background 10.36 +/- 0.86, with QCD Zgamma gamma 3.32 +/- 0.53, QCD Zgamma 1.52 +/- 0.54, EW Zgamma 5.36 +/- 0.40, ttbar gamma 0.15 +/- 0.10 and displayed tW gamma 0.00 +/- 0.00. The rounded zero is not proof of negligibility. Paper significance 4.50 +/- 0.17 (pp. 9–10) is not a prediction for this project. We have not independently reproduced its simulation or uncertainties.

Missing reproducibility information in the supplied paper: exact Pythia8 patch/tune, PDF set/member and LHAPDF version, scale prescription, seed list, sample counts, complete cards/card hashes, matching scales and validation plots, detector modifications, and nuisance-parameter likelihood. The reference does not establish a Higgs diphoton decay model, physical BR normalization, mass resolution, or signal-window/sideband scheme for ZHjj.

## Blockers and executable next steps
1. Capture live `/status` in this same session. Preserve Codex 0.158.0 and current model/effort. No replacement session is an acceptable proxy.
2. Select and validate a coherent MG5/PY8/Delphes/PDF stack. None is production-pinned. The following read-only commands inspect existing candidates; they do not install or generate events:
```bash
ls /cvmfs/sft.cern.ch/lcg/releases/LCG_108/MCGenerators/madgraph5amc/3.5.9.atlas13/x86_64-el9-gcc13-opt
ls /cvmfs/sft.cern.ch/lcg/releases/LCG_108/MCGenerators/pythia8/315/x86_64-el9-gcc13-opt
ls /cvmfs/sft.cern.ch/lcg/releases/LCG_108/delphes/3.5.1pre12/x86_64-el9-gcc13-opt
rg -n '^(madgraph5amc|pythia8|lhapdf);' /cvmfs/sft.cern.ch/lcg/releases/LCG_108/LCG_generators_x86_64-el9-gcc13-opt.txt
```
These candidates require a documented version decision; they are not recommended replacements for the paper versions. If MG5 3.6.3 is required, obtain a vetted source/checksum and select project-local storage before any later installation. No unverified download URL or installation command is supplied.
3. Recheck storage and scheduler without changing data:
```bash
fs lq /afs/cern.ch/user/r/rjiang
eos root://eoshome-r.cern.ch quota
eos root://eoshome-r.cern.ch quota ls -u 155524 -p /eos/user/r/rjiang/
condor_q -name bigbird26.cern.ch rjiang -totals
```
Avoid AFS for builds/events. Batch submission, job flavour/resources and staging must be tested later with a tiny job before bulk work; no production capacity is certified here.
4. Establish a project-only git snapshot without staging unrelated home-directory content. Inspect first with `git status --short -- .` and `git ls-files -- .`; do not use an unscoped `git add .` from the parent repository. Report the actual project-containing commit when available.
5. Phase 01 must decide gauge-invariant EW orders/all diagrams, Higgsstrahlung/interference, flavour and off-shell conventions, and supported H->gamma gamma decay/BR bookkeeping. Phase 02 must validate prompt EW/QCD, fake, top/diboson and other-Higgs categories plus photon-shower overlap. Cards, seeds, PDFs, scale choices and component git hashes are **unassigned/unpinned blockers**, not implicit defaults. No process card is labelled validated in Phase 00.

## Checks and phase disposition
Environment and PDF evidence collection is complete. Report tables are audit summaries; physics plots/cutflows are not applicable because no events were generated. Existing preflight was preserved and verified by hash. Required report/index existence and expected content are checked after writing, with evidence in 00_report_verification.txt. Full pipeline, cross-section, decay, merging and detector tests remain unperformed. Phase status remains BLOCKED; no physics sign-off or observability claim is made. Stop here as requested.
