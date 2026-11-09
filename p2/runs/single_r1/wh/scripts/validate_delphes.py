#!/usr/bin/env python3
"""single_r1 WH Phase 03: Delphes-level validation of the condor test jobs (one per sample type).
For every wh/work/test/<sample>/<tag>.root (+ <tag>_gen.root GenTruth friend):
  * event counts, N_prompt_photons distribution (overlap partition input, 02 report §3)
  * ILLUSTRATIVE pre-declared WH baseline cutflow (NOT optimised; 02 report §5), sigma in fb BEFORE the sample's
    external BR factors (WF/BGG) — the BR ledger is applied only in xsec/N tables, never here
  * parametrised-fake pilots: j->gamma weights for 1-/2-fake samples, j->lepton weights for fake-lepton samples
For the signal (S_EW_WHjj) additionally: H->gg truth check, m_gg peak/resolution, photon & lepton efficiency,
MET resolution, mT, VBS-jet matching/response; figure wh/figures/p03_signal_validation.{png,pdf}.
Output: wh/work/p03/delphes_validation.json.   Usage: python3 -P wh/scripts/validate_delphes.py
"""
import os, sys, glob, json, numpy as np, awkward as ak, uproot
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_cards as MC
WH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
XS = json.load(open(f"{WH}/work/p03/xsec.json"))["xsec"]
# pre-declared fake scenarios (02 report §4; ZH-inherited, NOT data-driven)
FJG = lambda pt, eta: 1e-3 * (np.maximum(pt, 20) / 50.0) ** -0.5 * np.where(np.abs(eta) > 1.479, 2.0, 1.0)   # j->gamma, nominal
FL = {"low": 3e-5, "nom": 2e-4, "high": 1e-3}                                                              # j->lepton per jet
FJG_SCALE = {"low": 0.3, "nom": 1.0, "high": 3.0}
FE = {"low": 0.01, "nom": 0.02, "high": 0.05}                                                             # e->gamma

def dphi(a, b): return (a - b + np.pi) % (2 * np.pi) - np.pi
def dR(e1, p1, e2, p2): return np.hypot(e1 - e2, dphi(p1, p2))

def load(f):
    t = uproot.open(f)["Delphes"]; g = uproot.open(f.replace(".root", "_gen.root"))["GenTruth"]
    A = lambda k: t[k].array()
    o = lambda n, ex=(): ak.zip({k.lower(): A(f"{n}/{n}.{k}") for k in ("PT", "Eta", "Phi") + ex})
    ev = dict(w=ak.to_numpy(A("Event/Event.Weight")[:, 0]), ph=o("Photon"), el=o("Electron", ("Charge",)), mu=o("Muon", ("Charge",)),
              jet=o("Jet", ("Mass", "BTag")), gjet=o("GenJet"), met=ak.to_numpy(A("MissingET/MissingET.MET")[:, 0]),
              metphi=ak.to_numpy(A("MissingET/MissingET.Phi")[:, 0]), gmet=ak.to_numpy(A("GenMissingET/GenMissingET.MET")[:, 0]),
              gmetphi=ak.to_numpy(A("GenMissingET/GenMissingET.Phi")[:, 0]))
    ev["gen"] = g.arrays(); return ev

def p4sum_m(o1, o2, m1=0., m2=0.):
    def comp(o, m):
        px, py, pz = o.pt * np.cos(o.phi), o.pt * np.sin(o.phi), o.pt * np.sinh(o.eta)
        return px, py, pz, np.sqrt(px**2 + py**2 + pz**2 + m**2)
    a, b = comp(o1, m1), comp(o2, m2)
    s = [a[i] + b[i] for i in range(4)]
    return np.sqrt(np.maximum(s[3]**2 - s[0]**2 - s[1]**2 - s[2]**2, 0))

