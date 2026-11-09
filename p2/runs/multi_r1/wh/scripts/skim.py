#!/usr/bin/env python3
"""Background-model / analysis skim (executor-wh FINAL, 05a). One input file -> one npz of candidate ROWS. Usage:
  skim.py <sample> <slim.root> <out.npz> [--rates work/bgmodel/rate_table.json]
A row = one analysis configuration of an event: lepton + two photons + remaining jets + MET + weight columns. Rows are produced by the model of `mode`:
 real2  : the two leading REAL photons (cls0 prompt-matched, cls1 e->gamma object within dR<0.2 of a prompt gen lepton).             kind 0
 fake1  : (n_prompt_photons==1) leading cls0 photon + one reco jet converted to a photon (weight = fake factor)                       kind 1
          direct counterparts: cls0 + leading cls2 (genuine in-jet) photon (kind 3, closure), + leading cls2/3 (artefact included, UPPER variation, kind 4)
 fake2  : (n_prompt_photons==0) two converted jets (weight f_a*f_b; kind 2); direct counterparts kind 3/4 with two cls2 / cls2-3 photons
 qlep   : real2 photons; DIRECT lepton rows (kind 0: a reco lepton from Delphes, heavy flavour and anything else kept) and per-jet fake-lepton rows
          (kind 5: events with no reco lepton pT>10; each jet pT>25,|eta|<2.4 may be the lepton, lepton pT = x*pT_jet, x~N(0.85,0.1) trunc [0.5,1]; weight column 1, scaled by f_l at analysis)
Photon classes (GenTruth, production slim files have no Particle record): cls0 prompt gen photon (prompt flag) within dR<0.1; cls1 prompt gen lepton within dR<0.2;
 else R = sum pT(gph within dR<0.2)/pT_reco: cls2 genuine non-prompt in-jet photon (R>=0.5), cls3 Delphes energy-flow artefact (R<0.5)  [veto validated in 05a sec. 1].
Skim (superset of every later selection; documented in 05a): exactly one lepton pT>25 (e |eta|<2.5, mu <2.4; others only recorded in nlep10), MET>20, photons pT>20 |eta|<2.5, 100<m_gg<180,
 remaining jets (pT>25,|eta|<4.7, dR>0.4 to lepton and photons, consumed jets removed): leading two pT>30 with m_jj>300 and |deta_jj|>2.0.
Weights: w_pb = Event.Weight[0] (signed, pb); yields at lumi L: L*1e3*k*sum(w_pb*f)/N_generated (SAMPLES.csv).  f columns (fake photons): nominal, up, dn, f_all (artefact-included rate), R0.3, R0.7."""
import sys, os, re, json, numpy as np, uproot, awkward as ak
CFG = {  # sample: (mode, rate class, keep LHE weights: 0 none, 1 all 145, 2 the 9 scale-variation entries 0,5,10,15,22,24,29,34,39)
    "S_EW_WHjj": ("real2", None, 1), "S_EW_WHjj_taunu": ("real2", None, 1), "B_QCD_Waajj_nomjj": ("real2", None, 1), "B_EW_Waajj_nomjj": ("real2", None, 1),
    "F_EW_Wajj_nomjj": ("fake1", "W", 2), "F_QCD_Wajjj_nomjj": ("fake1", "W", 2), "F_QCD_Wajj_nomjj": ("fake1", "W", 2), "F_Wjjjj": ("fake2", "W", 2),
    "T_ttjj_1l": ("fake2", "TT", 2), "T_tta_1l": ("fake1", "TT", 2), "T_tWa_1l": ("fake1", "TT", 2), "T_ttaa_1l": ("real2", None, 2),
    "V_WWa_WH": ("real2", None, 2), "V_WZa_WH": ("real2", None, 2), "V_ZZa_WH": ("real2", None, 2),
    "H_QCD_WH_mlm": ("real2", None, 1), "H_QCD_WHjj_fixed": ("real2", None, 1), "H_ggZH_wh": ("real2", None, 2), "H_ZH_tautau_wh": ("real2", None, 2), "H_ttH_1l": ("real2", None, 2),
    "H_ttH_dilep_wh": ("real2", None, 2), "H_tHq_lep": ("real2", None, 2), "H_tHW_1l": ("real2", None, 2), "H_VBFH_jj": ("qlep", None, 2), "H_ggF_jj": ("qlep", None, 2),
    "Q_aajj": ("qlep", None, 2), "Q_aajjj": ("qlep", None, 2),
    "ZH_Zaajj_QCD_nomjj_lostlep": ("real2", None, 2), "ZH_Zaajj_EW_lostlep": ("real2", None, 2), "ZH_Zajj_eFake": ("real2", None, 2), "ZH_EW_ZHjj_lostlep": ("real2", None, 2), "ZH_QCD_ZHjj_lostlep": ("real2", None, 2)}
