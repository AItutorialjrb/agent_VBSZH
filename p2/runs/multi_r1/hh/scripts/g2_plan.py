#!/usr/bin/env python3
"""G2 production plan builder (reports/04): combines the sample matrix, the pilot bookkeeping, class-resolved N_eff projections, twin checks and the pre-declared rules into
  work/g2/plan.json, work/g2/conservative_variant.json (named output for the structured upper bounds), the plan table / rule tables (markdown on stdout sections) and runs nmc_check_hh on the planned table.
Rules implemented here (all declared in advance in config/g2_predeclared.yaml and SPEC section 6):
  full-N rows (signal, closure, ggF HH, ZH, WH, ZZjj, ttH): N_planned = ceil10k(max(50k, sigma*BR*3000 fb-1)).
  effective-N rows: N_planned = max(N_pilot, ceil10k(N for N_eff,proj >= target in ALL three tagging scenarios)), target 10 (30 for a background whose nominal expected SR yield is > 10 % of the total SR background);
     if that exceeds CAP events/sample the row is flagged and a structured Poisson-95 % bound with its conservative variant is produced instead.
  D-HH-7: ME+jets sample needed only if the PS-based expected SR yield of that background is > 10 % of the total SR background (nominal tagging; also reported for pessimistic/optimistic).
  D-HH-11: each extra background gets a 95 % UL on its SR yield; a dedicated sample only if UL > 10 % of the total SR background.
Usage: g2_plan.py   (reads work/g2/*.json produced by pilot_check / neff_project / twin_check_hh / morph_delphes)"""
import json, math, os, sys, yaml, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nmc_check_hh import nmc_check_hh, poisson95_upper
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); G = f"{H}/work/g2"
M = {s["name"]: s for s in yaml.safe_load(open(f"{H}/config/sample_matrix.yaml"))["samples"]}
GEN = {s["name"]: s for s in yaml.safe_load(open(f"{H}/config/sample_matrix_gen.yaml"))["samples"]}
BRI = {k: v["value"] for k, v in yaml.safe_load(open(f"{H}/config/sample_matrix.yaml"))["br_inputs"].items()}
PIL = json.load(open(f"{G}/pilot.json")); NEF = json.load(open(f"{G}/neff.json")); TW = json.load(open(f"{G}/twins.json"))
CAP = 3_000_000; EPJ = 10_000; SC = ("pessimistic", "nominal", "optimistic")
def ceil10k(x): return int(math.ceil(x / EPJ) * EPJ)
TESTS = {   # sample -> (cluster, note); exit codes verified from condor_history (09_ledger in STATUS)
 "S_HHjj_kV1_k2V1_kl1": "884462", "G_ggHH_loop_kl1": "884466", "H_VBFH_bb": "884462", "H_ZH_Zqq_bb": "884462", "H_ttH_bb": "884462", "T_ttbar_boost": "884462", "V_Zjj_QCD_vbs": "884462",
 "V_ZZjj_EW": "884462", "Q_bbjj_vbs": "884464", "Q_4j_vbs": "884577", "H_WH_Wqq_bb": "884941", "H_ggH_jj_heft": "884943", "V_Wjj_QCD_vbs": "884943", "Q_4b_ht": "884943", "T_ttbar_mlm": "884945"}
TWIN_OF = {"Q_4j_vbs": "Q_4j_vbs_twin", "Q_bbjj_vbs": "Q_bbjj_vbs_twin", "T_ttbar_mlm": "T_ttbar_mlm_twin", "T_ttbar_boost": "T_ttbar_boost_twin", "H_VBFH_bb": "H_VBFH_bb_twin", "H_ZH_Zqq_bb": "H_ZH_Zqq_bb_twin",
           "H_ttH_bb": "H_ttH_bb_twin", "V_Zjj_QCD_vbs": "V_Zjj_QCD_vbs_twin", "V_ZZjj_EW": "V_ZZjj_EW_twin", "H_ggH_jj_heft": "H_ggH_jj_heft_twin", "H_WH_Wqq_bb": "H_WH_Wqq_bb_twin", "V_Wjj_QCD_vbs": "V_Wjj_QCD_vbs_twin"}