def select(ev, fake=None, scen="nom"):
    """Illustrative WH baseline. fake=None (genuine objects) | 'g1' (1 j->gamma) | 'g2' (2 j->gamma) | 'l' (1 j->lepton).
    Returns per-event weight multipliers (array) for each cutflow step."""
    n = len(ev["w"]); ph, el, mu, jet = ev["ph"], ev["el"], ev["mu"], ev["jet"]
    ph = ph[(ph.pt > 20) & (np.abs(ph.eta) < 2.5) & ~((np.abs(ph.eta) > 1.4442) & (np.abs(ph.eta) < 1.566))]
    lep = ak.concatenate([el[(el.pt > 10) & (np.abs(el.eta) < 2.5)], mu[(mu.pt > 10) & (np.abs(mu.eta) < 2.4)]], axis=1)
    lep = lep[ak.argsort(lep.pt, ascending=False)]
    jets = jet[(jet.pt > 30) & (np.abs(jet.eta) < 4.7)]
    steps = {}; mult = np.ones(n)
    rows = []
    for i in range(n):
        P = list(zip(ak.to_list(ph.pt[i]), ak.to_list(ph.eta[i]), ak.to_list(ph.phi[i])))
        L = list(zip(ak.to_list(lep.pt[i]), ak.to_list(lep.eta[i]), ak.to_list(lep.phi[i])))
        J = list(zip(ak.to_list(jets.pt[i]), ak.to_list(jets.eta[i]), ak.to_list(jets.phi[i]), ak.to_list(jets.btag[i])))
        J = [j for j in J if all(dR(j[1], j[2], p[1], p[2]) > 0.4 for p in P) and all(dR(j[1], j[2], l[1], l[2]) > 0.4 for l in L)]
        # enumerate fake assignments: (weight, photons, leptons, jets)
        cands = []
        if fake is None: cands = [(1.0, P, L, J)]
        elif fake in ("g1", "g2"):
            k = 1 if fake == "g1" else 2; s = FJG_SCALE[scen]
            elig = [j for j in J if abs(j[1]) < 2.5]
            import itertools
            for comb in itertools.combinations(range(len(elig)), k):
                fw = np.prod([s * FJG(elig[c][0], elig[c][1]) for c in comb])
                fph = [(0.85 * elig[c][0], elig[c][1], elig[c][2]) for c in comb]
                cands.append((fw, sorted(P + fph, reverse=True), L, [j for jj, j in enumerate(elig) if jj not in comb] + [j for j in J if abs(j[1]) >= 2.5]))
        elif fake == "l":
            for c, j in enumerate(J):
                if abs(j[1]) < 2.4 and j[0] > 25:
                    cands.append((FL[scen], P, sorted(L + [(0.6 * j[0], j[1], j[2])], reverse=True), [x for xx, x in enumerate(J) if xx != c]))
        elif fake == "e":   # e->gamma (02 §3 rule 6): drop Delphes photons near a prompt gen electron, then promote reco e
            g = ev["gen"]; ge = [(e, p) for e, p, pid, pr in zip(ak.to_list(g["glep_eta"][i]), ak.to_list(g["glep_phi"][i]),
                                                               ak.to_list(g["glep_pid"][i]), ak.to_list(g["glep_prompt"][i])) if abs(pid) == 11 and pr]
            P2 = [p for p in P if all(dR(p[1], p[2], e, f) > 0.1 for e, f in ge)]
            E = [(a, b, c) for a, b, c in zip(ak.to_list(el.pt[i]), ak.to_list(el.eta[i]), ak.to_list(el.phi[i])) if a > 20 and abs(b) < 2.5]
            for e in E:
                Lr = [l for l in L if not (abs(l[0] - e[0]) < 1e-6 and abs(l[1] - e[1]) < 1e-6)]
                cands.append((FE[scen], sorted(P2 + [e], reverse=True), Lr, J))
        rows.append((cands, ev["met"][i]))
    names = ["all", ">=2 gamma", "pT/m_gg & 105<m_gg<160", "1 lepton pT>25 (veto 2nd>10)", "MET>30", ">=2 jets", "m_jj>500 & |deta|>2.5", "b-veto", "120<m_gg<130"]
    W = np.zeros((n, len(names)))
    for i, (cands, met) in enumerate(rows):
        W[i, 0] = 1.0
        acc = np.zeros(len(names))
        for fw, P, L, J in cands:
            if len(P) < 2: continue
            p1, p2 = P[0], P[1]
            m = float(p4sum_m(ak.Record(dict(pt=p1[0], eta=p1[1], phi=p1[2])), ak.Record(dict(pt=p2[0], eta=p2[1], phi=p2[2]))))
            c = [True, True, (105 < m < 160) and p1[0] / m > 1 / 3 and p2[0] / m > 1 / 4,
                 len(L) >= 1 and L[0][0] > 25 and (len(L) < 2 or L[1][0] < 10), met > 30, len(J) >= 2]
            if len(J) >= 2:
                j1, j2 = J[0], J[1]
                mjj = float(p4sum_m(ak.Record(dict(pt=j1[0], eta=j1[1], phi=j1[2])), ak.Record(dict(pt=j2[0], eta=j2[1], phi=j2[2]))))
                c += [mjj > 500 and abs(j1[1] - j2[1]) > 2.5, not any(j[3] > 0 and abs(j[1]) < 2.5 for j in J), 120 < m < 130]
            else: c += [False, False, False]
            ok = True
            for k in range(1, len(names)):
                ok = ok and c[k]
                if ok: acc[k] += fw
        W[i, 1:] = acc[1:]
    return names, W

