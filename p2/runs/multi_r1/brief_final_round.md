# Brief: final round before refreeze, multi_r1 (orchestrator, 2026-11-14; human decisions D39–D48)

Binding sources: p2/SPEC.md §6 D39–D48 (read D42, D46, D47 verbatim), this brief, and the earlier briefs brief_wh_final.md / brief_zh_erratum.md, whose write-location and safety rules still apply unchanged.
- ZH tree (repo root reports/ cards/ config/ scripts/ work/ production/ figures/) is frozen and read-only.
- Never touch other run directories (multi_r2, multi_r3, single_r*), hh/, ~/.codex, /eos/home-r/rjiang/.git.
- No git (orchestrator commits). No tokens in files/logs. Anything >~10 min CPU goes to condor (bigbird103.cern.ch); toys included.
- Human decisions: D39, D40, D41, D43, D44, D45 = the recorded defaults. D46: 3.8σ (convention-independent) is primary; ≈6σ quoted only with its convention (sign on κW, κZ=κt=+1) stated next to it.

Two executors work in parallel. Interfaces between them are files in p2/combination/vh_ws/ (create it).

## Part A — executor-wh (writes p2/runs/multi_r1/wh/, p2/combination/ except ZH_erratum.md and zh_check/, p2/production/wh/ v1.2 rows only)
A1. Production (D42 + N rule).
 - ZH_Zajj nomjj top-up (the ≈2.4M, ≈125 core-h option you quoted for D42), as v1.2 rows: test job, N rule, seeds per SPEC §3.4 (J ≥ 600, no collision with existing seeds; check), D33 for held jobs.
 - Any further top-up needed so that EVERY SR background class has N_eff ≥ 10 (lost-lepton is at 7.6). List all classes with N_eff before and after. If a class cannot reach 10 within the 200 GB budget, state the cost and raise it in STATUS (do not stop other work).
 - Update SAMPLES.csv, SHA256SUMS, V1.2_NOTES.md; record new manifest for the orchestrator.
A2. Re-evaluate with FROZEN cuts and models (D45: check the >30 % share-change trigger and report it; retrain only if it fires, nested CV only, primary choice not re-decided). Also the PRE-region lost-lepton/e→γ with the nomjj sample (replaces the stated bound).
A3. Joint VH likelihood (D47 (1)), one pyhf workspace, committed as p2/combination/vh_ws/VH_workspace.json (plus WH_workspace.json, ZH_workspace.json single-channel versions built from the same code):
 - ZH channel = the ZH executor's templates (Part B, vh_ws/zh_channel_inputs.json). WH channel = yours.
 - EW ZHjj signal in the WH SR (lost lepton) is a signal-like sample: scaled by μ_VH (common) / μ_ZH (2D), and by the ZH coupling dependence (κZ, λWZ) in coupling fits; not a fixed background. Same for WH signal in the ZH SR (from Part B). Report their yields.
 - Correlation scheme (write a table in VH_combination.md and as vh_ws/correlation_scheme.json): correlated = lumi, photon efficiency, lepton efficiency, photon energy scale / m_γγ resolution, theory scale and PDF for common processes (state which processes are common); uncorrelated = MC statistics (per-bin, per channel), channel-specific background normalisations unless the same sample/process (state). 
 - Same λWZ sign convention (convention-independent κZ-sign primary, κW-sign variant) and same R_BR treatment in both channels; state it. Check the ZH q-curves are re-derived, not inherited.
 - Results at 500/1000/3000 fb⁻¹: common μ_VH (Z0, μ95); 2D (μ_WH, μ_ZH) contours + channel-compatibility test (p-value); 2D (κW, κZ) contours and 1D λWZ for WH, ZH and VH (λ=−1 and λ<0 exclusions).
A4. Validation of asymptotics (D47 (2)): toys (condor) or exact method for Z0 and μ95 at 500 fb⁻¹ for WH, ZH and VH, and for the λWZ=−1 exclusion. Report asymptotic vs toy with toy MC error; state N toys.
A5. Limitations (D47 (3)) in FINAL_report.md and VH_combination.md: f_μ placeholder (D40); fake-photon calibration reference mismatch (D39/D43, scan ×0.3–×3 covers it); other-Higgs backgrounds not rescaled under coupling hypotheses (quantify if cheap); no Zγ+3j row in ZH (D43).
A6. Paper package p2/combination/paper/ (D47 (5)): one consistent set, ZH (corrected) | WH | VH side by side, PDF+PNG figures, LaTeX-ready tables (.tex) + one paper_numbers.json from which EVERY number in tables/figures is generated (each entry: value, source json path/key, script). Contents: samples (σ, BR, N); cutflows; background composition incl. non-prompt classes; Z (Eq. 1 and PL) and μ95 at 500/1000/3000 for defs (a) and (b); systematics impact; non-prompt normalisation scans (photon, lepton separately); λWZ and (κW, κZ); c_A for ZH (from Part B); CMS/ATLAS comparison at matched luminosity (verified citations). Plus paper/README.md (how to regenerate; one command).
A7. Regenerate all reports from scripts. Replace ORCH_COMMIT_PLACEHOLDER handling: generators read the hash from a file vh_ws/ANALYSIS_COMMIT (orchestrator writes it) so regeneration does not lose the pin.
A8. VERIFY_REQUEST per block (production, re-evaluation, workspace/combination, toys, paper package) listing every changed number old→new with source key.

## Part B — ZH-erratum executor (writes p2/combination/zh_check/ and p2/combination/vh_ws/zh_* only)
B1. zh_channel_inputs.json: corrected ZH SR per-bin m_γγ templates (signal defs (a),(b), each background class, MC-stat per bin, systematics as up/down per bin with names following the correlation-scheme names in A3; agree the names by writing vh_ws/nuisance_names_zh.json first).
B2. Event-level orthogonality: apply the frozen ZH SR selection and the WH SR selection (read-only: wh/reports/05_selection.md and the WH selection code under wh/work or wh/scripts; do not edit) to all signal samples of both channels and the main shared backgrounds; report the overlap count (raw and weighted) per sample. Write vh_ws/orthogonality.json.
B3. WH signal in the ZH SR: yield (raw, weighted, MC unc.) from the WH signal and WH coupling samples; template for B1 as a signal-like sample.
B4. ZH coupling templates per bin for (κW, κZ) / λWZ with corrected inputs, same per-bin-quadratic method, sign convention and R_BR as WH (read wh/work/stat/couplings_kzneg_v11.json for the convention, read-only). c_A for ZH: re-derive with corrected inputs (or state frozen ZH value unchanged and why).
B5. Samples/cutflow/composition tables for ZH (corrected) in json for the paper package: vh_ws/zh_paper_inputs.json.
B6. VERIFY_REQUEST in zh_check/ listing every changed number.

## Protocol
- STATUS.md (≤ 25 lines) per executor (wh/STATUS.md; zh_check/STATUS.md); reply to the orchestrator = pointer only.
- Waiting on condor: set STATUS "waiting on clusters X" and return; no idle polling.
- First line of work log: ROLE=executor-wh PHASE=FINAL-R2 / ROLE=executor-zh-erratum PHASE=FINAL-R2.
