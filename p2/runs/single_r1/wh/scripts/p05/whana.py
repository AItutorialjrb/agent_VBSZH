#!/usr/bin/env python3
"""single_r1 WH Phase 05-07 analysis core (Delphes level only).
Inputs : wh/work/nt/<sample>/*.npz (scripts/p05/ntuple_wh.py over the frozen wh-prod-v1(.1) package, the frozen ZH rows
         and own samples), p2/production/wh/SAMPLES.csv + SHA256SUMS (read-only).
Normalisation (FORMAT §4): sigma x BR [fb] of a set S = 1e3 * k * sum_{i in S} Event.Weight_i[pb] / N_generated.
Estimation per sample and per direct-event category (photon pair / lepton origin, see CATS):
  P    both selected photons prompt (or muon-brem), lepton prompt   -> direct (overlap rule on n_prompt_photons)
  NPG  >= 1 non-prompt photon                                       -> direct, or replaced by F1/F2 per-jet weighting
  EG   >= 1 photon from a prompt electron (Delphes e->gamma)        -> direct, or replaced by EG per-electron weighting
  NPL  non-prompt lepton                                            -> direct, or FL per-jet weighting (max(param, direct))
Rates are declared scenarios (G1 defaults), never tuned: j->gamma f = 1e-3 (pT_j/50)^-0.5 (x2 endcap) x {0.3,1,3};
e->gamma P(e->gamma | gen e) = {1,2,5} %; j->lepton per jet {3e-5, 2e-4, 1e-3}.  Delphes-measured rates (FORMAT §6a/6b) are
used only for closure tests and as robustness variants.
"""
import os, glob, csv, json, numpy as np
from scipy import optimize
E = "/eos/home-r/rjiang/vbs_zh_codex_starter"; P2 = f"{E}/p2"; WP = f"{P2}/production/wh"; WH = f"{P2}/runs/single_r1/wh"; NT = f"{WH}/work/nt"
BRF = dict(BGG=0.00227, WF=0.960076, WFTAU=0.00232439/0.00227, WHAD=0.970555/0.960076, ZF=0.9783, BR_ZLL=0.000152757/0.00227, one=1.0)
NMC_L = 3000.0
LUMIS = (500., 1000., 3000.)

# ------------------------------------------------------------------ SAMPLES.csv (read-only) + frozen-ZH directory rows
CSV = {r["sample"]: r for r in csv.DictReader(open(f"{WP}/SAMPLES.csv"))}
def kfac(desc):
    """'WF*BGG = 0.00217937' -> (factor list, product)"""
    names = [x.strip() for x in desc.split("=")[0].split("*")]
    return names, float(np.prod([BRF[n] for n in names]))
# key: (role, class, br desc, N_generated, overlap max npr (None = no cut), theory group, note)
R = {}
def add(key, role, cls, br, N, ovl, th, note, csvrow=None, src=None):
    R[key] = dict(role=role, cls=cls, br=br, N=int(N), ovl=ovl, th=th, note=note, csv=csvrow, src=src or key)
for s, r in CSV.items():
    if int(r["N_generated_LHE"] or 0) == 0 or s.startswith("ZH_"): continue
    role = ("sig" if s == "S_EW_WHjj" else "qcdwh" if s == "H_QCD_WH_mlm" else "coup" if s.startswith("K_") else
            "xcheck" if s in ("H_QCD_WHjj_fixed", "Q_aajj") else "bkg")
    cls = {"F_EW_Wajj_nomjj": "F1", "F_QCD_Wajjj_nomjj": "F1", "T_tta_1l": "F1", "T_tWa_1l": "F1", "F_Wjjjj": "F2", "T_ttjj_1l": "F2",
           "Q_aajj": "FL", "Q_aajjj": "FL", "H_VBFH_jj": "FL", "F_QCD_llajj_loose": "EG", "V_WWa_WH": "EG", "V_WZa_WH": "EG", "V_ZZa_WH": "EG"}.get(s, "D")
    ovl = {"F_EW_Wajj_nomjj": 1, "F_QCD_Wajjj_nomjj": 1, "F_Wjjjj": 0, "T_ttjj_1l": 0, "F_QCD_llajj_loose": 1}.get(s)
    th = ("sig" if s in ("S_EW_WHjj", "S_EW_WHjj_taunu") or s.startswith("K_") else "qcdwh" if s.startswith("H_QCD_WH") else
          "top" if s.startswith(("T_", "H_tt", "H_tH")) else "higgs" if s.startswith("H_") else "ewaa" if s == "B_EW_Waajj_nomjj" else
          "qcdaa" if s == "B_QCD_Waajj_nomjj" else "fake")
    add(s, role, cls, r["BR_k_factors_applied_once"], r["N_generated_LHE"], ovl, th, r["role"][:90], csvrow=r)
