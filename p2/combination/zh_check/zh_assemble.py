#!/usr/bin/env python3
"""B1/B3/B4: assemble vh_ws/zh_channel_inputs.json from out/zh_templates_raw.json (condor dump of the corrected analysis), out/ortho_*.json (WH signal in the ZH SR) and the K-sample histograms."""
import json, glob, csv, numpy as np
P = "/eos/home-r/rjiang/vbs_zh_codex_starter"; Zd = P + "/p2/combination/zh_check/out"; VW = P + "/p2/combination/vh_ws"
R = json.load(open(Zd + "/zh_templates_raw.json")); O = json.load(open(VW + "/orthogonality.json")); EDG = np.array(R["edges"]); NB = len(EDG) - 1
LREF = 500.0
NAME = {"S_EW_ZHjj": "zhjj_ew", "H_QCD_ZHjj": "zhjj_qcd", "H_ggZH": "ggzh", "H_ttH": "tth", "H_tHW": "thw", "H_ZH_tautau": "zh_tautau", "B_QCD_Zaajj_vbs": "zaajj_qcd",
        "B_EW_Zaajj_vbs_is1": "zaajj_ew_is1", "B_EW_Zaajj_vbs_is2": "zaajj_ew_is2", "B_EW_Zaajj_vbs_is3": "zaajj_ew_is3", "T_ttaa": "ttaa", "T_tta": "tta", "T_tWa": "twa", "F_QCD_Zajj": "fake1_qcd", "F_EW_Zajj": "fake1_ew"}
CLASS = {"zhjj_ew": "signal EW ZHjj", "zhjj_qcd": "QCD ZHjj", "ggzh": "other H->gg", "tth": "other H->gg", "thw": "other H->gg", "zh_tautau": "other H->gg", "zaajj_qcd": "Zgg (QCD+EW)", "zaajj_ew_is1": "Zgg (QCD+EW)", "zaajj_ew_is2": "Zgg (QCD+EW)", "zaajj_ew_is3": "Zgg (QCD+EW)",
         "ttaa": "top", "tta": "top", "twa": "top", "fake1_qcd": "Zg + fake g (corrected FF)", "fake1_ew": "Zg + fake g (corrected FF)"}
BRSM = dict(bb=0.5824, WW=0.2137, gg=0.0818, tautau=0.0627, cc=0.0289, ZZ=0.0264, gamgam=0.00227, Zgam=0.00154, mumu=0.00022)
def rbr(kW, kZ):
    ag = (-8.32*kW + 1.84)**2/(-8.32 + 1.84)**2; w = sum(BRSM.values()) - BRSM["WW"] - BRSM["ZZ"] - BRSM["gamgam"]; w += BRSM["WW"]*kW**2 + BRSM["ZZ"]*kZ**2 + BRSM["gamgam"]*ag; return float(ag/(w/sum(BRSM.values())))
def sample(sid, role, mu):
    s = R["samples"][sid]; nm = NAME[sid]
    REN = {"scale_fake1_qcd": "scale_top_zh", "scale_efake_qcd_ll": "scale_zjfake_qcd_zh", "scale_efake_ew": "scale_zjfake_ew_zh"}
    nuis = {}
    for k, v in s["norm"].items():
        k = REN.get(k, k)
        if k.startswith("zh_norm_"): nuis[k] = dict(norm_up=float(v[0]), norm_down=float(1.0/v[0]))      # log-normal-style symmetric (R3 fix 5)
        else: nuis[k] = dict(norm_up=float(v[0]), norm_down=float(v[1]))
    for k, v in s["shape"].items(): nuis[k] = dict(up=[x*LREF for x in v["up"]], down=[x*LREF for x in v["down"]])
    return nm, dict(role=role, mu=mu, nominal=[x*LREF for x in s["per_fb"]["nominal"]], mcstat=[x*LREF for x in s["per_fb"]["mcstat"]], nuis=nuis, process=sid, class_label=CLASS[nm],
                    yield_window_500=s["per_fb"]["y_window"]*LREF, yield_bins_121_129_500=float(sum(x for x, c in zip(s["per_fb"]["nominal"], 0.5*(EDG[1:] + EDG[:-1])) if 121.0 < c < 129.0))*LREF, mc_window_500=s["per_fb"]["mc_window"]*LREF, method=s["per_fb"]["method"], raw_win=s["per_fb"]["raw_win"], raw_wide=s["per_fb"]["raw_wide"])
