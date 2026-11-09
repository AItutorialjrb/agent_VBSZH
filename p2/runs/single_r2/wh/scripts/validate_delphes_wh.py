#!/usr/bin/env python3
"""Phase-03 Delphes object validation for WH (single_r2).  VALIDATION ONLY - not a yield, not an optimised selection.
Usage: python3 -P validate_delphes_wh.py <delphes.root (with Particle)> <sigma_fb_before_ext_BR> <out_prefix> [label]
Writes <out_prefix>.json and <out_prefix>.png.
Truth: last-copy H daughters, W -> l nu flavour/charge.  Objects: photons, leptons, jets, MET (reco vs GenMissingET and vs
truth neutrino sum).  m_gg Gaussian-core fit.  Illustrative smoke cutflow with weighted MC errors (sigma before B_gg/WF)."""
import sys, json, math
import numpy as np, uproot, awkward as ak

fn, sig_fb, outp = sys.argv[1], float(sys.argv[2]), sys.argv[3]
label = sys.argv[4] if len(sys.argv) > 4 else outp
t = uproot.open(fn)["Delphes"]
N = t.num_entries
br = lambda *names: t.arrays(list(names), library="ak")

res = dict(file=fn, n_events=N, sigma_fb_input=sig_fb, label=label)
# ---------------- truth (Particle branch)
P = br("Particle.PID", "Particle.Status", "Particle.M1", "Particle.D1", "Particle.D2", "Particle.PT", "Particle.Eta", "Particle.Phi")
pid, st = P["Particle.PID"], P["Particle.Status"]
d1, d2 = P["Particle.D1"], P["Particle.D2"]
nH_gg = nH_other = nH_none = 0
nW = {"e": 0, "mu": 0, "tau": 0, "none": 0, "had": 0}  # had = events with a hadronic W/Z resonance in the record
gen_acc = np.zeros(N, bool)
qW = {"+": 0, "-": 0}
nu_px = np.zeros(N); nu_py = np.zeros(N)
for i in range(N):
    p = np.asarray(pid[i]); a1 = np.asarray(d1[i]); a2 = np.asarray(d2[i]); s = np.asarray(st[i])
    # last-copy H: PID 25 whose daughters are not a 25
    hs = [k for k in np.where(p == 25)[0] if a1[k] >= 0 and p[a1[k]] != 25]
    if not hs: nH_none += 1
    else:
        k = hs[-1]; ds = sorted({int(p[x]) for x in range(a1[k], max(a1[k], a2[k]) + 1)})
        if ds == [22]: nH_gg += 1
        else: nH_other += 1
    # W/Z resonances (last copies). Leptonic W = W with an e/mu/tau daughter; hadronic V = W/Z with quark daughters
    # (MG5 writes s-channel resonances, e.g. Higgsstrahlung-like W(->jj)WH topologies, into the LHE)
    lepW = None; hadV = False
    for k in np.where(np.isin(np.abs(p), [23, 24]))[0]:
        if a1[k] < 0 or abs(p[a1[k]]) in (23, 24): continue
        ds = {abs(int(p[x])) for x in range(a1[k], max(a1[k], a2[k]) + 1)}
        if abs(p[k]) == 24 and ds & {11, 13, 15} and lepW is None: lepW = (k, ds)
        elif ds and max(ds) <= 5: hadV = True
    if lepW is None: nW["none"] += 1
    else:
        k, ds = lepW; qW["+" if p[k] > 0 else "-"] += 1
        nW["e" if 11 in ds else "mu" if 13 in ds else "tau"] += 1
    nW["had"] += int(hadV)
    # generator charged lepton (status 1 e/mu, |eta|<2.5, pT>15) from the leptonic W (mother chain not needed: only one prompt lepton)
    ptl, etl = np.asarray(P["Particle.PT"][i]), np.asarray(P["Particle.Eta"][i]); m1 = np.asarray(P["Particle.M1"][i])
    cand = [x for x in np.where((s == 1) & np.isin(np.abs(p), [11, 13]))[0] if m1[x] >= 0 and abs(p[m1[x]]) in (11, 13, 24)]
    gen_acc[i] = any(ptl[x] > 15 and abs(etl[x]) < 2.5 for x in cand)
    # prompt-neutrino sum (final-state neutrinos, status 1)
    nus = np.where((s == 1) & np.isin(np.abs(p), [12, 14, 16]))[0]
    pt, ph = np.asarray(P["Particle.PT"][i])[nus], np.asarray(P["Particle.Phi"][i])[nus]
    nu_px[i] = np.sum(pt*np.cos(ph)); nu_py[i] = np.sum(pt*np.sin(ph))
