# 08 — Reproducibility (FINAL RUN)

- **Date:** 2026-11-03 14:25 UTC
- **Status:** PASS (all inputs pinned; the commands below regenerate every number in FINAL_report.md from the EOS outputs).
- **Git commit of the code:** `b8f2a7d`. Repository git@github.com:AItutorialjrb/agent_VBSZH.git (project-only; the parent repo is untouched).

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
| T_tta | 1362500 | 142300000–142300519 (520 jobs) | 2000 | py8_generic.cmnd | 520 | `ce1332d68badacfe…` |
| T_tWa | 1362600 | 142400000–142400079 (80 jobs) | 2000 | py8_generic.cmnd | 80 | `f8b572ea84018e49…` |
| K_EW_ZHjj_lam_m100 | 1365000 | 142500000–142500024 (25 jobs) | 2000 | py8_ew_zhjj_haa.cmnd | 25 | `d07364648b82af4f…` |
| K_EW_ZHjj_lam_m050 | 1365100 | 142600000–142600024 (25 jobs) | 2000 | py8_ew_zhjj_haa.cmnd | 25 | `37a641e64db16ecb…` |
| K_EW_ZHjj_lam_p000 | 1365200 | 142700000–142700024 (25 jobs) | 2000 | py8_ew_zhjj_haa.cmnd | 25 | `abe7784d7eaaab3c…` |
| K_EW_ZHjj_lam_p050 | 1365300 | 142800000–142800024 (25 jobs) | 2000 | py8_ew_zhjj_haa.cmnd | 25 | `8b342cf5ae65ce61…` |
| K_EW_ZHjj_lam_p100 | 1365400 | 142900000–142900024 (25 jobs) | 2000 | py8_ew_zhjj_haa.cmnd | 25 | `e2720694df810254…` |
| K_EW_ZHjj_lam_p150 | 1365500 | 143000000–143000024 (25 jobs) | 2000 | py8_ew_zhjj_haa.cmnd | 25 | `1ecaca0debf3aee0…` |
| K_EW_ZHjj_cpo_p2 | 1365600 | 143100000–143100024 (25 jobs) | 2000 | py8_ew_zhjj_haa.cmnd | 25 | `b8365412791584b5…` |
| K_EW_ZHjj_cpo_m2 | 1365700 | 143200000–143200024 (25 jobs) | 2000 | py8_ew_zhjj_haa.cmnd | 24 | `6b59bf9817b310ce…` |
| F_QCD_llajj_nomjj | 1365800 | 143300000–143300099 (100 jobs) | 2000 | py8_generic.cmnd | 100 | `135a2182f848ad9d…` |
| B_QCD_zaajj_nomjj | 1365900 | 143400000–143400049 (50 jobs) | 2000 | py8_generic.cmnd | 50 | `646ce330b59d1668…` |

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
afcd6260690a90e23098c9cea5e11f623ba63d2d4da8daa84504b4a23432d37b  cards/production_final/B_EW_llaajj_vbs.mg5
33099476a2b7ccd78f981a1401a6ee38427f460f9019327c59569964ab2a8e54  cards/production_final/B_EW_zaajj_vbs.mg5
a93c5f479a3be57c2f95c555a508878314ff0256775a58c3185c62eee06804b3  cards/production_final/B_EW_zaajj_vbs_is1.mg5
8d95a49897ec49114e7c0f50a8b0162bf13ecb5c116ca285de3eee5761d6dce7  cards/production_final/B_EW_zaajj_vbs_is1h.mg5
c0cbaa7b0e40c5d7479c7aa21c475b94184ce4437d9a0865384eb5a25210f0e4  cards/production_final/B_EW_zaajj_vbs_is2.mg5
94d48cbb1e8d8a52d9ff77f22ce6dec0cde02412d98164605c7626f28509930a  cards/production_final/B_EW_zaajj_vbs_is3.mg5
7f72cd46449f33e1dbfdcdcc862b72afbe0ad7d3ad7827d2876beedaca203690  cards/production_final/B_EW_zaajj_vbs_is3h.mg5
b306d666b259a4d78cc756bb023906728ac0ed0484d7b2b3fa6259ae52bd611c  cards/production_final/B_QCD_llaajj_vbs.mg5
7b47a98889578f2d0edecb896484f0dc0a29a00191571bf612ab0fc57b637d9b  cards/production_final/B_QCD_zaajj_nomjj.mg5
6c3ed23b8fb3fdca0bbe179db3af82833a70a5fb85c3527b707c278974b8a162  cards/production_final/B_QCD_zaajj_vbs.mg5
3951b7ee4c73492832d229a2f94327136fd838fe0f499ede99babe583dd57cc5  cards/production_final/F_EW_llajj_vbs.mg5
95fe33a21fcf5eabdd8f0e7ff9c3d2350f4852427d88384e9635d101d7447b0e  cards/production_final/F_QCD_llajj_nomjj.mg5
33a5ea6332f29a01113b633c5b046e3ccc4d329d5bf103a3d86309f6ca6148f0  cards/production_final/F_QCD_llajj_vbs.mg5
3ab6b167880bac1370f326cb72545fab08de5514545d0ed0d969c6f4f5ea4473  cards/production_final/H_ggZH_py8dec.mg5
1c8eee0de895e2d1b80f9048280666305e899e94609d3bf7c9e0ddf615d61ead  cards/theory/E_zaajj_nodec_is1.mg5
c7fc07d1bc83cc84cbf0fe0a4e4bab0c2e51626b30ee8f1c73715dad6c62d941  cards/theory/E_zaajj_nodec_is2.mg5
6743e27ad26850115dba441d9c60b75550aeff9dd3b7e3d124047b2f07f79414  cards/theory/E_zaajj_nodec_is3.mg5
be3ece702f66645ca45cd5f3d8b454728f9fe683f469603c635f69fd1cba90e0  cards/theory/I_zaajj_nodec_is1.mg5
d17a3a66599813ea901569515b5b06ed5d42957d25c770a4d479d2ccdf8430ec  cards/theory/I_zaajj_nodec_is2.mg5
3a1e3c318738e808b202e0fd95aa144df927c794f9ae681bc555f65489d3c55e  cards/theory/I_zaajj_nodec_is3.mg5
7e838413091aa57042b92b383e141d6e4060b878c9ec4716785e0c45a0ac224a  cards/theory/I_zaajj_vbs_is1.mg5
dfaaa170ed45126ebd8005bfdf220912292c6321dd43948f87b60d2ced220ac1  cards/theory/I_zaajj_vbs_is2.mg5
6ace9f68c9d1bc24ecb0b3702356977622d843ed10c1593d2aaf886d99034b67  cards/theory/I_zaajj_vbs_is3.mg5
3ebb06398925bd1ac10458839625fcfd0ecf76105fef576c8c769b5a11c98528  cards/theory/Q_llaa0j.mg5
7dedf29c632e9e22ad41f85277c35c7fcba993a00c7ef7696f44fe9488ffab63  cards/theory/Q_zaa0j.mg5
35aeb1ca59449c28636f2eb478d8e59d66045ebfa023c9d69b3b844b54eff623  cards/coupling/K_EW_ZHjj_cpo_m2.mg5
67c1e5e8f4f5abb0b06eaeeb87641cb64f77b2cd3a0e52dc93b994f3f7db7b3a  cards/coupling/K_EW_ZHjj_cpo_p2.mg5
17a40abfff48e4dd304e4ef767193fa6f20ec42955de13c1912b796541eab098  cards/coupling/K_EW_ZHjj_lam_m050.mg5
4f4169ad996bae4cd4b77bdab4d552aed8b90bf838b07ccdbbffa036ea0cd03e  cards/coupling/K_EW_ZHjj_lam_m100.mg5
5555b9527507429a6a30b06299a34ec06e93b11424408139c7fb5dc4259bcba7  cards/coupling/K_EW_ZHjj_lam_p000.mg5
3f8b6ba84b58dff5e341b909a38fbc55ecff3faa7a6a8618f670f99b4b2e53bd  cards/coupling/K_EW_ZHjj_lam_p050.mg5
ce7c8a13e74217db12b5745824392ad75deff0d4a3f9185c21aeaf964321330d  cards/coupling/K_EW_ZHjj_lam_p100.mg5
077eadf6930132cfca3bbec7ea5b1aee2dc9a2dd32be88973ae90163b2ff830c  cards/coupling/K_EW_ZHjj_lam_p150.mg5
c2abbfb11488dbfefa4530a6362b6fd295e1d2f5a249333e666c04fa87a0c7a5  cards/phase03_smoke/py8_ew_zhjj_haa.cmnd
619a84f38c3c1b8d68b2e6885fad84b9dd674d338c83c8a8f0e2bf976e03d794  cards/phase03_smoke/py8_generic.cmnd
c7f739d30accf5c726e5eb15b76df4772e12b10180e25685471894a22cf27424  cards/phase03_smoke/py8_generic_dipole.cmnd
fa2dae249ff1c0a0134c4efea5ba54fd09e1151bfc6f423b5767719e9ddbe367  cards/phase03_smoke/py8_ggzh_zll_haa.cmnd
af58bfc04f9d968b47ab8a170763c32d0f5c353a1cb029e1a04f3c04b2e556f5  cards/phase03_smoke/py8_mlm_zh_haa.cmnd
92e7f74e0a224189dc8994727a52d063d79a08356f282aaa0868fe1158ffe760  cards/phase03_smoke/py8_qcd_zhjj_haa.cmnd
016d842d1f2651ab46480ccae5bca77331f284ddaaf817225577c4a77740e797  cards/phase03_smoke/py8_common_CP5.cmnd
9309a6ba2e386b6b8dd1c4b9608a8e27c0b2d9ba9013f590c56f24c79e47c7e9  cards/phase04_candidates/delphes_card_CMS_slim_v1.tcl
0710047c82de39d86ea118ff0305aea1f8150377656e1ec7c94eb0bbcf8efedc  scripts/condor/run_job.sh
87d6ddf932779ac33d9843ce3beb8bd447a5bc2be5a6e729f028fef4da873454  scripts/condor/make_gridpack.sh
31362d2a1f4c92e179a582d60a54c8d6c4d2ae611787c38fee526d0e9c91b951  scripts/condor/lhe_only.sh
736bc30967e5dff831ec77e73933f963765deb8cf59d116c1fbc82d65419de33  scripts/condor/mg5_run.sh
f9e0dafba6afe36eab93ff12c1447bd04590c614457f6200f406ad57de063616  scripts/condor/pyjob.sh
4ae19b9d99ad00703be1e05d064c8723354015d19f15c91dd4308510279cb25a  scripts/theory/lhe_theory.py
1dbaaf25fb4e84e8757545032e7968ebbbe909b7e2d9528e834bbbe6325395c8  scripts/theory/theory_summary.py
55e5500adc6dcb785899294487da5cfea5547b55056ed6bc103ffe413d360643  scripts/models/make_hc_kvv.sh
c290ad525cbe5fbbafba14e7701b331bc1b5fce3fbbee7ab3061d6051b4d95ee  scripts/metrics/extract_prompts.py
55c351187382640d52ea0c669011dafa11db078a45bf7c78f8d0c251ac7df4f6  scripts/metrics/make_ledger.py
558470985f741ba54ca26818badde9c2cce3c869d3f5e4ced35b93d05fa0c2ab  scripts/metrics/parse_usage.py
7e260a66be3e58b18b7a0a0f87775a99a9e9497d61012bab3f890ab622052f41  software/install/HC_NLO_X0_kVV.tgz
b91d8788ed66a12a3eaf9e1f8771f98b789b4b3fc8b10eeb32c9c04f057ae1bd  software/models_dl/HC_NLO_X0_UFO.zip
d818079e8391ab3ab2054bd1c2593c60400ce17ce36216e0b0830d0910bd077b  work/theory/theory_summary.json
85a904327200169cd292a8425bf771c4a67e92b1bab0fae8fbd8f3b70eef7abf  scripts/setup_stack.sh
88741f21624adfe00f60d936e646cb21ae5dc9e1a6383fc119092ee658f580fb  scripts/run_py8_delphes.sh
685f87d91ada2b412cbe79f0cf46d97e29a0ca6314b29487cb176d1278fffeaa  scripts/slim_gentruth.py
f9c3fc48d65b25978e320d838d1f99615c9d60cd00b0570a7bf14568e8d98736  scripts/analysis/coupling_section.py
a8cff114c7c7f09973744d4ecff0506a1766e445d9c78d96dc445ca1d2679f27  scripts/analysis/final_analysis.py
ca607ed65081d071a240e2f4548ff57d602434f810f535ceaeacb5a12a8be56f  scripts/analysis/final_tables.py
df1d662dda8e569ac84d748712774f0fba20300111486f556b24381282b95a5c  scripts/analysis/make_final_report.py
156a915f508c7bb10f0fdb1fbcc36e6aedad46d1b6fefd2984e645a31dbba396  scripts/analysis/make_repro.py
6d941a3dd2cf5394789c87ee20e2abb104fe9cc26f7e0cff7ca5e85e1f8e44eb  scripts/analysis/mjj_resolution.py
b01d808db1c1ed4f1d90ea0338239a3d9993c88e75e2385dd237b4e91bf63784  scripts/analysis/ntuple.py
28d119cbd1193cb269b4b145bb979b3fd77ebed814ce4cfab5ee6df5895e78a4  scripts/analysis/object_eff.py
18858ca1aa0284c3d4abb6b89f19cdcdabfcc31fd181372733a6963d5ecd8c67  scripts/analysis/override_test_v2.py
abd5c52d3f5115fd66e41ebec7467c699f327a22c328f7749ffbc1f2e8253022  scripts/analysis/sensitivity.py
0085b62307ddca6f6661a78a9825803945456643d29354b4c5c92678b8483381  scripts/analysis/skim_npz.py
0f8e4f1615d001e493d8dd399496146cde93b6d4d3d4e54c8bb53667e2e888c5  scripts/analysis/tables05.py
8cbb9cc95238c1ab9863703bca0adaaf64e899f4b002a5e24f91dc8ca167d667  scripts/analysis/tta_xcheck.py
d23890a34cf619bf7822ac0e2c432e506af90d6ab6402342ecf241a1a0486b25  scripts/analysis/verify_final.py
b657f72cd4ae2adb8a43f455e64ef862f7c3ef035cd13cf182ba0430e2c57e56  scripts/analysis/ntuple_job.sh
e18e6e508f6e3c67b70ecad39a98628cc42c3c894c767882f370abad7283f511  scripts/plan/make_submit_final.py
a9876b6101f861a0071ab164762623a7c1139282fc24dfcce2326604c0543cc8  work/final_ntuples/final.json
```

Gridpack status files (σ and the integration record):
```
3a152591e450e58f38a0a4b5daeb3e07181b458059c148893d503f554ddf1ce9  production/gridpacks/B_EW_zaajj_vbs_is1h_status.txt
67f671b713b2ffb3a8d6f1435de8c636d8a4e46d60b5ae8904c130ce97f4ee4d  production/gridpacks/B_EW_zaajj_vbs_is2_status.txt
0e6b68e21f93dca2c261f42b9a1589f6cc4ac59268f2813f879c4b715a876211  production/gridpacks/B_EW_zaajj_vbs_is3_status.txt
9ca0cfd1419b55858dd524cf13a4a0530786249e5fc6dceeb3d31a71c6144eae  production/gridpacks/B_QCD_llaa_0j_status.txt
c6acd12736161cb3b766a1c42b37a74502dceb6cbd6c8db87563184ee402904b  production/gridpacks/B_QCD_llaa_1j_status.txt
6560e668fbb5c84bb11fe8a7c6d381081ce3d1c7783c47cff6bff6257b9efa5d  production/gridpacks/B_QCD_zaajj_nomjj_status.txt
37e0810ed9df48244f4d5e8718c82bbd2918297e9643a51808459fdcf78b6aa9  production/gridpacks/B_QCD_zaajj_vbs_status.txt
49cb3432704f98079e02d2212c73f8147999385dc691828252865caf41031a31  production/gridpacks/F_EW_llajj_status.txt
2e6a015a9f46cc712cc90630eb865b3ce749338e251bb1ebb5502e418f355831  production/gridpacks/F_EW_llajj_vbs_status.txt
00be14d475e7af2d79dec1f8f207a73206924302affd4b9f9edc80ae1f27ab05  production/gridpacks/F_QCD_lla_0j_check_status.txt
baa13b01b1d23276247d0aa3e7f9aef9242bf6d82ccdeb3138fc7e13b96c8d9d  production/gridpacks/F_QCD_llajj_nomjj_status.txt
e98b112004a7a24a52b0b177f5c30d5a93f50252b220c3d89eb33af354a64ac5  production/gridpacks/F_QCD_llajj_vbs_status.txt
16c637006a109da786eb4811b6ecee6827523d5361b74edf9b7fd2a83a3f65e5  production/gridpacks/F_Zjets_01j_check_status.txt
12411ad27cd52df448d70c69662a05185fee0c48a411dba99934e8e61b193005  production/gridpacks/H_QCD_ZH_mlm_status.txt
18000eb7cad41582eb6cf2eba569fa99f0f49b1e5f92bbdeefd7fdf083deae64  production/gridpacks/H_ZH_tautau_status.txt
aaf22f8bc2c9994923aa355f15b3bbbc91ff8de9682dec87437fec028e8cbe2c  production/gridpacks/H_ggZH_py8dec_status.txt
023da880013ffe47ab4bebf3c7546e81721fb254bc775d5cb3caeb8492cdb9aa  production/gridpacks/H_ggZH_status.txt
2cc1a15a44c06c3b3c9d926bca6f6ff5c3e3caf5cefb964fbba40a6df929fdda  production/gridpacks/H_tHW_status.txt
1b4ea7e1b445fbc1d0e4a368e961903686c1e9f381e9580529504e82d9db71af  production/gridpacks/H_ttH_status.txt
107b98be9410e07d3f831badd9d325bafdbd8a8e4f36ff81e4eda8f65d8b64a9  production/gridpacks/I_ZHjj_status.txt
e7c2f2d4d49aa9ad21ac550cab3cbdec0e600e3e9c49ac018fc42036780330d2  production/gridpacks/K_EW_ZHjj_cpo_m2_status.txt
12a11814880a5bb31f8cc8b7653d4849e3f580b1f15a78069a91420f5f1bc659  production/gridpacks/K_EW_ZHjj_cpo_p2_status.txt
ab156150b339d7b6a020ab57b720349cb7682c921c579bbac31f54fadc4a07b5  production/gridpacks/K_EW_ZHjj_lam_m050_status.txt
35fc2a365f61f65e81a8c9c3681031bd832b5068e70e06960394af6907b2d6c1  production/gridpacks/K_EW_ZHjj_lam_m100_status.txt
f25f08cf8198764070f91fbe1b99eb205041f1beb78a19c274831e21578e1ee3  production/gridpacks/K_EW_ZHjj_lam_p000_status.txt
dd1b311d491ede68b6024881521e6ba8fa910d129e4fc567897800449fee75df  production/gridpacks/K_EW_ZHjj_lam_p050_status.txt
e42157a4f4a5ea76ce599234726b79e452fb2b88e4f625fa0c63159c6090472a  production/gridpacks/K_EW_ZHjj_lam_p100_status.txt
314e28139ab66dd1082754cee7b3cba817a0ba4e0a28c09c3b26055a06aa2a13  production/gridpacks/K_EW_ZHjj_lam_p150_status.txt
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
