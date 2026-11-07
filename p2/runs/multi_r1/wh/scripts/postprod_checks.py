#!/usr/bin/env python3
"""Post-production checks on the delivered samples (04 sec. 20). Run inside the pinned stack: bash scripts/envrun.sh python3 -P scripts/postprod_checks.py <stage>
stage 'run'  : per-file pilots on production files (fake-photon rows: fakefactor_pilot_w.py with RATE_CLASS W/TT; non-prompt-lepton rows: fakelep_pilot.py) and the PEAK-region yield of the prompt rows (srsel with the 120-130 GeV window), in a process pool; files are a pre-declared sub-sample (every k-th file, k stated per row) -> work/postprod/*.json
stage 'agg'  : combines the per-file results: yield, sum w^2, N_eff and sigma_MC extrapolated to the full delivered N (sigma_MC ~ 1/sqrt(N)), D29 fractions, nmc_check with MEASURED N, the sigma_MC criteria -> work/postprod_checks.json
Combination of per-file pilot results (file f with n_f events, w_evt = sigma*L/n_f): Y = sum Y_f n_f/N ; sum w^2 = sum (Y_f^2/Neff_f) (n_f/N)^2 with N = sum n_f (subset), then sigma_MC(full) = sqrt(sum w^2) x sqrt(N_sub/N_full)."""
import sys, os, json, glob, re, subprocess, math, yaml, numpy as np
from multiprocessing import Pool
WH = "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh"; PR = "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/production/wh"; OUT = os.environ.get("POSTPROD_OUT", f"{WH}/work/postprod"); PHDIR = os.environ.get("PH_DIR", OUT)   # PH_DIR: directory of the fake-photon pilot results used by the agg stage (production-table re-run)
sys.path.insert(0, f"{WH}/scripts")
STAGE = sys.argv[1]
def files(s, k):
    fs = sorted(f for f in glob.glob(f"{PR}/{s}/*.root") if not f.endswith(("_gen.root", "_full.root"))); return fs[::k] if k > 1 else fs
# row, kind, class, nfake, every-k-th file
PILOT = [("F_Wjjjj", "ph", "W", 2, int(os.environ.get("FW_K", "8"))), ("F_QCD_Wajjj_nomjj", "ph", "W", 1, 4), ("F_EW_Wajj_nomjj", "ph", "W", 1, 1), ("T_ttjj_1l", "ph", "TT", 2, 1), ("T_tta_1l", "ph", "TT", 1, 3), ("T_tWa_1l", "ph", "TT", 1, 4),
         ("Q_aajj", "lep", None, None, 8), ("H_VBFH_jj", "lep", None, None, 1)]
PROMPT = [("B_QCD_Waajj_nomjj", 2, 5), ("B_EW_Waajj_nomjj", 2, 5), ("S_EW_WHjj", 2, 4), ("S_EW_WHjj_taunu", 2, 5), ("V_WWa_WH", 2, 5), ("V_WZa_WH", 2, 5), ("V_ZZa_WH", 2, 5), ("H_QCD_WH_mlm", 2, 3), ("H_ggZH_wh", 2, 5),
          ("H_ttH_1l", 2, 4), ("H_tHq_lep", 2, 3), ("H_tHW_1l", 2, 3), ("H_ttH_dilep_wh", 2, 5), ("H_ZH_tautau_wh", 2, 3), ("T_ttaa_1l", 2, 5)]
sk = {}
for l in open(f"{WH}/work/ff_F_Wjjjj.json"): break
def job_pilot(a):
    s, kind, cls, nf, f = a; stem = f[:-5]; o = f"{OUT}/{s}__{os.path.basename(stem)}.json"
    if os.path.exists(o): return o
    ff = json.load(open(f"{WH}/work/ff_{s if s != 'F_QCD_Wajjj_nomjj' else 'F_QCD_Wajjj_nomjj'}.json")); sig = ff["sigma_fb"] if "sigma_fb" in ff else ff["sigma_k_fb"]
    env = dict(os.environ, BVETO="1", PHOTON_PT="25")
    if kind == "ph":
        env["RATE_CLASS"] = cls; cmd = [sys.executable, "-P", f"{WH}/scripts/fakefactor_pilot_w.py", f, stem + "_gen.root", "-", str(sig), str(nf), o]
    else: cmd = [sys.executable, "-P", f"{WH}/scripts/fakelep_pilot.py", f, stem + "_gen.root", str(sig), o]
    r = subprocess.run(cmd, env=env, capture_output=True, text=True)
    if r.returncode: open(o + ".err", "w").write(r.stderr[-500:]); return None
    return o