# frozen ZH rows (READ-ONLY), one key per directory, N per directory (SAMPLES.csv notes / V1.1_NOTES.md)
add("ZH_B_QCD_zaajj_nomjj", "bkg", "D", "ZF", 100000, None, "qcdaa", "frozen ZH Zgg jj QCD (no gen mjj cut), lost lepton")
for i, n in (("1h", 20000), ("2", 20000), ("3", 20000)):
    add(f"ZH_B_EW_zaajj_vbs_is{i}", "bkg", "D", "ZF", n, None, "ewaa", "frozen ZH Zgg jj EW (gen mjj>400; C=0.958+-0.061), lost lepton")
add("ZH_ew_zhjj_zll", "bkg", "D", "ZF*BGG", 200000, None, "sig", "frozen ZH EW ZHjj Z->ll, lost lepton")
add("ZH_qcd_zhjj_zll", "bkg", "D", "ZF*BGG", 100000, None, "qcdwh", "frozen ZH QCD ZHjj Z->ll, lost lepton")
add("ZH_F_EW_llajj_vbs", "bkg", "EG", "one", 500000, 1, "fake", "frozen ZH EW ll gamma jj (gen mjj>400), e->gamma")
add("ZH_B_QCD_zaajj_vbs", "xcheck", "D", "ZF", 100000, None, "qcdaa", "frozen ZH Zgg jj QCD gen mjj>400 (cross-check only)")
add("H_ggF_jj_nomjj", "bkg", "FL", "BGG", 59945, None, "higgs", "own sample (single_r1 idx 42): ggF H+2j HEFT LO, no gen mjj cut")
R["Q_aajjj"]["role"] = "bkg"
for k, r in R.items():
    names, prod = kfac(r["br"] if "=" in r["br"] else r["br"] + " = 0")
    assert names.count("BGG") <= 1 and names.count("WF") + names.count("WFTAU") <= 2 and names.count("ZF") + names.count("BR_ZLL") <= 1, k
    if r["csv"] is not None: assert abs(prod - float(r["csv"]["k"]))/prod < 2e-5, (k, prod, r["csv"]["k"])
    r["k"], r["factors"] = prod, names

# ------------------------------------------------------------------ loading
COLS = None
def load(key, tables=("D", "F1", "F2", "FL", "EG")):
    fs = sorted(glob.glob(f"{NT}/{key}/{key}__c*.npz"))
    out = {t: {} for t in tables}; H = {}; M = dict(nev=0, sumw=0.0, files=[], sha=[], sha_gen=[], nneg=0)
    for ci, f in enumerate(fs):
        d = np.load(f, allow_pickle=False)
        for t in tables:
            ks = [k for k in d.files if k.startswith(t + "_")]
            for k in ks: out[t].setdefault(k[len(t) + 1:], []).append(d[k] + ci*10**9 if k.endswith("_evt") else d[k])
        for k in d.files:
            if k.startswith("H_"): H[k[2:]] = H.get(k[2:], 0) + d[k]
        M["nev"] += int(d["M_nev"].sum()); M["sumw"] += float(d["M_sumw"].sum()); M["nneg"] += int(d["M_nneg"].sum())
        M["files"] += list(d["M_files"]); M["sha"] += list(d["M_sha"]); M["sha_gen"] += list(d["M_sha_gen"])
    for t in tables:
        out[t] = {k: np.concatenate(v) for k, v in out[t].items()} if out[t] else {}
    return out, H, M, len(fs)

SHA = {}
for line in open(f"{WP}/SHA256SUMS"):
    h, p = line.split(); SHA[p] = h
