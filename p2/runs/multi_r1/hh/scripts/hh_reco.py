#!/usr/bin/env python3
"""Shared Delphes-level reconstruction for the HH studies (pre-G2): per-event numpy arrays from slim Delphes + GenTruth friend files.
Selection objects (pre-declared, config/tagging_scenarios.yaml):  fat jets anti-kT 0.8, pT>=300, |eta|<2.4 (two leading); VBS AK5 pair: pT>30, |eta|<4.7, dR>0.8 from
the selected fat jets, opposite hemispheres, anchor rule mjj>500 & |d eta|>3.5 (any pair); soft-drop mass of each fat jet from SoftDroppedP4[5] (no JES: Delphes limitation).
Truth classes of a fat jet (first match wins): 5 top (nWq==2&ntb==1), 4 Hbb (nHb==2), 3 bb_nonH (nB>=2), 2 b (nB==1), 1 c (nC>=1), 0 l.
load(files) -> dict(n_gen, arrays...). n_gen = sum of json n_lhe (LHE events processed by PY8, so MLM-vetoed events still count in the normalisation).
Usage as a library; run directly to cache a sample: hh_reco.py <outdir/sample_dir> <cache.npz>"""
import glob, json, os, sys
import numpy as np, awkward as ak, uproot
CLS = ["l", "c", "b", "bb_nonH", "Hbb", "top"]
def dphi(a, b): return (a - b + np.pi) % (2 * np.pi) - np.pi
def sample_files(d, name=None):
    """complete jobs only: <name>_s<seed>.root + _gen.root + .json"""
    out = []
    for f in sorted(glob.glob(f"{d}/*_s[0-9]*.root")):
        if f.endswith("_gen.root") or f.endswith("_full.root"): continue
        j = f[:-5] + ".json"; g = f[:-5] + "_gen.root"
        if os.path.exists(j) and os.path.exists(g): out.append(f)
    return out
def _one(f):
    t = uproot.open(f)["Delphes"]; g = uproot.open(f[:-5] + "_gen.root")["GenTruth"]; n = t.num_entries
    meta = json.load(open(f[:-5] + ".json"))
    pt, eta, phi, m = (t[f"FatJet/FatJet.{k}"].array() for k in ("PT", "Eta", "Phi", "Mass"))
    p4 = t["FatJet/FatJet.SoftDroppedP4[5]"].array()[:, :, 0]; msd = np.sqrt(np.maximum(p4.fE**2 - p4.fP.fX**2 - p4.fP.fY**2 - p4.fP.fZ**2, 0))
    nB, nC, nWq, ntb, nHb = (g[k].array() for k in ("fj_nB", "fj_nC", "fj_nWq", "fj_ntb", "fj_nHb"))
    sel = (pt >= 300) & (abs(eta) < 2.4)
    cls = ak.where((nWq == 2) & (ntb == 1), 5, ak.where(nHb == 2, 4, ak.where(nB >= 2, 3, ak.where(nB == 1, 2, ak.where(nC >= 1, 1, 0)))))
    def two(x, fill=0.0): return ak.to_numpy(ak.fill_none(ak.pad_none(x[sel], 2, axis=1)[:, :2], fill))
    P, E, PH, M, MS, C = two(pt), two(eta), two(phi), two(m), two(msd), two(cls, -1)
    nsel = ak.to_numpy(ak.num(pt[sel]))
    jpt, jeta, jphi, jm = (t[f"Jet/Jet.{k}"].array() for k in ("PT", "Eta", "Phi", "Mass"))
    a, b = ak.unzip(ak.cartesian([ak.zip({"e": jeta, "p": jphi}), ak.zip({"e": eta[sel], "p": phi[sel]})], axis=1, nested=True))
    ok = (jpt > 30) & (abs(jeta) < 4.7) & ak.all(np.hypot(a.e - b.e, dphi(a.p, b.p)) > 0.8, axis=2)
    J = ak.zip({"pt": jpt[ok], "eta": jeta[ok], "phi": jphi[ok], "m": jm[ok]})
    x, y = ak.unzip(ak.combinations(J, 2, axis=1))
    px = x.pt * np.cos(x.phi) + y.pt * np.cos(y.phi); py = x.pt * np.sin(x.phi) + y.pt * np.sin(y.phi); pz = x.pt * np.sinh(x.eta) + y.pt * np.sinh(y.eta)
    e = np.sqrt(x.m**2 + (x.pt * np.cosh(x.eta))**2) + np.sqrt(y.m**2 + (y.pt * np.cosh(y.eta))**2); mjj = np.sqrt(np.maximum(e**2 - px**2 - py**2 - pz**2, 0))
    opp = (x.eta * y.eta < 0); de = abs(x.eta - y.eta)
    anchor = ak.to_numpy(ak.any(opp & (mjj > 500) & (de > 3.5), axis=1))
    mjj_opp = ak.fill_none(ak.max(ak.where(opp, mjj, 0.0), axis=1), 0.0)
    J0 = ak.zip({"pt": jpt[(jpt > 30) & (abs(jeta) < 4.7)], "eta": jeta[(jpt > 30) & (abs(jeta) < 4.7)], "phi": jphi[(jpt > 30) & (abs(jeta) < 4.7)], "m": jm[(jpt > 30) & (abs(jeta) < 4.7)]})
    x0, y0 = ak.unzip(ak.combinations(J0, 2, axis=1))
    qx = x0.pt * np.cos(x0.phi) + y0.pt * np.cos(y0.phi); qy = x0.pt * np.sin(x0.phi) + y0.pt * np.sin(y0.phi); qz = x0.pt * np.sinh(x0.eta) + y0.pt * np.sinh(y0.eta)
    qe = np.sqrt(x0.m**2 + (x0.pt * np.cosh(x0.eta))**2) + np.sqrt(y0.m**2 + (y0.pt * np.cosh(y0.eta))**2); mjj0 = np.sqrt(np.maximum(qe**2 - qx**2 - qy**2 - qz**2, 0))
    pair_only = ak.to_numpy(ak.any((x0.eta * y0.eta < 0) & (mjj0 > 500) & (abs(x0.eta - y0.eta) > 3.5), axis=1))     # VBS pair ignoring the fat jets (twin-check factorisation only)
    # fat-jet pair invariant mass (proxy for m(HH))
    ok2 = nsel >= 2
    px2 = P[:, 0] * np.cos(PH[:, 0]) + P[:, 1] * np.cos(PH[:, 1]); py2 = P[:, 0] * np.sin(PH[:, 0]) + P[:, 1] * np.sin(PH[:, 1]); pz2 = P[:, 0] * np.sinh(E[:, 0]) + P[:, 1] * np.sinh(E[:, 1])
    e2 = np.sqrt(M[:, 0]**2 + (P[:, 0] * np.cosh(E[:, 0]))**2) + np.sqrt(M[:, 1]**2 + (P[:, 1] * np.cosh(E[:, 1]))**2)
    mHH = np.where(ok2, np.sqrt(np.maximum(e2**2 - px2**2 - py2**2 - pz2**2, 0)), 0.0)
    hb = ak.to_numpy(g["g_nhard_b"].array()) if "g_nhard_b" in g.keys() else np.zeros(n, int); hbb = ak.to_numpy(g["g_nhard_bbar"].array()) if "g_nhard_bbar" in g.keys() else np.zeros(n, int)
    return dict(n_entries=n, bbbar_hard=((hb >= 1) & (hbb >= 1)), n_lhe=int(meta["n_lhe"]), nsel=nsel, pt1=P[:, 0], pt2=P[:, 1], eta1=E[:, 0], eta2=E[:, 1], msd1=MS[:, 0], msd2=MS[:, 1], cls1=C[:, 0], cls2=C[:, 1],
                vbs=anchor, pair_only=pair_only, mjj_opp=ak.to_numpy(mjj_opp), mHH=mHH,
                fj_pt_all=ak.to_numpy(ak.flatten(pt[sel])), fj_msd_all=ak.to_numpy(ak.flatten(msd[sel])), fj_cls_all=ak.to_numpy(ak.flatten(cls[sel])))
