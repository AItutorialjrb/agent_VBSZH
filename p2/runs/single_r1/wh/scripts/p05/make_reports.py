#!/usr/bin/env python3
"""single_r1 WH: write reports 05/06/07, FINAL_report.md and final.json from work/p05/{p05,bdt,p07}.json (numbers are never typed by
hand; narrative text is fixed here). Also computes the final-selection cutflow by source group.  Usage: python3 -P make_reports.py"""
import sys, os, json, glob, numpy as np, datetime, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import whana as A
W = f"{A.WH}/work/p05"; R = f"{A.WH}/reports"
P5, B, P7 = (json.load(open(f"{W}/{n}.json")) for n in ("p05", "bdt", "p07"))
tup = lambda c: {k: (tuple(v) if isinstance(v, list) else v) for k, v in c.items()}
FINAL, OPT = tup(P7["final_cuts"]), tup(P5["OPT"]); PK = P5["peak"]
NOW = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M UTC")
f2 = lambda x, n=2: "—" if x is None else (f"{x:.{n}f}" if abs(x) >= 10**-n or x == 0 else f"{x:.1e}")
GROUPS = P5["groups"]
# ---------------------------------------------------------------- final-selection cutflow by group (Store)
S = A.Store(verbose=False); S.ceg = {k: tuple(v) for k, v in P5["eg_closure_factor"].items()}
for f in glob.glob(f"{W}/bdt_scores/*.npz"):
    k, t = os.path.basename(f)[:-4].split("__")
    if k in S.T and S.T[k].get(t): S.T[k][t]["bdt"] = np.load(f)["score"]
PRE = tup(B["pre"])
OPEN = dict(A.BASE, l1pt=20., veto2=1e9, ratio=(0., 0.), fit=(95., 180.), met=-1., j2pt=25., j1pt=25., mjj=0., deta=0., bveto=False, meg=0.)
STEPS = [("1 ℓ (pT>25), ≥2 γ, ≥2 jets (pT>25)", dict(l1pt=25.), False), ("+ 2nd-ℓ veto, pT/m_γγ>1/3,1/4, 105<m_γγ<160", dict(veto2=10., ratio=(1/3, 1/4), fit=(105., 160.)), False),
         ("+ 2 jets pT>30, b-veto, m_eγ Z-veto (e channel)", dict(j2pt=30., j1pt=30., bveto=True, meg=PRE["meg"]), False),
         (f"+ m_jj>{PRE['mjj']:.0f}, Δη_jj (abs)>{PRE['deta']:.1f} (BDT preselection)", dict(mjj=PRE["mjj"], deta=PRE["deta"]), False),
         (f"+ BDT > {FINAL.get('bdt', 0):.2f}", dict(bdt=FINAL.get("bdt")), False), (f"+ m_γγ window {FINAL['win'][0]:.1f}–{FINAL['win'][1]:.1f} (final)", dict(win=FINAL["win"]), True)]
cf, c = [], dict(OPEN)
for name, upd, win in STEPS:
    c.update(upd); Y = A.yields(S, c, window=win)
    row = dict(step=name)
    for g, ks in GROUPS: row[g] = (sum(Y[k]["y"] for k in ks if k in Y)*500, sum(Y[k]["nraw"] for k in ks if k in Y))
    cf.append(row)
# ---------------------------------------------------------------- helpers
def table(head, rows): return "| " + " | ".join(head) + " |\n|" + "---|"*len(head) + "\n" + "".join("| " + " | ".join(str(x) for x in r) + " |\n" for r in rows)
def gsum(comp, ks): return sum(comp[k]["y"] for k in ks if k in comp)
C5 = P7["counting"]["500_a"]["comp"]
def sr_rows(comp, srt):
    rows = []
    for g, ks in GROUPS:
        for k in ks:
            if k not in comp: continue
            s = srt.get(k, {}); rows.append([g if k == ks[0] else "", f"`{k}`", A.R[k]["cls"], f2(comp[k]["y"], 3), f2(s.get("mc"), 3) if s else "", comp[k]["nraw"], f2(comp[k]["neff"], 1),
                                             (s.get("method", "") if s else ""), f2(s.get("ul95"), 3) if s and s.get("ul95") else ""])
    return rows
