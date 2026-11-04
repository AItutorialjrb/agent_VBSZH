#!/usr/bin/env python3
"""Renders the data-driven tables of reports/04_production_plan.md from work/g2/*.json into work/g2/tables.md (sections referenced by @@NAME@@ tokens in reports/04_production_plan.src.md -> 04_production_plan.md)."""
import json, os, sys, yaml, math, subprocess, re
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); G = f"{H}/work/g2"
PL = json.load(open(f"{G}/plan.json")); PIL = json.load(open(f"{G}/pilot.json")); NEF = json.load(open(f"{G}/neff.json")); TW = json.load(open(f"{G}/twins.json"))
MO = json.load(open(f"{G}/morph_delphes.json")); ML = json.load(open(f"{G}/mlm_check.json")); VA = json.load(open(f"{G}/variations.json"))
M = {s["name"]: s for s in yaml.safe_load(open(f"{H}/config/sample_matrix.yaml"))["samples"]}
R = PL["rows"]; T = {}
def g(x, p=3): return "n/a" if x is None else (f"{x:.{p}g}")
def sci(x): return f"{x:.3g}"
def kfmt(x): return f"{x:,}" if isinstance(x, int) else str(x)
# ---------- T1 production plan table
def cutstr(c): return ", ".join(f"{k}={v}" for k, v in c.items() if k not in ("dynamical_scale_choice", "ptj", "etaj", "drjj"))
L = ["| sample | class | σ_LO [fb] ⇒ K ⇒ σ [fb] (source) | BR (applied once) | generator filters; twin evidence | rule | N required / N_eff target | N_planned (pilot done) | projected N_eff in SR p / n / o (class-resolved top) | seeds | jobs × events | wall-clock h | storage [GB] | test job |", "|---|" * 14]
L[1] = "|" + "---|" * 14
order = [n for n in R if n.startswith("S_")] + [n for n in R if n.startswith("G_")] + [n for n in R if not n.startswith(("S_", "G_", "X_"))] + [n for n in R if n.startswith("X_")]
for n in order:
    r = R[n]; s = M[n]
    src = {"signal": "MG5 LO gridpack (EW, QCD=0), no K", "ggF_HH": "MG5 LO loop × K (HWG 33.62 fb @13.6 TeV)"}.get(s["cls"], "MG5 LO gridpack at the generator cuts; K = 1 (LO; normalisation unc. in 06)")
    brs = "×".join(r["br_ledger"]) + f" = {r['br_total']:.4g}"
    tw = r.get("twin"); twstr = "—"
    if tw:
        if tw.get("switched"): twstr = tw["sample"] + " (" + tw["basis"] + ")"
        elif tw.get("inherited"): twstr = f"{tw['sample']}: {'ok' if tw['ok'] else 'NOT ok'}"
        elif tw.get("loss") is not None: twstr = f"{tw['sample']}: loss {tw['loss']*100:+.0f}±{tw['err']*100:.0f} % (k={tw['k'][0]}/{tw['k'][1]}); {'ok' if tw['ok'] else 'NOT ok'} ({tw.get('basis','')})"
        else: twstr = f"{tw['sample']}: {'ok' if tw['ok'] else 'NOT ok'}"
    rule = r["rule"] + (" (D-HH-12)" if r["rule"] == "full-N" and not n.startswith(("S_", "G_")) else "")
    req = f"N ≥ {kfmt(r['N_required'])}" if r.get("N_required") else (f"N_eff ≥ {r['neff_target']:g}" if r.get("neff_target") else "cross-check / bound")
    ne = r.get("neff_proj_planned"); nes = "—" if not ne else " / ".join(g(ne[x], 3) for x in ("pessimistic", "nominal", "optimistic")) + (" (" + "; ".join(f"{a} {b:.0%}, {c:g}" for a, b, c in r.get("top_classes", [])) + ")" if r.get("top_classes") else "")
    if r.get("cap_exceeded"): nes += " **cap exceeded → bound**"
    seeds = f"{r['seeds_new'][0]}–{r['seeds_new'][1]}" if r.get("seeds_new") else "pilot only"
    jobs = f"{r['jobs_new']} × 10k" if r["jobs_new"] else "0"
    tj = r.get("test") or ("σ-closure LHE job 884463 + pilot" if n.startswith("S_") else "pilot job (10k)")
    L.append(f"| {n} | {r['cls']} | {sci(r['sigma_LO_fb'])} ⇒ {r['K']:.3g} ⇒ {sci(r['sigma_norm_fb'])} ({src}) | {brs} | {cutstr(r['filters'])}; {twstr} | {rule} | {req} | {kfmt(r['N_planned'])} ({kfmt(r['N_pilot'])}) | {nes} | {seeds} | {jobs} | {r['wall_h_new']:.1f} | {r['storage_GB_total']:.2f} | {tj} |")
