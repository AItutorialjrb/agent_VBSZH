#!/usr/bin/env python3
"""FINAL analysis (Phase 06-08): every yield from Delphes-level reconstructed objects (ntuple.py direct mode).
Inputs : work/final_ntuples/<sample>__cNNN.npz (batch ntuples of production/final), work/m7_analysis/*.npz (Tier-1
         signal / QCD ZHjj and test_v2 samples), work/final_ntuples/verify.json (job verification, sigma).
Output : <out.json> with registry, resolution, optimum, cutflows, yields, results, fit results, scans, checks.
Usage  : python3 -P final_analysis.py <out.json>

Estimation hierarchy per background (all Delphes-level; method recorded per number):
  L0 direct        : sum of weights in the m_gg window, used when >= 10 raw MC events.
  L1 shape (cont.) : continuum samples: N(all cuts, 105<m_gg<165) x f_win(exponential MLE fit of that sample), when
                     the wide-range count has >= 10 raw events.
  L2 VBS-factorised: N(all cuts except mjj/deta/Zeppenfeld [+window via L0/L1]) x eps(VBS | preselection), 100% unc.
  L3 transfer      : no longer used for yields (2026-11-03): ttgamma / tWgamma are now direct Delphes samples with
                     N >= 4 x sigma x BR x 3000 fb^-1; the transfer factor survives only as a cross-check (tf_xcheck).
  UL               : zero raw support: central = 1.14 x w_evt (68% CL Poisson bound), 100% unc.; 95% UL = 3 x w_evt.
Overlap removal (hard/soft photon): samples with one ME photon keep GenTruth n_prompt_photons <= 1 (pT>15, |eta|<2.5,
dR>0.4: the Zgg/ttgg ME phase space); photon-less samples keep n_prompt_photons == 0.
"""
import sys, os, glob, json, numpy as np
from scipy import stats, optimize

OUT = sys.argv[1]
P = "/eos/home-r/rjiang/vbs_zh_codex_starter"; NT = f"{P}/work/final_ntuples"; M7 = f"{P}/work/m7_analysis"
MZ, BGG, ZF = 91.1876, 0.002270, 0.9783
BR_ZLL = 0.033632 + 0.033662          # PDG Z -> ee + mumu (ggZH: Z decayed in Pythia8, e/mu only)
LUMI_UNC = 0.025
# 2026-11-03 additions: theory (scale+PDF per process, correlated within a theory group), off-shell/FSR correction of the
# on-shell-Z Zgg samples, Zggjj EW x QCD interference, ggZH x2/x0.5 normalisation, CMS-like object efficiencies.
TS = json.load(open(f"{P}/work/theory/theory_summary.json"))
OFFSHELL = TS["offshell_Zaa"]["applied_factor"]; OFFSHELL_UNC = TS["offshell_Zaa"]["applied_unc"]/TS["offshell_Zaa"]["applied_factor"]
INT_ZAA = abs(TS["interference_Zaajj"]["frac_of_EW"])
GGZH_LN = np.log(2.0)          # x2 / x0.5 normalisation nuisance (log-normal sigma)
NMC_L = 3000.0                 # N_MC >= sigma x BR x NMC_L required for every sample entering s or b
VER = json.load(open(f"{NT}/verify.json")) if os.path.exists(f"{NT}/verify.json") else {}

def tier1_sigma(s):
    J = [json.load(open(f)) for f in glob.glob(f"{P}/production/v1/{s}/*.json")]
    x = np.array([[float(v) for v in j["lhe_init_xsec_pb_err_pb_max_lprup"].split()[:2]] for j in J]); w = 1/x[:, 1]**2
    return 1e3*(x[:, 0]*w).sum()/w.sum(), len(J), sum(j["n_delphes"] for j in J)
def tv2_sigma(tid, mlm):
    j = json.load(open(glob.glob(f"{P}/production/test_v2/{tid}/*.json")[0]))
    if mlm: return float(j["pythia_sum_line"].split("|")[-2].split()[0])*1e12
    return float(open(f"{P}/production/gridpacks/{tid}_status.txt").read().split("Cross-section :")[1].split()[0])*1e3
def fin_sigma(s): return VER[s]["sigma_used_fb"]

sEW, nEW, _ = tier1_sigma("ew_zhjj_zll"); sQCD, nQCD, _ = tier1_sigma("qcd_zhjj_zll")
# id -> chunks, sigma [fb], k (BR), role, group, syst class, overlap (max n_prompt_photons), kind (res/cont/fake/tf)
def R(chunks, sig, k, role, grp, syst, ovl, kind, src): return dict(chunks=chunks, sig=sig, k=k, role=role, grp=grp, syst=syst, ovl=ovl, kind=kind, src=src)
fin = lambda s: sorted(glob.glob(f"{NT}/{s}__c[0-9][0-9][0-9].npz"))
REG = {
 "S_EW_ZHjj":  R([f"{M7}/S_EW_ZHjj.npz"], sEW, ZF*BGG, "sig", "EW ZHjj (signal)", "other", None, "res", f"Tier-1 v1 ({nEW} jobs, 200k ev)"),
 "H_QCD_ZHjj": R([f"{M7}/H_QCD_ZHjj.npz"], sQCD, ZF*BGG, "qcdzh", "QCD ZHjj", "other", None, "res", f"Tier-1 v1 ({nQCD} jobs, 100k ev)"),
 "H_ggZH":     R(fin("H_ggZH_py8dec"), None, BR_ZLL*BGG, "bkg", "other H->gg", "other", None, "res", "final: gg->ZH loop-induced, Z->ll & H->gg forced in PY8"),
 "H_ttH":      R(fin("H_ttH") + [f"{M7}/tv2_H_ttH.npz"], None, BGG, "bkg", "other H->gg", "other", None, "res", "final + test_v2"),
 "H_ZH_tautau":R(fin("H_ZH_tautau") + [f"{M7}/tv2_H_ZH_tautau.npz"], None, BGG, "bkg", "other H->gg", "other", None, "res", "final + test_v2 (MLM)"),
 "H_tHW":      R([f"{M7}/tv2_H_tHW.npz"], None, BGG, "bkg", "other H->gg", "other", None, "res", "test_v2"),
 **{f"B_QCD_llaa_2j_is{i}": R(fin(f"B_QCD_llaa_2j_is{i}"), None, 1.0, "bkg", "Zgg (QCD+EW)", "other", None, "cont", "final (MLM, highest multiplicity)") for i in range(1, 5)},
 **{f"B_EW_llaajj_is{i}": R(fin(f"B_EW_llaajj_is{i}"), None, 1.0, "bkg", "Zgg (QCD+EW)", "other", None, "cont", "final") for i in range(1, 5)},
 "B_QCD_Zaajj_vbs": R(fin("B_QCD_zaajj_vbs"), None, ZF, "bkg", "Zgg (QCD+EW)", "other", None, "cont", "final, fixed order, on-shell Z->ll, VBS-biased generation"),
 **{f"B_EW_Zaajj_vbs_is{i}": R(fin(f"B_EW_zaajj_vbs_is{i}h") or fin(f"B_EW_zaajj_vbs_is{i}"), None, ZF, "bkg", "Zgg (QCD+EW)", "other", None, "cont", "final, fixed order 4F, on-shell Z->ll, VBS-biased, beam-1 split") for i in (1, 2, 3)},
 "T_ttaa":     R(fin("T_ttaa") + [f"{M7}/tv2_T_ttaa.npz"], None, 1.0, "bkg", "top (ttgg, ttg, tWg)", "other", None, "cont", "final + test_v2"),
 "F_QCD_Zajj": R(fin("F_QCD_llajj_vbs"), None, 1.0, "bkg", "Zg + fake g (QCD+EW)", "fake", 1, "cont", "final, direct Delphes fakes (VBS-biased generation)"),
 "F_EW_Zajj":  R(fin("F_EW_llajj_vbs"), None, 1.0, "bkg", "Zg + fake g (QCD+EW)", "fake", 1, "cont", "final, direct Delphes fakes (VBS-biased generation)"),
 "T_tta":      R(fin("T_tta"), None, 1.0, "bkg", "top (ttgg, ttg, tWg)", "fake", 1, "cont", "final, direct Delphes (ref. Table I: both t -> b l nu), N = 4.05 x sigma x 3000 fb^-1"),
 "T_tWa":      R(fin("T_tWa"), None, 1.0, "bkg", "top (ttgg, ttg, tWg)", "fake", 1, "cont", "final, direct Delphes (ref. Table I: tW-a + t~W+a, both W -> l nu), N = 4.1 x sigma x 3000 fb^-1"),
}
SIGSRC = {"B_QCD_Zaajj_vbs": ("B_QCD_zaajj_vbs", "fin"), **{f"B_EW_Zaajj_vbs_is{i}": ((f"B_EW_zaajj_vbs_is{i}h" if fin(f"B_EW_zaajj_vbs_is{i}h") else f"B_EW_zaajj_vbs_is{i}"), "fin") for i in (1, 2, 3)}, "H_ggZH": ("H_ggZH_py8dec", "fin"), "H_ttH": ("H_ttH", "fin"), "H_ZH_tautau": ("H_ZH_tautau", "fin"), "T_ttaa": ("T_ttaa", "fin"),
          "F_QCD_Zajj": ("F_QCD_llajj_vbs", "fin"), "F_EW_Zajj": ("F_EW_llajj_vbs", "fin"), "H_tHW": ("H_tHW", "tv2"),
          "T_tta": ("T_tta", "fin"), "T_tWa": ("T_tWa", "fin"),
          **{f"B_QCD_llaa_2j_is{i}": (f"B_QCD_llaa_2j_is{i}", "fin") for i in range(1, 5)},
          **{f"B_EW_llaajj_is{i}": (f"B_EW_llaajj_is{i}", "fin") for i in range(1, 5)}}
