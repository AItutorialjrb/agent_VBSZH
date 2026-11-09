#!/usr/bin/env python3
"""Background-model yields per class with lower/upper bounds (05a v2, after review wh_05a_background HOLD). Usage:
  bash scripts/envrun.sh python3 -P scripts/bg_yields.py [--noiso] [--tag T] [--ccal-photon c] [--f-electron f] [--f-muon f] [--nonprompt-lo 0.3] [--nonprompt-hi 3] [--nonclosure 0.4] [--floor 0.2]
Writes work/bgmodel/yields<tag>.json.  Block-level regions (NOT the final selection): PRE / VBS / PEAK of scripts/bgmodel.py.
Classes (SPEC D32): prompt_irreducible, fake_photon_1, fake_photon_2, nonprompt_lepton, lost_lepton_egamma, other_higgs, tau_feeddown (+ signal, xcheck).
Bounds (declared; low/high = min/max over the listed variations, multiplied by the tau factor [1, 1+2 r_tau] (nominal 1+r_tau, D9)):
  all rows        : QCD 7-point scale envelope.
  fake photons    : f stat dn/up, veto cut R 0.7/0.3; LOW additionally x NONCLOSURE (0.4, one-sided, one-fake classes only: measured direct/FF closure ~0.39) and x(1-FLOOR);
                    HIGH additionally x(1+FLOOR) (D39 floor 20 %, CMS syst/yield) and the direct count incl. the artefact (kind 4; 3-jet row only, therefore a LOWER LIMIT on the true upper variation).
  non-prompt lept.: misID per jet nominal = f_e + f_mu (2e-5 + 2e-5 placeholder D40); low = x0.3, high = x3 (D36 envelope, D35 reading pending human question a);
                    robustness variants (labelled, NOT bounds): per flavour 2e-4 (medium), 2e-3 (loose), and the x100 scan (beyond D36). Heavy flavour: direct rows (nominal), factorised variant
                    (direct PRE rate x kind-5 eff PEAK/PRE, +-100 %), UL kept as conservative variant; HIGH includes 2 x factorised.
  frozen ZH rows  : generator-cut factors C (bgmodel.CFAC, 04 sec. 15(7)) applied in VBS/PEAK with range low/high (Zajj QCD [1, 2.732], i.e. the 87 % C systematic; Zaajj EW 0.958 +- 0.061);
                    PRE has no mjj cut: nominal C = 1 (LOWER limit), high = C central.
Zero MC support: 95 % Poisson UL = 2.996 x per-event weight (unit) is reported (also for the direct variation), never 0."""
import sys, json, numpy as np
sys.path.insert(0, "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh/scripts")
from bgmodel import *
def _arg(n, d): return float(sys.argv[sys.argv.index(n)+1]) if n in sys.argv else d
ISO = "--noiso" not in sys.argv
OUTTAG = sys.argv[sys.argv.index("--tag")+1] if "--tag" in sys.argv else ""
CCAL = _arg("--ccal-photon", 1.0)      # D39 switch: calibration factor of the per-photon j->gamma rate (one-fake x c, two-fake x c^2)
FE = _arg("--f-electron", 2e-5); FMU = _arg("--f-muon", 2e-5)   # D35 / D40 switch (muon = placeholder)
NPLO = _arg("--nonprompt-lo", 0.3); NPHI = _arg("--nonprompt-hi", 3.0)   # D36 envelope on the light-misID normalisation (human question a)
NONCLO = _arg("--nonclosure", 0.4); FLOOR = _arg("--floor", 0.2)
FNOM = FE+FMU; FL = {"low": NPLO*FNOM, "nom": FNOM, "high": NPHI*FNOM, "rob_med": 2*2e-4, "rob_loose": 2*2e-3, "scan100": 100*FNOM}
CL = {"prompt_irreducible": ["B_QCD_Waajj_nomjj", "B_EW_Waajj_nomjj", "T_ttaa_1l"], "fake_photon_1": ["F_QCD_Wajjj_nomjj", "F_EW_Wajj_nomjj", "T_tta_1l", "T_tWa_1l"], "fake_photon_2": ["F_Wjjjj", "T_ttjj_1l"],
      "nonprompt_lepton": ["Q_aajjj", "H_VBFH_jj", "H_ggF_jj"], "lost_lepton_egamma": ["V_WWa_WH", "V_WZa_WH", "V_ZZa_WH", "ZH_Zaajj_QCD_nomjj_lostlep", "ZH_Zaajj_EW_lostlep", "ZH_Zajj_eFake"],
      "other_higgs": ["H_QCD_WH_mlm", "H_ggZH_wh", "H_ZH_tautau_wh", "H_ttH_1l", "H_ttH_dilep_wh", "H_tHq_lep", "H_tHW_1l", "ZH_EW_ZHjj_lostlep", "ZH_QCD_ZHjj_lostlep"], "tau_feeddown": ["S_EW_WHjj_taunu"], "signal": ["S_EW_WHjj"],
      "xcheck": ["Q_aajj"]}
