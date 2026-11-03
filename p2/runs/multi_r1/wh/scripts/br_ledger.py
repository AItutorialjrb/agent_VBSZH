#!/usr/bin/env python3
"""WH BR ledger + N_MC check (standalone; structure follows lib/scripts/analysis/final_analysis.py BRDEF/nmc_check).
Run `python3 -P scripts/br_ledger.py` to print the derivation of WF and to self-test the assertions."""
import math
# --- inputs (all pinned, sources in reports/01_signal_definition.md)
BGG = 0.002270                       # B(H->gamma gamma), LHCHWG YR4, mH=125.00 (as ZH)
B_PDG_E, B_PDG_MU = 0.1071, 0.1063   # PDG 2025 W->e nu, W->mu nu (config/pdg2025_W.pdf)
MW, GF, WW = 80.419002, 1.16639e-5, 2.047600   # MG5 sm-no_b_mass param_card (MW derived from aEWM1=132.507, Gf, MZ; WW fixed)
G_L = GF*MW**3/(6*math.sqrt(2)*math.pi)         # tree W->l nu partial width per lepton flavour (massless leptons)
B_MG_L = G_L/WW                                  # MG5-LO B(W->l nu) per flavour (decay-table definition)
B_MG_LL = 2*B_MG_L
B_PDG_LL = B_PDG_E + B_PDG_MU
WF = B_PDG_LL/B_MG_LL                            # analogue of ZF = 0.9783 (Z)
BR_WLL = B_PDG_LL                                # W -> e nu + mu nu physical (W decayed in PY8/other generators)
ZF, BR_ZLL = 0.9783, 0.033632+0.033662
B_PDG_TAU, B_PDG_HAD = 0.1138, 0.6741        # PDG 2025 W->tau nu, W->hadrons
B_MG_HAD = 6*G_L/WW                                # MG5-LO tree: 3 colours x 2 generations of quark doublets (diagonal CKM, no QCD correction)
WFTAU = B_PDG_TAU/B_MG_L                           # tau feed-down samples (W->tau nu in ME)
WHAD = B_PDG_HAD/B_MG_HAD                          # hadronic W in top decays / tW (single-lepton configurations)
F = dict(BGG=BGG, WF=WF, WFTAU=WFTAU, WHAD=WHAD, ZF=ZF, BR_WLL=BR_WLL, BR_ZLL=BR_ZLL, one=1.0)
# per-sample ledger: (decay in ME / elsewhere, H decay, factors multiplied once)
LEDGER = {}
def register(sid, wdec, hdec, factors):
    prod = 1.0
    for x in factors: prod *= F[x]
    assert factors.count("BGG") <= 1 and sum(factors.count(x) for x in ("WF","WFTAU","ZF","BR_WLL","BR_ZLL")) <= 1 + (1 if "WHAD" in factors else 0) + (1 if factors.count("WF")==2 else 0), f"BR applied twice for {sid}"
    LEDGER[sid] = dict(decay=wdec, h=hdec, factors=factors, k=prod)
    return prod
def nmc_check(rows, L=3000.0, floor=50000):
    """rows: {sid: dict(N=generated events, sig=sigma[fb] before external BR)}; N >= max(floor, sig*k*L), else SystemExit (SPEC 4.2)."""
    bad = []
    for sid, r in rows.items():
        need = max(floor, r["sig"]*LEDGER[sid]["k"]*L)
        if r["N"] < need: bad.append(f"{sid}: N={r['N']} < max({floor}, sigma*BR*L)={need:.0f}")
    if bad: raise SystemExit("N_MC policy VIOLATED:\n  "+"\n  ".join(bad))
if __name__ == "__main__":
    print(f"Gamma(W->l nu) tree = {G_L*1e3:.3f} MeV ; WW(MG5) = {WW} GeV ; 9*G_L = {9*G_L:.4f} GeV")
    print(f"B_MG5(W->l nu) = {B_MG_L:.5f}/flavour, e+mu = {B_MG_LL:.5f} ; B_PDG(e+mu) = {B_PDG_LL:.4f} ; WF = {WF:.4f}")
    # uncertainty on WF from PDG (e, mu errors uncorrelated: 0.16, 0.15 %) 
    print(f"B_MG(had) = {B_MG_HAD:.5f}; WHAD = {WHAD:.4f}; WFTAU = {WFTAU:.4f}")
    print(f"WF err (PDG) = {math.hypot(0.0016,0.0015)/B_MG_LL:.4f}")
    k = register("S_EW_WHjj", "W->l nu in MG5 ME (e,mu)", "H->gg forced in PY8 (cond. BR 1)", ["WF","BGG"]); print("k(S_EW_WHjj) =", k)
    try: register("bad","","",["WF","BGG","BGG"]); print("FAIL: no assertion")
    except AssertionError as e: print("assertion OK:", e)
