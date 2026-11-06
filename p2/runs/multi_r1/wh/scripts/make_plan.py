#!/usr/bin/env python3
"""Builds reports/04_production_plan.md.body (G2 deliverable tables) from config/sample_matrix.yaml, test-job jsons (work/xrd), SR-proxy counts and fake-factor results.
Usage (pinned env for the SR proxy): scripts/envrun.sh python3 -P scripts/make_plan.py     Rerunnable: pending items are printed as PENDING, never invented."""
import os, sys, json, glob, math, yaml, subprocess, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import seeds as S, br_ledger as B
WH = S.WH; M = yaml.safe_load(open(f"{WH}/config/sample_matrix.yaml"))["samples"]; byid = {r["id"]: r for r in M}
EOS = "root://eosuser.cern.ch"; EP = WH.replace("/eos/home-r/", "/eos/user/r/")
DEF_COST, DEF_KB = 0.13, 2.8      # s/event (gridpack ME + PY8 + Delphes + slim) and kB/event: DEFAULTS from the first 8 test jobs (0.09-0.25 s/ev, 2.0-3.1 kB/ev), used only when a sample has no test json
# ------- test jobs: cluster IDs (submission order) and files
CL = {"S_EW_WHjj": "884457.0", "H_QCD_WH_mlm": "884457.1", "H_ttH_1l": "884457.2", "B_EW_Waajj_vbs": "885078.0 (fresh seed 2113101; 884457.3 and 885043.3 produced no events)", "F_Wjj_pilot": "884457.4", "F_Wajj_pilot": "884457.5",
      "B_QCD_Waajj_nomjj": "884460.0", "F_QCD_Wajj_nomjj": "884460.1", "B_QCD_Waajj_vbs": "884860.0"}
TEST_ORDER = ["S_EW_WHjj_taunu","H_QCD_WHjj_fixed","I_WHjj","H_tHq_lep","H_tHW_1l","T_tta_1l","T_ttaa_1l","T_tWa_1l","T_tt_1l","T_ttjj_1l","F_Wjjjj","F_EW_Wajj_vbs","F_QCD_Wajj_vbs",
              "F_EW_Wajj_nomjj","B_EW_Waajj_nomjj","V_WZa_WH","V_WWa_WH","V_ZZa_WH","H_ggZH_wh","H_ttH_dilep_wh","H_ZH_tautau_wh"]
CL.update({s: f"884935.{i}" for i, s in enumerate(TEST_ORDER)})
CL.update({"Q_aajj": "885126.0", "H_VBFH_jj": "885125.0", "F_QCD_Wajjj_nomjj": "893599.0", "Q_aajjj": "893599.1"})   # as recorded at submission (g3 tests)
_auto = json.load(open(f"{WH}/work/test_clusters.json")) if os.path.exists(f"{WH}/work/test_clusters.json") else {}   # scripts/test_clusters.py (submit-file queue order x condor event log)
for _s, _c in _auto.items():
    if _s in ("V_WZa_WH", "V_WWa_WH", "V_ZZa_WH", "B_EW_Waajj_nomjj") or _s.startswith("K_EW_WHjj_"): CL[_s] = _c   # re-run / late tests (the 884935.x entries for these were removed)
def jsons():
    d = {}
    for f in glob.glob(f"{WH}/work/test/*/*.json"):
        j = json.load(open(f)); d.setdefault(j["sample"], []).append((f, j))
    return d
J = jsons()
def tinfo(s):
    if s not in J: return None
    f, j = sorted(J[s])[0]; tag = f[:-5]
    sz = sum(os.path.getsize(tag + e) for e in (".root", "_gen.root") if os.path.exists(tag + e)); n = max(j["n_delphes"], 1)
    return dict(json=j, cost=(j["t_gridpack_s"]+j["t_py8_delphes_s"]+j["t_slim_s"])/max(j["n_lhe"], 1), kb=sz/n/1e3, acc=j["n_delphes"]/max(j["n_lhe"], 1), n=j["n_delphes"], nlhe=j["n_lhe"], root=tag + ".root", seed=j["mg_seed"])
