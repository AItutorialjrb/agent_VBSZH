#!/usr/bin/env python3
"""Per-file measurement of the decontaminated Delphes jet->photon rate with the GenTruth artefact veto (D34 a'). Usage: rate_genuine.py <slim.root> <out.json>
Definition = postprod_rate.py v2 (GenJet pT>25,|eta|<2.5, no prompt gen lepton pT>10 within dR<0.4, events n_prompt_photons==0, reco photon pT>20 (not 10: the veto is complete only above ~15 GeV, 05a sec. 1) within dR<0.2 of the GenJet, photons dR<0.1 to a prompt gen photon excluded = real)
plus the veto: R = sum pT of GenTruth gph (status-1 photons pT>10,|eta|<3; any prompt flag) within dR<0.2 of the reco photon / reco pT.
  genuine in-jet photon : R >= RCUT (nominal 0.5; variants 0.3, 0.7);  Delphes energy-flow artefact : R < RCUT.
Counts per [barrel,endcap] x jet-pT bin: den, num_gen[RCUT], num_art[RCUT=0.5], x-histogram of genuine photons. The jet is counted once (leading matched photon)."""
import sys, json, numpy as np, uproot, awkward as ak
PT = [25, 35, 50, 75, 100, 150, 1000]; XB = np.linspace(0, 1.5, 16); nb = len(PT)-1; RC = (0.3, 0.5, 0.7)
def dphi(a, b): return (a-b+np.pi) % (2*np.pi)-np.pi
f, out = sys.argv[1:3]
T = uproot.open(f)["Delphes"]; G = uproot.open(f[:-5]+"_gen.root")["GenTruth"]
a = T.arrays(["GenJet.PT", "GenJet.Eta", "GenJet.Phi", "Photon.PT", "Photon.Eta", "Photon.Phi"], library="ak")
g = G.arrays(["n_prompt_photons", "gph_pt", "gph_eta", "gph_phi", "gph_prompt", "glep_pt", "glep_eta", "glep_phi", "glep_prompt"], library="ak")
den = np.zeros((2, nb)); ng = np.zeros((len(RC), 2, nb)); na = np.zeros((2, nb)); xh = np.zeros((nb, len(XB)-1)); nreal = np.zeros((2, nb))
sel = np.nonzero(ak.to_numpy(g["n_prompt_photons"]) == 0)[0]
L = {k: ak.to_list(g[k][sel]) for k in g.fields if k != "n_prompt_photons"}; A = {k: ak.to_list(a[k][sel]) for k in a.fields}
for n in range(len(sel)):
    gp = list(zip(L["gph_pt"][n], L["gph_eta"][n], L["gph_phi"][n], L["gph_prompt"][n])); pl = [(e, p) for e, p, q, r in zip(L["glep_eta"][n], L["glep_phi"][n], L["glep_pt"][n], L["glep_prompt"][n]) if r and q > 10]
    ph = [(q, e, p) for q, e, p in zip(A["Photon.PT"][n], A["Photon.Eta"][n], A["Photon.Phi"][n]) if q > 20 and abs(e) < 2.5]
    for q, e, p in zip(A["GenJet.PT"][n], A["GenJet.Eta"][n], A["GenJet.Phi"][n]):
        if q <= 25 or abs(e) >= 2.5: continue
        if any(np.hypot(e-le, dphi(p, lp)) < 0.4 for le, lp in pl): continue
        ie = 0 if abs(e) < 1.5 else 1; ip = int(np.digitize(q, PT)-1)
        if not 0 <= ip < nb: continue
        den[ie, ip] += 1
        m = [x for x in ph if np.hypot(e-x[1], dphi(p, x[2])) < 0.2]
        if not m: continue
        lead = max(m, key=lambda z: z[0])
        if any(pr and np.hypot(lead[1]-ge, dphi(lead[2], gf)) < 0.1 for _, ge, gf, pr in gp): nreal[ie, ip] += 1; continue
        R = sum(gq for gq, ge, gf, _ in gp if np.hypot(lead[1]-ge, dphi(lead[2], gf)) < 0.2)/lead[0]
        for k, rc in enumerate(RC):
            if R >= rc: ng[k, ie, ip] += 1
        if R >= 0.5: xh[ip] += np.histogram([lead[0]/q], bins=XB)[0]
        else: na[ie, ip] += 1
json.dump(dict(file=f, n_events=T.num_entries, den=den.tolist(), num_gen=ng.tolist(), num_art=na.tolist(), n_real=nreal.tolist(), xh=xh.tolist(), rcuts=RC), open(out, "w"))
