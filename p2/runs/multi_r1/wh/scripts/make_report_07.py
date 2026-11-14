#!/usr/bin/env python3
"""Writes reports/06_systematics.md and reports/07_sensitivity.md from work/stat/*.json (all expected-only)."""
import json, os, datetime, numpy as np, sys
import sys as _s0, os as _o0; _s0.path.insert(0, _o0.path.dirname(_o0.path.abspath(__file__)))
from pin import COMMIT
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
WH = "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh"; S = f"{WH}/work/stat"
def _p(n): return next((f"{S}/{n}{x}.json" for x in ("_v12", "_v11", "") if os.path.exists(f"{S}/{n}{x}.json")), f"{S}/{n}.json")   # v1.1 results preferred (loose eFake QCD sample); rank has no v1.1 rerun
J = lambda n: json.load(open(_p(n))) if os.path.exists(_p(n)) else None
now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M"); L = [500, 1000, 3000]
c = J("counting"); sel = json.load(open(f"{WH}/work/sel/selection_final.json"))
# ---------------- 06
A = []; a = A.append
a(f"""# 06 Systematic and mass-window models (executor-wh FINAL, block 3)
Date UTC: {now}. Status: **PASS for verification** (expected results only; no data). Analysis commit: {COMMIT}.
## Goal
Fix the signal-window / m_gg model and the nuisance model before the sensitivity numbers (07): window and resolution dependence, the pre-declared nuisance list of 05a v2.1 (sec. 'nuisance list') and 05 addendum, Barlow-Beeston, with/without MC stat.
## Inputs / commands
Cut-based PRIMARY selection (05_selection.md: mjj>600, |deta|>4.0, pT(gg)>75, rest baseline), table work/sel/table_v11.npz (05a v2.1 nominal weights with the v1.1 loose eFake sample; the v2.1 table.npz only for the robustness row and the ranking). Code: scripts/stat_lib.py (model), stat_run.py (tasks), condor job_stat.sh (clusters 899917 removed after the Z0 factor-2 bug and the unsmoothed-template bias, 899918 results, 899919 ranking; schedd bigbird103). pyhf 0.7.6 (asymptotic q0 / q_mu~), seeds: none (Asimov, no toys).
## 1. m_gg model
Signal resolution: sigma_eff = 2.10 GeV, mean 125.06 GeV (selected signal). Fit range 100-180 GeV in 40 bins of 2 GeV. Window of the cut-based counting selection: |m_gg-125|<3.5 GeV (declared grid {{2.5,3.5,5.0}}). Sidebands (outside the window) constrain the background in the fit; no data are used.
**Background templates are smoothed (bias fix):** an Asimov dataset built from the unsmoothed MC in 2 GeV bins is biased high (bins with a low-fluctuating b inflate Z; the first PL numbers, Z0 about 0.66, were of this kind and are discarded, files work/stat_unsmoothed/). Non-resonant groups are replaced by exp(slope*(m-140 GeV)) x group integral (slope fitted per group when N_eff>=20, else the total-background slope); resonant groups (signal, tau feed-down, QCD WH, other Higgs) are kept raw. Barlow-Beeston-lite errors of smoothed groups = sqrt(h_smooth * wbar).
Mass scale/resolution: photon energy scale 0.5 % (histosys on the signal), resolution +-10 % (histosys): both ASSUMED (Delphes has no scale data); resolution dependence is scanned in 07 sec. 6.
## 2. Nuisance model (pyhf modifiers, all Gaussian-constrained unless stated)
| nuisance | groups | hi / lo (relative) | origin | basis |
|---|---|---|---|---|
| lumi | all | +-2.5 % | no luminosity measurement in the study | ASSUMPTION |
| pheff | all with real photons | +-4 % (two real photons), +-2 % (one) | 2 % per photon, Delphes has no scale factors | ASSUMPTION |
| lepeff | real-lepton groups | +-1 % | no scale factors in Delphes | ASSUMPTION |
| tau_r | W/Z groups | (1+2 r_tau)/(1+r_tau), 1/(1+r_tau), r_tau = 0.083 | D9 human-set +-100 % of the MC-measured tau uplift | human rule (judgement on the size) |
| scale_<group> | per group | 7-point QCD scale envelope of the 05a VBS-region sample envelopes (signal: selection-level from the LHE weights) | LHE weights | MC-derived (LO only) |
| pdf_sig | signal | rms of 100 NNPDF3.1 replicas at the selection | LHE weights | MC-derived |
| ps_qcd | B_QCD_Waajj, F_QCD_Wajjj/T_tta/T_tWa, ZH_Zaajj_QCD, and (v1.1) the loose eFake QCD part | 1.45 / 0.55 (correlated) | 04:136 declared 100 % PS-jet fraction (twin loss fractions 15-45 %) | judgement |
| C_eFake | eFake QCD part (v2.1 model only; NOT used in v1.1: replaced by ps_qcd on the loose sample) | 1.464 / 0.536 | C range [1, 2.732] about 1.866 (twin ratio with a full-difference systematic) | MC-derived range, judgement on the width |
| C_EW | eFake EW part | +-2.5 % | EW twin loss fraction 2.4 +- 0.3 % | MC-derived / judgement |
| C_ZaaEW | other lost-lepton (Zaajj EW, V_*) | +-6.4 % | 05a item 6 declared (twin statistics 0.061/0.958; reconciled in v3: v1/v2 of this block used 2.5 %) | MC-derived |
| cov_eFake | eFake QCD lost-lepton part (v2.1 model only; NOT used in v1.1) | one-sided +105 % (theta in [0,3], half-normal) | 04:139 sigma ratio 1.679/0.818 pb | MC-derived bound, pessimistic by construction |
| fakerate | fake photons | one-fake +-20 %, two-fake -36 %/+44 % (c^2) | D39 floor (CMS syst/yield 19.6 %, record verified but no comparable phase space) | judgement |
| nonclosure | one-fake | one-sided -60 % (theta in [0,1.6]) | direct/FF closure 0.39-0.41 (3-6 raw events) | MC-derived, low statistics |
| fake2_scen | two-fake | x9 / x0.09 | D27 per-photon x3 / x0.3 scenarios | judgement (human D27) |
| npl_norm | light-misID | x3 / x0.3 | D35/D36 envelope (human question a); muon rate is a placeholder (D40) | judgement |
| hf_var | heavy-flavour factorised | x2 / ~0 | +-100 % on a factorised estimate with 5 raw rows | judgement |
| phscale, phres | signal | histosys, 0.5 % / 10 % | no photon calibration data | ASSUMPTION |
| mcstat | all | per-bin Barlow-Beeston-lite (staterror) | MC statistics | MC-derived |
Every nuisance not derived from MC or data is an ASSUMPTION or a judgement (stated in the last column); the combination of ps_qcd, C_eFake, cov_eFake, fakerate, nonclosure, npl_norm and hf_var constrains nothing from data (no data exist) and only widens the expected profile.
D29 100 % PS on V_WWa/WZa/ZZa (05a item 4): the three rows have ZERO MC rows at the selection, so the nuisance would act on nothing and is not added (logged deviation; the UL variant at PEAK, 0.65 events, is in sec. 5).
(The tables of this report are the v1.1 model: the v2.1-only nuisances are listed for the robustness row of sec. 5.)\nNot in the fit (variants in 07): zero-support ULs (V_* 0.65, non-prompt 0.76, direct-fake variation 0.97 events at PEAK, 05a), class lower/upper bounds, D29 PS 100 % on V_* (zero events at the selection).
Correlations: nuisances with the same name act coherently on all listed groups (e.g. tau_r, ps_qcd, fakerate). Correlation with ZH (combination) is handled in the combination block.""")
r = J("rank")
if r:
    a("\n## 3. Nuisance impact (500 fb^-1, def. a; one family removed at a time; computed with the v2.1 table before the v1.1 replacement, condor 899923; no nuisance moves Z0 by more than 0.8 % or mu95 by more than 1.2 %: the expected profile is dominated by the signal/background statistics and MC statistics, not by these systematics; the ASSUMPTION nuisances are therefore not driving the result)\n\n| removed | Z0 | mu95 median |\n|---|---|---|")
    for x in r["rows"]: a(f"| {x['removed']} | {x['Z0']:.4f} | {x['mu95']:.3f} |")
