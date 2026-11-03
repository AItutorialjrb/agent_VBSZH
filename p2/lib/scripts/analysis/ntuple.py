#!/usr/bin/env python3
"""Phase-05 pilot ntupler: Delphes (slim or full) + GenTruth friend -> flat per-event (direct) or
per-fake-combination (fake factor) arrays in an .npz.  No physics normalisation here (done in sensitivity.py).

Usage: python3 -P ntuple.py <out.npz> <mode direct|ff1|ff2> <delphes.root>[,<more.root>...]
       (GenTruth friends are found as <file without .root>_gen.root, same entry order)

Object definitions (reference arXiv:2512.07689 Sec. III "good particles", plus standard overlap removal):
  leptons  e: pT>15, |eta|<2.5 ; mu: pT>15, |eta|<2.4 ; OSSF pair with m_ll closest to mZ=91.19
  photons  pT>20, |eta|<2.5, outside 1.4442<|eta|<1.566, dR(gamma, chosen leptons)>0.4   (Delphes photons are isolated)
  jets     pT>25, |eta|<4.7, dR(jet, chosen leptons & leading two photons)>0.4 ; tag jets = leading two
  b-tag    selected jets with |eta|<2.5 and (BTag & 1)
Fake-factor modes (cross-check only; never use Delphes fakes):
  ff1: events with exactly one prompt generator photon (GenTruth.n_prompt_photons==1); the leading reco photon is the real
       one, every other selected-jet candidate (pT>20,|eta|<2.5 after x-scaling) may fake the second photon.
  ff2: events with n_prompt_photons==0; every jet pair may fake both photons.
  Fake pT = x*pT(jet), x~N(0.85,0.10) truncated [0.5,1] (fixed seed); remaining jets (pT>25) give the tag jets.
  Stored per row: wf_flat = prod(1e-3) and wf_pt = prod(1e-3*(pT_jet/50)^-0.5, x2 endcap); scenarios scale linearly.
"""
import sys, numpy as np, awkward as ak, uproot

MZ = 91.1876
out, mode, files = sys.argv[1], sys.argv[2], sys.argv[3].split(",")
rng = np.random.default_rng(13600555)

def m_of(pt1, eta1, phi1, m1, pt2, eta2, phi2, m2):
    px = pt1*np.cos(phi1) + pt2*np.cos(phi2); py = pt1*np.sin(phi1) + pt2*np.sin(phi2)
    pz = pt1*np.sinh(eta1) + pt2*np.sinh(eta2)
    e = np.sqrt((pt1*np.cosh(eta1))**2 + m1**2) + np.sqrt((pt2*np.cosh(eta2))**2 + m2**2)
    return np.sqrt(np.maximum(e**2 - px**2 - py**2 - pz**2, 0)), px, py, pz, e

def p4(pt, eta, phi, m=0.0):
    return np.stack([pt*np.cos(phi), pt*np.sin(phi), pt*np.sinh(eta), np.sqrt((pt*np.cosh(eta))**2 + m**2)], -1)

def kin(P):  # P[...,4] -> m, pt, rapidity
    px, py, pz, e = P[..., 0], P[..., 1], P[..., 2], P[..., 3]
    m = np.sqrt(np.maximum(e**2 - px**2 - py**2 - pz**2, 0)); pt = np.hypot(px, py)
    with np.errstate(all="ignore"):
        y = 0.5*np.log((e + pz)/(e - pz))
    return m, pt, y

def dphi(a, b): return (a - b + np.pi) % (2*np.pi) - np.pi
def dR(e1, p1, e2, p2): return np.hypot(e1 - e2, dphi(p1, p2))

def load(f):
    t = uproot.open(f)["Delphes"]
    br = {}
    for c, keys in (("Electron", "PT Eta Phi Charge"), ("Muon", "PT Eta Phi Charge"), ("Photon", "PT Eta Phi"),
                    ("Jet", "PT Eta Phi Mass BTag")):
        for k in keys.split():
            br[f"{c}.{k}"] = t[f"{c}/{c}.{k}"].array()
    g = uproot.open(f[:-5] + "_gen.root")["GenTruth"]
    br["npr"] = ak.to_numpy(g["n_prompt_photons"].array())
    assert g.num_entries == t.num_entries, f
    return br

def best_pair(pt, eta, phi, q, mass):
    sel = (pt > 15) & (abs(eta) < (2.5 if mass < 0.01 else 2.4))
    L = ak.zip({"pt": pt[sel], "eta": eta[sel], "phi": phi[sel], "q": q[sel]})
    c = ak.combinations(L, 2, fields=["a", "b"])
    mm = m_of(c.a.pt, c.a.eta, c.a.phi, mass, c.b.pt, c.b.eta, c.b.phi, mass)[0]
    mm = ak.where(c.a.q * c.b.q < 0, mm, -1e9)
    i = ak.argmin(abs(mm - MZ), axis=1, keepdims=True)
    b = c[i]; mb = mm[i]
    b = ak.firsts(b); mb = ak.fill_none(ak.firsts(mb), -1e9)
    ok = mb > 0
    return ok, ak.where(ok, mb, np.nan), b