def verify_sha(M):
    """returns (n_checked, n_bad, n_noref); production/wh files are checked against SHA256SUMS"""
    nc = nb = nn = 0
    for f, h, hg in zip(M["files"], M["sha"], M["sha_gen"]):
        for ff, hh in ((f, h), (f[:-5] + "_gen.root", hg)):
            rel = ff.split("/production/wh/")[-1] if "/p2/production/wh/" in ff else None
            if rel is None: nn += 1; continue
            nc += 1; nb += int(SHA.get(rel) != hh)
    return nc, nb, nn

# ------------------------------------------------------------------ object efficiencies (D-WH-4 default: CMS-like)
CMS_EFF = {  # lib/scripts/analysis/final_analysis.py (ZH final), copied verbatim
 "e": dict(eta=[0, 1.5, 2.5], pt=[10, 20, 30, 50, 1e9], eff=[[0.70, 0.80, 0.88, 0.92], [0.65, 0.75, 0.83, 0.88]]),
 "m": dict(eta=[0, 1.5, 2.4], pt=[10, 20, 30, 50, 1e9], eff=[[0.93, 0.96, 0.96, 0.96], [0.93, 0.96, 0.96, 0.96]]),
 "g": dict(eta=[0, 1.4442, 2.5], pt=[20, 30, 40, 60, 1e9], eff=[[0.85, 0.88, 0.92, 0.92], [0.80, 0.83, 0.88, 0.88]])}
EFF_D = None   # Delphes efficiencies measured from gen-matched prompt objects (set by set_delphes_eff)
def set_delphes_eff(H):
    global EFF_D
    EFF_D = {t: np.where(H[f"eff_{t}_den"] > 0, H[f"eff_{t}_num"]/np.maximum(H[f"eff_{t}_den"], 1), 1.0) for t in "emg"}
def _bins(t, pt, eta):
    e = np.clip(np.searchsorted(CMS_EFF[t]["eta"], np.abs(np.nan_to_num(eta)), side="right") - 1, 0, 1)
    p = np.clip(np.searchsorted(CMS_EFF[t]["pt"], np.nan_to_num(pt), side="right") - 1, 0, 3); return e, p
def lookup(tab, t, pt, eta):
    """tab: 'cms' (assumed CMS-like) or 'delphes' (measured, gen-matched)"""
    e, p = _bins(t, pt, eta); return (np.asarray(CMS_EFF[t]["eff"]) if tab == "cms" else EFF_D[t])[e, p]
def eff_ratio(t, pt, eta):
    with np.errstate(all="ignore"):
        r = lookup("cms", t, pt, eta)/np.maximum(lookup("delphes", t, pt, eta), 1e-3)
    return np.where(np.isfinite(pt), r, 1.0)

# ------------------------------------------------------------------ fake / non-prompt rates (declared scenarios)
def f_jg(pt, eta, s=1.0): return s*1e-3*(np.maximum(pt, 1.0)/50.)**-0.5*np.where(np.abs(eta) > 1.5, 2.0, 1.0)
F_EG = dict(low=0.01, nom=0.02, high=0.05); F_JL = dict(low=3e-5, nom=2e-4, high=1e-3); S_JG = dict(low=0.3, nom=1.0, high=3.0)
# Delphes-measured rates (FORMAT §6a W+jets class, §6b electrons) for closure / variants
JPT = np.array([25, 35, 50, 75, 100, 150, 1e5])
R6A = {"W": np.array([[0.0036, 0.0041, 0.0053, 0.0073, 0.0087, 0.0100], [0.0035, 0.0037, 0.0062, 0.0082, 0.0107, 0.0151]])*1e-2,
       "T": np.array([[0.0058, 0.0061, 0.0057, 0.0040, 0.0034, 0.0076], [0.0008, 0.0045, 0.0042, 0.0035, 0.0036, 0.0152]])*1e-2}
EPT = np.array([25, 40, 60, 100, 1e5]); R6B = np.array([[3.81, 4.93, 6.85, 6.24], [9.22, 12.26, 15.20, 14.53]])*1e-2
def r6a(pt, eta, cls="W"):
    i = np.clip(np.searchsorted(JPT, pt, side="right") - 1, 0, 5); e = (np.abs(eta) > 1.5).astype(int); return R6A[cls][e, i]