for d in ("a", "b"):
    p = [J(f"pl_{l}_{d}") for l in L]
    if all(p):
        a(f"\n## 4{'a' if d=='a' else 'b'}. With / without systematics and MC stat, signal definition ({d})\n\n| L | variant | expected Z0 | PL asymptotic CLs mu95 (-1s, median, +1s) | n par |\n|---|---|---|---|---|")
        for l, x in zip(L, p):
            for k, v in x.items():
                if isinstance(v, dict) and "Z0" in v: a(f"| {l} | {k} | {v['Z0']:.3f} | {', '.join('%.2f' % z for z in v['mu95_exp'])} | {v['npar']} |")
b = J("bounds")
if b:
    a("\n## 5. Class lower/upper bounds and zero-support variants (def. a)\n\n| variant | L | Z (Eq. 1 window) | Z0 (PL, syst+BB) | PL asymptotic mu95 median (-1s,+1s) |\n|---|---|---|---|---|")
    for x in b["rows"]: a(f"| bounds {x['bounds']} | {x['lumi']:.0f} | {x['Z_eq1']:.3f} | {x['Z0_PL']:.3f} | {('%.2f (%.2f, %.2f)' % (x['mu95_exp'][1], x['mu95_exp'][0], x['mu95_exp'][2])) if x['mu95_exp'] else '-'} |")
    for x in b["ul_variants"]: a(f"| UL variant {x['variant']} (UL {x['UL_events_at_500']:.2f} ev in PEAK, {x['extra_in_window_at_500']:.2f} ev in the +-3.5 GeV window, {x['extra_total_in_range']:.1f} in 100-180 at 500) | {x['lumi']:.0f} | {x['Z_eq1']:.3f} | {x['Z0_PL']:.3f} | - |")
    for l_ in L:
        v1 = json.load(open(f"{S}/pl_{l_}_a.json")) if os.path.exists(f"{S}/pl_{l_}_a.json") else None
        if v1: f1 = v1["full_syst_BB"]; a(f"| ROBUSTNESS v1 model: vbs x C eFake QCD (C_eFake, cov_eFake nuisances), full syst+BB | {l_} | - | {f1['Z0']:.3f} | {f1['mu95_exp'][1]:.2f} ({f1['mu95_exp'][0]:.2f}, {f1['mu95_exp'][2]:.2f}) |")
    gg = J("ggf_variant")
    if gg:
        for r_ in gg["rows"]: a(f"| H_ggF_jj D38 scaled proxy added ({gg['UL_events_in_window_500']:.3f} ev in the window at 500) | {r_['lumi']:.0f} | - | {r_['Z0_with_ggF_UL']:.3f} (PL; nominal {r_['Z0_nominal']:.3f}) | - |")