res["truth"] = dict(H_to_gg=nH_gg, H_other=nH_other, no_H=nH_none, W_decay=nW, W_charge=qW, n_gen_lep_in_acc=int(gen_acc.sum()))

# ---------------- objects
O = br("Photon.PT", "Photon.Eta", "Photon.Phi", "Photon.E", "Electron.PT", "Electron.Eta", "Electron.Phi", "Electron.Charge",
       "Muon.PT", "Muon.Eta", "Muon.Phi", "Muon.Charge", "Jet.PT", "Jet.Eta", "Jet.Phi", "Jet.Mass", "Jet.BTag",
       "MissingET.MET", "MissingET.Phi", "GenMissingET.MET", "GenMissingET.Phi", "Event.Weight")
w = ak.to_numpy(ak.firsts(O["Event.Weight"]))
res["weights"] = dict(sum_w=float(w.sum()), unique=sorted(set(np.round(w, 12).tolist()))[:5], n_negative=int((w < 0).sum()))
wn = sig_fb/N*np.ones(N)  # unweighted LO sample: each event = sigma/N

def vec(pt, eta, phi, m=0.0):
    px, py, pz = pt*np.cos(phi), pt*np.sin(phi), pt*np.sinh(eta); e = np.sqrt(px**2 + py**2 + pz**2 + m**2); return px, py, pz, e
def minv(a, b):
    px, py, pz, e = (a[i] + b[i] for i in range(4)); return np.sqrt(np.maximum(e**2 - px**2 - py**2 - pz**2, 0))

gpt, geta, gphi = O["Photon.PT"], O["Photon.Eta"], O["Photon.Phi"]
gsel = (gpt > 20) & (abs(geta) < 2.5) & ~((abs(geta) > 1.4442) & (abs(geta) < 1.566))
gpt, geta, gphi = gpt[gsel], geta[gsel], gphi[gsel]
ng = ak.to_numpy(ak.num(gpt))
esel = (O["Electron.PT"] > 15) & (abs(O["Electron.Eta"]) < 2.5); msel = (O["Muon.PT"] > 15) & (abs(O["Muon.Eta"]) < 2.5)
ne, nm = ak.to_numpy(ak.sum(esel, axis=1)), ak.to_numpy(ak.sum(msel, axis=1))
nl = ne + nm
lpt_all = ak.concatenate([O["Electron.PT"][esel], O["Muon.PT"][msel]], axis=1)
lead_lpt = ak.to_numpy(ak.fill_none(ak.max(lpt_all, axis=1), 0))
jsel = (O["Jet.PT"] > 25) & (abs(O["Jet.Eta"]) < 4.7)
jpt, jeta, jphi, jm, jb = (O[k][jsel] for k in ("Jet.PT", "Jet.Eta", "Jet.Phi", "Jet.Mass", "Jet.BTag"))
nj = ak.to_numpy(ak.num(jpt)); nb = ak.to_numpy(ak.sum(jb[abs(jeta) < 2.5] > 0, axis=1))
met = ak.to_numpy(ak.firsts(O["MissingET.MET"])); metphi = ak.to_numpy(ak.firsts(O["MissingET.Phi"]))
gmet = ak.to_numpy(ak.firsts(O["GenMissingET.MET"])); gmetphi = ak.to_numpy(ak.firsts(O["GenMissingET.Phi"]))

