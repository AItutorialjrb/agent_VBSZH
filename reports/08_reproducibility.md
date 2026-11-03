# 08 — Reproducibility (FINAL RUN)

- **Date:** 2026-11-03 02:21 UTC
- **Status:** PASS (all inputs pinned; the commands below regenerate every number in FINAL_report.md from the EOS outputs).
- **Git commit of the code:** `55d4b11`. Repository git@github.com:AItutorialjrb/agent_VBSZH.git (project-only; the parent repo is untouched).

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

## Seeds and samples (FINAL RUN productions)

- The MG5 gridpack seed is the `gseed` in the gridpack file name.
- The per-job MG5 seed is `seed`; the Pythia seed is seed + 100000000.
- Earlier samples are documented in 04/05: Tier-1 seeds 13611000–099 (EW) and 13621000–049 (QCD); test_v2 seeds are base + 99999.

| sample | gridpack seed | job seeds | events/job | Pythia cmnd | verified jobs | gridpack sha256 |
|---|---|---|---|---|---|---|
| H_ttH | 1360500 | 141000000–141000019 (20 jobs) | 2000 | py8_qcd_zhjj_haa.cmnd | 20 | `7f6ebebb3a930873…` |
| H_ZH_tautau | 1360700 | 141100000–141100003 (4 jobs) | 4000 | py8_mlm_zh_haa.cmnd | 4 | `f146feadf51f79e8…` |
| T_ttaa | 1362400 | 141200000–141200009 (10 jobs) | 2000 | py8_generic.cmnd | 10 | `fb69d03574a4d8d1…` |
| F_QCD_llajj_vbs | 1363000 | 140000000–141601999 (3000 jobs) | 2000 | py8_generic.cmnd | 2995 | `399df09090dd696e…` |
| H_ggZH_py8dec | 1363200 | 141300000–141300009 (10 jobs) | 2000 | py8_ggzh_zll_haa.cmnd | 10 | `265f9d6af4462e08…` |
| F_EW_llajj_vbs | 1363100 | 140100000–140100249 (250 jobs) | 2000 | py8_generic_dipole.cmnd | 250 | `b6836a2a24284195…` |
| B_QCD_zaajj_vbs | 1363500 | 141700000–141700049 (50 jobs) | 2000 | py8_generic.cmnd | 50 | `4fd73edb86b3ec46…` |
| B_EW_zaajj_vbs_is1h | 1364000 | 142100000–142100009 (10 jobs) | 2000 | py8_generic_dipole.cmnd | 10 | `99c36c4ca8bcd4c4…` |
| B_EW_zaajj_vbs_is2 | 1363800 | 141900000–141900009 (10 jobs) | 2000 | py8_generic_dipole.cmnd | 10 | `cbe47d95e00b1386…` |
| B_EW_zaajj_vbs_is3 | 1363900 | 142000000–142000009 (10 jobs) | 2000 | py8_generic_dipole.cmnd | 10 | `ce5073ac48b2e1a9…` |

Dropped segments (no output, not resubmitted): F_QCD_llajj_vbs 140000354, 140000409 (deterministic Delphes segfault), 141600295, 141600415, 141600900 (lost after the LHE stage).

## Checksums (sha256)

