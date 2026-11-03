#!/usr/bin/env python3
"""Phase-03 Delphes object validation of a *full* Delphes+Pythia8 file (with Particle branch) from a W(->l nu) H(->gg) sample.
Usage: python3 -I validate_delphes.py <full.root> <sigma_fb_before_Hdecay_BR> <outdir> [label]
Checks (validation only, NOT an analysis selection): H->gg / W->l nu closure at generator level, reco lepton efficiency,
MET resolution vs GenMissingET, photon pair + m_gg peak, VBS-jet reco/gen matching and m_jj resolution."""
import sys, json, os
import numpy as np, uproot, awkward as ak
fn, outdir = sys.argv[1], sys.argv[3]; label = sys.argv[4] if len(sys.argv) > 4 else os.path.basename(fn)
os.makedirs(outdir, exist_ok=True)
t = uproot.open(fn)["Delphes"]; A = lambda k: t[k].array()
N = t.num_entries
pid, d1, d2 = A("Particle/Particle.PID"), A("Particle/Particle.D1"), A("Particle/Particle.D2")
st = A("Particle/Particle.Status"); gpt, geta, gphi = A("Particle/Particle.PT"), A("Particle/Particle.Eta"), A("Particle/Particle.Phi")
nH = nHaa = nW = 0; wdec = {"e": 0, "mu": 0, "tau": 0, "other": 0}; glep = []   # per event: (pt, eta, phi, flavour) of W-daughter lepton
for i in range(N):
    p = ak.to_numpy(pid[i]); a = ak.to_numpy(d1[i]); b = ak.to_numpy(d2[i]); lep = None
    for k in np.where(np.abs(p) == 25)[0]:
        dau = [p[j] for j in range(a[k], b[k] + 1)] if a[k] >= 0 and b[k] >= a[k] else []
        if 25 in dau or not dau: continue
        nH += 1; nHaa += sorted(dau) == [22, 22]
    for k in np.where(np.abs(p) == 24)[0]:
        dau = [p[j] for j in range(a[k], b[k] + 1)] if a[k] >= 0 and b[k] >= a[k] else []
        if not dau or 24 in [abs(x) for x in dau]: continue
        nW += 1; ad = sorted(abs(x) for x in dau if x != 22)   # radiative W->l nu gamma copies counted with their l nu
        if ad == [11, 12]: wdec["e"] += 1
        elif ad == [13, 14]: wdec["mu"] += 1
        elif ad == [15, 16]: wdec["tau"] += 1
        else: wdec["other"] += 1
        for j in range(a[k], b[k] + 1):
            if abs(p[j]) in (11, 13): lep = (float(gpt[i][j]), float(geta[i][j]), float(gphi[i][j]), abs(int(p[j])))
    glep.append(lep)
def dphi(x, y): return (x - y + np.pi) % (2*np.pi) - np.pi
el = {v: A(f"Electron/Electron.{v}") for v in ("PT", "Eta", "Phi")}; mu = {v: A(f"Muon/Muon.{v}") for v in ("PT", "Eta", "Phi")}
res = dict(label=label, n_events=int(N), gen_H_lastcopy=int(nH), gen_H_to_gg=int(nHaa), gen_W_lastcopy=int(nW), gen_W_decay=wdec)
# lepton efficiency (gen lepton pT>25, |eta|<2.5 ; reco match dR<0.2, reco pT>0.5*gen)
eff = {}
for fl, nm, ob in ((11, "electron", el), (13, "muon", mu)):
    nacc = nrec = 0
    for i, l in enumerate(glep):
        if l is None or l[3] != fl or l[0] < 25 or abs(l[1]) > 2.5: continue
        nacc += 1
        dr = np.hypot(ak.to_numpy(ob["Eta"][i]) - l[1], dphi(ak.to_numpy(ob["Phi"][i]), l[2]))
        ok = (dr < 0.2) & (ak.to_numpy(ob["PT"][i]) > 0.5*l[0])
        nrec += bool(np.any(ok))
    eff[nm] = dict(n_gen_acc=nacc, n_reco=nrec, eff=(nrec/nacc if nacc else None), err=(np.sqrt(nrec/nacc*(1-nrec/nacc)/nacc) if nacc else None))
res["lepton_eff"] = eff
# MET resolution
met = A("MissingET/MissingET.MET")[:, 0]; mphi = A("MissingET/MissingET.Phi")[:, 0]
gmet = A("GenMissingET/GenMissingET.MET")[:, 0]; gphi_ = A("GenMissingET/GenMissingET.Phi")[:, 0]
met, mphi, gmet, gphi_ = (ak.to_numpy(x) for x in (met, mphi, gmet, gphi_))
dx = met*np.cos(mphi) - gmet*np.cos(gphi_); dy = met*np.sin(mphi) - gmet*np.sin(gphi_)
sel = gmet > 30
def rms68(x): q = np.percentile(x, [16, 84]); return float((q[1]-q[0])/2)
res["MET"] = dict(n_genMET_gt30=int(sel.sum()), sigma68_dx=rms68(dx), sigma68_dy=rms68(dy), median_rel_bias=float(np.median((met[sel]-gmet[sel])/gmet[sel])),
                  sigma68_rel=rms68((met[sel]-gmet[sel])/gmet[sel]), median_gen=float(np.median(gmet)), median_reco=float(np.median(met)))
