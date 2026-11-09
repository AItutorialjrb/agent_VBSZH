#!/usr/bin/env python3
"""ZH erratum (D37) ntupler.  Read-only on the frozen ZH production.  One pass per list of Delphes files producing
  <out>_rate.npz : lepton-decontaminated per-GenJet j->gamma rate histograms (genuine in-jet photons vs energy-flow artefact class)
  <out>_dir.npz  : frozen direct-mode ntuple (identical object definitions to scripts/analysis/ntuple.py) + per-photon truth class gcls
  <out>_ffm.npz  : fake-factor candidate rows (one per event x fake-candidate GenJet)  [events with n_prompt_photons==1 only]
Usage: python3 -P zh_ntuple.py <out_prefix> <modes: comma list of rate,dir,ffm> <files comma list>
Truth class of a reco photon (GenTruth only; Particle is not in the production slim files):
  1 prompt     : gen photon with prompt flag, pT>10, within dR<0.1
  2 lepton     : (not prompt-matched) a gen status-1 e/mu (pT>5) within dR<0.2          [e->gamma / FSR-like]
  3 genuine    : a non-prompt gen photon (pi0/eta/... decay photon, pT>10) within dR<0.1 with pT_gen > 0.5 pT_reco
  4 artefact   : none of the above (no gen photon pT>10 within dR<0.1 carrying >50 % of the reco pT): energy-flow artefact class
"""
import sys, numpy as np, awkward as ak, uproot
MZ = 91.1876
out, modes, files = sys.argv[1], sys.argv[2].split(","), sys.argv[3].split(",")
def dphi(a, b): return (a - b + np.pi) % (2*np.pi) - np.pi
def dR(e1, p1, e2, p2): return np.hypot(e1 - e2, dphi(p1, p2))
def first_n(x, n, fill=np.nan): return ak.to_numpy(ak.fill_none(ak.pad_none(x, n, clip=True), fill))
def m_of(pt1, eta1, phi1, m1, pt2, eta2, phi2, m2):
    px = pt1*np.cos(phi1) + pt2*np.cos(phi2); py = pt1*np.sin(phi1) + pt2*np.sin(phi2); pz = pt1*np.sinh(eta1) + pt2*np.sinh(eta2)
    e = np.sqrt((pt1*np.cosh(eta1))**2 + m1**2) + np.sqrt((pt2*np.cosh(eta2))**2 + m2**2)
    return np.sqrt(np.maximum(e**2 - px**2 - py**2 - pz**2, 0)), px, py, pz, e
def p4(pt, eta, phi, m=0.0): return np.stack([pt*np.cos(phi), pt*np.sin(phi), pt*np.sinh(eta), np.sqrt((pt*np.cosh(eta))**2 + m**2)], -1)
def kin(P):
    px, py, pz, e = P[..., 0], P[..., 1], P[..., 2], P[..., 3]
    m = np.sqrt(np.maximum(e**2 - px**2 - py**2 - pz**2, 0)); pt = np.hypot(px, py)
    with np.errstate(all="ignore"): y = 0.5*np.log((e + pz)/(e - pz))
    return m, pt, y
def best_pair(pt, eta, phi, q, mass):
    sel = (pt > 15) & (abs(eta) < (2.5 if mass < 0.01 else 2.4))
    L = ak.zip({"pt": pt[sel], "eta": eta[sel], "phi": phi[sel], "q": q[sel]})
    c = ak.combinations(L, 2, fields=["a", "b"])
    mm = m_of(c.a.pt, c.a.eta, c.a.phi, mass, c.b.pt, c.b.eta, c.b.phi, mass)[0]
    mm = ak.where(c.a.q * c.b.q < 0, mm, -1e9)
    i = ak.argmin(abs(mm - MZ), axis=1, keepdims=True)
    b = ak.firsts(c[i]); mb = ak.fill_none(ak.firsts(mm[i]), -1e9)
    ok = mb > 0
    return ok, ak.where(ok, mb, np.nan), b
def mindR(eta, phi, ceta, cphi, mask):
    """per object minimum dR to the (jagged, masked) collection c; large if none. eta/phi: jagged (events x objects)"""
    de = eta[:, :, None] - ceta[:, None, :]; dp = (phi[:, :, None] - cphi[:, None, :] + np.pi) % (2*np.pi) - np.pi
    return ak.fill_none(ak.min(ak.where(mask[:, None, :], np.hypot(de, dp), 99.0), axis=2, mask_identity=True), 99.0)

