#!/usr/bin/env python3
"""EXTENDED nmc_check for HH (patch 006 on lib/scripts/analysis/final_analysis.py::nmc_check; the lib rule is kept for signal-like samples).
Rules (SPEC 4.3, declared in advance):
  role 'sig' (and any sample flagged 'strict'):  N_gen >= max(50_000, sigma*BR*L)                      [lib rule + 50k floor]
  role 'bkg':  generator filter looser than reco baseline (twin_ok=True required),  truth-tag weights (no tag cut),
               in the final SR  N_eff = (sum w)^2/sum w^2 >= 10  OR a direct upper bound is supplied (ul_fb) and the conservative variant is flagged.
Every sample must also carry a BR ledger whose factors multiply to br_total (BR once).  Fails loudly with SystemExit listing ALL violations.
Input: list of dict(name, role, N_gen, sigma_fb, br_total, br_ledger=[...], twin_ok, sr_sumw, sr_sumw2, ul_fb)"""
import sys, math
NMIN = 50_000; NEFF_MIN = 10.0
def neff(sw, sw2): return sw * sw / sw2 if sw2 > 0 else 0.0
SIG_ROLES = ("sig", "basis", "closure")        # registry roles of samples entering s (twin/validation/ggHH-closure are not signal)
def br_product(ledger, br_inputs): return math.prod(br_inputs[b.split("@")[0]] for b in ledger)
def nmc_check_hh(reg, L_fb=3000.0, br_inputs=None, check_bkg=True):
    bad, rows = [], {}
    for r in reg:
        n = r["name"]; need = r["sigma_fb"] * r["br_total"] * L_fb
        if br_inputs is not None:
            prod = br_product(r["br_ledger"], br_inputs)
            if abs(prod - r["br_total"]) > 1e-9 * max(1.0, prod): bad.append(f"{n}: br_total {r['br_total']!r} != product of ledger {r['br_ledger']} = {prod!r} (BR once)")
            if len(set(r["br_ledger"])) != len(r["br_ledger"]): bad.append(f"{n}: identical ledger label repeated (BR applied twice to the same particle): {r['br_ledger']}")
            for b in r["br_ledger"]:
                if b.split("@")[0] not in br_inputs: bad.append(f"{n}: unknown BR input {b}")
        if r["role"].split("(")[0] in SIG_ROLES or r.get("strict"):   # role normalised: "closure(kl)" -> "closure"
            req = max(NMIN, need)
            rows[n] = dict(rule="N>=max(50k,sigma*BR*L)", N=r["N_gen"], required=req, ok=r["N_gen"] >= req)
            if r["N_gen"] < req: bad.append(f"{n}: N_gen={r['N_gen']} < max(50k, sigma*BR*L={need:.0f})")
        elif check_bkg:
            ne = neff(r.get("sr_sumw", 0.0), r.get("sr_sumw2", 0.0)); ul = r.get("ul_fb")
            ok = r.get("twin_ok", False) and (ne >= NEFF_MIN or ul is not None)
            rows[n] = dict(rule="effective-N", N_eff_SR=ne, ul_fb=ul, twin_ok=r.get("twin_ok", False), ok=ok, conservative_variant_required=(ne < NEFF_MIN))
            if not r.get("twin_ok", False): bad.append(f"{n}: generator filter not proven safe by a twin sample")
            if ne < NEFF_MIN and ul is None: bad.append(f"{n}: N_eff(SR)={ne:.2f} < {NEFF_MIN} and no direct upper bound; NOT zero-yield-negligible")
    if bad: raise SystemExit("HH N/effective-N policy VIOLATED:\n  " + "\n  ".join(bad))
    return rows
def matrix_check(path, planned=True):
    """Run the BR-once + signal-N rule on the REAL registry (config/sample_matrix.yaml); signal N_gen = planned N_MC_required (production not yet run)."""
    import yaml
    planned = []; m = yaml.safe_load(open(path)); bi = {k: v["value"] for k, v in m["br_inputs"].items()}; reg = []
    for s in m["samples"]:
        if s.get("sigma_fb") is None: planned.append(s["name"]); continue
        reg.append(dict(name=s["name"], role=s["role"], N_gen=s.get("N_MC_required", 0), sigma_fb=s["sigma_fb"], br_total=s["br_total"], br_ledger=s["br_ledger"]))
    rows = nmc_check_hh(reg, br_inputs=bi, check_bkg=False)
    for n in planned: rows[n] = dict(status="planned, unchecked (no sigma yet)")
    print(f"{len(planned)} rows planned, unchecked: {planned}")
    return rows
if __name__ == "__main__":
    import sys
    bi = {"B_bb": 0.5824, "B_Zqq": 0.6991, "one": 1.0}
    good = [dict(name="S", role="basis", N_gen=60000, sigma_fb=1.0, br_total=0.5824**2, br_ledger=["B_bb@H1", "B_bb@H2"]),
            dict(name="ZZ", role="bkg", N_gen=1e6, sigma_fb=1e3, br_total=0.6991**2, br_ledger=["B_Zqq@Z1", "B_Zqq@Z2"], twin_ok=True, sr_sumw=50.0, sr_sumw2=100.0),
            dict(name="Q", role="bkg", N_gen=1e6, sigma_fb=1e6, br_total=1.0, br_ledger=["one"], twin_ok=True, sr_sumw=50.0, sr_sumw2=100.0)]
    print(nmc_check_hh(good, br_inputs=bi))
    bad = [dict(good[0], name="S_lowN", N_gen=1000), dict(good[0], name="C_lowN", role="closure", N_gen=1000), dict(good[2], name="Q", sr_sumw=3.0, sr_sumw2=9.0, twin_ok=False),
           dict(good[0], name="S2", br_total=0.5824**3, br_ledger=["B_bb@H1", "B_bb@H2", "B_bb@H2"]), dict(good[0], name="S3", br_total=0.5824**2 * 1.0000001)]
    try: nmc_check_hh(bad, br_inputs=bi); print("SELFTEST FAILED: did not raise"); sys.exit(1)
    except SystemExit as e:
        msg = str(e); assert all(k in msg for k in ("S_lowN", "C_lowN", "Q:", "S2", "S3")), msg; print("self-test OK (raised on all 5 bad entries):\n" + msg)
    if len(sys.argv) > 1: print(matrix_check(sys.argv[1]))
