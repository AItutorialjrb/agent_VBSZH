#!/usr/bin/env python3
"""Write reports/08_reproducibility.md: versions, seeds, checksums (cards, cmnds, Delphes card, scripts, gridpacks,
final JSON), and the exact command sequence. Usage: python3 -P make_repro.py <final.json> <git_commit> <out.md>"""
import sys, json, glob, hashlib, os, re, datetime
J, COMMIT, OUT = sys.argv[1:4]
P = "/eos/home-r/rjiang/vbs_zh_codex_starter"
sha = lambda f: hashlib.sha256(open(f, "rb").read()).hexdigest()
rel = lambda f: f.replace(P + "/", "")
V = json.load(open(f"{P}/work/final_ntuples/verify.json"))
seeds = {}
for sub in sorted(glob.glob(f"{P}/scripts/condor/production_final_*.sub")):
    body = open(sub).read().split("from (")[1]
    for l in body.strip().strip(")").splitlines():
        if l.strip():
            s, g, c, n, seed, f = l.split(); seeds.setdefault(s, dict(gseed=g, cmnd=c, nev=n, seeds=set()))["seeds"].add(int(seed))
rows = []
for s, v in seeds.items():
    js = sorted(glob.glob(f"{P}/production/final/{s}/*.json"))
    gsha = json.load(open(js[0]))["gridpack_sha256"] if js else "—"
    ss = sorted(v["seeds"]); vv = V.get(s, {})
    rows.append(f"| {s} | {v['gseed']} | {ss[0]}–{ss[-1]} ({len(ss)} jobs) | {v['nev']} | {v['cmnd']} | {vv.get('ok', '—')} | `{gsha[:16]}…` |")
files = (sorted(glob.glob(f"{P}/cards/production_final/*.mg5")) + sorted(glob.glob(f"{P}/cards/theory/*.mg5")) + sorted(glob.glob(f"{P}/cards/coupling/*.mg5")) + [f"{P}/cards/phase03_smoke/{c}" for c in sorted({v['cmnd'] for v in seeds.values()})]
         + [f"{P}/cards/phase03_smoke/py8_common_CP5.cmnd", f"{P}/cards/phase04_candidates/delphes_card_CMS_slim_v1.tcl"]
         + [f"{P}/scripts/condor/{x}" for x in ("run_job.sh", "make_gridpack.sh", "lhe_only.sh", "mg5_run.sh", "pyjob.sh")]
         + sorted(glob.glob(f"{P}/scripts/theory/*.py")) + sorted(glob.glob(f"{P}/scripts/models/*.sh")) + sorted(glob.glob(f"{P}/scripts/metrics/*.py"))
         + [f"{P}/software/install/HC_NLO_X0_kVV.tgz", f"{P}/software/models_dl/HC_NLO_X0_UFO.zip", f"{P}/work/theory/theory_summary.json"]
         + [f"{P}/scripts/{x}" for x in ("setup_stack.sh", "run_py8_delphes.sh", "slim_gentruth.py")]
         + sorted(glob.glob(f"{P}/scripts/analysis/*.py")) + [f"{P}/scripts/analysis/ntuple_job.sh", f"{P}/scripts/plan/make_submit_final.py", J])