a("\n## 6. Caveats\nAll nuisance widths marked ASSUMPTION are placeholders; the dominant impacts are in sec. 3. Asymptotic formulas with b of order 0.1 events/bin are approximate; the counting exact-Poisson numbers of 07 are the cross-check. Systematics from the ZH side (combination) are not in this block.\n")
open(f"{WH}/reports/06_systematics.md", "w").write("\n".join(A))
# ---------------- 07
B = []; a = B.append
a(f"""# 07 Sensitivity (executor-wh FINAL, block 3)
Date UTC: {now}. Status: **PASS for verification**; ALL numbers are EXPECTED (Asimov datasets, nominal background model of 05a v2.1 + the v1.1 loose-cut eFake sample, primary = cut-based selection; D44). No claim of a result; a null or sub-1-sigma expectation is stated as such. Analysis commit: {COMMIT}.
## Selection (frozen in 05): mjj>600, |deta_jj|>4.0, pT(gg)>75, MET>30, pT(l)>25, |m_gg-125|<3.5 (counting); MVA alternative not adopted.
## 1. Counting window (Eq. 1, stat only) and exact-Poisson CLs
Window yields at 500 fb^-1: s = {c['window_500']['s']:.3f}, b = {c['window_500']['b']:.3f} +- {c['window_500']['sigma_b_MC']:.3f} (MC stat).
| L [fb^-1] | s | b | Z Eq. 1 | Z (b -MC, b +MC) | exact-Poisson counting CLs mu95 (q16, median, q84) | def (b): s, b, Z, mu95 median |
|---|---|---|---|---|---|---|""")
for l in L:
    x = c[f"L{l}"]; y = c[f"def_b_L{l}"]; m = x["mu95_poisson"]; my = y["mu95_poisson"]
    a(f"| {l} | {x['s']:.3f} | {x['b']:.3f} | {x['Z_eq1']:.3f} | {x['Z_eq1_bMCplus']:.3f}, {x['Z_eq1_bMCminus']:.3f} | {m['q16_low_limit']:.2f}, {m['median']:.2f}, {m['q84_high_limit']:.2f} | {y['s']:.3f}, {y['b']:.3f}, {y['Z_eq1']:.3f}, {my['median']:.2f} |")