T["PLAN"] = "\n".join(L)
# ---------- totals
tt = PL["totals"]
T["TOTALS"] = f"New events beyond the pilots: **{tt['events_new']:,.0f}** in **{tt['jobs_new']:.0f}** jobs; new CPU **{tt['wall_h_new']:.0f} wall-h**; storage of all planned samples (pilot + new) **{tt['storage_GB_total']:.1f} GB** (new: {tt['storage_GB_new']:.1f} GB)."
# ---------- pilot table
T["TESTS"] = open(f"{G}/sigma_closure_tests.md").read()
T["PILOT"] = open(f"{G}/pilot.md").read()
# ---------- twin table
T["TWIN"] = open(f"{G}/twins.md").read()
# ---------- D7 / D11
d7 = ["| background | ME+jets sample in question | expected SR events @500 fb⁻¹ (pess/nom/opt, smoothed estimator) | share of total SR bkg (nominal) | > 10 %? | outcome |", "|---|---|---|---|---|---|"]
for n, v in PL["D7"].items(): d7.append(f"| {n} | {v['group']} | {g(NEF[n]['scen']['pessimistic']['yield_500fb_smoothed'])} / {g(NEF[n]['scen']['nominal']['yield_500fb_smoothed'])} / {g(NEF[n]['scen']['optimistic']['yield_500fb_smoothed'])} | {v['share_nominal']*100:.2g} % (pess {v['share_pessimistic']*100:.2g} %, opt {v['share_optimistic']*100:.2g} %) | {'yes' if v['need_ME_sample'] else 'no'} | {v['rule_result']} |")
tot = PL["total_bkg_500fb"]; d7.append(f"\nTotal SR background (sum of the main backgrounds, 500 fb⁻¹, smoothed estimator, before the multijet ±100 %): pessimistic {tot['pessimistic']:.3g}, nominal {tot['nominal']:.3g}, optimistic {tot['optimistic']:.3g} events.")
T["D7"] = "\n".join(d7)
d11 = ["| extra background | pilot N | raw SR count | expected SR @500 fb⁻¹ (nominal, smoothed) | 95 % UL (nominal; class-aware Poisson) | UL / total SR bkg | UL > 10 %? | outcome |", "|---|---|---|---|---|---|---|---|"]
for n, v in PL["D11"].items(): d11.append(f"| {n} | {NEF[n]['N_pilot']} | {NEF[n]['n_SR_direct']} | {g(v['yield_nominal'])} | {g(v['UL95']['nominal'])} (pess {g(v['UL95']['pessimistic'])}, opt {g(v['UL95']['optimistic'])}) | {v['share_UL_nominal']*100:.2g} % | {'yes' if v['dedicated_sample_needed'] else 'no'} | {'dedicated sample (effective-N plan in the table)' if v['dedicated_sample_needed'] else 'bound only: UL enters as an extra background term in the conservative variant (work/g2/conservative_variant.json)'} |")
T["D11"] = "\n".join(d11)
# ---------- class-resolved N_eff for the dominant backgrounds
cr = ["| sample | pilot N | pre-window events V | raw SR | N_eff proj. (pilot, p/n/o) | class pair | share of E[Σw] | N_eff proj. of the class (nominal, at the PILOT N) |", "|---|---|---|---|---|---|---|---|"]
for n in ("Q_4j_vbs", "Q_bbjj_vbs", "Q_4b_ht", "T_ttbar_mlm", "H_ttH_bb", "V_Zjj_QCD_vbs", "V_Wjj_QCD_vbs", "H_ggH_jj_heft", "V_ZZjj_EW", "H_ZH_Zqq_bb", "H_WH_Wqq_bb", "H_VBFH_bb"):
    if n not in NEF: continue
    r = NEF[n]; sc = r["scen"]; cl = sorted(sc["nominal"]["classes"].items(), key=lambda kv: -kv[1]["E_sumw_frac"])[:4]
    for i, (k, v) in enumerate(cl):
        first = f"| {n} | {r['N_pilot']} | {r['n_V']} | {r['n_SR_direct']} | {g(sc['pessimistic']['neff_proj_pilot'])} / {g(sc['nominal']['neff_proj_pilot'])} / {g(sc['optimistic']['neff_proj_pilot'])} " if i == 0 else "| | | | | "
        cr.append(first + f"| {k} (V={v['n_V']}) | {v['E_sumw_frac']*100:.0f} % | {g(v['neff_proj_pilot'])} |")
