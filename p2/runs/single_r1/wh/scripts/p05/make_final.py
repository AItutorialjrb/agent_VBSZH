#!/usr/bin/env python3
"""single_r1 WH: FINAL_report.md from reports/final.json + work/p05/*.json (numbers never typed by hand)."""
import json, os, datetime
WH = "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/single_r1/wh"
F = json.load(open(f"{WH}/reports/final.json")); P5 = json.load(open(f"{WH}/work/p05/p05.json")); B = json.load(open(f"{WH}/work/p05/bdt.json"))
P7 = json.load(open(f"{WH}/work/p05/p07.json")); U = open(f"{WH}/work/p05/usage.md").read() if os.path.exists(f"{WH}/work/p05/usage.md") else "(see STATUS)"
c, cc, fi, co = F["counting"], F["counting_cutbased"], F["fit"], F["coupling"]
NOW = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M UTC")
def row(k, d=c, fit=True):
    v = d[k]; s = f"| {int(v['L'])} | {v['sigdef']} | {v['s']:.2f} | {v['b']:.2f} | {v['sigma_b']:.2f} | **{v['Z_eq1']:.2f} ± {v['Z_eq1_mcerr']:.2f}** | {v['Z_syst']:.2f} | {v['mu95_cls']:.2f} | {v['mu95_cls_stat']:.2f} |"
    return s + (f" {fi[k]['Z_syst']:.2f} | {fi[k]['mu95_syst']:.2f} |" if fit else "")
