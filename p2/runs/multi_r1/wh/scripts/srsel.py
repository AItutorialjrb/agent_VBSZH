"""Reco SR-baseline proxy used by twin tests (review 7c): exactly 1 e/mu (pT>25,|eta|<2.5; no 2nd lepton pT>10), MET>30, 0 b-tags (jets pT>30,|eta|<2.5),
photons pT>25,|eta|<2.5 (ng=2: two leading with 100<m_gg<170; ng=1: >=1 photon, 2nd photon = fake modelled by weights), >=2 jets pT>30,|eta|<4.7 (dR>0.4 to selected photons/lepton),
leading-two-jet m_jj>500 and |deta|>2.5. Phase 05 will replace this by the final baseline; the twin ratio is re-derived there."""
import math, numpy as np, uproot, awkward as ak
def vec(pt, eta, phi, m): return np.array([pt*math.cos(phi), pt*math.sin(phi), pt*math.sinh(eta), math.sqrt((pt*math.cosh(eta))**2+m*m)])
def minv(a, b): s = a+b; return math.sqrt(max(s[3]**2-s[0]**2-s[1]**2-s[2]**2, 0))
def dr(e1, p1, e2, p2): return math.hypot(e1-e2, (p1-p2+math.pi) % (2*math.pi)-math.pi)
def select(slim, ng):
    t = uproot.open(slim)["Delphes"]; A = lambda k: t[k].array(library="ak")
    met = ak.fill_none(ak.firsts(A("MissingET/MissingET.MET")), 0)
    ept, eeta, ephi = A("Electron/Electron.PT"), A("Electron/Electron.Eta"), A("Electron/Electron.Phi")
    mpt, meta, mphi = A("Muon/Muon.PT"), A("Muon/Muon.Eta"), A("Muon/Muon.Phi")
    gpt, geta, gphi = A("Photon/Photon.PT"), A("Photon/Photon.Eta"), A("Photon/Photon.Phi")
    nl = ak.sum((ept > 10) & (abs(eeta) < 2.5), axis=1) + ak.sum((mpt > 10) & (abs(meta) < 2.5), axis=1)
    ngam = ak.sum((gpt > 25) & (abs(geta) < 2.5), axis=1)
    jpt = A("Jet/Jet.PT"); pre = np.asarray((met > 30) & (nl == 1) & (ngam >= ng) & (ak.num(jpt) >= 2))
    jeta, jphi, jm, jb = A("Jet/Jet.Eta"), A("Jet/Jet.Phi"), A("Jet/Jet.Mass"), A("Jet/Jet.BTag")
    sel = np.zeros(len(pre), bool)
    for i in np.nonzero(pre)[0]:
        L = [(ept[i][k], eeta[i][k], ephi[i][k]) for k in range(len(ept[i])) if ept[i][k] > 10 and abs(eeta[i][k]) < 2.5] + [(mpt[i][k], meta[i][k], mphi[i][k]) for k in range(len(mpt[i])) if mpt[i][k] > 10 and abs(meta[i][k]) < 2.5]
        if L[0][0] < 25: continue
        G = sorted([(gpt[i][k], geta[i][k], gphi[i][k]) for k in range(len(gpt[i])) if gpt[i][k] > 25 and abs(geta[i][k]) < 2.5], reverse=True)
        if ng == 2 and not (100 < minv(vec(G[0][0], G[0][1], G[0][2], 0), vec(G[1][0], G[1][1], G[1][2], 0)) < 170): continue
        if any(jpt[i][k] > 30 and abs(jeta[i][k]) < 2.5 and jb[i][k] > 0 for k in range(len(jpt[i]))): continue
        J = [k for k in range(len(jpt[i])) if jpt[i][k] > 30 and abs(jeta[i][k]) < 4.7 and all(dr(jeta[i][k], jphi[i][k], g[1], g[2]) > 0.4 for g in G[:ng]) and dr(jeta[i][k], jphi[i][k], L[0][1], L[0][2]) > 0.4]
        if len(J) < 2: continue
        a, b = J[0], J[1]
        sel[i] = minv(vec(jpt[i][a], jeta[i][a], jphi[i][a], jm[i][a]), vec(jpt[i][b], jeta[i][b], jphi[i][b], jm[i][b])) > 500 and abs(jeta[i][a]-jeta[i][b]) > 2.5
    return sel