# ---------------- WH signal in the ZH SR (B3)
def whsig():
    names = ["WH_S_EW_WHjj", "WH_S_EW_WHjj_taunu"]; nom = np.zeros(NB); mc2 = np.zeros(NB); info = {}
    for n in names:
        o = O["samples"][n]; fac = o["norm_factor_500fb_per_sum_w_pb"]; info[n] = dict(zh_sr_raw=o["flags"]["zh_sr"]["raw"], zh_sr_yield_500=o["flags"]["zh_sr"]["yield_500fb"], zh_sr_mc_500=o["flags"]["zh_sr"]["mc_unc_500fb"],
                                                                              zh_sr_nowindow_raw=o["zh_sr_without_window_105_165"]["raw"], zh_sr_nowindow_yield_500=o["zh_sr_without_window_105_165"]["yield_500fb"], n_events=o["n_events_processed"], ul95_500=o["flags"]["zh_sr"]["ul95_yield_500fb"], zh_pre_raw=o["flags"]["zh_pre"]["raw"], zh_pre_yield_500=o["flags"]["zh_pre"]["yield_500fb"])
        info[n]["w_evt_500"] = fac*O["samples"][n]["flags"]["all"]["yield_500fb"]/max(O["samples"][n]["flags"]["all"]["yield_500fb"], 1e-30)
    wevt = {n: O["samples"][n]["norm_factor_500fb_per_sum_w_pb"]*(O["samples"][n]["flags"]["all"]["yield_500fb"]/O["samples"][n]["norm_factor_500fb_per_sum_w_pb"]/O["samples"][n]["flags"]["all"]["raw"]) for n in names}
    for n in names: info[n]["per_event_weight_500"] = wevt[n]; info[n]["ul95_zero_support_500"] = 3.0*wevt[n]
    mcb = 1.14*sum(wevt.values())
    return dict(nominal=[1e-10]*NB, mcstat=[mcb/NB**0.5]*NB, info=info, note="zero MC support in the ZH SR (all cuts, m_gg 105-165): central 1e-10 per bin (placeholder), per-bin MC uncertainty 1.14 x (sum of the single-event weights)/sqrt(nbins); 95 % CL UL = 3 x weight per event (frozen convention). The yield is negligible (<1e-6 events at 500 fb^-1).")
# ---------------- samples
defs = {}
for d in ("a", "b"):
    S = {}
    for sid in R["samples"]:
        role = "background"; mu = "none"
        if sid == "S_EW_ZHjj": role, mu = "signal", "mu_ZH"
        if sid == "H_QCD_ZHjj" and d == "b": role, mu = "signal", "mu_ZH"
        nm, sm = sample(sid, role, mu); S[nm] = sm
    defs[d] = dict(samples=S)
# ---------------- couplings: per-bin quadratic, WH convention (alpha kW^2 + beta kW kZ + gamma kZ^2) x R_BR
cp = R["coupling_points"]
PTS = {f"K_EW_ZHjj_{t}": (kw, 1.0) for t, kw in (("lam_m100", -1.0), ("lam_m050", -0.5), ("lam_p000", 0.0), ("lam_p050", 0.5), ("lam_p100", 1.0), ("lam_p150", 1.5))}
def quad_fit(sb, pts, loo=None):
    names = [s for s in pts if s != loo]; A = np.array([[pts[s][0]**2, pts[s][0]*pts[s][1], pts[s][1]**2] for s in names]); co = np.zeros((NB, 3)); cov = []
    for i in range(NB):
        y = np.array([sb[s][0][i] for s in names]); e = np.array([max(np.sqrt(sb[s][1][i]), 0.02*abs(sb[s][0][i]), 1e-4*max(abs(np.array([sb[q][0] for q in names])).max(), 1e-12)) for s in names]); W = 1/e
        M = A*W[:, None]; co[i] = np.linalg.lstsq(M, y*W, rcond=None)[0]; cov.append(np.linalg.pinv(M.T @ M))
    return co, cov
