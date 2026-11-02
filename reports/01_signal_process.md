# Phase 01 — scientific signal/process definition audit

Date UTC: 2026-11-02. **Status: BLOCKED.** Scientific definition and implementation proposal documented; no generator syntax execution, amplitude validation, cross section or decay closure test completed. This is not a Phase 01 pass. Stop here for human review; Phase 02 and production remain gated.

## Goal, provenance and storage

Define EW pp -> ZHjj at sqrt(s)=13.6 TeV, followed by Z -> ee/mumu and H -> gamma gamma, for an unknown-research projection at 500 fb^-1. There are no calculated yields, efficiencies or significances. No event generation, installation, build or batch submission occurred.

Read AGENTS.md, PROJECT_BRIEF.md, Phase 00 and the supplied reference extraction. Fresh evidence is in [01_environment_evidence.txt](01_environment_evidence.txt), [01_capabilities_evidence.txt](01_capabilities_evidence.txt), [01_reference_text.txt](01_reference_text.txt) and [01_sources/manifest.txt](01_sources/manifest.txt). The first two logs record literal probe commands, outputs and individual exit codes; directory inventories additionally record exact roots. Local reference SHA256 remains `3a456511c4b1faa69397394895f42ea4b76d466580b1c30d51d58154804fcd0a`. Its methodology concerns continuum Zgamma gamma jj, not this Higgs signal. Reference pp. 4–5 specify MG5 3.6.3, 13.6 TeV, Pythia8, Delphes 3.5, CMS card and MLM QCD samples; none supplies our missing signal rate or H decay validation.

Actual path checks preceded writes. All new cards, source snapshots, extraction, evidence, reports and checksums are under `/eos/home-r/rjiang/vbs_zh_codex_starter`. No AFS or /tmp project files were created this turn. CVMFS is read-only external infrastructure inspected at the user's request; it is not a project installation. Future persistent caches, sources, builds, logs, Git metadata and events must also be on EOS; any local /tmp runtime state must be unavoidable and cannot be the only reproducibility record. No credentials, Codex home or configuration were changed.

The sandbox again failed during startup trying to create the absent project `.git`; subsequent tools used explicit escalation, not an alternate storage location. Host for this audit is lxplus9109.cern.ch, distinct from the previous host. CLI verified `codex-cli 0.158.0`. User stipulates this same session, GPT-6-Astra default and unchanged reasoning configuration; no model switch, upgrade or subagent was used. Live `/status` cannot be obtained through this tool interface; exact active effort remains unverified rather than invented.

Source-control work was done first: [01_source_control.md](01_source_control.md) proposes a nested standalone EOS repository. No Git init, add or commit was run. Parent HEAD `6ea6cb9462533bbc1b209f7d4b4b67fd49b4d737` is NOT this project's snapshot; scoped tracked-file list is empty. Project commit remains a blocker, with hashes supplying interim provenance.

## Scientific definition and gauge invariance

The central theoretical object is the complete on-shell Born EW amplitude for each allowed partonic initial/final state ab -> Z H c d, summed coherently over every diagram at QCD amplitude order 0 and EW/Yukawa amplitude order 4. Convolve with explicitly specified proton PDFs and sum distinct external flavours with the generator's symmetry factors. Its squared rate is O(alpha_EW^4). No topology filters, required intermediate vector bosons, s-channel exclusions or internal-particle vetoes define the signal. Completeness is relative to the specified SM parameter/flavour scheme, which still needs sign-off below.

This includes vector-boson exchange/scattering configurations, radiation from quark lines, crossed/identical-quark terms, and Higgsstrahlung-like s-channel configurations such as associated ZVH with V -> qq. Their same-order interference belongs inside the signal. “VBS” or “VBF-like” describes a later fiducial region of this full amplitude, not a separately measurable diagram subset. Large mjj, separated tagging jets and central Z/H can enrich that region without removing diagrams. A cut on final-state mjj (including a possible resonance-region control bin) is an observable; a diagram veto on a hadronic W/Z is a different and generally unsafe operation. No numerical VBS fraction is asserted.