# jet-pT / eta bins of the rate (same as the WH table: 25-35, 35-50, 50-75, 75-100, 100-150, 150-1000; barrel |eta|<1.5)
PTB = np.array([25, 35, 50, 75, 100, 150, 1000.]); ETB = np.array([0, 1.5, 2.5]); XB = np.linspace(0, 1.5, 16)
R = dict(den=np.zeros((6, 2)), num_gen=np.zeros((6, 2)), num_art=np.zeros((6, 2)), num_lep=np.zeros((6, 2)), num_old=np.zeros((6, 2)),
         xh=np.zeros((6, 15)), xh_art=np.zeros((6, 15)), rec_over_gen_sum=np.zeros(6), rec_over_gen_n=np.zeros(6))
D = {}; F = {}
def push(S, d):
    for k, v in d.items(): S.setdefault(k, []).append(np.asarray(v))
nev_total = 0; NEVT = 0
for f in files:
    t = uproot.open(f)["Delphes"]; g = uproot.open(f[:-5] + "_gen.root")["GenTruth"]
    assert g.num_entries == t.num_entries, f
    rd = lambda c, ks: {k: t[f"{c}/{c}.{k}"].array() for k in ks.split()}
    El, Mu, Ph, Jt, GJ = rd("Electron", "PT Eta Phi Charge"), rd("Muon", "PT Eta Phi Charge"), rd("Photon", "PT Eta Phi"), rd("Jet", "PT Eta Phi Mass BTag"), rd("GenJet", "PT Eta Phi")
    G = {k: g[k].array() for k in ("n_prompt_photons", "gph_pt", "gph_eta", "gph_phi", "gph_prompt", "glep_pt", "glep_eta", "glep_phi", "glep_prompt")}
    npr = ak.to_numpy(G["n_prompt_photons"]); N = len(npr); nev_total += N; evbase = nev_total - N
    gpr = ak.values_astype(G["gph_prompt"], bool); glp = ak.values_astype(G["glep_prompt"], bool)
    # ---------------------------------------------------------------- truth class of reco photons
    def pclass(pt, eta, phi):
        """jagged reco photons -> class code (1..4), same structure"""
        dd = mindR(eta, phi, G["gph_eta"], G["gph_phi"], (G["gph_pt"] > 10) & gpr)
        dl = mindR(eta, phi, G["glep_eta"], G["glep_phi"], G["glep_pt"] > 5)
        de = eta[:, :, None] - G["gph_eta"][:, None, :]; dp = (phi[:, :, None] - G["gph_phi"][:, None, :] + np.pi) % (2*np.pi) - np.pi
        okg = (~gpr)[:, None, :] & (np.hypot(de, dp) < 0.1) & (G["gph_pt"][:, None, :] > 0.5*pt[:, :, None])
        gen = ak.any(okg, axis=2)
        return ak.to_numpy(ak.flatten(ak.where(dd < 0.1, 1, ak.where(dl < 0.2, 2, ak.where(gen, 3, 4))))) if False else ak.where(dd < 0.1, 1, ak.where(dl < 0.2, 2, ak.where(gen, 3, 4)))
    # ---------------------------------------------------------------- rate (GenJet-based)
    if "rate" in modes:
        sel = (GJ["PT"] > 25) & (abs(GJ["Eta"]) < 2.5) & (npr[:, None] <= 1)
        gjpt, gjeta, gjphi = GJ["PT"][sel], GJ["Eta"][sel], GJ["Phi"][sel]
        dl_g = mindR(gjeta, gjphi, G["glep_eta"], G["glep_phi"], glp & (G["glep_pt"] > 10))
        dl_r = ak.where(ak.num(gjpt) >= 0, 99.0, 99.0)
        for C in (El, Mu):
            lm = C["PT"] > 10
            dl_r = ak.where(mindR(gjeta, gjphi, C["Eta"], C["Phi"], lm) < dl_r, mindR(gjeta, gjphi, C["Eta"], C["Phi"], lm), dl_r)
        dphp = mindR(gjeta, gjphi, G["gph_eta"], G["gph_phi"], (G["gph_pt"] > 10) & gpr)
        ok = (dl_g > 0.4) & (dl_r > 0.4) & (dphp > 0.4)
        # reco photons (pT>10, |eta|<2.5) near each jet
        pm = (Ph["PT"] > 10) & (abs(Ph["Eta"]) < 2.5)
        pp, pe, pph = Ph["PT"][pm], Ph["Eta"][pm], Ph["Phi"][pm]
        cl = pclass(pp, pe, pph)
        # lepton-near flags per photon (gen or reco lepton within 0.2)
        near_l = mindR(pe, pph, G["glep_eta"], G["glep_phi"], G["glep_pt"] > 5) < 0.2
        for C in (El, Mu): near_l = near_l | (mindR(pe, pph, C["Eta"], C["Phi"], C["PT"] > 10) < 0.2)
        near_pr = mindR(pe, pph, G["gph_eta"], G["gph_phi"], (G["gph_pt"] > 10) & gpr) < 0.1
        de = pe[:, None, :] - gjeta[:, :, None]; dp = (pph[:, None, :] - gjphi[:, :, None] + np.pi) % (2*np.pi) - np.pi
        inj = np.hypot(de, dp) < 0.2                                  # (events, jets, photons)
        inj_clean = inj & (~near_l)[:, None, :] & (~near_pr)[:, None, :]
        isg = (cl == 3)[:, None, :]; isa = (cl == 4)[:, None, :]
        gen_j = ak.any(inj_clean & isg, axis=2); art_j = ak.any(inj_clean & isa, axis=2) & ~gen_j
        lep_j = ak.any(inj & near_l[:, None, :] & ~near_pr[:, None, :], axis=2) & ~gen_j & ~art_j
        old_j = ak.any(inj & ~near_pr[:, None, :], axis=2)            # un-decontaminated numerator (WH multi_r1 v1 style)
        fl = lambda x: ak.to_numpy(ak.flatten(x[ok]))
        jp, je = fl(gjpt), np.abs(fl(gjeta)); gj, aj, lj, oj = fl(gen_j), fl(art_j), fl(lep_j), fl(old_j)
        ib = np.digitize(jp, PTB) - 1; ie = (je >= 1.5).astype(int); v = ib >= 0; v &= ib < 6
        for key, w in (("den", np.ones(len(jp))), ("num_gen", gj), ("num_art", aj), ("num_lep", lj), ("num_old", oj)):
            np.add.at(R[key], (ib[v], ie[v]), w[v].astype(float))
        # x = pT(photon)/pT(GenJet) of the leading in-jet clean photon (genuine / artefact)
        for cls, key in ((3, "xh"), (4, "xh_art")):
            m_ = inj_clean & (cl == cls)[:, None, :]
            xx = ak.max(ak.where(m_, pp[:, None, :]/gjpt[:, :, None], -1.0), axis=2, mask_identity=True); xx = ak.fill_none(xx, -1.0)
            xf = ak.to_numpy(ak.flatten(xx[ok]))
            mm = v & (xf > 0)
            if mm.any():
                h = np.histogram2d(ib[mm], xf[mm], bins=[np.arange(7) - 0.5, XB])[0]; R[key] += h
    # ---------------------------------------------------------------- frozen object selection
    oke, mee, be = best_pair(El["PT"], El["Eta"], El["Phi"], El["Charge"], 0.000511)
    okm, mmm, bm = best_pair(Mu["PT"], Mu["Eta"], Mu["Phi"], Mu["Charge"], 0.1057)
    oke = ak.to_numpy(oke); okm = ak.to_numpy(okm); mee = ak.to_numpy(mee); mmm = ak.to_numpy(mmm)
    use_e = oke & (~okm | (np.abs(np.nan_to_num(mee, nan=1e9) - MZ) <= np.abs(np.nan_to_num(mmm, nan=1e9) - MZ)))
    has = oke | okm; lep = {}
    for k in ("pt", "eta", "phi"):
        for s in "ab":
            lep[s+k] = np.where(use_e, ak.to_numpy(ak.fill_none(be[s][k], np.nan)), ak.to_numpy(ak.fill_none(bm[s][k], np.nan)))
    mll = np.where(use_e, mee, mmm); mll[~has] = np.nan; flav = np.where(use_e, 11, 13); flav[~has] = 0
    la_e, la_p, lb_e, lb_p = [np.nan_to_num(lep[k], nan=99.) for k in ("aeta", "aphi", "beta", "bphi")]
    gsel = (Ph["PT"] > 20) & (abs(Ph["Eta"]) < 2.5) & ~((abs(Ph["Eta"]) > 1.4442) & (abs(Ph["Eta"]) < 1.566)) \
        & (dR(Ph["Eta"], Ph["Phi"], la_e, la_p) > 0.4) & (dR(Ph["Eta"], Ph["Phi"], lb_e, lb_p) > 0.4)
    gpt, geta, gphi = Ph["PT"][gsel], Ph["Eta"][gsel], Ph["Phi"][gsel]
    ng = ak.to_numpy(ak.num(gpt)); Gp = {k: first_n(v, 2) for k, v in (("pt", gpt), ("eta", geta), ("phi", gphi))}
    jpt, jeta, jphi, jm, jb = Jt["PT"], Jt["Eta"], Jt["Phi"], Jt["Mass"], Jt["BTag"]
    jsel = (jpt > 25) & (abs(jeta) < 4.7) & (dR(jeta, jphi, la_e, la_p) > 0.4) & (dR(jeta, jphi, lb_e, lb_p) > 0.4)
    for k in range(2): jsel = jsel & (dR(jeta, jphi, np.nan_to_num(Gp["eta"][:, k], nan=99.), np.nan_to_num(Gp["phi"][:, k], nan=99.)) > 0.4)
    nb = ak.to_numpy(ak.sum(jsel & (abs(jeta) < 2.5) & ((jb & 1) == 1), axis=1))
    Jj = {k: first_n(v[jsel], 2) for k, v in (("pt", jpt), ("eta", jeta), ("phi", jphi), ("m", jm))}
    nj = ak.to_numpy(ak.num(jpt[jsel]))
    if "dir" in modes:
        gc = ak.to_numpy(ak.fill_none(ak.pad_none(pclass(gpt, geta, gphi), 2, clip=True), 0))
        push(D, dict(npr=npr, ng=ng, nj=nj, nb=nb, mll=mll, flav=flav, l1pt=np.fmax(lep["apt"], lep["bpt"]), l2pt=np.fmin(lep["apt"], lep["bpt"]),
                     la=np.stack([lep["apt"], lep["aeta"], lep["aphi"]], -1), lb=np.stack([lep["bpt"], lep["beta"], lep["bphi"]], -1),
                     g=np.stack([Gp["pt"], Gp["eta"], Gp["phi"]], -1), j=np.stack([Jj["pt"], Jj["eta"], Jj["phi"], Jj["m"]], -1),
                     gcls=gc, evt=np.arange(N) + evbase))
    # ---------------------------------------------------------------- FF candidate rows
    if "ffm" in modes:
        cand = np.where(has & (npr == 1) & (ng == 1) & (Gp["pt"][:, 0] > 25) & (mll > 55))[0]
        if len(cand):
            gprm = ak.to_list(ak.zip({"pt": G["gph_pt"], "eta": G["gph_eta"], "phi": G["gph_phi"], "pr": gpr})[cand])
            GJl = ak.to_list(ak.zip({"pt": GJ["PT"], "eta": GJ["Eta"], "phi": GJ["Phi"]})[cand])
            glL = ak.to_list(ak.zip({"pt": G["glep_pt"], "eta": G["glep_eta"], "phi": G["glep_phi"], "pr": glp})[cand])
            Jl = ak.to_list(ak.zip({"pt": jpt, "eta": jeta, "phi": jphi, "m": jm, "b": jb})[cand])
            for ii, i in enumerate(cand):
                r0 = (Gp["pt"][i, 0], Gp["eta"][i, 0], Gp["phi"][i, 0])
                if not any(p["pr"] and p["pt"] > 10 and dR(p["eta"], p["phi"], r0[1], r0[2]) < 0.1 for p in gprm[ii]): continue   # base photon must be the prompt one
                leps = [(lep["aeta"][i], lep["aphi"][i]), (lep["beta"][i], lep["bphi"][i])]
                base_j = [j for j in Jl[ii] if j["pt"] > 25 and abs(j["eta"]) < 4.7 and all(dR(j["eta"], j["phi"], e, p) > 0.4 for e, p in leps) and dR(j["eta"], j["phi"], r0[1], r0[2]) > 0.4]
                for c in GJl[ii]:
                    if not (c["pt"] > 25 and abs(c["eta"]) < 2.5): continue
                    if any(l["pr"] and l["pt"] > 10 and dR(l["eta"], l["phi"], c["eta"], c["phi"]) < 0.4 for l in glL[ii]): continue
                    if any(dR(c["eta"], c["phi"], e, p) < 0.4 for e, p in leps) or dR(c["eta"], c["phi"], r0[1], r0[2]) < 0.4: continue
                    if any(p["pr"] and p["pt"] > 10 and dR(p["eta"], p["phi"], c["eta"], c["phi"]) < 0.4 for p in gprm[ii]): continue
                    # remove the reco jet that is the faking jet (closest within 0.4)
                    dd = [dR(j["eta"], j["phi"], c["eta"], c["phi"]) for j in base_j]
                    rem = [j for k, j in enumerate(base_j) if not (dd and k == int(np.argmin(dd)) and dd[k] < 0.4)]
                    if len(rem) < 2: continue
                    rem = sorted(rem, key=lambda j: -j["pt"]); nbb = sum(1 for j in rem if abs(j["eta"]) < 2.5 and (j["b"] & 1))
                    push(F, dict(npr=npr[i], flav=flav[i], mll=mll[i], la=[lep["apt"][i], lep["aeta"][i], lep["aphi"][i]], lb=[lep["bpt"][i], lep["beta"][i], lep["bphi"][i]],
                                 g0=list(r0), jc=[c["pt"], c["eta"], c["phi"]], nj=len(rem), nb=nbb,
                                 j=[[x["pt"], x["eta"], x["phi"], x["m"]] for x in (rem + [dict(pt=np.nan, eta=np.nan, phi=np.nan, m=np.nan)]*2)[:2]], evt=evbase + i))