def job_prompt(a):
    s, ng, f = a; o = f"{OUT}/{s}__{os.path.basename(f)[:-5]}.pk.json"
    if os.path.exists(o): return o
    from srsel import select
    j = json.load(open(f[:-5] + ".json")); sel = select(f, ng, win=(120, 130)); json.dump(dict(n_lhe=j["n_lhe"], n_delphes=j["n_delphes"], n_sel=int(sel.sum()), n_slim=len(sel)), open(o, "w")); return o
if STAGE in ("run", "runph"):
    os.makedirs(OUT, exist_ok=True); tasks = [(s, k_, c, n, f) for s, k_, c, n, k in PILOT for f in files(s, k)]; pt = [(s, ng, f) for s, ng, k in PROMPT for f in files(s, k)]
    print(len(tasks), "pilot files,", len(pt), "prompt files", flush=True)
    if STAGE == "runph": tasks = [x for x in tasks if x[1] == "ph"]; pt = []
    with Pool(8) as p: r1 = p.map(job_pilot, tasks, chunksize=1); r2 = p.map(job_prompt, pt, chunksize=1)
    print("failed pilots:", sum(x is None for x in r1), "prompt files done:", len(r2))
if STAGE == "agg":
    import csv, br_ledger as B
    mat = {r["id"]: r for r in yaml.safe_load(open(f"{WH}/config/sample_matrix.yaml"))["samples"]}; val = {r["sample"]: r for r in csv.DictReader(open(f"{WH}/work/prod_validation.csv"))}
    res = {}; L = 500.0
    def comb(rows, key):    # rows: list of (N_f, Y_f, Neff_f); returns dict
        Nsub = sum(r[0] for r in rows); Y = sum(r[1]*r[0] for r in rows)/Nsub
        sw2 = sum((r[1]**2/r[2])*(r[0]/Nsub)**2 for r in rows if r[2] > 0); return Nsub, Y, sw2
    for s, kind, cls, nf, k in PILOT:
        fs = sorted(glob.glob(f"{(PHDIR if kind == 'ph' else OUT)}/{s}__*.json")); fs = [f for f in fs if not f.endswith(".pk.json")]; rows = []; var = {}
        for f in fs:
            j = json.load(open(f)); N = j["N_gen"]; d = j["regions"].get("PEAK", {})
            if kind == "ph": Y = d.get("yield_events_at_lumi", 0.0); Ne = d.get("N_eff", 0.0); vv = d.get("yield_variants_at_lumi", {})
            else: Y = d.get("yield_nominal", 0.0); Ne = d.get("N_eff", 0.0); vv = {"nom": Y, "f2e-5": d.get("yield_f2e-5", 0.0), "f2e-3": d.get("yield_f2e-3", 0.0)}
            rows.append((N, Y, Ne))
            for a, b in vv.items(): var.setdefault(a, []).append((N, b))
        Nsub, Y, sw2 = comb(rows, "Y"); Nfull = int(val[s]["n_delphes"]); sigmc = math.sqrt(sw2)*math.sqrt(Nsub/Nfull) if sw2 > 0 else float("nan")
        res[s] = dict(kind=kind, n_files=len(fs), N_sub=Nsub, N_full=Nfull, yield_PEAK=Y, yield_variants={a: sum(x[1]*x[0] for x in v)/Nsub for a, v in var.items()}, sumw2_sub=sw2, sigma_MC_full=sigmc, N_eff_full=(Y**2/sw2)*(Nfull/Nsub) if sw2 > 0 else 0.0, raw_PEAK_events_sub=sum(1 for r in rows if r[1] > 0))
    for s, ng, k in PROMPT:
        fs = sorted(glob.glob(f"{OUT}/{s}__*.pk.json")); P = [json.load(open(f)) for f in fs]; nl = sum(p["n_lhe"] for p in P); ns = sum(p["n_sel"] for p in P); r = mat[s]
        Y = r["sigma_fb"]*r["k_external"]*L*ns/nl; res[s] = dict(kind="prompt", n_files=len(P), N_lhe_sub=nl, n_sel=ns, yield_PEAK=Y, sigma_stat=r["sigma_fb"]*r["k_external"]*L*math.sqrt(max(ns, 1))/nl, N_full_lhe=int(val[s]["n_lhe"]))
    # --- D29 totals (production rows in b; frozen ZH rows are not in the package: fractions are UPPER bounds)
    EXCL = {"S_EW_WHjj", "H_QCD_WHjj_fixed"} | {k for k in res if k.startswith("K_EW")}
    bkg = {s: v["yield_PEAK"] for s, v in res.items() if s not in EXCL}
    tot = sum(bkg.values()); q_hi = res["Q_aajj"]["yield_variants"].get("f2e-3", 0.0)
    d29 = dict(total_bkg_PEAK=tot, rows=bkg, F_QCD_Wajjj_fraction=bkg.get("F_QCD_Wajjj_nomjj", 0)/tot if "F_QCD_Wajjj_nomjj" in bkg else None, Q_aajj_fraction_nominal=bkg.get("Q_aajj", 0)/tot, Q_aajj_fraction_upper=q_hi/(tot-bkg.get("Q_aajj", 0)+q_hi), signal_PEAK=res["S_EW_WHjj"]["yield_PEAK"])
    S = d29["signal_PEAK"]; crit = {}
    for s in ("F_Wjjjj", "T_ttjj_1l", "F_QCD_Wajjj_nomjj"):
        sm = res[s]["sigma_MC_full"]; crit[s] = dict(sigma_MC=sm, over_S_measured=sm/S, over_0p1S_ref_0p09=sm/0.09, meets_0p09=bool(sm <= 0.09), D_WH_15_trigger_sigma_MC_gt_0p5S=bool(sm > 0.5*S) if s == "F_QCD_Wajjj_nomjj" else None, N_eff_full=res[s]["N_eff_full"])
    # --- nmc_check with MEASURED N
    SANCT = ("F_Wjjjj", "T_ttjj_1l"); chk = {}
    for s, v in val.items():
        if s in SANCT or s == "H_QCD_WHjj_fixed": continue
        r = mat[s]; B.register(s, "", "", r["br_factors_external"]); chk[s] = dict(N=int(v["n_delphes"]), sig=r["sigma_for_N_fb"])
    try: nchk = B.nmc_check(chk); msg = f"PASS ({nchk} rows checked with the MEASURED delivered N (Delphes events); exempt: {', '.join(SANCT)} (human-sanctioned, gated by N_eff), H_QCD_WHjj_fixed (cross-check))"
    except SystemExit as e: msg = "FAIL: " + str(e)
    out = dict(pilots={s: res[s] for s in res}, D29=d29, sigma_MC_criteria=crit, nmc_check_measured=msg, N_eff_gate={s: dict(N_eff_full=res[s]["N_eff_full"], threshold_10=res[s]["N_eff_full"] >= 10, threshold_50=res[s]["N_eff_full"] >= 50) for s in SANCT})
    json.dump(out, open(os.environ.get("AGG_OUT", f"{WH}/work/postprod_checks.json"), "w"), indent=1, default=float)
    print(msg); print("D29", {k: (round(v, 4) if isinstance(v, float) else v) for k, v in d29.items() if k != "rows"}); print("sigma_MC", {s: {k: (round(v, 3) if isinstance(v, float) else v) for k, v in c.items()} for s, c in crit.items()}); print("N_eff", out["N_eff_gate"])