NG = {"F_": 1, "T_tta_1l": 1, "T_tWa_1l": 1, "T_tt": 1, "V_": 2, "I_": 2}
def ng_of(s):
    for k, v in NG.items():
        if s.startswith(k): return v
    return 2
SRC = f"{WH}/work/srproxy.json"; SRP = json.load(open(SRC)) if os.path.exists(SRC) else {}
def srproxy(s, ti):
    if s in SRP and SRP[s]["root"] == ti["root"]: return SRP[s]
    from srsel import select
    try: sel = select(ti["root"], ng_of(s)); r = dict(root=ti["root"], n_sel=int(sel.sum()), N=len(sel), ng=ng_of(s))
    except Exception as e: r = dict(root=ti["root"], err=str(e)[:80], n_sel=None, N=ti["n"], ng=ng_of(s))
    SRP[s] = r; json.dump(SRP, open(SRC, "w"), indent=1); return r
def flavour(w):
    for lim, f in ((1200, "espresso"), (3600, "microcentury"), (7200, "longlunch"), (28800, "workday")):
        if w < lim: return f
    return "tomorrow"
def fffile(s): return f"{WH}/work/ff_{s}.json"
TWIN = {"B_QCD_Waajj_nomjj": "none (nominal = no mjj cut). Twin 2000 ev: mmjj>400 loses 47.6 +- 5.5 % (loose sel.); 40k twin: no cut >=100 GeV safe (loss 15-45 +- 2 %, 518 sel. events)", "F_QCD_Wajj_nomjj": "none (nominal). Twin 2000 ev: mmjj>400 loses 37 +- 9 %; 40k twin: loss 14-42 +- 2 % for 100-400 GeV (531 sel. events)", "F_QCD_Wajjj_nomjj": "none (nominal). ME+1-jet model: the 2-jet twin evidence (F_QCD_Wajj_nomjj, 40k events, SR proxy) is the cross-check; generator cut ptj>20 on the converted jet: 04 sec. 19",
        "B_EW_Waajj_nomjj": "none (nominal). EW twin (40k ev, 3724 selected at the reco SR, ng=2, cluster 893415): mmjj>400 loses 1.56 +- 0.20 %, 100 GeV 0.54 +- 0.12 % => safe (<=5 % within stat); the vbs sample is an allowed alternative", "F_EW_Wajj_nomjj": "none (nominal). EW twin (40k ev, 3824 selected): mmjj>400 loses 2.4 +- 0.3 %, 100 GeV 0.6 +- 0.1 % => safe (<=5 %); the vbs sample would be an allowed alternative"}
from scipy.stats import chi2
def lowfac(n):
    """one-sided 95 % lower Poisson bound on the PEAK-event rate, as a fraction of the observed n (pilot projection uncertainty; VERIFY #10 item 11)"""
    return float(chi2.ppf(0.05, 2*n)/2/n) if n > 0 else 0.0
STAT_REF_S, STAT_FRAC = 0.9, 0.1   # recheck-2 sev-1(a): MC-stat error of EACH ME-jet fake row in the PEAK region must be <= 0.1 x S (S ~ 0.9 events at 500/fb, 04 sec. 6e) = 0.09 events: sigma_MC(N) = (Y/sqrt(N_eff))_pilot x sqrt(N_gen/N)
STATROWS = ("F_Wjjjj", "T_ttjj_1l")
SANCTIONED = ("F_Wjjjj", "T_ttjj_1l")   # ONLY these two rows are planned by N_eff instead of the N rule (human-approved D4/D27: fake-factor weights, N_eff >= 10 in the SR). Q_aajj, H_VBFH_jj, H_ggF_jj are NOT sanctioned (D31): full N.
KFOLD = 5   # brief v2 step 3: disjoint training/evaluation folds; each evaluation fold must keep N_eff >= 10
def neff_gate(per_event_neff, n_planned, rule=10.0):
    """projected N_eff = (measured N_eff per generated event in the test pilot PEAK region) x N_planned. Returns the projection; raises SystemExit if < rule."""
    proj = per_event_neff*n_planned
    if proj < rule: raise SystemExit(f"N_eff gate: projected {proj:.2f} < {rule}")
    return proj
