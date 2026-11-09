#!/usr/bin/env python3
"""ZH erratum analysis: artefact fractions (Q2), rate table + lepton contamination + disjoint-split closure (Q3), CMS calibration kappa.
Usage: python3 -P zh_analyze.py   (reads zh_check/out/*.npz, frozen work/final_ntuples/{final,verify}.json; writes zh_check/out/analysis.json)"""
import glob, json, os, sys, numpy as np
P = "/eos/home-r/rjiang/vbs_zh_codex_starter"; Z = f"{P}/p2/combination/zh_check"; OUT = f"{Z}/out"
VER = json.load(open(f"{P}/work/final_ntuples/verify.json")); FIN = json.load(open(f"{P}/work/final_ntuples/final.json"))
MU, SIG = FIN["resolution"]["mu"], FIN["resolution"]["sigma_core"]; OPT = FIN["optimum"]; MZ = 91.1876
exec(open(f"{Z}/zh_ffmod_lib.py").read())          # ff_expand etc. without the sample-level scenario machinery
SAMPLES = {"F_QCD_llajj_vbs": (VER["F_QCD_llajj_vbs"]["sigma_used_fb"], 1.0), "F_EW_llajj_vbs": (VER["F_EW_llajj_vbs"]["sigma_used_fb"], 1.0),
           "F_QCD_llajj_nomjj": (VER["F_QCD_llajj_nomjj"]["sigma_used_fb"], 1.0), "B_QCD_zaajj_nomjj": (VER["B_QCD_zaajj_nomjj"]["sigma_used_fb"], 0.9783),
           "T_tta": (VER["T_tta"]["sigma_used_fb"], 1.0), "T_tWa": (VER["T_tWa"]["sigma_used_fb"], 1.0)}
def load(sample, kind):
    ch = sorted(glob.glob(f"{OUT}/{sample}__c[0-9][0-9][0-9]_{kind}.npz")); A = {}; off = 0; N = 0; par = []
    for i, c in enumerate(ch):
        d = np.load(c); n = int(d["nev_total"]); N += n
        for k in d.files:
            if k != "nev_total": A.setdefault(k, []).append(d[k] + (off if k == "evt" else 0))
        L = len(d["evt"]) if "evt" in d.files else 0; par.append(np.full(L, int(c.split("__c")[1][:3]) % 2))
        off += 10**8
    A = {k: np.concatenate(v) for k, v in A.items()}; A["par"] = np.concatenate(par); A["N"] = N; A["nch"] = len(ch); return A
res = {}
# ---------------------------------------------------------------- Q2: artefact fractions on the direct samples
def sel_levels(d):
    with np.errstate(invalid="ignore"):
        two = (d["ng"] >= 2) & np.isfinite(d["mll"])
        z = two & (np.abs(d["mll"] - MZ) < 25) & (d["g1pt"] > 25) & (d["g2pt"] > 25) & (d["mllgg"] > 100)
        v = z & (d["mjj"] > 500) & (d["detajj"] > 3.5) & (d["nj"] >= 2)
        sr = v & (d["mgg"] > MU - 2*SIG) & (d["mgg"] < MU + 2*SIG)
        wide = v & (d["mgg"] > 105) & (d["mgg"] < 165)
    return {"2 photons (pT>20) + OSSF": two, "+ Z window, pT>25, mllgg>100": z, "+ VBS (mjj>500, deta>3.5)": v, "+ VBS, 105<mgg<165": wide, "+ VBS + mgg window (frozen SR)": sr}
Q2 = {}
for s in ("F_QCD_llajj_vbs", "F_EW_llajj_vbs", "F_QCD_llajj_nomjj", "T_tta", "T_tWa", "B_QCD_zaajj_nomjj"):
    d = load(s, "dir")
    if d["nch"] == 0: continue
    sig, k = SAMPLES[s]; we = sig*k/d["N"]; q = {"N_events": d["N"], "w_evt_fb": we, "levels": {}}
    # classes of the leading two selected photons, in events with 2 photons
    g = d["gcls"]
    for lab, m in sel_levels(d).items():
        row = {}
        for kk, name in ((1, "prompt"), (2, "lepton"), (3, "genuine"), (4, "artefact")):
            cnt = int(((g[m, 0] == kk).sum() + (g[m, 1] == kk).sum())); row[name] = cnt
        ev_fake_art = int((m & ((g[:, 0] == 4) | (g[:, 1] == 4))).sum()); ev_fake_any = int((m & (np.isin(g[:, 0], (2, 3, 4)) | np.isin(g[:, 1], (2, 3, 4)))).sum())
        ev_gen = int((m & (np.isin(g[:, 0], (2, 3)) | np.isin(g[:, 1], (2, 3))) & ~((g[:, 0] == 4) | (g[:, 1] == 4))).sum())
        row.update(raw_events=int(m.sum()), events_with_nonprompt_photon=ev_fake_any, events_with_artefact=ev_fake_art, events_nonprompt_without_artefact=ev_gen,
                   artefact_event_fraction=(ev_fake_art/ev_fake_any if ev_fake_any else None), weighted_yield_fb=float(m.sum()*we))
        npn = row["lepton"] + row["genuine"] + row["artefact"]; row["artefact_photon_fraction"] = (row["artefact"]/npn if npn else None)
        if row["artefact"]: 
            a = np.concatenate([d["g"][m & (g[:, i] == 4), i, 0] for i in range(2)]); row["artefact_pt_q"] = np.percentile(a, [5, 50, 95]).tolist()
        q["levels"][lab] = row
    Q2[s] = q
