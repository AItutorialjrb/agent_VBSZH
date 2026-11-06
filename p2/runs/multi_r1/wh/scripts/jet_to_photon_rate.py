#!/usr/bin/env python3
"""Direct Delphes jet -> photon rate = the NOMINAL fake-photon model (D4/D-WH-2), v3 (recheck 2: parentage + reco-jet binning + split closure).
DENOMINATOR: GenJets (pT>25, |eta|<2.5) of events with GenTruth n_prompt_photons == 0, binned in GenJet pT and |eta| (barrel <1.5, endcap 1.5-2.5). Reco jets cannot be used: Delphes removes photon candidates from the Jet collection (checked: 0 of 12 reco photons lie within dR<0.2 of a reco jet, 9 of 12 within dR<0.2 of a GenJet). The pilots apply the rate to reco jet pT; the reco/gen jet pT mapping (mean and rms per bin) is stored in reco_over_gen_jet_pT_per_ptbin. NUMERATOR: a reco Photon (pT>10, |eta|<2.5, dR<0.2 to the jet), classified with the generator record (Particle branch of the *_full.root) by the best dR<0.1 status-1 gen photon:
  had   = a hadron (|pid|>100, not a proton/diquark) in the ancestry (pi0, eta, ... decays)            -> FAKE, in the numerator
  none  = no gen photon within dR<0.1 (calorimeter/merged object)                                       -> FAKE, in the numerator
  nonhad= no hadron ancestor (parton/lepton/boson parent: quark FSR/ISR photon, same definition as 'prompt' in slim_gentruth.py) -> REAL photon, EXCLUDED from the numerator (already modelled by the W gamma jj / W gamma gamma jj samples; excluding it avoids double counting)
Statistics: Clopper-Pearson 68 %. Classes W (W+jets) and TT (ttbar); nominal for W-dominated rows = rate_W, for ttbar rows = rate_TT, pooled = variant; process error = |r_W - r_TT|/2 (applies to the pooled variant).
Closure split: even/odd event index of each sample: rate from the even half, predicted matched count in the odd half vs observed per bin (and vice versa).
Usage: jet_to_photon_rate.py <out.json> <sample_dir:class> [...]   (dirs of test jobs, read-only: <tag>.root, <tag>_gen.root, <tag>_full.root)"""
import sys, json, glob, numpy as np, uproot, awkward as ak
from scipy.stats import beta
from scipy.optimize import minimize
out, specs = sys.argv[1], sys.argv[2:]
PT = [25, 35, 50, 75, 100, 150, 1000]; ETA = [(0, 1.5), (1.5, 2.5)]; XB = np.linspace(0, 1.5, 16); nb, ne = len(PT)-1, len(ETA)
def zer(): return np.zeros((ne, nb))
K = ("den", "num_fake", "num_had", "num_none", "num_nonhad", "num_all", "den_gen", "numg_all")
cnt = {c: {h: {k: zer() for k in K} for h in ("all", "even", "odd")} for c in ("W", "TT")}
ratio = [[] for _ in range(nb)]; xh = {c: np.zeros((nb, len(XB)-1)) for c in ("W", "TT")}; nev = {"W": 0, "TT": 0}; used = []
def dphi(a, b): return (a-b+np.pi) % (2*np.pi)-np.pi
for sp in specs:
    d, cls = sp.split(":")
    for f in sorted(glob.glob(d + "/*_full.root")):
        base = f[:-10]; used.append(base)
        npr = ak.to_numpy(uproot.open(base + "_gen.root")["GenTruth"]["n_prompt_photons"].array())
        T = uproot.open(f)["Delphes"]; i0 = 0
        for a in T.iterate(["Jet.PT", "Jet.Eta", "Jet.Phi", "GenJet.PT", "GenJet.Eta", "GenJet.Phi", "Photon.PT", "Photon.Eta", "Photon.Phi", "Particle.PID", "Particle.Status", "Particle.M1", "Particle.PT", "Particle.Eta", "Particle.Phi"], step_size=250, library="np"):
            n = len(a["Jet.PT"])
            for j in range(n):
                ie_ev = i0+j
                if npr[ie_ev] != 0: continue
                half = "even" if ie_ev % 2 == 0 else "odd"; nev[cls] += 1
                ph = [(q, e, p) for q, e, p in zip(a["Photon.PT"][j], a["Photon.Eta"][j], a["Photon.Phi"][j]) if q > 10 and abs(e) < 2.5]
                pid = a["Particle.PID"][j]; st = a["Particle.Status"][j]; m1 = a["Particle.M1"][j]
                gsel = [k for k in range(len(pid)) if st[k] == 1 and pid[k] == 22 and a["Particle.PT"][j][k] > 5]
                gph = [(a["Particle.Eta"][j][k], a["Particle.Phi"][j][k], a["Particle.PT"][j][k], k) for k in gsel]
                def origin(rp):
                    best = None
                    for ge, gp, gq, k in gph:
                        dr = np.hypot(rp[1]-ge, dphi(rp[2], gp))
                        if dr < 0.1 and (best is None or abs(gq-rp[0]) < abs(best[0]-rp[0])): best = (gq, k)
                    if best is None: return "none"
                    k = best[1]; steps = 0
                    while k >= 0 and steps < 400:
                        k = int(m1[k]); steps += 1
                        if k < 0: break
                        ap = abs(int(pid[k]))
                        if ap > 100 and ap != 2212 and not (ap > 1000 and (ap//10) % 10 == 0): return "had"
                    return "nonhad"
                for q, e, p in zip(a["GenJet.PT"][j], a["GenJet.Eta"][j], a["GenJet.Phi"][j]):
                    if q <= 25 or abs(e) >= 2.5: continue
                    ie = 0 if abs(e) < 1.5 else 1; ip = int(np.digitize(q, PT)-1)
                    if not 0 <= ip < nb: continue
                    m = [x for x in ph if np.hypot(e-x[1], dphi(p, x[2])) < 0.2]
                    for h in ("all", half): cnt[cls][h]["den"][ie, ip] += 1
                    if m:
                        lead = max(m, key=lambda z: z[0]); o = origin(lead)
                        for h in ("all", half):
                            cnt[cls][h]["num_all"][ie, ip] += 1; cnt[cls][h]["num_" + o][ie, ip] += 1
                            if o != "nonhad": cnt[cls][h]["num_fake"][ie, ip] += 1
                        if o != "nonhad": xh[cls][ip] += np.histogram([lead[0]/q], bins=XB)[0]
                for q, e, p in zip(a["GenJet.PT"][j], a["GenJet.Eta"][j], a["GenJet.Phi"][j]):   # reco/gen jet pT mapping (the rate is binned in GenJet pT and applied to reco jet pT)
                    if q <= 25 or abs(e) >= 2.5: continue
                    ip = int(np.digitize(q, PT)-1)
                    if not 0 <= ip < nb: continue
                    cand = [(np.hypot(e-e2, dphi(p, p2)), q2) for q2, e2, p2 in zip(a["Jet.PT"][j], a["Jet.Eta"][j], a["Jet.Phi"][j]) if np.hypot(e-e2, dphi(p, p2)) < 0.3]
                    if cand: ratio[ip].append(min(cand)[1]/q)
            i0 += n
def tot(h, k): return cnt["W"][h][k]+cnt["TT"][h][k]
def cp(k, n): return (float(beta.ppf(0.16, k, n-k+1)) if k > 0 else 0.0, float(beta.ppf(0.84, k+1, n-k)) if n else 1.0)
def rate(num, den): return np.where(den > 0, num/np.maximum(den, 1), 0.0)
def err(num, den): return np.array([[0.5*(cp(num[i, j], den[i, j])[1]-cp(num[i, j], den[i, j])[0]) for j in range(nb)] for i in range(ne)])
pooled = rate(tot("all", "num_fake"), tot("all", "den")); rW = rate(cnt["W"]["all"]["num_fake"], cnt["W"]["all"]["den"]); rT = rate(cnt["TT"]["all"]["num_fake"], cnt["TT"]["all"]["den"])
res = dict(note=__doc__.split("Usage")[0].strip(), rate_class_definitions={"W": "W+jets samples (class W above); nominal for the W-dominated rows F_*", "TT": "ttbar samples; nominal for the T_* rows", "pooled": "both; variant (key rate)"}, spec_classes=specs, files=used, n_events_no_prompt=nev, pt_edges=PT, eta_bins=ETA)
res["rate"] = pooled.tolist(); res["err_stat"] = err(tot("all", "num_fake"), tot("all", "den")).tolist()
res["rate_W"] = rW.tolist(); res["err_stat_W"] = err(cnt["W"]["all"]["num_fake"], cnt["W"]["all"]["den"]).tolist()
res["rate_TT"] = rT.tolist(); res["err_stat_TT"] = err(cnt["TT"]["all"]["num_fake"], cnt["TT"]["all"]["den"]).tolist()
res["err_process"] = (0.5*np.abs(rW-rT)).tolist(); res["err_total"] = np.sqrt(np.array(res["err_stat"])**2+np.array(res["err_process"])**2).tolist()
res["err_total_W"] = res["err_stat_W"]; res["err_total_TT"] = res["err_stat_TT"]   # class-specific nominal: stat error (the other class is the process variant)
for k in ("den", "num_fake", "num_had", "num_none", "num_nonhad", "num_all"): res[k] = tot("all", k).tolist(); res[k+"_W"] = cnt["W"]["all"][k].tolist(); res[k+"_TT"] = cnt["TT"]["all"][k].tolist()
res["rate_all_photons_incl_real_fsr"] = rate(tot("all", "num_all"), tot("all", "den")).tolist()
res["reco_over_gen_jet_pT_per_ptbin"] = [dict(n=len(r), mean=float(np.mean(r)) if r else None, rms=float(np.std(r)) if r else None) for r in ratio]
res["real_fsr_fraction_of_matched"] = float(tot("all", "num_nonhad").sum()/max(tot("all", "num_all").sum(), 1))
# closure on disjoint halves: rate from one half, predicted vs observed matched count in the other (per class pooled, per eta/pT bin)
clo = {}
for a_, b_ in (("even", "odd"), ("odd", "even")):
    r_a = rate(tot(a_, "num_fake"), tot(a_, "den")); pred = r_a*tot(b_, "den"); obs = tot(b_, "num_fake")
    sig = np.sqrt(np.maximum(pred, 1e-9)+ (tot(b_, "den")*np.array(err(tot(a_, "num_fake"), tot(a_, "den"))))**2)
    z = np.where(pred > 0, (obs-pred)/sig, 0.0); clo[f"measure_{a_}_test_{b_}"] = dict(pred=pred.tolist(), obs=obs.tolist(), pull=z.tolist(), chi2=float((z**2).sum()), ndof=int((tot(b_, "den") > 0).sum()))
res["closure_split"] = clo
XE = XB; res["x_edges"] = XB.tolist(); res["x_hist_per_ptbin"] = (xh["W"]+xh["TT"]).tolist(); res["x_hist_per_ptbin_W"] = xh["W"].tolist(); res["x_hist_per_ptbin_TT"] = xh["TT"].tolist()
pc = np.array([30, 42, 62, 87, 125, 220.0]); fit = {}
for ie in range(ne):
    num, den = tot("all", "num_fake")[ie], tot("all", "den")[ie]
    def nll(par):
        a_, b_ = par; mu = den*a_*(pc/50)**b_; return float(np.sum(mu-num*np.log(np.maximum(mu, 1e-300))))
    r = minimize(nll, [3e-3, 0.3], method="Nelder-Mead"); fit[("barrel", "endcap")[ie]] = dict(a=float(r.x[0]), b=float(r.x[1]))
res["powerlaw_fit_pooled_r_eq_a_pT_over_50_to_b"] = fit
res["assumed_form"] = [[1e-3*(c/50)**-0.5*(2 if ie else 1) for c in pc] for ie in range(ne)]
json.dump(res, open(out, "w"), indent=1)
print(json.dumps({k: res[k] for k in ("n_events_no_prompt", "den", "num_all", "num_had", "num_none", "num_nonhad", "rate", "rate_W", "rate_TT", "real_fsr_fraction_of_matched")}))
print("closure chi2/ndof:", {k: (round(v["chi2"], 1), v["ndof"]) for k, v in clo.items()})