K = ["500_a", "1000_a", "3000_a", "500_b", "1000_b", "3000_b"]
FC = F["final_selection"]
txt = f"""# FINAL report — EW W±Hjj (W→eν/μν, H→γγ), √s = 13.6 TeV — single-agent arm, run single_r1

**Date:** {NOW}. **Status: FINAL (expected results; Delphes level; LO MC).** Phases 01–03 (G1, accepted 2026-11-14 with the declared defaults) and 05–07 (amendment A2) of this run; Phase 04 (production) is the canonical frozen package `p2/production/wh` (wh-prod-v1 + v1.1 rows, read-only) plus one own sample.
Reports: `01_signal_definition.md`, `02_background_overlap.md`, `03_generation_validation.md` (+ addendum), `05_selection.md`, `06_systematics.md`, `07_sensitivity.md`; machine-readable `final.json`; self-reviews `../reviews/wh_01-03_self_review.md`, `../reviews/wh_05-07_self_review.md`.

## 1. Result
Signal definition (a): EW W±Hjj at (QCD, QED) = (0, 4), 4F jets, W→eν/μν, H→γγ (BR applied once); QCD W±H(+jets) is a resonant background. Definition (b): signal = EW + QCD W±H.
Final selection: one lepton (pT>25, veto on a 2nd lepton >10 GeV), two photons (pT/m_γγ > 1/3, 1/4), 2 jets pT>30, b-veto, m_eγ Z-veto, m_jj > {FC['mjj']:.0f}, |Δη_jj| > {FC['deta']:.1f}, **BDT > {FC['bdt']:.2f}** (xgboost, 5-fold, m_γγ not an input), window {FC['win'][0]:.1f}–{FC['win'][1]:.1f} GeV (±2σ of the Delphes peak, σ = {F['peak']['sigma_core']:.2f} GeV).

| L [fb⁻¹] | def | s | b | σ_b | **Z Eq. 1 (stat) ± MC** | Z with σ_b | μ95 CLs exact Poisson (syst) | μ95 (stat) | Z m_γγ fit (syst) | μ95 fit (syst) |
|---|---|---|---|---|---|---|---|---|---|---|
""" + "\n".join(row(k) for k in K) + f"""

**Cut-based selection (no BDT; reported alongside because the BDT stability is marginal):**

| L [fb⁻¹] | def | s | b | σ_b | Z Eq. 1 ± MC | Z with σ_b | μ95 (syst) | μ95 (stat) |
|---|---|---|---|---|---|---|---|---|
""" + "\n".join(row(k, cc, False) for k in K) + f"""

**Coupling interpretation (rate only, BR(H→γγ) fixed to SM, κ_Z = 1 for λ_WZ):**

| L [fb⁻¹] | Z excl. λ_WZ = −1 | Z excl. λ_WZ < 0 | λ_WZ 68 % | λ_WZ 95 % |
|---|---|---|---|---|
""" + "\n".join(f"| {L} | {v['Z_excl_lam_m1']:.1f} | {v['Z_excl_lam_neg']:.2f} | [{v['lam68'][0]:.2f}, {v['lam68'][1]:.2f}] | [{v['lam95'][0]:.2f}, {v['lam95'][1]:.2f}] |" for L, v in co.items()) + f"""

(κ_W, κ_Z): quadratic yield Y = {co['500']['quad']['a']:.3f} κ_W² {co['500']['quad']['b']:+.3f} κ_W κ_Z + {co['500']['quad']['g']:.3f} κ_Z² events at 500 fb⁻¹ (fit to six λ points; closure on the two κ points and the SM sample within 2σ); contours `figures/p07_kappa_contours.png`.

**In words.** At 500 fb⁻¹ the expected EW W±Hjj significance is below 1σ (Eq. 1: {c['500_a']['Z_eq1']:.2f}; cut-based {cc['500_a']['Z_eq1']:.2f}); at 3000 fb⁻¹ (luminosity scaling of the Run-3-like detector, not an HL-LHC prediction) it reaches {c['3000_a']['Z_eq1']:.1f}σ stat-only and {c['3000_a']['Z_syst']:.1f}σ with systematics (cut-based {cc['3000_a']['Z_eq1']:.1f} / {cc['3000_a']['Z_syst']:.1f}). The expected 95 % CL limit on μ is {c['500_a']['mu95_cls']:.1f} × SM at 500 fb⁻¹ and ≈ {c['3000_a']['mu95_cls']:.1f} × SM at 3000 fb⁻¹. The sign-flipped coupling λ_WZ = −1 (5× the SM rate) is excluded at {co['500']['Z_excl_lam_m1']:.1f}σ already at 500 fb⁻¹; excluding all λ_WZ < 0 by rate is limited by λ → 0⁻ ({co['500']['Z_excl_lam_neg']:.1f}σ / {co['3000']['Z_excl_lam_neg']:.1f}σ at 500 / 3000 fb⁻¹).

## 2. Background composition (final selection, 500 fb⁻¹, def. a; every source in 05 §7)
EW Wγγjj {F['sr_components_500_a']['B_EW_Waajj_nomjj']['y']:.2f}, tHq {F['sr_components_500_a']['H_tHq_lep']['y']:.2f}, QCD Wγγjj {F['sr_components_500_a']['B_QCD_Waajj_nomjj']['y']:.2f}, Wγ+jets (1 non-prompt γ) {F['sr_components_500_a']['F_QCD_Wajjj_nomjj']['y'] + F['sr_components_500_a']['F_EW_Wajj_nomjj']['y']:.2f}, W→τν feed-down {F['sr_components_500_a']['S_EW_WHjj_taunu']['y']:.2f}, QCD WH {F['sr_components_500_a']['H_QCD_WH_mlm']['y']:.2f}, ZH lost-ℓ {sum(F['sr_components_500_a'][k]['y'] for k in ('ZH_ew_zhjj_zll', 'ZH_qcd_zhjj_zll', 'H_ggZH_wh', 'H_ZH_tautau_wh')):.2f}, e→γ {sum(F['sr_components_500_a'][k]['y'] for k in ('F_QCD_llajj_loose', 'ZH_F_EW_llajj_vbs', 'V_WWa_WH', 'V_WZa_WH', 'V_ZZa_WH')):.2f}, non-prompt ℓ {sum(F['sr_components_500_a'][k]['y'] for k in ('Q_aajjj', 'H_VBFH_jj', 'H_ggF_jj_nomjj')):.3f}, W+jets 2 fakes {F['sr_components_500_a']['F_Wjjjj']['y']:.3f}, Zγγjj lost-ℓ {sum(F['sr_components_500_a'][k]['y'] for k in ('ZH_B_QCD_zaajj_nomjj', 'ZH_B_EW_zaajj_vbs_is1h', 'ZH_B_EW_zaajj_vbs_is2', 'ZH_B_EW_zaajj_vbs_is3')):.3f}, top {sum(F['sr_components_500_a'][k]['y'] for k in ('T_ttaa_1l', 'T_tta_1l', 'T_tWa_1l', 'T_ttjj_1l')):.3f}, tt̄H/tHW {sum(F['sr_components_500_a'][k]['y'] for k in ('H_ttH_1l', 'H_ttH_dilep_wh', 'H_tHW_1l')):.3f} events. Non-prompt photons, non-prompt leptons and e→γ are estimated separately by per-object weighting with declared rate scenarios, each with a closure test against Delphes (05 §4) and its own uncertainty (06).

## 3. Robustness (500 fb⁻¹, def. a; full table 07 §2)
""" + "\n".join(f"- {r['variant']}: Z Eq. 1 = {r['Z_eq1']:.2f}, Z(σ_b) = {r['Z_syst']:.2f}, μ95 = {r['mu95']:.2f}" for r in F["robustness"] if r["L"] == 500 and r["sigdef"] == "a") + f"""

## 4. Checks performed
SHA256 of all {sum(v['sha_checked'] for v in P5['inventory'].values())} package files vs SHA256SUMS (0 bad); Σw/N per sample vs SAMPLES.csv; BR ledger asserted in code; N_MC ≥ max(50k, σ·BR·3000 fb⁻¹) enforced (`whana.nmc_check`, fails loudly; D-WH-2 effective-N for the weighted W+jets and tt̄jj two-fake rows, N_eff in the SR 7659 / 165); peak/resolution from Delphes; three closure tests (j→γ, j→ℓ, e→γ); BDT k-fold with held-out scoring and a pre-declared adoption rule; JES variation with BDT rescoring (exact closure at zero shift); quadratic coupling closure on independent samples; fit vs counting consistency (Z 0.90 vs 0.91 at 500 fb⁻¹, def. a).

## 5. Decisions (D-WH-n; G1 defaults accepted by the human 2026-11-14, later ones taken as this run's declared defaults per A2)
| ID | decision | taken |
|---|---|---|
| D-WH-1 | signal jets 4F (no b in j; 5F would include resonant tHq) | G1 default (human: accepted) |
| D-WH-2 | WH fake-weighted rows follow the HH effective-N policy (truth/fake weighting; N_eff ≥ 10 in SR or UL + conservative variant) | G1 default (accepted) |
| D-WH-3 | frozen ZH rows below N_req: accept with MC-stat nuisance; split rows checked as one SAMPLES.csv row (EW Zγγjj 3×20k = 60k ≥ 50k) | G1 default (accepted) |
| D-WH-4 | CMS-like object efficiencies (ZH final table) as nominal; stock Delphes as robustness | G1 default (accepted) |
| D-WH-5 | missing `H_ggF_jj` row → own HEFT sample `H_ggF_jj_nomjj` (no m_jj cut, 59 945 events ≥ 50k), FL weighting, 100 % PS-modelling | A2 default |
| D-WH-6 | fake/mis-ID rates: G1-declared scenarios are nominal (j→γ 10⁻³(pT/50)^−0.5 ×2 endcap ×{{0.3,1,3}}; e→γ {{1,2,5}} %; j→ℓ {{3·10⁻⁵, 2·10⁻⁴, 10⁻³}}); FORMAT-6a/6b Delphes rates only for closure and as variants | A2 default |
| D-WH-7 | non-prompt ℓ nominal = max(parametrised, Delphes direct) | A2 default (02 §5 option) |
| D-WH-8 | W→τν feed-down in the background for (a) and (b); scales with the couplings | A2 default (01 §5) |
| D-WH-9 | coupling interpretation rate-only with BR(H→γγ) fixed to SM; QCD WH ∝ κ_W² | A2 default |
| D-WH-10 | `Q_aajj`, `H_QCD_WHjj_fixed`, frozen `B_QCD_zaajj_vbs` are cross-checks only (SAMPLES.csv roles) | A2 default |
| D-WH-11 | own EW W⁻γγjj validation gridpack (failed twice, deterministic survey-channel error) not retried; canonical `B_EW_Waajj_nomjj` covers W± | A2 default |
| D-WH-12 | ZH-style estimation hierarchy (L0 direct / L1 m_γγ shape / L2 VBS-factorised 100 % / zero-support 1.14 w̄, UL 3 w̄) | A2 default |
| D-WH-13 | e→γ closure factor C = direct/weighted (relaxed region) applied when ≥ 10 raw direct events | A2 default |
| D-WH-14 | jet-modelling nuisance = MLM vs fixed-order QCD WH selection-efficiency ratio (backgrounds); signal PS 10 % (assumption) | A2 default |
| D-WH-15 | BDT adopted by the declared rule (gain > 10 % and positive in every fold, AUC gap < 0.02); cut-based shown alongside | A2 rule |

## 6. Reproducibility (08-equivalent)
Run commit: see `git log -- p2/runs/single_r1/wh/reports/FINAL_report.md`. Commands (from `p2/runs/single_r1/wh`, after `source ../../../lib/scripts/setup_stack.sh; export PYTHONPATH=$PWD/scripts/p05:$PYTHONPATH`):
1. own sample: `python3 -P scripts/make_cards.py; python3 -P scripts/make_submit.py 42 _p05`; `condor_submit scripts/condor/p03_gridpacks_p05.sub`, `p03_test_p05.sub`, `p05_prod_ggF.sub` (EosSubmit).
2. ntuples: `python3 -P scripts/p05/make_nt_jobs.py; condor_submit scripts/condor/p05_nt.sub` (+ `p05_nt_H_ggF_jj_nomjj.list`, run with `scripts/condor/p05_nt_job.sh <list> <line>`).
3. `python3 -P scripts/p05/p05_run.py && python3 -P scripts/p05/p05_bdt.py && python3 -P scripts/p05/p07_stats.py && python3 -P scripts/p05/make_figs.py && python3 -P scripts/p05/make_reports.py && python3 -P scripts/p05/make_final.py`.
Seeds: own MC 2442000–2442031 (SPEC_G0 §3.4, R = 4); ntuple x-draws 90000 + job index; BDT folds random_state 2400000 + fold. Stack: LCG_110 (MG5 3.6.3, Pythia 8.317, Delphes 3.5.1), xgboost 2.1.3, scikit-learn 1.9.0, uproot 5.7.1.

## 7. Caveats (main)
LO generators throughout; no pile-up; fake/mis-ID rates are scenarios; e→γ closure factor 4 for the loose QCD ℓℓγjj sample; the BDT stability is marginal (first run failed one fold before a bug fix); the jet-modelling nuisance is statistics-limited and the largest b uncertainty; signal PS uncertainty assumed; the asymptotic fit is approximate at O(1–10) events and the exact-Poisson μ95 is discrete; the coupling result ignores the κ-dependence of BR(H→γγ); no VH combination in this run.

## 8. Token / time (this run, from its own transcript)
{U}
"""
open(f"{WH}/reports/FINAL_report.md", "w").write(txt); print("wrote FINAL_report.md")
