#!/usr/bin/env python3
"""B2/B3: event-level orthogonality of the frozen ZH SR and the WH SR (cut-based primary). Read-only on all inputs.
Usage: ortho.py <out.json> <sample_label> <files comma list>
ZH SR (frozen optimum, final.json 'optimum'): OSSF pair (e: pT>15,|eta|<2.5; mu: pT>15,|eta|<2.4; m_ll closest to mZ), >=2 photons (pT>20,|eta|<2.5, no crack, dR>0.4 to the pair), jets pT>25 |eta|<4.7 dR>0.4
 to leptons and leading two photons (>=2), |mll-mZ|<25, mllgg>100, pT_gamma>25, pT1/mgg>1/3, pT2/mgg>0.25, mjj>500, |deta_jj|>3.5, |mgg-mu|<2 sigma_core.
WH SR (05_selection.md primary, bgmodel.regions + sel_final cuts): exactly one lepton with pT>10 (e |eta|<2.5, mu <2.4) and its pT>25, RhoCorr isolation <0.15; MET>30; two leading photons (pT>20 |eta|<2.5) both pT>25,
 neither in the crack (1.4442-1.566); b-veto (remaining jets pT>30,|eta|<2.5,BTag>0), remaining jets (pT>25,|eta|<4.7, dR>0.4 to lepton and to the two photons) leading two pT>30; mjj>600, |deta_jj|>4.0, pT_gg>75, |mgg-125|<3.5.
Flags counted per file (raw n, sum Event.Weight [pb], sum w^2): all, zh_pre (OSSF + 2 photons + 2 jets), zh_sr, wh_pre (lepton block + MET + 2 photons >25 + 2 jets), wh_sr, both_pre, both_sr, plus zh_sr_nl10eq1 (ZH SR events with exactly one pT>10 lepton: must be 0)."""
import sys, json, numpy as np, awkward as ak, uproot
MZ = 91.1876; MU_ZH, SIG_ZH = 124.9, 2.07
FZ = json.load(open("/eos/home-r/rjiang/vbs_zh_codex_starter/work/final_ntuples/final.json")); MU_ZH, SIG_ZH = FZ["resolution"]["mu"], FZ["resolution"]["sigma_core"]; OPT = FZ["optimum"]
out, label, files = sys.argv[1], sys.argv[2], sys.argv[3].split(",")
def dphi(a, b): return (a - b + np.pi) % (2*np.pi) - np.pi
def dR(e1, p1, e2, p2): return np.hypot(e1 - e2, dphi(p1, p2))
def mass(pts, etas, phis, ms):
    px = sum(p*np.cos(f) for p, f in zip(pts, phis)); py = sum(p*np.sin(f) for p, f in zip(pts, phis)); pz = sum(p*np.sinh(e) for p, e in zip(pts, etas))
    E = sum(np.sqrt((p*np.cosh(e))**2 + m**2) for p, e, m in zip(pts, etas, ms)); return np.sqrt(max(E**2 - px**2 - py**2 - pz**2, 0.0))
def rap(pt, eta, phi, m):
    E = np.sqrt((pt*np.cosh(eta))**2 + m**2); pz = pt*np.sinh(eta); return 0.5*np.log((E + pz)/(E - pz))