def r6b(pt, eta):
    i = np.clip(np.searchsorted(EPT, pt, side="right") - 1, 0, 3); e = (np.abs(eta) > 1.5).astype(int); return R6B[e, i]

# ------------------------------------------------------------------ per-row weights
def row_weights(key, tab, T, sc):
    """fb per row at 1 fb^-1 for table T of sample key, scenario dict sc"""
    r = R[key]; w = 1e3*r["k"]*T["w"]/r["N"]
    if sc.get("eff", "cms") == "cms":
        lp = T["l1prompt"] > 0.5
        fl = np.abs(T["l1pid"]) == 11
        re = np.where(fl, eff_ratio("e", T["l1pt"], T["l1eta"]), eff_ratio("m", T["l1pt"], T["l1eta"]))
        w = w*np.where(lp, re, 1.0)
        for g in ("g1", "g2"):
            real = (T[f"{g}fake"] == 0) & (T[f"{g}prompt"] > 0.5)
            w = w*np.where(real, eff_ratio("g", T[f"{g}pt"], T[f"{g}eta"]), 1.0)
    if tab == "F1":
        w = w*(f_jg(T["fk1pt"], T["fk1eta"], S_JG[sc.get("jg", "nom")]) if sc.get("jgrate") != "delphes" else r6a(T["fk1pt"], T["fk1eta"], "T" if key.startswith("T_") else "W"))
    elif tab == "F2":
        if sc.get("jgrate") == "delphes":
            c = "T" if key.startswith("T_") else "W"; w = w*r6a(T["fk1pt"], T["fk1eta"], c)*r6a(T["fk2pt"], T["fk2eta"], c)
        else:
            s = S_JG[sc.get("jg", "nom")]; w = w*f_jg(T["fk1pt"], T["fk1eta"], s)*f_jg(T["fk2pt"], T["fk2eta"], s)
    elif tab == "FL":
        w = w*F_JL[sc.get("jl", "nom")]
    elif tab == "EG":
        rate = r6b(T["egpt"], T["egeta"]) if sc.get("egrate") == "delphes" else F_EG[sc.get("eg", "nom")]
        w = w*rate/np.maximum(lookup("delphes", "e", T["egpt"], T["egeta"]), 0.05)
    return w

def cats(T):
    """direct-row category: P, NPG, EG, NPL (precedence NPG > EG > NPL > P)"""
    npg = ((T["g1prompt"] < 0.5) & (T["g1lm"] == 0)) | ((T["g2prompt"] < 0.5) & (T["g2lm"] == 0))
    eg = (T["g1lm"] == 1) | (T["g2lm"] == 1)
    npl = T["l1prompt"] < 0.5
    c = np.full(len(npg), "P", dtype="<U3"); c[npl] = "NPL"; c[eg] = "EG"; c[npg] = "NPG"
    return c

# ------------------------------------------------------------------ selection
BASE = dict(l1pt=25., veto2=10., ratio=(1/3, 1/4), fit=(105., 160.), met=30., j2pt=30., mjj=500., deta=2.5, bveto=True,
            win=(120., 130.), zgg=99., mtw=0., meg=0., ptgg=0., j1pt=30.)
def sel(T, c, window=True, fitrange=True):
    with np.errstate(invalid="ignore"):
        m = (T["l1pt"] > c["l1pt"]) & ~(T["l2pt"] > c["veto2"]) & (T["ng20"] >= 2)
        m &= (T["g1pt"] > c["ratio"][0]*T["mgg"]) & (T["g2pt"] > c["ratio"][1]*T["mgg"])
        m &= (T["met"] > c["met"]) & (T["j2pt"] > c["j2pt"]) & (T["j1pt"] > c["j1pt"]) & (T["mjj"] > c["mjj"]) & (T["detajj"] > c["deta"])
        if c["bveto"]: m &= T["nb"] == 0
        if c["zgg"] < 90: m &= T["zgg"] < c["zgg"]
        if c["mtw"] > 0: m &= T["mtw"] > c["mtw"]
        if c["ptgg"] > 0: m &= T["ptgg"] > c["ptgg"]
        if c["meg"] > 0:   # electron channel Z(ee)-veto on m(e, photon)
            ee = np.abs(T["l1pid"]) == 11
            m &= ~(ee & ((np.abs(T["mlg1"] - 91.19) < c["meg"]) | (np.abs(T["mlg2"] - 91.19) < c["meg"])))
        if c.get("bdt") is not None:
            assert "bdt" in T, "BDT cut requested but no scores attached"
            m &= T["bdt"] > c["bdt"]
        if fitrange: m &= (T["mgg"] > c["fit"][0]) & (T["mgg"] < c["fit"][1])
        if window: m &= (T["mgg"] > c["win"][0]) & (T["mgg"] < c["win"][1])
    return m