```
afcd6260690a90e23098c9cea5e11f623ba63d2d4da8daa84504b4a23432d37b  cards/production_final/B_EW_llaajj_vbs.mg5
33099476a2b7ccd78f981a1401a6ee38427f460f9019327c59569964ab2a8e54  cards/production_final/B_EW_zaajj_vbs.mg5
a93c5f479a3be57c2f95c555a508878314ff0256775a58c3185c62eee06804b3  cards/production_final/B_EW_zaajj_vbs_is1.mg5
8d95a49897ec49114e7c0f50a8b0162bf13ecb5c116ca285de3eee5761d6dce7  cards/production_final/B_EW_zaajj_vbs_is1h.mg5
c0cbaa7b0e40c5d7479c7aa21c475b94184ce4437d9a0865384eb5a25210f0e4  cards/production_final/B_EW_zaajj_vbs_is2.mg5
94d48cbb1e8d8a52d9ff77f22ce6dec0cde02412d98164605c7626f28509930a  cards/production_final/B_EW_zaajj_vbs_is3.mg5
7f72cd46449f33e1dbfdcdcc862b72afbe0ad7d3ad7827d2876beedaca203690  cards/production_final/B_EW_zaajj_vbs_is3h.mg5
b306d666b259a4d78cc756bb023906728ac0ed0484d7b2b3fa6259ae52bd611c  cards/production_final/B_QCD_llaajj_vbs.mg5
6c3ed23b8fb3fdca0bbe179db3af82833a70a5fb85c3527b707c278974b8a162  cards/production_final/B_QCD_zaajj_vbs.mg5
3951b7ee4c73492832d229a2f94327136fd838fe0f499ede99babe583dd57cc5  cards/production_final/F_EW_llajj_vbs.mg5
33a5ea6332f29a01113b633c5b046e3ccc4d329d5bf103a3d86309f6ca6148f0  cards/production_final/F_QCD_llajj_vbs.mg5
3ab6b167880bac1370f326cb72545fab08de5514545d0ed0d969c6f4f5ea4473  cards/production_final/H_ggZH_py8dec.mg5
619a84f38c3c1b8d68b2e6885fad84b9dd674d338c83c8a8f0e2bf976e03d794  cards/phase03_smoke/py8_generic.cmnd
c7f739d30accf5c726e5eb15b76df4772e12b10180e25685471894a22cf27424  cards/phase03_smoke/py8_generic_dipole.cmnd
fa2dae249ff1c0a0134c4efea5ba54fd09e1151bfc6f423b5767719e9ddbe367  cards/phase03_smoke/py8_ggzh_zll_haa.cmnd
af58bfc04f9d968b47ab8a170763c32d0f5c353a1cb029e1a04f3c04b2e556f5  cards/phase03_smoke/py8_mlm_zh_haa.cmnd
92e7f74e0a224189dc8994727a52d063d79a08356f282aaa0868fe1158ffe760  cards/phase03_smoke/py8_qcd_zhjj_haa.cmnd
016d842d1f2651ab46480ccae5bca77331f284ddaaf817225577c4a77740e797  cards/phase03_smoke/py8_common_CP5.cmnd
9309a6ba2e386b6b8dd1c4b9608a8e27c0b2d9ba9013f590c56f24c79e47c7e9  cards/phase04_candidates/delphes_card_CMS_slim_v1.tcl
0710047c82de39d86ea118ff0305aea1f8150377656e1ec7c94eb0bbcf8efedc  scripts/condor/run_job.sh
febb819f363ac52f014e98c38c586b370ce682eef5fd60361a78ee983d59f77a  scripts/condor/make_gridpack.sh
85a904327200169cd292a8425bf771c4a67e92b1bab0fae8fbd8f3b70eef7abf  scripts/setup_stack.sh
88741f21624adfe00f60d936e646cb21ae5dc9e1a6383fc119092ee658f580fb  scripts/run_py8_delphes.sh
685f87d91ada2b412cbe79f0cf46d97e29a0ca6314b29487cb176d1278fffeaa  scripts/slim_gentruth.py
f793bfc7d1f7c024d21e3d5d0c88930549a27d0749bab2770a2d5be00e10007a  scripts/analysis/final_analysis.py
cab379709d065124190397870b788e573b29c763cfb7b484ac9f6c3c6aaa7090  scripts/analysis/final_tables.py
48f263b43932e8ef94323ddf2a8c396ab18ac6c3c65b0efa28b1be076e94188f  scripts/analysis/make_final_report.py
31ba90373b0af33abc65a7644449d4211eaab34f0622724dabf77bf276976cd6  scripts/analysis/make_repro.py
b01d808db1c1ed4f1d90ea0338239a3d9993c88e75e2385dd237b4e91bf63784  scripts/analysis/ntuple.py
18858ca1aa0284c3d4abb6b89f19cdcdabfcc31fd181372733a6963d5ecd8c67  scripts/analysis/override_test_v2.py
abd5c52d3f5115fd66e41ebec7467c699f327a22c328f7749ffbc1f2e8253022  scripts/analysis/sensitivity.py
0085b62307ddca6f6661a78a9825803945456643d29354b4c5c92678b8483381  scripts/analysis/skim_npz.py
0f8e4f1615d001e493d8dd399496146cde93b6d4d3d4e54c8bb53667e2e888c5  scripts/analysis/tables05.py
d23890a34cf619bf7822ac0e2c432e506af90d6ab6402342ecf241a1a0486b25  scripts/analysis/verify_final.py
b657f72cd4ae2adb8a43f455e64ef862f7c3ef035cd13cf182ba0430e2c57e56  scripts/analysis/ntuple_job.sh
5ec95eb2ac6d10d05f1bb1ea151725e3d881f319160bd21f0975863209235fc7  scripts/plan/make_submit_final.py
3be5d55d9ea350d63a2485fbf9888d5a1b3e34d371e8c00dc0a294c52a7a4bef  work/final_ntuples/final.json
```