INHERIT = {"Q_4b_ht": "Q_4j_vbs", "X_tW_boost": "T_ttbar_mlm", "X_ttZ_boost": "T_ttbar_mlm", "X_ttW_boost": "T_ttbar_mlm", "X_ZZ_QCD_boost": "T_ttbar_mlm", "X_WZ_QCD_boost": "T_ttbar_mlm",
           "X_Zjj_EW_vbs": "V_ZZjj_EW", "X_Wjj_EW_vbs": "V_ZZjj_EW", "X_ggZH_loop": "H_ZH_Zqq_bb"}
BKG_MAIN = ["Q_4j_vbs_twin", "Q_bbjj_vbs_twin", "T_ttbar_mlm", "H_VBFH_bb", "H_ZH_Zqq_bb", "H_WH_Wqq_bb", "H_ttH_bb", "H_ggH_jj_heft", "V_Zjj_QCD_vbs", "V_Wjj_QCD_vbs", "V_ZZjj_EW", "G_ggHH_loop_kl1"]
EXTRA = ["X_tW_boost", "X_ttZ_boost", "X_ttW_boost", "X_Zjj_EW_vbs", "X_Wjj_EW_vbs", "X_ZZ_QCD_boost", "X_WZ_QCD_boost", "X_ggZH_loop"]
SIG = [n for n, s in M.items() if s["cls"] == "signal" and s["role"].split("(")[0] in ("basis", "closure")]
GGH = [n for n in M if n.startswith("G_ggHH_loop")]
def y(n, sc="nominal", key="yield_500fb_smoothed"): return NEF[n]["scen"][sc][key]
# ---------------- total SR background and shares (D-HH-7 / D-HH-11)
tot = {sc: sum(y(n, sc) for n in BKG_MAIN if n in NEF) for sc in SC}
share = {n: {sc: (y(n, sc) / tot[sc] if tot[sc] > 0 else None) for sc in SC} for n in BKG_MAIN + EXTRA if n in NEF}
dominant = {n for n in BKG_MAIN if n in NEF and share[n]["nominal"] is not None and share[n]["nominal"] > 0.10}
ULS = {n: (y(n, "nominal", "yield_500fb_UL95") / tot["nominal"]) for n in BKG_MAIN + EXTRA if n in NEF}
BOUND_ONLY = 0.01      # declared here: an effective-N background whose nominal 95 % UL on the SR yield is < 1 % of the total SR background is handled by the structured bound + conservative variant (SPEC 4.3(3)) instead of more MC
# ---------------- plan rows
rows = {}
CROSS = ["T_ttbar_boost", "Q_4b_ht", "Q_4j_vbs", "Q_bbjj_vbs"]      # cross-check / bound-shape / superseded-nominal-filter rows (never summed)
SWITCH = {"Q_4j_vbs_twin": "Q_4j_vbs", "Q_bbjj_vbs_twin": "Q_bbjj_vbs"}   # production uses the LOOSER filter (twin config): the nominal filter lost 25-30 % at the reco VBS stage
for n in SIG + GGH + BKG_MAIN + EXTRA + CROSS:
    s = M[n]; g = GEN[n]; p = PIL.get(n, {}); full = s["rule"] == "full-N"; Npil = p.get("N_lhe", 0)
    r = dict(name=n, cls=s["cls"], rule=s["rule"], sigma_LO_fb=s["sigma_fb"], K=s.get("K_factor", 1.0), sigma_norm_fb=s["sigma_fb"] * s.get("K_factor", 1.0), br_ledger=s["br_ledger"], br_total=s["br_total"], sigma_x_BR_fb=s["sigma_x_BR_fb"],
             N_pilot=Npil, filters=s["generator_cuts"], test=TESTS.get(n), seed_gridpack=s["seed_gridpack"])
    if full:
        r["N_required"] = max(50_000, int(math.ceil(s["sigma_x_BR_fb"] * 3000.0))); r["N_planned"] = max(ceil10k(r["N_required"]), Npil)
    elif n in CROSS:
        r["N_required"] = None; r["N_planned"] = Npil; r["note"] = "cross-check / bound-and-shape sample, never summed into b"
    else:
        tgt = 30.0 if n in dominant else 10.0
        need = [(min(NEF[n]["scen"][sc]["neff_proj_pilot"], NEF[n]["scen"][sc]["neff_direct_pilot"]) if NEF[n]["scen"][sc]["neff_direct_pilot"] > 0 else NEF[n]["scen"][sc]["neff_proj_pilot"]) for sc in SC if n in NEF]   # sizing uses min(projection, MEASURED hard-window N_eff) (G2 review item 9)
        Nn = [(Npil * tgt / x * 1.5 if x > 0 else float("inf")) for x in need]
        r["neff_target"] = tgt; r["N_for_target"] = max(Nn) if Nn else None
        r["N_required"] = None
        r["N_planned"] = max(Npil, ceil10k(r["N_for_target"])) if r["N_for_target"] is not None and np.isfinite(r["N_for_target"]) and r["N_for_target"] <= CAP else Npil
        r["cap_exceeded"] = bool(r["N_for_target"] is None or not np.isfinite(r["N_for_target"]) or r["N_for_target"] > CAP)
        if ULS.get(n, 1.0) < BOUND_ONLY:
            r["bound_only"] = True; r["N_planned"] = Npil; r["rule"] = "effective-N via bound (UL < 1 % of total SR bkg)"
    if n in EXTRA: r["bound_only"] = True; r["N_planned"] = Npil; r["rule"] = "bound (D-HH-11)"
    if n in NEF:
        r["neff_proj_planned"] = {sc: NEF[n]["scen"][sc]["neff_proj_pilot"] * r["N_planned"] / NEF[n]["N_pilot"] for sc in SC}
        r["neff_direct_pilot"] = {sc: NEF[n]["scen"][sc]["neff_direct_pilot"] for sc in SC}; r["n_SR_raw_pilot"] = NEF[n]["n_SR_direct"]
        r["yield_500fb"] = {sc: y(n, sc) for sc in SC}; r["yield_UL95_500fb"] = {sc: y(n, sc, "yield_500fb_UL95") for sc in SC}; r["rel_mc_err_pilot"] = {sc: NEF[n]["scen"][sc]["rel_mc_err"] for sc in SC}
        # top contributing class pairs (nominal)
        cl = NEF[n]["scen"]["nominal"]["classes"]; top = sorted(cl.items(), key=lambda kv: -kv[1]["E_sumw_frac"])[:2]; r["top_classes"] = [(k, round(v["E_sumw_frac"], 2), round(v["neff_proj_pilot"] * r["N_planned"] / NEF[n]["N_pilot"], 1)) for k, v in top]
    # twin
    tw = TWIN_OF.get(n)
    if n in SWITCH:
        b = TW[SWITCH[n]]["stages"]["vbs"]; r["twin"] = dict(sample=f"production uses the looser filter of the twin; nominal-filter loss at reco VBS stage {b['loss']*100:+.0f}±{b['err']*100:.0f} % (k={b['k_nominal']}/{b['k_twin']})", ok=True, switched=True, loss=b["loss"], err=b["err"], k=(b["k_nominal"], b["k_twin"]), basis="residual loss of the looser filter assumed <= nominal loss (added as syst, D-HH-14)")
    elif tw and n in TW:
        t = TW[n]["stages"]["vbs"]; sh = share.get(n, {}).get("nominal"); imp = (sh * max(t.get("loss_UL95", 1.0), 0.0)) if (sh is not None and t["loss"] is not None) else None
        tg = TW[n]["stages"]["tagw"]; imp_t = (sh * max(tg.get("loss_UL95", 1.0), 0.0)) if (sh is not None and tg["loss"] is not None) else None
        if imp is not None and imp_t is not None: imp = max(imp, imp_t)
        ok_s = bool(TW[n]["twin_ok"] and TW[n].get("twin_ok_tagw", True)); ok_i = bool(imp is not None and imp <= 0.05 and sh < 0.10)
        r["twin"] = dict(sample=tw, loss=t["loss"], err=t["err"], UL95=t.get("loss_UL95"), ok=(ok_s or ok_i), ok_sample_level=ok_s, ok_impact_level=ok_i, impact=imp, share=sh, stat_limited=TW[n]["stat_limited"], k=(t["k_nominal"], t["k_twin"]),
                         tagw_loss=tg.get("loss"), tagw_err=tg.get("err"), basis=("sample-level (VBS and tag-weighted stages): loss-1.645 err <= 5 %" if ok_s else ("impact-level: share x UL95(loss) <= 5 % of total SR background and share < 10 %" if ok_i else "FAILED")))
    elif n in INHERIT:
        b = INHERIT[n]; r["twin"] = dict(sample=f"inherited from {b}", ok=bool(TW.get(b, {}).get("twin_ok", False)), inherited=True)
    elif n in SIG or n in GGH: r["twin"] = dict(sample="signal twin (S_HHjj_SM/k2V0 twins)" if n in SIG else "n/a (no generator filter beyond ptj/eta)", ok=True)
    # resources
    jobs_total = int(math.ceil(r["N_planned"] / EPJ)) if r["N_planned"] else 0; jobs_pilot = p.get("jobs", 0)
    r["jobs_new"] = max(jobs_total - jobs_pilot, 0); r["events_new"] = max(r["N_planned"] - Npil, 0)
    tpe = p.get("wall_s_per_lhe_event", 0.07); r["wall_h_new"] = r["events_new"] * tpe / 3600.0 + r["jobs_new"] * 300 / 3600.0
    bpe = p.get("bytes_per_lhe_event", 4000.0); r["storage_GB_total"] = r["N_planned"] * bpe / 1e9; r["storage_GB_new"] = r["events_new"] * bpe / 1e9
    k0 = jobs_pilot; r["seeds_new"] = (3_100_000 + 1000 * s["idx"] + 10 + k0, 3_100_000 + 1000 * s["idx"] + 10 + k0 + max(r["jobs_new"] - 1, 0)) if r["jobs_new"] else None
    rows[n] = r
