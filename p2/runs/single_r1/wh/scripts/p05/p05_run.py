#!/usr/bin/env python3
"""single_r1 WH Phase 05: inventory (SHA256, sum-of-weights closure, N_MC rule), Delphes object efficiencies, m_gg peak,
baseline cutflow and SR yields with per-source estimation method / N_eff / 95% UL, closure tests of the three non-prompt /
mis-ID methods, cut-based optimisation on expected quantities.  Output: wh/work/p05/p05.json (+ pickled OPT for 06/07).
Usage: python3 -P p05_run.py"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import whana as A
from scipy import optimize
OUT = f"{A.WH}/work/p05"; os.makedirs(OUT, exist_ok=True)
S = A.Store()
J = dict(missing=[k for k in A.R if k not in S.T])

# ------------------------------------------------------------------ inventory
inv = {}
for k, r in A.R.items():
    if k not in S.M: continue
    M = S.M[k]; nc, nb, nn = A.verify_sha(M)
    row = dict(files=len(M["files"]), nev=M["nev"], N_gen=r["N"], sumw_pb=M["sumw"], nneg=M["nneg"], sha_checked=nc, sha_bad=nb, sha_noref=nn,
               k=r["k"], factors=r["factors"], cls=r["cls"], role=r["role"])
    if r["csv"] is not None:
        row["sumw_csv"] = float(r["csv"]["sum_weights_pb_signed"]); row["sumw_ratio"] = M["sumw"]/row["sumw_csv"]
        row["files_csv"] = int(r["csv"]["n_files"]); row["nev_csv"] = int(r["csv"]["N_Delphes"])
    inv[k] = row
bad = [k for k, v in inv.items() if v["sha_bad"] or ("sumw_ratio" in v and abs(v["sumw_ratio"] - 1) > 1e-4) or ("nev_csv" in v and v["nev"] != v["nev_csv"])]
J["inventory"] = inv; J["inventory_bad"] = bad
if bad: print("INVENTORY MISMATCH:", bad)
J["nmc"] = A.nmc_check(S)
J["eff_delphes"] = {t: A.EFF_D[t].tolist() for t in "emg"}; J["eff_cms"] = {t: A.CMS_EFF[t]["eff"] for t in "emg"}
J["eff_counts"] = {k: v.tolist() for k, v in S.effH.items()}

CLE = {}
cl_e = dict(A.BASE, mjj=0., deta=0., met=0., bveto=False, j2pt=25., j1pt=25.)     # relaxed region (no VBS / MET / b cuts), fit range
for k in ("F_QCD_llajj_loose", "ZH_F_EW_llajj_vbs", "V_WWa_WH", "V_WZa_WH", "V_ZZa_WH"):
    if k not in S.T: continue
    T, w, use = S.rows(k, "D", A.SC0); mD = A.sel(T, cl_e, window=False) & (T["cat"] == "EG")
    if A.R[k]["ovl"] is not None: mD &= T["npr"] <= A.R[k]["ovl"]
    out = dict(direct=float(w[mD].sum()), direct_raw=int(mD.sum()))
    for nm, sc in (("pred_delphes6b", dict(A.SC0, egrate="delphes", noC=True)), ("pred_scenario_nom", dict(A.SC0, noC=True))):
        T2, w2, use2 = S.rows(k, "EG", sc)
        if T2 is None: out[nm] = 0.0; continue
        m2 = A.sel(T2, cl_e, window=False) & use2; out[nm] = float(w2[m2].sum()); out[nm + "_raw"] = int(m2.sum())
    CLE[k] = out
J["closure_eg"] = CLE
for k, v in CLE.items():     # closure factor C = direct / weighted(Delphes 6b rate) in the relaxed region, applied to the weighted e->gamma rows
    if v.get("pred_delphes6b", 0) > 0 and v["direct_raw"] >= 10:
        C = v["direct"]/v["pred_delphes6b"]; dC = C*np.sqrt(1/v["direct_raw"] + 1/max(v.get("pred_delphes6b_raw", 1), 1))
        S.ceg[k] = (C, dC); v["C"] = C; v["C_stat"] = dC
S.cache.clear(); S.wcache.clear()
J["eg_closure_factor"] = {k: list(v) for k, v in S.ceg.items()}

# ------------------------------------------------------------------ m_gg peak (Delphes EW signal, loose selection)
T, w, use = S.rows("S_EW_WHjj", "D", A.SC0)
c0 = dict(A.BASE, mjj=0., deta=0., met=0., bveto=False)
m = A.sel(T, c0, window=False) & use; x = T["mgg"][m]
h, e = np.histogram(x, bins=60, range=(110, 140)); cc = 0.5*(e[1:] + e[:-1]); cw = (cc > 121) & (cc < 129)
(pA, MU, SIG), cov = optimize.curve_fit(lambda q, a, mu, s: a*np.exp(-0.5*((q - mu)/s)**2), cc[cw], h[cw], p0=[h.max(), 125, 2])
SIG = abs(SIG); q = np.sort(x[(x > 110) & (x < 140)]); n = len(q); kk = int(0.683*n); SEFF = float((q[kk:] - q[:n - kk]).min()/2)
J["peak"] = dict(mu=float(MU), sigma_core=float(SIG), sigma_core_err=float(np.sqrt(cov[2, 2])), sigma_eff=SEFF, n=int(len(x)),
                 frac_120_130=float(((x > 120) & (x < 130)).mean()))
print("peak", J["peak"])

# ------------------------------------------------------------------ groups, uncertainty model for the optimisation
GROUPS = [("EW W±Hjj (signal)", ["S_EW_WHjj"]), ("QCD W±H (+jets, MLM)", ["H_QCD_WH_mlm"]), ("EW W→τν feed-down", ["S_EW_WHjj_taunu"]),
          ("EW Wγγjj", ["B_EW_Waajj_nomjj"]), ("QCD Wγγjj", ["B_QCD_Waajj_nomjj"]),
          ("Wγ+jets, 1 non-prompt γ", ["F_EW_Wajj_nomjj", "F_QCD_Wajjj_nomjj"]), ("W+jets, 2 non-prompt γ", ["F_Wjjjj"]),
          ("top: tt̄γγ, tt̄γ, tWγ, tt̄jj", ["T_ttaa_1l", "T_tta_1l", "T_tWa_1l", "T_ttjj_1l"]),
          ("tt̄H, tHq, tHW", ["H_ttH_1l", "H_ttH_dilep_wh", "H_tHq_lep", "H_tHW_1l"]),
          ("ZH (EW, QCD, gg, ττ), lost ℓ", ["ZH_ew_zhjj_zll", "ZH_qcd_zhjj_zll", "H_ggZH_wh", "H_ZH_tautau_wh"]),
          ("Zγγjj, lost ℓ", ["ZH_B_QCD_zaajj_nomjj", "ZH_B_EW_zaajj_vbs_is1h", "ZH_B_EW_zaajj_vbs_is2", "ZH_B_EW_zaajj_vbs_is3"]),
          ("e→γ: Zγjj, WWγ/WZγ/ZZγ", ["F_QCD_llajj_loose", "ZH_F_EW_llajj_vbs", "V_WWa_WH", "V_WZa_WH", "V_ZZa_WH"]),
          ("non-prompt ℓ: γγ+3j, VBF H, ggF H", ["Q_aajjj", "H_VBFH_jj", "H_ggF_jj_nomjj"])]
J["groups"] = GROUPS
def summary(c, L=500., sc=A.SC0, sigdef="a"): return A.summary(S, c, L, sc, sigdef)

# ------------------------------------------------------------------ baseline cutflow (500 fb^-1)
OPEN = dict(A.BASE, l1pt=20., veto2=1e9, ratio=(0., 0.), fit=(95., 180.), met=-1., j2pt=25., j1pt=25., mjj=0., deta=0., bveto=False)
STEPS = [("1 lepton pT>25, >=2 photons, >=2 jets pT>25", dict(l1pt=25.)), ("+ 2nd-lepton veto (pT>10)", dict(veto2=10.)),
         ("+ pT/m_gg > 1/3, 1/4; 105<m_gg<160", dict(ratio=(1/3, 1/4), fit=(105., 160.))), ("+ MET > 30", dict(met=30.)),
         ("+ 2 jets pT>30", dict(j2pt=30., j1pt=30.)), ("+ m_jj > 500", dict(mjj=500.)), ("+ |Δη_jj| > 2.5", dict(deta=2.5)),
         ("+ b-veto", dict(bveto=True)), ("+ 120<m_gg<130", None)]
cf, c = [], dict(OPEN)
for name, upd in STEPS:
    win = upd is None
    if upd: c.update(upd)
    Y = A.yields(S, c, window=win)
    cf.append(dict(step=name, **{k: dict(y500=v["y"]*500, n=v["nraw"]) for k, v in Y.items()}))
J["cutflow_base"] = cf

# ------------------------------------------------------------------ SR yields with method / N_eff / UL
def sr_table(c, L=500.):
    Y = A.yields(S, c, detail=True); tab = {}
    for k, y in Y.items():
        r = A.R[k]; wb = A.wbar(S, k, c)*L
        row = dict(y=y["y"]*L, mc=np.sqrt(y["var"])*L, nraw=y["nraw"], neff=y["neff"], method=y["method"], wbar=wb, l2=y["l2"]*L,
                   cls=r["cls"], role=r["role"], comp={t: {kk: (vv*L if kk in ("y", "y_direct", "y_noVBS") else vv) for kk, vv in d.items() if kk != "var"} for t, d in y["comp"].items()})
        if y["nraw"] == 0 and y["y"] <= 0: row.update(y_central=1.14*wb, ul95=3.0*wb, rule="zero support: central 1.14 w̄ (100 %), 95 % UL = 3 w̄")
        elif y["l2"] > 0: row["rule"] = "L2 VBS-factorised component(s), 100 % uncertainty"
        tab[k] = row
    return tab
J["sr_base"] = sr_table(A.BASE)

# ------------------------------------------------------------------ closures
CL = {}
for k in ("F_Wjjjj", "T_ttjj_1l", "F_QCD_Wajjj_nomjj", "F_EW_Wajj_nomjj", "T_tta_1l", "T_tWa_1l"):
    if k not in S.H: continue
    H = S.H[k]; cls = "T" if k.startswith("T_") else "W"
    R6 = A.R6A[cls]                                               # [eta region, jet-pT bin]
    pred_d = np.einsum("pemj,ej->pem", H["cg_pred"], R6)          # Delphes per-jet rate (FORMAT 6a)
    jc = 0.5*(A.JPT[:-1] + np.minimum(A.JPT[1:], 300.))           # scenario f_jg at the jet-pT bin centre
    fs = np.array([[1e-3*(x/50.)**-0.5*(2.0 if e else 1.0) for x in jc] for e in (0, 1)])
    pred_s = np.einsum("pemj,ej->pem", H["cg_pred"], fs)
    dirr = H["cg_dir"]                                            # [photon pT, eta, mjj, dR-to-GenJet class]
    rawd = H["cg_dir_raw"]
    sc = 1e3*A.R[k]["k"]/A.R[k]["N"]
    CL[k] = dict(direct_all=float(dirr.sum()*sc), direct_raw=int(rawd.sum()), direct_dR_lt02=float(dirr[..., 0].sum()*sc),
                 direct_dR_02_04=float(dirr[..., 1].sum()*sc), direct_dR_gt04=float(dirr[..., 2].sum()*sc),
                 pred_delphes6a=float(pred_d.sum()*sc), pred_scenario_nom=float(pred_s.sum()*sc),
                 by_mjj=dict(direct=(dirr.sum((0, 1, 3))*sc).tolist(), direct_raw=rawd.sum((0, 1, 3)).tolist(),
                             pred_delphes6a=(pred_d.sum((0, 1))*sc).tolist(), pred_scenario=(pred_s.sum((0, 1))*sc).tolist()),
                 by_pt=dict(direct=(dirr.sum((1, 2, 3))*sc).tolist(), direct_raw=rawd.sum((1, 2, 3)).tolist(),
                            pred_delphes6a=(pred_d.sum((1, 2))*sc).tolist(), pred_scenario=(pred_s.sum((1, 2))*sc).tolist()),
                 unit="fb at 1/fb (1-fake level: lepton pT>25, n_prompt_photons = %d)" % (0 if k in ("F_Wjjjj", "T_ttjj_1l") else 1))
J["closure_jg"] = CL
CLL = {}
for k in ("Q_aajjj", "Q_aajj", "H_VBFH_jj", "H_ggF_jj_nomjj"):
    if k not in S.H: continue
    H = S.H[k]; sc = 1e3*A.R[k]["k"]/A.R[k]["N"]
    pred1 = H["cl_pred"].sum()*sc            # unit per-jet weight
    CLL[k] = dict(direct=float(H["cl_dir"].sum()*sc), direct_raw=int(H["cl_dir_raw"].sum()), pred_unit=float(pred1),
                  njets_raw=int(H["cl_pred_raw"].sum()), f_eff_direct=float(H["cl_dir"].sum()/max(H["cl_pred"].sum(), 1e-30)),
                  by_mjj_direct=(H["cl_dir"].sum(0)*sc).tolist(), by_mjj_direct_raw=H["cl_dir_raw"].sum(0).tolist(),
                  by_mjj_pred_unit=(H["cl_pred"].sum((0, 2))*sc).tolist(),
                  unit="fb at 1/fb; events with >= 2 reco photons pT>20; f_eff_direct = Delphes direct non-prompt leptons per candidate jet")
J["closure_jl"] = CLL


# ------------------------------------------------------------------ cut-based optimisation (expected, 500/fb, def. a, Z_syst)
J["base_summary"] = summary(A.BASE)[0]
WIN = {"120-130": (120., 130.), "±1.5σ": (MU - 1.5*SIG, MU + 1.5*SIG), "±2σ": (MU - 2*SIG, MU + 2*SIG), "±1σ_eff·1.5": (MU - 1.5*SEFF, MU + 1.5*SEFF)}
GRID = dict(win=list(WIN.values()), ratio=[(1/3, 1/4), (0.35, 0.25), (0.40, 0.30)], met=[0., 20., 30., 40., 50.], mtw=[0., 20., 40.],
            zgg=[99., 1.5, 1.0, 0.7], meg=[0., 10.], j2pt=[30., 40.], ptgg=[0., 40., 80., 120.])
MJJ = [300., 400., 500., 600., 700., 800., 1000., 1200.]; DETA = [2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
def fom(c): t = summary(c)[0]; return t["Zsyst"], t["s"], t["b"]
def pick(cands):
    zs = [fom(x) for x in cands]; zmax = max(z[0] for z in zs)
    ok = [i for i, z in enumerate(zs) if z[0] >= 0.97*zmax]; i = max(ok, key=lambda i: zs[i][1]); return cands[i], zs[i], zs
OPT = dict(A.BASE); HIST = []
for it in range(5):
    old = json.dumps(OPT, sort_keys=True)
    for kk, vals in GRID.items():
        OPT, z, _ = pick([dict(OPT, **{kk: v}) for v in vals]); HIST.append((it, kk, str(OPT[kk]), z[0], z[1], z[2]))
    OPT, z, _ = pick([dict(OPT, mjj=a, deta=b2) for a in MJJ for b2 in DETA]); HIST.append((it, "mjj,deta", f"{OPT['mjj']},{OPT['deta']}", z[0], z[1], z[2]))
    print("iter", it, z, OPT)
    if json.dumps(OPT, sort_keys=True) == old: break
J["opt_history"] = HIST; J["OPT"] = OPT
SC = {}
for a in MJJ:
    for b2 in DETA:
        t = summary(dict(OPT, mjj=a, deta=b2))[0]; SC[f"{a:.0f},{b2:.1f}"] = dict(Z=t["Z"], Zsyst=t["Zsyst"], s=t["s"], b=t["b"])
J["scan_mjj_deta_500"] = SC
# stability: one grid step around the optimum in every variable
stab = {}
for kk, vals in list(GRID.items()) + [("mjj", MJJ), ("deta", DETA)]:
    if OPT[kk] not in vals: continue
    i = vals.index(OPT[kk]); stab[kk] = {str(vals[j]): fom(dict(OPT, **{kk: vals[j]}))[0] for j in (i - 1, i, i + 1) if 0 <= j < len(vals)}
J["opt_stability"] = stab
J["opt_summary"] = summary(OPT)[0]; J["sr_opt"] = sr_table(OPT)
cf, c = [], dict(OPEN)
for name, upd in STEPS[:-1] + [("+ optimised cuts (zgg, mtw, ptgg, m_eγ, ratio, jets, MET)", {kk: OPT[kk] for kk in ("ratio", "met", "mtw", "zgg", "meg", "j2pt", "j1pt", "ptgg", "mjj", "deta")}), (f"+ m_gg window {OPT['win'][0]:.1f}-{OPT['win'][1]:.1f}", None)]:
    win = upd is None
    if upd: c.update(upd)
    Y = A.yields(S, c, window=win); cf.append(dict(step=name, **{k: dict(y500=v["y"]*500, n=v["nraw"]) for k, v in Y.items()}))
J["cutflow_opt"] = cf
json.dump(J, open(f"{OUT}/p05.json", "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
print("base", J["base_summary"]); print("opt", J["opt_summary"]); print("wrote", f"{OUT}/p05.json")