# ------------------------------------------------------------------ data store
class Store:
    """all samples loaded once; rows per (key, table) with categories and per-scenario weights computed on demand"""
    def __init__(self, keys=None, verbose=True):
        self.T, self.H, self.M, self.nf = {}, {}, {}, {}
        for k in (keys or R):
            tabs, H, M, nf = load(k)
            if nf == 0:
                if verbose: print("MISSING ntuples:", k)
                continue
            self.T[k], self.H[k], self.M[k], self.nf[k] = tabs, H, M, nf
            if "D" in tabs and tabs["D"]: tabs["D"]["cat"] = cats(tabs["D"])
        Hs = {}
        for k in ("S_EW_WHjj", "B_EW_Waajj_nomjj", "B_QCD_Waajj_nomjj", "H_QCD_WH_mlm", "S_EW_WHjj_taunu"):
            for h in ("eff_e_num", "eff_e_den", "eff_m_num", "eff_m_den", "eff_g_num", "eff_g_den"):
                if k in self.H: Hs[h] = Hs.get(h, 0) + self.H[k][h]
        set_delphes_eff(Hs); self.effH = Hs
        self.wcache = {}; self.ceg = {}; self.cache = {}
    def rows(self, key, tab, sc):
        """(table dict, weights[fb at 1/fb], usable mask) applying the per-class direct/weighted policy"""
        T = self.T[key].get(tab)
        if not T: return None, None, None
        ck = (key, tab, json.dumps(sc, sort_keys=True))
        if ck not in self.wcache:
            w = row_weights(key, tab, T, sc); r = R[key]; use = np.ones(len(w), bool)
            if tab == "EG" and not sc.get("noC"): w = w*self.ceg.get(key, (1.0, 0.0))[0]   # e->gamma closure factor (p05)
            if r["ovl"] is not None and tab == "D": use &= T["npr"] <= r["ovl"]
            if r["ovl"] is not None and tab in ("F1", "F2", "EG"): use &= T["npr"] <= r["ovl"]
            if tab == "D":
                c = T["cat"]
                if r["cls"] in ("F1", "F2"): use &= c != "NPG"
                if r["cls"] == "EG": use &= c != "EG"
                if r["cls"] == "FL": use &= c != "NPL"     # direct non-prompt leptons handled in yields() (max rule)
            self.wcache[ck] = (w, use)
        w, use = self.wcache[ck]
        return T, w, use

SC0 = dict(eff="cms", jg="nom", eg="nom", jl="nom")
WIDE = (105., 160.)
def is_res(k): return "BGG" in R[k]["factors"]
def fwin_exp(x, w, win):
    """fraction of a weighted exponential (unbinned MLE) m_gg spectrum on WIDE that falls in the window"""
    x = np.asarray(x, float) - WIDE[0]; w = np.asarray(w, float); Lw = WIDE[1] - WIDE[0]; lo, hi = win[0] - WIDE[0], win[1] - WIDE[0]
    if len(x) < 3 or w.sum() <= 0: return (hi - lo)/Lw, 0.0
    W = w.sum(); xm = (w*x).sum()/W
    nll = lambda lam: (np.log(Lw) if abs(lam) < 1e-7 else -(np.log(abs(lam)) - lam*xm) + np.log(abs(1 - np.exp(-lam*Lw))))
    lam = optimize.minimize_scalar(nll, bounds=(-0.15, 0.15), method="bounded").x
    if abs(lam) < 1e-7: return (hi - lo)/Lw, 0.0
    return float((np.exp(-lam*lo) - np.exp(-lam*hi))/(1 - np.exp(-lam*Lw))), float(lam)
