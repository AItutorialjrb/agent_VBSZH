#!/usr/bin/env python3
"""Origin diagnosis of the lepton-free non-prompt reco photons (pT > 25, |eta| < 2.5, no crack, no prompt gen photon within dR 0.1, no prompt gen lepton within dR 0.2) on the EXISTING test-job *_full.root files (the Particle record is NOT in the production slim files). Per photon:
 - nearest GenJet (pT > 15) dR and pT; ratio of the reco photon pT to the sum of gen EM pT (status-1 gamma, e+-) within dR < 0.1;
 - leading status-1 gen particle within dR < 0.1 and its ancestry class: pi0/eta decay, other hadron decay, parton/boson parent (quark FSR/ISR; the 'prompt' flag treats these as prompt), lepton, none (no status-1 particle within 0.1).
Usage: bash scripts/envrun.sh python3 -P scripts/diag_photon_origin.py <out.json> <full.root>[:nprompt] ..."""
import sys, json, numpy as np, uproot, awkward as ak
out = sys.argv[1]; specs = sys.argv[2:]
def dphi(a, b): return (a-b+np.pi) % (2*np.pi)-np.pi
res = {}
for sp in specs:
    f, npw = (sp.split(":") + ["0"])[:2]; npw = int(npw); base = f[:-10]
    T = uproot.open(f)["Delphes"]; G = uproot.open(base + "_gen.root")["GenTruth"]
    a = T.arrays(["Photon.PT", "Photon.Eta", "Photon.Phi", "GenJet.PT", "GenJet.Eta", "GenJet.Phi", "Particle.PID", "Particle.Status", "Particle.M1", "Particle.PT", "Particle.Eta", "Particle.Phi"], library="np")
    g = G.arrays(["n_prompt_photons", "gph_eta", "gph_phi", "gph_prompt", "glep_pt", "glep_eta", "glep_phi", "glep_prompt"], library="ak"); npr = ak.to_numpy(g["n_prompt_photons"]); L = [ak.to_list(g[k]) for k in ("gph_eta", "gph_phi", "gph_prompt", "glep_eta", "glep_phi", "glep_pt", "glep_prompt")]
    rows = []
    for i in range(len(npr)):
        if npr[i] != npw: continue
        gp = [(e, p) for e, p, r in zip(L[0][i], L[1][i], L[2][i]) if r]; pl = [(e, p) for e, p, q, r in zip(L[3][i], L[4][i], L[5][i], L[6][i]) if r and q > 10]
        pid = a["Particle.PID"][i]; st = a["Particle.Status"][i]; m1 = a["Particle.M1"][i]; ppt = a["Particle.PT"][i]; pe = a["Particle.Eta"][i]; pp = a["Particle.Phi"][i]
        stable = [k for k in range(len(pid)) if st[k] == 1 and abs(pe[k]) < 5.5]
        for q, e, p in zip(a["Photon.PT"][i], a["Photon.Eta"][i], a["Photon.Phi"][i]):
            if q <= 25 or abs(e) >= 2.5 or 1.4442 < abs(e) < 1.566: continue
            if any(np.hypot(e-ge, dphi(p, gf)) < 0.1 for ge, gf in gp) or any(np.hypot(e-le, dphi(p, lp)) < 0.2 for le, lp in pl): continue
            wide = [(np.hypot(e-pe[k], dphi(p, pp[k])), k) for k in stable if np.hypot(e-pe[k], dphi(p, pp[k])) < 0.2]
            em2 = sum(ppt[k] for d, k in wide if abs(pid[k]) in (22, 11)); neut = sum(ppt[k] for d, k in wide if abs(pid[k]) in (130, 2112, 3122, 310, 3322, 3212, 14, 12, 16) and abs(pid[k]) not in (12, 14, 16)); chg = sum(ppt[k] for d, k in wide if abs(pid[k]) in (211, 321, 2212, 3222, 3112, 3312, 3334, 13))
            top = sorted(wide, key=lambda z: -ppt[z[1]])[:3]; topd = [(int(pid[k]), round(float(ppt[k]), 1), round(float(d), 3)) for d, k in top]
            carrier = "EM (gamma/e) within 0.2 carries >= 50 % of the reco pT" if em2 >= 0.5*q else ("hadron deposit (neutral/charged hadrons within 0.2 carry >= 50 %)" if (neut+chg) >= 0.5*q else "unexplained (< 50 % of the reco pT in status-1 gamma/e/hadrons within 0.2)")
            near = [(np.hypot(e-pe[k], dphi(p, pp[k])), k) for k in stable if np.hypot(e-pe[k], dphi(p, pp[k])) < 0.1]
            em = sum(ppt[k] for d, k in near if abs(pid[k]) in (22, 11)); lead = max(near, key=lambda z: ppt[z[1]])[1] if near else None
            cls = "none"
            if lead is not None:
                k = lead; cls = "stable-particle pid %d" % pid[k]; chain = []; steps = 0
                while k >= 0 and steps < 400:
                    k = int(m1[k]); steps += 1
                    if k < 0: break
                    ap = abs(int(pid[k])); chain.append(ap)
                    if ap in (111, 221, 331, 223, 113, 213, 333): cls = "decay of pi0/eta/eta'/omega/rho"; break
                    if ap > 100 and ap != 2212 and not (ap > 1000 and (ap//10) % 10 == 0): cls = "decay of other hadron (%d)" % ap; break
                    if ap in (11, 13, 15): cls = "lepton parent"; break
                else: pass
                if not cls.startswith(("decay", "lepton")): cls = "no hadron/lepton ancestor (parton/boson parent: FSR/ISR)" if abs(pid[lead]) == 22 else cls
            dj = [(np.hypot(e-e2, dphi(p, p2)), q2) for q2, e2, p2 in zip(a["GenJet.PT"][i], a["GenJet.Eta"][i], a["GenJet.Phi"][i]) if q2 > 15]; dmin = min(dj) if dj else (99.0, 0.0)
            rows.append(dict(pt=float(q), eta=float(e), cls=cls, carrier=carrier, em_sum_0p2=float(em2), neutral_had_0p2=float(neut), charged_had_0p2=float(chg), top3=topd, dr_genjet=float(dmin[0]), genjet_pt=float(dmin[1]), em_sum=float(em), n_near=len(near)))
    res[sp] = rows
json.dump(res, open(out, "w"), indent=1)
import collections
for sp, rows in res.items():
    n = len(rows); print(sp.split("/")[-1], "photons", n)
    if not n: continue
    c = collections.Counter(r["cls"] for r in rows); print("  origin:", {k: round(v/n, 3) for k, v in c.most_common(6)})
    cc = collections.Counter(r["carrier"] for r in rows); print("  pT carrier:", {k: round(v/n, 3) for k, v in cc.most_common(4)})
    d = np.array([r["dr_genjet"] for r in rows]); print("  dR(GenJet pT>15): <0.2 %.2f, 0.2-0.4 %.2f, 0.4-0.8 %.2f, 0.8-1.5 %.2f, >1.5 %.2f" % tuple(np.histogram(d, bins=[0, 0.2, 0.4, 0.8, 1.5, 100])[0]/n))
    em = np.array([r["em_sum"]/r["pt"] for r in rows]); print("  gen EM pT sum within 0.1 / reco pT: median %.2f, 10-90 %%: %.2f-%.2f" % (np.median(em), *np.percentile(em, [10, 90])))