for k, (s, how) in SIGSRC.items():
    if how == "fin" and s in VER and VER[s]["ok"] > 0: REG[k]["sig"] = fin_sigma(s)
    elif how == "fin" or how.startswith("tv2"):
        try: REG[k]["sig"] = tv2_sigma(s, how == "tv2m" or k == "H_ZH_tautau")
        except Exception: pass
# prompt Zgg+jj: use the VBS-biased fixed-order samples when produced, else the MLM / split samples (never both)
_vbs = {"B_QCD_Zaajj_vbs": "B_QCD_llaa_2j_is", "B_EW_Zaajj_vbs_is": "B_EW_llaajj_is"}
for kv, pref in _vbs.items():
    new = [k for k in REG if k.startswith(kv)]
    if any(REG[k]["chunks"] for k in new): [REG.pop(k) for k in list(REG) if k.startswith(pref)]
    else: [REG.pop(k) for k in new]
MISSING = [k for k, r in REG.items() if not r["chunks"] or r["sig"] is None or not all(os.path.exists(c) for c in r["chunks"])]
if "F_QCD_Zajj" in MISSING: MISSING += [k for k, r in REG.items() if r["kind"] == "tf" and k not in MISSING]
for k in MISSING: REG[k]["missing"] = True

def load(chunks):
    A, off, N = {}, 0, 0
    for c in chunks:
        d = np.load(c); n = int(d["nev_total"])
        for key in d.files:
            if key == "nev_total": continue
            v = d[key] + (off if key == "evt" else 0); A.setdefault(key, []).append(v)
        off += 10**8; N += n
    A = {k: np.concatenate(v) for k, v in A.items()}; A["N"] = N; return A
DATA = {}
for sid, r in REG.items():
    if r.get("missing"): continue
    d = load(r["chunks"])
    if r["ovl"] is not None:
        keep = d["npr"] <= r["ovl"]; r["overlap_removed_rows"] = int((~keep).sum())
        d = {k: (v[keep] if isinstance(v, np.ndarray) and len(v) == len(keep) else v) for k, v in d.items()}
    vs = SIGSRC.get(sid, (None,))[0]
    if vs in VER and VER[vs]["ok"] > 0 and all(os.path.dirname(c) == NT for c in r["chunks"]):
        r["N_verify"] = VER[vs]["n_delphes"]; r["N_closure_ok"] = bool(r["N_verify"] == d["N"])   # ntuples cover exactly the verified jobs
    r["corr"] = OFFSHELL if sid.startswith(("B_QCD_Zaajj", "B_EW_Zaajj")) else 1.0   # off-shell/FSR correction (A4)
    r["N"] = d["N"]; r["w_evt_fb"] = r["sig"]*r["k"]*r["corr"]/d["N"]; d["w"] = np.full(len(d["mll"]), r["w_evt_fb"])
    DATA[sid] = d

# ------------------------------------------------------------------ A1: generator mjj>400 bias of QCD-type VBS-biased samples
# C(c) = Y(no-mjj-cut twin) / Y(VBS-biased sample) at a relaxed Delphes selection with the same VBS-jet, Z-window and photon
# pT cuts (1 photon for Zg+jets, 2 photons in 105-165 GeV for Zgg); applied as a multiplicative correction, its statistical
# uncertainty as a per-process nuisance. EW-type samples: 1.4% (EW ZHjj proxy, work/theory/mjj_resolution.json), not corrected.
GENMJJ = {"F_QCD_Zajj": ("F_QCD_llajj_nomjj", 1), "B_QCD_Zaajj_vbs": ("B_QCD_zaajj_nomjj", 2)}
AUX = {}
for sid, (tw, ng_) in GENMJJ.items():
    ch = fin(tw)
    if sid in DATA and ch and tw in VER and VER[tw]["ok"] > 0:
        d = load(ch); keep = d["npr"] <= (REG[sid]["ovl"] if REG[sid]["ovl"] is not None else 99)
        d = {k: (v[keep] if isinstance(v, np.ndarray) and len(v) == len(keep) else v) for k, v in d.items()}
        AUX[sid] = dict(d=d, w=VER[tw]["sigma_used_fb"]*REG[sid]["k"]/d["N"], N=d["N"], sig=VER[tw]["sigma_used_fb"], ng=ng_, twin=tw)
GMC = {}
def genmjj_corr(sid, c):
    if sid not in AUX: return 1.0, 0.0
    key = (sid, json.dumps(c, sort_keys=True))
    if key in GMC: return GMC[key]
    out = []
    for d, w in ((AUX[sid]["d"], AUX[sid]["w"]), (DATA[sid], REG[sid]["w_evt_fb"]/REG[sid]["corr"])):
        with np.errstate(invalid="ignore"):
            lo, hi = c["zwin"] if isinstance(c["zwin"], tuple) else (MZ - c["zwin"], MZ + c["zwin"])
            m = np.isfinite(d["mll"]) & (d["mll"] > lo) & (d["mll"] < hi) & (d["nj"] >= 2) & (d["mjj"] > c["mjj"]) & (d["detajj"] > c["deta"])
            m &= (d["ng"] >= 1) & (d["g1pt"] > c["gpt"]) if AUX[sid]["ng"] == 1 else (d["ng"] >= 2) & (d["g2pt"] > c["gpt"]) & (d["mgg"] > WIDE[0]) & (d["mgg"] < WIDE[1])
        n = raw(d, m); out.append((n*w, n))
    (ya, na), (yb, nb_) = out
    C = ya/yb if yb > 0 else 1.0; rel = np.sqrt(1/max(na, 1) + 1/max(nb_, 1))
    GMC[key] = (C, rel, na, nb_); return GMC[key]

# ------------------------------------------------------------------ BR applied exactly once (A6) and N_MC >= sigma x BR x L (A10)
# per sample: where each decay happens and which factors enter k. The product of the listed factors must equal k.
BRF = dict(BGG=BGG, ZF=ZF, BR_ZLL=BR_ZLL, one=1.0)
BRDEF = {
 "S_EW_ZHjj":  ("Z->ll in MG5 ME (e,mu)", "H->gg forced in PY8 (cond. BR 1)", ["ZF", "BGG"]),
 "H_QCD_ZHjj": ("Z->ll in MG5 ME (e,mu)", "H->gg forced in PY8 (cond. BR 1)", ["ZF", "BGG"]),
 "H_ggZH":     ("Z->ee/mumu forced in PY8 (cond. BR 1)", "H->gg forced in PY8 (cond. BR 1)", ["BR_ZLL", "BGG"]),
 "H_ttH":      ("t->b l nu in MG5 (l=e,mu)", "H->gg forced in PY8 (cond. BR 1)", ["BGG"]),
 "H_ZH_tautau":("Z->tautau in MG5 ME", "H->gg forced in PY8 (cond. BR 1)", ["BGG"]),
 "H_tHW":      ("t, W -> l nu in MG5", "H->gg forced in PY8 (cond. BR 1)", ["BGG"]),
 "B_QCD_Zaajj_vbs": ("Z->ll in MG5 decay chain", "no H (prompt photons in ME)", ["ZF"]),
 **{f"B_EW_Zaajj_vbs_is{i}": ("Z->ll in MG5 decay chain", "no H (prompt photons in ME)", ["ZF"]) for i in (1, 2, 3)},
 "T_ttaa":     ("t->b l nu in MG5", "no H", ["one"]), "T_tta": ("t->b l nu in MG5", "no H", ["one"]), "T_tWa": ("t, W -> l nu in MG5", "no H", ["one"]),
 "F_QCD_Zajj": ("l+l- in ME (gamma*/Z, no decay chain)", "no H", ["one"]), "F_EW_Zajj": ("l+l- in ME (gamma*/Z, no decay chain)", "no H", ["one"]),
}
BRTAB = {}
for sid, r in REG.items():
    if r.get("missing"): continue
    zdec, hdec, fac = BRDEF[sid]; prod = float(np.prod([BRF[x] for x in fac]))
    if abs(prod - r["k"]) > 1e-12*max(1.0, r["k"]): raise SystemExit(f"BR ledger mismatch for {sid}: k={r['k']} vs product {fac}={prod}")
    if fac.count("BGG") > 1 or fac.count("ZF") + fac.count("BR_ZLL") > 1: raise SystemExit(f"BR factor applied twice for {sid}")
    BRTAB[sid] = dict(z_or_W_decay=zdec, h_decay=hdec, factors=fac, k=r["k"], offshell_corr=r["corr"])