LOOSE = dict(l1pt=25., veto2=10., ratio=(1/3, 1/4), fit=WIDE, met=-1., j2pt=30., j1pt=30., mjj=0., deta=0., bveto=False, win=(120., 130.),
             zgg=99., mtw=0., meg=0., ptgg=0.)
def component(S, k, tab, c, sc, window):
    """estimate of one (sample, table) component.  Hierarchy (ZH final_analysis.py, adapted):
      L0 direct   : resonant samples, N_eff(window) >= 10           -> window count
      L1 shape    : continuum samples, N_eff(fit range) >= 10       -> fit-range count x f_win (own exponential MLE)
      L2 factorised (100 %): N(all cuts except m_jj, |deta_jj|) x eps(m_jj, deta | loose objects) [x f_win for continuum]
      zero        : no support anywhere -> y = 0 here; the caller sets central 1.14 w_bar (100 %), 95 % UL = 3 w_bar
    window=False returns the fit-range (105-160) yield (no window, no hierarchy beyond L0)."""
    T, w, use = S.rows(k, tab, sc)
    if T is None: return None
    base = use.copy()
    if R[k]["cls"] == "FL" and tab == "D": base &= T["cat"] != "NPL"
    mF = sel(T, c, window=False) & base
    yF, vF = float(w[mF].sum()), float((w[mF]**2).sum()); neF = yF*yF/vF if vF > 0 else 0.0
    if not window: return dict(y=yF, var=vF, neff=neF, n=int(mF.sum()), nev=int(len(np.unique(T["evt"][mF]))), method="fit range")
    inw = (T["mgg"] > c["win"][0]) & (T["mgg"] < c["win"][1])
    mW = mF & inw; yW, vW = float(w[mW].sum()), float((w[mW]**2).sum()); neW = yW*yW/vW if vW > 0 else 0.0
    out = dict(n=int(mW.sum()), nev=int(len(np.unique(T["evt"][mW]))), y_direct=yW, neff_direct=neW)
    res = is_res(k)
    if res and neW >= 10: return dict(out, y=yW, var=vW, neff=neW, method="L0 direct")
    if not res and neF >= 10:
        f, lam = fwin_exp(T["mgg"][mF], w[mF], c["win"]); return dict(out, y=yF*f, var=vF*f*f, neff=neF, method="L1 shape", f_win=f, lam=lam)
    # L2: VBS-factorised
    cn = dict(c, mjj=0., deta=0., bdt=None); mN = sel(T, cn, window=False) & base
    lo = dict(LOOSE, win=c["win"]); mL = sel(T, lo, window=False) & base
    mLV = mL & (T["mjj"] > c["mjj"]) & (T["detajj"] > c["deta"])
    if c.get("bdt") is not None: mLV &= T["bdt"] > c["bdt"]          # the BDT cut is factorised together with the VBS cuts
    yL = float(w[mL].sum()); eps = float(w[mLV].sum())/yL if yL > 0 else 0.0
    if res: yN, vN = float(w[mN & inw].sum()), float((w[mN & inw]**2).sum()); f = 1.0
    else:
        yN, vN = float(w[mN].sum()), float((w[mN]**2).sum()); f, _ = fwin_exp(T["mgg"][mN], w[mN], c["win"])
    if eps <= 0 and mL.sum() > 0: eps = 0.5/(mL.sum() + 1)
    y = yN*eps*f
    return dict(out, y=y, var=y*y, neff=(yN*yN/vN if vN > 0 else 0.0), method="L2 VBS-factorised (100 %)", eps_vbs=eps, f_win=f, y_noVBS=yN)