for s in ("lam_m100", "lam_m050", "lam_p000", "lam_p050", "lam_p100", "lam_p150", "kap_W15_Z075", "kap_W05_Z15", "cpo_p2", "cpo_m2"): CFG["K_EW_WHjj_" + s] = ("real2", None, 1)
PTG, JETPT, TAGPT = 20.0, 25.0, 30.0
def dphi(a, b): return (a-b+np.pi) % (2*np.pi)-np.pi
def dr(e1, p1, e2, p2): return np.hypot(e1-e2, dphi(p1, p2))
def lv(pt, eta, phi): return np.array([pt*np.cos(phi), pt*np.sin(phi), pt*np.sinh(eta), pt*np.cosh(eta)])
def minv(a, b): s = a+b; return float(np.sqrt(max(s[3]**2-s[0]**2-s[1]**2-s[2]**2, 0.0)))
def run(sample, slim, outnpz, ratefile=None, lumi_dummy=None):
    mode, rcls, keeplhe = CFG[sample]; seed = int(re.search(r"_s(\d+)\.root", slim).group(1)); rng = np.random.default_rng(seed + 777)
    RT = json.load(open(ratefile)) if ratefile and rcls else None
    if RT:
        PTE = np.array(RT["pt_edges"]); XE = np.array(RT["x_edges"]); XH = np.array(RT["x_hist_" + rcls], float)
        FV = {k: np.array(RT[k + "_" + rcls]) for k in ("nom", "up", "dn", "all", "r03", "r07")}
    def ptbin(pt): return min(max(int(np.digitize(pt, PTE)-1), 0), len(PTE)-2)
    def frates(pt, eta):
        ie = 0 if abs(eta) < 1.5 else 1; ib = ptbin(pt); return np.array([FV[k][ie, ib] for k in ("nom", "up", "dn", "all", "r03", "r07")])
    def drawx(pt):
        h = XH[ptbin(pt)]
        if h.sum() <= 0: h = XH.sum(0)
        c = np.cumsum(h)/h.sum(); k = int(np.searchsorted(c, rng.random())); k = min(k, len(XE)-2); return 0.5*(XE[k]+XE[k+1])
    T = uproot.open(slim)["Delphes"]; G = uproot.open(slim[:-5]+"_gen.root")["GenTruth"]; N = T.num_entries
    br = ["Electron.PT", "Electron.Eta", "Electron.Phi", "Electron.Charge", "Electron.IsolationVarRhoCorr", "Muon.PT", "Muon.Eta", "Muon.Phi", "Muon.Charge", "Muon.IsolationVarRhoCorr",
          "Photon.PT", "Photon.Eta", "Photon.Phi", "Photon.IsolationVarRhoCorr", "Photon.EhadOverEem", "Jet.PT", "Jet.Eta", "Jet.Phi", "Jet.Mass", "Jet.BTag", "MissingET.MET", "MissingET.Phi", "Event.Weight"]
    a = T.arrays(br, library="ak"); g = G.arrays(["n_prompt_photons", "gph_pt", "gph_eta", "gph_phi", "gph_prompt", "glep_pt", "glep_eta", "glep_phi", "glep_prompt"], library="ak")
    w = ak.to_numpy(ak.firsts(a["Event.Weight"])).astype(float); npr = ak.to_numpy(g["n_prompt_photons"])
    met = ak.to_numpy(ak.fill_none(ak.firsts(a["MissingET.MET"]), 0.0)); mphi = ak.to_numpy(ak.fill_none(ak.firsts(a["MissingET.Phi"]), 0.0))
    el = (a["Electron.PT"] > 10) & (abs(a["Electron.Eta"]) < 2.5); mu = (a["Muon.PT"] > 10) & (abs(a["Muon.Eta"]) < 2.4)
    nl10 = ak.sum(el, axis=1) + ak.sum(mu, axis=1); nl25 = ak.sum(el & (a["Electron.PT"] > 25), axis=1) + ak.sum(mu & (a["Muon.PT"] > 25), axis=1)
    nph = ak.sum((a["Photon.PT"] > PTG) & (abs(a["Photon.Eta"]) < 2.5), axis=1); nj = ak.sum((a["Jet.PT"] > JETPT) & (abs(a["Jet.Eta"]) < 4.7), axis=1)
    nlep = ak.to_numpy(nl25) == 1; nolep = ak.to_numpy(nl10) == 0
    cf = {"n_events": N, "sum_w": float(w.sum()), "sum_absw": float(np.abs(w).sum())}
    def stage(name, m): cf[name] = [int(m.sum()), float(w[m].sum())]
    allm = np.ones(N, bool); stage("all", allm)
    if mode == "fake1": base = npr == 1
    elif mode == "fake2": base = npr == 0
    else: base = allm
    stage("npr_condition", base)
    lepok = (nlep | nolep) if mode == "qlep" else nlep
    m1 = base & lepok; stage("lepton", m1)
    m2 = m1 & (met > 20); stage("MET>20", m2)
    need_g = {"real2": 2, "qlep": 2, "fake1": 1, "fake2": 0}[mode]; need_j = {"real2": 2, "qlep": 2, "fake1": 3, "fake2": 4}[mode]
    m3 = m2 & (ak.to_numpy(nph) >= need_g) & (ak.to_numpy(nj) >= need_j); stage("photon/jet multiplicity", m3)
    # direct (kind 3/4) rows need photons objects too: for fake modes the reco photon multiplicity pre-cut is only for the real photon; use jets
    idx = np.nonzero(m3)[0]
    S = {k: ak.to_list(a[k][idx]) for k in br if k != "Event.Weight"}; GG = {k: ak.to_list(g[k][idx]) for k in g.fields if k != "n_prompt_photons"}
    rows = {k: [] for k in ("evt", "kind", "w", "f", "lep", "ph", "met", "jets", "njets")}; lhe = []
    SC9 = [0, 5, 10, 15, 22, 24, 29, 34, 39]   # (MUR,MUF) = (.5,.5),(.5,1),(.5,2),(1,.5),(1,1)=nominal,(1,2),(2,.5),(2,1),(2,2), dyn_scale_choice 3 (04 FORMAT sec. 4)
    WL = T["WeightLHEF/WeightLHEF.Weight"].array(library="ak")[idx] if keeplhe else None
    if keeplhe == 2: WL = ak.to_numpy(WL)[:, SC9]
    nrow = {k: 0 for k in range(6)}; ev_with_row = set()
    for n, i in enumerate(idx):
        # leptons
        L = sorted([(S["Electron.PT"][n][k], S["Electron.Eta"][n][k], S["Electron.Phi"][n][k], 11*S["Electron.Charge"][n][k]*-1, S["Electron.IsolationVarRhoCorr"][n][k]) for k in range(len(S["Electron.PT"][n])) if S["Electron.PT"][n][k] > 10 and abs(S["Electron.Eta"][n][k]) < 2.5] +
                   [(S["Muon.PT"][n][k], S["Muon.Eta"][n][k], S["Muon.Phi"][n][k], 13*S["Muon.Charge"][n][k]*-1, S["Muon.IsolationVarRhoCorr"][n][k]) for k in range(len(S["Muon.PT"][n])) if S["Muon.PT"][n][k] > 10 and abs(S["Muon.Eta"][n][k]) < 2.4], reverse=True)
        gp = list(zip(GG["gph_pt"][n], GG["gph_eta"][n], GG["gph_phi"][n], GG["gph_prompt"][n])); gl = [(e, p) for e, p, q, r in zip(GG["glep_eta"][n], GG["glep_phi"][n], GG["glep_pt"][n], GG["glep_prompt"][n]) if r and q > 10]
        P = []   # reco photons: (pt, eta, phi, cls, iso, ehad)
        for k in range(len(S["Photon.PT"][n])):
            q, e, p = S["Photon.PT"][n][k], S["Photon.Eta"][n][k], S["Photon.Phi"][n][k]
            if q <= PTG or abs(e) >= 2.5: continue
            if any(pr and dr(e, p, ge, gf) < 0.1 for _, ge, gf, pr in gp): cls = 0
            elif any(dr(e, p, le, lp) < 0.2 for le, lp in gl): cls = 1
            else:
                R = sum(gq for gq, ge, gf, _ in gp if dr(e, p, ge, gf) < 0.2)/q; cls = 2 if R >= 0.5 else 3
            P.append((q, e, p, cls, S["Photon.IsolationVarRhoCorr"][n][k], S["Photon.EhadOverEem"][n][k]))
        P.sort(reverse=True)
        Jall = sorted([(S["Jet.PT"][n][k], S["Jet.Eta"][n][k], S["Jet.Phi"][n][k], S["Jet.Mass"][n][k], float(S["Jet.BTag"][n][k])) for k in range(len(S["Jet.PT"][n])) if S["Jet.PT"][n][k] > JETPT and abs(S["Jet.Eta"][n][k]) < 4.7], reverse=True)
        def emit(kind, lep, phs, consumed, f6, lepmode_fake=False):
            Jr = [j for j in Jall if j not in consumed and all(dr(j[1], j[2], x[1], x[2]) > 0.4 for x in phs) and dr(j[1], j[2], lep[1], lep[2]) > 0.4]
            if len(Jr) < 2 or Jr[0][0] <= TAGPT or Jr[1][0] <= TAGPT: return
            if abs(Jr[0][1]-Jr[1][1]) <= 2.0 or minv(lv_m(Jr[0]), lv_m(Jr[1])) <= 300: return
            mgg = minv(lv(*phs[0][:3]), lv(*phs[1][:3]))
            if not (100 < mgg < 180): return
            jj = np.zeros((6, 5));
            for k, j in enumerate(Jr[:6]): jj[k] = j
            rows["evt"].append(int(i)); rows["kind"].append(kind); rows["w"].append(w[i]); rows["f"].append(f6)
            rows["lep"].append([lep[0], lep[1], lep[2], lep[3], lep[4], len(L)]); rows["ph"].append([[x[0], x[1], x[2], x[3], x[4], x[5]] for x in phs]); rows["met"].append([met[i], mphi[i]]); rows["jets"].append(jj); rows["njets"].append(len(Jr))
            if keeplhe: lhe.append(np.asarray(WL[n], dtype=np.float32))
            nrow[kind] += 1; ev_with_row.add(int(i))
        def lv_m(j):
            pt, eta, phi, m = j[:4]; return np.array([pt*np.cos(phi), pt*np.sin(phi), pt*np.sinh(eta), np.sqrt((pt*np.cosh(eta))**2+m*m)])
        ONE = np.ones(6)
        if mode in ("real2", "qlep"):
            R2 = [x for x in P if x[3] in (0, 1)][:2]
            if len(R2) < 2: continue
            if sum(1 for l in L if l[0] > 25) == 1:
                lead = [l for l in L if l[0] > 25][0]; emit(0, lead, R2, [], ONE)
            if mode == "qlep" and len(L) == 0:
                for jk, j in enumerate(Jall):
                    if j[0] <= 25 or abs(j[1]) >= 2.4: continue
                    x = float(np.clip(rng.normal(0.85, 0.10), 0.5, 1.0))
                    if x*j[0] <= 25: continue
                    emit(5, (x*j[0], j[1], j[2], 0.0, 0.0), R2, [j], ONE)
        else:
            lead = [l for l in L if l[0] > 25]
            if len(lead) != 1: continue
            lead = lead[0]; real = [x for x in P if x[3] == 0]; gen = [x for x in P if x[3] == 2]; npn = [x for x in P if x[3] in (2, 3)]
            if mode == "fake1":
                if not real: continue
                r0 = real[0]
                cand = [j for j in Jall if j[0] > 25 and abs(j[1]) < 2.5 and dr(j[1], j[2], lead[1], lead[2]) > 0.4 and dr(j[1], j[2], r0[1], r0[2]) > 0.4]
                for j in cand:
                    x = drawx(j[0]); q = x*j[0]
                    if q <= PTG: continue
                    emit(1, lead, sorted([r0, (q, j[1], j[2], 2, 0.0, 0.0)], reverse=True), [j], frates(j[0], j[1]))
                if gen: emit(3, lead, sorted([r0, gen[0]], reverse=True), [], ONE)
                if npn: emit(4, lead, sorted([r0, npn[0]], reverse=True), [], ONE)
            else:
                cand = [j for j in Jall if j[0] > 25 and abs(j[1]) < 2.5 and dr(j[1], j[2], lead[1], lead[2]) > 0.4]
                xs = {id(j): drawx(j[0]) for j in cand}
                for a_ in range(len(cand)):
                    for b_ in range(a_+1, len(cand)):
                        ja, jb = cand[a_], cand[b_]
                        if dr(ja[1], ja[2], jb[1], jb[2]) <= 0.4: continue
                        qa, qb = xs[id(ja)]*ja[0], xs[id(jb)]*jb[0]
                        if qa <= PTG or qb <= PTG: continue
                        emit(2, lead, sorted([(qa, ja[1], ja[2], 2, 0.0, 0.0), (qb, jb[1], jb[2], 2, 0.0, 0.0)], reverse=True), [ja, jb], frates(ja[0], ja[1])*frates(jb[0], jb[1]))
                if len(gen) >= 2: emit(3, lead, gen[:2], [], ONE)
                if len(npn) >= 2: emit(4, lead, npn[:2], [], ONE)
    out = dict(evt=np.array(rows["evt"], np.int32), kind=np.array(rows["kind"], np.int8), w=np.array(rows["w"]), f=np.array(rows["f"]).reshape(-1, 6), lep=np.array(rows["lep"], np.float32).reshape(-1, 6),
               ph=np.array(rows["ph"], np.float32).reshape(-1, 2, 6), met=np.array(rows["met"], np.float32).reshape(-1, 2), jets=np.array(rows["jets"], np.float32).reshape(-1, 6, 5), njets=np.array(rows["njets"], np.int16))
    if keeplhe: out["lhe"] = np.array(lhe, np.float32).reshape(len(lhe), -1) if lhe else np.zeros((0, 9 if keeplhe == 2 else 145), np.float32)
    cf["rows_by_kind"] = nrow; cf["events_with_row"] = len(ev_with_row); cf["sum_w_events_with_row"] = float(w[sorted(ev_with_row)].sum()) if ev_with_row else 0.0
    np.savez_compressed(outnpz, **out); json.dump(dict(sample=sample, file=slim, seed=seed, mode=mode, cutflow=cf), open(outnpz[:-4] + ".json", "w"))
if __name__ == "__main__":
    rf = sys.argv[sys.argv.index("--rates")+1] if "--rates" in sys.argv else None
    run(sys.argv[1], sys.argv[2], sys.argv[3], rf)
