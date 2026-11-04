#!/usr/bin/env python3
"""EXTENDED nmc_check for HH (patch 006 on lib/scripts/analysis/final_analysis.py::nmc_check; the lib rule is kept for signal-like samples).
Rules (SPEC 4.3, declared in advance):
  role 'sig' (and any sample flagged 'strict'):  N_gen >= max(50_000, sigma*BR*L)                      [lib rule + 50k floor]
  role 'bkg':  generator filter looser than reco baseline (twin_ok=True required),  truth-tag weights (no tag cut),
               in the final SR  N_eff = (sum w)^2/sum w^2 >= 10  OR a direct upper bound is supplied (ul_fb) and the conservative variant is flagged.
G2 revision (review item 5): a direct upper bound is NOT accepted as a bare number.  `ul` must be a dict(method="poisson95_wmax", k=<raw SR count>, scale=<sigma*BR*L/N_gen in events/gen-event>, wmax=<max per-event weight>,
  value=<events>, conservative_file=<path>) that the checker RECOMPUTES (Poisson 95 % upper limit of k  x scale x wmax, 1e-6 relative) and the named conservative-variant output must exist and contain the same value for this sample
  (the analysis sets the background to the bound; it is a named output of the analysis, not a promise).  Rule 'full-N' rows (D-HH-12: ggF HH, ZH, ZZjj, ttH) are checked strictly like signal.
Every sample must also carry a BR ledger whose factors multiply to br_total (BR once).  Fails loudly with SystemExit listing ALL violations.
Input: list of dict(name, role, N_gen, sigma_fb, br_total, br_ledger=[...], twin_ok, sr_sumw, sr_sumw2, ul_fb)"""
import sys, math, os, json
from scipy.stats import chi2
NMIN = 50_000; NEFF_MIN = 10.0
def neff(sw, sw2): return sw * sw / sw2 if sw2 > 0 else 0.0
SIG_ROLES = ("sig", "basis", "closure")        # registry roles of samples entering s (twin/validation/ggHH-closure are not signal)
def poisson95_upper(k): return 0.5 * chi2.ppf(0.95, 2 * (int(k) + 1))      # one-sided 95 % CL upper limit on the Poisson mean (k=0 -> 2.996)
def check_ul(name, ul, bad):
    """recompute a structured upper bound; returns True if accepted"""
    if not isinstance(ul, dict): bad.append(f"{name}: upper bound given as a bare number ({ul!r}); a structured record with method/k/scale/wmax/value/conservative_file is required"); return False
    if ul.get("method") == "poisson95_direct":           # UL = yield_direct x Poisson95(k)/k : proper Poisson 95 % upper limit on the raw hard-window SR count k, times the mean weight scale (yield_direct/k)
        miss = [k for k in ("k", "yield_direct", "value", "conservative_file") if k not in ul]
        if miss: bad.append(f"{name}: ul record lacks {miss}"); return False
        val = ul["yield_direct"] * poisson95_upper(ul["k"]) / ul["k"] if ul["k"] > 0 else float("inf")
    elif ul.get("method") == "poisson95_classaware":       # UL = E x Poisson95(n)/n on the class-aware smoothed expectation E (events) with n = (sum pw)^2/sum (pw)^2 effective count
        miss = [k for k in ("n_eff_s", "yield_est", "value", "conservative_file") if k not in ul]
        if miss: bad.append(f"{name}: ul record lacks {miss}"); return False
        n_ = ul["n_eff_s"]; val = ul["yield_est"] * (0.5 * chi2.ppf(0.95, 2 * (n_ + 1))) / n_ if n_ > 0 else float("inf")
    else:
        miss = [k for k in ("method", "k", "scale", "wmax", "value", "conservative_file") if k not in ul]
        if miss: bad.append(f"{name}: ul record lacks {miss}"); return False
        if ul["method"] != "poisson95_wmax": bad.append(f"{name}: ul method {ul['method']!r} unknown (poisson95_wmax, poisson95_classaware)"); return False
        val = poisson95_upper(ul["k"]) * ul["scale"] * ul["wmax"]
    if abs(val - ul["value"]) > 1e-6 * max(1e-300, abs(val)): bad.append(f"{name}: stated bound {ul['value']!r} != recomputed {ul['method']} = {val!r}"); return False
    cf = ul["conservative_file"]
    if not (isinstance(cf, str) and os.path.exists(cf)): bad.append(f"{name}: conservative-variant output {cf!r} does not exist"); return False
    try: cv = json.load(open(cf))[name]
    except Exception as e: bad.append(f"{name}: conservative-variant file unreadable or lacks this sample ({e!r})"); return False
    if abs(cv.get("sr_background_events", -1) - ul["value"]) > 1e-6 * max(1e-300, abs(ul["value"])): bad.append(f"{name}: conservative variant uses {cv.get('sr_background_events')!r}, not the bound {ul['value']!r}"); return False
    return True
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
            ok_ul = True
            if ne < NEFF_MIN:
                if ul is None: bad.append(f"{n}: N_eff(SR)={ne:.2f} < {NEFF_MIN} and no direct upper bound; NOT zero-yield-negligible"); ok_ul = False
                else: ok_ul = check_ul(n, ul, bad)
            ok = r.get("twin_ok", False) and (ne >= NEFF_MIN or ok_ul)
            rows[n] = dict(rule="effective-N", N_eff_SR=ne, ul=ul, twin_ok=r.get("twin_ok", False), ok=ok, conservative_variant_required=(ne < NEFF_MIN))
            if not r.get("twin_ok", False): bad.append(f"{n}: generator filter not proven safe by a twin sample")
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
    # --- upper-bound provenance tests (review item 5)
    import tempfile
    tmp = tempfile.mkdtemp(); cf = os.path.join(tmp, "cons.json")
    scale, wmax = 2.0, 0.36; val = poisson95_upper(0) * scale * wmax
    json.dump({"U_ok": {"sr_background_events": val}, "U_wrongcons": {"sr_background_events": 1.0 * val}}, open(cf, "w"))
    base = dict(name="U_ok", role="bkg", N_gen=1e6, sigma_fb=1e3, br_total=1.0, br_ledger=["one"], twin_ok=True, sr_sumw=0.0, sr_sumw2=0.0)
    ulok = dict(method="poisson95_wmax", k=0, scale=scale, wmax=wmax, value=val, conservative_file=cf)
    nmc_check_hh([dict(base, ul_fb=ulok)], br_inputs=bi); print("structured Poisson95 bound accepted")
    badul = [dict(base, name="U_bare", ul_fb=123.0), dict(base, name="U_value", ul_fb=dict(ulok, value=val * 0.5)), dict(base, name="U_nofile", ul_fb=dict(ulok, conservative_file=os.path.join(tmp, "none.json"))),
             dict(base, name="U_nosample", ul_fb=ulok), dict(base, name="U_method", ul_fb=dict(ulok, method="guess")), dict(base, name="U_wrongcons", ul_fb=dict(ulok, value=val))]
    json.dump({"U_value": {"sr_background_events": val * 0.5}, "U_wrongcons": {"sr_background_events": 2 * val}, "U_method": {"sr_background_events": val}}, open(cf, "w"))
    try: nmc_check_hh(badul, br_inputs=bi); print("SELFTEST FAILED: bad bounds accepted"); sys.exit(1)
    except SystemExit as e:
        msg = str(e); assert all(k in msg for k in ("U_bare", "U_value", "U_nofile", "U_nosample", "U_method", "U_wrongcons")), msg; print("self-test OK: all 6 malformed bounds rejected")
    if len(sys.argv) > 1: print(matrix_check(sys.argv[1]))