def cutflow(ev, sigma_fb, **kw):
    names, W = select(ev, **kw); w = ev["w"] / ev["w"].sum() * sigma_fb
    out = []
    for k, nm in enumerate(names):
        x = W[:, k] * w
        out.append(dict(step=nm, sigma_fb=float(x.sum()), err_fb=float(np.sqrt((x**2).sum())), n_mc=int((W[:, k] > 0).sum())))
    return out

def signal_validation(ev):
    g = ev["gen"]; R = {}
    R["H_last_copy_present"] = float(np.mean(ak.to_numpy(g["gH_pt"]) > -999))
    R["n_prompt_photons_ge2_frac"] = float(np.mean(ak.to_numpy(g["n_prompt_photons"]) >= 2))
    # m_gg of two leading reco photons
    ph = ev["ph"][(ev["ph"].pt > 20) & (np.abs(ev["ph"].eta) < 2.5)]
    has2 = ak.to_numpy(ak.num(ph) >= 2); p = ph[has2]
    mgg = ak.to_numpy(p4sum_m(p[:, 0], p[:, 1])); win = mgg[(mgg > 110) & (mgg < 140)]
    q16, q50, q84 = np.percentile(win, [16, 50, 84])
    R["mgg"] = dict(n2ph=int(has2.sum()), frac_2ph=float(np.mean(has2)), median=float(q50), half68=float((q84 - q16) / 2),
                    frac_120_130=float(np.mean((mgg > 120) & (mgg < 130))))
    # photon efficiency: prompt gen photons pT>25, |eta|<2.5 (excl. crack), matched dR<0.1 to reco photon
    def eff(gpt, geta, gphi, gok, reco, label, bins):
        res = {}
        for lo, hi in bins:
            sel = gok & (np.abs(geta) >= lo) & (np.abs(geta) < hi)
            gp = ak.zip(dict(eta=geta[sel], phi=gphi[sel]))
            pairs = ak.cartesian([gp, reco], nested=True)
            a, b = ak.unzip(pairs)
            matched = ak.any(dR(a.eta, a.phi, b.eta, b.phi) < 0.1, axis=2)
            ntot = int(ak.sum(ak.num(gp))); nm = int(ak.sum(matched))
            res[f"{label} |eta| {lo}-{hi}"] = dict(n_gen=ntot, eff=nm / ntot if ntot else None, err=(np.sqrt(nm * (ntot - nm) / ntot) / ntot) if ntot else None)
        return res
    gok = g["gph_prompt"] & (g["gph_pt"] > 25)
    R["photon_eff"] = eff(g["gph_pt"], g["gph_eta"], g["gph_phi"], gok, ev["ph"], "photon", [(0, 1.4442), (1.566, 2.5)])
    for fl, pidv, reco in (("electron", 11, ev["el"]), ("muon", 13, ev["mu"])):
        lok = g["glep_prompt"] & (g["glep_pt"] > 25) & (abs(g["glep_pid"]) == pidv)
        R[f"{fl}_eff"] = eff(g["glep_pt"], g["glep_eta"], g["glep_phi"], lok, reco, fl, [(0, 1.479), (1.479, 2.4)])
    # W charge from leading prompt gen lepton
    lp = g["glep_pid"][g["glep_prompt"] & (g["glep_pt"] > 5)]; lead = ak.firsts(lp)
    R["W_charge_frac_plus"] = float(np.mean(ak.to_numpy(ak.fill_none(lead, 0)) < 0))   # l+ has negative PDG id
    R["flavour_frac_e"] = float(np.mean(np.abs(ak.to_numpy(ak.fill_none(lead, 0))) == 11))
    # MET resolution
    dx = ev["met"] * np.cos(ev["metphi"]) - ev["gmet"] * np.cos(ev["gmetphi"]); dy = ev["met"] * np.sin(ev["metphi"]) - ev["gmet"] * np.sin(ev["gmetphi"])
    q = np.percentile(np.concatenate([dx, dy]), [16, 50, 84])
    sel = ev["gmet"] > 30
    R["met"] = dict(sigma_xy_half68=float((q[2] - q[0]) / 2), bias_xy=float(q[1]), response_median=float(np.median(ev["met"][sel] / ev["gmet"][sel])),
                    gen_met_median=float(np.median(ev["gmet"])), frac_met_gt30=float(np.mean(ev["met"] > 30)))
    # VBS jets: two leading reco jets (pT>30) matched to GenJets
    jets = ev["jet"][(ev["jet"].pt > 30) & (np.abs(ev["jet"].eta) < 4.7)]; h2 = ak.to_numpy(ak.num(jets) >= 2); j = jets[h2]
    gj = ev["gjet"][h2]
    pairs = ak.cartesian([j[:, :2], gj], nested=True); a, b = ak.unzip(pairs); d = dR(a.eta, a.phi, b.eta, b.phi)
    best = ak.argmin(d, axis=2, keepdims=True); dmin = ak.flatten(ak.min(d, axis=2)); gpt = ak.flatten(ak.flatten(b.pt[best], axis=2))
    m = ak.to_numpy(dmin < 0.3); resp = ak.to_numpy(ak.flatten(j[:, :2].pt))[m] / ak.to_numpy(gpt)[m]
    mjj = ak.to_numpy(p4sum_m(j[:, 0], j[:, 1], j[:, 0].mass, j[:, 1].mass)); deta = np.abs(ak.to_numpy(j[:, 0].eta - j[:, 1].eta))
    r = np.percentile(resp, [16, 50, 84])
    R["jets"] = dict(frac_ge2=float(np.mean(h2)), match_frac=float(np.mean(m)), pt_response_median=float(r[1]), pt_response_half68=float((r[2] - r[0]) / 2),
                     mjj_median=float(np.median(mjj)), frac_mjj500=float(np.mean(mjj > 500)), deta_median=float(np.median(deta)))
    # mT(lepton, MET)
    lep = ak.concatenate([ev["el"], ev["mu"]], axis=1); lep = lep[ak.argsort(lep.pt, ascending=False)]; h1 = ak.num(lep) >= 1
    l1 = ak.firsts(lep[h1]); mt = np.sqrt(2 * ak.to_numpy(l1.pt) * ev["met"][ak.to_numpy(h1)] * (1 - np.cos(ak.to_numpy(l1.phi) - ev["metphi"][ak.to_numpy(h1)])))
    R["mT"] = dict(median=float(np.median(mt)), frac_lt100=float(np.mean(mt < 100)))
    return R, dict(mgg=mgg, dx=np.concatenate([dx, dy]), mt=mt, mjj=mjj, deta=deta, resp=resp)