res["Q2"] = Q2
# ---------------------------------------------------------------- rate table
RT = {}
for s in ("F_QCD_llajj_vbs", "F_EW_llajj_vbs", "F_QCD_llajj_nomjj"):
    A = {}
    for f in sorted(glob.glob(f"{OUT}/{s}__c[0-9][0-9][0-9]_rate.npz")):
        d = np.load(f)
        for k in d.files:
            if k != "nev_total": A[k] = A.get(k, 0) + d[k]
    RT[s] = A
tot = {k: RT["F_QCD_llajj_vbs"][k] + RT["F_EW_llajj_vbs"][k] for k in RT["F_QCD_llajj_vbs"]}
def rr(a, den): return np.where(den > 0, a/np.maximum(den, 1), 0)
res["rate"] = dict(pt_bins=[25, 35, 50, 75, 100, 150, 1000], eta_bins=["barrel |eta|<1.5", "endcap 1.5-2.5"], **{k: tot[k].tolist() for k in ("den", "num_gen", "num_art", "num_lep", "num_old")},
                   rate_gen=rr(tot["num_gen"], tot["den"]).tolist(), rate_gen_err=(np.sqrt(np.maximum(tot["num_gen"], 1))/np.maximum(tot["den"], 1)).tolist(),
                   rate_art=rr(tot["num_art"], tot["den"]).tolist(), rate_old=rr(tot["num_old"], tot["den"]).tolist(), rate_lep=rr(tot["num_lep"], tot["den"]).tolist(),
                   px=(tot["xh"].sum(0)/tot["xh"].sum()).tolist(), x_mean=float((tot["xh"].sum(0)*0.5*(np.linspace(0, 1.5, 16)[1:] + np.linspace(0, 1.5, 16)[:-1])).sum()/tot["xh"].sum()),
                   x_mean_art=float((tot["xh_art"].sum(0)*0.5*(np.linspace(0, 1.5, 16)[1:] + np.linspace(0, 1.5, 16)[:-1])).sum()/max(tot["xh_art"].sum(), 1)),
                   per_sample={s: dict(den=float(RT[s]["den"].sum()), gen=float(RT[s]["num_gen"].sum()), art=float(RT[s]["num_art"].sum()), lep=float(RT[s]["num_lep"].sum()), old=float(RT[s]["num_old"].sum())) for s in RT})
# ---------------------------------------------------------------- closure: rate from even chunks applied to odd chunks and vice versa
def rate_from(par):
    A = {}
    for s in ("F_QCD_llajj_vbs", "F_EW_llajj_vbs"):
        for f in sorted(glob.glob(f"{OUT}/{s}__c[0-9][0-9][0-9]_rate.npz")):
            if int(f.split("__c")[1][:3]) % 2 != par: continue
            d = np.load(f)
            for k in ("den", "num_gen", "xh"): A[k] = A.get(k, 0) + d[k]
    return A
CL = {}
def evgrp_err(evt, w):
    if len(w) == 0: return 0.0
    u, inv = np.unique(evt, return_inverse=True); return float(np.sqrt((np.bincount(inv, weights=w)**2).sum()))
