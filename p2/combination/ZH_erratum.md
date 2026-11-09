STATUS (2026-11-09): COMPLETE (PASS with caveats). Answers 1-4 below; corrected numbers in zh_check/zh_corrected_inputs.json (changed = true). No condor jobs outstanding.

# ZH erratum (D37): fake-photon component of the frozen ZH study (tag zh-final-v1.1)
ROLE=executor-zh-erratum PHASE=FINAL, multi_r1. Date 2026-11-09 UTC. Frozen ZH tree untouched (read-only); everything is in p2/combination/zh_check/.

## DECISION NEEDED (non-blocking; the study is finished with the choices stated)
1. **Calibration reference mismatch (D34).** The only published CMS non-prompt-photon number in a comparable final state that I could verify is arXiv:2105.12780 (JHEP 10 (2021) 174), Table 2, Z gamma gamma: misidentified-jet backgrounds 42 (ee) and 98 (mumu) events against expected signal 68 and 157 (137 fb^-1). It is inclusive in jet multiplicity, while the frozen ZH fake samples are Z gamma + >=2 ME partons. The calibration factor kappa = 0.96 is therefore a rough closure, not an independent measurement. Its effect is negligible (see variations), so I did not stop. If a different record or a like-for-like inclusive Z gamma(+gamma) sample is wanted, say so.
2. **No Z gamma + 3 jets (ME+1j) row exists in the frozen ZH production.** With the fake photon consuming one jet, the third jet is parton-shower only. The same limitation holds for the frozen direct count, but it means the corrected fake component may be an underestimate. Bound: setting the fake component back to the frozen direct count moves Z by +5 % at most (table below). Producing the row would be new production under SPEC section 3.4; I have not started it.

## Answers
### 1. Inheritance: NO
- The ZH study never used any measured j->gamma table, contaminated or not. Its fake-factor cross-check used an *assumed* flat/parametrised rate: config/sample_matrix_phase02.yaml:149-157 (f_nominal 1.0e-3, f(pT) = f0 (pT/50)^-0.5, x2 in the endcap, "NOT data-driven"), applied in scripts/analysis/ntuple.py:13-18,128,137-138 (x ~ N(0.85,0.10), weights 1e-3 and 1e-3 (pT/50)^-0.5) and scripts/fakefactor_pilot.py:16 (F0 = 1.0e-3) and :45 (frate). The cross-check results are in scripts/analysis/final_analysis.py:563-575 (ff_xcheck: f = 5e-4, 1e-3, 2e-3 -> 0.0142/0.0284/0.0568 events at 500 fb^-1, direct 0.0372).
- The nominal ZH fake rows are *direct Delphes counts*: scripts/analysis/final_analysis.py:65-66 (F_QCD_Zajj, F_EW_Zajj, "direct Delphes fakes"), with a flat 50 % normalisation uncertainty (final_analysis.py:319,335). No lepton-removal step was applied because no rate was built; no electron-induced photon-object rate entered.
- No WH table or code can have entered: the ZH tag zh-final-v1.1 is dated 2026-11-03 15:25 +0100, the ZH scripts are dated 2026-11-02/03, while the lepton-contaminated tables are from the WH multi_r1 work of 2026-11-04..07 (SPEC section 7). p2/lib/scripts (the ZH export) differs from the ZH tree only by condor files (diff -rq scripts p2/lib/scripts) and contains no WH-derived code; neither final_analysis.py, ntuple.py nor sensitivity.py references WH.
- What ZH does inherit is the *artefact* (Q2), not the contamination: the direct-count photons come from the same Delphes card.

### 2. Artefact in the ZH direct-count fake photons: YES, 70-100 % of the non-prompt photons
Definition (GenTruth only; Particle is not in the production slim files): a selected reco photon is *prompt* if a prompt generator photon (pT > 10) lies within dR < 0.1; *lepton* if a generator e/mu (pT > 5) lies within dR < 0.2; *genuine* if a non-prompt generator photon (pT > 10) lies within dR < 0.1 and carries pT_gen > 0.5 pT_reco; otherwise *artefact* (no gen photon pT > 10 within dR < 0.1 carrying > 50 % of the reco pT, i.e. the energy-flow class). Code: zh_check/zh_ntuple.py (class codes 1-4), summary zh_check/out/analysis.json (Q2). The direct ntuples reproduce the frozen ones event for event (mll of file 0 identical; N_events 5 989 548 / 500 000 equal to final verify.json).
Raw counts in the frozen samples (selected photons of the leading two, events with 2 photons pT>20 and an OSSF pair):