def yields(S, c, sc=SC0, window=True, keys=None, detail=False):
    """per sample: dict(y [fb at 1/fb], var, nraw, neff, comp{table: component}); FL class: y = max(param FL, direct NPL)"""
    out = {}
    for k in (keys or S.T):
        y = v = 0.0; nr = 0; comp = {}; ck = (k, json.dumps(c, sort_keys=True, default=str), json.dumps(sc, sort_keys=True), window)
        if ck in S.cache: out[k] = S.cache[ck]; continue
        for tab in ("D", "F1", "F2", "FL", "EG"):
            d = component(S, k, tab, c, sc, window)
            if d is not None: comp[tab] = d
        if R[k]["cls"] == "FL" and "D" in comp:      # direct Delphes non-prompt leptons (max rule)
            T, w, use = S.rows(k, "D", sc); mn = sel(T, c, window) & (T["cat"] == "NPL")
            comp["D_NPL"] = dict(y=float(w[mn].sum()), var=float((w[mn]**2).sum()), n=int(mn.sum()), nev=int(len(np.unique(T["evt"][mn]))), method="direct NPL")
            if "FL" in comp and comp["D_NPL"]["y"] > comp["FL"]["y"]: comp["FL"] = dict(comp["D_NPL"], method="direct NPL (> parametrised)")
        meth = []
        for tab, d in comp.items():
            if tab == "D_NPL": continue
            y += d["y"]; v += d["var"]; nr += d["nev"]
            if d["n"] > 0 or d["y"] > 0: meth.append(f"{tab}:{d['method'].split(' ')[0]}")
        out[k] = dict(y=y, var=v, nraw=nr, neff=(y*y/v if v > 0 else 0.0), method=",".join(meth) or "none",
                      l2=sum(d["y"] for t, d in comp.items() if t != "D_NPL" and d["method"].startswith("L2")), comp=comp)
        S.cache[ck] = out[k]
    return out

REL = dict(D=0.10, F1=1.0, F2=1.5, FL=1.0, EG=1.0)   # optimisation-level normalisation uncertainty per estimation class
def summary(S, c, L=500., sc=SC0, sigdef="a"):
    """expected s, b, MC stat and sigma_b for the optimisation figure of merit (Z_syst): per-class normalisation (REL),
    L2 components 100 %, zero-support sources at 1.14 w_bar with 100 %, luminosity 2.5 %, MC stat"""
    Y = yields(S, c, sc)
    s = b = vs = vb = var = 0.0
    for k, y in Y.items():
        r = R[k]
        if r["role"] in ("xcheck", "coup"): continue
        yy, vv = y["y"]*L, y["var"]*L*L
        if r["role"] == "sig" or (sigdef == "b" and r["role"] == "qcdwh"): s += yy; vs += vv; continue
        if y["nraw"] == 0 and y["y"] <= 0: yy = 1.14*wbar(S, k, c)*L; var += yy**2
        l2 = y["l2"]*L; vv = vv - l2**2 if l2 > 0 else vv
        b += yy; vb += max(vv, 0.0); var += (REL[r["cls"]]*(yy - l2))**2 + l2**2
    sb = np.sqrt(var + vb + (0.025*b)**2)
    return dict(s=s, b=b, s_mc=float(np.sqrt(vs)), b_mc=float(np.sqrt(vb)), sigma_b=float(sb), Z=zeq1(s, b), Zsyst=z_syst(s, b, sb)), Y

def wbar(S, k, c):
    """mean per-row weight [fb at 1/fb] in the loose object-level region: the per-event weight scale for zero-support ULs"""
    wl = []
    for t in ("D", "F1", "F2", "FL", "EG"):
        T, w, use = S.rows(k, t, SC0)
        if T is None: continue
        mm = sel(T, dict(LOOSE, win=c["win"], bdt=None), window=False) & use
        if mm.any(): wl.append(w[mm])
    r = R[k]; return float(np.mean(np.concatenate(wl))) if wl else 1e3*r["k"]*S.M[k]["sumw"]/r["N"]/max(S.M[k]["nev"], 1)