def selftests():
    """writes nothing: a bad row must make each gate fail loudly (VERIFY #8 items 4, 9)."""
    ok = 0
    for fn, args in ((neff_gate, (1e-4, 50000)), (B.nmc_check, ({}, )), (B.nmc_check, ({"S_EW_WHjj": dict(N=10, sig=13.77)}, ))):
        try: fn(*args)
        except SystemExit: ok += 1
    assert ok == 3, "gate self-test FAILED: a bad row did not fail"
    return ok
SELFTEST = selftests()
for r_ in M:     # populate the BR ledger from the matrix (register() otherwise only runs under br_ledger.__main__ -> empty ledger -> silent no-op)
    if "br_factors_external" in r_ and "path" not in r_: B.register(r_["id"], "", "", r_["br_factors_external"])
assert len(B.LEDGER) > 20, "BR ledger empty"
FAIL = []; PENDW = []; NMAXP = 2.0e7
def submitted_jobs(s):
    """actual submitted composition 'n x ev (+ n x ev ...)' from the submitted submit files (first cluster, top-ups, resubmissions), else None"""
    import collections as _c
    parts = []
    for f in sorted(glob.glob(f"{WH}/work/condor/prod/prod_{s}*.sub")):
        b = os.path.basename(f)[5:-4]
        if b != s and not re.fullmatch(re.escape(s) + r"_(topup|resub\d+)", b): continue
        if not os.path.exists(f"{WH}/work/condor/prod/.submitted_{b}"): continue
        c = _c.Counter(int(l.split()[3]) for l in open(f) if l.startswith("  ") and "tar.gz" in l); parts += [f"{n} x {e}" for e, n in sorted(c.items())]
    return " + ".join(parts) if parts else None
