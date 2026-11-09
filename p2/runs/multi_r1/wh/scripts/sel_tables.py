#!/usr/bin/env python3
"""(fold = (evt + const(sample)) mod 5 since 2654435761 = 1 mod 5; folds disjoint in (sample, event).)
Build the flat selection table from the skims (05 selection stage): all rows of the VBS block region (bgmodel.regions: lepton pT>25 iso<0.15, no 2nd lepton pT>10, MET>30, photons pT>25 no crack, b-veto,
tag jets pT>30 mjj>500 |deta|>2.5, 100<mgg<180) for every class sample, with NOMINAL event weights (events at 500 fb^-1, BR once, fake factor nominal, f_l nominal 2x2e-5, C central, tau factor (1+r_tau) on W/Z classes), class id, kind and kinematic variables.
Usage: bash scripts/envrun.sh python3 -P scripts/sel_tables.py  -> work/sel/table.npz (+ table_meta.json)"""
import sys, os, json, numpy as np
sys.path.insert(0, "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh/scripts")
from bgmodel import *
Y = json.load(open(f"{WH}/work/bgmodel/yields.json")); RTAU = Y["regions"]["VBS"]["r_tau"]
CL = {"signal": ["S_EW_WHjj"], "prompt_irreducible": ["B_QCD_Waajj_nomjj", "B_EW_Waajj_nomjj", "T_ttaa_1l"], "fake_photon_1": ["F_QCD_Wajjj_nomjj", "F_EW_Wajj_nomjj", "T_tta_1l", "T_tWa_1l"], "fake_photon_2": ["F_Wjjjj", "T_ttjj_1l"],
      "nonprompt_lepton": ["Q_aajjj", "H_VBFH_jj", "H_ggF_jj"], "lost_lepton_egamma": ["V_WWa_WH", "V_WZa_WH", "V_ZZa_WH", "ZH_Zaajj_QCD_nomjj_lostlep", "ZH_Zaajj_EW_lostlep", "ZH_Zajj_eFake"] + (["F_QCD_llajj_loose"] if os.environ.get("V11") == "1" else []),
      "other_higgs": ["H_QCD_WH_mlm", "H_ggZH_wh", "H_ZH_tautau_wh", "H_ttH_1l", "H_ttH_dilep_wh", "H_tHq_lep", "H_tHW_1l", "ZH_EW_ZHjj_lostlep", "ZH_QCD_ZHjj_lostlep"], "tau_feeddown": ["S_EW_WHjj_taunu"]}