GROUP_ROW = {f"ZH_B_EW_zaajj_vbs_is{i}": "ZH_Zaajj_EW_lostlep" for i in ("1h", "2", "3")}   # beam-1 splits of ONE SAMPLES.csv row
def nmc_check(S, L=NMC_L):
    """SPEC_G0 §1.5: N_generated >= max(50k, sigma x BR x 3000/fb) for every sample entering s or b; fails loudly.
    A sample generated as disjoint phase-space splits (frozen ZH EW Zgg jj beam-1 splits is1h/is2/is3 = SAMPLES.csv row
    ZH_Zaajj_EW_lostlep) is checked as one sample (sum of N, sum of sigma); each split is also listed.
    Weighted fake / non-prompt rows (F1, F2, FL, EG classes) follow D-WH-2 (G1 default): effective-N policy, N_eff >= 10 in
    the SR or a direct 95% UL with the conservative variant in the robustness table (checked in the SR, not here)."""
    rows, bad, grp = {}, [], {}
    for k, r in R.items():
        if k not in S.M or r["role"] in ("xcheck", "coup"): continue
        sig_fb = 1e3*S.M[k]["sumw"]/r["N"]     # Sum w / N_generated (pb -> fb)
        rows[k] = dict(N=r["N"], sigma_fb=sig_fb, sigmaBR_fb=sig_fb*r["k"], need=max(5e4, sig_fb*r["k"]*L), cls=r["cls"])
        rows[k]["ratio"] = r["N"]/rows[k]["need"]
        if k in GROUP_ROW:
            g = grp.setdefault(GROUP_ROW[k], dict(N=0, sigmaBR_fb=0.0, members=[])); g["N"] += r["N"]; g["sigmaBR_fb"] += sig_fb*r["k"]; g["members"].append(k)
            rows[k]["policy"] = f"split of {GROUP_ROW[k]} (checked as one sample)"; continue
        if r["N"] < rows[k]["need"]:
            if r["cls"] in ("F1", "F2", "FL", "EG"): rows[k]["policy"] = "D-WH-2 effective-N (weighted rows)"
            else: bad.append(f"{k}: N={r['N']} < {rows[k]['need']:.0f}")
    for g, v in grp.items():
        v["need"] = max(5e4, v["sigmaBR_fb"]*L); v["ratio"] = v["N"]/v["need"]; rows[g] = dict(v, cls="D")
        if v["N"] < v["need"]: bad.append(f"{g}: N={v['N']} < {v['need']:.0f}")
    if bad: raise SystemExit("N_MC >= max(50k, sigma x BR x 3000/fb) VIOLATED:\n  " + "\n  ".join(bad))
    return rows

# ------------------------------------------------------------------ statistics (lib/scripts/analysis/final_analysis.py, copied)
from scipy import stats, optimize
def zeq1(s, b): return float(np.sqrt(2*((s + b)*np.log(1 + s/b) - s))) if b > 0 and s > 0 else 0.0
def zeq1_err(s, b, ds, db):
    h1, h2 = max(1e-6, 1e-3*s), max(1e-6, 1e-3*b)
    gs = (zeq1(s + h1, b) - zeq1(s - h1, b))/(2*h1); gb = (zeq1(s, b + h2) - zeq1(s, max(b - h2, 1e-9)))/(2*h2)
    return float(np.hypot(gs*ds, gb*db))
def z_syst(s, b, sb):
    if sb <= 0: return zeq1(s, b)
    t1 = (s + b)*np.log((s + b)*(b + sb**2)/(b**2 + (s + b)*sb**2)); t2 = b**2/sb**2*np.log(1 + sb**2*s/(b*(b + sb**2)))
    return float(np.sqrt(max(2*(t1 - t2), 0)))
def cls_limit(s, b, sb, alpha=0.05, ss=0.0):
    """median expected 95% CL CLs upper limit on mu: exact Poisson counting; b and s marginalised over log-normals"""
    gx, gw = np.polynomial.hermite_e.hermegauss(30); gw = gw/gw.sum()
    def ln(x, rel):
        if rel <= 0: return np.full(1, x), np.ones(1)
        v = np.log(1 + rel**2); return x*np.exp(np.sqrt(v)*gx - 0.5*v), gw
    bs, wb = ln(b, sb/b if b > 0 else 0); s_, ws = ln(s, ss/s if s > 0 else 0)
    BS, SS = np.meshgrid(bs, s_); W2 = np.outer(ws, wb)
    cdf = lambda n, mu: (W2*stats.poisson.cdf(n, mu*SS + BS)).sum()
    cdf0 = lambda n: (wb*stats.poisson.cdf(n, bs)).sum()
    nn = np.arange(0, int(b + 10*np.sqrt(b + 1) + 10*sb + 20)); nmed = nn[np.searchsorted(np.array([cdf0(k) for k in nn]), 0.5)]
    f = lambda mu: cdf(nmed, mu)/cdf0(nmed) - alpha; hi = 1.0
    while f(hi) > 0: hi *= 2
    return float(optimize.brentq(f, 0, hi)), int(nmed)