def nmc_check(reg, L=NMC_L):
    """A10: every sample entering s or b must have N_MC >= sigma x BR x L. Fails loudly (SystemExit) otherwise."""
    rows, bad = {}, []
    for sid, r in reg.items():
        if r.get("missing"): continue
        need = r["sig"]*r["k"]*L; rows[sid] = dict(N=r["N"], sigmaBR_fb=r["sig"]*r["k"], sigmaBRL=need, ratio=r["N"]/need, w_evt_L=need/r["N"])
        if r["N"] < need: bad.append(f"{sid}: N={r['N']} < sigma x BR x {L:.0f} = {need:.0f}")
    if bad: raise SystemExit("N_MC >= sigma x BR x L VIOLATED:\n  " + "\n  ".join(bad))
    return rows
NCHECK = nmc_check(REG)
# auxiliary twins (A1) enter b only through the ratio C, whose MC-stat uncertainty is a nuisance; listed and FLAGGED, not exempted silently
for sid, a in AUX.items():
    need = a["sig"]*REG[sid]["k"]*NMC_L
    NCHECK[f"{a['twin']} (aux, ratio only)"] = dict(N=a["N"], sigmaBR_fb=a["sig"]*REG[sid]["k"], sigmaBRL=need, ratio=a["N"]/need, w_evt_L=need/a["N"],
        aux=True, note="DECISION: auxiliary ratio sample for the generator-mjj correction C; N < sigma x BR x L accepted because only the ratio C enters b and its MC-stat uncertainty is propagated as a nuisance")

# ------------------------------------------------------------------ nuisance model (counting and fit)
TH = TS["processes"]
def th(name, proxy=None):
    if name in TH: return TH[name]["total"], name
    return TH[proxy]["total"], f"{proxy} (proxy)"
THMAP = {"S_EW_ZHjj": ("S_EW_ZHjj", None, "th_sig"), "H_QCD_ZHjj": ("H_QCD_ZHjj", None, "th_qcdzh"), "H_ggZH": ("H_ggZH_py8dec", None, "th_ggzh"),
         "H_ttH": ("H_ttH", None, "th_tth"), "H_tHW": ("H_tHW", "H_ttH", "th_tth"), "H_ZH_tautau": ("H_ZH_tautau", "H_QCD_ZHjj", "th_zhtt"),
         "B_QCD_Zaajj_vbs": ("B_QCD_zaajj_vbs", "F_QCD_llajj_vbs", "th_qcdzaa"), "B_EW_Zaajj_vbs_is1": ("B_EW_zaajj_vbs_is1h", None, "th_ewzaa"),
         "B_EW_Zaajj_vbs_is2": ("B_EW_zaajj_vbs_is2", None, "th_ewzaa"), "B_EW_Zaajj_vbs_is3": ("B_EW_zaajj_vbs_is3", None, "th_ewzaa"),
         "F_QCD_Zajj": ("F_QCD_llajj_vbs", None, "th_fqcd"), "F_EW_Zajj": ("F_EW_llajj_vbs", None, "th_few"),
         "T_ttaa": ("T_ttaa", None, "th_top"), "T_tta": ("T_tta", None, "th_top"), "T_tWa": ("T_tWa", None, "th_top")}
NUIS, THSRC = {}, {}
for sid, r in REG.items():
    if r.get("missing"): continue
    nm, px, grp = THMAP[sid]; rel, src = th(nm, px); THSRC[sid] = dict(group=grp, rel=rel, source=src)
    n = {grp: rel, "lumi": LUMI_UNC}
    if sid.startswith(("B_QCD_Zaajj", "B_EW_Zaajj")): n["offshell"] = OFFSHELL_UNC
    if sid.startswith("B_EW_Zaajj"): n["int_zaa"] = INT_ZAA
    if sid == "H_ggZH": n["ggzh_norm"] = GGZH_LN
    NUIS[sid] = n
THEORY_GROUPS = lambda g: g.startswith("th_") or g in ("offshell", "int_zaa", "ggzh_norm")
SCALE = {}        # per-sample yield multipliers for robustness variations (ggZH x2 / x0.5)
EFFON = [False]   # CMS-like object-efficiency reweighting (A7)
OE = TS.get("object_eff")
CMS_EFF = {  # assumed CMS-like reco x ID x iso efficiencies (Run 2/3 performance; JINST 16 (2021) P05014, JINST 13 (2018) P06015)
 "e": dict(eta=[0, 1.5, 2.5], pt=[10, 20, 30, 50, 1e9], eff=[[0.70, 0.80, 0.88, 0.92], [0.65, 0.75, 0.83, 0.88]]),
 "m": dict(eta=[0, 1.5, 2.4], pt=[10, 20, 30, 50, 1e9], eff=[[0.93, 0.96, 0.96, 0.96], [0.93, 0.96, 0.96, 0.96]]),
 "g": dict(eta=[0, 1.4442, 2.5], pt=[20, 30, 40, 60, 1e9], eff=[[0.85, 0.88, 0.92, 0.92], [0.80, 0.83, 0.88, 0.88]])}
def _lookup(tab, k, pt, eta):
    e = np.clip(np.searchsorted(tab[k]["eta" if "eta" in tab[k] else "eta_edges"], np.abs(eta)) - 1, 0, 1)
    p = np.clip(np.searchsorted(tab[k]["pt" if "pt" in tab[k] else "pt_edges"], pt) - 1, 0, 3)
    return np.asarray(tab[k]["eff"])[e, p]
if OE:
    for sid, d in DATA.items():
        w = np.ones(len(d["mll"]))
        with np.errstate(invalid="ignore", divide="ignore"):
            for lk in ("la", "lb"):
                pt, eta = np.nan_to_num(d[lk][:, 0], nan=0.), np.nan_to_num(d[lk][:, 1], nan=0.); k = np.where(d["flav"] == 11, "e", "m")
                for t in ("e", "m"):
                    m = (k == t) & (pt > 10); de = _lookup(OE, t, pt[m], eta[m]); w[m] *= np.where(de > 0, _lookup(CMS_EFF, t, pt[m], eta[m])/np.maximum(de, 1e-9), 1.0)
            for i in range(2):
                pt, eta = np.nan_to_num(d["g"][:, i, 0], nan=0.), np.nan_to_num(d["g"][:, i, 1], nan=0.); m = pt > 20
                de = _lookup(OE, "g", pt[m], eta[m]); w[m] *= np.where(de > 0, _lookup(CMS_EFF, "g", pt[m], eta[m])/np.maximum(de, 1e-9), 1.0)
        d["w_cms"] = w
def effcorr(sid, c):
    if not EFFON[0] or "w_cms" not in DATA[sid]: return 1.0
    d = DATA[sid]; pre, lg, jb, vbs, win, wide = masks(d, c); m = pre & lg & jb
    return float(d["w_cms"][m].mean()) if m.sum() else float(d["w_cms"][pre].mean() if pre.sum() else 1.0)

# ------------------------------------------------------------------ m_gg peak from the Delphes EW signal
m = DATA["S_EW_ZHjj"]["mgg"]; m = m[np.isfinite(m) & (m > 110) & (m < 140)]
h, e = np.histogram(m, bins=60, range=(110, 140)); c = 0.5*(e[1:] + e[:-1]); cw = (c > 121) & (c < 129)
(pA, MU, SIG), cov = optimize.curve_fit(lambda x, a, mu, s: a*np.exp(-0.5*((x-mu)/s)**2), c[cw], h[cw], p0=[h.max(), 125, 2])
SIG = abs(SIG); q = np.sort(m); n = len(q); kk = int(0.683*n); wd = q[kk:] - q[:n-kk]
RES = dict(mu=float(MU), sigma_core=float(SIG), sigma_core_err=float(np.sqrt(cov[2, 2])), sigma_eff=float(wd.min()/2))
WIDE = (105., 165.)

# ------------------------------------------------------------------ selection
# reference-like baseline (arXiv:2512.07689 Sec. III; photon pT raised 20->25 GeV to stay inside the pta>25 generator
# cut of the VBS-biased fake samples): 70<mll<120, mllgg>100, mjj>700, |deta|>2.0, +-2 sigma window
BASE = dict(zwin=(70., 120.), mllgg=100., gpt=25., ratio=None, bveto=False, zep=99., mjj=700., deta=2.0, wk=2.0)
def masks(d, c):
    with np.errstate(invalid="ignore"):
        lo, hi = c["zwin"] if isinstance(c["zwin"], tuple) else (MZ - c["zwin"], MZ + c["zwin"])
        pre = np.isfinite(d["mll"]) & (d["ng"] >= 2) & (d["nj"] >= 2)
        lg = (d["mll"] > lo) & (d["mll"] < hi) & (d["mllgg"] > c["mllgg"]) & (d["g1pt"] > c["gpt"]) & (d["g2pt"] > c["gpt"])
        if c["ratio"]: lg &= (d["g1pt"]/d["mgg"] > c["ratio"][0]) & (d["g2pt"]/d["mgg"] > c["ratio"][1])
        jb = (d["nb"] == 0) if c["bveto"] else np.ones(len(pre), bool)
        vbs = (d["mjj"] > c["mjj"]) & (d["detajj"] > c["deta"]) & (d["zep_gg"] < c["zep"])
        wlo, whi = MU - c["wk"]*SIG, MU + c["wk"]*SIG
        win = (d["mgg"] > wlo) & (d["mgg"] < whi); wide = (d["mgg"] > WIDE[0]) & (d["mgg"] < WIDE[1])
    return pre, lg, jb, vbs, win, wide