| sample, level | prompt | lepton | genuine | artefact | artefact fraction of non-prompt photons |
|---|---|---|---|---|---|
| F_QCD_llajj_vbs, 2 photons + OSSF | 19866 | 82 | 212 | 1022 | 77.7 % |
| F_QCD_llajj_vbs, + Z window, pT>25, mllgg>100 | 11089 | 19 | 142 | 458 | 74.0 % |
| F_QCD_llajj_vbs, + VBS (mjj>500, deta>3.5) | 1814 | 1 | 21 | 86 | 79.6 % |
| F_QCD_llajj_vbs, + VBS + 105<mgg<165 | 466 | 0 | 5 | 25 | 83.3 % |
| F_QCD_llajj_vbs, frozen SR (+ mgg window) | 89 | 0 | 0 | 5 | 5 of 5 events |
| F_EW_llajj_vbs, 2 photons + OSSF | 4796 | 22 | 35 | 129 | 69.4 % |
| F_EW_llajj_vbs, + VBS | 2154 | 6 | 9 | 53 | 77.9 % |
| F_EW_llajj_vbs, + VBS + 105<mgg<165 | 562 | 1 | 0 | 17 | 94.4 % |
| F_EW_llajj_vbs, frozen SR | 99 | 0 | 0 | 3 | 3 of 3 events |
| T_tta, 2 photons + OSSF | 902 | 3 | 5 | 48 | 85.7 % |
| T_tWa, 2 photons + OSSF | 125 | 0 | 0 | 9 | 100 % |
| control B_QCD_zaajj_nomjj (prompt Zgg), 2 photons + OSSF | 20736 | 41 | 4 | 11 | 19.6 % (of 56 photons; the 11 are mostly FSR-like/merged) |

- Artefact photon pT: median 28-36 GeV (5-95 %: 20-117 GeV; in the SR 34-38 GeV), consistent with the 27-49 GeV class of the WH origin diagnosis. The frozen direct SR fake yield (0.0372 + 0.0218 events at 500 fb^-1) is built on 8 raw events (5 + 3, plus the exponential shape extrapolation), all of artefact class; zero events contain a genuine in-jet photon. The raw statistics are small (+-0.3 in fraction at the SR level), but the pattern is stable over all levels.
- T_tta/T_tWa direct photons are also dominated by the artefact class at the loose level; their contribution to b is 0.0034 events (0.7 %) and is left unchanged (flagged in zh_corrected_inputs.json).