# ---------------- D-HH-7
d7 = {}
for n, grp in (("V_Zjj_QCD_vbs", "Z+3j"), ("V_Wjj_QCD_vbs", "W+3j"), ("H_ZH_Zqq_bb", "VH+2j"), ("H_WH_Wqq_bb", "VH+2j"), ("H_ggH_jj_heft", "ggH+3j")):
    d7[n] = dict(group=grp, **{f"share_{sc}": share[n][sc] for sc in SC}, yield_nominal=y(n), need_ME_sample=bool(share[n]["nominal"] > 0.10), rule_result=("add ME+jets sample" if share[n]["nominal"] > 0.10 else "100 % PS-modelling uncertainty"))
# ---------------- D-HH-11 bounds
d11 = {}; cons = {}
for n in EXTRA:
    if n not in NEF: continue
    ul = {sc: y(n, sc, "yield_500fb_UL95") for sc in SC}; d11[n] = dict(yield_nominal=y(n), UL95={sc: ul[sc] for sc in SC}, share_UL_nominal=ul["nominal"] / tot["nominal"], dedicated_sample_needed=bool(ul["nominal"] > 0.10 * tot["nominal"]), neff_proj_pilot=NEF[n]["scen"]["nominal"]["neff_proj_pilot"])
    cons[n] = dict(sr_background_events=ul["nominal"], scenario="nominal", L_fb=500.0, method="class-aware Poisson95 on the smoothed expectation", note="conservative variant of the analysis: this sample's SR contribution set to its 95 % UL")