def figure(H):
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    C1, INK, MUTED = "#2a78d6", "#0b0b0b", "#52514e"
    plt.rcParams.update({"font.size": 9, "axes.edgecolor": MUTED, "axes.labelcolor": INK, "xtick.color": MUTED, "ytick.color": MUTED,
                         "axes.spines.top": False, "axes.spines.right": False})
    fig, ax = plt.subplots(2, 3, figsize=(11, 6.2))
    spec = [("mgg", np.linspace(110, 140, 61), r"$m_{\gamma\gamma}$ (two leading reco photons) [GeV]"),
            ("dx", np.linspace(-80, 80, 81), r"$E_{T,x/y}^{miss}$ reco $-$ gen [GeV]"),
            ("mt", np.linspace(0, 200, 51), r"$m_T(\ell, E_T^{miss})$ [GeV]"),
            ("mjj", np.linspace(0, 3000, 61), r"$m_{jj}$ (two leading jets) [GeV]"),
            ("deta", np.linspace(0, 9, 46), r"$|\Delta\eta_{jj}|$"),
            ("resp", np.linspace(0.4, 1.6, 61), r"tag-jet $p_T^{reco}/p_T^{gen}$ (matched $\Delta R<0.3$)")]
    for a, (k, b, lab) in zip(ax.flat, spec):
        a.hist(np.clip(H[k], b[0], b[-1]), bins=b, histtype="step", lw=1.6, color=C1)
        a.set_xlabel(lab); a.set_ylabel("MC events"); a.grid(alpha=0.25, lw=0.5)
    fig.suptitle("EW W±Hjj (W→eν/μν, H→γγ), single_r1 Phase-03 test job, Delphes CMS slim_v1 — unweighted MC counts", color=INK, fontsize=10)
    fig.tight_layout()
    for e in ("png", "pdf"): fig.savefig(f"{WH}/figures/p03_signal_validation.{e}", dpi=130)