TAUCLASSES = {"prompt_irreducible", "fake_photon_1", "fake_photon_2", "lost_lepton_egamma", "other_higgs"}   # r_tau measured on W (signal taunu/signal); applied to Z-lepton rows (lost-lepton, ZH) as the same +-100 % envelope: Z->tau tau->l l feed-down is of the same size (BR(tau->l nu nu)=0.35 vs 0.18 per W-lepton...), conservative, +-8 % effect
SC7 = [0, 1, 3, 4, 5, 7, 8]; DATA = {}
def get(s):
    if s not in DATA: DATA[s] = load(s)
    return DATA[s]
def cvec(D, reg):
    """per-row multiplicative C: returns (nominal, low, high)"""
    c = D["cfac"]
    if reg == "PRE": return np.ones(len(c)), np.minimum(1.0, c[:, 0]), np.maximum(1.0, c[:, 0])   # PRE: no mjj cut -> C=1 (lower limit), bounds [min(1,C), max(1,C)]
    return c[:, 0], c[:, 1], c[:, 2]
def sample_yields(s, reg):
    D = get(s)
    if D is None: return None
    R, _ = regions(D, iso=ISO); m = R[reg]; kind = D["kind"]; k = float(SAMP[s]["k"]); Nn = float(SAMP[s]["N_generated_LHE"])
    cn, cl, ch = cvec(D, reg); base = D["w"]*D["norm"]*LUMI
    out = {"n_files": D["n_files"], "n_events_skimmed": D["n_events_skimmed"], "rows_by_kind": D["rows_by_kind"], "cutflow": D["cutflow"], "sumw_over_N_pb": D["sumw_over_N_pb"], "sigma_pb_SAMPLES": SAMP[s]["sigma_pb_pre_decay"]}
    unit_w = float(np.mean(np.abs(D["w"])*D["norm"])*LUMI) if len(D["w"]) else LUMI*1e3*k*float(SAMP[s]["sigma_pb_pre_decay"] or 0)/Nn; out["unit_event_weight"] = unit_w
    def Y(mm, f=None, fk=None, cvar=None, mult=1.0):
        cc = (CCAL if fk == 1 else CCAL**2 if fk == 2 else 1.0) if f is not None else 1.0
        cv = {None: cn, "low": cl, "high": ch}[cvar]
        w = base*cc*mult*cv*(1.0 if f is None else D["f"][:, FC[f]]); r = ysum(w, mm, unit=None)
        if r["nraw"] == 0:
            fu = 1.0 if f is None else (float(np.median(D["f"][(kind == fk), FC[f]])) if (kind == fk).any() else 1.0); r["UL95"] = 2.996*unit_w*fu*cc*mult*(float(np.max(ch)) if len(ch) else 1.0)
        return r
    def scale_env(mm, f=None):
        if "lhe" not in D or len(D["lhe"]) != len(mm) or not mm.any(): return None
        L9 = D["lhe"]; nomc = L9[:, 4] if L9.shape[1] == 9 else L9[:, 22]; ok = np.abs(nomc) > 0; idx = SC7 if L9.shape[1] == 9 else [0, 5, 10, 15, 22, 24, 34, 39]
        w = base*cn*(1.0 if f is None else D["f"][:, FC[f]]); v = [float((w[mm & ok]*L9[mm & ok, i]/nomc[mm & ok]).sum()) for i in idx]; return dict(min=min(v), max=max(v), nominal=float(w[mm].sum()))
    if s in CL["fake_photon_1"] or s in CL["fake_photon_2"]:
        fk = 1 if s in CL["fake_photon_1"] else 2; mm = m & (kind == fk)
        out["nom"] = Y(mm, "nom", fk); [out.__setitem__(v, Y(mm, v, fk)) for v in ("up", "dn", "r03", "r07")]
        out["direct_genuine_kind3"] = Y(m & (kind == 3)); out["direct_all_kind4"] = Y(m & (kind == 4)); out["scale"] = scale_env(mm, "nom")
        k3 = out["direct_genuine_kind3"]
        if fk == 1 and k3["nraw"] > 0:   # closure: observed raw direct-genuine rows vs expected from the FF prediction (same mean row weight)
            mw = k3["Y"]/k3["nraw"]; exp = out["nom"]["Y"]/mw if mw != 0 else 0.0; out["closure"] = dict(observed_raw=k3["nraw"], expected_raw=exp, ratio=k3["nraw"]/exp if exp > 0 else None)
        elif fk == 1:
            out["closure"] = dict(observed_raw=0, expected_raw=out["nom"]["Y"]/unit_w if unit_w > 0 else None, ratio=0.0)
    elif s in CL["nonprompt_lepton"] or s in CL["xcheck"]:
        md = m & (kind == 0); mf = m & (kind == 5); out["heavy_flavour_direct"] = Y(md)
        for t, f in FL.items():
            ws = (base*f)[mf]; r2 = dict(Y=float(ws.sum()), stat=float(np.sqrt((ws**2).sum())), nraw=int(mf.sum()), neff=float(ws.sum()**2/(ws**2).sum()) if mf.any() else 0.0)
            if not mf.any(): r2["UL95"] = 2.996*unit_w*f
            out["fakelep_" + t] = r2
        # factorised heavy-flavour variant: HF direct in PRE x (kind-5 yield PEAK-or-VBS / PRE)
        Rall = {rn: mk for rn, mk in R.items()}; y5 = {rn: float(base[(kind == 5) & mk].sum()) for rn, mk in Rall.items()}
        hfpre = float(base[(kind == 0) & Rall["PRE"]].sum()); eff = (y5[reg]/y5["PRE"]) if y5["PRE"] > 0 else 0.0
        out["heavy_flavour_factorised"] = dict(Y=hfpre*eff, rel_unc=1.0, hf_PRE_direct=hfpre, eff_kind5=eff, nraw_PRE=int(((kind == 0) & Rall["PRE"]).sum()))
        out["scale"] = scale_env(mf)
    else:
        out["nom"] = Y(m); out["scale"] = scale_env(m)
        if s == "ZH_Zajj_eFake":
            ncls1 = (D["ph"][:, :, 3] == 1).sum(1); out["egamma_part"] = Y(m & (ncls1 >= 1)); out["lostlep_part"] = Y(m & (ncls1 == 0)); out["qcd_part"] = Y(m & np.char.startswith(D["dirname"].astype(str), "F_QCD"))
            out["qcd_lostlep_part"] = Y(m & (ncls1 == 0) & np.char.startswith(D["dirname"].astype(str), "F_QCD"))
        if s in ("ZH_Zaajj_QCD_nomjj_lostlep", "B_QCD_Waajj_nomjj"): out["qcd_part"] = out["nom"]
        if np.any(cl != cn) or np.any(ch != cn): out["C_low"] = Y(m, cvar="low"); out["C_high"] = Y(m, cvar="high")
    return out