rows = []; tot = dict(cpu=0.0, gb=0.0, jobs=0); notes = []
for r in M:
    s = r["id"]; frozen = "path" in r
    if frozen or r.get("in_bs") is False: continue
    ti = tinfo(s); sig, k, need = r.get("sigma_fb"), r["k_external"], r.get("N_required")
    cost = ti["cost"] if ti else DEF_COST; kb = ti["kb"] if ti else DEF_KB; acc = ti["acc"] if ti else 1.0
    lhef = min(1.0, r.get("n_lhe_over_requested_test") or 1.0)
    Nacc = r.get("N_planned")           # accepted (Delphes) events required
    weighted_note = ""; FFROWS = ("F_Wjjjj", "T_ttjj_1l", "F_QCD_Wajjj_nomjj", "F_EW_Wajj_nomjj", "T_tta_1l", "T_tWa_1l", "Q_aajj", "H_VBFH_jj", "H_ggF_jj")
    if s in FFROWS:      # ONE fake model for every fake-photon / non-prompt-lepton row (G2 items 1,3,4): per-jet probability weights, final-SR-like PEAK region, photons pT>25
        ff = fffile(s); kind = "non-prompt-lepton f_l weights (f_l 2e-5/2e-4/2e-3 per D28 (ATLAS 1110.3174))" if s in ("Q_aajj", "H_VBFH_jj", "H_ggF_jj") else "jet->photon fake-factor weights = MEASURED Delphes j->gamma rate (nominal; assumed form kept as variant), photons pT>25"
        if os.path.exists(ff):
            f = json.load(open(ff)); reg = f["regions"].get("PEAK", {}); ne = reg.get("N_eff"); nev = reg.get("n_events", 0); per = (ne or 0)/f["N_gen"]
            if per <= 0: FAIL.append(f"{s}: zero PEAK events in the test job -> N_eff projection impossible (need a larger test or looser projection region)")
            else:
                Nneed = int(math.ceil(max(50000, 10*KFOLD/(per*lowfac(nev)))/1000)*1000)      # N_eff >= 10 in EVERY evaluation fold of a K-fold BDT (K=5 -> total N_eff >= 50)
                Nacc = max(Nneed, int(math.ceil(need/1000)*1000)) if (need and s not in SANCTIONED) else Nneed     # planning (design target N_eff = 10 x K, K = 5)
                if s in STATROWS:
                    _y = reg.get('yield_events_at_lumi', 0.0); _sig = _y/math.sqrt(ne) if ne else 0.0
                    _Ns = int(math.ceil(f['N_gen']*(_sig/(STAT_FRAC*STAT_REF_S))**2/1000)*1000); Nacc = max(Nacc, _Ns)
                if Nacc > NMAXP: FAIL.append(f"{s}: N_planned {Nacc} > feasible {NMAXP:.0e}")
            weighted_note = f"{kind}; test ({f['N_gen']} ev): PEAK n_events={nev}, N_eff={ne if ne is None else round(ne,2)} -> N_eff/event {per:.2e}; sigma_MC(B_row) at N_planned = {( (reg.get('yield_events_at_lumi',0)/math.sqrt(ne))*math.sqrt(f['N_gen']/Nacc) if ne else float('nan')):.3f} events (criterion <= {STAT_FRAC*STAT_REF_S:.2f} = 0.1 S for the ME-jet rows F_Wjjjj, T_ttjj_1l); projected N_eff at N_planned = {'-' if not per else round(per*Nacc,1)} central, {'-' if not per else round(per*Nacc*lowfac(nev),1)} at the 95 % one-sided Poisson lower bound of the pilot PEAK rate (factor {lowfac(nev):.2f} from {nev} raw events) (rule >= 10; top-up rule sec. 6d)"
        else: weighted_note = f"{kind}: N_eff projection PENDING (test job + weighting pilot)"; PENDW.append(s)
    if sig is None or (Nacc is None and need is None): nl = None
    else: nl = int(math.ceil((Nacc or 0)/acc/lhef/1000)*1000) if Nacc else None   # LHE events REQUESTED: accepted fraction (MLM) and gridpack shortfall (n_lhe/n_requested in the test) both divided out
    ev_pj = None; njobs = None; cpu = gb = None; fl = None; sd = "PENDING"
    if nl:
        ev_pj = min(50000, max(math.ceil(nl/800/1000)*1000, int(14400/cost/1000)*1000, 1000)); ev_pj = min(ev_pj, max(1000, math.ceil(nl/10/1000)*1000))
        njobs = math.ceil(nl/ev_pj); assert njobs <= 800, (s, njobs)
        cpu = nl*cost/3600; gb = (Nacc)*kb/1e6; fl = flavour(ev_pj*cost*2.6+300); tot["cpu"] += cpu; tot["gb"] += gb; tot["jobs"] += njobs   # wall-time margin x2.6 (was x1.3): 4 Q_aajj jobs of 50 000 ev were removed at the 2 h limit on 2026-11-06
        sd = f"{S.seed(s,200)}-{S.seed(s,200+njobs-1)}"
    prj = "PENDING (no test job yet)"
    if ti and s not in FFROWS:
        sp = srproxy(s, ti)
        if sp.get("n_sel") is None: prj = "n/a (" + sp.get("err", "") + ")"
        elif sp["n_sel"] > 0 and Nacc: prj = f"{sp['n_sel']}/{sp['N']} in SR proxy (ng={sp['ng']}) -> {sp['n_sel']/sp['N']*Nacc:.0f} sel. events (unweighted => N_eff = N_sel)"
        else: prj = f"0/{sp['N']} in SR proxy (ng={sp['ng']}); 95% UL on SR fraction {3/sp['N']:.1e} -> N_sel < {3/sp['N']*(Nacc or 0):.0f}"
    elif s in FFROWS: prj = weighted_note
    tstat = "PENDING" if not ti else f"cluster {CL.get(s,'?')}, exit 0, LHE={ti['nlhe']}, Delphes={ti['n']} (executor audit; independent verifier check: VERIFY #4-#7, see VERIFY_REQUEST.md)"
    if s == "B_EW_Waajj_vbs": pass
    rows.append(dict(id=s, role=r["role"], sig=sig, sigsrc=r["sigma_source"], k=k, kf="x".join(r["br_factors_external"]), cuts=r["gen_cuts"], twin=TWIN.get(s, "mmjj>400 cross-check sample (not in b)" if "vbs" in s else "no generator mjj cut / not applicable"),
        need=need, sigN=r.get('sigma_for_N_fb'), plan=Nacc, nlhe=nl, weight=("per-jet probability weights (fake model above)" if s in FFROWS else "none (unit weights)") + ("; MLM matched, N = accepted" if acc < 0.9 else ""), prj=prj, seeds=sd, jobs=f"{njobs} x {ev_pj}" if njobs else "PENDING", cpu=cpu, gb=gb, test=tstat, flag=r.get("N_shortfall_flag"), flav=fl))