def main():
    J = f"{WH}/work/p03/delphes_validation.json"
    out = json.load(open(J)) if os.path.exists(J) and not os.environ.get("FORCE") else {}   # cache: skip samples already done
    roles = {s["name"]: s["role"] for s in MC.S}
    for d in sorted(glob.glob(f"{WH}/work/test/*/")):
        name = os.path.basename(d.rstrip("/")); files = [f for f in glob.glob(f"{d}/*.root") if not f.endswith(("_gen.root", "_full.root"))]
        if not files or name not in XS or "sigma_fb" not in XS[name]: continue
        if name in out and out[name].get("file") == os.path.relpath(files[0], WH): continue
        ev = load(files[0]); sig = XS[name]["sigma_fb"]; role = roles[name]
        npg = ak.to_numpy(ev["gen"]["n_prompt_photons"])
        R = dict(file=os.path.relpath(files[0], WH), n_events=len(ev["w"]), sigma_fb_gridpack=sig,
                 weights_constant=bool(np.allclose(ev["w"], ev["w"][0])), n_prompt_photons={int(k): int((npg == k).sum()) for k in np.unique(npg)})
        R["cutflow_genuine"] = cutflow(ev, sig)
        if role in ("fake1_bkg",): R["cutflow_fake_g1_nom"] = cutflow(ev, sig, fake="g1")
        if role in ("fake2_bound",):
            for sc in FJG_SCALE: R[f"cutflow_fake_g2_{sc}"] = cutflow(ev, sig, fake="g2", scen=sc)
        if role in ("fakelep_bkg",):
            for sc in FL: R[f"cutflow_fake_l_{sc}"] = cutflow(ev, sig, fake="l", scen=sc)
        if name == "S_EW_WHjj":
            R["signal_validation"], H = signal_validation(ev); figure(H)
        out[name] = R; print(name, R["n_events"], R["cutflow_genuine"][-1])
        json.dump(out, open(J, "w"), indent=1)

if __name__ == "__main__":
    main()
