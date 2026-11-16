# exec'd at the end of final_analysis_ff_dump.py (namespace of the frozen analysis + corrected fake rows). Dumps per-bin m_gg templates (events per fb^-1, BR applied once) for the ZH SR at the FROZEN optimum.
import numpy as _np
EDG2 = _np.arange(105.0, 165.01, 2.0); CEN2 = 0.5*(EDG2[1:] + EDG2[:-1]); NB2 = len(CEN2)
OUTD = os.environ["DUMP_OUT"]
cw = dict(OPT, wk=99.)                       # all frozen cuts except the m_gg window
SCALE_NAMES = {"S_EW_ZHjj": ("scale_sig", "pdf_sig"), "H_QCD_ZHjj": ("scale_hqcd",), "H_ggZH": ("scale_higgs_other",), "H_ttH": ("scale_higgs_other",), "H_tHW": ("scale_higgs_other",), "H_ZH_tautau": ("scale_higgs_other",),
               "B_QCD_Zaajj_vbs": ("scale_prompt_qcd",), "F_QCD_Zajj": ("scale_efake_qcd_ll",), "F_EW_Zajj": ("scale_efake_ew",), "T_ttaa": ("scale_prompt_ew",), "T_tta": ("scale_fake1_qcd",), "T_tWa": ("scale_fake1_qcd",)}
for i in (1, 2, 3): SCALE_NAMES[f"B_EW_Zaajj_vbs_is{i}"] = ("scale_prompt_ew",)
PROC_GROUP = {"S_EW_ZHjj": "zhjj_ew", "H_QCD_ZHjj": "zhjj_qcd"}
TJ = TS["processes"]
def th_rel(sid):
    nm, px, grp = THMAP[sid]; key = nm if nm in TJ else px; return TJ[key]
nph2 = {"F_QCD_Zajj", "F_EW_Zajj"}
def sig_shape(shift=None):
    d = DATA["S_EW_ZHjj"]; pre, lg, jb, vbs, win, wide = masks(d, cw); m = pre & lg & jb & vbs & wide
    x = d["mgg"][m]
    if shift == "sc_hi": x = x*1.005
    elif shift == "sc_lo": x = x*0.995
    elif shift == "res_hi": x = MU + (x - MU)*1.10
    elif shift == "res_lo": x = MU + (x - MU)*0.90
    return _np.histogram(x, bins=EDG2)[0].astype(float)
HS0 = sig_shape(); HSWIN = float(((CEN2 > MU - OPT["wk"]*SIG) & (CEN2 < MU + OPT["wk"]*SIG)).dot(HS0)); xw = DATA["S_EW_ZHjj"]["mgg"]
_pre, _lg, _jb, _vbs, _win, _wide = masks(DATA["S_EW_ZHjj"], OPT); HSWIN_EXACT = float(raw(DATA["S_EW_ZHjj"], _pre & _lg & _jb & _vbs & _win))
def templ(sid):
    r = REG[sid]; y, e, nw, nwd, meth, det = estimate(sid, OPT); gc = genmjj_corr(sid, OPT); f = SCALE.get(sid, 1.0)*gc[0]; y1, e1 = y*f, e*f
    if r["kind"] == "res":
        nu = y1*HS0/HSWIN_EXACT          # window events of the signal sample set the normalisation, shape = signal shape, per fb^-1
    else:
        if sid in FFD_ and FFMODE == "ff":
            dd = dict(FFD_[sid]); dd["w"] = dd["wr"]*r["w_evt_fb"]; p, l, j, v, w_, wd = masks(dd, dict(OPT, mjj=OPT["mjj"])); m = p & l & j & v & wd
            fw, lam = fwin_w(dd["mgg"][m], dd["w"][m], OPT) if m.sum() >= 5 else (0.0, 0.0)
            if m.sum() < 5: m = p & wd; fw, lam = fwin_w(dd["mgg"][m], dd["w"][m], OPT)
        else:
            d = DATA[sid]; p, l, j, v, w_, wd = masks(d, OPT); mm = d["mgg"][p & l & j & v & wd]
            if len(mm) < 5: mm = d["mgg"][p & wd]
            fw, lam = fwin(mm, OPT)
        x0 = EDG2 - WIDE[0]; Lw = WIDE[1] - WIDE[0]
        cdf = (x0/Lw) if abs(lam) < 1e-6 else (1 - _np.exp(-lam*x0))/(1 - _np.exp(-lam*Lw))
        nu = (y1/max(fw, 1e-12))*_np.diff(cdf)
    err = _np.sqrt(_np.maximum(nu, 0)*(e1**2/y1 if y1 > 0 else 0.0))
    return nu, err, y1, e1, meth, nw, nwd