def fmt(x, f="%.4g"): return "PENDING" if x is None else f % x
L = ["| sample | role (s/b class) | σ (fb), source | BR / k (applied once) | generator cuts; twin evidence | N_required | N_planned (accepted) [LHE gen.] | weighting | projected N_eff in SR | seeds | jobs x ev/job (flavour) | CPU-h | storage GB | test job |", "|---|" + "---|"*13]
for x in rows:
    L.append(f"| {x['id']} | {x['role']} | {fmt(x['sig'])} ({x['sigsrc'][:60]}) | {x['kf']} = {x['k']:.5g} | {x['cuts'][:90]}; {x['twin']} | {fmt(x['need'], '%d')} | {fmt(x['plan'], '%d')} [{fmt(x['nlhe'], '%d')}] {('**flag ' + x['flag'] + '**') if x['flag'] else ''} | {x['weight']} | {x['prj']} | {x['seeds']} | {(submitted_jobs(x['id']) + ' (SUBMITTED; plan ' + x['jobs'] + ')') if submitted_jobs(x['id']) else x['jobs']} ({x['flav'] or '-'}) | {fmt(x['cpu'], '%.1f')} | {fmt(x['gb'], '%.2f')} | {x['test']} |")
open(f"{WH}/work/plan_table.md", "w").write("\n".join(L) + "\n")
GATED = {}
for x in rows:      # gate on the FINAL emitted N_planned (independent of the planning formula)
    if x["id"] in FFROWS and x["plan"] and os.path.exists(fffile(x["id"])):
        f_ = json.load(open(fffile(x["id"]))); ne_ = f_["regions"].get("PEAK", {}).get("N_eff")
        if not ne_: FAIL.append(f"{x['id']}: no PEAK N_eff in the pilot"); continue
        try: GATED[x["id"]] = neff_gate(lowfac(f_["regions"]["PEAK"]["n_events"])*ne_/f_["N_gen"], x["plan"], rule=10.0*KFOLD)
        except SystemExit as e: FAIL.append(f"{x['id']}: {e}")
NOTEVAL = [x["id"] for x in rows if x["id"] in FFROWS and x["id"] not in GATED]
GATE_LINE = (f"N_eff gate ENFORCED threshold = {10*KFOLD:.0f} (= 10 x K, K = {KFOLD}) at the 95 % one-sided Poisson lower bound of the pilot PEAK rate; evaluated and passed: {', '.join(sorted(GATED))}; "
             f"NOT EVALUATED (no pilot / no plan yet, PENDING: bulk of these rows must not be released): {', '.join(NOTEVAL) or 'none'}")
for _x in NOTEVAL:
    if _x not in PENDW and _x != "H_ggF_jj": FAIL.append(f"{_x}: N_eff gate not evaluated and not declared pending")
# ---- N check on the planned table (br_ledger.nmc_check = SPEC 4.2); pending / weighted rows listed explicitly
chk = {}; pend = []
for x in rows:
    if x["sig"] is None or x["plan"] is None: pend.append(x["id"]); continue
    if x['id'] in SANCTIONED: continue
    chk[x["id"]] = dict(N=x["plan"], sig=abs(x["sigN"] if x["sigN"] is not None else x["sig"]))