NOWIN = []   # ZH-SR events without the m_gg window: (mgg, w, mjj-pass)
FL = ["all", "zh_pre", "zh_sr", "wh_pre", "wh_sr", "both_pre", "both_sr", "zh_sr_nl10eq1", "zh_pre_nl10eq1"]
C = {k: [0, 0.0, 0.0] for k in FL}; N = 0
def add(k, w): C[k][0] += 1; C[k][1] += w; C[k][2] += w*w
for f in files:
    t = uproot.open(f)["Delphes"]; n = t.num_entries; N += n
    g = lambda c, ks: {k: t[f"{c}/{c}.{k}"].array(library="ak") for k in ks.split()}
    El, Mu, Ph, Jt = g("Electron", "PT Eta Phi Charge IsolationVarRhoCorr"), g("Muon", "PT Eta Phi Charge IsolationVarRhoCorr"), g("Photon", "PT Eta Phi"), g("Jet", "PT Eta Phi Mass BTag")
    met = ak.to_numpy(ak.fill_none(ak.firsts(t["MissingET/MissingET.MET"].array(library="ak")), 0.0)); W = ak.to_numpy(ak.firsts(t["Event.Weight"].array(library="ak"))).astype(float)
    L = lambda: None
    ne10 = ak.to_numpy(ak.sum((El["PT"] > 10) & (abs(El["Eta"]) < 2.5), axis=1)); nm10 = ak.to_numpy(ak.sum((Mu["PT"] > 10) & (abs(Mu["Eta"]) < 2.4), axis=1)); nl10 = ne10 + nm10
    ne15 = ak.to_numpy(ak.sum((El["PT"] > 15) & (abs(El["Eta"]) < 2.5), axis=1)); nm15 = ak.to_numpy(ak.sum((Mu["PT"] > 15) & (abs(Mu["Eta"]) < 2.4), axis=1))
    ngam = ak.to_numpy(ak.sum((Ph["PT"] > 20) & (abs(Ph["Eta"]) < 2.5), axis=1)); nj = ak.to_numpy(ak.sum((Jt["PT"] > 25) & (abs(Jt["Eta"]) < 4.7), axis=1))
    cand = np.where(((ne15 >= 2) | (nm15 >= 2) | ((nl10 == 1))) & (ngam >= 2) & (nj >= 2))[0]
    for i in range(n):
        pass
    for i in range(n): add("all", W[i]) if False else None
    C["all"][0] += n; C["all"][1] += float(W.sum()); C["all"][2] += float((W**2).sum())
    EL = ak.to_list(ak.zip({"pt": El["PT"], "eta": El["Eta"], "phi": El["Phi"], "q": El["Charge"], "iso": El["IsolationVarRhoCorr"]})[cand]); MUL = ak.to_list(ak.zip({"pt": Mu["PT"], "eta": Mu["Eta"], "phi": Mu["Phi"], "q": Mu["Charge"], "iso": Mu["IsolationVarRhoCorr"]})[cand])
    PHL = ak.to_list(ak.zip({"pt": Ph["PT"], "eta": Ph["Eta"], "phi": Ph["Phi"]})[cand]); JL = ak.to_list(ak.zip({"pt": Jt["PT"], "eta": Jt["Eta"], "phi": Jt["Phi"], "m": Jt["Mass"], "b": Jt["BTag"]})[cand])
    for ii, i in enumerate(cand):
        w = W[i]; e_ = EL[ii]; m_ = MUL[ii]
        # ------------------------------ ZH SR
        best = None
        for coll, mass_l, etamax in ((e_, 0.000511, 2.5), (m_, 0.1057, 2.4)):
            s = [x for x in coll if x["pt"] > 15 and abs(x["eta"]) < etamax]
            for a in range(len(s)):
                for b in range(a+1, len(s)):
                    if s[a]["q"]*s[b]["q"] < 0:
                        mm = mass([s[a]["pt"], s[b]["pt"]], [s[a]["eta"], s[b]["eta"]], [s[a]["phi"], s[b]["phi"]], [mass_l, mass_l])
                        if best is None or abs(mm - MZ) < abs(best[0] - MZ): best = (mm, s[a], s[b], mass_l)
        zh_pre = zh_sr = False
        if best is not None:
            mll, la, lb, ml = best
            G = sorted([(p["pt"], p["eta"], p["phi"]) for p in PHL[ii] if p["pt"] > 20 and abs(p["eta"]) < 2.5 and not (1.4442 < abs(p["eta"]) < 1.566) and dR(p["eta"], p["phi"], la["eta"], la["phi"]) > 0.4 and dR(p["eta"], p["phi"], lb["eta"], lb["phi"]) > 0.4], reverse=True)
            if len(G) >= 2:
                J = [j for j in JL[ii] if j["pt"] > 25 and abs(j["eta"]) < 4.7 and dR(j["eta"], j["phi"], la["eta"], la["phi"]) > 0.4 and dR(j["eta"], j["phi"], lb["eta"], lb["phi"]) > 0.4 and all(dR(j["eta"], j["phi"], x[1], x[2]) > 0.4 for x in G[:2])]
                if len(J) >= 2:
                    zh_pre = True
                    mgg = mass([G[0][0], G[1][0]], [G[0][1], G[1][1]], [G[0][2], G[1][2]], [0, 0]); mllgg = mass([la["pt"], lb["pt"], G[0][0], G[1][0]], [la["eta"], lb["eta"], G[0][1], G[1][1]], [la["phi"], lb["phi"], G[0][2], G[1][2]], [ml, ml, 0, 0])
                    J = sorted(J, key=lambda j: -j["pt"]); mjj = mass([J[0]["pt"], J[1]["pt"]], [J[0]["eta"], J[1]["eta"]], [J[0]["phi"], J[1]["phi"]], [J[0]["m"], J[1]["m"]])
                    zh_nw = (abs(mll - MZ) < OPT["zwin"] and mllgg > OPT["mllgg"] and G[0][0] > OPT["gpt"] and G[1][0] > OPT["gpt"] and G[0][0]/mgg > OPT["ratio"][0] and G[1][0]/mgg > OPT["ratio"][1]
                             and mjj > OPT["mjj"] and abs(J[0]["eta"] - J[1]["eta"]) > OPT["deta"])
                    zh_sr = zh_nw and abs(mgg - MU_ZH) < OPT["wk"]*SIG_ZH
                    if zh_nw and 105 < mgg < 165: NOWIN.append((float(mgg), float(w)))
        # ------------------------------ WH SR
        Ls = [("e", x) for x in e_ if x["pt"] > 10 and abs(x["eta"]) < 2.5] + [("m", x) for x in m_ if x["pt"] > 10 and abs(x["eta"]) < 2.4]
        wh_pre = wh_sr = False
        if len(Ls) == 1 and Ls[0][1]["pt"] > 25 and Ls[0][1]["iso"] < 0.15 and met[i] > 30:
            lep = Ls[0][1]
            G = sorted([(p["pt"], p["eta"], p["phi"]) for p in PHL[ii] if p["pt"] > 20 and abs(p["eta"]) < 2.5], reverse=True)[:2]
            if len(G) == 2 and G[0][0] > 25 and G[1][0] > 25 and not any(1.4442 < abs(x[1]) < 1.566 for x in G):
                J = sorted([j for j in JL[ii] if j["pt"] > 25 and abs(j["eta"]) < 4.7 and dR(j["eta"], j["phi"], lep["eta"], lep["phi"]) > 0.4 and all(dR(j["eta"], j["phi"], x[1], x[2]) > 0.4 for x in G)], key=lambda j: -j["pt"])
                if len(J) >= 2 and J[0]["pt"] > 30 and J[1]["pt"] > 30 and not any(j["pt"] > 30 and abs(j["eta"]) < 2.5 and j["b"] > 0 for j in J):
                    wh_pre = True
                    mgg = mass([G[0][0], G[1][0]], [G[0][1], G[1][1]], [G[0][2], G[1][2]], [0, 0]); mjj = mass([J[0]["pt"], J[1]["pt"]], [J[0]["eta"], J[1]["eta"]], [J[0]["phi"], J[1]["phi"]], [J[0]["m"], J[1]["m"]])
                    ptgg = np.hypot(G[0][0]*np.cos(G[0][2]) + G[1][0]*np.cos(G[1][2]), G[0][0]*np.sin(G[0][2]) + G[1][0]*np.sin(G[1][2]))
                    wh_sr = (100 < mgg < 180 and mjj > 600 and abs(J[0]["eta"] - J[1]["eta"]) > 4.0 and ptgg > 75 and abs(mgg - 125) < 3.5)
        if zh_pre: add("zh_pre", w)
        if zh_sr: add("zh_sr", w)
        if wh_pre: add("wh_pre", w)
        if wh_sr: add("wh_sr", w)
        if zh_pre and wh_pre: add("both_pre", w)
        if zh_sr and wh_sr: add("both_sr", w)
        if zh_pre and nl10[i] == 1: add("zh_pre_nl10eq1", w)
        if zh_sr and nl10[i] == 1: add("zh_sr_nl10eq1", w)
json.dump(dict(label=label, n_files=len(files), n_events=N, counts={k: dict(raw=v[0], sumw_pb=v[1], sumw2=v[2]) for k, v in C.items()}, zh_sr_nowindow_mgg_w=NOWIN), open(out, "w"))
print(label, N, {k: v[0] for k, v in C.items()})