### 3. Re-evaluation with the H1 method (D34)
Method (code zh_check/zh_ntuple.py, zh_ffmod_lib.py, zh_ffmod.py, final_analysis_ff.py):
- **Rate.** r(pT, |eta|) = fraction of GenJets (pT 25-1000, |eta| < 2.5, no prompt gen lepton and no reco lepton (pT>10) within dR < 0.4, no prompt gen photon within dR < 0.4, events with n_prompt_photons <= 1) that have a reco photon (pT > 10, |eta| < 2.5) within dR < 0.2 which is (i) not within dR < 0.1 of a prompt gen photon, (ii) **not within dR < 0.2 of a gen or reco lepton (lepton decontamination)**, and (iii) of the *genuine* class (artefact excluded). Same bins as the WH table (jet pT 25-35, 35-50, 50-75, 75-100, 100-150, 150-1000; barrel |eta| < 1.5). Built on F_QCD_llajj_vbs + F_EW_llajj_vbs (14.4 M + 0.72 M denominator jets). There is no Z+jets or W+jets sample in the frozen ZH production (npr == 0 rows do not exist); the Z gamma jets rows are the only jet-rich ones.
- Rate (percent per jet, barrel / endcap): 25-35: 0.0080/0.0045; 35-50: 0.0118/0.0088; 50-75: 0.0126/0.0122; 75-100: 0.0144/0.0111; 100-150: 0.0145/0.0131; 150-1000: 0.0175/0.0176 (raw numerators 111/40, 150/76, 181/121, 153/76, 223/112, 533/189 over the denominators in analysis.json). They are 1.7-3 times the WH W+jets values, i.e. ~1e-4 per jet, a factor ~8 below the flat 1e-3 assumed in the frozen cross-check. Mean x = pT(photon)/pT(GenJet) = 0.887 (artefact class 0.897). Pooled over jet pT, the x distribution (15 bins) is used for the fake-photon pT.
- Contamination check: counting every photon within dR < 0.2 of a jet without the lepton/artefact requirements gives 1952 + 266 against 1726 + 239 clean genuine, plus 177 + 24 artefact and 49 + 3 lepton-near; only 2 % of the numerator is lepton-near in ZH (98.8 % in the WH tables), because the denominator already excludes jets within dR < 0.4 of a lepton.
- **Application.** For each event of the F_* samples with n_prompt_photons == 1, one selected reco photon matched to the prompt photon, a Z candidate (mll > 55) and at least two remaining reco jets, each fake-candidate GenJet gives rows (jet, x-bin); weight = w_event x r(jet) x P(x); the faking jet is removed from the tag jets (closest reco jet within dR < 0.4); all frozen selection masks, the generator-mjj correction C (computed from 1-photon-level counts, unchanged), the window handling (L0 when >= 10 distinct events), the efficiency reweighting and the nuisance model are the frozen ones.
- **Closure (disjoint split).** Rate built on even chunks and applied to odd chunks and vice versa, against direct events of the other half with one prompt and one genuine-class photon (raw counts): F_QCD, Z + 2 photons pT>25, no VBS: observed 68 vs predicted 102.1 (ratio 0.67 +- 0.08, even->odd) and 69 vs 101.4 (0.68 +- 0.08, odd->even); with VBS: 7 vs 12.3 (0.57 +- 0.21) and 13 vs 12.1 (1.07 +- 0.30). F_EW: 7 vs 5.7 (1.2 +- 0.5), 21 vs 8.3 (2.5 +- 0.6), VBS: 3 vs 1.8, 6 vs 2.6. The prediction is therefore ~1.5x high for the QCD row at the pre-VBS level (a statistically significant non-closure of about 33 %, consistent in both halves) and scattered but statistics-limited for the EW row. The 50 % normalisation uncertainty of the frozen fake rows covers the QCD non-closure; the closure-scaled variant below uses kappa = 1.43.
- **CMS calibration.** Record: arXiv:2105.12780, JHEP 10 (2021) 174, doi:10.1007/JHEP10(2021)174, Table 2: R_CMS = misid jets / expected Zgg signal = (42 + 98)/(68 + 157) = 0.622 (relative uncertainty ~26 %, from the quoted syst. 9/42 and 27/98 plus the signal uncertainty). MC counterpart at a CMS-like selection (leading lepton pT > 35/30 GeV (e/mu), second > 15, mll > 55, two photons pT > 20, dR(gamma,gamma) > 0.4; >= 2 jets required in both samples): FF Z gamma + jets (F_QCD_llajj_nomjj, no generator mjj cut) 0.01794 fb over prompt Z gamma gamma + jets (B_QCD_zaajj_nomjj, 10283 raw) 0.02755 fb: R_MC = 0.651, so **kappa = R_CMS / R_MC = 0.956 +- 0.013 (MC stat only; CMS uncertainty 26 %)**. The difference is applied as a systematic: relative 4.6 % added in quadrature to the 50 % fake normalisation (FFD = 0.046). Caveat: see DECISION NEEDED 1.
- **Direct count as upper variation**: the frozen numbers (artefact included).

### 4. Impact on ZH b, Z and mu95 (frozen cuts; the re-optimisation returns the identical optimum: mjj > 500, |deta| > 3.5, |mll - mZ| < 25, +-2 sigma window)
Fake-photon component (events at 500 fb^-1 / 3000 fb^-1, F_QCD + F_EW, incl. generator-mjj correction): frozen direct 0.0590 / 0.3538 (raw window events 5 + 1; L1 shape fit) -> corrected 0.0081 / 0.0485 (0.0072 + 0.0009; 42 429 distinct events in the F_QCD window at 500 fb^-1; MC stat 1 %; rate statistical uncertainty 2.4 %). Calibrated/uncalibrated/closure-scaled: 0.0081 / 0.0085 / 0.0121 (500 fb^-1).

Per class, definition (a), expected events (all other classes identical):
| class | frozen 500 | corrected 500 | frozen 3000 | corrected 3000 |
|---|---|---|---|---|
| EW ZHjj (signal) | 0.0879 | 0.0879 | 0.5273 | 0.5273 |
| QCD ZHjj | 0.0474 | 0.0474 | 0.2844 | 0.2844 |
| Zg + fake g (QCD+EW) | 0.0590 | 0.0081 | 0.3538 | 0.0485 |
| Zgg (QCD+EW) | 0.3417 | 0.3417 | 2.0504 | 2.0504 |
| other H->gg | 0.0670 | 0.0670 | 0.4021 | 0.4021 |
| top (ttgg, ttg, tWg) | 0.0045 | 0.0045 | 0.0269 | 0.0269 |

