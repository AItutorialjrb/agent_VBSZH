#!/usr/bin/env python3
"""Fake-factor (parametrised j->gamma) estimate on a pilot sample + generator-filter safety test.
Usage: python3 -P fakefactor_pilot.py <slim.root> <gen.root> <events.lhe.gz> <sigma_fb> <nfake 1|2> <out.json> [lumi_fb=500]
 - nfake=2 (W+jets): N_prompt_photons==0 required; every ordered-free pair of reco jets may fake two photons.
 - nfake=1 (Zgamma+jets): N_prompt_photons==1 required; one reco photon (real) + one jet faking.
 f(pT,eta) = F0*(pT/50)^-0.5, x2 for |eta|>1.566 (config/sample_matrix_phase02.yaml); fake pT = x*pT(jet),
 x ~ N(0.85,0.10) truncated [0.5,1] (fixed RNG seed). Remaining jets supply the two VBS tag jets.
 Regions: PRE = 1 lepton + MET>30 + 2 photons (pT>20, |eta|<2.5, no crack) + >=2 tag jets pT>30;
          VBS = PRE + mjj>500, |deta_jj|>2.5;  PEAK = VBS + 120<m_gg<130.
Reports sum of weights (fb, F0=1e-3 nominal), effective N, mean physical event weight, and the fraction of
fake-weighted VBS/PRE yield lost by parton-level HT filters (from the LHE)."""
import sys, os, gzip, json, numpy as np, awkward as ak, uproot
PTG = float(os.environ.get("PHOTON_PT", "25"))   # G2-FIX item 4: photon pT threshold of the SR (25 GeV); the G1/G2-prep numbers used 20
BVETO = os.environ.get("BVETO", "0") == "1"   # G2: drop combinations with a b-tagged jet (pT>30,|eta|<2.5) that is not one of the fake-photon jets

slim, genf, lhe, sigma, nfake, outj = sys.argv[1:7]; sigma = float(sigma); nfake = int(nfake)
lumi = float(sys.argv[7]) if len(sys.argv) > 7 else 500.0
F0 = 1.0e-3
rng = np.random.default_rng(13600999)
t = uproot.open(slim)["Delphes"]; g = uproot.open(genf)["GenTruth"]
N = t.num_entries
A = lambda k: t[k].array()
w_evt = sigma * lumi / N  # physical weight per generated (unweighted) event, before fake factors

# parton HT per event from LHE (outgoing status-1 quarks/gluons)
ht = []
with gzip.open(lhe, "rt") as f:
    inev = False; lines = []
    for line in f:
        if line.startswith("<event"): inev, lines = True, []; continue
        if line.startswith("</event"):
            inev = False; h = 0.0
            for l in lines[1:]:
                p = l.split()
                if len(p) >= 13 and p[1] == "1" and (abs(int(p[0])) <= 5 or p[0] == "21"):
                    h += np.hypot(float(p[6]), float(p[7]))
            ht.append(h); continue
        if inev and not line.startswith("<") and not line.startswith("#"): lines.append(line)
ht = np.array(ht)
assert len(ht) == N, f"LHE ({len(ht)}) / Delphes ({N}) event mismatch"

def lv(pt, eta, phi):
    return np.array([pt*np.cos(phi), pt*np.sin(phi), pt*np.sinh(eta), pt*np.cosh(eta)])
def m(a, b):
    s = a + b; return np.sqrt(max(s[3]**2 - s[0]**2 - s[1]**2 - s[2]**2, 0.0))
def photon_ok(pt, eta): return pt > PTG and abs(eta) < 2.5 and not (1.4442 < abs(eta) < 1.566)
def frate(pt, eta): return F0 * (pt/50.0)**-0.5 * (2.0 if abs(eta) > 1.566 else 1.0)

jpt, jeta, jphi, jbt = A("Jet/Jet.PT"), A("Jet/Jet.Eta"), A("Jet/Jet.Phi"), A("Jet/Jet.BTag")
ept, eeta, ephi, eq = A("Electron/Electron.PT"), A("Electron/Electron.Eta"), A("Electron/Electron.Phi"), A("Electron/Electron.Charge")
mpt, meta, mphi, mq = A("Muon/Muon.PT"), A("Muon/Muon.Eta"), A("Muon/Muon.Phi"), A("Muon/Muon.Charge")
gpt, geta, gphi = A("Photon/Photon.PT"), A("Photon/Photon.Eta"), A("Photon/Photon.Phi")
npr = ak.to_numpy(g["n_prompt_photons"].array())