# mgg (two leading photons)
two = ng >= 2
g1 = vec(*(ak.to_numpy(ak.pad_none(x, 2)[:, 0][two]) for x in (gpt, geta, gphi)))
g2 = vec(*(ak.to_numpy(ak.pad_none(x, 2)[:, 1][two]) for x in (gpt, geta, gphi)))
mgg = minv(g1, g2)
mggw = mgg[(mgg > 110) & (mgg < 140)]
def core_fit(x, lo=115, hi=135, it=5):
    mu, s = np.median(x), np.std(x[(x > lo) & (x < hi)])
    for _ in range(it):
        sel = abs(x - mu) < 2*s; mu, s = x[sel].mean(), x[sel].std()/0.8796  # truncated-Gaussian (±2σ) correction
    return float(mu), float(s)
q16, q50, q84 = np.percentile(mggw, [16, 50, 84]) if len(mggw) > 10 else (np.nan,)*3
mu, sg = core_fit(mggw) if len(mggw) > 50 else (np.nan, np.nan)
res["mgg"] = dict(n_2g=int(two.sum()), median=float(q50), half_width_68=float((q84 - q16)/2), core_mu=mu, core_sigma=sg,
                  frac_120_130=float(((mgg > 120) & (mgg < 130)).mean()) if two.sum() else None)
# MET resolution: reco vs GenMissingET (= Delphes truth invisible sum) and GenMET vs status-1 neutrino sum (closure)
dmx = met*np.cos(metphi) - gmet*np.cos(gmetphi); dmy = met*np.sin(metphi) - gmet*np.sin(gmetphi)
nu_pt = np.hypot(nu_px, nu_py)
def s68(x): a, b = np.percentile(x, [16, 84]); return float((b - a)/2)
res["met"] = dict(genmet_vs_nusum_median_abs_diff=float(np.median(abs(gmet - nu_pt))), reco_minus_gen_median=float(np.median(met - gmet)),
                  sigma68_dmetx=s68(dmx), sigma68_dmety=s68(dmy), rms_dmetx=float(np.std(dmx)),
                  rel_res68_genmet_gt50=s68((met - gmet)[gmet > 50]/gmet[gmet > 50]) if (gmet > 50).sum() > 20 else None,
                  median_genmet=float(np.median(gmet)), median_met=float(np.median(met)))
# leptons: efficiency for truth W->e/mu with gen lepton in acceptance
res["leptons"] = dict(n_1lep=int((nl == 1).sum()), n_ge1lep=int((nl >= 1).sum()), n_e=int(ne.sum()), n_mu=int(nm.sum()),
                      frac_ge1lep_given_W_emu=float((nl >= 1).sum()/max(1, nW["e"] + nW["mu"])),
                      n_gen_lep_in_acc=int(gen_acc.sum()), eff_reco_given_acc=float(((nl >= 1) & gen_acc).sum()/max(1, gen_acc.sum())))
# jets
two_j = nj >= 2
pj = lambda x, k: ak.to_numpy(ak.pad_none(x, 2)[:, k][two_j])
j1 = vec(pj(jpt, 0), pj(jeta, 0), pj(jphi, 0), pj(jm, 0)); j2 = vec(pj(jpt, 1), pj(jeta, 1), pj(jphi, 1), pj(jm, 1))
mjj = minv(j1, j2); deta = abs(pj(jeta, 0) - pj(jeta, 1))
res["jets"] = dict(n_ge2j=int(two_j.sum()), mjj_median=float(np.median(mjj)) if two_j.sum() else None,
                   frac_mjj_gt500=float((mjj > 500).mean()) if two_j.sum() else None,
                   frac_deta_gt2p5=float((deta > 2.5).mean()) if two_j.sum() else None,
                   frac_60_mjj_110=float(((mjj > 60) & (mjj < 110)).mean()) if two_j.sum() else None,
                   frac_ge1b=float((nb >= 1).mean()))