def run():
    res = {"iso_lepton_0p15": ISO, "lumi_fb": LUMI, "switches": dict(ccal_photon=CCAL, f_electron=FE, f_muon=FMU, nonprompt_lo=NPLO, nonprompt_hi=NPHI, nonclosure=NONCLO, floor=FLOOR, FL=FL), "regions": {}}
    for rn in ("PRE", "VBS", "PEAK"):
        S = {}
        for c, ss in CL.items():
            for s in ss:
                r = sample_yields(s, rn)
                if r is not None: S[s] = r
        sig = S["S_EW_WHjj"]["nom"]["Y"]; tau = S["S_EW_WHjj_taunu"]["nom"]["Y"]; rtau = tau/sig if sig > 0 else 0.0; C = {}
        for c, ss in CL.items():
            lo = nom = hi = 0.0; st2 = 0.0; comps = {}; ulsum = 0.0; uldir = 0.0; missing = [s for s in ss if s not in S]
            for s in ss:
                if s not in S: continue
                r = S[s]; tf = {"low": 1.0, "nom": 1+rtau, "high": 1+2*rtau} if c in TAUCLASSES else {"low": 1.0, "nom": 1.0, "high": 1.0}
                sc = r.get("scale"); smin = (sc["min"]/sc["nominal"] if sc and sc["nominal"] > 0 else 1.0); smax = (sc["max"]/sc["nominal"] if sc and sc["nominal"] > 0 else 1.0); ul = 0.0; uld = 0.0
                if c in ("fake_photon_1", "fake_photon_2"):
                    n_ = r["nom"]["Y"]; ncl = NONCLO if c == "fake_photon_1" else 1.0
                    fl_ = (1-FLOOR)**(1 if c == "fake_photon_1" else 2); fh_ = (1+FLOOR)**(1 if c == "fake_photon_1" else 2)   # floor on the per-photon rate: two-fake follows c^2 (-36 %/+44 %)
                    l_ = min(r["dn"]["Y"], r["r07"]["Y"], n_)*smin*ncl*fl_; k4 = r["direct_all_kind4"]
                    h_ = max(r["up"]["Y"], r["r03"]["Y"], n_, k4["Y"])*smax*fh_; st = r["nom"]["stat"]; ul = r["nom"].get("UL95", 0.0); uld = k4.get("UL95", 0.0)
                elif c in ("nonprompt_lepton", "xcheck"):
                    d = r["heavy_flavour_direct"]["Y"]; hf = r["heavy_flavour_factorised"]["Y"]; n_ = r["fakelep_nom"]["Y"]+hf   # nominal HF = factorised (equals the direct value in PRE by construction; no nominal 0 from zero MC support)
                    l_ = r["fakelep_low"]["Y"]+0.0; h_ = r["fakelep_high"]["Y"]+2*hf+d; st = float(np.hypot(r["fakelep_nom"]["stat"], r["heavy_flavour_direct"]["stat"]))
                    ul = r["fakelep_nom"].get("UL95", 0.0) + r["heavy_flavour_direct"].get("UL95", 0.0)
                else:
                    n_ = r["nom"]["Y"]; cl_ = r["C_low"]["Y"] if "C_low" in r else n_; ch_ = r["C_high"]["Y"] if "C_high" in r else n_
                    l_ = min(n_, cl_, ch_)*smin; h_ = max(n_, cl_, ch_)*smax; st = r["nom"]["stat"]; ul = r["nom"].get("UL95", 0.0)
                nom += n_*tf["nom"]; lo += l_*tf["low"]; hi += h_*tf["high"]; st2 += (st*tf["nom"])**2; ulsum += ul; uldir += uld
                comps[s] = dict(nom=n_*tf["nom"], low=l_*tf["low"], high=h_*tf["high"], stat=st*tf["nom"], UL95_zero_support_nominal=ul, UL95_zero_support_direct_variation=uld)
            C[c] = dict(nom=nom, low=lo, high=hi, stat=float(np.sqrt(st2)), UL95_sum_zero_support_rows=ulsum, UL95_sum_direct_variation=uldir, components=comps, missing_samples=missing)
        tfn = 1+rtau; g = lambda x, k="nom": S[x][k]["Y"] if x in S else 0.0
        qcd = {x: g(x)*tfn for x in ("B_QCD_Waajj_nomjj", "F_QCD_Wajjj_nomjj", "ZH_Zaajj_QCD_nomjj_lostlep", "T_tta_1l", "T_tWa_1l")}; qcd["ZH_Zajj_eFake(QCD part)"] = S["ZH_Zajj_eFake"]["qcd_part"]["Y"]*tfn
        eC = S["ZH_Zajj_eFake"]
        res.setdefault("nuisance_impacts_events", {})[rn] = dict(
            PS_jet_fraction_100pct_nominal_pm45pct={"total_pm": 0.45*sum(qcd.values()), "per_row_yield": qcd, "note": "04:136; correlated across QCD-type rows; for the eFake QCD part it overlaps with the C systematic (take the larger, not the sum); Q_aajj is a cross-check; the ME-jet rows F_Wjjjj/T_ttjj carry LO scale envelope + D27 instead"},
            lepton_coverage_plus105pct_eFake_lostlepton_part={"plus": 1.053*eC["lostlep_part"]["Y"]*tfn, "lostlep_part_yield": eC["lostlep_part"]["Y"]*tfn, "note": "04:139,:181 one-sided; overlaps with C (both act on the eFake QCD part; both removed for that part if the loose-cut sample replaces it)"},
            C_syst_eFake_QCD={"low": eC["C_low"]["Y"]*tfn, "nom": eC["nom"]["Y"]*tfn, "high": eC["C_high"]["Y"]*tfn},
            eFake_egamma_part=eC["egamma_part"]["Y"]*tfn, eFake_lostlep_part=eC["lostlep_part"]["Y"]*tfn)
        res["regions"][rn] = dict(r_tau=rtau, classes=C, samples=S)
    json.dump(res, open(f"{WH}/work/bgmodel/yields{'' if ISO else '_noiso'}{OUTTAG}.json", "w"), indent=1, default=float)
    for rn in ("PRE", "VBS", "PEAK"):
        print(f"== {rn}  (r_tau {res['regions'][rn]['r_tau']:.3f})")
        for c, v in res["regions"][rn]["classes"].items(): print(f"  {c:20s} nom {v['nom']:10.4g} [{v['low']:9.3g}, {v['high']:9.3g}] stat {v['stat']:8.3g} UL0 {v['UL95_sum_zero_support_rows']:.3g} ULdir {v['UL95_sum_direct_variation']:.3g} missing {v['missing_samples']}")
if __name__ == "__main__": run()