out = dict(edges=EDG2.tolist(), window=[float(MU - OPT["wk"]*SIG), float(MU + OPT["wk"]*SIG)], mu=float(MU), sigma_core=float(SIG), optimum=OPT, samples={})
for sid, r in REG.items():
    if r.get("missing") or r["role"] == "excl": continue
    nu, err, y1, e1, meth, nw, nwd = templ(sid)
    n = {}
    ths = th_rel(sid); rel_scale = float(ths["scale_sym"]) if "scale_sym" in ths else None
    sn = SCALE_NAMES[sid]
    if sid == "S_EW_ZHjj": n["scale_sig"] = [1 + ths["scale_up"], 1 - ths["scale_down"]]; n["pdf_sig"] = [1 + ths["pdf"], 1 - ths["pdf"]]
    else: n[sn[0]] = [1 + ths["total"], 1 - ths["total"]]
    n["lumi"] = [1 + LUMI_UNC, 1 - LUMI_UNC]; n["pheff"] = [1.02, 0.98] if sid in nph2 else [1.04, 0.96]; n["lepeff"] = [1.02, 0.98]
    if sid in nph2: n["fakerate"] = [1.2, 0.8]
    if sid.startswith(("B_QCD_Zaajj", "B_EW_Zaajj")): n["zh_offshell"] = [1 + OFFSHELL_UNC, 1 - OFFSHELL_UNC]
    if sid.startswith("B_EW_Zaajj"): n["zh_int_zaa"] = [1 + INT_ZAA, 1 - INT_ZAA]
    if sid == "H_ggZH": n["zh_ggzh_norm"] = [2.0, 0.5]
    gcv = genmjj_corr(sid, OPT)
    if sid in AUX: n[f"zh_genmjj_{sid}"] = [1 + gcv[1], 1 - gcv[1]]
    rs = (float(_np.hypot(0.5, FFDD[sid])) if sid in FFSIDS else 0.5) if r["syst"] == "fake" else 0.10
    n[f"zh_norm_{sid}"] = [1 + rs, max(1 - rs, 1e-3)]
    shp = {}
    if sid == "S_EW_ZHjj":
        for nm_, (a_, b_) in dict(phscale=("sc_hi", "sc_lo"), phres=("res_hi", "res_lo")).items():
            shp[nm_] = dict(up=(y1*sig_shape(a_)/HSWIN_EXACT).tolist(), down=(y1*sig_shape(b_)/HSWIN_EXACT).tolist())
    out["samples"][sid] = dict(role=r["role"], kind=r["kind"], per_fb=dict(nominal=nu.tolist(), mcstat=err.tolist(), y_window=float(y1), mc_window=float(e1), method=meth, raw_win=int(nw), raw_wide=int(nwd)), norm=n, shape=shp, syst_rel=rs)
# coupling templates (per fb^-1, sample weights include k = ZF x BGG): per-bin sums over the SR-without-window events
if all(t in KREG for t in KPTS):
    ch = {}
    for tag, d in KREG.items():
        d_ = d["d"]; pre, lg, jb, vbs, win, wide = masks(d_, cw); m = pre & lg & jb & vbs & wide
        ch[tag] = dict(sumw=(_np.histogram(d_["mgg"][m], bins=EDG2)[0]*d["w"]).tolist(), raw=_np.histogram(d_["mgg"][m], bins=EDG2)[0].tolist(), w=d["w"], lam=KPTS.get(tag), cA=CPPTS.get(tag))
    out["coupling_points"] = ch

# corrected fake-factor cutflow (500 fb^-1, before the generator-mjj correction C): steps as in the frozen cutflow()
FFCF = {}
for sid_ in FFD_:
    dd = dict(FFD_[sid_]); wgt = dd["wr"]*REG[sid_]["w_evt_fb"]*500.0; c = OPT
    with _np.errstate(invalid="ignore"):
        lo, hi = c["zwin"] if isinstance(c["zwin"], tuple) else (MZ - c["zwin"], MZ + c["zwin"])
        pre = _np.isfinite(dd["mll"]) & (dd["ng"] >= 2) & (dd["nj"] >= 2); mz = (dd["mll"] > lo) & (dd["mll"] < hi) & (dd["mllgg"] > c["mllgg"])
        mg = (dd["g1pt"] > c["gpt"]) & (dd["g2pt"] > c["gpt"])
        if c["ratio"]: mg &= (dd["g1pt"]/dd["mgg"] > c["ratio"][0]) & (dd["g2pt"]/dd["mgg"] > c["ratio"][1])
        mv = (dd["mjj"] > c["mjj"]) & (dd["detajj"] > c["deta"]); wlo, whi = MU - c["wk"]*SIG, MU + c["wk"]*SIG; win = (dd["mgg"] > wlo) & (dd["mgg"] < whi)
    seq = [("pre-selection: Z candidate + real photon + fake-candidate jet + >=2 tag jets", pre)]; cur = pre
    for nm_, m_ in (("+ Z window & m_llgg", mz), ("+ photon pT, pT/m_gg", mg), ("+ mjj, deta_jj", mv), ("+ m_gg window", win)): cur = cur & m_; seq.append((nm_, cur))
    FFCF[sid_] = [dict(step=nm_, y_500=float(wgt[m_].sum()), n_events=int(len(_np.unique(dd["evt"][m_]))), n_rows=int(m_.sum()), mc_500=float(_evt_err(dd["evt"][m_], wgt[m_]))) for nm_, m_ in seq]
out["ff_cutflow"] = FFCF
json.dump(out, open(OUTD, "w"))
print("DUMPED", OUTD)