a("\nNOT the same quantity as the profile-likelihood mu95 of sec. 2 (asymptotic q~ CLs on the m_gg shape fit, pyhf). The Poisson 'q16/q84' columns are the observed-count quantiles of Poisson(b) mapped to mu95 (discrete).")
a("\n## 2. Profile likelihood (m_gg 100-180 GeV, 40 bins, all nuisances of 06 + Barlow-Beeston)\n\n| L | def | expected Z0 | PL asymptotic (q~) CLs mu95 median (-1s, +1s) | Z0 stat-only | Z0 without MC stat | Z0 MC-stat only |\n|---|---|---|---|---|---|---|")
for d in ("a", "b"):
    for l in L:
        x = J(f"pl_{l}_{d}")
        if x: f = x["full_syst_BB"]; a(f"| {l} | {d} | {f['Z0']:.3f} | {f['mu95_exp'][1]:.2f} ({f['mu95_exp'][0]:.2f}, {f['mu95_exp'][2]:.2f}) | {x['stat_only']['Z0']:.3f} | {x['syst_noMCstat']['Z0']:.3f} | {x['MCstat_only']['Z0']:.3f} |")
a("\nWith/without MC-stat impact on Z0 at 500 fb^-1 and mu95 is in 06 sec. 4: Barlow-Beeston is mandatory (cut-based b N_eff 63 in v1.1, 135 in v2.1).")
for kind, ttl in (("fake", "fake photons (per-photon rate x f; one-fake x f, two-fake x f^2)"), ("npl", "non-prompt leptons (light misID and heavy flavour x f)")):
    for l in (500, 3000):
        d = J(f"d36_{kind}_{l}")
        if d:
            a(f"\n## 3. D36 scan: {ttl}, {l} fb^-1 (def. a, PL with all nuisances)\nD36 range x0.3-x3; f = 10, 30, 100 are BEYOND D36 (robustness only).\n\n| f | Z0 (PL) | mu95 median (-1s, +1s) | Z Eq. 1 counting | b window |\n|---|---|---|---|---|")
            for r in d["scan"]: a(f"| {r['f']}{' (beyond D36)' if r['f'] > 3 else ''} | {r['Z0_PL']:.3f} | {r['mu95_exp'][1]:.2f} ({r['mu95_exp'][0]:.2f}, {r['mu95_exp'][2]:.2f}) | {r['Z_eq1_counting']:.3f} | {r['b_window']:.3f} |")
