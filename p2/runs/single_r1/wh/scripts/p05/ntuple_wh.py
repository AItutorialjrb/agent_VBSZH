#!/usr/bin/env python3
"""single_r1 WH Phase 05 ntupler: slim Delphes + GenTruth (RNTuple) -> per-file .npz of analysis rows.
No normalisation, no fake/non-prompt RATE is applied here (rates are scenario choices made in the analysis);
pseudo-event rows carry the kinematics of the object that is promoted, so any rate can be applied later.

Usage: python3 -P ntuple_wh.py <out.npz> <modes: comma list of D,F1,F2,FL,EG> <seed> <file1.root> [file2.root ...]
       (GenTruth friend = <file>_gen.root, same entry order; sha256 of both files is computed and stored)

Objects (reco, Delphes UniqueObjectFinder output = isolated objects):
  leptons e: pT>10 |eta|<2.5; mu: pT>10 |eta|<2.4; pid = -11*q / -13*q; prompt = gen prompt lepton, same flavour, dR<0.1
  photons pT>15, |eta|<2.5, not 1.4442<|eta|<1.566, dR(photon, any selected lepton)>0.4;
          prompt = gen prompt photon dR<0.1; lmatch = 1 (2) if a gen prompt e (mu) is within dR<0.2 (e->gamma / brem object)
  jets    pT>20, |eta|<4.7, dR>0.4 to selected leptons and photons; btag = BTag&1; gpt = pT of the nearest GenJet (dR<0.3) else reco pT
Row tables (all rows: l1pt>20, >=2 photons pT>20, >=2 jets pT>25, 95<m_gg<180; pseudo-event rows additionally
  100<m_gg<170, pT1/m_gg>0.30, pT2/m_gg>0.22, m_jj>300 (looser than every selection used); variables from derive()):
  D  : direct Delphes events.
  F1 : 1 jet -> photon, real photons = prompt-matched reco photons only (other reco photons dropped); photon pT = x*gpt,
       x ~ N(0.85,0.10) truncated [0.5,1]; candidate jets |eta|<2.5 outside the crack; fake photon among the leading two.
  F2 : 2 jets -> photons in events with n_prompt_photons == 0 (all reco photons dropped); both selected photons fake.
  FL : 1 jet -> lepton in events with no reco lepton (pT>10); lepton pT = x*gpt, |eta|<2.4, flavour e/mu 50/50.
  EG : 1 reco prompt electron -> photon (same pT, eta, phi) in events with >=2 reco leptons; e-photon among the leading two.
Histograms: closure of the per-jet j->gamma and j->lepton methods against Delphes direct non-prompt objects (unit per-jet
weight, binned so any per-jet rate can be applied offline); gen-matched object efficiencies (e, mu, gamma) for D-WH-4.
"""
import sys, hashlib, numpy as np, awkward as ak, uproot

OUT, MODES, SEED, FILES = sys.argv[1], set(sys.argv[2].split(",")), int(sys.argv[3]), sys.argv[4:]
rng = np.random.default_rng(SEED)
NL, NG, NJ = 3, 4, 8
CRACK = (1.4442, 1.566)
# histogram binning (closure + efficiencies)
JPT = np.array([25, 35, 50, 75, 100, 150, 1e5]); GPT = np.array([20, 25, 30, 40, 60, 100, 1e5]); MJJB = np.array([0, 200, 500, 1000, 1e6])
EFFB = {"e": (np.array([0, 1.5, 2.5]), np.array([10, 20, 30, 50, 1e9])), "m": (np.array([0, 1.5, 2.4]), np.array([10, 20, 30, 50, 1e9])),
        "g": (np.array([0, 1.4442, 2.5]), np.array([20, 30, 40, 60, 1e9]))}

def sha256(f):
    h = hashlib.sha256()
    with open(f, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 22), b""): h.update(b)
    return h.hexdigest()