The on-shell Z and H definition uses a pole/narrow-width approximation. It does not claim to equal the complete off-shell ll gamma gamma jj amplitude. Preserve the Z spin density matrix using a correlated ME decay chain (or validated MadSpin Z decay); preserve the scalar H two-body decay in its rest frame. The physical H pole residue/decay factorization is a controlled approximation whose continuum interference must be assessed separately. Finite widths in off-shell internal W/Z poles require a consistent gauge treatment; compare a supported complex-mass or pole scheme and gauge checks, not arbitrary fixed-width edits.

Proposed practical baseline: five-flavour proton and jet labels explicitly containing g,u,d,s,c,b and antiquarks, no photon or top PDF, massless b and light quarks and zero corresponding Yukawas, diagonal CKM. The available `sm-no_b_mass` restriction supports this approximation. It is preferable to silently relying on MG5's multiparticle defaults. The on-shell pure EW tree sample has no external gluon contribution even though g is in the labels. External flavour selection is distinguishable from diagram deletion and can define gauge-invariant components.

However, the full physical SM includes nonzero bottom/charm Yukawas and CKM mixing. The massless baseline is **not yet certified as complete physical SM**. Compare a compatible massive-bottom/4FS calculation and retained heavy-Yukawa contribution, choose a consistent PDF flavour scheme, and document CKM effects. Do not simply combine 4FS and 5FS samples or arbitrarily remove internal top lines. If b-related resonant top configurations occur in the generated external states, inspect and treat their full amplitudes/resonances consistently before assigning other-production labels. Top and photon-initiated external states are outside the proposed Born PDF definition; quantify relevant additions rather than silently claiming they vanish. This flavour decision remains a Phase 01 blocker.

## Coupling derivation and candidate MG5 syntax

For a renormalizable tree 2 -> 4 process, the total coupling degree is four (quartic vertices count two; a Yukawa counts one). Thus M_EW ~ g_EW^4 and M_QCD ~ g_s^2 g_EW^2, giving the following bookkeeping before decays:

| Component | Amplitude orders (QCD,QED) | Rate order | Treatment |
|---|---|---|---|
| Complete tree EW | (0,4) | alpha_EW^4 | signal |
| Tree QCD-induced ZHjj | (2,2) | alpha_s^2 alpha_EW^2 | separate resonant-H component |
| EW–QCD cross term | (0,4) x (2,2) | alpha_s alpha_EW^3 | signed contribution; evaluate |
| EW with explicit ll | (0,5) | alpha_EW^5 | before H decay; finite-width/pole comparison |
| QCD with explicit ll | (2,3) | alpha_s^2 alpha_EW^3 | alternative decayed QCD control |
| Cross term with ll | squared orders (2,8) | alpha_s alpha_EW^4 | if same external ll states |

These rate powers are formal fixed-width ME counting. Integrating a resonant Z propagator gives its inverse-width factor; the physical narrow-width relation is sigma(ZHjj) times BR(Z->ll), not an extra ad hoc alpha suppression. H diphoton loop factors are contained in the decay width/BR, not in the Born production `QED` setting.