sbz = {}
for tag in PTS:
    t = tag.replace("K_EW_ZHjj_", ""); c = cp[t]; w = c["w"]*LREF; sbz[tag] = (np.array(c["sumw"])*LREF, np.array(c["raw"])*w**2)
co_z, cov_z = quad_fit(sbz, PTS)
# closure: leave-one-out totals
clo = []
for tag in PTS:
    c1, _ = quad_fit(sbz, PTS, loo=tag); kw, kz = PTS[tag]; pred = (c1[:, 0]*kw**2 + c1[:, 1]*kw*kz + c1[:, 2]*kz**2).sum(); obs = sbz[tag][0].sum(); err = np.sqrt(sbz[tag][1].sum())
    clo.append(dict(point=tag, obs_total=float(obs), pred_total=float(pred), pull=float((pred - obs)/max(err, 1e-12)), raw=int(round(sum(cp[tag.replace("K_EW_ZHjj_", "")]["raw"])))))
# WH signal in ZH SR: coupling templates from the 8 WH CP-even points (zero-support)
WHP = {"lam_m100": (-1.0, 1.0), "lam_m050": (-0.5, 1.0), "lam_p000": (0.0, 1.0), "lam_p050": (0.5, 1.0), "lam_p100": (1.0, 1.0), "lam_p150": (1.5, 1.0), "kap_W15_Z075": (1.5, 0.75), "kap_W05_Z15": (0.5, 1.5)}
sbw = {}
for t, kk in WHP.items():
    o = O["samples"]["WH_K_EW_WHjj_" + t]; fac = o["norm_factor_500fb_per_sum_w_pb"]; wpe = o["flags"]["all"]["yield_500fb"]/o["flags"]["all"]["raw"]   # events/500 fb per raw event
    sbz_ = np.zeros(NB); raw = np.zeros(NB)
    # per-event (mgg, w_pb) lists were stored for the ZH SR without window: bin them
    sbw[t] = None
nw = {}
for f in sorted(glob.glob(Zd + "/ortho_WH_K_EW_WHjj_*__*.json")):
    d = json.load(open(f)); t = d["label"].split("WH_K_EW_WHjj_")[1].rsplit("__", 1)[0]; nw.setdefault(t, []).extend(d.get("zh_sr_nowindow_mgg_w", []))
sbw = {}
for t, kk in WHP.items():
    o = O["samples"]["WH_K_EW_WHjj_" + t]; fac = o["norm_factor_500fb_per_sum_w_pb"]; ev = nw.get(t, [])
    h = np.histogram([m for m, w in ev], bins=EDG, weights=[w*fac for m, w in ev])[0] if ev else np.zeros(NB); h2 = np.histogram([m for m, w in ev], bins=EDG, weights=[(w*fac)**2 for m, w in ev])[0] if ev else np.zeros(NB)
    sbw[t] = (h, h2)
def quad_fit2(sb, pts):
    names = list(pts); A = np.array([[pts[s][0]**2, pts[s][0]*pts[s][1], pts[s][1]**2] for s in names]); co = np.zeros((NB, 3))
    wpe = np.mean([O["samples"]["WH_K_EW_WHjj_" + s]["flags"]["all"]["yield_500fb"]/O["samples"]["WH_K_EW_WHjj_" + s]["flags"]["all"]["raw"] for s in names])
    for i in range(NB):
        y = np.array([sb[s][0][i] for s in names]); e = np.array([max(np.sqrt(sb[s][1][i]), 1.14*wpe) for s in names]); W = 1/e; co[i] = np.linalg.lstsq(A*W[:, None], y*W, rcond=None)[0]
    return co
