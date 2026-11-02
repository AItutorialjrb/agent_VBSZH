#!/usr/bin/env python3
"""Phase 03 smoke validation of a Delphes (CMS card) file: gen H->gamma gamma closure and reco objects.
Usage: python3 -I smoke_analysis.py <delphes.root> <sigma_fb_of_input> <outdir>
Prints/writes JSON with event-count cutflow (unweighted & weighted) and object checks. Not an analysis selection."""
import sys, json, os
import numpy as np, uproot, awkward as ak

fn, sigma_fb, outdir = sys.argv[1], float(sys.argv[2]), sys.argv[3]
os.makedirs(outdir, exist_ok=True)
t = uproot.open(fn)["Delphes"]
w = ak.to_numpy(t["Event/Event.Weight"].array()[:, 0])
N = len(w)
arr = lambda k: t[k].array()
pid, d1, d2 = arr("Particle/Particle.PID"), arr("Particle/Particle.D1"), arr("Particle/Particle.D2")
# gen H closure: last-copy H (daughters not H) must decay to exactly gamma gamma
nH_aa = 0; nH = 0; nother = 0
for p, a, b in zip(pid, d1, d2):
    p = ak.to_numpy(p); a = ak.to_numpy(a); b = ak.to_numpy(b)
    for i in np.where(p == 25)[0]:
        if a[i] < 0: continue
        dau = [p[k] for k in range(a[i], b[i] + 1)] if b[i] >= a[i] else [p[a[i]]]
        if 25 in dau: continue
        nH += 1
        if sorted(dau) == [22, 22]: nH_aa += 1
        else: nother += 1

def obj(name, extra=()):
    return {v: arr(f"{name}/{name}.{v}") for v in ("PT", "Eta", "Phi") + tuple(extra)}

ph = obj("Photon", ("E",)); el = obj("Electron", ("Charge",)); mu = obj("Muon", ("Charge",)); jt = obj("Jet", ("Mass", "BTag"))
def p4(o, m=0.0, mass=None):
    pt, eta, phi = o["PT"], o["Eta"], o["Phi"]
    mm = mass if mass is not None else m
    px, py, pz = pt * np.cos(phi), pt * np.sin(phi), pt * np.sinh(eta)
    e = np.sqrt(px**2 + py**2 + pz**2 + mm**2)
    return px, py, pz, e
def minv(a, b):
    px, py, pz, e = (a[i] + b[i] for i in range(4))
    return np.sqrt(np.maximum(e**2 - px**2 - py**2 - pz**2, 0))

# photons: pT>20, |eta|<2.5 excl. 1.4442-1.566
gsel = (ph["PT"] > 20) & (abs(ph["Eta"]) < 2.5) & ~((abs(ph["Eta"]) > 1.4442) & (abs(ph["Eta"]) < 1.566))
P = {k: v[gsel] for k, v in ph.items()}
c_2g = ak.num(P["PT"]) >= 2
lsel_e = (el["PT"] > 15) & (abs(el["Eta"]) < 2.5); lsel_m = (mu["PT"] > 15) & (abs(mu["Eta"]) < 2.4)
E = {k: v[lsel_e] for k, v in el.items()}; M = {k: v[lsel_m] for k, v in mu.items()}
jsel = (jt["PT"] > 25) & (abs(jt["Eta"]) < 4.7); J = {k: v[jsel] for k, v in jt.items()}
c_2j = ak.num(J["PT"]) >= 2
def pair(o, m):
    ok = ak.num(o["PT"]) >= 2
    f = lambda v: ak.to_numpy(ak.fill_none(ak.pad_none(v, 2)[:, :2], 0.0))
    pt, eta, phi = f(o["PT"]), f(o["Eta"]), f(o["Phi"])
    a = p4({"PT": pt[:, 0], "Eta": eta[:, 0], "Phi": phi[:, 0]}, m); b = p4({"PT": pt[:, 1], "Eta": eta[:, 1], "Phi": phi[:, 1]}, m)
    return ak.to_numpy(ok), minv(a, b), pt, eta