Frozen vs corrected, all luminosities (columns: frozen = direct count with artefact; corrected = FF nominal with kappa = 0.956; uncal = kappa 1; closure-scaled = kappa 1.43):

| 500 | a | b | 0.5196 | 0.4687 | 0.4691 | 0.4727 |
| 500 | a | sigma_b | 0.0701 | 0.0647 | 0.0647 | 0.0649 |
| 500 | a | Z (Eq.1) | 0.1187 | 0.1246 | 0.1246 | 0.1241 |
| 500 | a | Z (with sigma_b) | 0.1181 | 0.1240 | 0.1240 | 0.1235 |
| 500 | a | mu95 CLs counting | 34.5012 | 34.5012 | 34.5012 | 34.5012 |
| 500 | a | mu95 mgg fit | 32.4879 | 31.7825 | 31.7878 | 31.8392 |
| 500 | a | Z mgg fit | 0.1251 | 0.1309 | 0.1308 | 0.1304 |
| 1000 | a | b | 1.0392 | 0.9374 | 0.9382 | 0.9454 |
| 1000 | a | sigma_b | 0.1402 | 0.1293 | 0.1293 | 0.1299 |
| 1000 | a | Z (Eq.1) | 0.1679 | 0.1763 | 0.1762 | 0.1755 |
| 1000 | a | Z (with sigma_b) | 0.1662 | 0.1746 | 0.1745 | 0.1739 |
| 1000 | a | mu95 CLs counting | 23.6669 | 23.9036 | 23.9017 | 23.8841 |
| 1000 | a | mu95 mgg fit | 19.2760 | 18.7628 | 18.7666 | 18.8040 |
| 1000 | a | Z mgg fit | 0.1761 | 0.1843 | 0.1842 | 0.1836 |
| 3000 | a | b | 3.1176 | 2.8123 | 2.8145 | 2.8363 |
| 3000 | a | sigma_b | 0.4205 | 0.3879 | 0.3880 | 0.3896 |
| 3000 | a | Z (Eq.1) | 0.2907 | 0.3053 | 0.3052 | 0.3041 |
| 3000 | a | Z (with sigma_b) | 0.2824 | 0.2970 | 0.2969 | 0.2958 |
| 3000 | a | mu95 CLs counting | 10.3672 | 10.6564 | 10.6541 | 10.6321 |
| 3000 | a | mu95 mgg fit | 9.0762 | 8.7697 | 8.7719 | 8.7941 |
| 3000 | a | Z mgg fit | 0.3001 | 0.3140 | 0.3139 | 0.3129 |
| 500 | b | b | 0.4722 | 0.4213 | 0.4217 | 0.4253 |
| 500 | b | sigma_b | 0.0679 | 0.0623 | 0.0623 | 0.0626 |
| 500 | b | Z (Eq.1) | 0.1884 | 0.1985 | 0.1984 | 0.1977 |
| 500 | b | Z (with sigma_b) | 0.1874 | 0.1975 | 0.1974 | 0.1967 |
| 500 | b | mu95 CLs counting | 22.7225 | 22.7225 | 22.7225 | 22.7225 |
| 500 | b | mu95 mgg fit | 20.7924 | 20.3109 | 20.3145 | 20.3497 |
| 500 | b | Z mgg fit | 0.1998 | 0.2098 | 0.2097 | 0.2090 |
| 1000 | b | b | 0.9444 | 0.8426 | 0.8434 | 0.8507 |
| 1000 | b | sigma_b | 0.1358 | 0.1246 | 0.1246 | 0.1252 |
| 1000 | b | Z (Eq.1) | 0.2665 | 0.2808 | 0.2806 | 0.2795 |
| 1000 | b | Z (with sigma_b) | 0.2637 | 0.2779 | 0.2778 | 0.2767 |
| 1000 | b | mu95 CLs counting | 15.7572 | 15.9263 | 15.9250 | 15.9124 |
| 1000 | b | mu95 mgg fit | 12.2685 | 11.9168 | 11.9195 | 11.9451 |
| 1000 | b | Z mgg fit | 0.2811 | 0.2953 | 0.2952 | 0.2941 |
| 3000 | b | b | 2.8332 | 2.5279 | 2.5302 | 2.5520 |
| 3000 | b | sigma_b | 0.4074 | 0.3738 | 0.3739 | 0.3755 |
| 3000 | b | Z (Eq.1) | 0.4615 | 0.4863 | 0.4861 | 0.4842 |
| 3000 | b | Z (with sigma_b) | 0.4475 | 0.4721 | 0.4719 | 0.4701 |
| 3000 | b | mu95 CLs counting | 7.0263 | 5.8856 | 5.8845 | 5.8742 |
| 3000 | b | mu95 mgg fit | 5.7283 | 5.5174 | 5.5190 | 5.5342 |
| 3000 | b | Z mgg fit | 0.4783 | 0.5023 | 0.5021 | 0.5004 |