def dphi(a, b): return (a - b + np.pi) % (2*np.pi) - np.pi
def dR(e1, p1, e2, p2): return np.sqrt((e1 - e2)**2 + dphi(p1, p2)**2)
def crack(eta): return (abs(eta) > CRACK[0]) & (abs(eta) < CRACK[1])
def pad(x, n): return ak.to_numpy(ak.fill_none(ak.pad_none(x, n, clip=True), np.nan)).astype(np.float64)
def mindr(a_eta, a_phi, b_eta, b_phi):
    """jagged: for each object in a, min dR to objects in b (same event); +inf if b empty"""
    c = ak.cartesian({"a": ak.zip({"e": a_eta, "p": a_phi}), "b": ak.zip({"e": b_eta, "p": b_phi})}, nested=True)
    d = np.sqrt((c.a.e - c.b.e)**2 + ((c.a.p - c.b.p + np.pi) % (2*np.pi) - np.pi)**2)
    return ak.fill_none(ak.min(d, axis=2), np.inf)
def sortpt(X):
    i = np.argsort(-np.nan_to_num(X[:, :, 0], nan=-1.0), axis=1, kind="stable")
    return np.take_along_axis(X, i[:, :, None], 1)
def p4(pt, eta, phi, m=0.0):
    return np.stack([pt*np.cos(phi), pt*np.sin(phi), pt*np.sinh(eta), np.sqrt((pt*np.cosh(eta))**2 + m**2)], -1)
def minv(P):
    return np.sqrt(np.maximum(P[..., 3]**2 - P[..., 0]**2 - P[..., 1]**2 - P[..., 2]**2, 0))
def xdraw(shape): return np.clip(rng.normal(0.85, 0.10, shape), 0.5, 1.0)

def derive(L, G, J, met, mphi):
    """L (n,k,[pt,eta,phi,pid,prompt]); G (n,k,[pt,eta,phi,prompt,lmatch,fake]); J (n,k,[pt,eta,phi,m,btag,gpt])"""
    L, G, J = sortpt(L), sortpt(G), sortpt(J)
    o = {}
    o["nl10"] = (L[:, :, 0] > 10).sum(1).astype(np.int8)
    for i, nm in enumerate(("pt", "eta", "phi", "pid", "prompt")): o[f"l1{nm}"] = L[:, 0, i]
    o["l2pt"] = L[:, 1, 0]
    o["ng20"] = (G[:, :, 0] > 20).sum(1).astype(np.int8)
    for k in (0, 1):
        for i, nm in enumerate(("pt", "eta", "phi", "prompt", "lm", "fake")): o[f"g{k+1}{nm}"] = G[:, k, i]
    P1, P2 = p4(G[:, 0, 0], G[:, 0, 1], G[:, 0, 2]), p4(G[:, 1, 0], G[:, 1, 1], G[:, 1, 2]); Pgg = P1 + P2
    o["mgg"] = minv(Pgg); o["ptgg"] = np.hypot(Pgg[:, 0], Pgg[:, 1])
    with np.errstate(all="ignore"): ygg = 0.5*np.log((Pgg[:, 3] + Pgg[:, 2])/(Pgg[:, 3] - Pgg[:, 2]))
    o["ygg"] = ygg
    o["nj25"] = (J[:, :, 0] > 25).sum(1).astype(np.int8); o["nj30"] = (J[:, :, 0] > 30).sum(1).astype(np.int8)
    for k in (0, 1):
        for i, nm in enumerate(("pt", "eta", "phi")): o[f"j{k+1}{nm}"] = J[:, k, i]
    o["j3pt"] = J[:, 2, 0]; o["j3eta"] = J[:, 2, 1]
    Pj1, Pj2 = p4(J[:, 0, 0], J[:, 0, 1], J[:, 0, 2], np.nan_to_num(J[:, 0, 3])), p4(J[:, 1, 0], J[:, 1, 1], J[:, 1, 2], np.nan_to_num(J[:, 1, 3]))
    o["mjj"] = minv(Pj1 + Pj2); o["detajj"] = np.abs(J[:, 0, 1] - J[:, 1, 1]); o["dphijj"] = np.abs(dphi(J[:, 0, 2], J[:, 1, 2]))
    o["nb"] = ((J[:, :, 4] > 0.5) & (np.abs(J[:, :, 1]) < 2.5) & (J[:, :, 0] > 25)).sum(1).astype(np.int8)
    o["ht"] = np.nansum(np.where(J[:, :, 0] > 25, J[:, :, 0], 0.0), 1)
    o["met"] = met; o["metphi"] = mphi
    o["mtw"] = np.sqrt(np.maximum(2*L[:, 0, 0]*met*(1 - np.cos(dphi(L[:, 0, 2], mphi))), 0))
    etab = 0.5*(J[:, 0, 1] + J[:, 1, 1]); de = np.maximum(o["detajj"], 1e-3)
    o["zgg"] = np.abs(ygg - etab)/de; o["zl"] = np.abs(L[:, 0, 1] - etab)/de
    o["drgg"] = dR(G[:, 0, 1], G[:, 0, 2], G[:, 1, 1], G[:, 1, 2])
    o["drlg"] = np.fmin(dR(L[:, 0, 1], L[:, 0, 2], G[:, 0, 1], G[:, 0, 2]), dR(L[:, 0, 1], L[:, 0, 2], G[:, 1, 1], G[:, 1, 2]))
    Pl = p4(L[:, 0, 0], L[:, 0, 1], L[:, 0, 2])
    o["mlg1"] = minv(Pl + P1); o["mlg2"] = minv(Pl + P2)
    o["drgj"] = np.fmin.reduce([dR(G[:, a, 1], G[:, a, 2], J[:, b, 1], J[:, b, 2]) for a in (0, 1) for b in (0, 1)])
    Pmet = np.stack([met*np.cos(mphi), met*np.sin(mphi)], -1)
    vs = Pj1[:, :2] + Pj2[:, :2] + Pgg[:, :2] + Pl[:, :2] + Pmet
    ss = J[:, 0, 0] + J[:, 1, 0] + G[:, 0, 0] + G[:, 1, 0] + L[:, 0, 0] + met
    o["ptbal"] = np.hypot(vs[:, 0], vs[:, 1])/ss
    return o

