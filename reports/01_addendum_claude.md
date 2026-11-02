# Phase 01 addendum — executed card audit and decisions (Claude Code)

Date UTC: 2026-11-02. **Status: PASS for the signal definition and Z/H decay accounting at LO (executed evidence below); flavour-scheme completeness remains a documented systematic (D2).** Supersedes nothing in [01_signal_process.md](01_signal_process.md) (unchanged, sha256 10ef6bca…); it closes items marked there as untested. Stack: [03_stack.md](03_stack.md). Numbers: [03_generation_validation.md](03_generation_validation.md).

## A. Executed parse audit of the six Phase 01 cards (MG5_aMC 3.6.3 upstream, `sm-no_b_mass`)
Command: `mg5_aMC work/m2_parse/<card>.parse.mg5` (card body verbatim + `display processes`); logs `work/m2_parse/*.parse.log`.

| Card | Result | Subprocesses / diagrams | Finding |
|---|---|---|---|
| ew_on_shell | parses | 87 / 1344 | no gluon-initiated/final subprocess (0 found) → pure EW as intended |
| qcd_on_shell | parses | 95 / 520 | (2,2) incl. gg/qg channels |
| ew_qcd_combined | parses | 107 / 1864 | **1344 + 520 = 1864**: combined = union of EW and QCD diagram sets (no extra sector) |
| ew_qcd_interference | parses | 75 / 1572 | MG5 echoes `QED<=4 QCD^2==2 QED^2==6` (amplitude `QCD<=2` implied) |
| ew_offshell_ll | parses | 174 / 5232 | ee+μμ, includes γ*/Z and non-resonant terms |
| **ew_z_decay** | **FAILS** | — | `Decay processes cannot specify squared orders constraints.` MG5 maps `QED==n` to a squared-order constraint. **Correction:** `p p > z h j j QCD=0 QED=4, z > l+ l-` (with `QCD=0`, `QED<=4` is equivalent to `==4` for a 2→4 tree). |

## B. Corrections / additions (evidence-backed)
1. **Decay-chain syntax** — fixed as above (cards/phase03_smoke/ew_zhjj_zll.mg5); executed: 174 subprocess, σ = 1.298 ± 0.008 fb.
2. **`maxjetflavor` defaults to 4** in the 3.6.3 run card (`banner.py add_param("maxjetflavor", 4)`); with b in `j` this must be 5 (and `asrwgtflavor 5`) — now pinned.
3. **`cut_decays` defaults to False** — lepton cuts would not act on Z daughters; we keep it False deliberately (generation cuts on jets only), leptons/photons cut at analysis level → clean BR closure.
4. **Scale** `dynamical_scale_choice=3` verified in `Template/LO/SubProcesses/setscales.f` as Σ m_T / 2. MLM samples must use −1.
5. **Z→ll BR closure (executed)**: σ(ZHjj→llHjj)/σ(ZHjj) = 0.06964 ± 0.00083 vs analytic tree 2Γ_ll/Γ_Z(MG) = 2·83.965 MeV/2.441404 GeV = 0.06878 (pull 1.0) → **PASS**. Per-flavour rescale to PDG: B_ee 0.033632/0.034392 = 0.9779, B_μμ 0.033662/0.034392 = 0.9788 (combined 0.9783).
6. **H→γγ route (executed)**: Pythia 8.317 forced `25:onIfMatch = 22 22` → 1000/1000 last-copy H decay to γγ (gen record). Pythia σ_gen = 1.290 fb equals LHE input 1.286–1.292 fb ⇒ **Pythia does not fold BR into σ for LHE input; B_γγ = 0.002270 is applied once externally** (contract of 01_signal_process.md confirmed). SLHA H decay table from MG5 is ignored by Pythia ("empty DECAY table … no BRs"), so no hidden BR.
7. **EW×QCD interference (executed, loose cuts)**: σ_I = −0.114 ± 0.007 fb = −0.61% of σ_EW (18.64 ± 0.19 fb).
8. Off-shell/pole comparison and 4F/heavy-Yukawa comparison: **not executed** (batch item, Phase 03b).

## C. Decisions (defaults taken; reversible unless noted)
| ID | Decision | Default adopted | Needs user? |
|---|---|---|---|
| D1 | Signal = full EW (0,4) ZHjj, on-shell Z (ME decay chain, spin-correlated), H undecayed in ME; off-shell llHjj as systematic only | adopted | no |
| D2 | 5F massless-b, diagonal CKM, `sm-no_b_mass`; 4F/massive-b + Yukawa as later systematic | adopted | no (systematic) |
| D3 | Stack LCG_110 + upstream MG5 3.6.3 (git tag; see 03_stack) | adopted | no |
| D4 | PDF NNPDF31_nnlo_as_0118 (303600) in ME and PY8; scale Σm_T/2 (fixed order), CKKW (MLM); 7-pt scale + PDF weights stored | adopted | no |
| D5 | Z BR: ME tree BR rescaled per flavour to PDG 2025; B_γγ (YR4) external, once | adopted | no |
| D6 | H decay: Pythia forced γγ, conditional BR = 1 | adopted (validated) | no |
| D7 | EW–QCD interference: separate signed term; assigned as signal-model uncertainty unless |I|/S > 10% after selection | adopted | **yes if threshold exceeded** |
| D8 | Shower: CP5; `SpaceShower:dipoleRecoil=on` for EW/VBS samples, global recoil for QCD samples (swap as systematic) | adopted | no |
| D9 | Gen cuts ZHjj: p_T(j)>20, |η(j)|<5, ΔR(jj)>0.4, no lepton cuts (`cut_decays=F`) | adopted | no |
| D10 | Project-local Git (`git init` per 01_source_control.md) | **not executed** | **yes — approval required** |
| D11 | Delphes card: (a) slim output (Particle branch = 80 % of 106 kB/event; in-job skim keeps generator overlap flags); (b) electron-before-photon priority (tested: ee pairs 127→141, minor); (c) electron isolation study for the 35 % vs 64 % ee/μμ pair efficiency (03 §4) | (a) adopted as a storage-only change; (b, c) Phase 04 | **yes for (b, c) (detector-model change)** |