metpt = A("MissingET/MissingET.MET")
def zcand(i):
    """WH selection (replaces the Z window of the ZH original): exactly one e/mu with pT>25 (|eta|<2.5 e, <2.4 mu), no second e/mu with pT>15, MET>30 GeV (ILLUSTRATIVE, not optimised)."""
    nl = [pt for pt, eta in ((ept[i][k], eeta[i][k]) for k in range(len(ept[i]))) if pt > 15 and abs(eta) < 2.5] + \
         [pt for pt, eta in ((mpt[i][k], meta[i][k]) for k in range(len(mpt[i]))) if pt > 15 and abs(eta) < 2.4]
    return len(nl) == 1 and nl[0] > 25 and metpt[i][0] > 30

reg = {r: [] for r in ("PRE", "VBS", "PEAK")}   # entries: (event index, fake weight)
for i in range(N):
    if npr[i] != (0 if nfake == 2 else 1) or not zcand(i): continue
    KJ = [k for k in range(len(jpt[i])) if jpt[i][k] > 20 and abs(jeta[i][k]) < 4.7]
    J = [(jpt[i][k], jeta[i][k], jphi[i][k]) for k in KJ]; JB = [bool(jbt[i][k] > 0 and jpt[i][k] > 30 and abs(jeta[i][k]) < 2.5) for k in KJ]
    xs = np.clip(rng.normal(0.85, 0.10, len(J)), 0.5, 1.0)
    real = [(gpt[i][k], geta[i][k], gphi[i][k]) for k in range(len(gpt[i])) if photon_ok(gpt[i][k], geta[i][k])]
    if nfake == 1:
        if len(real) < 1: continue
        r0 = real[0]
        keep = [np.hypot(j[1]-r0[1], (j[2]-r0[2]+np.pi) % (2*np.pi)-np.pi) > 0.4 for j in J]
        JB = [b for b, kp in zip(JB, keep) if kp]; J = [(j, x) for j, x, kp in zip(J, xs, keep) if kp]
        combos = [((k,), [r0]) for k in range(len(J))]
    else:
        J = list(zip(J, xs))
        combos = [((a, b), []) for a in range(len(J)) for b in range(a+1, len(J))]
    acc = {r: 0.0 for r in reg}
    for fk, reals in combos:
        phs, wf = list(reals), 1.0
        ok = True
        for k in fk:
            (pt, eta, phi), x = J[k]
            if not photon_ok(x*pt, eta): ok = False; break
            phs.append((x*pt, eta, phi)); wf *= frate(pt, eta)
        if not ok: continue
        if BVETO and any(JB[k] for k in range(len(J)) if k not in fk): continue
        tags = sorted([J[k][0] for k in range(len(J)) if k not in fk and J[k][0][0] > 30], reverse=True)
        if len(tags) < 2: continue
        acc["PRE"] += wf
        j1, j2 = tags[0], tags[1]
        if m(lv(*j1), lv(*j2)) > 500 and abs(j1[1]-j2[1]) > 2.5:
            acc["VBS"] += wf
            if 120 < m(lv(*phs[0]), lv(*phs[1])) < 130: acc["PEAK"] += wf
    for r in reg:
        if acc[r] > 0: reg[r].append((i, acc[r]))

res = {"selection": {"bveto": BVETO, "bveto_def": "no b-tagged jet (BTag>0, pT>30, |eta|<2.5) outside the two fake-photon jets", "nfake": nfake, "lepton": "exactly 1 e/mu pT>25, no 2nd pT>15, MET>30", "photon_pt_min": PTG, "regions": "PRE=1l+MET+2 fake photons(pT>20)+>=2 tag jets pT>30; VBS=PRE+mjj>500,|deta|>2.5; PEAK=VBS+120<m_gg<130 (= the final-SR-like region)"}, "slim": slim, "N_gen": N, "sigma_fb": sigma, "lumi_fb": lumi, "F0": F0, "w_evt_unweighted": w_evt,
       "frac_events_HT_gt": {str(c): float((ht > c).mean()) for c in (50, 100, 150, 200, 300)}, "regions": {}}
for r, lst in reg.items():
    if not lst: res["regions"][r] = {"n_events": 0}; continue
    idx = np.array([e for e, _ in lst]); wf = np.array([x for _, x in lst]); W = w_evt * wf
    res["regions"][r] = {"n_events": len(lst), "yield_events_at_lumi": float(W.sum()),
                         "N_eff": float(W.sum()**2 / (W**2).sum()), "mean_event_weight": float(W.mean()),
                         "max_event_weight": float(W.max()),
                         "lost_frac_by_HT_filter": {str(c): float(W[ht[idx] <= c].sum() / W.sum()) for c in (50, 100, 150, 200, 300)}}
json.dump(res, open(outj, "w"), indent=1)
print(json.dumps(res, indent=1))