def first_n(x, n, fill=np.nan):
    return ak.to_numpy(ak.fill_none(ak.pad_none(x, n, clip=True), fill))

rows = {}
def push(d):
    for k, v in d.items():
        rows.setdefault(k, []).append(np.asarray(v))

nev_total = 0
for f in files:
    B = load(f); N = len(B["npr"]); nev_total += N
    oke, mee, be = best_pair(B["Electron.PT"], B["Electron.Eta"], B["Electron.Phi"], B["Electron.Charge"], 0.000511)
    okm, mmm, bm = best_pair(B["Muon.PT"], B["Muon.Eta"], B["Muon.Phi"], B["Muon.Charge"], 0.1057)
    oke = ak.to_numpy(oke); okm = ak.to_numpy(okm); mee = ak.to_numpy(mee); mmm = ak.to_numpy(mmm)
    use_e = oke & (~okm | (np.abs(np.nan_to_num(mee, nan=1e9) - MZ) <= np.abs(np.nan_to_num(mmm, nan=1e9) - MZ)))
    has = oke | okm
    lep = {}
    for k in ("pt", "eta", "phi"):
        for s in "ab":
            ve = ak.to_numpy(ak.fill_none(be[s][k], np.nan)) if True else None
            vm = ak.to_numpy(ak.fill_none(bm[s][k], np.nan))
            lep[s+k] = np.where(use_e, ve, vm)
    mll = np.where(use_e, mee, mmm); mll[~has] = np.nan
    flav = np.where(use_e, 11, 13); flav[~has] = 0
    la_e, la_p, lb_e, lb_p = [np.nan_to_num(lep[k], nan=99.) for k in ("aeta", "aphi", "beta", "bphi")]
    # photons
    gpt, geta, gphi = B["Photon.PT"], B["Photon.Eta"], B["Photon.Phi"]
    gsel = (gpt > 20) & (abs(geta) < 2.5) & ~((abs(geta) > 1.4442) & (abs(geta) < 1.566)) \
        & (dR(geta, gphi, la_e, la_p) > 0.4) & (dR(geta, gphi, lb_e, lb_p) > 0.4)
    gpt, geta, gphi = gpt[gsel], geta[gsel], gphi[gsel]
    ng = ak.to_numpy(ak.num(gpt))
    G = {k: first_n(v, 2) for k, v in (("pt", gpt), ("eta", geta), ("phi", gphi))}
    # jets
    jpt, jeta, jphi, jm, jb = B["Jet.PT"], B["Jet.Eta"], B["Jet.Phi"], B["Jet.Mass"], B["Jet.BTag"]
    jsel = (jpt > 25) & (abs(jeta) < 4.7) & (dR(jeta, jphi, la_e, la_p) > 0.4) & (dR(jeta, jphi, lb_e, lb_p) > 0.4)
    for k in range(2):
        jsel = jsel & (dR(jeta, jphi, np.nan_to_num(G["eta"][:, k], nan=99.), np.nan_to_num(G["phi"][:, k], nan=99.)) > 0.4)
    nb = ak.to_numpy(ak.sum(jsel & (abs(jeta) < 2.5) & ((jb & 1) == 1), axis=1))
    J = {k: first_n(v[jsel], 2) for k, v in (("pt", jpt), ("eta", jeta), ("phi", jphi), ("m", jm))}
    nj = ak.to_numpy(ak.num(jpt[jsel]))
    if mode == "direct":
        push(dict(npr=B["npr"], ng=ng, nj=nj, nb=nb, mll=mll, flav=flav, l1pt=np.fmax(lep["apt"], lep["bpt"]),
                  l2pt=np.fmin(lep["apt"], lep["bpt"]), la=np.stack([lep["apt"], lep["aeta"], lep["aphi"]], -1),
                  lb=np.stack([lep["bpt"], lep["beta"], lep["bphi"]], -1),
                  g=np.stack([G["pt"], G["eta"], G["phi"]], -1), j=np.stack([J["pt"], J["eta"], J["phi"], J["m"]], -1),
                  wf_flat=np.ones(N), wf_pt=np.ones(N), evt=np.arange(N) + nev_total - N))
        continue
    # ---------------- fake-factor modes: python loop over candidate events ----------------
    nreq = 1 if mode == "ff1" else 0
    cand = np.where(has & (B["npr"] == nreq))[0]
    Jall = ak.to_list(ak.zip({"pt": B["Jet.PT"], "eta": B["Jet.Eta"], "phi": B["Jet.Phi"], "m": B["Jet.Mass"], "b": B["Jet.BTag"]})[cand])
    Gl = ak.to_list(ak.zip({"pt": gpt, "eta": geta, "phi": gphi})[cand])
    for ii, i in enumerate(cand):
        leps = [(lep["aeta"][i], lep["aphi"][i]), (lep["beta"][i], lep["bphi"][i])]
        real = Gl[ii][:1] if mode == "ff1" else []
        if mode == "ff1" and not real: continue
        jets = [j for j in Jall[ii] if j["pt"] > 20 and abs(j["eta"]) < 4.7
                and all(dR(j["eta"], j["phi"], e, p) > 0.4 for e, p in leps)
                and all(dR(j["eta"], j["phi"], r["eta"], r["phi"]) > 0.4 for r in real)]
        xs = np.clip(rng.normal(0.85, 0.10, len(jets)), 0.5, 1.0)
        nf = 1 if mode == "ff1" else 2
        combos = [(a,) for a in range(len(jets))] if nf == 1 else \
                 [(a, b) for a in range(len(jets)) for b in range(a+1, len(jets))]
        for fk in combos:
            phs = [(r["pt"], r["eta"], r["phi"]) for r in real]; wfl, wpt, ok = 1.0, 1.0, True
            for k in fk:
                pt, eta = xs[k]*jets[k]["pt"], jets[k]["eta"]
                if not (pt > 20 and abs(eta) < 2.5 and not (1.4442 < abs(eta) < 1.566)): ok = False; break
                phs.append((pt, eta, jets[k]["phi"])); wfl *= 1e-3
                wpt *= 1e-3*(jets[k]["pt"]/50.)**-0.5*(2.0 if abs(eta) > 1.566 else 1.0)
            if not ok: continue
            phs.sort(key=lambda p: -p[0])
            rest = [jets[k] for k in range(len(jets)) if k not in fk and jets[k]["pt"] > 25]
            nbb = sum(1 for j in rest if abs(j["eta"]) < 2.5 and (j["b"] & 1))
            jj = (rest + [dict(pt=np.nan, eta=np.nan, phi=np.nan, m=np.nan)]*2)[:2]
            push(dict(npr=B["npr"][i], ng=2, nj=len(rest), nb=nbb, mll=mll[i], flav=flav[i],
                      l1pt=max(lep["apt"][i], lep["bpt"][i]), l2pt=min(lep["apt"][i], lep["bpt"][i]),
                      la=[lep["apt"][i], lep["aeta"][i], lep["aphi"][i]], lb=[lep["bpt"][i], lep["beta"][i], lep["bphi"][i]],
                      g=[list(p) for p in phs[:2]], j=[[x["pt"], x["eta"], x["phi"], x["m"]] for x in jj],
                      wf_flat=wfl, wf_pt=wpt, evt=nev_total - N + i))