def raw(d, m): return len(np.unique(d["evt"][m]))
def fwin(mgg, c):
    """fraction of an exponential (unbinned MLE) m_gg spectrum inside the window, relative to WIDE"""
    x = mgg - WIDE[0]; L = WIDE[1] - WIDE[0]; lo, hi = MU - c["wk"]*SIG - WIDE[0], MU + c["wk"]*SIG - WIDE[0]
    if len(x) < 5: return (hi - lo)/L, 0.0
    nll = lambda lam: (len(x)*np.log(L)) if abs(lam) < 1e-6 else -(np.log(abs(lam)) - lam*x).sum() + len(x)*np.log(abs(1 - np.exp(-lam*L)))
    lam = optimize.minimize_scalar(nll, bounds=(-0.2, 0.2), method="bounded").x
    if abs(lam) < 1e-6: return (hi - lo)/L, 0.0
    return (np.exp(-lam*lo) - np.exp(-lam*hi))/(1 - np.exp(-lam*L)), float(lam)

TFCACHE = {}
def transfer_factor(c):
    """P(event passes the 2-photon cuts + window | 1-photon level) in direct Delphes F_QCD_Zajj (VBS cuts removed for stats)"""
    key = json.dumps(c, sort_keys=True)
    if key in TFCACHE: return TFCACHE[key]
    d = DATA["F_QCD_Zajj"]; c2 = dict(c, mjj=0., deta=0., zep=99.)
    pre, lg, jb, vbs, win, wide = masks(d, c2)
    with np.errstate(invalid="ignore"):
        lo, hi = c["zwin"] if isinstance(c["zwin"], tuple) else (MZ - c["zwin"], MZ + c["zwin"])
        one = np.isfinite(d["mll"]) & (d["ng"] >= 1) & (d["nj"] >= 2) & (d["mll"] > lo) & (d["mll"] < hi) & jb & (d["g1pt"] > c["gpt"])
    nfull = raw(d, pre & lg & jb & wide); f, _ = fwin(d["mgg"][pre & lg & jb & wide], c)
    tf = (nfull*f/raw(d, one)) if raw(d, one) else 0.0
    TFCACHE[key] = (tf, nfull, raw(d, one)); return TFCACHE[key]

def estimate(sid, c):
    """expected yield per fb^-1, MC-stat (per fb^-1), raw in window, raw in wide, method, extra"""
    r = REG[sid]; d = DATA[sid]; we = r["w_evt_fb"]
    pre, lg, jb, vbs, win, wide = masks(d, c)
    full = pre & lg & jb & vbs
    nwin, nwide = raw(d, full & win), raw(d, full & wide)
    if r["kind"] == "tf":
        with np.errstate(invalid="ignore"):
            lo, hi = c["zwin"] if isinstance(c["zwin"], tuple) else (MZ - c["zwin"], MZ + c["zwin"])
            one = np.isfinite(d["mll"]) & (d["ng"] >= 1) & (d["nj"] >= 2) & (d["mll"] > lo) & (d["mll"] < hi) & jb & vbs & (d["g1pt"] > c["gpt"])
        n1 = raw(d, one); tf, ntf, nden = transfer_factor(c)
        if n1 == 0:   # VBS-factorise the 1-photon level
            with np.errstate(invalid="ignore"):
                one0 = np.isfinite(d["mll"]) & (d["ng"] >= 1) & (d["nj"] >= 2) & (d["mll"] > lo) & (d["mll"] < hi) & jb & (d["g1pt"] > c["gpt"])
            pv = np.isfinite(d["mll"]) & (d["ng"] >= 1) & (d["nj"] >= 2)
            ev = raw(d, pv & vbs)/max(raw(d, pv), 1); y1 = raw(d, one0)*we*(ev if ev > 0 else 0.5/(raw(d, pv) + 1)); n1 = raw(d, one0)
        else: y1 = n1*we
        y = y1*tf
        if y <= 0: y = 1.14*we*max(tf, 0); return y, y, nwin, nwide, "UL (1-photon level x TF)", dict(n_1photon=n1, TF=tf)
        return y, y, nwin, nwide, "L3 transfer (Delphes TF, 100% unc.)", dict(n_1photon=n1, TF=tf, TF_num=ntf, TF_den=nden)
    if nwin >= 10:
        return nwin*we, np.sqrt(nwin)*we, nwin, nwide, "L0 direct", {}
    if r["kind"] == "cont" and nwide >= 10:
        f, lam = fwin(d["mgg"][full & wide], c); y = nwide*we*f
        return y, np.sqrt(nwide)*we*f, nwin, nwide, "L1 m_gg-shape (exp. fit, Delphes)", dict(f_win=f, lam=lam)
    # L2: VBS-factorised
    nL = raw(d, pre & lg & jb & (wide if r["kind"] == "cont" else win))
    nP = raw(d, pre); nPV = raw(d, pre & vbs)
    if nL > 0 and nP > 0:
        ev = nPV/nP if nPV > 0 else 0.5/(nP + 1)
        if r["kind"] == "cont": f, _ = fwin(d["mgg"][pre & lg & jb & wide], c)
        else: f = 1.0
        y = nL*we*f*ev
        return y, y, nwin, nwide, "L2 VBS-factorised (100% unc.)", dict(n_noVBS=nL, eps_vbs=ev, n_presel=nP, n_presel_vbs=nPV)
    # L2b (2026-11-03): direct sample, VBS AND window factorised: N(pre & lepton/photon cuts) x eps(VBS | pre) x f(window | pre)
    nLb = raw(d, pre & lg & jb)
    if nLb > 0 and nP > 0 and r["kind"] == "cont":
        ev = nPV/nP if nPV > 0 else 0.5/(nP + 1)
        pw = raw(d, pre & wide)/nP; fw, _ = fwin(d["mgg"][pre & wide], c); fw *= pw
        y = nLb*we*ev*fw
        return y, y, nwin, nwide, "L2b VBS+window-factorised, direct sample (100% unc.)", dict(n_lep_pho=nLb, eps_vbs=ev, f_win=fw, n_presel=nP, UL95_direct=3.0*we)
    return 1.14*we, 1.14*we, nwin, nwide, "UL (zero support): 1.14 w_evt", dict(UL95=3.0*we)

SYST = {"fake": 0.50, "other": 0.10}
def totals(c, L, sigdef="a", fake_syst=0.5, details=False, theory=True):
    """s, b, MC stat, sigma_b (per-process normalisation (+) MC stat (+) correlated groups: theory per group, off-shell,
    Zgg interference, ggZH x2, luminosity; groups summed linearly over processes, then in quadrature) and sigma_s"""
    s = b = vs = vb = var_proc = 0.0; comp = {}; Gb = {}; Gs = {}
    for sid, r in REG.items():
        if r.get("missing") or r["role"] == "excl": continue
        y, e, nw, nwd, meth, det = estimate(sid, c); gc = genmjj_corr(sid, c); f = SCALE.get(sid, 1.0)*effcorr(sid, c)*gc[0]; y, e = y*L*f, e*L*f
        if details: comp[sid] = dict(y=y, mcstat=e, raw_win=nw, raw_wide=nwd, method=meth, w_evt=r["w_evt_fb"]*L, **{k: float(v) for k, v in det.items()})
        sig = r["role"] == "sig" or (sigdef == "b" and r["role"] == "qcdzh")
        G = Gs if sig else Gb
        for g, rel in list(NUIS[sid].items()) + ([(f"genmjj_{sid}", gc[1])] if sid in AUX else []):
            if theory or not THEORY_GROUPS(g): G[g] = G.get(g, 0.0) + rel*y
        if details and sid in AUX: comp[sid].update(genmjj_C=float(gc[0]), genmjj_rel=float(gc[1]), genmjj_raw_twin=gc[2], genmjj_raw_vbs=gc[3])
        if sig: s += y; vs += e**2; continue
        b += y; vb += e**2
        rs = fake_syst if r["syst"] == "fake" else SYST["other"]
        var_proc += (rs*y)**2
    sb = np.sqrt(var_proc + vb + sum(v**2 for v in Gb.values())); ss = np.sqrt(vs + sum(v**2 for v in Gs.values()))
    return dict(s=s, b=b, s_mc=np.sqrt(vs), b_mc=np.sqrt(vb), sigma_b=sb, sigma_s=ss, comp=comp,
                groups_b={k: float(v) for k, v in Gb.items()}, groups_s={k: float(v) for k, v in Gs.items()})