# photons
ph = {v: A(f"Photon/Photon.{v}") for v in ("PT", "Eta", "Phi", "E")}
pt, eta, phi = ph["PT"], ph["Eta"], ph["Phi"]
ok = (pt > 20) & (abs(eta) < 2.5) & ~((abs(eta) > 1.4442) & (abs(eta) < 1.566))
n2 = ak.sum(ok, axis=1) >= 2; res["photons"] = dict(frac_ge2_gamma=float(np.mean(ak.to_numpy(n2))))
m = []
for i in np.where(ak.to_numpy(n2))[0]:
    o = np.argsort(-ak.to_numpy(pt[i][ok[i]]))[:2]
    P = [(ak.to_numpy(pt[i][ok[i]])[j], ak.to_numpy(eta[i][ok[i]])[j], ak.to_numpy(phi[i][ok[i]])[j]) for j in o]
    px = sum(p[0]*np.cos(p[2]) for p in P); py = sum(p[0]*np.sin(p[2]) for p in P); pz = sum(p[0]*np.sinh(p[1]) for p in P); e = sum(p[0]*np.cosh(p[1]) for p in P)
    m.append(np.sqrt(max(e*e-px*px-py*py-pz*pz, 0)))
m = np.array(m); w = m[(m > 100) & (m < 150)]
res["photons"].update(n_pairs=int(len(m)), mgg_median=float(np.median(w)) if len(w) else None, mgg_sigma68=rms68(w) if len(w) else None,
                      frac_pairs_120_130=float(np.mean((m > 120) & (m < 130))) if len(m) else None)
# jets: reco jets (pT>25, |eta|<4.7) matched to GenJet; m_jj resolution of leading-two matched
jpt, jeta, jphi, jm = (A(f"Jet/Jet.{v}") for v in ("PT", "Eta", "Phi", "Mass")); gj = {v: A(f"GenJet/GenJet.{v}") for v in ("PT", "Eta", "Phi", "Mass")}
def mjj(o, i, j): 
    P = []
    for k in (i, j):
        pt_, e_, f_, m_ = o
        P.append((pt_*np.cos(f_), pt_*np.sin(f_), pt_*np.sinh(e_), np.sqrt((pt_*np.cosh(e_))**2 + m_**2)))
    s = [P[0][q]+P[1][q] for q in range(4)]; return np.sqrt(max(s[3]**2-s[0]**2-s[1]**2-s[2]**2, 0))
rr = []; deta = []; mj = []; nj2 = 0
for i in range(N):
    sj = (jpt[i] > 25) & (abs(jeta[i]) < 4.7); idx = np.where(ak.to_numpy(sj))[0]
    if len(idx) < 2: continue
    nj2 += 1; a, b = idx[0], idx[1]
    def v4(pt_, e_, f_, m_): return np.array([pt_*np.cos(f_), pt_*np.sin(f_), pt_*np.sinh(e_), np.sqrt((pt_*np.cosh(e_))**2+m_**2)])
    R = [v4(*(float(jpt[i][k]), float(jeta[i][k]), float(jphi[i][k]), float(jm[i][k]))) for k in (a, b)]
    s = R[0]+R[1]; mr = np.sqrt(max(s[3]**2-s[0]**2-s[1]**2-s[2]**2, 0)); mj.append(mr); deta.append(abs(float(jeta[i][a])-float(jeta[i][b])))
    G = []
    for k in (a, b):
        dr = np.hypot(ak.to_numpy(gj["Eta"][i]) - float(jeta[i][k]), dphi(ak.to_numpy(gj["Phi"][i]), float(jphi[i][k])))
        if len(dr) == 0 or dr.min() > 0.3: break
        g = int(np.argmin(dr)); G.append(v4(float(gj["PT"][i][g]), float(gj["Eta"][i][g]), float(gj["Phi"][i][g]), float(gj["Mass"][i][g])))
    if len(G) == 2:
        s = G[0]+G[1]; mg = np.sqrt(max(s[3]**2-s[0]**2-s[1]**2-s[2]**2, 0))
        if mg > 300: rr.append(mr/mg - 1)
mj = np.array(mj); deta = np.array(deta); rr = np.array(rr)
res["jets"] = dict(frac_ge2jets=nj2/N, mjj_median=float(np.median(mj)), frac_mjj_gt500_deta_gt2p5=float(np.mean((mj > 500) & (deta > 2.5))),
                   n_matched_mjj_gt300=int(len(rr)), mjj_resolution_sigma68=rms68(rr) if len(rr) > 20 else None, mjj_median_bias=float(np.median(rr)) if len(rr) > 20 else None)
json.dump(res, open(f"{outdir}/validation.json", "w"), indent=1)
try:
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    f, ax = plt.subplots(1, 4, figsize=(17, 3.6))
    ax[0].hist(m[(m > 100) & (m < 150)], 50); ax[0].set_xlabel("m_gg [GeV]")
    ax[1].hist(np.clip(met, 0, 300), 40, alpha=.6, label="reco"); ax[1].hist(np.clip(gmet, 0, 300), 40, histtype="step", label="gen"); ax[1].legend(); ax[1].set_xlabel("MET [GeV]")
    ax[2].hist((met[sel]-gmet[sel])/gmet[sel], 50, range=(-1, 1)); ax[2].set_xlabel("(MET_reco-MET_gen)/MET_gen")
    ax[3].hist(np.clip(mj, 0, 2500), 50); ax[3].set_xlabel("m_jj [GeV]"); f.suptitle(label); f.tight_layout(); f.savefig(f"{outdir}/validation.png", dpi=90)
except Exception as e: print("plot failed", e)
print(json.dumps(res, indent=1))