okg, mgg, ptg, etag = pair(P, 0.0)
oke, mee, _, _ = pair(E, 0.000511); okm, mmm, _, _ = pair(M, 0.1057)
qe = ak.to_numpy(ak.fill_none(ak.pad_none(E["Charge"], 2)[:, :2], 0)); qm = ak.to_numpy(ak.fill_none(ak.pad_none(M["Charge"], 2)[:, :2], 0))
os_e = oke & (qe[:, 0] * qe[:, 1] < 0); os_m = okm & (qm[:, 0] * qm[:, 1] < 0)
mll = np.where(os_e, mee, np.where(os_m, mmm, 0.0)); c_ll = os_e | os_m
okj, mjj, ptj, etaj = pair(J, 0.0)
detajj = np.abs(etaj[:, 0] - etaj[:, 1])
c_z = c_ll & (mll > 70) & (mll < 110)  # loose validation window, not the analysis cut
c_g = ak.to_numpy(c_2g); c_j = ak.to_numpy(c_2j)
steps = [("all", np.ones(N, bool)), (">=2 photons pT>20", c_g), ("+OSSF ll pT>15", c_g & c_ll),
         ("+70<mll<110", c_g & c_z), ("+>=2 jets pT>25", c_g & c_z & c_j),
         ("+mjj>500 & |deta|>2.5 (illustrative)", c_g & c_z & c_j & (mjj > 500) & (detajj > 2.5))]
sw = w.sum()
cut = [{"step": s, "n": int(m.sum()), "frac_w": float(w[m].sum() / sw), "sigma_fb": float(sigma_fb * w[m].sum() / sw),
        "sigma_err_fb": float(sigma_fb * np.sqrt((w[m] ** 2).sum()) / sw)} for s, m in steps]
m_ok = mgg[c_g]
core = m_ok[(m_ok > 110) & (m_ok < 140)]
q16, q50, q84 = np.percentile(core, [16, 50, 84]) if len(core) else (0, 0, 0)
res = {"file": fn, "N": N, "sum_w": float(sw), "gen_H_last_copies": nH, "gen_H_to_aa": nH_aa, "gen_H_other": nother,
       "n_photon_mean": float(ak.mean(ak.num(ph["PT"]))), "n_electron_ossf": int(os_e.sum()), "n_muon_ossf": int(os_m.sum()),
       "mgg_median_110_140": float(q50), "mgg_halfwidth68": float((q84 - q16) / 2), "mgg_frac_in_120_130": float(((m_ok > 120) & (m_ok < 130)).sum() / max(len(m_ok), 1)),
       "mll_median_os": float(np.median(mll[c_ll])) if c_ll.any() else 0, "mjj_median_2j": float(np.median(mjj[c_j])) if c_j.any() else 0,
       "frac_mjj_gt500_given2j": float((mjj[c_j] > 500).mean()) if c_j.any() else 0,
       "frac_mjj_60_110_given2j": float(((mjj[c_j] > 60) & (mjj[c_j] < 110)).mean()) if c_j.any() else 0,
       "nbtag_mean_selected_jets": float(ak.mean(ak.sum(J["BTag"] > 0, axis=1))), "cutflow": cut}
json.dump(res, open(os.path.join(outdir, "smoke_summary.json"), "w"), indent=1)
try:
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 3, figsize=(13, 3.6))
    ax[0].hist(m_ok, bins=60, range=(100, 150)); ax[0].set_xlabel("m_gg [GeV] (>=2 photons)")
    ax[1].hist(mll[c_ll], bins=50, range=(50, 130)); ax[1].set_xlabel("m_ll [GeV] (OSSF)")
    ax[2].hist(mjj[c_j], bins=50, range=(0, 3000)); ax[2].set_xlabel("m_jj [GeV] (>=2 jets)")
    for a in ax: a.set_ylabel("events (unweighted MC)")
    fig.suptitle(os.path.basename(fn) + " — smoke test, not a result"); fig.tight_layout(); fig.savefig(os.path.join(outdir, "smoke_validation.png"), dpi=90)
except Exception as e:
    print("plot skipped:", e)
print(json.dumps({k: v for k, v in res.items() if k != "cutflow"}, indent=0))
for c in cut: print(f"{c['step']:40s} n={c['n']:5d}  sigma={c['sigma_fb']:.4g} +- {c['sigma_err_fb']:.2g} fb")