def zeq1(s, b): return np.sqrt(2*((s + b)*np.log(1 + s/b) - s)) if b > 0 and s > 0 else 0.0
def zeq1_err(s, b, ds, db):
    h1, h2 = max(1e-6, 1e-3*s), max(1e-6, 1e-3*b)
    gs = (zeq1(s + h1, b) - zeq1(s - h1, b))/(2*h1); gb = (zeq1(s, b + h2) - zeq1(s, max(b - h2, 1e-9)))/(2*h2)
    return np.hypot(gs*ds, gb*db)
def z_syst(s, b, sb):
    if sb <= 0: return zeq1(s, b)
    t1 = (s + b)*np.log((s + b)*(b + sb**2)/(b**2 + (s + b)*sb**2)); t2 = b**2/sb**2*np.log(1 + sb**2*s/(b*(b + sb**2)))
    return float(np.sqrt(max(2*(t1 - t2), 0)))
def cls_limit(s, b, sb, alpha=0.05, ss=0.0):
    """median expected 95% CL CLs upper limit on mu: exact Poisson counting; b and s marginalised over log-normals
    (relative widths sb/b and ss/s, independent)"""
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

# ------------------------------------------------------------------ optimisation on expected quantities (500 fb^-1, def. a)
LOPT = 500.0
def fom(c):
    T = totals(c, LOPT); return z_syst(T["s"], T["b"], T["sigma_b"]), T["s"], T["b"]
GRID = dict(wk=[1.5, 2.0], ratio=[(1/3, 1/4), (0.35, 0.25), (0.4, 0.3)], zwin=[(70., 120.), 25., 20., 15., 10.],
            zep=[99., 1.5, 1.0, 0.7], mllgg=[100., 150., 200., 250., 300.], bveto=[False, True])
MJJ = [500., 600., 700., 800., 900., 1000., 1200.]; DETA = [2.0, 2.5, 3.0, 3.5, 4.0, 4.5]
def pick(cands):
    zs = [fom(x) for x in cands]; zmax = max(z[0] for z in zs)
    ok = [i for i, z in enumerate(zs) if z[0] >= 0.97*zmax]; i = max(ok, key=lambda i: zs[i][1]); return cands[i], zs[i]
OPT = dict(BASE, ratio=(1/3, 1/4), gpt=25.); HIST = []
for it in range(3):
    old = json.dumps(OPT, sort_keys=True)
    for k, vals in GRID.items():
        OPT, z = pick([dict(OPT, **{k: v}) for v in vals]); HIST.append((it, k, str(OPT[k]), z[0]))
    OPT, z = pick([dict(OPT, mjj=a, deta=b2) for a in MJJ for b2 in DETA]); HIST.append((it, "mjj,deta", f"{OPT['mjj']},{OPT['deta']}", z[0]))
    if json.dumps(OPT, sort_keys=True) == old: break
SCAN = {}
for L in (500., 3000.):
    for a in MJJ:
        for b2 in DETA:
            T = totals(dict(OPT, mjj=a, deta=b2), L); SCAN[f"{int(L)}|{a:.0f},{b2:.1f}"] = dict(Z=zeq1(T["s"], T["b"]), Zsyst=z_syst(T["s"], T["b"], T["sigma_b"]), s=T["s"], b=T["b"])

# ------------------------------------------------------------------ results
def results(c, tag):
    out = {}
    for L in (500., 1000., 3000.):
        for sd in ("a", "b"):
            T = totals(c, L, sd, details=(L == 500. or L == 3000.)); T0 = totals(c, L, sd, theory=False)
            mu, nmed = cls_limit(T["s"], T["b"], T["sigma_b"], ss=T["sigma_s"]); mu0, _ = cls_limit(T["s"], T["b"], 0.0)
            mu_nth, _ = cls_limit(T0["s"], T0["b"], T0["sigma_b"], ss=T0["sigma_s"])
            out[f"{int(L)}_{sd}"] = dict(L=L, sigdef=sd, s=T["s"], b=T["b"], s_mc=T["s_mc"], b_mc=T["b_mc"], sigma_b=T["sigma_b"], sigma_s=T["sigma_s"],
                sigma_b_notheory=T0["sigma_b"], Z_eq1=zeq1(T["s"], T["b"]), Z_eq1_mcerr=zeq1_err(T["s"], T["b"], T["s_mc"], T["b_mc"]),
                Z_syst_counting=z_syst(T["s"], T["b"], T["sigma_b"]), Z_syst_counting_notheory=z_syst(T0["s"], T0["b"], T0["sigma_b"]),
                mu95_cls=mu, mu95_cls_stat=mu0, mu95_cls_notheory=mu_nth, n_median=nmed, groups_b=T["groups_b"], groups_s=T["groups_s"],
                comp=T["comp"])
    return out
RESULTS = results(OPT, "opt"); RES_BASE = results(BASE, "base")

# ------------------------------------------------------------------ cutflow (Table III-like), 500 fb^-1
def cutflow(c, L=500.0):
    steps = [("N generated x sigma x BR", None), ("OSSF + >=2 photons + >=2 jets", "pre"), ("+ Z window & m_llgg", "z"),
             ("+ photon pT, pT/m_gg", "g"), ("+ b-veto", "bv"), ("+ mjj, deta_jj", "vbs"), ("+ Zeppenfeld", "zep"),
             (f"+ m_gg window ({MU - c['wk']*SIG:.1f}-{MU + c['wk']*SIG:.1f})", "win")]
    rows = []
    for name, key in steps:
        row = dict(step=name)
        for sid, r in REG.items():
            if r.get("missing") or r["role"] == "excl": continue
            d = DATA[sid]; we = r["w_evt_fb"]*L
            if key is None: row[sid] = dict(y=r["sig"]*r["k"]*L, raw=r["N"]); continue
            pre, lg, jb, vbs, win, wide = masks(d, c)
            with np.errstate(invalid="ignore"):
                lo, hi = c["zwin"] if isinstance(c["zwin"], tuple) else (MZ - c["zwin"], MZ + c["zwin"])
                mz = (d["mll"] > lo) & (d["mll"] < hi) & (d["mllgg"] > c["mllgg"])
                mg = (d["g1pt"] > c["gpt"]) & (d["g2pt"] > c["gpt"])
                if c["ratio"]: mg &= (d["g1pt"]/d["mgg"] > c["ratio"][0]) & (d["g2pt"]/d["mgg"] > c["ratio"][1])
                mv = (d["mjj"] > c["mjj"]) & (d["detajj"] > c["deta"]); mzp = d["zep_gg"] < c["zep"]
            seq = {"pre": pre}; seq["z"] = seq["pre"] & mz; seq["g"] = seq["z"] & mg; seq["bv"] = seq["g"] & jb
            seq["vbs"] = seq["bv"] & mv; seq["zep"] = seq["vbs"] & mzp; seq["win"] = seq["zep"] & win
            n = raw(d, seq[key]); row[sid] = dict(y=n*we, raw=n)
        rows.append(row)
    return rows
CUTFLOW = cutflow(OPT); CUTFLOW_BASE = cutflow(BASE)

# ------------------------------------------------------------------ SUPPLEMENTARY: binned profile-likelihood fit in m_gg
EDGES = np.array([105., 110., 115., 120.] + [MU - 2*SIG, MU - SIG, MU, MU + SIG, MU + 2*SIG] + [130., 135., 140., 145., 150., 155., 160., 165.])
EDGES = np.unique(np.sort(EDGES[(EDGES >= 105.) & (EDGES <= 165.)]))
def templates(c, L, sigdef):
    """per process: expected counts per m_gg bin (resonant: EW-signal Delphes shape; continuum: exponential fit),
    total normalised to the hierarchy estimate over WIDE (window estimate / f_win)"""
    cw = dict(c, wk=99.)   # all cuts except the window
    ds = DATA["S_EW_ZHjj"]; pre, lg, jb, vbs, win, wide = masks(ds, c)
    hs, _ = np.histogram(ds["mgg"][pre & lg & jb & vbs], bins=EDGES); res_shape = hs/hs.sum()
    T = []
    for sid, r in REG.items():
        if r.get("missing") or r["role"] == "excl": continue
        y, e, nw, nwd, meth, det = estimate(sid, c)
        role = "sig" if (r["role"] == "sig" or (sigdef == "b" and r["role"] == "qcdzh")) else "bkg"
        if r["kind"] == "res":
            # window yield -> full-range normalisation with the resonant shape
            wmask = (0.5*(EDGES[1:] + EDGES[:-1]) > MU - c["wk"]*SIG) & (0.5*(EDGES[1:] + EDGES[:-1]) < MU + c["wk"]*SIG)
            nu = y*L*res_shape/res_shape[wmask].sum()
        else:
            d = DATA[sid] if r["kind"] != "tf" else DATA["F_QCD_Zajj"]
            p, l, j, v, _, wd = masks(d, dict(c, mjj=0., deta=0., zep=99.) if r["kind"] == "tf" else c)
            mg = d["mgg"][p & l & j & (v if r["kind"] != "tf" else True) & wd]
            if len(mg) < 5: mg = d["mgg"][p & wd]
            fw, lam = fwin(mg, c); x0 = EDGES - WIDE[0]; Lw = WIDE[1] - WIDE[0]
            cdf = (x0/Lw) if abs(lam) < 1e-6 else (1 - np.exp(-lam*x0))/(1 - np.exp(-lam*Lw))
            nu = (y*L/max(fw, 1e-12))*np.diff(cdf)
        rel_mc = (e/y) if y > 0 else 1.0
        gc = genmjj_corr(sid, c); f = SCALE.get(sid, 1.0)*effcorr(sid, c)*gc[0]
        gr = {g: v for g, v in NUIS[sid].items() if THEORY_ON[0] or not THEORY_GROUPS(g)}
        if sid in AUX: gr[f"genmjj_{sid}"] = gc[1]
        T.append(dict(id=sid, role=role, nu=nu*f, syst=(0.5 if r["syst"] == "fake" else 0.10), mc=min(rel_mc, 1.0), groups=gr))
    return T