V11 = os.environ.get('V11') == '1'   # v1.1: F_QCD_llajj_loose replaces the QCD part of ZH_Zajj_eFake (EW part kept)
KMODE = os.environ.get('KSAMPLES') == '1'
if KMODE: CL = {'K': ['K_EW_WHjj_' + x for x in ('lam_m100', 'lam_m050', 'lam_p000', 'lam_p050', 'lam_p100', 'lam_p150', 'kap_W15_Z075', 'kap_W05_Z15', 'cpo_p2', 'cpo_m2')]}
TAUC = {"prompt_irreducible", "fake_photon_1", "fake_photon_2", "lost_lepton_egamma", "other_higgs"}; FNOM = 4e-5
CID = {c: i for i, c in enumerate(CL)}
OUTN = 'table_K' if KMODE else ('table_v11' if V11 else 'table'); cols = {}; meta = {"classes": CID, "samples": [], "r_tau": RTAU}
def add(k, v): cols.setdefault(k, []).append(v)
for c, ss in CL.items():
    for s in ss:
        D = load(s)
        if D is None: continue
        R, d = regions(D); m = R["VBS"]
        if V11 and s == "ZH_Zajj_eFake": m &= ~np.char.startswith(D["dirname"].astype(str), "F_QCD")
        kind = D["kind"]; w = D["w"]*D["norm"]*LUMI*D["cfac"][:, 0]
        if c in ("fake_photon_1", "fake_photon_2"): m &= (kind == (1 if c == "fake_photon_1" else 2)); w = w*D["f"][:, 0]
        elif c == "nonprompt_lepton":   # 05a v2.1 nominal: light-misID (kind 5, f_l nominal) x (1 + factorised heavy flavour hf_PRE/Y5_PRE); direct rows (kind 0) are NOT used (HF is the factorised variant)
            ys = Y["regions"]["PRE"]["samples"][s]; ratio = ys["heavy_flavour_factorised"]["hf_PRE_direct"]/ys["fakelep_nom"]["Y"] if ys["fakelep_nom"]["Y"] > 0 else 0.0
            m &= (kind == 5); whf = w*FNOM*ratio; w = w*FNOM*(1+ratio)
        else: m &= (kind == 0)
        if KMODE: whf = np.zeros(len(w))
        elif c != "nonprompt_lepton": whf = np.zeros(len(w))
        if c in TAUC: w = w*(1+RTAU)
        lep, ph, j, met = D["lep"][m], D["ph"][m], D["jets"][m], D["met"][m]; n = int(m.sum()); sid = len(meta["samples"]); meta["samples"].append(s)
        e1 = ph[:, 0]; e2 = ph[:, 1]; px_l = lep[:, 0]*np.cos(lep[:, 2]); py_l = lep[:, 0]*np.sin(lep[:, 2])
        px = e1[:, 0]*np.cos(e1[:, 2])+e2[:, 0]*np.cos(e2[:, 2]); py = e1[:, 0]*np.sin(e1[:, 2])+e2[:, 0]*np.sin(e2[:, 2]); pz = e1[:, 0]*np.sinh(e1[:, 1])+e2[:, 0]*np.sinh(e2[:, 1]); Eg = e1[:, 0]*np.cosh(e1[:, 1])+e2[:, 0]*np.cosh(e2[:, 1])
        ptgg = np.hypot(px, py); etagg = np.arcsinh(pz/np.maximum(ptgg, 1e-6)); mgg = d["mgg"][m]
        dphi = lambda a, b: (a-b+np.pi) % (2*np.pi)-np.pi
        drgg = np.hypot(e1[:, 1]-e2[:, 1], dphi(e1[:, 2], e2[:, 2])); mt = np.sqrt(np.maximum(2*lep[:, 0]*met[:, 0]*(1-np.cos(dphi(lep[:, 2], met[:, 1]))), 0))
        eta1, eta2 = j[:, 0, 1], j[:, 1, 1]; zstar = np.abs(etagg-0.5*(eta1+eta2))/np.maximum(np.abs(eta1-eta2), 1e-3)
        drlg = np.minimum(np.hypot(lep[:, 1]-e1[:, 1], dphi(lep[:, 2], e1[:, 2])), np.hypot(lep[:, 1]-e2[:, 1], dphi(lep[:, 2], e2[:, 2])))
        dphijj_gg = np.abs(dphi(np.arctan2(j[:, 0, 0]*np.sin(j[:, 0, 2])+j[:, 1, 0]*np.sin(j[:, 1, 2]), j[:, 0, 0]*np.cos(j[:, 0, 2])+j[:, 1, 0]*np.cos(j[:, 1, 2])), np.arctan2(py, px)))
        for k_, v in dict(w=w[m], whf=whf[m], cls=np.full(n, CID[c], np.int8), sid=np.full(n, sid, np.int16), kind=kind[m], evt=D["evt"][m], mjj=d["mjj"][m], deta=d["deta"][m], mgg=mgg, ptgg=ptgg, drgg=drgg, ptl=lep[:, 0], etal=lep[:, 1], mt=mt, met=met[:, 0],
                          pt1=e1[:, 0], pt2=e2[:, 0], pt1m=e1[:, 0]/mgg, pt2m=e2[:, 0]/mgg, ptggm=ptgg/mgg, ptj1=j[:, 0, 0], ptj2=j[:, 1, 0], etaj1=eta1, etaj2=eta2, zstar=zstar, drlg=drlg, dphijjgg=dphijj_gg, njets=D["njets"][m], ptj3=j[:, 2, 0], mtwgg=np.sqrt(np.maximum((np.sqrt(mgg**2+ptgg**2)+np.sqrt(80.4**2+(np.hypot(px_l+met[:, 0]*np.cos(met[:, 1]), py_l+met[:, 0]*np.sin(met[:, 1])))**2))**2-((px+px_l+met[:, 0]*np.cos(met[:, 1]))**2+(py+py_l+met[:, 0]*np.sin(met[:, 1]))**2), 0)),
                          ncls1=(ph[:, :, 3] == 1).sum(1), qcddir=np.char.startswith(D["dirname"][m].astype(str), "F_QCD"), fold=((D["evt"][m].astype(np.int64)*2654435761+sid*40503) % 5).astype(np.int8)).items(): add(k_, np.asarray(v, np.float64) if k_ not in ("cls", "sid", "kind", "evt", "fold", "ncls1", "qcddir") else v)
        if (c in ("signal", "tau_feeddown") or s == "H_QCD_WH_mlm") and not KMODE: cols.setdefault("lhe_" + s, []).append(D["lhe"][m].astype(np.float32))   # LHE weights (145 / 147) for the theory nuisances and defs (b)
        print(c, s, n, float(w[m].sum()), flush=True)
LH = {k: np.concatenate(v) for k, v in cols.items() if k.startswith("lhe_")}; cols = {k: v for k, v in cols.items() if not k.startswith("lhe_")}
np.savez_compressed(f"{WH}/work/sel/lhe_rows{OUTN[5:]}.npz", **LH)
np.savez_compressed(f"{WH}/work/sel/{OUTN}.npz", **{k: np.concatenate(v) for k, v in cols.items()}); json.dump(meta, open(f"{WH}/work/sel/{OUTN}_meta.json", "w"), indent=1)