Summary (definition (a), counting Eq. 1, 500 / 1000 / 3000 fb^-1): b 0.520 / 1.039 / 3.118 -> 0.469 / 0.937 / 2.812 (-9.8 %, -9.8 %, -9.8 %); Z_Eq1 0.1187 / 0.1679 / 0.2907 -> 0.1246 / 0.1763 / 0.3053 (+5.0 %); mu95 (CLs counting) 34.50 / 23.67 / 10.37 -> 34.50 / 23.90 / 10.66; mu95 (mgg profile-likelihood fit) 32.49 / 19.28 / 9.08 -> 31.78 / 18.76 / 8.77. The counting mu95 moves by -0 to +3 % and is non-monotonic: it is a discretised median (n_median) of the Poisson CLs and moves with b only in jumps; the fit mu95 improves by 2-3 %. The conclusion is unchanged: the ZH channel has Z << 1 (0.12-0.31) and mu95 >> 1 at all luminosities. Removing the artefact-dominated fake rows makes the background marginally smaller, not larger.

## Reproduction closure
Frozen final_analysis.py (read-only copy run via condor, job 899727, output zh_check/out/repro_final.json): all 8826 numeric fields of the output (registry, optimum, results, cutflows, fit, robustness, scans, coupling) agree with work/final_ntuples/final.json to a relative 1e-9 (results: 680 numbers, fit 36, robustness 80, zero differences). Eq. 1 Z 0.11869 / 0.16786 / 0.29074 and mu95 34.5012 / 23.6669 / 10.3672 at 500/1000/3000 fb^-1 reproduced. The corrected analysis is the same code with five documented string patches (final_analysis_ff.py header; patch list: exec zh_ffmod.py before SYST, fake-row nuisance quadrature with FFD, FIXOPT switch, ffinfo in the output).

## Caveats
- The rate is built on Z gamma + jets rows with a VBS-biased generation (jet pT, flavour mix and gluon fraction differ from W/Z + jets); there is no jets-only ZH sample, and statistical coverage at high pT is the best (533 events), at low pT the worst (40-111).
- Non-closure of ~33 % (QCD, pre-VBS) and a larger scatter for EW; both inside the 50 % normalisation used in the frozen study. The direct-count artefact fraction in the SR is based on 5 + 3 raw events.
- The genuine/artefact split uses GenTruth photons with pT > 10 only (Particle absent); genuine photons below 10 GeV would be classified as artefact. The WH executor's *_full.root validation of the veto was not repeated for ZH (no ZH *_full files).
- Both direct and FF fake estimates lack a Z gamma + 3 jets ME row (DECISION NEEDED 2), and double-fake (Z+jets, tt-bar) backgrounds remain outside b as in the frozen study.
- The "genmjj" correction C = 2.05 +- 3.4 % (unchanged) is applied to the FF F_QCD row; it was derived with direct 1-photon counts and does not depend on the fake method.
- Calibration reference caveat (DECISION NEEDED 1); electron->photon, other-Higgs and top rows unchanged.

## Files
zh_check/: zh_ntuple.py, job.sh, jobs/{submit,repro,scen}.sub, zh_ffmod_lib.py, zh_ffmod.py, final_analysis_ff.py, zh_analyze.py, make_tables.py, out/{analysis.json,*_rate.npz,*_dir.npz,*_ffm.npz,ff_*.json,repro_final.json,tables.md}, zh_corrected_inputs.json, VERIFY_REQUEST.md. Condor clusters: 899727 (reproduction), 899825 (ntupling; 899726 and 899731 failed on destination path/arguments and wrote nothing), 899830 (corrected analysis scenarios). Seeds: none (no MC generation).
