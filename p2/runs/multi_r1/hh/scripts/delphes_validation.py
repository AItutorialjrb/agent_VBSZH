#!/usr/bin/env python3
"""Delphes object validation on the Phase-03 test samples (SMALL STATISTICS, validation only, no yields).
Usage: delphes_validation.py <test_dir> <out_json> [fig_dir]
For each <test_dir>/<sample>/<sample>_s*.root (+ _gen.root): large-R jets (R=0.8: pT, ungroomed and soft-drop mass, tau21/tau32), containment of H->bb in a fat jet,
VBS tagging jets (AK5 not overlapping fat jets), truth labels (nB,nC,nHb,nVq,nWq,ntb) and an ILLUSTRATIVE truth-tag weight (placeholder rates, NOT a result)."""
import sys, glob, os, json, numpy as np, awkward as ak, uproot
td, outj = sys.argv[1], sys.argv[2]; fd = sys.argv[3] if len(sys.argv) > 3 else None
def msd(t):
    p4 = t["FatJet/FatJet.SoftDroppedP4[5]"].array()[:, :, 0]
    return np.sqrt(np.maximum(p4.fE**2 - p4.fP.fX**2 - p4.fP.fY**2 - p4.fP.fZ**2, 0.0))
def dphi(a, b): return (a - b + np.pi) % (2 * np.pi) - np.pi
# ILLUSTRATIVE per-jet tag probabilities (nominal scenario placeholder; the declared scenarios live in config/tagging_scenarios.yaml)
P = dict(bb=0.60, b=0.05, c=0.02, l=0.01)
def pclass(nB, nC): return ak.where(nB >= 2, P["bb"], ak.where(nB == 1, P["b"], ak.where(nC >= 1, P["c"], P["l"])))
res = {}
for d in sorted(glob.glob(f"{td}/*/")):
    s = os.path.basename(d.rstrip("/")); fs = glob.glob(f"{d}/{s}_s*[0-9].root")
    if not fs: continue
    t = uproot.open(fs[0])["Delphes"]; g = uproot.open(fs[0].replace(".root", "_gen.root"))["GenTruth"]; n = t.num_entries
    fpt, feta, fphi, fm = (t[f"FatJet/FatJet.{k}"].array() for k in ("PT", "Eta", "Phi", "Mass")); sd = msd(t)
    tau = t["FatJet/FatJet.Tau[5]"].array(); t21 = ak.where(tau[:, :, 0] > 0, tau[:, :, 1] / tau[:, :, 0], -1.0); t32 = ak.where(tau[:, :, 1] > 0, tau[:, :, 2] / tau[:, :, 1], -1.0)
    sel = (fpt > 250) & (abs(feta) < 2.4); n2 = int(ak.sum(ak.num(fpt[sel]) >= 2))
    G = {k: g[k].array() for k in ("fj_nB", "fj_nC", "fj_nHb", "fj_nVq", "fj_nWq", "fj_ntb")}
    # VBS jets: AK5 pT>30,|eta|<4.7, dR>0.8 from every selected fat jet
    jpt, jeta, jphi, jm = (t[f"Jet/Jet.{k}"].array() for k in ("PT", "Eta", "Phi", "Mass"))
    a, b = ak.unzip(ak.cartesian([ak.zip({"e": jeta, "p": jphi}), ak.zip({"e": feta[sel], "p": fphi[sel]})], axis=1, nested=True))
    far = ak.all(np.hypot(a.e - b.e, dphi(a.p, b.p)) > 0.8, axis=2)
    ok = (jpt > 30) & (abs(jeta) < 4.7) & far
    J = ak.zip({"pt": jpt[ok], "eta": jeta[ok], "phi": jphi[ok], "m": jm[ok]})
    j1, j2 = ak.pad_none(J, 2, axis=1)[:, 0], ak.pad_none(J, 2, axis=1)[:, 1]
    def mjj(x, y):
        px = x.pt * np.cos(x.phi) + y.pt * np.cos(y.phi); py = x.pt * np.sin(x.phi) + y.pt * np.sin(y.phi); pz = x.pt * np.sinh(x.eta) + y.pt * np.sinh(y.eta)
        e = np.sqrt(x.m**2 + (x.pt * np.cosh(x.eta))**2) + np.sqrt(y.m**2 + (y.pt * np.cosh(y.eta))**2); return np.sqrt(np.maximum(e**2 - px**2 - py**2 - pz**2, 0))
    has2 = ak.num(J) >= 2; M = ak.to_numpy(ak.fill_none(mjj(j1, j2), -1)); DE = ak.to_numpy(ak.fill_none(abs(j1.eta - j2.eta), -1))
    vbs = (M > 500) & (DE > 3.5) & ak.to_numpy(has2)
    r = dict(file=os.path.basename(fs[0]), n_events=int(n), frac_ge1_fatjet_pt250=float(ak.mean(ak.num(fpt[sel]) >= 1)), frac_ge2_fatjet_pt250=n2 / n,
             frac_ge2_AK5_nonoverlap=float(ak.mean(has2)), frac_vbs_pair_m500_deta35=float(vbs.mean()),
             lead_fatjet_pt_median=float(np.median(ak.to_numpy(ak.fill_none(ak.firsts(fpt[sel]), 0))[ak.to_numpy(ak.num(fpt[sel]) > 0)])) if ak.any(ak.num(fpt[sel]) > 0) else None)
    # containment / mass for H->bb
    if "fj_nHb" in G and ak.sum(G["fj_nHb"] == 2) > 0:
        full = sel & (G["fj_nHb"] == 2); nH = ak.to_numpy(g["gnH"].array()); H1, H2 = g["gH1_pt"].array(), g["gH2_pt"].array()
        r["n_fatjets_with_both_Hb_inside"] = int(ak.sum(full)); r["n_gen_H"] = int(nH.sum())
        r["containment_per_genH"] = float(ak.sum(full) / max(nH.sum(), 1))
        r["Hbb_fatjet_mass_median_ungroomed"] = float(np.median(ak.to_numpy(ak.flatten(fm[full])))); q = np.percentile(ak.to_numpy(ak.flatten(sd[full])), [16, 50, 84])
        r["Hbb_fatjet_msd_p16_p50_p84"] = [float(x) for x in q]; r["Hbb_fatjet_nB_eq2_frac"] = float(ak.mean(ak.flatten(G["fj_nB"][full]) == 2))
        r["Hbb_fatjet_tau21_median"] = float(np.median(ak.to_numpy(ak.flatten(t21[full]))))
        # containment vs gen-H pT (both Higgs)
        hp = ak.to_numpy(ak.concatenate([H1[H1 > 0], H2[H2 > 0]])); edges = [0, 200, 300, 400, 600, 1000, 5000]
        # per-event: H matched if exists fat jet with nHb==2 and |pt-gH_pt|/gH_pt<0.3
        mtot = np.zeros(len(edges) - 1); mmat = np.zeros(len(edges) - 1)
        for Hk in (H1, H2):
            for i, (lo, hi) in enumerate(zip(edges[:-1], edges[1:])):
                inb = (Hk >= lo) & (Hk < hi); mtot[i] += float(ak.sum(inb))
                ptm = ak.any(full & (abs(fpt - Hk) < 0.3 * Hk), axis=1); mmat[i] += float(ak.sum(inb & ptm))
        r["containment_vs_pTH"] = dict(edges=edges, n_H=mtot.tolist(), n_matched=mmat.tolist())
    # truth-class census of the two leading selected fat jets + illustrative truth-tag weight
    L2 = ak.pad_none(sel, 2, axis=1)
    nB, nC = G["fj_nB"], G["fj_nC"]
    pj = pclass(nB, nC); pj = pj[sel]; pj2 = ak.pad_none(pj, 2, axis=1)[:, :2]; w = ak.to_numpy(ak.prod(ak.fill_none(pj2, 0.0), axis=1)) * (ak.to_numpy(ak.num(pj) >= 2))
    r["illustrative_truth_tag_weight"] = dict(note="placeholder per-jet rates P=%s, validation of the mechanism only" % P, sum_w=float(w.sum()), neff_w=float(w.sum()**2 / max((w**2).sum(), 1e-30)),
                                              n_events_with_2fj=int(n2), neff_raw=float(n2))
    cls = ak.to_numpy(ak.flatten(ak.where(nB[sel] >= 2, 2, ak.where(nB[sel] == 1, 1, ak.where(nC[sel] >= 1, -1, 0)))))
    r["fatjet_truth_census_pt250"] = {"bb(nB>=2)": int((cls == 2).sum()), "b(nB=1)": int((cls == 1).sum()), "c(nC>=1,nB=0)": int((cls == -1).sum()), "light": int((cls == 0).sum())}
    r["frac_fatjet_with_top_contained(nWq=2,ntb=1)"] = float(ak.mean(ak.flatten((G["fj_nWq"][sel] == 2) & (G["fj_ntb"][sel] == 1)))) if ak.sum(sel) else None
    res[s] = r
    if fd:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
        os.makedirs(fd, exist_ok=True); fig, ax = plt.subplots(1, 3, figsize=(13, 3.6))
        allfj = ak.to_numpy(ak.flatten(sd[sel])); ax[0].hist(allfj, bins=np.linspace(0, 300, 31), histtype="step", label="all selected fat jets (m_SD)")
        if "fj_nHb" in G and ak.sum(sel & (G["fj_nHb"] == 2)) > 0: ax[0].hist(ak.to_numpy(ak.flatten(sd[sel & (G["fj_nHb"] == 2)])), bins=np.linspace(0, 300, 31), histtype="step", label="both H->bb b quarks inside")
        ax[0].set_xlabel("soft-drop mass [GeV]"); ax[0].legend(fontsize=7); ax[0].set_title(s, fontsize=8)
        ax[1].hist(ak.to_numpy(ak.flatten(fpt[sel])), bins=np.linspace(250, 1500, 26), histtype="step"); ax[1].set_xlabel("fat-jet pT [GeV]"); ax[1].set_yscale("log")
        ax[2].hist(M[M > 0], bins=np.linspace(0, 4000, 41), histtype="step"); ax[2].set_xlabel("m(jj) non-overlap AK5 leading pair [GeV]")
        fig.tight_layout(); fig.savefig(f"{fd}/val_{s}.png", dpi=110); fig.savefig(f"{fd}/val_{s}.pdf"); plt.close(fig)
json.dump(res, open(outj, "w"), indent=1, default=float); print("samples:", list(res))
# ---- preselection / window fractions for the sample-matrix feasibility estimate (appended, validation only)
