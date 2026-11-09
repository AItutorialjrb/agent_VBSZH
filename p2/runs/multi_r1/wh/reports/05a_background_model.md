# 05a Background model (executor-wh FINAL, block 1)

Date UTC: 2026-11-09 00:39. Status: **PASS for verification request** (selection NOT started; waiting for verifier/review). Git commit: see orchestrator commit. **Version v2 (reissue after review reviews/wh_05a_background.md, HOLD).**

## Changelog v1 -> v2 (review HOLD, all items)
1. (sev-1) Frozen multi-directory ZH rows: directory label now derived from the file-name prefix (skim metadata held bare file names), N and sum w per directory. Check below: sum w/N equals SAMPLES sigma for every row (ZH_Zajj_eFake 0.08039 vs 0.08051 pb). PEAK eFake before C 2.41 (v1: 1.14), Zaajj EW 0.113 (v1: 0.040).
2. (sev-1) C factors applied in VBS/PEAK (Zajj QCD 1.866 with range [1, 2.732] = the 87 % C systematic; Zaajj EW 0.958 +- 0.061); PRE: C = 1 (lower limit), bound [min(1,C), max(1,C)]. The ZH_Zajj nomjj top-up is NOT generated (human question c).
3. (sev-1) D35: light-misID bounds are x0.3 / x3 of the nominal (D36 envelope; switchable `--nonprompt-lo/--nonprompt-hi`); electron-only and the loose 2e-3 are no longer bounds. 2e-4 / 2e-3 per flavour are reported as labelled robustness variants and the x100 scan is labelled beyond D36. Deviation to log in SPEC section 7 (orchestrator): v1 used low = electron only, high = loose 2e-3 per flavour (contradicts D35); the Q_aajjj D29 trigger (Q_aajj 28-31 % > 10 % of SR background) was evaluated at f_l = 2e-3 (D28 loose); at the D35 nominal the trigger would not fire (Q_aajj fraction <1 %); Q_aajjj remains the nominal row (already produced, harmless).
4. (sev-2) one-sided non-closure systematic x0.4 on the one-fake low bound (measured direct/FF ratio 0.39 PRE, 0.41 VBS, see sec. 2). 5. D39 floor +-20 % is a declared nuisance and is in the bounds. 6. direct count labelled a LOWER LIMIT of the true upper variation (3-jet row only; artefacts lie outside jets, a 2j row would add); converted-jet generator-cut safety (04 sec. 19(2), scripts/convjet_cut_safety.py): weighted fraction of conversions with GenJet pT < 20 GeV 1.4 %, < 25 GeV 3.7 %, < 30 GeV 8.1 % (safe, < 5 % at the generator cut). 7. factorised heavy-flavour variant added (sec. 3), UL kept. 8. see item 3 (D29 trigger at 2e-3). 9. nuisance list below. 10. zero-support ULs in the direct variation are reported (column ULdir), r_tau on Z rows justified (sec. 5), commit placeholder.

## Pre-declared nuisance list for the statistics stage (fixed here, before any selection)
(1) MC statistics per bin (Barlow-Beeston), (2) tau uplift +-100 % of r_tau (D9), (3) QCD 7-point scale envelope per process class, (4) D29 PS-modelling 100 % on V_WWa/WZa/ZZa and on the missing 2j+PS fake topology, (5) D27 two-fake per-photon scenarios x{0.3,1,3} (yield x{0.09,1,9}), (6) generator-cut C systematic (Zajj QCD [1, 2.732], Zaajj EW +-6.4 %), (7) D39 calibration floor +-20 % on the fake-photon rate (correlated one-/two-fake), (8) one-sided fake-photon non-closure -60 % (one-fake), (9) non-prompt light-misID normalisation x0.3-x3 (D36) with robustness variants 2e-4 / 2e-3, (10) heavy-flavour non-prompt-lepton factorised variant +-100 % with the UL as conservative variant, (11) luminosity and theory (combination stage). D36 scans: fake photons and non-prompt leptons separately, x0.3-x3.