msg = "PASS"
try: nchk = B.nmc_check(chk); msg = f"PASS ({nchk} rows checked; EXEMPT from the N rule, human-sanctioned D4/D27 and gated by N_eff instead: {', '.join(SANCTIONED)}; Q_aajj/H_VBFH_jj/H_ggF_jj are CHECKED (full N, D31); ledger has {len(B.LEDGER)} entries, self-tests {SELFTEST}/3 failed-as-expected)"
except SystemExit as e: msg = "FAIL: " + str(e)
open(f"{WH}/work/plan_nmc.txt", "w").write(f"nmc_check on {len(chk)} planned rows (br_ledger.nmc_check, N >= max(50k, sigma_N*k*3000), sigma_N = max(primary, PY8 test sigma) x 1.05): {msg}\nPENDING (sigma or N not yet known): {', '.join(pend)}\nweighted/fake-model rows (N_eff>=10 rule in the PEAK region, ENFORCED: any violation exits non-zero): {'; '.join(x['id'] + ': ' + ('PENDING' if 'PENDING' in x['prj'] else x['prj'].split('projected N_eff at N_planned = ')[-1][:110]) for x in rows if x['id'] in FFROWS)}\n{GATE_LINE}\nN_eff projection pending for: {', '.join(PENDW) or 'none'}\nENFORCEMENT FAILURES: {'; '.join(FAIL) or 'none'}\n")
open(f"{WH}/work/plan_totals.txt", "w").write(f"planned new production (rows with known N): jobs={tot['jobs']}, CPU-h={tot['cpu']:.0f}, storage={tot['gb']:.1f} GB (budget WH <= 200 GB)\n")
if FAIL: print("N_eff / N rule FAILED:", FAIL, file=sys.stderr)
print(open(f"{WH}/work/plan_nmc.txt").read(), open(f"{WH}/work/plan_totals.txt").read())
# ---- machine-readable plan (consumed by make_prod_sub.py after G2) and the frozen-reuse table
json.dump({x["id"]: {k: v for k, v in x.items() if k in ("plan", "nlhe", "jobs", "seeds", "flav", "cpu", "gb")} | {"gp": None} for x in rows}, open(f"{WH}/work/plan.json", "w"), indent=1)
SRN = {"ZH_Zaajj_QCD_nomjj_lostlep": "280 selected of 100000 (ratio_C json, SR proxy ng=2)", "ZH_Zaajj_QCD_lostlep": "1099 selected of 100000 (ratio_C json)", "ZH_Zajj_eFake": "2857 (QCD vbs part, first 200k ev, ng=1; ratio_C json)"}
F = ["| frozen ZH sample (read-only reuse) | role | σ (fb), source | k | N available | N_required | selected events at the SR proxy (N_eff, unit weights) | generator cuts; correction | status |", "|---|---|---|---|---|---|---|---|---|"]
for r in M:
    if "path" not in r or r.get("in_bs") is False: continue
    c = r.get("c_gen_cut"); ct = "none" if not c else (f"C = {c['factor']} ± {c['factor']*c['rel_err_stat']:.3f} (stat, absolute; {100*c['rel_err_stat']:.1f} %), syst = full difference {c['syst_full_difference']}); {c['source'][:90]}" if c.get("factor") else "C PENDING: " + c["source"][:110])
    F.append(f"| {r['id']} | {r['role']} | {r['sigma_fb']:.4g}, {r['sigma_source'][:40]} | {r['k_external']:.5g} | {r['N_available']} | {r['N_required']} | {SRN.get(r['id'], 'frozen ZH sample, not passed through the WH SR proxy (no WH-selection yield is quoted for it; evaluated on the production-file selection at Phase 05)')} | {r['gen_cuts'][:60]}; {ct} | {'N OK' if r.get('N_ok') else 'N SHORT'} |")
open(f"{WH}/work/plan_frozen.md", "w").write("\n".join(F) + "\n")

if FAIL: raise SystemExit("N_eff rule violated for weighted rows: " + "; ".join(FAIL))
