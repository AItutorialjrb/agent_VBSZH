#!/usr/bin/env python3
"""B5: vh_ws/zh_paper_inputs.json (ZH, corrected) for the paper package. Every entry carries 'src' (json file : key path) so that tables are generated, not typed."""
import json, sys, numpy as np
sys.path.insert(0, "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/combination/zh_check")
from d2_cls import asimov as ASIM
P = "/eos/home-r/rjiang/vbs_zh_codex_starter"; Zd = P + "/p2/combination/zh_check/out"; VW = P + "/p2/combination/vh_ws"
FR = json.load(open(P + "/work/final_ntuples/final.json")); NOM = json.load(open(Zd + "/ff2_nominal.json")); RAW = json.load(open(Zd + "/zh_templates_raw.json")); AN = json.load(open(Zd + "/analysis.json"))
VAR = {n: json.load(open(f"{Zd}/{f}.json")) for n, f in (("closure_scaled_kappa0.64", "ff2_closdown"), ("EW_x2.5", "ff2_ew2p5"), ("uncalibrated_kappa1", "ff_uncal_fix"))}
ORT = json.load(open(VW + "/orthogonality.json"))
def eq1(s, b): return float(np.sqrt(2*((s + b)*np.log1p(s/b) - s))) if s > 0 and b > 0 else 0.0
out = dict(description="ZH channel (corrected fake-photon inputs, D37/D43) for the paper package; frozen = zh-final-v1.1 direct-count numbers; every table value is read from a source json key given in 'src'", sources=dict(frozen=f"work/final_ntuples/final.json", corrected="p2/combination/zh_check/out/ff2_nominal.json", templates="p2/combination/zh_check/out/zh_templates_raw.json", analysis="p2/combination/zh_check/out/analysis.json"))
# samples
S = {}
for sid, r in NOM["registry"].items():
    S[sid] = dict(sigma_fb=r["sig"], k=r["k"], N_delphes=r["N"], w_evt_fb=r["w_evt_fb"], role=r["role"], group=r["grp"], source=r["src"], br=NOM["br_table"][sid], nmc_check=NOM["nmc_check"].get(sid), src="ff2_nominal.json:registry/br_table/nmc_check")
out["samples"] = S; out["branching"] = dict(src="ff2_nominal.json:br", **NOM["br"])
# cutflow (500 fb^-1)
out["cutflow"] = dict(optimum=NOM["optimum"], frozen_steps=[{k: v for k, v in row.items()} for row in FR["cutflow"]], src_frozen="final.json:cutflow", note="Fake-photon rows in this cutflow are the DIRECT-count rows of the frozen study (artefact included); the corrected fake-factor cutflow is in ff_cutflow.", ff_cutflow=RAW["ff_cutflow"], src_ff="zh_templates_raw.json:ff_cutflow", baseline=FR["cutflow_baseline"], src_baseline="final.json:cutflow_baseline")
# composition + results
def comp(d, k):
    c = d["results"][k]["comp"]; return {sid: dict(y=v["y"], mcstat=v["mcstat"], raw_win=v["raw_win"], raw_wide=v["raw_wide"], method=v["method"]) for sid, v in c.items()}
CL = {sid: r["grp"] for sid, r in NOM["registry"].items()}
res = {}
for k in ("500_a", "1000_a", "3000_a", "500_b", "1000_b", "3000_b"):
    row = {}
    for tag, d in (("frozen", FR), ("corrected", NOM), *VAR.items()):
        v = d["results"][k]; f = d["fit"][k]
        row[tag] = dict(s=v["s"], b=v["b"], s_mc=v["s_mc"], b_mc=v["b_mc"], sigma_b=v["sigma_b"], Z_eq1=v["Z_eq1"], Z_eq1_mcerr=v["Z_eq1_mcerr"], Z_with_sigma_b=v["Z_syst_counting"], mu95_cls_discretised=v["mu95_cls"], mu95_cls_stat=v["mu95_cls_stat"],
                        mu95_asimov_smooth=float(ASIM(v["s"], v["b"], v["sigma_b"])), fit_Z_syst=f["Z_syst"], fit_Z_stat=f["Z_stat"], fit_mu95_syst=f["mu95_syst"], fit_mu95_stat=f["mu95_stat"], n_median=v["n_median"])
        if "comp" in v and v["comp"]:
            row[tag]["classes"] = {}
            for sid, c in v["comp"].items(): row[tag]["classes"][CL[sid]] = row[tag]["classes"].get(CL[sid], 0.0) + c["y"]
            row[tag]["components"] = {sid: dict(y=c["y"], mcstat=c["mcstat"], raw_win=c["raw_win"], raw_wide=c["raw_wide"], method=c["method"]) for sid, c in v["comp"].items()}
    res[k] = row