T["CLASSES"] = "\n".join(cr)
# ---------- morph
mc = ["| closure point (κV, κ2V, κλ) | Σ|c_i| | stage | raw k (direct) | predicted [fb] | direct [fb] | pull |", "|---|---|---|---|---|---|---|"]
for n, v in MO["closure"].items():
    for st, x in v["stages"].items(): mc.append(f"| {tuple(v['point'])} | {v['sum_abs_c']:.2f} | {st} | {x['k_direct']} | {x['pred_fb']:.4g} ± {x['pred_err']:.2g} | {x['direct_fb']:.4g} ± {x['direct_err']:.2g} | {x['pull']:+.2f} |")
    h = v["mHH_hist_pre_window"]; mc.append(f"| {tuple(v['point'])} | | m(HH)-proxy histogram, pre-window region | | | | χ²/ndf = {h['chi2']:.1f}/{h['ndf']} |")
T["MORPH_CLOSURE"] = "\n".join(mc)
am = ["| scan | κ | Σ|c_i| | morphed SR yield Y [fb] (raw, no tagging) | rel. MC error at pilot N | rel. MC error at planned N | absolute MC error [events @500 fb⁻¹, ε_H²=0.36] at planned N |", "|---|---|---|---|---|---|---|"]
for lab, pts in (("κ2V (κV=κλ=1)", [(1, x, 1) for x in (-1, 0, 0.5, 1, 1.5, 2, 3)]), ("κλ (κV=κ2V=1)", [(1, 1, x) for x in (-5, -2, 0, 1, 2, 5, 10)]), ("κV (κ2V=κλ=1)", [(x, 1, 1) for x in (0.5, 0.7, 0.9, 1.1, 1.3, 1.5)])):
    key = {"κ2V": "k2V", "κλ": "kl", "κV": "kV"}[lab.split()[0]]
    for k in pts:
        row = min(MO["amplification"][key], key=lambda r: sum((a - b) ** 2 for a, b in zip(r["k"], k)))
        e = row["relerr_plannedN"]; absn = abs(row["Y_win_fb"]) * e * 500 * 0.36 if e is not None else None
        am.append(f"| {lab} | {tuple(round(x, 2) for x in row['k'])} | {row['sum_abs_c']:.1f} | {row['Y_win_fb']:.3g} | {g(row['relerr_pilotN'], 2)} | {g(e, 2)} | {g(absn, 2)} |")
T["MORPH_AMP"] = "\n".join(am)
# ---------- MLM
S = ML["samples"]; ml = ["| sample | xqcut / qCut | σ_MG5 [pb] | N_LHE | accepted | matching eff. | σ_matched [pb] | ratio to nominal | stage two / lead / VBS (ratio to nominal, ± stat of the ratio) |", "|---|---|---|---|---|---|---|---|---|"]
xq = {"T_ttbar_mlm": "30 / 40", "T_ttbar_mlm_xq20": "20 / 26", "T_ttbar_mlm_xq45": "45 / 60", "T_ttbar_boost": "PS only (0 ME jets)"}
for n, s in S.items():
    rat = ML["ratios"].get(n); st = "—" if not rat else " / ".join(f"{rat['stage_'+k]['ratio']:.2f}" + (f"±{rat['stage_'+k]['ratio_err']:.2f}" if rat['stage_'+k]['ratio_err'] else "") for k in ("two", "lead", "vbs"))
    ml.append(f"| {n} | {xq[n]} | {s['sigma_MG5_fb']/1e3:.4g} | {s['n_lhe']} | {s['n_accepted']} | {s['match_eff']:.3f} | {s['sigma_matched_fb']/1e3:.4g} | {('%.3f' % (s['sigma_matched_fb']/S['T_ttbar_mlm']['sigma_matched_fb']))} | {st} |")