cp = J("couplings"); cn = J("couplings_nobr"); ck = J("couplings_kzneg")
if cp and ck:
    q = lambda d_, l_, lab="reduced_model": d_["expected_exclusion"][lab]["Z_lam_m1"]
    a(f"""
## 4. Couplings (lambda_WZ = kappa_W/kappa_Z, (kappa_W, kappa_Z)) from the direct samples, expected, SM data (Asimov), asymptotic
**Sign convention (SPEC D46, orchestrator default pending the human).** The signal yield is even under (kW, kZ) -> (-kW, -kZ), so (kW, kZ) = (-1, 1) and (1, -1) are the same point for the VBS yield; they differ only in the H->gamma gamma branching ratio, through the sign of kW*kt in the W-top loop (A_W = -8.32 kW, A_t = +1.84 kt, standard loop functions, e.g. A. Djouadi, Phys. Rept. 457 (2008) 1, hep-ph/0503172; recomputed here at mH = 125 GeV, mW = 80.4, mt = 172.5; YR4 BRs; kb = kt = ktau = kc = 1).
* **PRIMARY (convention-independent): lambda = -1 realised as kZ = -1, kW = +1 (sign carried by kZ, R_BR = 1 at this point): expected exclusion Z = {q(ck, 0):.1f} sigma at 500 fb^-1 (stat-only {ck['expected_exclusion']['stat_only']['Z_lam_m1']:.1f}).**
* kW-sign convention (kW = -1, kZ = +1 = kt): the W-top interference raises BR(gamma gamma) by x2.45 and the expected exclusion is ~6 sigma ({q(cp, 0):.1f} sigma central; 5.1-7.1 under a +-30 % closure variation of the predicted signal), asymptotic. This number needs the convention and the BR modelling: it is NOT the headline.
* Whole lambda<0 region: expected Z = {ck['expected_exclusion']['reduced_model']['Z_lambda_lt0']:.2f} sigma (kZ-sign convention; its closest point is lambda about -0.05, where the signal is similar to the lambda about 0.2 gamma gamma amplitude zero) and {cp['expected_exclusion']['reduced_model']['Z_lambda_lt0']:.2f} sigma (kW-sign convention): robust to the convention; the lambda<0 region cannot be excluded in this channel.
* "R_BR = 1 for all lambda" (the samples with the SM BR only, {cn['expected_exclusion']['reduced_model']['Z_lambda_lt0']:.2f} sigma at lambda=0) is UNPHYSICAL and is not a result: the gamma gamma amplitude and the width depend on kW at every lambda.
Method (scripts/coup_run.py): per-bin quadratic Y_i = alpha_i kW^2 + beta_i kW kZ + gamma_i kZ^2 from the 8 CP-even points (weighted LSQ) x R_BR(kW, kZ). **REDUCED nuisance model** (per-class background normalisations with the 05a class-bound widths, signal theory 5 %, lumi 2.5 % ASSUMPTION, Barlow-Beeston-lite), not the full 06 model: stat-only / MC-stat / reduced differ by <= 2 % in Z; the full-model ranking (06 sec. 3) says no nuisance moves Z0 by more than 0.8 %. Binning chosen before the fit by the expected exclusion of lambda=-1: {cp['binning_chosen']} (edges {cp['binning_choice'][cp['binning_chosen']]['edges']}).
**Other-Higgs backgrounds (12 % of b: QCD WH, ggZH, ttH, tH) are NOT rescaled under the coupling hypotheses; only the signal carries kappa and R_BR.** tHq grows by about x10 at kW*kt < 0; leaving it unscaled is likely conservative for the exclusion of lambda=-1 (more background would lower it) but untested.
**Precision:** these are expected values from the asymptotic formula; the 4 bins hold O(1) events and no toy or exact check of the ~4-6 sigma tail exists. The +-30 % closure variation of the tested signal (Z(lambda=-1) {ck['closure_sensitivity_signal_scale_of_tested_hypothesis']['0.7']['Z_lam_m1']:.1f} / {ck['closure_sensitivity_signal_scale_of_tested_hypothesis']['1.0']['Z_lam_m1']:.1f} / {ck['closure_sensitivity_signal_scale_of_tested_hypothesis']['1.3']['Z_lam_m1']:.1f} for 0.7 / 1.0 / 1.3 in the kZ convention = PRIMARY band; 5.1 / 6.2 / 7.1 in the kW convention) is NOT shown to cover the leave-one-out per-bin pulls (up to 3.3 sigma at lambda = 0 and -0.5); read the numbers to the nearest sigma.""")
    a("\n### (kappa_W, kappa_Z) map (kW-sign convention, reduced model, 500 fb^-1): expected q = Z^2 of excluding the point against the SM data\n")
    m2 = cp["map2d"]; kz = m2["kZ"]; a("| kW \\ kZ | " + " | ".join(f"{z:.2f}" for z in kz) + " |\n|---|" + "---|"*len(kz))
    for ia, kw in enumerate(m2["kW"]): a(f"| {kw:+.1f} | " + " | ".join(f"{(m2['q'][ia][ib])**0.5:.1f}" for ib in range(len(kz))) + " |")
    a("(entries are Z = sqrt(q); the SM point (1, 1) is 0 by construction; |kW| ~ 0.2-0.5 with kZ ~ 1 and the kW<0 sector near kW ~ 0 are not excluded, in line with the lambda<0 result.)")
    a("\nLeave-one-out closure of the per-bin quadratic (LSQ covariance included): totals |pull| <= {:.1f}; per-bin pulls up to {:.1f}.".format(max(abs(r["pull_total"]) for r in cp["closure_loo"]), max(abs(p) for r in cp["closure_loo"] for p in r["pulls_per_bin"])))
    a("\n### D36 scans for the lambda<0 exclusion (reduced coupling model, kW-sign convention)\n\n| kind | f | Z(lambda=-1) | Z(lambda=0) | Z(lambda=0.5) |\n|---|---|---|---|---|")
    for r in cp["d36_lambda"]: a(f"| {r['kind']} | {r['f']}{' (beyond D36)' if r['beyond_D36'] else ''} | {r['Z_lam_m1']:.2f} | {r['Z_lam_0']:.2f} | {r['Z_lam_p05']:.2f} |")
    a("\n### D36 scans for the lambda<0 exclusion, kZ convention (PRIMARY; reduced coupling model)\n\n| kind | f | Z(lambda=-1) | Z(lambda=0) | Z(lambda=0.5) |\n|---|---|---|---|---|")
    for r in ck["d36_lambda"]: a(f"| {r['kind']} | {r['f']}{' (beyond D36)' if r['beyond_D36'] else ''} | {r['Z_lam_m1']:.2f} | {r['Z_lam_0']:.2f} | {r['Z_lam_p05']:.2f} |")