THEORY_ON = [True]
def fit_groups(T): return sorted({g for t in T for g in t["groups"]})
def nll_fit(T, data, mu, theta):
    """theta = [one log-normal per background process (normalisation (+) MC stat)] + [one per correlated group: theory
    groups, off-shell, Zgg interference, ggZH x2 (log-normal ln 2), luminosity], shared by signal and backgrounds"""
    GL = fit_groups(T); nbk = sum(1 for t in T if t["role"] != "sig"); th = dict(zip(GL, theta[nbk:]))
    lam = np.zeros(len(EDGES) - 1); k = 0; pen = 0.5*np.sum(np.asarray(theta)**2)
    for t in T:
        mod = np.exp(sum(np.log(1 + v)*th[g] if g != "ggzh_norm" else v*th[g] for g, v in t["groups"].items()))
        if t["role"] == "sig": lam += mu*mod*t["nu"]
        else:
            sg = np.sqrt(np.log(1 + t["syst"]**2 + t["mc"]**2)); lam += mod*t["nu"]*np.exp(sg*theta[k]); k += 1
    lam = np.maximum(lam, 1e-12)
    return (lam - data*np.log(lam)).sum() + pen
def profile(T, data, mu, fixed_theta=False):
    nb = sum(1 for t in T if t["role"] != "sig") + len(fit_groups(T))
    if fixed_theta: return nll_fit(T, data, mu, np.zeros(nb))
    return optimize.minimize(lambda th: nll_fit(T, data, mu, th), np.zeros(nb), method="L-BFGS-B").fun
def fit_results(c):
    out = {}
    for L in (500., 1000., 3000.):
        for sd in ("a", "b"):
            T = templates(c, L, sd)
            asimov = lambda mu: sum((mu if t["role"] == "sig" else 1.0)*t["nu"] for t in T)
            r = {}
            for lab, fx in (("syst", False), ("stat", True)):
                d1 = asimov(1.0)
                best = optimize.minimize_scalar(lambda m: profile(T, d1, m, fx), bounds=(-5, 20), method="bounded")
                q0 = 2*(profile(T, d1, 0.0, fx) - best.fun); r[f"Z_{lab}"] = float(np.sqrt(max(q0, 0)))
                d0 = asimov(0.0); n0 = profile(T, d0, 0.0, fx)
                qmu = lambda m: 2*(profile(T, d0, m, fx) - n0) - stats.norm.ppf(0.975)**2   # median expected CLs (asymptotic)
                hi = 1.0
                while qmu(hi) < 0 and hi < 1e5: hi *= 2
                r[f"mu95_{lab}"] = float(optimize.brentq(qmu, 1e-6, hi))
            r["s_tot"] = float(sum(t["nu"].sum() for t in T if t["role"] == "sig")); r["b_tot_wide"] = float(sum(t["nu"].sum() for t in T if t["role"] != "sig"))
            out[f"{int(L)}_{sd}"] = r
    return out
FIT = fit_results(OPT)

# ------------------------------------------------------------------ robustness / checks (500 fb^-1, def. a; each row with mu95)
ROB = {}
def rob(name, c, **kw):
    T = totals(c, 500., **kw); mu, _ = cls_limit(T["s"], T["b"], T["sigma_b"], ss=T["sigma_s"])
    ROB[name] = dict(s=T["s"], b=T["b"], Z_eq1=zeq1(T["s"], T["b"]), Z_syst=z_syst(T["s"], T["b"], T["sigma_b"]), mu95=mu)
for name, c in [("optimum", OPT), ("window +-1.5 sigma", dict(OPT, wk=1.5)), ("reference-like baseline (photon pT > 25 GeV, not 20)", BASE),
                ("b-veto toggled", dict(OPT, bveto=not OPT["bveto"])), ("Zeppenfeld z* < 1.0" if OPT["zep"] > 50 else "no Zeppenfeld", dict(OPT, zep=1.0 if OPT["zep"] > 50 else 99.)),
                ("mjj > 700, |deta| > 3.0", dict(OPT, mjj=700., deta=3.0))]:
    rob(name, c)
for fs in (0.25, 1.0): rob(f"fake syst {int(fs*100)}%", OPT, fake_syst=fs)
for sc in (0.75, 1.25): rob(f"window x{sc} (resolution proxy)", dict(OPT, wk=OPT["wk"]*sc))
rob("theory / off-shell / interference nuisances removed", OPT, theory=False)
for fct in (2.0, 0.5):
    SCALE["H_ggZH"] = fct; rob(f"ggZH normalisation x{fct:g}", OPT); SCALE.clear()
_c = OFFSHELL
for sid in REG:
    if sid.startswith(("B_QCD_Zaajj", "B_EW_Zaajj")) and sid in DATA: SCALE[sid] = 1.0/_c
rob("no off-shell/FSR correction of Zgg (x1/1.128)", OPT); SCALE.clear()
for sid in ("T_tta", "T_tWa"):
    if sid in DATA:
        y = estimate(sid, OPT)[0]; SCALE[sid] = (3.0*REG[sid]["w_evt_fb"])/y if y > 0 else 1.0
rob("ttgamma, tWgamma at their direct zero-count 95% UL (3 w_evt each)", OPT); SCALE.clear()
EFFON[0] = True; rob("CMS-like e/mu/gamma efficiencies (A7 reweighting)", OPT)
T3 = {}
for L in (500., 3000.):
    for sd in ("a", "b"):
        T = totals(OPT, L, sd); mu, _ = cls_limit(T["s"], T["b"], T["sigma_b"], ss=T["sigma_s"])
        T3[f"{int(L)}_{sd}"] = dict(s=T["s"], b=T["b"], Z_eq1=zeq1(T["s"], T["b"]), Z_syst=z_syst(T["s"], T["b"], T["sigma_b"]), mu95=mu)
EFFON[0] = False
EFF_SUMMARY = dict(results=T3, cms_eff=CMS_EFF, delphes_eff=OE, mean_w_signal=float(DATA["S_EW_ZHjj"]["w_cms"][masks(DATA["S_EW_ZHjj"], OPT)[0]].mean()) if OE else None)