for sample in ("F_QCD_llajj_vbs", "F_EW_llajj_vbs"):
    dd, ff = load(sample, "dir"), load(sample, "ffm")
    for parA in (0, 1):
        A = rate_from(parA); B = 1 - parA
        if not np.any(A.get("den", 0)): continue
        rate = A["num_gen"]/np.maximum(A["den"], 1); px = A["xh"].sum(0)/A["xh"].sum()
        mB = ff["par"] == B; Fb = {k: v[mB] for k, v in ff.items() if k not in ("par", "N", "nch")}
        X = ff_expand(Fb, rate=rate, px=px); g = dd["gcls"]
        mD = dd["par"] == B
        with np.errstate(invalid="ignore"):
            base = mD & (dd["npr"] == 1) & (dd["ng"] == 2) & np.isfinite(dd["mll"]) & (np.abs(dd["mll"] - MZ) < 25) & (dd["g1pt"] > 25) & (dd["g2pt"] > 25) & (dd["mllgg"] > 100) & (dd["nj"] >= 2)
            gen2 = base & (((g[:, 0] == 1) & (g[:, 1] == 3)) | ((g[:, 0] == 3) & (g[:, 1] == 1)))
            prd = (np.abs(X["mll"] - MZ) < 25) & (X["g1pt"] > 25) & (X["g2pt"] > 25) & (X["mllgg"] > 100)
            for lab, cd, cx in (("Z + 2 photons (pT>25), no VBS", np.ones(len(dd["mll"]), bool), np.ones(len(X["mll"]), bool)),
                                ("+ mjj>500, deta>3.5", (dd["mjj"] > 500) & (dd["detajj"] > 3.5), (X["mjj"] > 500) & (X["detajj"] > 3.5))):
                o = gen2 & cd; p = prd & cx; n_o = int(o.sum()); pred = float(X["wr"][p].sum()); err = evgrp_err(X["evt"][p], X["wr"][p])
                CL.setdefault(sample, []).append(dict(rate_from=("even" if parA == 0 else "odd") + " chunks", applied_to=("odd" if B else "even") + " chunks", selection=lab,
                    observed_genuine_events=n_o, predicted_events=pred, predicted_err=err, ratio=(n_o/pred if pred > 0 else None),
                    ratio_err=((n_o/pred)*np.hypot(1/np.sqrt(max(n_o, 1)), err/pred) if pred > 0 and n_o > 0 else None)))
res["closure"] = CL
# ---------------------------------------------------------------- CMS-like calibration (arXiv:2105.12780 Table 2, Z gamma gamma, ee + mumu)
def cms_sel(l1, l2, flav, mll, g1, g2):
    lead = np.fmax(l1, l2); sub = np.fmin(l1, l2); thr = np.where(flav == 11, 35.0, 30.0)
    with np.errstate(invalid="ignore"): return np.isfinite(mll) & (mll > 55) & (lead > thr) & (sub > 15) & (g1 > 20) & (g2 > 20)
dB = load("B_QCD_zaajj_nomjj", "dir"); gB = dB["gcls"]
dRgg = np.hypot(dB["g"][:, 0, 1] - dB["g"][:, 1, 1], (dB["g"][:, 0, 2] - dB["g"][:, 1, 2] + np.pi) % (2*np.pi) - np.pi)
with np.errstate(invalid="ignore"):
    mB = cms_sel(dB["l1pt"], dB["l2pt"], dB["flav"], dB["mll"], dB["g1pt"], dB["g2pt"]) & (dB["ng"] >= 2) & (dRgg > 0.4)
yB = mB.sum()*SAMPLES["B_QCD_zaajj_nomjj"][0]*SAMPLES["B_QCD_zaajj_nomjj"][1]/dB["N"]; nB = int(mB.sum())
fN = load("F_QCD_llajj_nomjj", "ffm"); dN = load("F_QCD_llajj_nomjj", "dir")
XN = ff_expand({k: v for k, v in fN.items() if k not in ("par", "N", "nch")}, rate=np.array(res["rate"]["rate_gen"]), px=np.array(res["rate"]["px"]))
mN = cms_sel(XN["l1pt"], XN["l2pt"], XN["flav"], XN["mll"], XN["g1pt"], XN["g2pt"])
wF = SAMPLES["F_QCD_llajj_nomjj"][0]/dN["N"]; yF = float(XN["wr"][mN].sum()*wF); eF = evgrp_err(XN["evt"][mN], XN["wr"][mN])*wF
RCMS = 140.0/225.0; RMC = yF/yB if yB > 0 else None
res["calibration"] = dict(CMS_record="arXiv:2105.12780, JHEP 10 (2021) 174, doi:10.1007/JHEP10(2021)174, Table 2 (Zgg, eegg + mumugg)",
    CMS_misid_jets=[42, 98], CMS_expected_signal=[68, 157], R_CMS=RCMS, R_CMS_rel_unc=float(np.hypot(np.hypot(4/42, 9/42) if False else 0.25, 0.07)),
    prompt_Zaajj_nomjj_fb=float(yB), prompt_raw=nB, FF_Zajj_nomjj_fb=yF, FF_err_fb=eF, R_MC=RMC, kappa=(RCMS/RMC if RMC else None),
    kappa_err=(RCMS/RMC*np.hypot(eF/yF, 1/np.sqrt(max(nB, 1))) if RMC else None))
json.dump(res, open(f"{OUT}/analysis.json", "w"), indent=1, default=lambda o: o.tolist() if isinstance(o, np.ndarray) else str(o))
print(json.dumps(res["calibration"], indent=1)); print("written")