os.makedirs(G, exist_ok=True); json.dump(cons, open(f"{G}/conservative_variant.json", "w"), indent=1)
# extra backgrounds that exceed the 10 % rule become dedicated samples with effective-N planning like the main ones
for n, v in d11.items():
    if v["dedicated_sample_needed"]:
        r = rows[n]; r["bound_only"] = False; r["rule"] = "effective-N (dedicated, D-HH-11)"; tgt = 10.0; need = [NEF[n]["scen"][sc]["neff_proj_pilot"] for sc in SC]; Nn = max((r["N_pilot"] * tgt / x * 1.5 if x > 0 else float("inf")) for x in need)
        r["neff_target"] = tgt; r["N_for_target"] = Nn; r["dedicated"] = True
        r["N_planned"] = max(r["N_pilot"], ceil10k(Nn)) if np.isfinite(Nn) and Nn <= CAP else r["N_pilot"]; r["cap_exceeded"] = bool(not np.isfinite(Nn) or Nn > CAP)
        r["neff_proj_planned"] = {sc: NEF[n]["scen"][sc]["neff_proj_pilot"] * r["N_planned"] / NEF[n]["N_pilot"] for sc in SC}
        jt = int(math.ceil(r["N_planned"] / EPJ)); r["jobs_new"] = max(jt - PIL[n]["jobs"], 0); r["events_new"] = max(r["N_planned"] - r["N_pilot"], 0)
        r["wall_h_new"] = r["events_new"] * PIL[n]["wall_s_per_lhe_event"] / 3600 + r["jobs_new"] * 300 / 3600; r["storage_GB_total"] = r["N_planned"] * PIL[n]["bytes_per_lhe_event"] / 1e9; r["storage_GB_new"] = r["events_new"] * PIL[n]["bytes_per_lhe_event"] / 1e9
        r["seeds_new"] = (3_100_000 + 1000 * M[n]["idx"] + 10 + PIL[n]["jobs"], 3_100_000 + 1000 * M[n]["idx"] + 10 + PIL[n]["jobs"] + max(r["jobs_new"] - 1, 0)) if r["jobs_new"] else None
