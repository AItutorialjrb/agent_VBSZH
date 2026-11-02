# M4 — software stack selection

Date UTC: 2026-11-02. **Status: PASS** (stack coherent and exercised end-to-end in M5; one documented provenance caveat for MG5).
Activation: `source scripts/setup_stack.sh` (single environment; never mix with system ROOT/Python or other LCG views).

## Selection
| Component | Version / build | Path / source | Why |
|---|---|---|---|
| Base | LCG_110 view `x86_64-el9-gcc13-opt` (newest numbered LCG; 110a identical generators) | /cvmfs/sft.cern.ch/lcg/views/LCG_110/x86_64-el9-gcc13-opt | first LCG with **stable Delphes 3.5.1** (LCG_108/109 ship only 3.5.1pre12/pre14) |
| MG5_aMC | **3.6.3 upstream** (reference-paper version), git tag v3.6.3, date 2025-06-12 | `software/install/MG5_aMC_v3.6.3`; source `software/sources/MG5_aMC_v3.6.3_github.tar.gz` sha256 `2bb0d085a37b704ef956e8e8ed468bdcfef13e638c82ed3f1c4e968a090ebd98` | all CVMFS MG5 builds are ATLAS-patched (`3.5.9.atlas13` … `3.8.1.atlas1`); avoided per brief |
| Pythia8 | 8.317 (LCG hash fcd99), LHAPDF6 plugin present | LCG view | — |
| Delphes | 3.5.1 (718d3), `DelphesPythia8` linked to the same view's libpythia8/ROOT (ldd checked) | LCG view; CMS card sha256 `e363da8b…5028c0` | stable release |
| ROOT / Python / GCC | 6.40.02 / 3.13.11 / 13.1.0 (gfortran 13.1.0) | LCG view | — |
| LHAPDF | 6.5.5; set NNPDF31_nnlo_as_0118 (LHAID 303600, 101 members, DataVersion 1, member-0 sha256 `dd261226…966817`) | /cvmfs/sft.cern.ch/lcg/external/lhapdfsets/current | CMS-standard PDF; matches CP5 |
| HepMC2/3, FastJet | 2.06.11 / 3.3.1, 3.5.1 | LCG view | not needed by DelphesPythia8 path |
| uproot / awkward / numpy | 5.7.1 / 2.9.0 / 2.4.4 | LCG view | analysis |

## Checks (executed)
- `mg5_aMC` runs under Python 3.13 (only harmless `SyntaxWarning: invalid escape sequence` from MG5 sources). LHAPDF interface: "Using LHAPDF v6.5.5 interface for PDFs"; α_s updated from PDF (0.1180).
- MG5 run wrote `lhapdf_py3 = lhapdf-config` into `software/install/MG5_aMC_v3.6.3/input/mg5_configuration.txt` (project-local; documented).
- Pythia σ/LHE closure and Delphes output: see 03_generation_validation.md.

## Caveats
1. **MG5 provenance**: the official launchpad release tarball was unreachable (HTTP 404 on the tried URLs), so the GitHub tag archive is used. Because it still contains `bin/create_release.py`, MG5 prints "UNKNOWN DEVELOPMENT VERSION – DO NOT USE FOR PRODUCTION" (`madgraph_interface.py:219`). The code is the v3.6.3 tag; this is a packaging marker, not a code difference. It was **not deleted** (file deletions need user approval). Remedy if desired: obtain the official tarball (e.g. from a CERN mirror) and compare the tree with `diff -r`.
2. `eos quota` returns "no quota for path /eos/user/r/rjiang" from this node; the Phase 00 figure (~780 GB used of 2 TB) is the best available quota estimate. Check before bulk production: `eos quota ls -u rjiang` or the CERNBox web quota.
3. HTCondor: the standard schedd rejects `/eos` paths. Jobs are submitted through **EosSubmit** schedds: `bash -lc 'module load lxbatch/eossubmit; condor_submit …'`.