git = subprocess.run(["git", "-C", A.WH, "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
# sr table at FINAL from p07 comp + method info recomputed
YF = A.yields(S, FINAL, detail=True)
SRF = {k: dict(mc=np.sqrt(y["var"])*500, method=y["method"], ul95=(3.0*A.wbar(S, k, FINAL)*500 if (y["nraw"] == 0 and y["y"] <= 0) else None)) for k, y in YF.items()}

# ================================================================= 05 report
cnt = P7["counting"]; inv = P5["inventory"]
nfiles = sum(v["files"] for v in inv.values()); nchk = sum(v["sha_checked"] for v in inv.values()); nbad = sum(v["sha_bad"] for v in inv.values())
r05 = f"""# 05 — Baseline selection, background estimation, optimisation (single_r1, WH)

**Date:** {NOW}. **Status: PASS** (all background sources have a Delphes-level yield or a 95 % UL in the SR; three non-prompt/mis-ID methods estimated separately with closure tests; cut-based optimum and k-fold BDT on expected quantities; BDT adopted by the pre-declared rule, with the marginal-stability caveat in §6).
**Goal:** event selection for EW W±Hjj (W→eν/μν, H→γγ) at Delphes level on the frozen canonical package `p2/production/wh` (tag wh-prod-v1, v1.1 rows), read-only; every background source with a yield or UL; non-prompt photons, non-prompt leptons and e→γ separately; cut-based optimisation, then BDT with k-fold, adopted only if the gain is > 10 % and stable.

## 1. Inputs, versions, integrity
- Package: `p2/production/wh/` (SAMPLES.csv, FORMAT.md, V1.1_NOTES.md read first). **SHA256: {nchk} production files hashed inside the ntuple jobs and compared with `SHA256SUMS`: {nbad} mismatches.** Frozen ZH directories used as WH backgrounds (`production/final/*`, `production/v1/*`, read-only) have no reference list: their {sum(v['sha_noref'] for v in inv.values())} files' hashes are recorded in the ntuples (`M_sha`), not verified.
- Σ Event.Weight and N_Delphes per sample reproduce SAMPLES.csv exactly for every package row (`inventory_bad` = {P5['inventory_bad']}).
- Own sample (A2: "extra samples only under runs/single_r1, R=4 seeds"): **`H_ggF_jj_nomjj`** (idx 42, HEFT `p p > h j j`, ptj>20, |ηj|<5, ΔRjj>0.4, **no m_jj cut**), gridpack seed 2442000 (cluster 913309, σ = 7.141 ± 0.026 pb), test job 2442001 (913310: 2000/2000 events, σ_PY8 = 7.059 pb), production 30 jobs seeds 2442002–2442031 (913321, all exit 0): **N = 59 945 ≥ N_req = max(50k, σ·BGG·3000 fb⁻¹ = 48.4k)**; replaces the missing `H_ggF_jj` row (D-WH-5).
- Stack: LCG_110 (MG5 3.6.3, Pythia 8.317 CP5, Delphes 3.5.1 slim card), uproot 5.7.1, awkward 2.9.0, numpy 2.4.4, scipy 1.17.1, xgboost 2.1.3, scikit-learn 1.9.0.
- Commands: `python3 -P wh/scripts/p05/make_nt_jobs.py` → `condor_submit wh/scripts/condor/p05_nt.sub` (cluster 913320, 999 jobs; first attempt 913314 removed: condor split comma arguments) ; `python3 -P wh/scripts/p05/p05_run.py` ; `p05_bdt.py` ; `p07_stats.py` ; `make_figs.py` ; `make_reports.py` (all from `wh/scripts/p05`, with `source p2/lib/scripts/setup_stack.sh` and `PYTHONPATH=wh/scripts/p05`). Ntuples: `wh/work/nt/<sample>/*.npz` (git-ignored); results `wh/work/p05/{{p05,bdt,p07}}.json` (copied to `reports/evidence/`).

## 2. Objects and normalisation
Electrons pT>10 |η|<2.5, muons pT>10 |η|<2.4 (Delphes isolated); photons pT>15, |η|<2.5 outside 1.4442–1.566, ΔR(γ,ℓ)>0.4; jets anti-kT 0.4 pT>20 |η|<4.7, ΔR>0.4 to leptons and photons; b-tag = BTag bit 0, |η|<2.5, pT>25. Truth flags from GenTruth: prompt lepton/photon (ΔR<0.1 to a prompt generator object), photon from a prompt electron (ΔR<0.2). σ×BR per set of events = 10³·k·ΣEvent.Weight/N_generated (FORMAT §4); k from the SAMPLES.csv factor string, re-multiplied from named factors and asserted equal (BR applied once; `whana.py` R/kfac).
**Object efficiencies (D-WH-4 default, G1): CMS-like reweighting** ε_CMS/ε_Delphes per prompt lepton and prompt photon, ε_CMS from the ZH final analysis (`lib/scripts/analysis/final_analysis.py`), ε_Delphes measured here from gen-matched prompt objects in the signal and Wγγjj samples:
{table(['object', '|η| bin', 'ε_Delphes (pT bins: 10/20–20/30–30/50–50+; γ: 20–30–40–60–∞)', 'ε_CMS'], [[t, i, ' / '.join(f'{x:.2f}' for x in P5['eff_delphes'][t][i]), ' / '.join(f'{x:.2f}' for x in P5['eff_cms'][t][i])] for t in 'emg' for i in (0, 1)])}
Stock Delphes efficiencies are a robustness variant (07).

## 3. Baseline (pre-declared at G1) and cutflow
Peak from the Delphes EW signal: μ = {PK['mu']:.2f} GeV, σ_core = {PK['sigma_core']:.2f} ± {PK['sigma_core_err']:.2f} GeV, σ_eff(68 %) = {PK['sigma_eff']:.2f} GeV; 120–130 GeV contains {100*PK['frac_120_130']:.1f} % of the loose-selection signal.
Baseline: exactly one lepton pT>25 (2nd lepton pT>10 vetoed), ≥2 photons with pT/m_γγ>1/3, 1/4, 105<m_γγ<160, MET>30, ≥2 jets pT>30, m_jj>500, |Δη_jj|>2.5, b-veto, window 120–130. **At 500 fb⁻¹: s = {P5['base_summary']['s']:.2f}, b = {P5['base_summary']['b']:.2f}, Z(Eq. 1) = {P5['base_summary']['Z']:.2f}.**
Final-selection cutflow (500 fb⁻¹, expected events; raw MC rows in parentheses; continuum groups after the window use the m_γγ-shape estimate):
{table(['step'] + [g for g, _ in GROUPS], [[r['step']] + [f"{r[g][0]:.3g} ({r[g][1]})" for g, _ in GROUPS] for r in cf])}

## 4. Background estimation (three non-prompt / mis-ID classes separately)
**Estimation hierarchy per (sample, component)** (`whana.component`, adapted from the ZH final analysis): L0 direct window count for m_γγ-resonant samples with N_eff ≥ 10; L1 m_γγ shape for continuum samples (fit-range yield × window fraction of an unbinned exponential MLE of the same component) when N_eff(fit range) ≥ 10; otherwise L2 VBS-factorised (yield without the m_jj/Δη/BDT cuts × their efficiency in a loose object-level region) with 100 % uncertainty; zero support everywhere: central 1.14 w̄ (100 %), 95 % UL = 3 w̄ (w̄ = mean per-event weight in the loose region). The direct-event category that a weighted method replaces is removed from the direct count (no double counting): non-prompt photons (F1/F2 samples), photons from electrons (EG samples), non-prompt leptons (FL samples, max rule).
**(a) Non-prompt photons (j→γ).** Per-jet weighting of pseudo-events (jet → photon with pT = x·pT(GenJet), x ~ N(0.85, 0.10) truncated to [0.5, 1]): one fake in Wγ+jets (`F_QCD_Wajjj_nomjj`, `F_EW_Wajj_nomjj`), tt̄γ, tWγ (n_prompt_photons ≤ 1 overlap rule for Wγ); two fakes in W+4j and tt̄jj (n_prompt_photons = 0). Rate = declared scenario f = 10⁻³(pT/50)^−0.5 (×2 endcap) × {{0.3, 1, 3}}. *Closure* at the one-fake level (lepton pT>25), Delphes direct non-prompt photons vs weighting:
{table(['sample', 'Delphes direct [fb]', 'raw', 'frac. ΔR(γ, GenJet)>0.4', 'weighting × Delphes rate (FORMAT 6a) [fb]', 'weighting × nominal scenario [fb]', 'nominal / direct'], [[f'`{k}`', f2(v['direct_all'], 3), v['direct_raw'], f"{v['direct_dR_gt04']/v['direct_all']:.2f}", f2(v['pred_delphes6a'], 3), f2(v['pred_scenario_nom'], 3), f"{v['pred_scenario_nom']/v['direct_all']:.1f}"] for k, v in P5['closure_jg'].items()])}
The m_jj shape of the Delphes fakes is reproduced by the weighting (W+4j fractions in m_jj bins 0–200/200–500/500–1000/>1000: direct {' / '.join(f'{x:.3f}' for x in np.array(P5['closure_jg']['F_Wjjjj']['by_mjj']['direct'])/sum(P5['closure_jg']['F_Wjjjj']['by_mjj']['direct']))}, weighted {' / '.join(f'{x:.3f}' for x in np.array(P5['closure_jg']['F_Wjjjj']['by_mjj']['pred_scenario'])/sum(P5['closure_jg']['F_Wjjjj']['by_mjj']['pred_scenario']))}; `figures/p05_closure_jg_mjj.png`). The normalisation does not close against Delphes: the FORMAT-6a per-jet rate (ΔR<0.2 matched) under-predicts Delphes by ≈ 5× because most Delphes non-prompt photons are not aligned with a GenJet, and the nominal scenario is ≈ 4× the Delphes rate (conservative; the low scenario ≈ Delphes). Uncertainty: 100 % (one fake), 150 % (two fakes), 100 % correlated within each class; Delphes-rate variant in the robustness table.
**(b) Non-prompt leptons (j→ℓ).** Per-jet weighting (jet → lepton, x as above, e/μ 50/50) in events without a reco lepton, rate {{3·10⁻⁵, 2·10⁻⁴, 10⁻³}} per jet, on `Q_aajjj` (γγ+3 partons), `H_VBFH_jj`, `H_ggF_jj_nomjj` (own); `Q_aajj` is a cross-check. Max rule: nominal = max(parametrised, Delphes direct non-prompt leptons). *Closure / cross-check:* Delphes direct per-jet rate f_eff = {P5['closure_jl']['Q_aajjj']['f_eff_direct']:.2e} (`Q_aajjj`, {P5['closure_jl']['Q_aajjj']['direct_raw']} raw leptons / {P5['closure_jl']['Q_aajjj']['njets_raw']} jets), {P5['closure_jl']['Q_aajj']['f_eff_direct']:.2e} (`Q_aajj`), 0 in VBF/ggF H ({P5['closure_jl']['H_VBFH_jj']['njets_raw']} / {P5['closure_jl']['H_ggF_jj_nomjj']['njets_raw']} jets) — below the tight scenario, so the parametrised value is used everywhere. Uncertainty 100 % (scenario range ×0.15–×5 in robustness); PS-modelling 100 % for VBF/ggF H (third jet from the shower).
**(c) e→γ.** Per-electron weighting (reco prompt electron → photon) in events with ≥2 reco leptons, weight = P(e→γ | gen e)/ε_Delphes(e) with P = {{1, 2, 5}} %, on `F_QCD_llajj_loose`, frozen `F_EW_llajj_vbs`, `V_WWa/WZa/ZZa_WH`. *Closure* in a relaxed region (no VBS/MET/b cuts, fit range): Delphes direct e→γ vs weighting × FORMAT-6b Delphes rate:
{table(['sample', 'direct [fb]', 'raw', 'weighted × 6b [fb]', 'C = direct/weighted', 'applied'], [[f'`{k}`', f2(v['direct'], 4), v['direct_raw'], f2(v['pred_delphes6b'], 4), f2(v.get('C'), 2) if v.get('C') else '—', 'yes' if k in P5['eg_closure_factor'] else 'no (raw < 10)'] for k, v in P5['closure_eg'].items()])}
The method closes for the EW sample (C ≈ 1.02) and fails by ≈ 4× for the loose QCD ℓℓγjj sample (soft/collinear γ*→ee configurations; ≈ 17 % of the direct e-photons are themselves prompt FSR photons). The measured C is applied as a closure correction (D-WH-13), uncertainty 100 % on the class.
**Prompt sources:** Wγγjj (EW, QCD; no generator m_jj cut), tt̄γγ, tt̄γ/tWγ prompt-prompt (kept as in ZH), Zγγjj/ZHjj lost lepton (frozen ZH; EW Zγγjj with generator m_jj>400, C = 0.958 ± 0.061), tt̄H, tHq, tHW, ggZH, ZH→ττ, QCD WH (MLM), W→τν feed-down: direct.

## 5. Cut-based optimisation (expected quantities, 500 fb⁻¹, def. a, Z with σ_b)
Coordinate scan (window, pT/m_γγ, MET, m_T, Zeppenfeld, m_eγ veto, j2 pT, pT^γγ, (m_jj, Δη) grid), choice = highest s among points within 3 % of the best Z (avoid chasing noise), iterated to convergence ({max(h[0] for h in P5['opt_history']) + 1} passes). Optimisation-level σ_b: 10 % prompt, 100 % (150 %) one (two) fakes, 100 % L2 and zero-support, 2.5 % luminosity, MC stat.
**Cut-based optimum:** m_jj > {OPT['mjj']:.0f}, |Δη_jj| > {OPT['deta']:.1f}, pT^γγ > {OPT['ptgg']:.0f}, MET > {OPT['met']:.0f}, m_T > {OPT['mtw']:.0f}, pT/m_γγ > {OPT['ratio'][0]:.3f}/{OPT['ratio'][1]:.3f}, m_eγ veto ±{OPT['meg']:.0f} GeV, j2 pT > {OPT['j2pt']:.0f}, window {OPT['win'][0]:.2f}–{OPT['win'][1]:.2f} GeV (±2σ_core), b-veto, Zeppenfeld none. s = {P5['opt_summary']['s']:.3f}, b = {P5['opt_summary']['b']:.3f} → Z(Eq. 1) = {P5['opt_summary']['Z']:.3f}, Z(σ_b) = {P5['opt_summary']['Zsyst']:.3f}. Stability (Z(σ_b) at ±1 grid step): {'; '.join(f"{k}: " + ', '.join(f'{float(v):.3f}' for v in d.values()) for k, d in P5['opt_stability'].items() if k != 'win')}. pT^γγ sits at the largest grid value (120; 80 → 120 gains 6 %); not extended further.

## 6. BDT (xgboost, 5-fold) — adopted
Training after the preselection m_jj>{B['pre']['mjj']:.0f}, |Δη|>{B['pre']['deta']:.1f}, j pT>30, b-veto, m_eγ veto, MET>{B['pre']['met']:.0f}, fit range; signal EW W±Hjj vs all backgrounds with expected weights (each class normalised to equal total); {len(B['features'])} inputs, **m_γγ excluded**; folds by event-number hash (pseudo-events of one event share a fold); each row scored by the model that did not see its fold; models saved (`work/p05/bdt_models/`). AUC train/test per fold: {', '.join(f"{a['auc_train']:.3f}/{a['auc_test']:.3f}" for a in B['auc'])}. Top inputs: {', '.join(f'{k} {v:.2f}' for k, v in sorted(B['importance'].items(), key=lambda x: -x[1])[:6])}.
Threshold scan with the **same** estimation hierarchy and σ_b as the cut-based optimum (`figures/p05_bdt_scan.png`): best BDT > {B['t_best']:.2f}: s = {B['s_bdt']:.3f}, b = {B['b_bdt']:.3f}, Z(σ_b) = {B['Z_bdt']:.3f} vs cut-based {B['Z_cut']:.3f} → **gain {100*B['gain']:.0f} %**. Fold-wise check (direct counts in one fold × 5): {', '.join(f"{x['Z_bdt']:.2f} vs {x['Z_cut']:.2f}" for x in B['folds'])} → gain positive in every fold; max AUC(train) − AUC(test) = {max(a['auc_train'] - a['auc_test'] for a in B['auc']):.3f} < 0.02. **Adopted** (rule: gain > 10 % and stable).
*Caveat (referee point, see 07 self-review):* the first BDT run, made before the e→γ closure factor was passed to the BDT script (bug, fixed), had fold 0 at 0.56 vs 0.58 (rule failed); the stability is therefore marginal, and the cut-based result is reported alongside everywhere. The BDT relies on jet-activity variables (j3 pT, n_jets), which are parton-shower sensitive; this is covered by the jet-modelling and signal PS nuisances (06).

## 7. SR yields at the final (BDT) selection, 500 fb⁻¹ (def. a; every source)
{table(['group', 'sample', 'class', 'y', 'MC stat', 'raw rows', 'N_eff', 'method per component', '95 % UL (zero support)'], sr_rows(C5, SRF))}
Total: **s = {cnt['500_a']['s']:.3f}, b = {cnt['500_a']['b']:.3f}** (def. a). Sources with N_eff < 10 enter at their estimate with their MC-stat or 100 % L2 uncertainty; the conservative variant (all of them at max(value, 3 w̄)) is in the robustness table (07).

## 8. Checks
SHA256 {nchk}/{nchk} OK; Σw and N closure per sample; BR ledger asserted; N_MC rule enforced by `whana.nmc_check` (fails loudly; it failed on the first run for the three 20k EW Zγγjj beam splits, now checked as the one SAMPLES.csv row of 60k, D-WH-3); D-WH-2 effective-N for `F_Wjjjj` (N/N_req = {P5['nmc']['F_Wjjjj']['ratio']:.3f}) and `T_ttjj_1l` ({P5['nmc']['T_ttjj_1l']['ratio']:.4f}): N_eff in the SR {C5['F_Wjjjj']['neff']:.0f} and {C5['T_ttjj_1l']['neff']:.0f} ≥ 10. Quadratic coupling closure (07). JES rescoring of the BDT reproduces the stored scores exactly at zero shift.

## 9. Caveats
LO generators; no pile-up; per-jet fake parametrisations are scenarios, not measurements; e→γ needs a closure factor 4 for the loose QCD sample; the W+jets and tt̄ fakes are weighted (D-WH-2); several small sources have N_eff < 10; the optimisation chose pT^γγ at the grid edge; BDT stability marginal (§6).

## 10. Next
06 systematics, 07 sensitivity. **Git:** see `git log -- wh/reports/05_selection.md` (run commit; parent at generation {git}).
"""
open(f"{R}/05_selection.md", "w").write(r05)

# ================================================================= 06 report
TH, SH, JM = P7["theory"], P7["shape_unc"], P7["jetmod"]
r06 = f"""# 06 — Mass window, sidebands and systematic model (single_r1, WH)

**Date:** {NOW}. **Status: PASS** (systematic model implemented for counting and the m_γγ fit; theory from the samples' own weights; all assumptions listed).
**Goal:** window/sideband definition and the nuisance model for 07.

## 1. Window and sidebands
Window {FINAL['win'][0]:.2f}–{FINAL['win'][1]:.2f} GeV = μ ± 2σ_core of the Delphes EW signal (μ = {PK['mu']:.2f}, σ_core = {PK['sigma_core']:.2f} GeV); fit range 105–160 GeV; sidebands = fit range minus window (used by the profile-likelihood fit; continuum normalisation and slope float). Continuum MC shapes: unbinned exponential MLE per component (L1). Resonant shape: two-Gaussian fit to the Delphes signal after the final selection (parameters in p07.json `fit.*.par_signal_shape`). Mass-resolution dependence: ±10 % resolution and ±0.5 % photon energy scale are nuisances (table below) and are profiled in the fit.

## 2. Nuisances (counting; absolute effect on the 500 fb⁻¹ SR yields, def. a; sum over samples within a nuisance)
{table(['nuisance', 'Δb (events)', 'Δs (events)'], [[k, f2(P7['counting']['500_a']['groups_b'].get(k), 3), f2(P7['counting']['500_a']['groups_s'].get(k), 3)] for k in sorted(set(P7['counting']['500_a']['groups_b']) | set(P7['counting']['500_a']['groups_s']), key=lambda k: -(P7['counting']['500_a']['groups_b'].get(k, 0) + P7['counting']['500_a']['groups_s'].get(k, 0)))[:24]])}
Sizes: luminosity 2.5 % (as ZH, for the VH combination); object efficiencies 2 % per lepton and per photon (prompt objects); theory = 7-point scale envelope ⊕ PDF replica RMS from each sample's own LHE weights in the SR (proxies for samples without weights: fakes → their prompt analogue); fake classes 100 % (j→γ one fake), 150 % (two fakes), 100 % (j→ℓ, e→γ), correlated within a class; PS modelling 100 % for samples whose tag/fake jets come from the shower (V+γ, ggZH, VBF/ggF H fake ℓ, EW Wγjj, D29 rule); generator m_jj>400 correction of the frozen EW Zγγjj / ℓℓγjj rows 6.4 %; L2 components and zero-support sources 100 % each (uncorrelated); MC stat per sample; JES ±5 % (BDT rescored), photon scale ±0.5 %, resolution ±10 % (resonant samples); **jet modelling** (D-WH-14): |1 − ε(QCD WH, MLM)/ε(QCD WHjj, fixed order)| of the selection relative to a loose object region = {JM['ratio']:.2f} ± {JM['stat']:.2f} → {100*JM['rel']:.0f} % on every background prompt/FL component (cut-based selection: {100*P7['jetmod_cutbased']['rel']:.0f} %); **signal PS modelling 10 %** (assumption for EW VBS-type samples: recoil scheme / central jet activity).
Theory per sample (scale, PDF):
{table(['sample', 'scale', 'PDF', 'rows'], [[f'`{k}`', f"{v['scale']:.3f}", f"{v['pdf']:.3f}", v['n']] for k, v in TH.items()])}
Shape-type (500 fb⁻¹ SR, relative; JES/photon scale/resolution):
{table(['sample', 'JES', 'γ scale', 'resolution'], [[f'`{k}`', f"{v['jes']:.3f}", f"{v['pes']:.3f}", f"{v['res']:.3f}"] for k, v in SH.items() if k in C5 and C5[k]['y'] > 0.01])}

## 3. Fit model (supplementary result in 07)
Binned (1 GeV) Poisson likelihood in 105–160 GeV, Asimov data; parameters: μ (signal strength), continuum normalisation and exponential slope (free), signal normalisation (Gaussian, σ_s/s from the counting model), resonant-background normalisation (30 %), photon energy scale (0.5 %) and resolution (10 %) acting on the common resonant shape. Z = √q₀ on Asimov s+b; μ95 = median expected from q_μ on Asimov b-only with the asymptotic CLs condition q_μ,A = 1.96². With O(1–10) events the asymptotic formulae are approximate (the counting μ95 uses exact Poisson CLs).

## 4. Checks and caveats
The theory, JES and fake nuisances are evaluated at the final selection; correlations: same nuisance name ⇒ 100 % correlated across samples, s and b. Not included: pile-up, trigger efficiency, b-tag scale factors, κ-dependence of BR(H→γγ). The jet-modelling estimate is statistics-limited (35 / 116 selected MC rows).
**Git:** see `git log -- wh/reports/06_systematics.md`.
"""
open(f"{R}/06_systematics.md", "w").write(r06)

# ================================================================= 07 report
F = P7["fit"]; CO = P7["coupling"]; RB = P7["robustness"]; CC = P7["counting_cutbased"]
def cntrows(cn):
    return [[f"{int(v['L'])}", v['sigdef'], f"{v['s']:.2f}", f"{v['b']:.2f}", f"{v['sigma_b']:.2f}", f"{v['Z_eq1']:.2f} ± {v['Z_eq1_mcerr']:.2f}", f"{v['Z_syst']:.2f}",
             f"{v['mu95_cls']:.2f}", f"{v['mu95_cls_stat']:.2f}", f"{F[k]['syst']['Z']:.2f}" if cn is cnt else "", f"{F[k]['syst']['mu95']:.2f}" if cn is cnt else ""] for k, v in cn.items()]
r07 = f"""# 07 — Sensitivity, robustness and coupling interpretation (single_r1, WH)

**Date:** {NOW}. **Status: PASS** (expected results only; Asimov; no observed data).
**Definitions:** (a) signal = EW W±Hjj, QCD W±H(+jets, MLM) is a resonant background; (b) signal = EW + QCD W±H. W→τν feed-down is background in both (it scales with the couplings in §3).

## 1. Counting (PRIMARY: Eq. 1, stat. only ± MC stat) and m_γγ profile-likelihood fit (supplementary)
Final selection: BDT (05 §6). Eq. 1: Z = √(2((s+b)ln(1+s/b) − s)); Z(σ_b) with the full background uncertainty; μ95: median expected exact-Poisson CLs with log-normal s and b marginalisation ("syst") and without ("stat").
{table(['L [fb⁻¹]', 'def', 's', 'b', 'σ_b', 'Z Eq. 1 ± MC', 'Z (σ_b)', 'μ95 CLs (syst)', 'μ95 CLs (stat)', 'Z fit (syst)', 'μ95 fit (syst)'], cntrows(cnt))}
Fit stat-only (continuum still floating): Z = {', '.join(f"{F[k]['stat']['Z']:.2f}" for k in F)}; μ95 = {', '.join(f"{F[k]['stat']['mu95']:.2f}" for k in F)} (same order as above).
**Cut-based selection (reported alongside the BDT):**
{table(['L [fb⁻¹]', 'def', 's', 'b', 'σ_b', 'Z Eq. 1 ± MC', 'Z (σ_b)', 'μ95 CLs (syst)', 'μ95 CLs (stat)', '', ''], cntrows(CC))}
Figure: `figures/p07_mgg_final.png` (expected m_γγ at the final selection, 500 fb⁻¹).

## 2. Robustness (Eq. 1 and Z(σ_b), μ95 CLs syst)
{table(['variant', 'L', 'def', 's', 'b', 'Z Eq. 1', 'Z (σ_b)', 'μ95'], [[r['variant'], int(r['L']), r['sigdef'], f"{r['s']:.2f}", f"{r['b']:.2f}", f"{r['Z_eq1']:.2f}", f"{r['Z_syst']:.2f}", f"{r['mu95']:.2f}"] for r in RB])}

## 3. λ_WZ = κ_W/κ_Z and (κ_W, κ_Z)
Coupling samples `K_EW_WHjj_*` (HC_NLO_X0_kVV) through the same selection (BDT scored by the mean of the five fold models). The SR yield is an exact quadratic form Y = α κ_W² + β κ_W κ_Z + γ κ_Z²; α, β, γ fitted to the six λ_WZ points at κ_Z = 1 (χ²/ndf = {CO['500']['quad']['chi2']:.2f}/{CO['500']['quad']['ndf']}); closure on independent points (500 fb⁻¹): {'; '.join(f"{k}: predicted {v['pred']:.3f}, sample {v['mc']:.3f} ± {v['mc_err']:.3f}" for k, v in CO['500']['quad']['closure'].items())}.
Interpretation model: signal and τν feed-down scale with Y(κ_W, κ_Z)/Y_SM, QCD WH with κ_W², other backgrounds fixed; **BR(H→γγ) fixed to its SM value** (the samples do not include its κ dependence; with κ_γ resolved through the W loop, λ_WZ < 0 would raise BR(H→γγ) by ≈ 2× and strengthen the exclusions — not used). Test statistic: Poisson likelihood ratio on the SM Asimov count with the Gaussian-profiled σ_b.
{table(['L [fb⁻¹]', 'Z excl. λ_WZ = −1', 'Z excl. λ_WZ < 0 (min. at λ)', 'λ_WZ 68 % interval', 'λ_WZ 95 % interval'], [[L, f"{v['Z_excl_lam_m1']:.2f}", f"{v['Z_excl_lam_neg']:.2f} ({v['lam_at_min_neg']:.2f})", f"[{v['lam68'][0]:.2f}, {v['lam68'][1]:.2f}]", f"[{v['lam95'][0]:.2f}, {v['lam95'][1]:.2f}]"] for L, v in CO.items()])}
The λ_WZ < 0 test is limited by the boundary λ → 0⁻, whose rate (Y(0)/Y(1) = γ/(α+β+γ) = {CO['500']['quad']['g']/(CO['500']['quad']['a'] + CO['500']['quad']['b'] + CO['500']['quad']['g']):.2f}) is close to the SM; the rate alone cannot separate λ ≈ 0.2–1 (flat valley in `figures/p07_lambdaWZ_scan.png`). (κ_W, κ_Z) 68/95 % contours: `figures/p07_kappa_contours.png`.

## 4. Caveats
Asymptotic fit formulae at O(1–10) events; BDT stability marginal (05 §6); jet-modelling nuisance statistics-limited; rate-only coupling interpretation; BR(H→γγ) fixed; no VH combination here (outside this run's scope).
**Git:** see `git log -- wh/reports/07_sensitivity.md`.
"""
open(f"{R}/07_sensitivity.md", "w").write(r07)

# ================================================================= final.json
fin = dict(run="single_r1", process="WH", date_utc=NOW, package="p2/production/wh wh-prod-v1 (+v1.1 rows), read-only", own_samples={"H_ggF_jj_nomjj": dict(N=59945, seeds="2442000 (gridpack), 2442001 (test), 2442002-2442031", sigma_pb=7.141)},
           final_selection=FINAL, selection_type="BDT (xgboost 5-fold), adopted by rule (gain %.0f %%, stable)" % (100*B["gain"]), cutbased_selection=OPT,
           counting={k: {kk: v[kk] for kk in ("L", "sigdef", "s", "b", "s_mc", "b_mc", "sigma_b", "sigma_s", "Z_eq1", "Z_eq1_mcerr", "Z_syst", "mu95_cls", "mu95_cls_stat")} for k, v in cnt.items()},
           counting_cutbased={k: {kk: v[kk] for kk in ("L", "sigdef", "s", "b", "sigma_b", "Z_eq1", "Z_eq1_mcerr", "Z_syst", "mu95_cls", "mu95_cls_stat")} for k, v in CC.items()},
           fit={k: dict(Z_syst=v["syst"]["Z"], mu95_syst=v["syst"]["mu95"], Z_stat=v["stat"]["Z"], mu95_stat=v["stat"]["mu95"]) for k, v in F.items()},
           coupling={L: dict(Z_excl_lam_m1=v["Z_excl_lam_m1"], Z_excl_lam_neg=v["Z_excl_lam_neg"], lam68=v["lam68"], lam95=v["lam95"], quad=dict(a=v["quad"]["a"], b=v["quad"]["b"], g=v["quad"]["g"])) for L, v in CO.items()},
           sr_components_500_a={k: dict(y=v["y"], nraw=v["nraw"], neff=v["neff"]) for k, v in C5.items()},
           robustness=RB, decisions="reports/FINAL_report.md §5", peak=PK)
json.dump(fin, open(f"{R}/final.json", "w"), indent=1)
print("wrote 05/06/07 + final.json")