out["results"] = res; out["results_src"] = "final.json:results,fit ; ff2_nominal.json / ff2_closdown.json / ff2_ew2p5.json / ff_uncal_fix.json:results,fit; mu95_asimov_smooth from zh_check/d2_cls.py"
# fake-photon normalisation scan (corrected row scaled; photon only; there is no non-prompt-lepton row in the ZH b)
scan = {}
for L, k in ((500, "500_a"), (1000, "1000_a"), (3000, "3000_a")):
    c = NOM["results"][k]["comp"] if NOM["results"][k]["comp"] else None
    if c is None:
        c = NOM["results"]["500_a"]["comp"]; fac = L/500.0
    else: fac = 1.0
    fk = sum(c[s]["y"] for s in ("F_QCD_Zajj", "F_EW_Zajj"))*fac; bo = NOM["results"][k]["b"] - fk; s_ = NOM["results"][k]["s"]
    scan[str(L)] = {f"x{f}": dict(b=bo + f*fk, Z_eq1=eq1(s_, bo + f*fk), mu95_asimov_stat=float(ASIM(s_, bo + f*fk, 1e-6*(bo + f*fk)))) for f in (0.0, 0.3, 0.5, 1.0, 2.0, 3.0)}
    scan[str(L)]["direct_count_frozen_equivalent"] = dict(b=FR["results"][k]["b"], Z_eq1=FR["results"][k]["Z_eq1"])
scan["note"] = "photon scan x0.3 .. x3 of the corrected fake-photon rows (D36-style); stat+norm-free Eq.1 and Asimov (no sigma_b); a scan of non-prompt leptons is not applicable: the ZH Zll selection has no non-prompt-lepton row in b (config/sample_matrix_phase02.yaml:88,147: < 1e-2 events at 500 fb^-1, not simulated); the rate would have to be x100 higher to matter."
out["fake_photon_scan"] = scan
out["robustness"] = dict(frozen=FR["robustness"], corrected=NOM["robustness"], src="final.json:robustness ; ff2_nominal.json:robustness")
out["systematics_groups_b_500_a"] = dict(frozen=FR["results"]["500_a"]["groups_b"], corrected=NOM["results"]["500_a"]["groups_b"])
out["fake_photon"] = dict(artefact_and_rate=dict(Q2=AN["Q2"], rate=AN["rate"], closure=AN["closure"], calibration=AN["calibration"], src="zh_check/out/analysis.json"),
    yields_500_a=dict(frozen_direct=FR["results"]["500_a"]["comp"]["F_QCD_Zajj"]["y"] + FR["results"]["500_a"]["comp"]["F_EW_Zajj"]["y"], corrected=NOM["results"]["500_a"]["comp"]["F_QCD_Zajj"]["y"] + NOM["results"]["500_a"]["comp"]["F_EW_Zajj"]["y"]),
    classes_note="two-fake (Z+jets, tt-bar) classes: not in b (order of magnitude only, frozen reference: neglected); non-prompt leptons: not in b (<1e-2 events)")