x = J("reso")
if x:
    a("\n## 6. Mass-resolution dependence (signal m_gg smeared about 125 GeV by r; 500 fb^-1, def. a)\n\n| r | s (+-3.5 window) | b | Z Eq. 1 | Z0 PL | mu95 median |\n|---|---|---|---|---|---|")
    for r in x["scan"]: a(f"| {r['resolution_factor']} | {r['s_window']:.3f} | {r['b_window']:.3f} | {r['Z_eq1']:.3f} | {r['Z0_PL']:.3f} | {r['mu95_exp'][1]:.2f} |")
a("""
## 7. Caveats / what this is not
Expected only; the sensitivity is below 1 sigma at 500 fb^-1 and about 1 sigma at 3000 fb^-1 (PL, cut-based): no evidence is expected and none is claimed. Delphes-level, LO, no pile-up. ASSUMPTION nuisances (lumi, photon/lepton efficiency, mass scale/resolution) have no data basis. **The v1.1 lost-lepton class has N_eff = 7.6 at the selection, below the SPEC sec. 4.3 standard N_eff >= 10 (36 % MC stat; its QCD part is one raw row); the v1 estimate (vbs x C) is carried as the robustness row in 06 sec. 5; the v1.1 nominal is kept (pre-declared by 04:139 and D45).** Signal definition (b) adds QCD WHjj (H_QCD_WH_mlm) as signal; its interference (-0.3 % of EW) is neglected. The v1.1 row F_QCD_llajj_loose IS included (replaces the QCD part of ZH_Zajj_eFake; all numbers in this report are the v1.1 evaluation, files *_v11.json; D45 trigger not fired); H_ggF_jj is NOT in the nominal: its gridpack (893012) failed, the D38 scaled central proxy (05a sec. 12, 0.024 events in the window, +1.3 % of b) is a bound variant that lowers Z0 by about 0.6 % (work/stat/ggf_variant_v11.json). MVA alternative not carried through the statistics here (D44: alternative only). Figures: figures/mgg_selection, Z_vs_lumi, d36_*, lambda_exclusion*.

## 8. Next
Verification; VH combination with the frozen ZH (swappable ZH table); comparison with CMS/ATLAS; reproducibility and FINAL report; v1.1 re-evaluations.
""")
open(f"{WH}/reports/07_sensitivity.md", "w").write("\n".join(B)); print("written")
