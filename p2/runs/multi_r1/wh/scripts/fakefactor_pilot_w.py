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
# NOMINAL fake model (orchestrator order 2026-11-06, D4): the MEASURED direct Delphes j->gamma rate table (scripts/jet_to_photon_rate.py -> work/jgamma_rate.json), per jet pT bin and barrel/endcap,
# with x = photon pT / jet pT drawn from the measured histogram. Variants reported next to it: up/down = nominal +/- total (stat (+) process) error, and the OLD assumed form F0 (pT/50)^-0.5 (x2 endcap, x~N(0.85,0.1)).
RJ = json.load(open(os.environ.get("RATE_FILE", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "work", "jgamma_rate.json"))))   # RATE_FILE: alternative table (production split closure)
CLS = os.environ.get("RATE_CLASS", "W")      # W: W+jets-dominated rows (F_*), TT: ttbar rows (T_*), pooled: both (variant)
sfx = {"W": "_W", "TT": "_TT", "pooled": ""}[CLS]
PTE = np.array(RJ["pt_edges"]); RT = np.array(RJ["rate" + sfx]); RE = np.array(RJ["err_total" + sfx]); RP = np.array(RJ["rate"])
XH = np.array(RJ["x_hist_per_ptbin" + sfx if ("x_hist_per_ptbin" + sfx) in RJ else "x_hist_per_ptbin"], float); XE = np.array(RJ["x_edges"])
VARS = ("nom", "up", "dn", "pooled", "assumed")
def ptbin(pt): return min(max(int(np.digitize(pt, PTE)-1), 0), len(PTE)-2)
def frates(pt, eta):
    ie = 0 if abs(eta) < 1.5 else 1; ib = ptbin(pt); r, e = RT[ie, ib], RE[ie, ib]
    return np.array([r, r+e, max(r-e, 0.0), RP[ie, ib], F0 * (pt/50.0)**-0.5 * (2.0 if abs(eta) > 1.566 else 1.0)])
def draw_x(pt, size_rng):
    h = XH[ptbin(pt)]; c = np.cumsum(h)/h.sum(); u = size_rng.random(); k = int(np.searchsorted(c, u)); return 0.5*(XE[k]+XE[k+1])
rng = np.random.default_rng(13600999)
t = uproot.open(slim)["Delphes"]; g = uproot.open(genf)["GenTruth"]
N = t.num_entries
A = lambda k: t[k].array()
w_evt = sigma * lumi / N  # physical weight per generated (unweighted) event, before fake factors

# parton HT per event from LHE (outgoing status-1 quarks/gluons)
ht = []
if lhe == "-":   # production files carry no LHE: HT-filter statistics are skipped (zeros)
    ht = [0.0]*N
else:
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
    xs = [draw_x(j[0], rng) for j in J]   # measured photon/jet pT ratio (nominal model); the assumed-form variant keeps only its weights
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
    acc = {r: np.zeros(len(VARS)) for r in reg}
    for fk, reals in combos:
        phs, wf = list(reals), np.ones(len(VARS))
        ok = True
        for k in fk:
            (pt, eta, phi), x = J[k]
            if not photon_ok(x*pt, eta): ok = False; break
            phs.append((x*pt, eta, phi)); wf = wf * frates(pt, eta)
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
        if acc[r][0] > 0 or acc[r].sum() > 0: reg[r].append((i, acc[r].copy()))

res = {"selection": {"bveto": BVETO, "bveto_def": "no b-tagged jet (BTag>0, pT>30, |eta|<2.5) outside the two fake-photon jets", "nfake": nfake, "lepton": "exactly 1 e/mu pT>25, no 2nd pT>15, MET>30", "photon_pt_min": PTG, "regions": "PRE=1l+MET+2 fake photons(pT>20)+>=2 tag jets pT>30; VBS=PRE+mjj>500,|deta|>2.5; PEAK=VBS+120<m_gg<130 (= the final-SR-like region)"}, "rate_class": CLS, "rate_file": "work/jgamma_rate.json", "rate_variants": list(VARS), "slim": slim, "N_gen": N, "sigma_fb": sigma, "lumi_fb": lumi, "F0": F0, "w_evt_unweighted": w_evt,
       "frac_events_HT_gt": {str(c): float((ht > c).mean()) for c in (50, 100, 150, 200, 300)}, "regions": {}}
for r, lst in reg.items():
    if not lst: res["regions"][r] = {"n_events": 0}; continue
    idx = np.array([e for e, _ in lst]); WF = np.array([x for _, x in lst])   # (n, variants)
    nz = WF[:, 0] > 0; W = w_evt * WF[:, 0][nz]
    d = {"n_events": int(nz.sum()), "yield_events_at_lumi": float(W.sum()), "N_eff": float(W.sum()**2 / (W**2).sum()) if nz.any() else 0.0, "mean_event_weight": float(W.mean()) if nz.any() else 0.0,
         "max_event_weight": float(W.max()) if nz.any() else 0.0, "yield_variants_at_lumi": {v: float(w_evt*WF[:, k].sum()) for k, v in enumerate(VARS)},
         "N_eff_variants": {v: (float((w_evt*WF[:, k]).sum()**2/((w_evt*WF[:, k])**2).sum()) if WF[:, k].sum() > 0 else 0.0) for k, v in enumerate(VARS)},
         "n_events_variants": {v: int((WF[:, k] > 0).sum()) for k, v in enumerate(VARS)}}
    if nz.any(): d["lost_frac_by_HT_filter"] = {str(c): float(W[ht[idx[nz]] <= c].sum() / W.sum()) for c in (50, 100, 150, 200, 300)}
    res["regions"][r] = d
json.dump(res, open(outj, "w"), indent=1)
print(json.dumps(res, indent=1))