def fin(S, derived):
    Rr = {k: np.concatenate(v) if v[0].ndim >= 1 and k not in () else np.array(v) for k, v in S.items()} if S else {}
    return Rr
if "rate" in modes: np.savez_compressed(out + "_rate.npz", nev_total=nev_total, **R)
if "dir" in modes:
    Dd = {k: np.concatenate(v) for k, v in D.items()}
    with np.errstate(invalid="ignore"): keep = np.isfinite(Dd["mll"]) & (Dd["ng"] >= 1) & (Dd["nj"] >= 2)
    Dd = {k: v[keep] for k, v in Dd.items()}
    la, lb, gg, jj = Dd["la"], Dd["lb"], Dd["g"], Dd["j"]
    PZ = p4(la[:, 0], la[:, 1], la[:, 2]) + p4(lb[:, 0], lb[:, 1], lb[:, 2]); PG = p4(gg[:, 0, 0], gg[:, 0, 1], gg[:, 0, 2]) + p4(gg[:, 1, 0], gg[:, 1, 1], gg[:, 1, 2])
    PJ1, PJ2 = p4(jj[:, 0, 0], jj[:, 0, 1], jj[:, 0, 2], jj[:, 0, 3]), p4(jj[:, 1, 0], jj[:, 1, 1], jj[:, 1, 2], jj[:, 1, 3])
    Dd["mgg"], Dd["ptgg"], ygg = kin(PG); Dd["mjj"], _, _ = kin(PJ1 + PJ2); _, _, y1 = kin(PJ1); _, _, y2 = kin(PJ2); _, Dd["ptZ"], yZ = kin(PZ)
    Dd["mllgg"], _, _ = kin(PZ + PG); Dd["detajj"] = abs(jj[:, 0, 1] - jj[:, 1, 1])
    with np.errstate(all="ignore"): Dd["zep_gg"] = abs(ygg - 0.5*(y1 + y2))/abs(y1 - y2)
    Dd["g1pt"], Dd["g2pt"] = gg[:, 0, 0], gg[:, 1, 0]
    np.savez_compressed(out + "_dir.npz", nev_total=nev_total, **Dd)
if "ffm" in modes:
    Ff = {k: np.array(v) for k, v in F.items()}
    np.savez_compressed(out + "_ffm.npz", nev_total=nev_total, **Ff)
print(f"{out}: modes={modes} files={len(files)} events={nev_total} ffm_rows={len(F.get('evt', []))}")