def keep(o, extra=None, strict=False):
    """D rows: loose skim; pseudo-event rows (strict=True): additionally 100<m_gg<170, pT/m_gg > 0.30/0.22, m_jj > 300"""
    with np.errstate(invalid="ignore"):
        m = (o["l1pt"] > 20) & (o["ng20"] >= 2) & (o["nj25"] >= 2) & (o["mgg"] > 95) & (o["mgg"] < 180)
        if strict: m &= (o["mgg"] > 100) & (o["mgg"] < 170) & (o["g1pt"] > 0.30*o["mgg"]) & (o["g2pt"] > 0.22*o["mgg"]) & (o["mjj"] > 300)
    return m if extra is None else m & extra

TAB = {}
def push(tab, o, m, **kw):
    for k, v in o.items():
        TAB.setdefault(f"{tab}_{k}", []).append(np.asarray(v)[m].astype(np.float32 if np.asarray(v).dtype.kind == "f" else np.int16))
    for k, v in kw.items():
        v = np.asarray(v)[m]; TAB.setdefault(f"{tab}_{k}", []).append(v.astype(np.float32) if v.dtype.kind == "f" else v.astype(np.int64))

H = {"cg_dir": np.zeros((6, 2, 4, 3)), "cg_dir_raw": np.zeros((6, 2, 4, 3)), "cg_pred": np.zeros((6, 2, 4, 6)), "cg_pred_raw": np.zeros((6, 2, 4, 6)),
     "cl_dir": np.zeros((6, 4)), "cl_dir_raw": np.zeros((6, 4)), "cl_pred": np.zeros((6, 4, 6)), "cl_pred_raw": np.zeros((6, 4, 6)),
     **{f"eff_{t}_{k}": np.zeros((2, 4)) for t in "emg" for k in ("num", "den")}}
def b(edges, x): return np.clip(np.searchsorted(edges, x, side="right") - 1, 0, len(edges) - 2)