# illustrative smoke cutflow (sigma in fb before external BRs; weighted MC error = sigma/N*sqrt(n))
mjj_full = np.zeros(N); deta_full = np.zeros(N); mjj_full[two_j] = mjj; deta_full[two_j] = deta
mgg_full = np.zeros(N); mgg_full[two] = mgg
steps = [("all", np.ones(N, bool)), (">=2 photons", ng >= 2), ("+ ==1 lepton (pT>15)", nl == 1), ("+ lead lepton pT>25", lead_lpt > 25),
         ("+ MET>30", met > 30), ("+ >=2 jets", nj >= 2), ("+ b-veto", nb == 0), ("+ mjj>500, |deta|>2.5", (mjj_full > 500) & (deta_full > 2.5)),
         ("+ 120<mgg<130", (mgg_full > 120) & (mgg_full < 130))]
cum = np.ones(N, bool); cf = []
for name, m in steps:
    cum = cum & m; n = int(cum.sum()); cf.append(dict(step=name, n_raw=n, sigma_fb=sig_fb*n/N, err_fb=sig_fb*math.sqrt(n)/N))
res["cutflow_illustrative"] = cf
json.dump(res, open(outp + ".json", "w"), indent=1)

# ---------------- figure (static validation panels; single series each, one hue)
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
C1, C2, INK, GRID = "#2a78d6", "#eb6834", "#3d3d3a", "#d9d8d3"
fig, ax = plt.subplots(2, 3, figsize=(13, 7.5))
def style(a, xl, title):
    a.set_xlabel(xl, color=INK); a.set_ylabel("events", color=INK); a.set_title(title, color=INK, fontsize=10, loc="left")
    a.grid(axis="y", color=GRID, lw=0.6); a.set_axisbelow(True)
    for s in ("top", "right"): a.spines[s].set_visible(False)
ax[0, 0].hist(mgg, bins=np.arange(110, 140.5, 0.5), color=C1, histtype="step", lw=2)
if not np.isnan(mu):
    xx = np.linspace(115, 135, 200); nrm = len(mggw)*0.5/(sg*math.sqrt(2*math.pi))
    ax[0, 0].plot(xx, nrm*np.exp(-0.5*((xx - mu)/sg)**2), color=C2, lw=1.5, label=f"core fit μ={mu:.2f}, σ={sg:.2f} GeV"); ax[0, 0].legend(frameon=False, fontsize=8)
style(ax[0, 0], "m_γγ [GeV] (2 leading photons)", "Diphoton mass")
ax[0, 1].hist(np.clip(dmx, -80, 80), bins=64, color=C1, histtype="step", lw=2); style(ax[0, 1], "MET_x(reco) − MET_x(gen) [GeV]", f"MET resolution σ68={res['met']['sigma68_dmetx']:.1f} GeV")
ax[0, 2].hist(np.clip(gmet, 0, 400), bins=40, color=C1, histtype="step", lw=2, label="GenMissingET")
ax[0, 2].hist(np.clip(met, 0, 400), bins=40, color=C2, histtype="step", lw=2, label="reco MET"); ax[0, 2].legend(frameon=False, fontsize=8)
style(ax[0, 2], "MET [GeV]", "Missing transverse momentum")
ax[1, 0].hist(np.clip(lead_lpt[nl >= 1], 0, 300), bins=30, color=C1, histtype="step", lw=2); style(ax[1, 0], "leading lepton pT [GeV]", "Isolated e/μ (pT>15, |η|<2.5)")
ax[1, 1].hist(np.clip(mjj, 0, 3000), bins=30, color=C1, histtype="step", lw=2); style(ax[1, 1], "m_jj [GeV] (2 leading jets)", "Tagging-jet mass")
ax[1, 2].hist(deta, bins=np.arange(0, 9.01, 0.3), color=C1, histtype="step", lw=2); style(ax[1, 2], "|Δη_jj|", "Tagging-jet separation")
fig.suptitle(f"{label}: Delphes validation ({N} events, VALIDATION ONLY)", color=INK, x=0.01, ha="left")
fig.tight_layout(); fig.savefig(outp + ".png", dpi=110)
print(json.dumps({k: res[k] for k in ("truth", "mgg", "met", "leptons", "jets")}, indent=1))