def load(files):
    parts = [_one(f) for f in files]
    d = {}
    for k in parts[0]:
        if k in ("n_entries", "n_lhe"): d[k] = sum(p[k] for p in parts)
        else: d[k] = np.concatenate([p[k] for p in parts])
    d["n_gen"] = d["n_lhe"]; d["files"] = [os.path.basename(f) for f in files]
    return d
def load_named(name, root):
    """load a sample directory; applies the flavour partition O1 (02 report): events of Q_4j_vbs with both a b and a bbar in the hard final state are REMOVED (their kinematics are covered by Q_bbjj_vbs); normalisation (n_gen) unchanged"""
    d = load(sample_files(f"{root}/{name}"))
    if name.startswith("Q_4j_vbs"):
        d["n_removed_partition"] = int(d["bbbar_hard"].sum()); d["nsel"] = np.where(d["bbbar_hard"], 0, d["nsel"])
    return d
def stages(d, lead=450.0, ptmin=300.0):
    two = (d["nsel"] >= 2) & (d["pt2"] >= ptmin); l = two & (d["pt1"] >= lead); v = l & d["vbs"]
    return two, l, v
def window(d, lo=90.0, hi=150.0, scale=1.0):
    """both leading fat jets in [lo,hi] after rescaling m_SD by `scale` (mass-scale variation)"""
    return (d["msd1"] * scale > lo) & (d["msd1"] * scale < hi) & (d["msd2"] * scale > lo) & (d["msd2"] * scale < hi)
def tag_prob(sc):
    """class index (0..5) -> probability, from a tagging scenario dict"""
    return np.array([sc["mistag_gluon_light"], sc["mistag_c"], sc["mistag_g2bb_or_b"], sc["mistag_bb_nonH"], sc["eff_Hbb_contained"], sc["mistag_top"]])
def tag_weight(d, sc):
    pr = tag_prob(sc); c1 = np.where(d["cls1"] < 0, 0, d["cls1"]).astype(int); c2 = np.where(d["cls2"] < 0, 0, d["cls2"]).astype(int)
    return pr[c1] * pr[c2]
if __name__ == "__main__":
    d = load(sample_files(sys.argv[1])); np.savez_compressed(sys.argv[2], **{k: v for k, v in d.items() if isinstance(v, (np.ndarray, int))}); print(sys.argv[1], d["n_gen"], d["n_entries"])