# couplings from the frozen method with corrected inputs (observable m_llgg)
a, b = FR["coupling"], NOM["coupling"]
cpl = dict(observable=b["choice"]["observable"], note="frozen ZH coupling method (BR fixed at SM = 'fixed'; 'resolved' = kappa_gamma(kW, kt=1) with sign on kW, i.e. the kW-sign convention) re-run on the corrected inputs (ff2_nominal.json:coupling). The mgg-template, kZ-sign-primary version is in zh_pyhf.json (qcurves).",
           lambda_curves={f"{L}|{br}": dict(frozen=dict(Z_m1=a[f"lambda|{L}|{br}"]["Z_excl_lambda_m1"], Z_neg=a[f"lambda|{L}|{br}"]["Z_excl_lambda_neg"], int95=a[f"lambda|{L}|{br}"]["int95"]), corrected=dict(Z_m1=b[f"lambda|{L}|{br}"]["Z_excl_lambda_m1"], Z_neg=b[f"lambda|{L}|{br}"]["Z_excl_lambda_neg"], int95=b[f"lambda|{L}|{br}"]["int95"], lam=b[f"lambda|{L}|{br}"]["lam"], q=b[f"lambda|{L}|{br}"]["q"])) for L in (500, 1000, 3000) for br in ("fixed", "resolved")},
           kappaZ={str(L): dict(corrected=dict(int68=b[f"kappaZ|{L}"]["int68"], int95=b[f"kappaZ|{L}"]["int95"]), frozen=dict(int68=a[f"kappaZ|{L}"]["int68"], int95=a[f"kappaZ|{L}"]["int95"])) for L in (500, 1000, 3000)},
           map2d={str(L): dict(kZ=b[f"2d|{L}"]["kZ"], lam=b[f"2d|{L}"]["lam"], q=b[f"2d|{L}"]["q"]) for L in (500, 3000)})
out["coupling"] = cpl
CH = []
for L in (500, 1000, 3000):
    for cl in ("noclip", "clip500"):
        for lv in ("int68", "int95"):
            fa, fb = a[f"cA|{L}|{cl}"][lv], b[f"cA|{L}|{cl}"][lv]
            if fa != fb: CH.append(f"{L}|{cl}|{lv}: {fa} -> {fb}")
out["cA"] = dict(note="c_A re-derived with the corrected inputs (same method, observable m_llgg, Lambda = 1 TeV, profiled nuisances); signal rates unchanged (CP samples), only b changes. Intervals that differ from the frozen ones (complete list, generated): " + "; ".join(CH), changed_intervals=CH,
    rates=dict(frozen=a["cA_rates"], corrected=b["cA_rates"]), intervals={f"{L}|{cl}": dict(frozen=dict(int68=a[f"cA|{L}|{cl}"]["int68"], int95=a[f"cA|{L}|{cl}"]["int95"]), corrected=dict(int68=b[f"cA|{L}|{cl}"]["int68"], int95=b[f"cA|{L}|{cl}"]["int95"], cA=b[f"cA|{L}|{cl}"]["cA"], q=b[f"cA|{L}|{cl}"]["q"])) for L in (500, 1000, 3000) for cl in ("noclip", "clip500")}, src="final.json:coupling ; ff2_nominal.json:coupling")
out["orthogonality"] = dict(total_overlap=ORT["total_overlap"], src="vh_ws/orthogonality.json")
out["limitations"] = ["no Z gamma + 3 jets ME row (D43): the corrected fake component may be low; the frozen direct count (+5 % Z at most) is the upper variation", "calibration reference mismatch (D39/D43): CMS inclusive in jets vs ZH >= 2 ME partons; kappa 0.5-1 moves Z by < 1 %", "other-Higgs, Zgg, top and fake rows are not rescaled under coupling hypotheses", "templates: pheff, lepeff, phscale, phres are assumptions (no Delphes scale factors), new relative to the frozen ZH study", "per-bin MC errors of the continuum rows use err_bin = sqrt(nu e^2/y) (Poisson-equivalent)"]
out["cms_atlas_comparison"] = dict(note="rows as in the frozen report (FINAL_report.md lines 595-596), WH/VBF-WH H->bb channels at their luminosities; not re-verified here (the WH executor owns the verified comparison)", rows=[dict(exp="CMS", ref="PLB 860 (2025) 139202, arXiv:2405.16566", channel="VBS WH, W->lnu, H->bb", lumi_fb=138, obs_exp_sigma="14.3 / 9.9 (VBS WH)", lam_m1="excluded beyond 5 sigma"), dict(exp="ATLAS", ref="PRL 133 (2024) 141801, arXiv:2402.00426", channel="VBF WH, W->lnu, H->bb", lumi_fb=140, obs_exp_sigma="9.0 / 8.7 (VBF WH)", lam_m1="excluded at >> 5 sigma")])
json.dump(out, open(VW + "/zh_paper_inputs.json", "w"), indent=1, default=lambda o: o.tolist() if isinstance(o, np.ndarray) else float(o))
print("written zh_paper_inputs.json", {k: round(res['500_a'][k]['Z_eq1'], 4) for k in ('frozen', 'corrected')})
