#!/usr/bin/env python3
"""Artefact-photon veto validation on the *_full.root test files (D34 a').
For every lepton-free non-prompt-origin reco photon (pT>10, |eta|<2.5, no prompt gen photon dR<0.1, no prompt gen lepton dR<0.2, any n_prompt_photons)
truth label  : Etrue/Ereco = sum E of the UNIQUE particles in Photon.Particles / reco E  (reviewer's test)  -> genuine if >= 0.5
GenTruth proxy (available in production slim files): R = sum pT of GenTruth gph (status-1 photons pT>10,|eta|<3) within dR<0.2 of the reco photon / reco pT; also dRmin to nearest gph.
Veto (proposal): artefact if R < RCUT (nominal 0.5). Prints the confusion matrix vs the truth label for RCUT in {0.3,0.5,0.7}.
Usage: bash scripts/envrun.sh python3 -P scripts/veto_validation.py out.json full1.root ..."""
import sys, json, numpy as np, uproot, awkward as ak
def dphi(a, b): return (a-b+np.pi) % (2*np.pi)-np.pi
rows = []
for f in sys.argv[2:]:
    base = f[:-10]; T = uproot.open(f)["Delphes"]; G = uproot.open(base+"_gen.root")["GenTruth"]
    ph = T.arrays(["Photon.PT", "Photon.Eta", "Photon.Phi", "Photon.E", "Photon.Particles"], library="ak")
    uid = T["Particle/Particle.fUniqueID"].array(library="ak"); pE = T["Particle/Particle.E"].array(library="ak")
    g = G.arrays(["gph_pt", "gph_eta", "gph_phi", "gph_prompt", "glep_eta", "glep_phi", "glep_pt", "glep_prompt"], library="ak")
    for i in range(len(ph["Photon.PT"])):
        pts = ph["Photon.PT"][i]
        if len(pts) == 0: continue
        gp = list(zip(g["gph_pt"][i], g["gph_eta"][i], g["gph_phi"][i], g["gph_prompt"][i])); gl = [(e, p) for e, p, q, r in zip(g["glep_eta"][i], g["glep_phi"][i], g["glep_pt"][i], g["glep_prompt"][i]) if r and q > 10]
        u2k = None
        for k in range(len(pts)):
            q, e, p = float(pts[k]), float(ph["Photon.Eta"][i][k]), float(ph["Photon.Phi"][i][k])
            if q <= 10 or abs(e) >= 2.5: continue
            if any(pr and np.hypot(e-ge, dphi(p, gf)) < 0.1 for _, ge, gf, pr in gp) or any(np.hypot(e-le, dphi(p, lp)) < 0.2 for le, lp in gl): continue
            if u2k is None: u2k = {int(x): j for j, x in enumerate(uid[i])}
            rl = ph["Photon.Particles"][i][k].to_list() if hasattr(ph["Photon.Particles"][i][k], "to_list") else ph["Photon.Particles"][i][k]
            refs = set(); 
            for tr in (rl if isinstance(rl, list) else [rl]):
                for x in (tr.get("refs", []) if isinstance(tr, dict) else []): refs.add(u2k.get(int(x)))
            refs.discard(None); Et = float(sum(pE[i][j] for j in refs)); Er = float(ph["Photon.E"][i][k])
            R = float(sum(gq for gq, ge, gf, _ in gp if np.hypot(e-ge, dphi(p, gf)) < 0.2))/q
            dm = min([np.hypot(e-ge, dphi(p, gf)) for _, ge, gf, _ in gp] or [99.0])
            rows.append(dict(file=f.split("/")[-1], ev=i, pt=q, eta=e, E_ref_over_E=Et/Er, nref=len(refs), R=R, dRmin=float(dm)))
json.dump(rows, open(sys.argv[1], "w"))
a = np.array([[r["E_ref_over_E"], r["R"], r["pt"]] for r in rows]); n = len(a); print("photons", n)
gen = a[:, 0] >= 0.5; print("truth genuine (Eref/E>=0.5): %d (%.1f %%), artefact: %d" % (gen.sum(), 100*gen.mean(), (~gen).sum()))
print("Eref/E percentiles 10/50/90 all:", np.percentile(a[:, 0], [10, 50, 90]).round(3))
for rc in (0.3, 0.5, 0.7):
    v = a[:, 1] >= rc; print("RCUT %.1f: kept(genuine-like) %d | truth genuine kept %d lost %d | truth artefact kept(leak) %d rejected %d" % (rc, v.sum(), (v & gen).sum(), (~v & gen).sum(), (v & ~gen).sum(), (~v & ~gen).sum()))
for lo, hi in ((10, 25), (25, 50), (50, 1000)):
    s = (a[:, 2] >= lo) & (a[:, 2] < hi); print("pT %d-%d: n=%d truth-genuine frac %.2f  proxy(R>=0.5) frac %.2f" % (lo, hi, s.sum(), gen[s].mean() if s.any() else -1, (a[s, 1] >= 0.5).mean() if s.any() else -1))
