#!/usr/bin/env python3
"""Order-of-magnitude ESTIMATES (not rigorous upper bounds: the efficiency factors below are ASSUMED and UNVALIDATED) for backgrounds without MC support -- Phase 02. NOT yields.
yield_estimate = sigma_B_gg [fb] * L * P(non-prompt lepton) * eps_extra_jet * eps_VBS * eps_MET * eps_window.
P(nonprompt lepton) per additional jet: low/nominal/high = 3e-5 / 1e-4 / 1e-3 (ZH config/sample_matrix_phase02.yaml fake_scenarios.nonprompt_lepton, NOT data-driven).
eps_VBS = P(m_jj>500, |deta|>2.5) ; eps_MET = P(MET>30 | non-prompt lepton, no genuine neutrino pair but semileptonic decays) ; eps_window = P(120<m_gg<130)."""
L = 500.0; BGG = 0.00227
PL = {"low": 3e-5, "nominal": 1e-4, "high": 1e-3}
rows = [
 # name, sigma*B_gg [fb] or fiducial sigma [fb], is_continuum, eps_extra_jet, eps_VBS, eps_MET, eps_window, source
 ("QCD gamma gamma + jj (LO MG5, pTg>25, 100<mgg<170, ptj>20)", 3542.0, 0.5, 0.10, 0.2, 0.14, "smoke Q_aajj_smoke: 3.542 pb (LO, no K-factor, fixed 2 jets)"),
 ("ggF H->gg (+jets)   [YR4 13 TeV 48.58 pb x1.1 = 53.4 pb]", 53.4e3*BGG, 0.5, 0.01, 0.2, 0.9, "YR4 x 1.1 scaling (as ZH); eps_VBS from ggF+2j fraction (assumed 1e-2)"),
 ("ZH, Z->nunu, H->gg [LO ZH 704 fb (ZH zh_0j 48.45 fb / 0.06878) x B(inv)=0.200 x B_gg]", 704.0*0.2*BGG, 0.5, 0.01, 0.8, 0.9, "LO sigma from the ZH smoke run; eps_VBS assumed 1e-2; genuine MET (eps_MET 0.8)"),
 ("VBF H->gg           [YR4 13 TeV 3.78 pb x1.1 = 4.16 pb]", 4.16e3*BGG, 0.3, 0.5, 0.2, 0.9, "YR4 x 1.1 scaling; extra (non-tag) jet fraction 0.3 assumed"),
]
print(f"{'component':64s}{'sigma_fid[fb]':>14s}" + "".join(f"{k:>10s}" for k in PL))
for n, s, ej, ev, em, ew, src in rows:
    ys = [s*L*p*ej*ev*em*ew for p in PL.values()]
    print(f"{n:64s}{s:14.4g}" + "".join(f"{y:10.3g}" for y in ys) + f"   | {src}")

# ---- ttbar single-lepton, two jet->gamma fakes (estimate; NO pilot run -> unquantified until a pilot exists, D-WH-2)
sk = 1.417e5*0.97056; npair = 15; f0 = 1e-3; e_pt = 0.5; e_win = 0.02; e_vbs = 0.01; e_bveto = 0.1
base = sk*L*npair*f0**2*e_pt*e_win*e_vbs*e_bveto
print(f"{'ttbar 1l, 2 jet->gamma fakes (15 jet pairs, f0=1e-3, eps_pT .5, window .02, VBS .01, b-veto .1)':64s}{sk:14.4g}" + "".join(f"{base*m:10.3g}" for m in (0.09, 1, 9)) + "   | f scenarios x{0.3,1,3} per photon -> x{0.09,1,9}; sigma = smoke T_tt_1l_smoke 141.7 pb x k; eps ASSUMED")