co_w = quad_fit2(sbw, WHP)
SM_REF = np.array(R["samples"]["S_EW_ZHjj"]["per_fb"]["nominal"])*LREF
out = dict(
 version="R2-1", written="2026-11-14", lumi_ref_fb=LREF, edges=EDG.tolist(),
 ZH_selection=("Frozen ZH cut-based optimum (final.json optimum): OSSF pair pT>15 with |mll-mZ|<25, mllgg>100, 2 photons pT>25 with pT1/mgg>1/3, pT2/mgg>0.25, no b-veto, no Zeppenfeld, mjj>500, |deta_jj|>3.5; the m_gg window is NOT applied: "
               "templates cover m_gg 105-165 GeV in 2 GeV bins, the +-2 sigma window (%.1f-%.1f GeV) of the counting analysis lies inside. Backgrounds: corrected fake-photon rows (fake factor, D34/D37, kappa=0.956, closure systematics), all other rows identical to zh-final-v1.1." % tuple(R["window"])),
 optimum=R["optimum"], window=R["window"], window_definition="yield_window_500 = exact +-2 sigma_core window of the counting analysis: mu=%.3f, sigma_core=%.3f -> %.2f-%.2f GeV (%.2f GeV wide); yield_bins_121_129_500 = sum of the 2 GeV bins with centres inside 121-129 (8 GeV wide), 3.4 percent smaller for flat shapes, e.g. fake1_qcd 0.00692 vs 0.0072" % (R["mu"], R["sigma_core"], R["window"][0], R["window"][1], R["window"][1]-R["window"][0]), sigma_core=R["sigma_core"], mu_core=R["mu"],
 normalisation="events per 500 fb^-1 at 13.6 TeV, BR(H->gg) = 0.00227 and Z->ee,mumu applied once (k in the sample weights); luminosity scaling linear for events and MC errors",
 template_method="resonant rows (EW and QCD ZHjj, ggZH, ttH, tHW, ZH(tautau)): signal-shape histogram of the EW ZHjj sample (all cuts, no window) scaled to the row's window yield; continuum rows (Zgg, top, fake): row window yield / exponential window fraction x exponential bin integral (frozen method, unbinned MLE; weighted MLE for the fake-factor rows). Per-bin MC error err_bin = sqrt(nu_bin e^2/y) so that the sum in quadrature equals the total MC uncertainty of the row estimate (L0/L1/L2 hierarchy of the frozen code).",
 defs=defs,
 coupling=dict(convention="Y_bin(kW,kZ) = alpha kW^2 + beta kW kZ + gamma kZ^2 (events/500 fb^-1, BR(H->gg) at SM inside k), times R_BR(kW,kZ) exactly as in wh/scripts/coup_run.py (|A_gg|^2 with A_W = -8.32 kW, A_t = +1.84, width sum BR_i kappa_i^2). Primary sign convention (D46): lambda = kW/kZ tested at kZ = -1 (kW = -lambda), kt = +1: the quadratic form is even under (kW,kZ) -> (-kW,-kZ), R_BR evaluated at the actual signs. Variant: sign on kW (kZ=+1). Sample points: HC_NLO_X0_kVV at kZ = 1 and lambda = -1,-0.5,0,0.5,1,1.5 (homogeneous degree 2: these determine alpha,beta,gamma exactly).",
               points={t: dict(generated_point=dict(kW=PTS[f"K_EW_ZHjj_{t}"][0], kZ=1.0, note="the sample as generated: HC_NLO_X0_kVV at kZ=+1, kW=lambda"), kW_sign_variant=dict(kW=PTS[f"K_EW_ZHjj_{t}"][0], kZ=1.0, R_BR=rbr(PTS[f"K_EW_ZHjj_{t}"][0], 1.0)), kZ_sign_primary=dict(kW=-PTS[f"K_EW_ZHjj_{t}"][0], kZ=-1.0, R_BR=rbr(-PTS[f"K_EW_ZHjj_{t}"][0], -1.0), note="same yield (even under (kW,kZ)->(-kW,-kZ)); only R_BR differs"), nominal=(np.array(cp[t]["sumw"])*LREF).tolist(), raw=cp[t]["raw"], mcstat=(np.sqrt(np.array(cp[t]["raw"]))*cp[t]["w"]*LREF).tolist(), event_weight_500=cp[t]["w"]*LREF) for t in [k.replace("K_EW_ZHjj_", "") for k in PTS]},
               quad=dict(alpha=co_z[:, 0].tolist(), beta=co_z[:, 1].tolist(), gamma=co_z[:, 2].tolist(), note="alpha: kW^2, beta: kW kZ, gamma: kZ^2; weighted least squares per bin (error floor 2 % and 1e-4 of the largest yield); per-fb scaling linear"),
               quad_cov=[c.tolist() for c in cov_z], closure_leave_one_out=clo, SM_template_vs_HC_lambda1=dict(sum_template=float(SM_REF.sum()), sum_quad_at_1_1=float(co_z.sum()), note="the SM template (Tier-1 model) and the HC lambda=1 point differ by the generator-mjj cut and the model: use the HC quad for every coupling hypothesis (ratio sum_quad/sum_template given), as in the frozen coupling analysis"),
               qcd_zhjj_scaling="H_QCD_ZHjj scales with kZ^2 (Higgsstrahlung type), as in the frozen coupling_section.py (def. b only); ggZH, ttH, tHW, ZH(tautau), Zgg, fake and top rows are NOT rescaled (limitation)",
               cA_rederived="see zh_paper_inputs.json['cA']"),
 wh_signal_in_zh_sr=dict(in_fit=False, treatment="NOT a sample of the ZH channel (R3 fix 3): zero MC support (0 raw events of 300k in the ZH SR, all cuts, 105-165 GeV; 0-2 raw events at the CP-even coupling points), so any central value or per-bin MC error would be noise and the old placeholder (mcstat 3.2e-5/bin, 9.7e-4 events in total) exceeded the 95 % UL. Stated bound instead: events at 500 fb^-1 in the ZH SR, mu_WH-scaled, negligible against the ZH background of 0.47 events.", info=whsig()["info"], ul95_events_500_total=float(sum(v["ul95_zero_support_500"] for v in whsig()["info"].values())), bound_vs_zh_background_500=float(sum(v["ul95_zero_support_500"] for v in whsig()["info"].values())/0.4687), coupling_points_raw_in_zh_sr={t: int(len(nw.get(t, []))) for t in WHP}),
 frozen_code_reference={}
)
out["coupling"]["SM_template_vs_HC_lambda1"]["sum_quad_at_1_1"] = float((co_z[:, 0] + co_z[:, 1] + co_z[:, 2]).sum())
FF = {}
for tag, f in (("corrected_nominal", "ff2_nominal"), ("frozen", None)):
    d = json.load(open(P + "/work/final_ntuples/final.json" if f is None else f"{Zd}/{f}.json"))
    FF[tag] = {k: dict(s=v["s"], b=v["b"], sigma_b=v["sigma_b"], Z_eq1=v["Z_eq1"], Z_syst_counting=v["Z_syst_counting"], mu95_cls_discretised=v["mu95_cls"], fit_Z_syst=d["fit"][k]["Z_syst"], fit_mu95_syst=d["fit"][k]["mu95_syst"]) for k, v in d["results"].items()}
out["frozen_code_reference"] = FF
json.dump(out, open(VW + "/zh_channel_inputs.json", "w"), indent=0)
print("written", VW + "/zh_channel_inputs.json", NB, "bins; signal sum", SM_REF.sum(), "quad sum(1,1)", out["coupling"]["SM_template_vs_HC_lambda1"]["sum_quad_at_1_1"])
print({d["point"]: (round(d["obs_total"], 5), round(d["pred_total"], 5), round(d["pull"], 2)) for d in clo})