Gridpack status files (σ and the integration record):
```
3a152591e450e58f38a0a4b5daeb3e07181b458059c148893d503f554ddf1ce9  production/gridpacks/B_EW_zaajj_vbs_is1h_status.txt
67f671b713b2ffb3a8d6f1435de8c636d8a4e46d60b5ae8904c130ce97f4ee4d  production/gridpacks/B_EW_zaajj_vbs_is2_status.txt
0e6b68e21f93dca2c261f42b9a1589f6cc4ac59268f2813f879c4b715a876211  production/gridpacks/B_EW_zaajj_vbs_is3_status.txt
9ca0cfd1419b55858dd524cf13a4a0530786249e5fc6dceeb3d31a71c6144eae  production/gridpacks/B_QCD_llaa_0j_status.txt
c6acd12736161cb3b766a1c42b37a74502dceb6cbd6c8db87563184ee402904b  production/gridpacks/B_QCD_llaa_1j_status.txt
37e0810ed9df48244f4d5e8718c82bbd2918297e9643a51808459fdcf78b6aa9  production/gridpacks/B_QCD_zaajj_vbs_status.txt
49cb3432704f98079e02d2212c73f8147999385dc691828252865caf41031a31  production/gridpacks/F_EW_llajj_status.txt
2e6a015a9f46cc712cc90630eb865b3ce749338e251bb1ebb5502e418f355831  production/gridpacks/F_EW_llajj_vbs_status.txt
00be14d475e7af2d79dec1f8f207a73206924302affd4b9f9edc80ae1f27ab05  production/gridpacks/F_QCD_lla_0j_check_status.txt
e98b112004a7a24a52b0b177f5c30d5a93f50252b220c3d89eb33af354a64ac5  production/gridpacks/F_QCD_llajj_vbs_status.txt
16c637006a109da786eb4811b6ecee6827523d5361b74edf9b7fd2a83a3f65e5  production/gridpacks/F_Zjets_01j_check_status.txt
12411ad27cd52df448d70c69662a05185fee0c48a411dba99934e8e61b193005  production/gridpacks/H_QCD_ZH_mlm_status.txt
18000eb7cad41582eb6cf2eba569fa99f0f49b1e5f92bbdeefd7fdf083deae64  production/gridpacks/H_ZH_tautau_status.txt
aaf22f8bc2c9994923aa355f15b3bbbc91ff8de9682dec87437fec028e8cbe2c  production/gridpacks/H_ggZH_py8dec_status.txt
023da880013ffe47ab4bebf3c7546e81721fb254bc775d5cb3caeb8492cdb9aa  production/gridpacks/H_ggZH_status.txt
2cc1a15a44c06c3b3c9d926bca6f6ff5c3e3caf5cefb964fbba40a6df929fdda  production/gridpacks/H_tHW_status.txt
1b4ea7e1b445fbc1d0e4a368e961903686c1e9f381e9580529504e82d9db71af  production/gridpacks/H_ttH_status.txt
107b98be9410e07d3f831badd9d325bafdbd8a8e4f36ff81e4eda8f65d8b64a9  production/gridpacks/I_ZHjj_status.txt
4e6a4da116f08018084cbbdcf4d7dc54f03b1d3571a01d0bcebb96fb90e39c86  production/gridpacks/S_EW_ZHjj_offshell_status.txt
81be67aaa92492b3fb2c4d32fc00824ea53f241c6b339d9d2199eff891e49140  production/gridpacks/T_tWa_status.txt
10a21df5fae1eec2e5fe9bef4827f2b13d7ada33e42123e61c29f566034a9acd  production/gridpacks/T_tt_status.txt
35b2cc86556f4f08c44edcc8fab238267880d568c4c54c26ebf8c926f0199064  production/gridpacks/T_tta_status.txt
6f83e02d3f75522ecb814f428c24763a687d7388e32415059166af6466e8257c  production/gridpacks/T_ttaa_status.txt
3d0bdd3664054bb9031e9afadea9c2ddf4b61643ad7266e0abc0fb7654f62fa8  production/gridpacks/V_WZa_status.txt
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
python3 -P scripts/analysis/final_analysis.py work/final_ntuples/final.json --plots figures
python3 -P scripts/analysis/final_tables.py work/final_ntuples/final.json > work/final_ntuples/tables_final.md
python3 -P scripts/analysis/make_final_report.py work/final_ntuples/final.json work/final_ntuples/tables_final.md <commit> reports/FINAL_report.md
python3 -P scripts/analysis/make_repro.py work/final_ntuples/final.json <commit> reports/08_reproducibility.md
```

The Tier-1 signal / QCD ZHjj ntuples and the test_v2 ntuples (`work/m7_analysis/*.npz`) are produced as in [05_pilot_sensitivity.md](05_pilot_sensitivity.md) §9. The analysis is deterministic: no random numbers, except the fake-factor x-smearing seed 13600555 inside `ntuple.py`.