if mode == "direct":
    R = {k: np.concatenate(v) for k, v in rows.items()}
else:
    R = {k: np.array(v, dtype=float) for k, v in rows.items()} if rows else {}
# derived variables
if R:
    la, lb, g, j = R["la"], R["lb"], R["g"], R["j"]
    PZ = p4(la[:, 0], la[:, 1], la[:, 2]) + p4(lb[:, 0], lb[:, 1], lb[:, 2])
    PG = p4(g[:, 0, 0], g[:, 0, 1], g[:, 0, 2]) + p4(g[:, 1, 0], g[:, 1, 1], g[:, 1, 2])
    PJ1, PJ2 = p4(j[:, 0, 0], j[:, 0, 1], j[:, 0, 2], j[:, 0, 3]), p4(j[:, 1, 0], j[:, 1, 1], j[:, 1, 2], j[:, 1, 3])
    R["mgg"], R["ptgg"], ygg = kin(PG)
    R["mjj"], _, _ = kin(PJ1 + PJ2)
    _, _, y1 = kin(PJ1); _, _, y2 = kin(PJ2)
    _, R["ptZ"], yZ = kin(PZ)
    R["mllgg"], _, _ = kin(PZ + PG)
    R["detajj"] = abs(j[:, 0, 1] - j[:, 1, 1])
    with np.errstate(all="ignore"):
        R["zep_gg"] = abs(ygg - 0.5*(y1 + y2)) / abs(y1 - y2)
        R["zep_Z"] = abs(yZ - 0.5*(y1 + y2)) / abs(y1 - y2)
    R["g1pt"], R["g2pt"] = g[:, 0, 0], g[:, 1, 0]
    R["j1pt"], R["j2pt"] = j[:, 0, 0], j[:, 1, 0]
R["nev_total"] = np.array(nev_total)
np.savez_compressed(out, **R)
print(f"{out}: mode={mode} files={len(files)} events={nev_total} rows={len(R.get('npr', []))}")