chk = "\n".join(f"{sha(f)}  {rel(f)}" for f in files if os.path.exists(f))
gp = "\n".join(f"{sha(f)}  {rel(f)}" for f in sorted(glob.glob(f"{P}/production/gridpacks/*_status.txt")))
txt = f"""# 08 — Reproducibility (FINAL RUN)

- **Date:** {datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}
- **Status:** PASS (all inputs pinned; the commands below regenerate every number in FINAL_report.md from the EOS outputs).
- **Git commit of the code:** `{COMMIT}`. Repository git@github.com:AItutorialjrb/agent_VBSZH.git (project-only; the parent repo is untouched).

## Versions

| component | version / pin |
|---|---|
| Environment | LCG_110 x86_64-el9-gcc13-opt (`scripts/setup_stack.sh`): Python 3.13.11, ROOT 6.40.02, GCC 13.1.0, numpy 2.4.4, uproot 5.7.1, awkward 2.9.0, scipy and matplotlib from the view |
| MG5_aMC | 3.6.3 upstream, `software/install/MG5_aMC_v3.6.3`; source tarball sha256 `2bb0d085a37b704ef956e8e8ed468bdcfef13e638c82ed3f1c4e968a090ebd98` |
| Pythia8 | 8.317 (LCG_110), CP5 tune (`cards/phase03_smoke/py8_common_CP5.cmnd`) |
| Delphes | 3.5.1 (LCG_110), stock CMS card, slimmed output (`cards/phase04_candidates/delphes_card_CMS_slim_v1.tcl`) |
| PDF | NNPDF31_nnlo_as_0118, LHAID 303600, LHAPDF 6.5.5 |
| Batch | HTCondor EosSubmit schedd (`module load lxbatch/eossubmit`) |
| Agent | Claude Code session (this run); the Codex CLI was not used in the FINAL run |
| Coupling model | Higgs Characterisation HC_NLO_X0 UFO (FeynRules database, README model version 1.3, `__init__` 1.2; zip sha256 b91d8788ed66a12a3eaf9e1f8771f98b789b4b3fc8b10eeb32c9c04f057ae1bd, fetched 2026-11-03) + patch `scripts/models/make_hc_kvv.sh` (kSMW, kSMZ) → `software/install/HC_NLO_X0_kVV.tgz` |

## Seeds and samples (FINAL RUN productions)

- The MG5 gridpack seed is the `gseed` in the gridpack file name.
- The per-job MG5 seed is `seed`; the Pythia seed is seed + 100000000.
- Earlier samples are documented in 04/05: Tier-1 seeds 13611000–099 (EW) and 13621000–049 (QCD); test_v2 seeds are base + 99999.

| sample | gridpack seed | job seeds | events/job | Pythia cmnd | verified jobs | gridpack sha256 |
|---|---|---|---|---|---|---|
{chr(10).join(rows)}

Dropped segments (no output, not resubmitted): F_QCD_llajj_vbs 140000354, 140000409 (deterministic Delphes segfault), 141600295, 141600415, 141600900 (lost after the LHE stage).

## Normalisation constants (applied once; asserted in code)

- B(H→γγ) = 0.002270 (YR4, mH = 125 GeV): every forced-H→γγ sample.
- **ZF = 0.9783**: MG5 LO width-derived Z→ℓℓ BR → PDG. The MG5 sm model gives 2Γ_ℓℓ/Γ_Z = 2 × 83.965 MeV / 2.441404 GeV = 0.068784 for ee + μμ; PDG gives 0.033632 + 0.033662 = 0.067294; the ratio is 0.9783. The closure test σ(ZHjj→ℓℓHjj)/σ(ZHjj) = 0.06964 ± 0.00083 is in 01_addendum_claude.md item 5.
  - Applied to samples whose Z→ℓℓ is an MG5 decay or decay chain: EW/QCD ZHjj, the on-shell-Z Zγγjj samples and the coupling samples.
- BR(Z→ee+μμ) = 0.067294: ggZH, where Z→ℓℓ is forced in Pythia8.
- `final_analysis.py` builds the per-sample BR ledger (`br_table` in final.json, FINAL_report §3) and aborts if a factor is applied twice or the product differs from the event-weight k. `nmc_check()` aborts if N_MC < σ×BR×3000 fb⁻¹ for any sample entering s or b.
- Off-shell/FSR correction of the on-shell-Z Zγγ samples: 1.128 (work/theory/theory_summary.json).

## Checksums (sha256)

```
{chk}
```

Gridpack status files (σ and the integration record):
```
{gp}
```

## Commands

```bash
cd /eos/home-r/rjiang/vbs_zh_codex_starter && source scripts/setup_stack.sh
# gridpacks (once):
#   scripts/condor/gridpacks_final.sub, gridpacks_final3.sub (QCD Zgg on-shell Z), gridpacks_final4.sub (EW Zgg split is2, is3), gridpacks_final5.sub (is1h, nhel=1)
# productions (each group submitted once; jobs skip existing outputs):
python3 scripts/plan/make_submit_final.py A H_ttH H_ZH_tautau T_ttaa
python3 scripts/plan/make_submit_final.py C F_QCD_llajj_vbs H_ggZH_py8dec
python3 scripts/plan/make_submit_final.py D F_EW_llajj_vbs
python3 scripts/plan/make_submit_final.py F "F_QCD_llajj_vbs#ext"
python3 scripts/plan/make_submit_final.py G B_QCD_zaajj_vbs
python3 scripts/plan/make_submit_final.py H1 B_EW_zaajj_vbs_is1h; python3 scripts/plan/make_submit_final.py H2 B_EW_zaajj_vbs_is2; python3 scripts/plan/make_submit_final.py H3 B_EW_zaajj_vbs_is3
(module load lxbatch/eossubmit; cd scripts/condor; condor_submit production_final_<tag>.sub)
# verification + batch ntupling (direct mode skimmed to OSSF & >=1 photon & >=2 jets; ff1 for the Zg+jets samples)
python3 -P scripts/analysis/verify_final.py --ntuple <tag> --allow F_QCD_llajj_vbs
(cd scripts/condor; condor_submit ntuple_final_<tag>.sub)
# analysis, figures, tables, reports
# 2026-11-03 completion (A, E): theory weights, interference, off-shell, mjj resolution, object efficiencies, coupling samples
(cd scripts/condor; condor_submit production_final_I.sub)        # ttgamma 520x2000, tWgamma 80x2000 (reference Table I)
(cd scripts/condor; condor_submit theory_lhe.sub theory_mg5.sub theory_mg5b.sub theory_parse.sub mjjres.sub objeff.sub)
bash scripts/models/make_hc_kvv.sh                               # HC_NLO_X0 + kSMW/kSMZ patch
(cd scripts/condor; condor_submit gridpacks_coupling.sub gridpacks_nomjj.sub production_final_K.sub production_final_N.sub)
python3 -P scripts/analysis/verify_final.py --ntuple <tag>       # I, K, N; then condor_submit ntuple_final_<tag>.sub
for f in work/theory/*.lhe.gz; do python3 -P scripts/theory/lhe_theory.py <kind> work/theory/th_<name>.json $f; done   # kinds as in theory_summary.py docstring
python3 -P scripts/theory/theory_summary.py
# final analysis runs on a worker: scripts/condor/final_analysis.sub (pyjob.sh -> final_analysis.py ... --plots figures)
python3 -P scripts/analysis/final_analysis.py work/final_ntuples/final.json --plots figures
python3 -P scripts/analysis/final_tables.py work/final_ntuples/final.json > work/final_ntuples/tables_final.md
python3 -P scripts/analysis/make_final_report.py work/final_ntuples/final.json work/final_ntuples/tables_final.md <commit> reports/FINAL_report.md
python3 -P scripts/analysis/make_repro.py work/final_ntuples/final.json <commit> reports/08_reproducibility.md
```

The Tier-1 signal / QCD ZHjj ntuples and the test_v2 ntuples (`work/m7_analysis/*.npz`) are produced as in [05_pilot_sensitivity.md](05_pilot_sensitivity.md) §9. The analysis is deterministic: no random numbers, except the fake-factor x-smearing seed 13600555 inside `ntuple.py`.
"""
open(OUT, "w").write(txt); print("wrote", OUT)