## Goal
Background model for pp -> WHjj (W->l nu, H->gamma gamma) at 13.6 TeV, L = 500 fb^-1, Delphes level: class table with lower/upper bounds for fake photons (D34 a'), non-prompt leptons (D35), e->gamma / lost lepton, irreducible and other Higgs; zero-support rows with Poisson ULs. Not the final selection: the regions below are block-level (PRE/VBS/PEAK, scripts/bgmodel.py `regions`).

## Inputs / versions
wh-prod-v1 (p2/production/wh, SAMPLES.csv, FORMAT.md), frozen ZH rows read-only from production/final, production/v1. Stack LCG_110 (scripts/envrun.sh). Normalisation: events = L*1e3*k*sum(w_pb*f)/N_gen (per directory for frozen ZH rows). Seeds: skim RNG seed = file seed + 777. No new samples, no git.

## Commands (all in wh/scripts, outputs in wh/work/bgmodel)
veto_validation.py (login, 5 k-event test files) -> veto_validation.json; rate_genuine.py via condor (cluster 899742, 484 jobs, schedd bigbird103) -> rate_table.py -> rate_table.json, rate_closure.json; skim.py via condor (899730: 761 jobs, 899824: 741 jobs; all 1502 exit 0, 0 missing outputs); bg_yields.py -> yields.json (log bg_yields.log); this report: make_report_05a.py. Failed attempt: cluster 899728 (argument order bug, removed, its 70 good outputs identical to the rerun).

## 1. Artefact veto (D34, validation on *_full.root)
Truth label = sum of E of the unique particles in Photon.Particles / E_reco >= 0.5 (reviewer's test; 575 lepton-free non-prompt-origin photons pT>10 over 35 test files). GenTruth proxy R = sum pT(GenTruth status-1 photons pT>10, within dR<0.2)/pT_reco; veto: artefact if R<0.5. Result: pT>20: 73 of 73 truth-genuine kept, 0 of 123 truth-artefact leaked; pT 10-15: proxy keeps 1/55 genuine (GenTruth threshold is 10 GeV), so the rate numerator and all photon use is restricted to reco pT>20. Cut variants 0.3 and 0.7 give identical purity (0 leaks) and 80 vs 77 kept (all photons). Only 8/575 photons have E_ref/E in (0.1,0.9) (labels are unambiguous). Fraction artefact at pT>25: 87/158 = 55 %.
Finding: photons matched to a GenJet within dR<0.2 are almost all genuine (artefact numerators in the jet cone are 0-4 per bin, table below): the energy-flow artefacts lie outside jets, so the decontaminated per-jet rate is essentially the earlier lepton-decontaminated rate; the artefact class enters only through the direct count (upper variation).

## 2. Fake photons (D34 option a')
Nominal: fake factor f(jet pT, |eta|) from genuine in-jet photons only (W-class from all 465 F_Wjjjj files, TT-class from 19 T_ttjj_1l files; bins with <5 genuine counts use the pooled rate), x = photon pT/jet pT from the measured genuine histogram, jet consumed, photon pT>20, applied to reco jets pT>25 |eta|<2.5 (dR>0.4 to lepton and the real photon). One-fake rows (F_QCD_Wajjj, F_EW_Wajj, T_tta, T_tWa; n_prompt_photons==1) and two-fake rows (F_Wjjjj, T_ttjj_1l; n_prompt_photons==0, weight f_a*f_b). Energy-flow artefact photons never enter the nominal. Variants: stat up/dn (Clopper-Pearson 68 %), veto cut 0.3/0.7, QCD 7-point scale envelope. UPPER variation: direct Delphes count including artefacts (kind 4). Closure test: direct genuine count (kind 3) vs nominal.
Rate table (genuine in-jet photons), per jet-pT bin [25,35,50,75,100,150,1000] (percent):
- W barrel [0.00376, 0.00456, 0.0058, 0.00672, 0.00742, 0.01232]; endcap [0.00333, 0.0046, 0.00574, 0.00787, 0.0097, 0.01609]; genuine counts [[376.0, 443.0, 553.0, 365.0, 394.0, 544.0], [170.0, 223.0, 267.0, 202.0, 232.0, 262.0]]; artefact counts in jet cone [[4.0, 1.0, 0.0, 0.0, 0.0, 0.0], [4.0, 0.0, 1.0, 0.0, 0.0, 0.0]]; N_jets (barrel) [9990056, 9706128, 9536170, 5430660, 5306781, 4416662]
- TT barrel [0.00539, 0.00614, 0.00548, 0.00396, 0.00341, 0.00764]; endcap [0.00325, 0.00374, 0.00416, 0.00773, 0.00945, 0.01521]; genuine counts [[14.0, 19.0, 21.0, 10.0, 9.0, 15.0], [0.0, 5.0, 6.0, 3.0, 2.0, 9.0]]; artefact counts in jet cone [[1.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 1.0, 0.0]]; N_jets (barrel) [259602, 309427, 383112, 252819, 263851, 196301]
- disjoint even/odd closure of the W rate: {'measure_even_test_odd': {'chi2': 14.89572022461594, 'ndof': 12}, 'measure_odd_test_even': {'chi2': 14.236578042230526, 'ndof': 12}}

**2j F_QCD row (brief 2a): not needed.** The nominal fake consumes a jet; one-fake topologies with two tag jets plus the converted jet need three hard jets, which F_QCD_Wajjj (3 ME jets, regions with >=3 reco jets incl. the converted jet: automatic here) covers; two-fake topologies need four jets (F_Wjjjj, W+4j). The Delphes artefact class, which would have needed the 2j sample, is excluded from the nominal. The remaining missing 2j+PS-jet topology is covered by the pre-declared 100 % PS-modelling uncertainty of D29 (statistics stage, not folded into the bounds below).
**Calibration to CMS (D34, open decision D39 = D-WH-17).** Record verified: CMS-SMP-19-013, JHEP 10 (2021) 174, arXiv:2105.12780, Table 2: misidentified-jet background 918 +- 23 (stat) +- 180 (syst) (e nu gamma gamma), 1441 +- 27 +- 280 (mu nu gamma gamma) of 2052 / 2334 predicted events (45 % / 62 %); Z channels 42 +- 4 +- 9 and 98 +- 5 +- 27; HEPData ins1865855 (DOI 10.17182/hepdata.113759.v1), Fig. 2 gives the pT(gamma gamma) distribution per process. No comparison with this model is possible: the frozen samples contain no inclusive (no-VBS-cut, <=2-jet) W+jets / W gamma+jets sample, the CMS selection is inclusive in jets, and F_Wjjjj / F_QCD_Wajjj are exclusive 4- and 3-parton rows. Default: calibration factor c = 1 (switch `--ccal-photon`, one-fake x c, two-fake x c^2), systematic floor +-20 % (CMS syst/yield 19.6 %), the D36 scan x0.3-x3, and the direct-count upper variation. A human answer (or a new inclusive sample) is a re-run of bg_yields.py with a different c, not a redesign.

## 3. Non-prompt leptons (D35, D40 = D-WH-18)
Heavy-flavour leptons: directly from the Delphes MC (rows with a reco lepton in Q_aajjj / H_VBFH_jj, weight 1, lepton isolation <0.15). Light-hadron misID: each jet pT>25, |eta|<2.4 of the sample's own jets is the lepton with weight f_l, lepton pT = x*pT_jet (x~N(0.85,0.1) truncated [0.5,1]: an uncited assumption), events without a reco lepton, jet consumed. Nominal rows: Q_aajjj (gamma gamma + 3 jets, replaces Q_aajj per D29), H_VBFH_jj; H_ggF_jj missing (gridpack 893012 still running; D38 fallback). Q_aajj is a cross-check, not in the class. f_e = 2e-5 (tight, ATLAS EPJC 72 (2012) 1909, arXiv:1110.3174 sec. 4.4, jet rejection about 5e4, identification only); f_mu = 2e-5 is a PLACEHOLDER equal to the electron value (D40: no citable per-jet muon value found; the CMS per-hadron value 0.1-0.5 % of arXiv:1804.04528 cannot be converted without an invented multiplicity); switches `--f-electron --f-muon --f-high`. Bounds (v2): low = x0.3, nominal = 4e-5 total (e + mu placeholder), high = x3 (D36 envelope, human question a pending). Robustness variants, NOT bounds: 2e-4 and 2e-3 per flavour (D35: 2e-3 is not an upper bound) and the x100 scan (beyond D36). Calibration to a published CMS non-prompt-lepton fraction: none found in a comparable final state (CMS Wgg/Zgg lists only misid jets, misid electrons, others). Heavy flavour: nominal = direct Delphes rows; factorised variant = direct PRE rate x (kind-5 yield region/PRE), +-100 % (about 0.055 in PEAK for Q_aajjj, entering the high bound as 2x); the zero-raw-row UL (0.47 + 0.28) is kept as the conservative variant.

## 4. e->gamma and lost lepton
Direct Delphes MC (V_WWa/WZa/ZZa without ME jets, frozen ZH_Zaajj lost-lepton rows, ZH_Zajj_eFake with the Delphes e->gamma object, photon class cls1 = within dR<0.2 of a prompt generator lepton). The measured Delphes e->gamma rate of FORMAT.md 6b (3.8-15 % for electrons, 0.5-0.7 % for muons) is the rate the direct MC already contains (cross-check in work/postprod/egamma_rate.json); no extra weighting. Generator-cut factors C (vbs rows mmjj>400; measured at the WH reco-SR proxy mjj>500, |deta|>2.5, 04 sec. 15(7)): Zajj QCD part 1.866 (range [1, 2.732] = full difference, the 87 % systematic), Zaajj EW 0.958 +- 0.061, applied in VBS/PEAK; the EW part of ZH_Zajj_eFake gets C = 1 (EW twin loss 2.4 +- 0.3 %). PRE has no mjj cut (the skim superset has mjj>300): C = 1 (lower limit) with bound [min(1,C), max(1,C)]. The Zaajj nomjj row needs none. Bounds: 7-point scale envelope and tau factor; V_* rows additionally carry the D29 100 % PS-modelling uncertainty (statistics stage).

## 5. Tau factor (D9)
r_tau = Y(S_EW_WHjj_taunu)/Y(S_EW_WHjj) per region (about 0.082). W/Z-containing classes: nominal x(1+r_tau), bounds [1, 1+2 r_tau]. S_EW_WHjj_taunu is listed separately as a signal-like feed-down.

## 6. Class tables (events at 500 fb^-1, Delphes level, BR applied once)
Bounds are low/high of the declared variations (bg_yields.py docstring); stat = weighted-MC uncertainty of the nominal; UL0 = sum of 95 % Poisson ULs (2.996 x unit weight x f) of rows with zero raw support. Raw N and N_eff per sample follow.

### PRE (r_tau 0.082; lepton iso<0.15)

| class | nominal | low | high | MC stat | UL0 (nominal rows) | UL direct variation | missing |
|---|---|---|---|---|---|---|---|
| prompt_irreducible | 57.65 | 44.3 | 76.2 | 1.3 | 0 | 0 | - |
| fake_photon_1 | 2.826 | 0.575 | 19.7 | 0.006 | 0 | 0 | - |
| fake_photon_2 | 0.06888 | 0.0277 | 0.171 | 8.8e-05 | 0 | 323 | - |
| nonprompt_lepton | 1.867 | 1.11 | 5.6 | 0.35 | 0.283 | 0 | H_ggF_jj |
| lost_lepton_egamma | 32.34 | 25.4 | 61.5 | 0.6 | 0.0316 | 0 | - |
| other_higgs | 1.568 | 1.33 | 1.88 | 0.04 | 0 | 0 | - |
| tau_feeddown | 0.09721 | 0.0908 | 0.105 | 0.0028 | 0 | 0 | - |
| signal | 1.184 | 1.11 | 1.27 | 0.0095 | 0 | 0 | - |
| xcheck | 1.289 | 0.72 | 3.87 | 0.27 | 0 | 0 | - |

| sample | nominal Y | raw N | N_eff | variants / UL |
|---|---|---|---|---|
| B_QCD_Waajj_nomjj | 38.73 | 1130 | 1130 |  |
| B_EW_Waajj_nomjj | 14.06 | 5111 | 5035 |  |
| T_ttaa_1l | 0.4855 | 86 | 86 |  |
| F_QCD_Wajjj_nomjj | 2.41 | 233698 | 199367 | dn 2.28 up 2.54 R0.7 2.37; direct genuine 0.946 (raw 6, UL 0); direct incl. artefact 8.99 (raw 57, UL 0) |
| F_EW_Wajj_nomjj | 0.09265 | 9225 | 7574 | dn 0.0875 up 0.0978 R0.7 0.0909; direct genuine 0.147 (raw 1, UL 0); direct incl. artefact 0.586 (raw 4, UL 0) |
| T_tta_1l | 0.09445 | 11423 | 10029 | dn 0.0673 up 0.122 R0.7 0.0916; direct genuine 0.156 (raw 1, UL 0); direct incl. artefact 0.468 (raw 3, UL 0) |
| T_tWa_1l | 0.01406 | 13708 | 12103 | dn 0.00994 up 0.0182 R0.7 0.0137; direct genuine 0.0196 (raw 1, UL 0); direct incl. artefact 0.0587 (raw 3, UL 0) |
| F_Wjjjj | 0.05303 | 1234354 | 991862 | dn 0.0476 up 0.0588 R0.7 0.0507; direct genuine 0 (raw 0, UL 31.8); direct incl. artefact 0 (raw 0, UL 31.8) |
| T_ttjj_1l | 0.01062 | 39535 | 30423 | dn 0.00534 up 0.0177 R0.7 0.00995; direct genuine 0 (raw 0, UL 292); direct incl. artefact 0 (raw 0, UL 292) |
| Q_aajjj | 1.861 | 169188 + 5 direct | 168664 | misID nominal 1.07 (low 0.321, high 3.21); heavy-flavour direct 0.792 (UL 0) |
| H_VBFH_jj | 0.005653 | 1498 + 0 direct | 1498 | misID nominal 0.00565 (low 0.0017, high 0.017); heavy-flavour direct 0 (UL 0.283) |
| V_WWa_WH | 0.4674 | 3 | 3 |  |
| V_WZa_WH | 0.2551 | 5 | 5 |  |
| V_ZZa_WH | 0 | 0 | 0 | UL95 0.0316 |
| ZH_Zaajj_QCD_nomjj_lostlep | 0.7989 | 598 | 598 |  |
| ZH_Zaajj_EW_lostlep | 0.9402 | 2944 | 2599 |  |
| ZH_Zajj_eFake | 27.42 | 3835 | 3410 |  |
| H_QCD_WH_mlm | 0.7003 | 440 | 436 |  |
| H_ggZH_wh | 0.03265 | 285 | 285 |  |
| H_ZH_tautau_wh | 0.01784 | 33 | 33 |  |
| H_ttH_1l | 0.2572 | 432 | 432 |  |
| H_ttH_dilep_wh | 0.05049 | 134 | 134 |  |
| H_tHq_lep | 0.2773 | 1622 | 1606 |  |
| H_tHW_1l | 0.02672 | 517 | 517 |  |
| ZH_EW_ZHjj_lostlep | 0.03141 | 4380 | 4300 |  |
| ZH_QCD_ZHjj_lostlep | 0.0547 | 483 | 479 |  |
| S_EW_WHjj_taunu | 0.09721 | 1221 | 1197 |  |
| S_EW_WHjj | 1.184 | 15746 | 15598 |  |
| Q_aajj | 1.289 | 128519 + 3 direct | 128271 | misID nominal 0.814 (low 0.244, high 2.44); heavy-flavour direct 0.476 (UL 0) |

### VBS (r_tau 0.083; lepton iso<0.15)

| class | nominal | low | high | MC stat | UL0 (nominal rows) | UL direct variation | missing |
|---|---|---|---|---|---|---|---|
| prompt_irreducible | 33.68 | 26.2 | 44.1 | 0.9 | 0 | 0 | - |
| fake_photon_1 | 1.381 | 0.28 | 9.68 | 0.0042 | 0 | 0.0587 | - |
| fake_photon_2 | 0.03458 | 0.0138 | 0.0864 | 6.3e-05 | 0 | 323 | - |
| nonprompt_lepton | 0.8031 | 0.463 | 2.49 | 0.22 | 0.283 | 0 | H_ggF_jj |
| lost_lepton_egamma | 29.21 | 16.3 | 49.1 | 0.59 | 0.498 | 0 | - |
| other_higgs | 0.7719 | 0.658 | 0.926 | 0.027 | 0 | 0 | - |
| tau_feeddown | 0.08482 | 0.0788 | 0.0918 | 0.0026 | 0 | 0 | - |
| signal | 1.02 | 0.949 | 1.1 | 0.0088 | 0 | 0 | - |
| xcheck | 0.6597 | 0.42 | 1.74 | 0.22 | 0 | 0 | - |

| sample | nominal Y | raw N | N_eff | variants / UL |
|---|---|---|---|---|
| B_QCD_Waajj_nomjj | 19.23 | 561 | 561 |  |
| B_EW_Waajj_nomjj | 11.66 | 4245 | 4173 |  |
| T_ttaa_1l | 0.2031 | 36 | 36 |  |
| F_QCD_Wajjj_nomjj | 1.165 | 112644 | 95634 | dn 1.1 up 1.23 R0.7 1.14; direct genuine 0.473 (raw 3, UL 0); direct incl. artefact 4.57 (raw 29, UL 0) |
| F_EW_Wajj_nomjj | 0.06118 | 6066 | 4936 | dn 0.0578 up 0.0646 R0.7 0.06; direct genuine 0 (raw 0, UL 0.439); direct incl. artefact 0.146 (raw 1, UL 0) |
| T_tta_1l | 0.04305 | 5161 | 4511 | dn 0.0307 up 0.0554 R0.7 0.0417; direct genuine 0 (raw 0, UL 0.467); direct incl. artefact 0.156 (raw 1, UL 0) |
| T_tWa_1l | 0.005801 | 5621 | 4944 | dn 0.00411 up 0.0075 R0.7 0.00564; direct genuine 0 (raw 0, UL 0.0587); direct incl. artefact 0 (raw 0, UL 0.0587) |
| F_Wjjjj | 0.02654 | 608930 | 485911 | dn 0.0238 up 0.0294 R0.7 0.0254; direct genuine 0 (raw 0, UL 31.8); direct incl. artefact 0 (raw 0, UL 31.8) |
| T_ttjj_1l | 0.005383 | 19867 | 15317 | dn 0.00271 up 0.00897 R0.7 0.00504; direct genuine 0 (raw 0, UL 292); direct incl. artefact 0 (raw 0, UL 292) |
| Q_aajjj | 0.7991 | 76355 + 2 direct | 75999 | misID nominal 0.482 (low 0.145, high 1.45); heavy-flavour direct 0.317 (UL 0) |
| H_VBFH_jj | 0.003951 | 1047 + 0 direct | 1047 | misID nominal 0.00395 (low 0.00119, high 0.0119); heavy-flavour direct 0 (UL 0.283) |
| V_WWa_WH | 0 | 0 | 0 | UL95 0.467 |
| V_WZa_WH | 0.1531 | 3 | 3 |  |
| V_ZZa_WH | 0 | 0 | 0 | UL95 0.0316 |
| ZH_Zaajj_QCD_nomjj_lostlep | 0.3448 | 258 | 258 |  |
| ZH_Zaajj_EW_lostlep | 0.7896 | 2565 | 2269 |  |
| ZH_Zajj_eFake | 25.68 | 2377 | 2329 |  |
| H_QCD_WH_mlm | 0.2974 | 186 | 186 |  |
| H_ggZH_wh | 0.01776 | 155 | 155 |  |
| H_ZH_tautau_wh | 0.005945 | 11 | 11 |  |
| H_ttH_1l | 0.1274 | 214 | 214 |  |
| H_ttH_dilep_wh | 0.02299 | 61 | 61 |  |
| H_tHq_lep | 0.179 | 1050 | 1034 |  |
| H_tHW_1l | 0.01246 | 241 | 241 |  |
| ZH_EW_ZHjj_lostlep | 0.02623 | 3663 | 3587 |  |
| ZH_QCD_ZHjj_lostlep | 0.02343 | 208 | 204 |  |
| S_EW_WHjj_taunu | 0.08482 | 1065 | 1045 |  |
| S_EW_WHjj | 1.02 | 13573 | 13429 |  |
| Q_aajj | 0.6597 | 54104 + 2 direct | 53948 | misID nominal 0.342 (low 0.103, high 1.03); heavy-flavour direct 0.317 (UL 0) |

### PEAK (r_tau 0.083; lepton iso<0.15)

| class | nominal | low | high | MC stat | UL0 (nominal rows) | UL direct variation | missing |
|---|---|---|---|---|---|---|---|
| prompt_irreducible | 5.148 | 4 | 6.72 | 0.35 | 0 | 0 | - |
| fake_photon_1 | 0.185 | 0.0375 | 1.29 | 0.0015 | 0 | 0.965 | - |
| fake_photon_2 | 0.004677 | 0.00186 | 0.0117 | 2.3e-05 | 0 | 323 | - |
| nonprompt_lepton | 0.07871 | 0.0236 | 0.347 | 0.0007 | 0.757 | 0 | H_ggF_jj |
| lost_lepton_egamma | 3.841 | 2.16 | 6.43 | 0.21 | 0.651 | 0 | - |
| other_higgs | 0.7493 | 0.64 | 0.898 | 0.026 | 0 | 0 | - |
| tau_feeddown | 0.08233 | 0.0765 | 0.0891 | 0.0026 | 0 | 0 | - |
| signal | 0.9905 | 0.921 | 1.07 | 0.0087 | 0 | 0 | - |
| xcheck | 0.05306 | 0.0159 | 0.221 | 0.00058 | 0.475 | 0 | - |

| sample | nominal Y | raw N | N_eff | variants / UL |
|---|---|---|---|---|
| B_QCD_Waajj_nomjj | 2.946 | 86 | 86 |  |
| B_EW_Waajj_nomjj | 1.779 | 650 | 634 |  |
| T_ttaa_1l | 0.0282 | 5 | 5 |  |
| F_QCD_Wajjj_nomjj | 0.1558 | 15608 | 13398 | dn 0.148 up 0.164 R0.7 0.153; direct genuine 0 (raw 0, UL 0.473); direct incl. artefact 0.631 (raw 4, UL 0) |
| F_EW_Wajj_nomjj | 0.007998 | 831 | 684 | dn 0.00755 up 0.00844 R0.7 0.00782; direct genuine 0 (raw 0, UL 0.439); direct incl. artefact 0 (raw 0, UL 0.439) |
| T_tta_1l | 0.006129 | 733 | 637 | dn 0.00437 up 0.00789 R0.7 0.00593; direct genuine 0 (raw 0, UL 0.467); direct incl. artefact 0 (raw 0, UL 0.467) |
| T_tWa_1l | 0.0008423 | 831 | 729 | dn 0.000593 up 0.00109 R0.7 0.000816; direct genuine 0 (raw 0, UL 0.0587); direct incl. artefact 0 (raw 0, UL 0.0587) |
| F_Wjjjj | 0.003555 | 85547 | 68966 | dn 0.00319 up 0.00394 R0.7 0.00339; direct genuine 0 (raw 0, UL 31.8); direct incl. artefact 0 (raw 0, UL 31.8) |
| T_ttjj_1l | 0.0007624 | 2876 | 2231 | dn 0.000384 up 0.00127 R0.7 0.000714; direct genuine 0 (raw 0, UL 292); direct incl. artefact 0 (raw 0, UL 292) |
| Q_aajjj | 0.07484 | 11839 + 0 direct | 11803 | misID nominal 0.0748 (low 0.0225, high 0.225); heavy-flavour direct 0 (UL 0.474) |
| H_VBFH_jj | 0.003876 | 1027 + 0 direct | 1027 | misID nominal 0.00388 (low 0.00116, high 0.0116); heavy-flavour direct 0 (UL 0.283) |
| V_WWa_WH | 0 | 0 | 0 | UL95 0.467 |
| V_WZa_WH | 0 | 0 | 0 | UL95 0.153 |
| V_ZZa_WH | 0 | 0 | 0 | UL95 0.0316 |
| ZH_Zaajj_QCD_nomjj_lostlep | 0.04945 | 37 | 37 |  |
| ZH_Zaajj_EW_lostlep | 0.1136 | 376 | 332 |  |
| ZH_Zajj_eFake | 3.383 | 316 | 304 |  |
| H_QCD_WH_mlm | 0.2926 | 183 | 183 |  |
| H_ggZH_wh | 0.01661 | 145 | 145 |  |
| H_ZH_tautau_wh | 0.005945 | 11 | 11 |  |
| H_ttH_1l | 0.1227 | 206 | 206 |  |
| H_ttH_dilep_wh | 0.02186 | 58 | 58 |  |
| H_tHq_lep | 0.1734 | 1017 | 1001 |  |
| H_tHW_1l | 0.0123 | 238 | 238 |  |
| ZH_EW_ZHjj_lostlep | 0.02509 | 3505 | 3429 |  |
| ZH_QCD_ZHjj_lostlep | 0.02139 | 190 | 186 |  |
| S_EW_WHjj_taunu | 0.08233 | 1032 | 1016 |  |
| S_EW_WHjj | 0.9905 | 13181 | 13045 |  |
| Q_aajj | 0.05306 | 8391 + 0 direct | 8351 | misID nominal 0.0531 (low 0.0159, high 0.159); heavy-flavour direct 0 (UL 0.475) |

## 7. Checks and caveats
- All 1502 skim jobs and 484 rate jobs exit 0 (counts match make_sub_py.py 'todo = 0'). Skim superset cuts (mjj>300, |deta|>2, mgg 100-180) are looser than the regions here.
- One-fake closure (direct genuine / nominal) is poor at the available statistics (see F_QCD_Wajjj: direct genuine 0.95 events (6 raw rows) in PRE vs 2.4 nominal, 0 in PEAK (UL shown)): not a validation of the nominal; the direct count with artefacts (upper variation) is 3-4x the nominal in PRE/PEAK and is carried only in the high bound.
- Two-fake: direct counts have zero raw support, UL (31.8 / 292 events) is far above the fake-factor prediction (0.05 / 0.01): uninformative, as the prediction is 3 orders below it.
- Non-prompt-lepton nominal is a parametrisation with uncited x distribution and a placeholder muon rate (D40); heavy-flavour direct has 5 raw rows in PRE and zero in PEAK (UL carried). H_ggF_jj missing.
- Region PRE/VBS/PEAK are block-level; b-veto uses at most the 6 stored remaining jets; no lepton isolation variation here; K-factors not applied (LO), no EW-QCD interference for Waajj.
- ZH_Zajj_eFake dominates the lost-lepton class; its C range is wide (the 87 % systematic); human question (c) (top-up) open.
- PS-modelling (D29 100 %) and D27 f-scenarios are statistics-stage nuisances, not in low/high.

## 8. Next
Wait for verification/review of this block; then selection (05_selection.md). H_ggF_jj when 893012 ends (D38 fallback UL otherwise).