META = dict(files=[], sha=[], sha_gen=[], nev=[], sumw=[], nneg=[], nlhew=[])
evoff = 0
for f in FILES:
    fg = f[:-5] + "_gen.root"
    META["files"].append(f); META["sha"].append(sha256(f)); META["sha_gen"].append(sha256(fg))
    t = uproot.open(f)["Delphes"]
    br = lambda c, k: t[f"{c}/{c}.{k}"].array()
    N = t.num_entries
    w = ak.to_numpy(br("Event", "Weight")[:, 0]).astype(np.float64)
    META["nev"].append(N); META["sumw"].append(float(w.sum())); META["nneg"].append(int((w < 0).sum()))
    gt = uproot.open(fg)["GenTruth"]; assert gt.num_entries == N, f
    GT = {k: gt[k].array() for k in ("n_prompt_photons", "gph_pt", "gph_eta", "gph_phi", "gph_prompt", "glep_pt", "glep_eta", "glep_phi", "glep_pid", "glep_prompt")}
    npr = ak.to_numpy(GT["n_prompt_photons"]).astype(np.int16)
    gpp = (GT["gph_prompt"] > 0); gp_eta, gp_phi, gp_pt = GT["gph_eta"][gpp], GT["gph_phi"][gpp], GT["gph_pt"][gpp]
    glp = (GT["glep_prompt"] > 0) & (GT["glep_pt"] > 5)
    gl_eta, gl_phi, gl_pt, gl_pid = GT["glep_eta"][glp], GT["glep_phi"][glp], GT["glep_pt"][glp], abs(GT["glep_pid"][glp])
    # ---- reco leptons
    e = ak.zip({"pt": br("Electron", "PT"), "eta": br("Electron", "Eta"), "phi": br("Electron", "Phi"), "q": br("Electron", "Charge")})
    mu = ak.zip({"pt": br("Muon", "PT"), "eta": br("Muon", "Eta"), "phi": br("Muon", "Phi"), "q": br("Muon", "Charge")})
    e = e[(e.pt > 10) & (abs(e.eta) < 2.5)]; mu = mu[(mu.pt > 10) & (abs(mu.eta) < 2.4)]
    e = ak.with_field(e, -11*e.q, "pid"); mu = ak.with_field(mu, -13*mu.q, "pid")
    lep = ak.concatenate([e, mu], axis=1); lep = lep[ak.argsort(lep.pt, axis=1, ascending=False)]
    ge, gm = gl_pid == 11, gl_pid == 13
    pe = mindr(lep.eta, lep.phi, gl_eta[ge], gl_phi[ge]) < 0.1; pm = mindr(lep.eta, lep.phi, gl_eta[gm], gl_phi[gm]) < 0.1
    lep = ak.with_field(lep, ak.where(abs(lep.pid) == 11, pe, pm), "prompt")
    # ---- photons
    ph = ak.zip({"pt": br("Photon", "PT"), "eta": br("Photon", "Eta"), "phi": br("Photon", "Phi")})
    ph = ph[(ph.pt > 15) & (abs(ph.eta) < 2.5) & ~crack(ph.eta)]
    ph = ph[mindr(ph.eta, ph.phi, lep.eta, lep.phi) > 0.4]
    php = mindr(ph.eta, ph.phi, gp_eta, gp_phi) < 0.1
    lme = mindr(ph.eta, ph.phi, gl_eta[ge], gl_phi[ge]) < 0.2; lmm = mindr(ph.eta, ph.phi, gl_eta[gm], gl_phi[gm]) < 0.2
    ph = ak.with_field(ak.with_field(ph, php, "prompt"), ak.where(lme, 1, ak.where(lmm, 2, 0)), "lm")
    # ---- jets
    jt = ak.zip({"pt": br("Jet", "PT"), "eta": br("Jet", "Eta"), "phi": br("Jet", "Phi"), "m": br("Jet", "Mass"), "b": br("Jet", "BTag") & 1})
    jt = jt[(jt.pt > 20) & (abs(jt.eta) < 4.7)]
    jt = jt[(mindr(jt.eta, jt.phi, lep.eta, lep.phi) > 0.4) & (mindr(jt.eta, jt.phi, ph.eta, ph.phi) > 0.4)]
    gj = ak.zip({"pt": br("GenJet", "PT"), "eta": br("GenJet", "Eta"), "phi": br("GenJet", "Phi")})
    c = ak.cartesian({"a": jt, "b": gj}, nested=True)
    dd = np.sqrt((c.a.eta - c.b.eta)**2 + ((c.a.phi - c.b.phi + np.pi) % (2*np.pi) - np.pi)**2)
    im = ak.argmin(dd, axis=2, keepdims=True); dmin = ak.fill_none(ak.firsts(dd[im], axis=2), np.inf)
    gpt_m = ak.fill_none(ak.firsts(c.b.pt[im], axis=2), np.nan)
    jt = ak.with_field(jt, ak.where(dmin < 0.3, gpt_m, jt.pt), "gpt")
    met = ak.to_numpy(br("MissingET", "MET")[:, 0]).astype(np.float64); mphi = ak.to_numpy(br("MissingET", "Phi")[:, 0]).astype(np.float64)
    # ---- padded numpy objects
    L = np.stack([pad(lep[k], NL) for k in ("pt", "eta", "phi", "pid", "prompt")], -1)
    G = np.stack([pad(ph[k], NG) for k in ("pt", "eta", "phi", "prompt", "lm")] + [np.zeros((N, NG))], -1); G[np.isnan(G[:, :, 0])] = np.nan
    J = np.stack([pad(jt[k], NJ) for k in ("pt", "eta", "phi", "m", "b", "gpt")], -1)
    evt = np.arange(N) + evoff
    # ---- efficiencies (gen-matched), D-WH-4
    for tkey, sel, reco in (("e", ge, e), ("m", gm, mu)):
        eta_, pt_ = gl_eta[sel], gl_pt[sel]
        mt = mindr(eta_, gl_phi[sel], reco.eta, reco.phi) < 0.1
        ee, pe_ = ak.to_numpy(ak.flatten(abs(eta_))), ak.to_numpy(ak.flatten(pt_)); mm = ak.to_numpy(ak.flatten(mt))
        ok = (ee < EFFB[tkey][0][-1]) & (pe_ > 10)
        for k, msk in (("den", ok), ("num", ok & mm)):
            H[f"eff_{tkey}_{k}"] += np.histogram2d(ee[msk], pe_[msk], bins=EFFB[tkey])[0]
    gjs = gj[gj.pt > 20]
    c2 = ak.cartesian({"a": ak.zip({"e": gp_eta, "p": gp_phi}), "b": ak.zip({"e": gjs.eta, "p": gjs.phi})}, nested=True)
    d2 = np.sqrt((c2.a.e - c2.b.e)**2 + ((c2.a.p - c2.b.p + np.pi) % (2*np.pi) - np.pi)**2)
    niso = ak.sum((d2 > 0.15) & (d2 < 0.4), axis=2)
    iso = (niso == 0) & (mindr(gp_eta, gp_phi, gl_eta, gl_phi) > 0.4) & (gp_pt > 20) & (abs(gp_eta) < 2.5) & ~crack(gp_eta)
    phall = ak.zip({"eta": br("Photon", "Eta"), "phi": br("Photon", "Phi")})
    mt = mindr(gp_eta[iso], gp_phi[iso], phall.eta, phall.phi) < 0.1
    ee, pe_, mm = ak.to_numpy(ak.flatten(abs(gp_eta[iso]))), ak.to_numpy(ak.flatten(gp_pt[iso])), ak.to_numpy(ak.flatten(mt))
    H["eff_g_den"] += np.histogram2d(ee, pe_, bins=EFFB["g"])[0]; H["eff_g_num"] += np.histogram2d(ee[mm], pe_[mm], bins=EFFB["g"])[0]
    # ---- D
    if "D" in MODES:
        o = derive(L, G, J, met, mphi); m = keep(o)
        kw = dict(w=w, evt=evt, npr=npr)
        lw = t["WeightLHEF/WeightLHEF.Weight"].array() if "WeightLHEF" in t.keys() else None
        nW = int(ak.max(ak.num(lw))) if lw is not None and N else 0; META["nlhew"].append(nW)
        if nW in (145, 147) and m.any():
            lw = ak.to_numpy(lw[m]).astype(np.float64); nom = lw[:, 22]; pdf0 = 44 if nW == 145 else 46   # 0-based index of PDF member 0
            with np.errstate(all="ignore"):
                sc = lw[:, [0, 5, 15, 24, 34, 39]]/nom[:, None]; pdf = lw[:, pdf0 + 1:pdf0 + 101]/nom[:, None]
            TAB.setdefault("D_scale", []).append(np.nan_to_num(sc, nan=1.0).astype(np.float32))
            TAB.setdefault("D_pdf", []).append(np.nan_to_num(pdf, nan=1.0).astype(np.float16))
            TAB.setdefault("D_wlhe", []).append((nom/w[m]).astype(np.float32))
        push("D", o, m, **kw)
    # ---- F1: one jet -> photon (real photons = prompt-matched reco photons)
    jcand = (J[:, :, 0] > 20) & (np.abs(J[:, :, 1]) < 2.5) & ~crack(J[:, :, 1])
    X = xdraw((N, NJ)); fpt = X*J[:, :, 5]
    if "F1" in MODES:
        Gr = G.copy(); Gr[Gr[:, :, 3] < 0.5] = np.nan
        ev0 = (L[:, 0, 0] > 20) & ((Gr[:, :, 0] > 20).sum(1) >= 1) & ((J[:, :, 0] > 20).sum(1) >= 3)
        ie, ik = np.nonzero(ev0[:, None] & jcand & (fpt > 20))
        if len(ie):
            Gp = np.concatenate([Gr[ie], np.full((len(ie), 1, 6), np.nan)], 1)
            Gp[:, -1, :] = np.stack([fpt[ie, ik], J[ie, ik, 1], J[ie, ik, 2], np.zeros(len(ie)), np.zeros(len(ie)), np.ones(len(ie))], -1)
            Jp = J[ie].copy(); Jp[np.arange(len(ie)), ik] = np.nan
            o = derive(L[ie], Gp, Jp, met[ie], mphi[ie]); m = keep(o, (o["g1fake"] == 1) | (o["g2fake"] == 1), strict=True)
            push("F1", o, m, w=w[ie], evt=evt[ie], npr=npr[ie], fk1pt=J[ie, ik, 5], fk1eta=J[ie, ik, 1])
    # ---- F2: two jets -> photons, events with n_prompt_photons == 0
    if "F2" in MODES:
        ev0 = (L[:, 0, 0] > 20) & (npr == 0) & ((J[:, :, 0] > 20).sum(1) >= 4)
        ok = ev0[:, None] & jcand & (fpt > 20)
        for a in range(NJ):
            for bb in range(a + 1, NJ):
                ie = np.nonzero(ok[:, a] & ok[:, bb])[0]
                if not len(ie): continue
                Pa = p4(fpt[ie, a], J[ie, a, 1], J[ie, a, 2]); Pb = p4(fpt[ie, bb], J[ie, bb, 1], J[ie, bb, 2]); mm_ = minv(Pa + Pb)
                ie = ie[(mm_ > 95) & (mm_ < 180)]
                if not len(ie): continue
                n = len(ie); Gp = np.full((n, 2, 6), np.nan)
                Gp[:, 0] = np.stack([fpt[ie, a], J[ie, a, 1], J[ie, a, 2], np.zeros(n), np.zeros(n), np.ones(n)], -1)
                Gp[:, 1] = np.stack([fpt[ie, bb], J[ie, bb, 1], J[ie, bb, 2], np.zeros(n), np.zeros(n), np.ones(n)], -1)
                Jp = J[ie].copy(); Jp[:, a] = np.nan; Jp[:, bb] = np.nan
                o = derive(L[ie], Gp, Jp, met[ie], mphi[ie]); m = keep(o, strict=True)
                push("F2", o, m, w=w[ie], evt=evt[ie], npr=npr[ie], fk1pt=J[ie, a, 5], fk1eta=J[ie, a, 1], fk2pt=J[ie, bb, 5], fk2eta=J[ie, bb, 1])
    # ---- FL: one jet -> lepton, events without a reco lepton
    if "FL" in MODES:
        ev0 = ((L[:, :, 0] > 10).sum(1) == 0) & ((G[:, :, 0] > 20).sum(1) >= 2) & ((J[:, :, 0] > 20).sum(1) >= 3)
        lpt = X*J[:, :, 5]
        ie, ik = np.nonzero(ev0[:, None] & (J[:, :, 0] > 20) & (np.abs(J[:, :, 1]) < 2.4) & (lpt > 20))
        if len(ie):
            n = len(ie); pid = np.where(rng.random(n) < 0.5, 11, 13)*np.where(rng.random(n) < 0.5, 1, -1)
            Lp = np.full((n, 2, 5), np.nan); Lp[:, 0] = np.stack([lpt[ie, ik], J[ie, ik, 1], J[ie, ik, 2], pid, np.zeros(n)], -1)
            Jp = J[ie].copy(); Jp[np.arange(n), ik] = np.nan
            # photons are kept; the promoted jet was already >0.4 from every photon (jet cleaning)
            o = derive(Lp, G[ie], Jp, met[ie], mphi[ie]); m = keep(o, strict=True)
            push("FL", o, m, w=w[ie], evt=evt[ie], npr=npr[ie], fljpt=J[ie, ik, 5], fljeta=J[ie, ik, 1])
    # ---- EG: one reco prompt electron -> photon
    if "EG" in MODES:
        ev0 = ((L[:, :, 0] > 10).sum(1) >= 2) & ((G[:, :, 0] > 20).sum(1) >= 1)
        ie, ik = np.nonzero(ev0[:, None] & (np.abs(L[:, :, 3]) == 11) & (L[:, :, 4] > 0.5) & (L[:, :, 0] > 20))
        if len(ie):
            n = len(ie); Lp = L[ie].copy(); Lp[np.arange(n), ik] = np.nan
            Gp = np.concatenate([G[ie], np.full((n, 1, 6), np.nan)], 1)
            Gp[:, -1] = np.stack([L[ie, ik, 0], L[ie, ik, 1], L[ie, ik, 2], np.zeros(n), np.ones(n), np.full(n, 2.0)], -1)
            ok_eta = ~crack(L[ie, ik, 1])
            o = derive(Lp, Gp, J[ie], met[ie], mphi[ie]); m = keep(o, ((o["g1fake"] == 2) | (o["g2fake"] == 2)) & ok_eta, strict=True)
            push("EG", o, m, w=w[ie], evt=evt[ie], npr=npr[ie], egpt=L[ie, ik, 0], egeta=L[ie, ik, 1])
    # ---- closure histograms (j -> gamma) at the one-fake level: npr == 0 (F2-type) or npr == 1 (F1-type)
    if "F1" in MODES or "F2" in MODES:
        nreq = 0 if "F2" in MODES else 1
        ev0 = (L[:, 0, 0] > 25) & (npr == nreq)
        # direct: every non-prompt, non-lepton reco photon with pT>20 (+ its dR to the nearest GenJet pT>15)
        gj15 = gj[gj.pt > 15]
        drg = pad(mindr(ph.eta, ph.phi, gj15.eta, gj15.phi), NG)
        Jm = J.copy();
        P1, P2 = p4(Jm[:, 0, 0], Jm[:, 0, 1], Jm[:, 0, 2], np.nan_to_num(Jm[:, 0, 3])), p4(Jm[:, 1, 0], Jm[:, 1, 1], Jm[:, 1, 2], np.nan_to_num(Jm[:, 1, 3]))
        mjj = np.nan_to_num(minv(P1 + P2), nan=0.0)*((Jm[:, 1, 0] > 25))
        for k in range(NG):
            s = ev0 & (G[:, k, 0] > 20) & (G[:, k, 3] < 0.5) & (G[:, k, 4] == 0)
            if not s.any(): continue
            ip, ie_, im_, idr = b(GPT, G[s, k, 0]), (np.abs(G[s, k, 1]) > 1.5).astype(int), b(MJJB, mjj[s]), np.digitize(drg[s, k], [0.2, 0.4])
            np.add.at(H["cg_dir"], (ip, ie_, im_, idr), w[s]); np.add.at(H["cg_dir_raw"], (ip, ie_, im_, idr), 1)
        # predicted (unit per-jet weight): each candidate jet k; mjj of the two leading OTHER jets
        for k in range(NJ):
            s = ev0 & jcand[:, k] & (fpt[:, k] > 20) & (J[:, k, 0] > 20)
            if not s.any(): continue
            Jo = J[s].copy(); Jo[:, k] = np.nan; Jo = sortpt(Jo)
            Pa, Pb = p4(Jo[:, 0, 0], Jo[:, 0, 1], Jo[:, 0, 2], np.nan_to_num(Jo[:, 0, 3])), p4(Jo[:, 1, 0], Jo[:, 1, 1], Jo[:, 1, 2], np.nan_to_num(Jo[:, 1, 3]))
            mo = np.nan_to_num(minv(Pa + Pb), nan=0.0)*(Jo[:, 1, 0] > 25)
            ij, ie_, im_, ip = b(JPT, J[s, k, 5]), (np.abs(J[s, k, 1]) > 1.5).astype(int), b(MJJB, mo), b(GPT, fpt[s, k])
            np.add.at(H["cg_pred"], (ip, ie_, im_, ij), w[s]); np.add.at(H["cg_pred_raw"], (ip, ie_, im_, ij), 1)
    # ---- closure histograms (j -> lepton): events with >= 2 reco photons pT>20
    if "FL" in MODES:
        ev0 = (G[:, :, 0] > 20).sum(1) >= 2
        P1, P2 = p4(J[:, 0, 0], J[:, 0, 1], J[:, 0, 2], np.nan_to_num(J[:, 0, 3])), p4(J[:, 1, 0], J[:, 1, 1], J[:, 1, 2], np.nan_to_num(J[:, 1, 3]))
        mjj = np.nan_to_num(minv(P1 + P2), nan=0.0)*(J[:, 1, 0] > 25)
        for k in range(NL):
            s = ev0 & (L[:, k, 0] > 20) & (L[:, k, 4] < 0.5)
            if s.any():
                np.add.at(H["cl_dir"], (b(GPT, L[s, k, 0]), b(MJJB, mjj[s])), w[s]); np.add.at(H["cl_dir_raw"], (b(GPT, L[s, k, 0]), b(MJJB, mjj[s])), 1)
        lpt = X*J[:, :, 5]
        for k in range(NJ):
            s = ev0 & (J[:, k, 0] > 20) & (np.abs(J[:, k, 1]) < 2.4) & (lpt[:, k] > 20)
            if not s.any(): continue
            Jo = J[s].copy(); Jo[:, k] = np.nan; Jo = sortpt(Jo)
            Pa, Pb = p4(Jo[:, 0, 0], Jo[:, 0, 1], Jo[:, 0, 2], np.nan_to_num(Jo[:, 0, 3])), p4(Jo[:, 1, 0], Jo[:, 1, 1], Jo[:, 1, 2], np.nan_to_num(Jo[:, 1, 3]))
            mo = np.nan_to_num(minv(Pa + Pb), nan=0.0)*(Jo[:, 1, 0] > 25)
            idx = (b(GPT, lpt[s, k]), b(MJJB, mo), b(JPT, J[s, k, 5]))
            np.add.at(H["cl_pred"], idx, w[s]); np.add.at(H["cl_pred_raw"], idx, 1)
    evoff += 10**7

out = {k: np.concatenate(v) for k, v in TAB.items()}
out.update({f"H_{k}": v for k, v in H.items()})
for k in ("nev", "sumw", "nneg", "nlhew"): out[f"M_{k}"] = np.asarray(META[k])
out["M_files"] = np.asarray(META["files"]); out["M_sha"] = np.asarray(META["sha"]); out["M_sha_gen"] = np.asarray(META["sha_gen"])
np.savez_compressed(OUT, **out)
print("wrote", OUT, {t: int(len(out.get(f"{t}_w", []))) for t in ("D", "F1", "F2", "FL", "EG")}, "nev", sum(META["nev"]))
