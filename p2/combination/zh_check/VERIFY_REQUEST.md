# VERIFY_REQUEST: ZH erratum (D37), executor-zh-erratum, multi_r1
Please verify independently (read-only):
1. Reproduction: p2/combination/zh_check/out/repro_final.json (condor 899727, frozen final_analysis.py unchanged) equals work/final_ntuples/final.json (all 8826 numeric fields to 1e-9).
2. Q1 inheritance: file:line claims in ZH_erratum.md answer 1 (config/sample_matrix_phase02.yaml:149-157, scripts/analysis/ntuple.py:13-18,128,137-138, scripts/analysis/final_analysis.py:65-66,319,335,563-575, scripts/fakefactor_pilot.py:16,45); tag date 2026-11-03 vs WH tables 2026-11-04..07.
3. Q2 artefact counts: out/analysis.json "Q2" (class definition in zh_ntuple.py docstring); direct ntuples match the frozen npz event for event (N events equal to verify.json; spot check mll of F_QCD file 0).
4. Q3 rate and closure: out/analysis.json "rate", "closure", "calibration"; recompute r = num_gen/den from the *_rate.npz files; check lepton decontamination (dR<0.2 to gen/reco lepton) and artefact exclusion in zh_ntuple.py rate block; check the CMS record (arXiv:2105.12780 Table 2 numbers 42, 98, 68, 157) and the CMS-like selection used for kappa.
5. Q4 impact: out/ff_*.json (condor 899830) vs frozen; compare zh_corrected_inputs.json with out/tables.md; check that only F_QCD_Zajj and F_EW_Zajj changed (components in out/ff_cal_fix.json) and that the re-optimised optimum equals the frozen one.
6. Judge the two DECISION NEEDED items (calibration reference mismatch; no Z gamma + 3 jets row).