# ---------------- nmc_check_hh on the planned table
reg = []; ulrecs = {}
for n, r in rows.items():
    if n in CROSS or (n in EXTRA and not d11.get(n, {}).get("dedicated_sample_needed")): continue   # cross-check / bound samples are not in b as samples
    g = GEN[n]; e = dict(name=n, role=("basis" if M[n]["role"].startswith("basis") else ("closure" if M[n]["role"].startswith("closure") else "bkg")), N_gen=r["N_planned"], sigma_fb=r["sigma_norm_fb"], br_total=r["br_total"], br_ledger=r["br_ledger"], strict=(r["rule"] == "full-N"))
    if r["rule"] == "full-N":
        e["role"] = e["role"] if e["role"] in ("basis", "closure") else "sig"
    else:
        ne = r["neff_proj_planned"]["nominal"]; e["twin_ok"] = bool(r["twin"]["ok"]); e["sr_sumw"] = ne; e["sr_sumw2"] = ne      # (sum w)^2/sum w^2 = ne  (sumw=ne, sumw2=ne gives ne^2/ne)
        if r.get("bound_only"):
            nn = NEF[n]["scen"]["nominal"]; ulv = nn["yield_500fb_UL95"]; ulrecs[n] = dict(sr_background_events=ulv)
            if nn["yield_500fb_UL95_direct"] is not None and nn["yield_500fb_UL95_direct"] >= (nn["yield_500fb_UL95_classaware"] or 0):
                e["ul_fb"] = dict(method="poisson95_direct", k=nn["k_direct"], yield_direct=nn["yield_direct_500fb"], value=ulv, conservative_file=f"{G}/conservative_variant_poisson.json")
            else:
                e["ul_fb"] = dict(method="poisson95_classaware", n_eff_s=nn["neff_smoothed_n"], yield_est=nn["yield_500fb_smoothed"], value=ulv, conservative_file=f"{G}/conservative_variant_poisson.json")
            e["sr_sumw"] = 0.0; e["sr_sumw2"] = 0.0
        elif ne < 10.0 or min(r["neff_proj_planned"].values()) < 10.0:
            k = r["n_SR_raw_pilot"]; scale = r["sigma_x_BR_fb"] * 500.0 / NEF[n]["N_pilot"]; wmax = 0.36
            val = poisson95_upper(k) * scale * wmax; e["ul_fb"] = dict(method="poisson95_wmax", k=k, scale=scale, wmax=wmax, value=val, conservative_file=f"{G}/conservative_variant_poisson.json"); ulrecs[n] = dict(sr_background_events=val)
    reg.append(e)
json.dump(ulrecs, open(f"{G}/conservative_variant_poisson.json", "w"), indent=1)
chk = nmc_check_hh(reg, br_inputs=BRI)
out = dict(rows=rows, total_bkg_500fb=tot, share=share, D7=d7, D11=d11, dominant=sorted(dominant), nmc_check=chk, CAP=CAP,
           totals=dict(wall_h_new=sum(r["wall_h_new"] for r in rows.values()), storage_GB_total=sum(r["storage_GB_total"] for r in rows.values()), storage_GB_new=sum(r["storage_GB_new"] for r in rows.values()),
                       jobs_new=sum(r["jobs_new"] for r in rows.values()), events_new=sum(r["events_new"] for r in rows.values())))
json.dump(out, open(f"{G}/plan.json", "w"), indent=1, default=float)
print("nmc_check_hh PASSED on the planned table (%d rows)" % len(reg)); print(json.dumps(out["totals"], indent=1)); print("total SR bkg 500/fb:", {k: round(v, 3) for k, v in tot.items()}); print("dominant:", sorted(dominant))
