#!/usr/bin/env python3
"""Feasibility / effective-N bookkeeping on the Phase-03 TEST samples (2000 events each) - NOT a result, NO optimisation.
Preliminary anchor (config/tagging_scenarios.yaml): 2 fat jets pT>=300 (lead>=450), |eta|<2.4; two non-overlap AK5 (pT>30, |eta|<4.7, dR>0.8 from fat jets) with mjj>500, |d eta|>3.5;
both fat-jet soft-drop masses in [90,150].  Truth-tag weight = product over the 2 leading fat jets of p(class; scenario).
Outputs per sample: raw counts at each stage, raw/weighted N in the anchor SR, N_eff = (sum w)^2/sum w^2, brute-force-equivalent expected SR events for L, and the generator
statistics needed to reach N_eff>=10 (naive scaling).  Usage: sr_feasibility.py <test_dir> <matrix.yaml> <scenarios.yaml> <out_json>"""
import sys, glob, os, json, yaml, numpy as np, awkward as ak, uproot
td, my, sy, outj = sys.argv[1:5]
M = {s["name"]: s for s in yaml.safe_load(open(my))["samples"]}; SC = yaml.safe_load(open(sy))["tagging"]
def dphi(a, b): return (a - b + np.pi) % (2 * np.pi) - np.pi
res = {}
for d in sorted(glob.glob(f"{td}/*/")):
    s = os.path.basename(d.rstrip("/")); fs = glob.glob(f"{d}/{s}_s*[0-9].root")
    if not fs or s not in M: continue
    t = uproot.open(fs[0])["Delphes"]; g = uproot.open(fs[0].replace(".root", "_gen.root"))["GenTruth"]; n = t.num_entries
    pt, eta, phi, m = (t[f"FatJet/FatJet.{k}"].array() for k in ("PT", "Eta", "Phi", "Mass"))
    p4 = t["FatJet/FatJet.SoftDroppedP4[5]"].array()[:, :, 0]; msd = np.sqrt(np.maximum(p4.fE**2 - p4.fP.fX**2 - p4.fP.fY**2 - p4.fP.fZ**2, 0))
    nB, nC, nWq, ntb, nHb = (g[k].array() for k in ("fj_nB", "fj_nC", "fj_nWq", "fj_ntb", "fj_nHb"))
    sel = (pt >= 300) & (abs(eta) < 2.4)
    two = ak.num(pt[sel]) >= 2
    lead = ak.fill_none(ak.firsts(pt[sel]), 0) >= 450
    jpt, jeta, jphi, jm = (t[f"Jet/Jet.{k}"].array() for k in ("PT", "Eta", "Phi", "Mass"))
    a, b = ak.unzip(ak.cartesian([ak.zip({"e": jeta, "p": jphi}), ak.zip({"e": eta[sel], "p": phi[sel]})], axis=1, nested=True))
    ok = (jpt > 30) & (abs(jeta) < 4.7) & ak.all(np.hypot(a.e - b.e, dphi(a.p, b.p)) > 0.8, axis=2)
    # best VBS pair: maximise |d eta| among opposite-hemisphere non-overlap jets satisfying mjj>500
    J = ak.zip({"pt": jpt[ok], "eta": jeta[ok], "phi": jphi[ok], "m": jm[ok]})
    x, y = ak.unzip(ak.combinations(J, 2, axis=1))
    px = x.pt * np.cos(x.phi) + y.pt * np.cos(y.phi); py = x.pt * np.sin(x.phi) + y.pt * np.sin(y.phi); pz = x.pt * np.sinh(x.eta) + y.pt * np.sinh(y.eta)
    e = np.sqrt(x.m**2 + (x.pt * np.cosh(x.eta))**2) + np.sqrt(y.m**2 + (y.pt * np.cosh(y.eta))**2); mjj = np.sqrt(np.maximum(e**2 - px**2 - py**2 - pz**2, 0))
    vbs = ak.any((mjj > 500) & (abs(x.eta - y.eta) > 3.5) & (x.eta * y.eta < 0), axis=1)
    msel = msd[sel]; m2 = ak.pad_none(msel, 2, axis=1)[:, :2]
    win = ak.to_numpy(ak.fill_none(ak.all((m2 > 90) & (m2 < 150), axis=1), False))
    base = ak.to_numpy(two) & ak.to_numpy(lead) & ak.to_numpy(vbs); full = base & win
    sig = M[s]["sigma_x_BR_fb"]; L = 3000.0; r = dict(n_gen=int(n), sigma_x_BR_fb=sig, raw=dict(two_fatjets=int(ak.sum(two)), plus_lead450=int((ak.to_numpy(two) & ak.to_numpy(lead)).sum()), plus_vbs=int(base.sum()), plus_msd_window=int(full.sum())))
    # truth-tag weights per scenario, two leading selected fat jets
    # classes (config/tagging_scenarios.yaml): 0 l, 1 c, 2 b(nB=1), 3 bb_nonH, 4 Hbb, 5 top   (first match wins: top > Hbb > bb_nonH > b > c > l)
    cls = ak.where((nWq[sel] == 2) & (ntb[sel] == 1), 5, ak.where(nHb[sel] == 2, 4, ak.where(nB[sel] >= 2, 3, ak.where(nB[sel] == 1, 2, ak.where(nC[sel] >= 1, 1, 0)))))
    c2 = ak.fill_none(ak.pad_none(cls, 2, axis=1)[:, :2], 0)
    from scipy.stats import chi2
    k = int(full.sum()); klo = 0.0 if k == 0 else 0.5 * chi2.ppf(0.025, 2 * k); khi = 0.5 * chi2.ppf(0.975, 2 * k + 2)
    r["weighted"] = {}
    for sc, q in SC.items():
        pr = np.array([q["mistag_gluon_light"], q["mistag_c"], q["mistag_g2bb_or_b"], q["mistag_bb_nonH"], q["eff_Hbb_contained"], q["mistag_top"]])
        w = np.prod(pr[ak.to_numpy(c2)], axis=1) * full
        sw, sw2 = float(w.sum()), float((w**2).sum()); sc_ev = sig * L / n
        wmax = q["eff_Hbb_contained"] ** 2
        d = dict(raw_SR=k, sum_w=sw, neff=sw**2 / sw2 if sw2 > 0 else 0.0, expected_SR_events_at_3000fb=sc_ev * sw, expected_SR_events_at_500fb=sig * 500 * sw / n,
                 stat_err_rel=(np.sqrt(sw2) / sw if sw > 0 else None))
        if k > 0:   # 95% Garwood interval on the raw count, applied multiplicatively to the weighted expectation
            d["interval95_500fb"] = [sig * 500 * sw / n * klo / k, sig * 500 * sw / n * khi / k]
        else:       # zero raw events: 95% UL = 3.0 raw events x per-event scale x conservative max weight eff_Hbb^2
            d["ul95_500fb"] = 3.0 * (sig * 500 / n) * wmax
        r["weighted"][sc] = d
    r["geom_acceptance_fraction"] = int(full.sum()) / n
    res[s] = r
json.dump(res, open(outj, "w"), indent=1, default=float)
for s, r in res.items(): print(s, r["raw"], {k: (round(v["expected_SR_events_at_3000fb"], 4), round(v["neff"], 2)) for k, v in r["weighted"].items()})