ml.append("\nShape comparison to the nominal (bin-wise, stat. errors only; bins with ≥ 5 events in both samples): " + "; ".join(f"{n}: " + ", ".join(f"{k[:-5]} χ²/ndf {v['chi2']:.0f}/{v['ndf']}" for k, v in r.items() if isinstance(v, dict) and 'chi2' in v) for n, r in ML["ratios"].items()))
T["MLM"] = "\n".join(ml)
# ---------- variations
v = ["| sample | baseline SR events @500 fb⁻¹ (nominal, smoothed) | trigger 500 | trigger 550 | m_SD ×0.95 | m_SD ×1.05 | m(HH)<1.5 TeV | m(HH)<1.0 TeV |", "|---|---|---|---|---|---|---|---|"]
for n, x in VA.items():
    b = x["baseline"]["smoothed_500fb"]; v.append(f"| {n} | {g(b)} | " + " | ".join((f"{x[k]['smoothed_500fb']/b:.2f}" if b > 0 else "n/a") for k in ("trigger500", "trigger550", "mSD_x0.95", "mSD_x1.05", "mHH<1500", "mHH<1000")) + " |")
T["VARIATIONS"] = "\n".join(v)
vn = ["| sample | N_planned | smoothed N_eff at planned N: baseline | trigger 550 | m(HH)<1.0 TeV | m_SD ×0.95 / ×1.05 | note |", "|---|---|---|---|---|---|---|"]
for n, x in VA.items():
    if n not in R: continue
    f = R[n]["N_planned"] / x["baseline"]["N_pilot"]; ne = lambda k: x[k]["neff_smoothed_pilot"] * f
    vn.append(f"| {n} | {R[n]['N_planned']:,} | {ne('baseline'):.1f} | {ne('trigger550'):.1f} | {ne('mHH<1000'):.1f} | {ne('mSD_x0.95'):.1f} / {ne('mSD_x1.05'):.1f} | " + ("N_eff ≥ 10 in all variation regions" if min(ne(k) for k in ('trigger550', 'mHH<1000', 'mSD_x0.95', 'mSD_x1.05')) >= 10 else "< 10 in a variation region: smoothed estimator with quoted MC error (rule in g2_predeclared.yaml)") + " |")
T["VARIATIONS_NEFF"] = "\n".join(vn)
T["SHA"] = open(f"{G}/sha_check_pilots.md").read(); T["O1"] = open(f"{G}/o1_partition.txt").read() if os.path.exists(f"{G}/o1_partition.txt") else ""
# ---------- nmc_check output
chk = PL["nmc_check"]; nc = ["| sample | rule | N | required / N_eff(proj, nominal) | ok |", "|---|---|---|---|---|"]
for n, c in chk.items():
    if c["rule"].startswith("N>="): nc.append(f"| {n} | {c['rule']} | {kfmt(int(c['N']))} | {kfmt(int(c['required']))} | {c['ok']} |")
    else: nc.append(f"| {n} | effective-N (twin_ok={c['twin_ok']}) | — | N_eff,proj = {c['N_eff_SR']:.1f} (UL record: {'yes' if c['ul'] else 'no'}) | {c['ok']} |")
T["NMC"] = "\n".join(nc)
open(f"{G}/tables.md", "w").write("\n\n".join(f"@@{k}@@\n{v}" for k, v in T.items()))
src = f"{H}/reports/04_production_plan.src.md"
if os.path.exists(src):
    t = open(src).read()
    for k, vv in T.items(): t = t.replace(f"@@{k}@@", vv)
    open(f"{H}/reports/04_production_plan.md", "w").write(t); print("rendered reports/04_production_plan.md")
else: print("tables only ->", f"{G}/tables.md")