The official [MG5 coupling-order documentation](https://amcatnlo.web.cern.ch/co.htm) says `=` means an upper bound, `==` equality, and `^2` restricts powers in the squared amplitude. With omitted orders MG5 may prioritize QCD. This was cross-checked against the installed candidate's `madgraph/interface/madgraph_interface.py` help text and SM `coupling_orders.py`. This verifies the documented meaning, **not successful parsing or physics of our process**. The [official input examples](https://cp3.irmp.ucl.ac.be/projects/madgraph/wiki/InputEx) also caution about intermediate-state restrictions.

[Candidate cards](../cards/phase01_candidates/README.md) contain separate calculations, no output/launch instructions:

```text
import model sm-no_b_mass
define p = g u c d s b u~ c~ d~ s~ b~
define j = g u c d s b u~ c~ d~ s~ b~
generate p p > z h j j QCD=0 QED==4
```

Alternative Z decays: `generate p p > z h j j QCD=0 QED==4, z > e+ e- QED==1`, plus a separate `add process` for mu+ mu-. The stored off-shell control uses `p p > e+ e- h j j QCD=0 QED==5` plus muons, with no required intermediate Z, allowing all permitted nonresonant/Z/gamma* terms at that order. It must not be added to the on-shell sample. Use matching cuts, mll window and width schemes to measure the approximation.

QCD candidate: `p p > z h j j QCD==2 QED==2`. Interference candidate: `p p > z h j j QCD<=2 QED<=4 QCD^2==2 QED^2==6`. Combined closure candidate: `p p > z h j j QCD<=2 QED<=4`. Verify actual orders and any additional sectors in the generated subprocess list before interpreting the last sample as exactly EW+QCD+interference. The signed interference cannot be assigned a positive unweighted sample or assumed zero from colour intuition. All syntax remains **UNTESTED**, including restriction import and decay-chain order scoping.

Proposed run specifications: proton beams 6800 GeV each, mH=125 GeV, initial parton jet pT>20 GeV, |eta|<5 and DeltaRjj>0.4. Loosen generation cuts for convergence checks; no final mjj/Deltaeta optimization is selected. A candidate baseline scale is HT/2 with HT=sum transverse masses of Z,H and two partons; the actual MG5 scale implementation must be verified, not guessed via an integer option. PDF set/member/order/alpha_s and scale choice are unpinned. Off-shell ll requires mll>50 GeV and aligned lepton acceptance. Photon cuts occur after decay. Candidate seed 13600501 is reserved for a future short check, **not used**; independent-repeat seeds and event counts remain unassigned. No run card is production-ready.

## H -> gamma gamma and branching normalization

The renormalizable tree SM has no HAA vertex. A static AST inspection of the available `models/sm/vertices.py` finds none; `sm`, `loop_sm` and `hgg_plugin` directories exist, but directory presence proves neither a complete loop-decay implementation nor a validated effective model. Do not append `h > a a` to this tree-SM process. MadSpin is not assumed to supply a missing SM loop decay. Do not change production to HEFT merely to manufacture a decay vertex.

Proposed implementation: generate correlated Z->ee/mumu with an undecayed on-shell H, pass LHE to Pythia8, and force only H->gamma gamma. The [Pythia decay controls](https://pythia.org/latest-manual/ParticleDataScheme.html) document `25:onMode = off`, `25:onIfMatch = 22 22`; `25:mayDecay = on` is included. Two-body scalar decay is isotropic for this unpolarized observable. The loop physics determines the physical partial width; forced-decay probability one is only a sampling choice. Preserve finite-H-width settings consistently if enabled and verify energy/momentum conservation and rest-frame angular distributions.

The [Pythia Higgs manual](https://pythia.org/latest-manual/HiggsProcesses.html) documents `HiggsSM:NLOWidths = on`. Its bundled 8.315 manuals were archived because web access returned 403. The XML static PDG-25 table has BR(gamma gamma)=0.0028438 and width=0.00374 GeV, whereas the inspected MG5 restriction has width=0.00638233934 GeV. Neither is our physical normalization input. Pythia resonance initialization can recompute widths; SLHA input can affect precedence. Inspect initialized data with all decays enabled before imposing the filter, then inspect after filtering, including logs of which decay table won. Do not infer the runtime BR from the XML alone. A complete driver, LHE/SLHA precedence and normalization closure are still unimplemented.

Proposed physical inputs, fixed for this audit at mH=125.00 GeV: BR(H->gamma gamma)=0.002270 and total width 0.004088 GeV, from the [LHCHWG YR4 BR table](https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageBR). The diphoton relative uncertainties are theory +1.73/-1.72%, quark-mass +0.93/-0.99%, alpha_s +0.61/-0.62%; preserve source components/correlations before constructing nuisances. These are identified YR4 inputs, not a claim of a newly computed latest BR. Archived numerical rows are in 01_sources/higgs_125_rows.txt. The [PDG 2025 Z listing](https://pdg.lbl.gov/2025/listings/rpp2025-list-z-boson.pdf), decay-mode summary, gives BR(ee)=0.033632 and BR(mumu)=0.033662, with absolute uncertainties 0.000042 and 0.000066. Sum B_ll=0.067294; do not replace it by another factor of two when both channels are already generated. Their covariance must be retained if propagating precision BR errors.

The exact accounting contract is:

- Undecayed production: sigma_prod in fb; sigma_decay = sigma_prod * (B_ee+B_mumu) * B_gg. With these inputs the BR product is 0.00015275738. This is a branching product, not a rate or yield. Flavour-dependent efficiencies require sigma_fid = sigma_prod * B_gg * (B_ee*A_ee+B_mumu*A_mumu).
- ME Z-decayed sample: its cross section already contains its model Z partial width/total width. In a controlled pole calculation normalize each flavour by B_l(physical)/B_l(ME), if adopting the physical PDG normalization; do not multiply again by B_ll. Establish B_l(ME) from the consistent uncut pole normalization or decay widths, not from an acceptance-limited ratio. Do not combine incompatible cuts or width schemes.
- Full off-shell ll sample: use its computed llHjj rate and multiply only by B_gg. A constant Z branching rescale is not generally justified for the nonresonant component. Quote the scheme difference rather than applying both prescriptions.
- External forced-H decay: attach B_gg once to an input rate that has no H decay. Verify whether the chosen shower interface modifies weights/cross sections for forced resonances; define a ledger factor recording already-applied BRs. If that interface already supplies B_gg, the external factor is one. Never multiply B_gg twice, and never use conditional BR=1 as the physical BR.

For a sample whose weights are normalized to its preselection cross section, selected yield is L*sigma_norm*sum_selected(w)/sum_all(w). Persist normalization denominator, generated/tried/accepted counts and filter efficiencies; distinguish pb from fb (1 pb=1000 fb). If event weights already carry cross-section units use their documented sum normalization instead. Weighted MC variances require sum(w^2) and the integration/normalization uncertainty; signed-interference errors need covariance or a separate signed estimator. No MC count, rate or uncertainty is currently available; none is reported as zero.

## Interference, overlap and other Higgs checks

| Issue | Required accounting/check |
|---|---|
| EW internal topologies | Keep all diagrams and their interference. Study mjj near W/Z poles and VBF-like region using observable bins, not diagram labels. |
| EW vs QCD ZHjj | Compute pure components, signed cross term and full coherent sum with identical inputs/cuts; require closure statistically and at phase-space points. |
| ZVH with V->jj | Already partly represented in full EW ZHjj. Do not add separate ZWH/ZZH hadronic samples for the same external state without a validated exclusive scheme. |
| QCD ZH + 0/1/2 jets | A merged alternative to fixed ZHjj plus shower; do not add overlapping inclusive and two-jet samples. Validate matching scales and jet transitions. |
| Loop-induced ggZH(+jets) | Not included by a tree `QCD==2` sample. Needs validated loop model/orders, exact masses, matching scheme and separation from corrections to tree ZH. No syntax guessed here. |
| Higgs-pole vs continuum ll gamma gamma jj | Assess interference with a consistent loop/effective Hggamma decay amplitude, full continuum, common widths and mass window. A forced Pythia decay alone cannot calculate it. Check mass-shape/sideband effects; do not transfer the reference's interference fraction. |
| ggF/VBF H, WH, ttH, tH, bbH | Additional leptons/jets can enter the reconstructed selection. Define distinct external states/decays and veto overlap with EW ZHjj/ZVH; do not assume negligible yields or classify solely by generator ancestry. |
| Z->tautau feed-down | Not primary ee/mumu signal; separate physical final state with neutrinos and its own selection/normalization. |
| Prompt photons vs showers/fakes | Phase 02 must define mutually exclusive prompt Zgamma gamma, Zgamma+jets and Z+jets regions, including QED shower photons/FSR. Hard-ancestry veto alone is not proof of exclusivity. Fake scenarios require uncertainties; no Delphes-only fake prediction is certified. |

No mass window is optimized here. Reserve diphoton signal/sideband regions before later expected-yield optimization, carry mass-resolution and interference effects into that model, and avoid maximizing noisy cut scans.

## Available stack and exact compatibility findings

All paths below are read-only candidates, not selected installations. Prefix A = `/cvmfs/sft.cern.ch/lcg/releases/LCG_108`; architecture = `x86_64-el9-gcc13-opt` unless stated.

| Component | Evidence | Disposition |
|---|---|---|
| MG5 | A/MCGenerators/madgraph5amc/3.5.9.atlas13/architecture; VERSION says 3.5.9 (2025-06-04), LCG manifest ebc2d, version.txt embeds 2543b | ATLAS patch provenance not audited; these identifiers are not git commits. Not paper 3.6.3, not adopted. |
| Other MG5 | Common release-directory inventory has 3.1.0 and many ATLAS 3.x candidates, no matching 3.6.3 directory in that scope | No unpatched compatible paper-version executable established. This is not an exhaustive absence claim across CVMFS. |
| Pythia8 | A/MCGenerators/pythia8/315/architecture; manifest 4b2bb; bundled htmldoc and particle XML read | 8.315 candidate, runtime/driver untested; exact upstream commit and tune unpinned. |
| LHAPDF | A/MCGenerators/lhapdf/6.5.5/architecture; fc9c9 | Package share/LHAPDF contains only lhapdf.conf and pdfsets.index. Shared grids exist under /cvmfs/sft.cern.ch/lcg/external/lhapdfsets/current (inventory saved), but a mutable current link and directory availability do not pin PDF set/member/data hash. |
| Delphes prerelease | A/delphes/3.5.1pre12/architecture; ae61c; built for ROOT 6.36.02 | Not adopted. Bare ldd misses libDelphes.so and libpythia8.so and resolves ROOT from /usr. |
| Delphes stable | /cvmfs/sft.cern.ch/lcg/releases/delphes/3.5.0-90626/x86_64-centos9-gcc11-opt | version.txt requires ROOT 6.26.08-69213, Python 3.9.12-9a1bc; bare ldd misses libDelphes.so and resolves system ROOT 6.40.04. Not a verified compatible runtime. |
| Current shell vs LCG | Python 3.9.25, GCC 11.5.0, ROOT 6.40.04 vs LCG Python 3.12.11, gcc13 architecture, ROOT 6.36.02 | Do not mix PATH/library environments. ldd also picks a CVMFS GCC13 libstdc++; a working C++ ABI cannot be inferred from gcc --version. |
| Event interface | Stable Delphes bin inventory includes HepMC2/3 readers; LCG manifest includes HepMC2 2.06.11 | Select matching Pythia writer/Delphes reader and preserve weights/units in a tiny test; existence alone is not interoperability. |

Missing libraries are observations in the unsourced current shell, not proof the CVMFS packages are intrinsically broken. No setup script was sourced or binary generation launched. Stable Delphes is a viable investigation path, not automatic approval to mix it with LCG_108. A coherent version decision is required before smoke tests.

## Validation plan and phase gate

1. Human review: approve the full-EW pole definition, five-flavour approximation versus heavy-Yukawa/CKM completion, physical BR convention, and a coherent unpatched MG5/stable Delphes stack (or explicitly justified alternatives). Capture same-session `/status` and establish project Git isolation/snapshot. No settings changes are requested.
2. Later short syntax/amplitude audit only after that decision: import the pinned model, inspect restrictions and all couplings, generate each card independently in an EOS work directory, save subprocess lists, diagram output, coupling-order counts, card/model hashes and gauge/permutation/Lorentz checks. Require supported gauge/width comparison with numerical precision checks at ordinary and high-energy points. No production syntax becomes “validated” from documentation alone.
3. Later small integration: fixed PDFs/member/alpha_s and identical cuts/seed policy; compare EW+QCD+signed interference with coherent total, on-shell vs full ll, ee vs mumu before detector effects, width variation and hadronic V resonance bins. Independently reproduce normalization in a separate analysis calculation/code path; another Codex agent is not needed or permitted. Document MC errors; repeat independent seeds. Agree tolerances before seeing results, using integration errors and numerical stability rather than a blanket percentage.
4. Decay closure: inspect pre/post-initialization PDG25 and SLHA tables, force two photons, verify mothers/kinematics, preserve Z spin correlations, record all input/output weight sums and failure counts. Reproduce expected external BR scaling in both flavours; compare an independent scalar-decay calculation or validated decay tool. Validate a physical-BR inclusive control statistically if feasible on batch, not by expecting rare gamma gamma counts in a tiny sample.
5. Theory uncertainties: factor-two muR/muF variations (seven-point where applicable), PDF/alpha_s variations, missing higher-order EW/QCD effects, flavour/CKM/pole-width differences, shower/tune and matching uncertainties, BR components. Pure Born EW has no explicit alpha_s power; a small scale band is not proof of small missing EW corrections. No assumed K-factor, interference size or percent production uncertainty is assigned.
6. Phase 02 must pass the exclusive background/overlap ledger before extensive MC. Later phases add detector photon efficiency/mass resolution, fake-rate scenarios, weighted cutflows and systematic likelihood/MC-stat checks. Nothing here authorizes bulk jobs on lxplus.

Executable non-destructive next probes (read-only; NOT an installation recipe):

```bash
cat /cvmfs/sft.cern.ch/lcg/releases/delphes/3.5.0-90626/x86_64-centos9-gcc11-opt/delphes-env.sh
cat /cvmfs/sft.cern.ch/lcg/releases/LCG_108/MCGenerators/madgraph5amc/3.5.9.atlas13/x86_64-el9-gcc13-opt/madgraph5amcenv-genser.sh
ls /cvmfs/sft.cern.ch/lcg/external/lhapdfsets/current
```

Inspect setup paths before choosing a coherent environment. If a vetted upstream release must later be downloaded/built, stage verified source/checksums under project `software/sources`, build under project `software/build`, install under project `software/install`, and send substantial compilation to batch. Configure tool-specific caches and TMPDIR to verified EOS subdirectories; do not repurpose HOME/CODEX_HOME. No install command is supplied until upstream provenance and compatibility are pinned.

## Checks, caveats and disposition

Documentation and source-level inspection completed; numerical generator implementation **not validated**. All six MG5 cards are marked UNTESTED; no `output` or `launch` is present. Higgs decay is a documented candidate fragment, not a complete tested shower job. Source-table extraction initially failed UTF-8 decoding and was rerun explicitly as Latin-1; numerical cells are saved. Official web sources were downloaded to EOS and hashed; no sole /tmp records were used. Git remains proposal-only; no unrelated parent data or configuration was changed.

Tables above are audit outputs; plots and event cutflows are not applicable because no MC was generated. No selected event count or cross section exists. Verification and hashes are in 01_report_verification.txt and SHA256SUMS_01.txt. Critical unresolved items are stack choice/pins, physical flavour/width prescription, executable diagram/subprocess/gauge validation, H decay/weight closure, project commit and live session status. Phase 01 remains **BLOCKED** and stops for human review.
