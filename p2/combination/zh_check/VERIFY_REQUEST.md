# VERIFY_REQUEST: ZH erratum (D37), executor-zh-erratum, multi_r1
Please verify independently (read-only):
1. Reproduction: p2/combination/zh_check/out/repro_final.json (condor 899727, frozen final_analysis.py unchanged) equals work/final_ntuples/final.json (all 8826 JSON leaves, 8334 numeric to 1e-9).
2. Q1 inheritance: file:line claims in ZH_erratum.md answer 1 (config/sample_matrix_phase02.yaml:149-157, scripts/analysis/ntuple.py:13-18,128,137-138, scripts/analysis/final_analysis.py:65-66,319,335,563-575, scripts/fakefactor_pilot.py:16,45); tag date 2026-11-03 vs WH tables 2026-11-04..07.
3. Q2 artefact counts: out/analysis.json "Q2" (class definition in zh_ntuple.py docstring); direct ntuples match the frozen npz event for event (N events equal to verify.json; spot check mll of F_QCD file 0).
4. Q3 rate and closure: out/analysis.json "rate", "closure", "calibration"; recompute r = num_gen/den from the *_rate.npz files; check lepton decontamination (dR<0.2 to gen/reco lepton) and artefact exclusion in zh_ntuple.py rate block; check the CMS record (arXiv:2105.12780 Table 2 numbers 42, 98, 68, 157) and the CMS-like selection used for kappa.
5. Q4 impact: out/ff2_*.json (condor 899913; ff_closcorr_fix.json is superseded) vs frozen; compare zh_corrected_inputs.json with out/tables.md; check that only F_QCD_Zajj and F_EW_Zajj changed (components in out/ff_cal_fix.json) and that the re-optimised optimum equals the frozen one.
6. Judge the two DECISION NEEDED items (calibration reference mismatch; no Z gamma + 3 jets row).


## R2 (final round, Part B, 2026-11-14)
Changed or new numbers (old -> new, source key):
1. ZH nominal corrected results (ff_cal_fix.json -> ff2_nominal.json, EW fake row uncertainty hypot(0.5,1.5) instead of hypot(0.5,0.046)): b, s, Z_eq1 unchanged; sigma_b 0.06465 -> 0.06467 (500 a), 0.3879 -> 0.3880 (3000 a); over all six results (500/1000/3000, defs a, b) the largest relative changes are 1.4e-5 for Z-type quantities (Z_eq1, Z with sigma_b, fit Z), 4.1e-6 for mu95-type quantities (counting CLs, fit mu95) and 2.5e-4 for sigma_b (out/ff_cal_fix.json -> out/ff2_nominal.json: results/fit). (Corrects the former statement '<= 2e-7'.)
2. vh_ws/zh_channel_inputs.json: ZH signal template sum 0.09333 events (= final.json fit s_tot 0.09333); corrected fake rows 0.0458 + 0.0061 over 105-165 GeV (window yields 0.0072 + 0.0009); per-bin templates; closure of the quadratic coupling model: LOO pulls in out (zh_assemble.py output).
3. vh_ws/orthogonality.json: overlap 0; per-sample counts (raw, weighted, MC unc.). Check: WH SR on S_EW_WHjj 8162 vs 8157 (WH table), ZH SR counts equal the frozen raw_win counts.
4. ZH-alone pyhf from the templates (out/zh_pyhf.json: repro): Z0_PL 0.1310 / 0.1839 / 0.3125 (500/1000/3000, def a) vs frozen-code fit 0.1309 / 0.1843 / 0.3140; mu95_PL 33.1 / 19.5 / 9.27 vs 31.8 / 18.8 / 8.77 (asymptotic CLs implementations differ, +4-6 %).
5. ZH-alone mgg q-curves (out/zh_pyhf.json qcurves): Z(lambda=-1) 0.2888/0.4066/0.6928 (kZ primary), 0.7205/1.0126/1.7136 (kW variant) at 500/1000/3000; c_A and lambda q-curves with corrected inputs (frozen method): zh_paper_inputs.json coupling/cA (frozen vs corrected both present).
6. New nuisances (pheff, lepeff, phscale, phres) in the ZH channel are assumptions copied from the WH model, not part of the frozen ZH study (nuisance_names_zh.json).
Please check: (a) the lepton-multiplicity exclusivity claim and the re-implementations (ortho.py), (b) the shapefactor-based q-curve construction in zh_pyhf.py (NLL constants), (c) alpha/beta/gamma labelling (alpha = kW^2 coefficient).


## R3 (verifier fixes 1-11, 2026-11-14)
1. tau_r: not applied in the ZH channel; argument in vh_ws/nuisance_names_zh.json['tau_r_decision'] (Z->tautau->OSSF ee/mumu is 0.31 % of Z->ee+mumu before the mass window, 30x below the WH r_tau = 0.083). Recommendation to the WH side: tau_r is applied to ZH-sample rows in the WH SR where the relevant effect is Z->tautau->l + lost lepton; make that name row-specific (e.g. tau_r_zrows). WH files not edited.
2. scale_fake1_qcd renamed scale_top_zh for T_tta/T_tWa (dilepton top samples, different from WH's fake1_qcd group); zh_channel_inputs.json nuis keys and nuisance_names_zh.json updated; correlated_with_WH = false, wh_name = null.
3. whsig_in_zh dropped from defs a/b (zero MC support). Bound kept in zh_channel_inputs.json['wh_signal_in_zh_sr']: in_fit = false, UL95 = 4.65e-4 events at 500 fb^-1 (both WH signal samples together), 0.1 % of the ZH background; per-point raw counts in the ZH SR are stored.
4. coupling.points: per point 'generated_point' (kW=lambda, kZ=+1, as generated), 'kW_sign_variant' (same, with R_BR) and 'kZ_sign_primary' (kW=-lambda, kZ=-1, R_BR); same yields, only R_BR differs.
5. zh_norm_<sid>: norm_up = 1+r, norm_down = 1/(1+r) (log-normal-style), no floor: F_EW row 2.581 / 0.3874.
6. window definition stated in zh_channel_inputs.json['window_definition']; per sample yield_window_500 (exact +-2 sigma window, 120.86-129.14 GeV, 8.28 GeV) and yield_bins_121_129_500 (whole 2 GeV bins, 8 GeV): fake1_qcd 0.007155 vs 0.006921.
7. orthogonality.json: now 47 samples, 13.2 M events, overlap 0; added WH_F_QCD_llajj_loose (5.75 M events: 3 ZH-SR, 1 WH-SR, 0 both; includes the v1.2 top-up) and WH_F_QCD_llajj_nomjj (v1.2, 2.6 M events: 4 ZH-SR, 0 WH-SR, 0 both; k = 1 assumed, the row is not in SAMPLES.csv). Notes added: fake rows tested with the real-photon selection only + the photon-independent exclusivity argument (lepton collection) for the one-photon fake method + the isolation remark (the veto in the code has no isolation).
8. zh_pyhf.py docstring corrected (q-curves exclude the signal phscale/phres histosys; everything else included).
9. R2 item 1 corrected (see above).
10. c_A note now lists every interval that differs (generated): 1000|noclip|int95 [-1.3,1.3] -> [-1.2,1.3] and 1000|clip500|int68 [-3.5,3.5] -> [-3.5,3.4].
11. wh_name fields are names only; prose moved to wh_note.
Please check: nuisance_names_zh.json tau_r_decision, the renamed key in zh_channel_inputs.json, and that no sample in defs carries role signal_like.