# ------------------------------------------------------------------ A1: 1D significance curves vs the mjj and |deta_jj| thresholds
MJJ1 = [400., 450., 500., 550., 600., 700., 800., 900., 1000., 1200.]; DETA1 = [2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
SCAN1D = {}
for L in (500., 3000.):
    for var, vals in (("mjj", MJJ1), ("deta", DETA1)):
        for v in vals:
            T = totals(dict(OPT, **{var: v}), L)
            SCAN1D[f"{int(L)}|{var}|{v:g}"] = dict(Z=zeq1(T["s"], T["b"]), Zsyst=z_syst(T["s"], T["b"], T["sigma_b"]), s=T["s"], b=T["b"],
                                                   gen_cut_region=bool(var == "mjj" and v < 500.))

# ------------------------------------------------------------------ A9: ttgamma at the reference-like baseline before any m_gg window (vs reference 0.15 +- 0.10 / 500 fb^-1)
TTA_XCHECK = {}
for sid in ("T_tta", "T_tWa"):
    if sid not in DATA: continue
    d = DATA[sid]; pre, lg, jb, vbs, win, wide = masks(d, BASE); m = pre & lg & jb & vbs; n = raw(d, m)
    TTA_XCHECK[sid] = dict(raw=n, y500=n*REG[sid]["w_evt_fb"]*500, y500_ul95=3.0*REG[sid]["w_evt_fb"]*500 if n == 0 else None,
                           raw_presel=raw(d, pre), raw_lg=raw(d, pre & lg))
TTA_XCHECK["reference"] = dict(T_tta=[0.15, 0.10], T_tWa=[0.00, 0.00], note="arXiv:2512.07689 Table IV (full reference cut flow, no m_gg window, photon pT > 20 GeV)")
# transfer-factor cross-check (the old L3 method) for the direct ttgamma result
TF_XCHECK = {}
if "F_QCD_Zajj" in DATA:
    tf, ntf, nden = transfer_factor(OPT)
    for sid in ("T_tta", "T_tWa"):
        if sid not in DATA: continue
        d = DATA[sid]; we = REG[sid]["w_evt_fb"]
        with np.errstate(invalid="ignore"):
            lo, hi = OPT["zwin"] if isinstance(OPT["zwin"], tuple) else (MZ - OPT["zwin"], MZ + OPT["zwin"])
            one = np.isfinite(d["mll"]) & (d["ng"] >= 1) & (d["nj"] >= 2) & (d["mll"] > lo) & (d["mll"] < hi) & (d["g1pt"] > OPT["gpt"]) & (d["mjj"] > OPT["mjj"]) & (d["detajj"] > OPT["deta"])
        TF_XCHECK[sid] = dict(n_1photon=raw(d, one), TF=tf, y500_tf=raw(d, one)*we*tf*500, y500_direct=RESULTS["500_a"]["comp"][sid]["y"])

# fake-factor cross-check on Delphes jets (F_QCD_Zajj ff1 rows): f = 5e-4, 1e-3, 2e-3 and pT-dependent
FF = {}
ffc = sorted(glob.glob(f"{NT}/F_QCD_llajj_vbs__c[0-9][0-9][0-9]_ff1.npz"))
if ffc and "F_QCD_Zajj" in DATA:
    d = load(ffc); r = REG["F_QCD_Zajj"]; we = r["sig"]*r["k"]/d["N"]
    pre, lg, jb, vbs, win, wide = masks(d, dict(OPT, mjj=0., deta=0., zep=99.)); m0 = pre & lg & jb & win
    pre, lg, jb, vbs, win, wide = masks(d, OPT); m1 = pre & lg & jb & vbs & win
    for f in (5e-4, 1e-3, 2e-3):
        FF[f"f={f:g}"] = dict(final=float((d["wf_flat"][m1]*f/1e-3).sum()*we*500), noVBS=float((d["wf_flat"][m0]*f/1e-3).sum()*we*500))
    FF["pT-dependent"] = dict(final=float(d["wf_pt"][m1].sum()*we*500), noVBS=float(d["wf_pt"][m0].sum()*we*500))
    dd = DATA["F_QCD_Zajj"]; pre, lg, jb, vbs, win, wide = masks(dd, dict(OPT, mjj=0., deta=0., zep=99.))
    FF["direct Delphes"] = dict(final=RESULTS["500_a"]["comp"]["F_QCD_Zajj"]["y"], noVBS=float(raw(dd, pre & lg & jb & win)*r["w_evt_fb"]*500),
                                raw_noVBS=raw(dd, pre & lg & jb & win))

# ------------------------------------------------------------------ E: coupling interpretation (same framework, exec'd in this namespace)
exec(compile(open(f"{P}/scripts/analysis/coupling_section.py").read(), f"{P}/scripts/analysis/coupling_section.py", "exec"))

json.dump(dict(registry={k: {kk: vv for kk, vv in v.items() if kk != "chunks"} | dict(chunks=[os.path.basename(x) for x in v["chunks"]]) for k, v in REG.items()},
               missing=MISSING, resolution=RES, base=BASE, optimum=OPT, opt_history=HIST, results=RESULTS, results_baseline=RES_BASE,
               cutflow=CUTFLOW, cutflow_baseline=CUTFLOW_BASE, scan=SCAN, fit=FIT, fit_edges=EDGES.tolist(), robustness=ROB, ff_xcheck=FF,
               lumi_unc=LUMI_UNC, syst=SYST, br=dict(BGG=BGG, ZF=ZF, BR_ZLL=BR_ZLL), br_table=BRTAB, nmc_check=NCHECK, nmc_L=NMC_L,
               nuisances=NUIS, theory_sources=THSRC, theory_summary={k: v for k, v in TS.items() if k not in ("object_eff",)},
               offshell=dict(factor=OFFSHELL, rel_unc=OFFSHELL_UNC), int_zaa=INT_ZAA, cms_eff=EFF_SUMMARY, scan1d=SCAN1D,
               tta_xcheck=TTA_XCHECK, tf_xcheck=TF_XCHECK, coupling=CPL,
               genmjj={sid: dict(twin=a["twin"], N=a["N"], sigma_fb=a["sig"], C_opt=genmjj_corr(sid, OPT)[0], rel_opt=genmjj_corr(sid, OPT)[1],
                                 raw_twin=genmjj_corr(sid, OPT)[2], raw_vbs=genmjj_corr(sid, OPT)[3]) for sid, a in AUX.items()}),
          open(OUT, "w"), indent=1, default=lambda o: o.tolist() if isinstance(o, np.ndarray) else (float(o) if isinstance(o, np.floating) else str(o)))
print("optimum:", OPT); print("missing:", MISSING)
for k, v in RESULTS.items():
    print(f"{k}: s={v['s']:.4f}+-{v['s_mc']:.4f} b={v['b']:.4f}+-{v['b_mc']:.4f} Zeq1={v['Z_eq1']:.3f}+-{v['Z_eq1_mcerr']:.3f} "
          f"Zsyst(cnt)={v['Z_syst_counting']:.3f} mu95={v['mu95_cls']:.2f} | fit Z_syst={FIT[k]['Z_syst']:.3f} mu95_fit={FIT[k]['mu95_syst']:.2f}")

# ------------------------------------------------------------------ figures (PDF + PNG) -> <out dir>/../../figures
if "--plots" in sys.argv:
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    FIG = sys.argv[sys.argv.index("--plots") + 1]; os.makedirs(FIG, exist_ok=True)
    plt.rcParams.update({"font.size": 11, "axes.spines.top": False, "axes.spines.right": False, "axes.edgecolor": "#555",
                         "axes.labelcolor": "#222", "xtick.color": "#444", "ytick.color": "#444", "legend.frameon": False})
    GROUPS = ["Zg + fake g (QCD+EW)", "Zgg (QCD+EW)", "QCD ZHjj", "other H->gg", "top (ttgg, ttg, tWg)"]
    COL = dict(zip(GROUPS, ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]))  # fixed categorical order (dataviz palette)
    LPL = 3000.0
    PS = dict(OPT, mjj=0., deta=0., zep=99., wk=99.)      # plotting selection: all non-VBS cuts of the optimum, no window
    def sel(d, c, drop=None):
        pre, lg, jb, vbs, win, wide = masks(d, c); return pre & lg & jb
    VARS = [("mgg", r"$m_{\gamma\gamma}$ [GeV]", np.linspace(105, 165, 31), "m_gg", PS),
            ("mll", r"$m_{\ell\ell}$ [GeV]", np.linspace(60, 120, 31), "m_ll", dict(PS, zwin=(50., 200.))),
            ("mjj", r"$m_{jj}$ [GeV]", np.linspace(0, 2500, 26), "m_jj", PS),
            ("detajj", r"$|\Delta\eta_{jj}|$", np.linspace(0, 8, 33), "deta_jj", PS),
            ("g1pt", r"leading photon $p_T$ [GeV]", np.linspace(25, 225, 26), "photon1_pt", PS),
            ("g2pt", r"subleading photon $p_T$ [GeV]", np.linspace(25, 125, 26), "photon2_pt", PS),
            ("zep_gg", r"Zeppenfeld $z^*_{\gamma\gamma}$", np.linspace(0, 3, 31), "zeppenfeld", PS)]
    for var, lab, bins, fname, c in VARS:
        fig, ax = plt.subplots(figsize=(6.4, 4.6)); bottom = np.zeros(len(bins) - 1)
        for g in GROUPS:
            hh = np.zeros(len(bins) - 1)
            for sid, r in REG.items():
                if r.get("missing") or r["grp"] != g or r["role"] == "excl" or r["kind"] == "tf": continue
                if sid in AUX:   # QCD-type samples: plot the unbiased no-mjj-cut twin (the VBS-biased sample has a cliff at mjj = 400 GeV)
                    d = AUX[sid]["d"]; wv = np.full(len(d["mll"]), AUX[sid]["w"]*REG[sid]["corr"])
                else: d = DATA[sid]; wv = d["w"]
                m = sel(d, c) & (np.isfinite(d["mgg"]) if var != "mgg" else (d["mgg"] > 0))
                hh += np.histogram(d[var][m], bins=bins, weights=wv[m]*LPL)[0]
            if hh.sum() > 0:
                ax.bar(bins[:-1], hh, width=np.diff(bins), bottom=bottom, align="edge", color=COL[g], edgecolor="white", linewidth=0.6, label=g)
                bottom += hh
        d = DATA["S_EW_ZHjj"]; m = sel(d, c)
        hs = np.histogram(d[var][m], bins=bins, weights=d["w"][m]*LPL)[0]
        ax.step(bins, np.r_[hs, hs[-1]], where="post", color="#111", lw=2, label="EW ZHjj signal")
        ax.set_yscale("log"); top = max(bottom.max(), hs.max()); ax.set_ylim(max(1e-5, 1e-4*top), top*30)
        ax.set_xlabel(lab); ax.set_ylabel(f"events / bin ({LPL:.0f} fb$^{{-1}}$, 13.6 TeV)")
        if var == "mgg": [ax.axvline(x, color="#777", ls="--", lw=1) for x in (MU - OPT["wk"]*SIG, MU + OPT["wk"]*SIG)]
        ax.set_title("Delphes CMS; all optimum cuts except VBS-jet cuts and m$_{\\gamma\\gamma}$ window", fontsize=9, color="#444")
        ax.legend(fontsize=8, ncol=2, loc="upper right"); fig.tight_layout()
        for ext in ("pdf", "png"): fig.savefig(f"{FIG}/{fname}.{ext}", dpi=150)
        plt.close(fig)
    for L in (500, 3000):
        Z = np.array([[SCAN[f"{L}|{a:.0f},{b2:.1f}"]["Z"] for b2 in DETA] for a in MJJ])
        fig, ax = plt.subplots(figsize=(6.6, 5)); im = ax.imshow(Z, origin="lower", cmap="Blues", aspect="auto")
        for i in range(len(MJJ)):
            for j in range(len(DETA)):
                ax.text(j, i, f"{Z[i, j]:.2f}", ha="center", va="center", fontsize=8, color="white" if Z[i, j] > Z.min() + 0.6*(Z.max() - Z.min()) else "#222")
        ax.set_xticks(range(len(DETA)), [f">{x:.1f}" for x in DETA]); ax.set_yticks(range(len(MJJ)), [f">{x:.0f}" for x in MJJ])
        ax.set_xlabel(r"$|\Delta\eta_{jj}|$ cut"); ax.set_ylabel(r"$m_{jj}$ cut [GeV]")
        ax.set_title(f"Eq. 1 significance (def. a), {L} fb$^{{-1}}$; other cuts at optimum", fontsize=10)
        fig.colorbar(im, ax=ax, label="Z (Eq. 1, stat. only)"); fig.tight_layout()
        for ext in ("pdf", "png"): fig.savefig(f"{FIG}/scan_mjj_deta_{L}.{ext}", dpi=150)
        plt.close(fig)
    # A1: Z vs the mjj and |deta_jj| lower cuts (other cuts at the optimum)
    MR = TS.get("mjj_resolution") or {}
    for var, vals, xl, fname in (("mjj", MJJ1, r"$m_{jj}$ lower cut [GeV]", "z_vs_mjj"), ("deta", DETA1, r"$|\Delta\eta_{jj}|$ lower cut", "z_vs_deta")):
        fig, ax = plt.subplots(figsize=(6.4, 4.4))
        for L, col in ((500, "#2a78d6"), (3000, "#eb6834")):
            z = [SCAN1D[f"{L}|{var}|{v:g}"]["Z"] for v in vals]; zs = [SCAN1D[f"{L}|{var}|{v:g}"]["Zsyst"] for v in vals]
            ax.plot(vals, z, "-o", color=col, lw=2, ms=5, label=f"Z Eq. 1, {L} fb$^{{-1}}$"); ax.plot(vals, zs, "--", color=col, lw=1.5, label=f"Z with $\\sigma_b$, {L} fb$^{{-1}}$")
        if var == "mjj":
            ax.axvspan(min(vals) - 25, 500, color="#999", alpha=0.18, lw=0)
            ax.text(405, ax.get_ylim()[1]*0.93, "affected by generator\nmjj > 400 GeV cut", fontsize=8, color="#444", va="top")
            r = MR.get("ew_zhjj_zll", {})
            if r: ax.set_title(f"Delphes mjj resolution (EW ZHjj, matched GenJets): $\\sigma_{{68}}$ = {100*r['sigma68_rel']:.0f}%", fontsize=9, color="#444")
        ax.axvline(OPT[var], color="#111", lw=1, ls=":"); ax.set_xlabel(xl); ax.set_ylabel("expected significance (def. a)")
        ax.set_ylim(bottom=0); ax.legend(fontsize=8, loc="lower left" if var == "deta" else "lower right"); fig.tight_layout()
        for ext in ("pdf", "png"): fig.savefig(f"{FIG}/{fname}.{ext}", dpi=150)
        plt.close(fig)
    # E: coupling figures
    if "choice" in CPL:
        fig, ax = plt.subplots(figsize=(6.4, 4.4))
        for L, col in ((500, "#2a78d6"), (1000, "#1baf7a"), (3000, "#eb6834")):
            r = CPL[f"lambda|{L}|fixed"]; ax.plot(r["lam"], r["q"], color=col, lw=2, label=f"{L} fb$^{{-1}}$, BR(H$\\to\\gamma\\gamma$) SM")
            r = CPL[f"lambda|{L}|resolved"]; ax.plot(r["lam"], r["q"], color=col, lw=1.2, ls="--", label=f"{L} fb$^{{-1}}$, resolved $\\kappa_\\gamma(\\kappa_W)$")
        for y, t in ((1, "68%"), (3.84, "95%")): ax.axhline(y, color="#777", lw=0.8, ls=":"); ax.text(1.75, y + 0.1, t, fontsize=8, color="#555")
        ax.set_xlabel(r"$\lambda_{WZ} = \kappa_W/\kappa_Z$ ($\kappa_Z = 1$)"); ax.set_ylabel(r"$-2\Delta\ln L$ (Asimov SM, profiled)"); ax.set_ylim(0, 12)
        ax.set_title(f"EW ZHjj, H$\\to\\gamma\\gamma$: binned fit in {CPL['choice']['observable']} (signal region)", fontsize=9, color="#444"); ax.legend(fontsize=7, ncol=2)
        fig.tight_layout(); [fig.savefig(f"{FIG}/lambdaWZ_scan.{e}", dpi=150) for e in ("pdf", "png")]; plt.close(fig)
        for L in (500, 3000):
            r = CPL[f"2d|{L}"]; K, Lm = np.meshgrid(r["lam"], r["kZ"]); Q = np.array(r["q"])
            fig, ax = plt.subplots(figsize=(6.0, 4.6)); cs = ax.contour(K, Lm, Q, levels=[2.30, 5.99], colors=["#2a78d6", "#eb6834"], linewidths=2)
            ax.clabel(cs, fmt={2.30: "68%", 5.99: "95%"}, fontsize=8); ax.plot([1], [1], "k*", ms=10, label="SM")
            ax.set_xlabel(r"$\lambda_{WZ}$"); ax.set_ylabel(r"$\kappa_Z$"); ax.legend(fontsize=8, loc="upper left")
            ax.set_title(f"Expected 2D contours, {L} fb$^{{-1}}$ (BR(H$\\to\\gamma\\gamma$) SM)", fontsize=9, color="#444")
            fig.tight_layout(); [fig.savefig(f"{FIG}/kappaZ_lambdaWZ_{L}.{e}", dpi=150) for e in ("pdf", "png")]; plt.close(fig)
        for var, lab, bins in (("mllgg", r"$m_{\ell\ell\gamma\gamma}$ [GeV]", np.linspace(100, 1500, 29)), ("ptgg", r"$p_T^{\gamma\gamma}$ [GeV]", np.linspace(0, 600, 25)),
                               ("mjj", r"$m_{jj}$ [GeV]", np.linspace(500, 4000, 29)), ("detajj", r"$|\Delta\eta_{jj}|$", np.linspace(3, 9, 25))):
            fig, ax = plt.subplots(figsize=(6.4, 4.4))
            for tag, col, lb in (("lam_p100", "#111", r"SM ($\lambda_{WZ}=1$)"), ("lam_m100", "#eb6834", r"$\lambda_{WZ}=-1$"), ("lam_p000", "#2a78d6", r"$\lambda_{WZ}=0$")):
                d = KREG[tag]["d"]; m = sr_mask(d); h = np.histogram(d[var][m], bins=bins, weights=np.full(m.sum(), KREG[tag]["w"]*3000))[0]
                ax.step(bins, np.r_[h, h[-1]], where="post", color=col, lw=2, label=lb)
            ax.set_xlabel(lab); ax.set_ylabel("events / bin (3000 fb$^{-1}$), signal region"); ax.legend(fontsize=8)
            ax.set_title("Delphes EW ZHjj at the optimum selection (incl. m$_{\\gamma\\gamma}$ window)", fontsize=9, color="#444")
            fig.tight_layout(); [fig.savefig(f"{FIG}/lambdaWZ_dist_{var}.{e}", dpi=150) for e in ("pdf", "png")]; plt.close(fig)
        if "cA|3000|noclip" in CPL:
            fig, ax = plt.subplots(figsize=(6.4, 4.4))
            for L, col in ((500, "#2a78d6"), (3000, "#eb6834")):
                for cl, ls in (("noclip", "-"), ("clip500", "--")):
                    r = CPL[f"cA|{L}|{cl}"]; ax.plot(r["cA"], r["q"], color=col, ls=ls, lw=2 if cl == "noclip" else 1.3, label=f"{L} fb$^{{-1}}$" + (", $m_{\\ell\\ell\\gamma\\gamma}$ < 500 GeV" if cl == "clip500" else ""))
            ax.axhline(3.84, color="#777", lw=0.8, ls=":"); ax.axhline(1, color="#777", lw=0.8, ls=":")
            ax.set_xlim(-1, 1); ax.set_ylim(0, 10); ax.set_xlabel(r"CP-odd $c_A = \sin\alpha\,\kappa_{AVV}$ ($\Lambda$ = 1 TeV)"); ax.set_ylabel(r"$-2\Delta\ln L$"); ax.legend(fontsize=8)
            fig.tight_layout(); [fig.savefig(f"{FIG}/cA_scan.{e}", dpi=150) for e in ("pdf", "png")]; plt.close(fig)
    print("figures ->", FIG)
