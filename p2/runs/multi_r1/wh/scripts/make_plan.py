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
TWIN = {"B_QCD_Waajj_nomjj": "none (nominal = no mjj cut). Twin 2000 ev: mmjj>400 loses 47.6 +- 5.5 % (loose sel.); 40k twin: no cut >=100 GeV safe (loss 15-45 +- 2 %, 518 sel. events)", "F_QCD_Wajj_nomjj": "none (nominal). Twin 2000 ev: mmjj>400 loses 37 +- 9 %; 40k twin: loss 14-42 +- 2 % for 100-400 GeV (531 sel. events)",
        "B_EW_Waajj_nomjj": "none (nominal); EW twin = this sample vs B_EW_Waajj_vbs (pending)", "F_EW_Wajj_nomjj": "none (nominal); EW twin vs F_EW_Wajj_vbs (pending)"}
rows = []; tot = dict(cpu=0.0, gb=0.0, jobs=0); notes = []
for r in M:
    s = r["id"]; frozen = "path" in r
    if frozen or r.get("in_bs") is False: continue
    ti = tinfo(s); sig, k, need = r.get("sigma_fb"), r["k_external"], r.get("N_required")
    cost = ti["cost"] if ti else DEF_COST; kb = ti["kb"] if ti else DEF_KB; acc = ti["acc"] if ti else 1.0
    Nacc = r.get("N_planned")           # accepted (Delphes) events required
    weighted_note = ""
    if r.get("weighted"):
        ff = fffile(s)
        if os.path.exists(ff):
            f = json.load(open(ff)); reg = f["regions"].get("PEAK", {}); ne = reg.get("N_eff"); nev = reg.get("n_events", 0)
            per = (ne or 0)/f["N_gen"]; Nacc = int(math.ceil(max(50000, 3*10/per)/1000)*1000) if per > 0 else None
            weighted_note = f"fake-factor weighting; test job ({f['N_gen']} ev): PEAK(final-SR-like)-region n_events={nev}, N_eff={ne if ne is None else round(ne,2)} -> N_eff/event = {per:.2e}; planned N gives projected N_eff = {'-' if not Nacc else round(per*Nacc,1)} (target >= 10, x3 safety)"
        else: weighted_note = "fake-factor weighting; N_planned from N_eff>=10 projection: PENDING (test job + scripts/fakefactor_pilot_w.py)"
    if sig is None or (Nacc is None and need is None): nl = None
    else: nl = int(math.ceil((Nacc or 0)/acc/1000)*1000) if Nacc else None
    ev_pj = None; njobs = None; cpu = gb = None; fl = None; sd = "PENDING"
    if nl:
        ev_pj = min(50000, max(math.ceil(nl/800/1000)*1000, int(14400/cost/1000)*1000, 1000)); ev_pj = min(ev_pj, max(1000, math.ceil(nl/10/1000)*1000))
        njobs = math.ceil(nl/ev_pj); assert njobs <= 800, (s, njobs)
        cpu = nl*cost/3600; gb = (Nacc)*kb/1e6; fl = flavour(ev_pj*cost*1.3+300); tot["cpu"] += cpu; tot["gb"] += gb; tot["jobs"] += njobs
        sd = f"{S.seed(s,200)}-{S.seed(s,200+njobs-1)}"
    prj = "PENDING (no test job yet)"
    if ti and not r.get("weighted"):
        sp = srproxy(s, ti)
        if sp.get("n_sel") is None: prj = "n/a (" + sp.get("err", "") + ")"
        elif sp["n_sel"] > 0 and Nacc: prj = f"{sp['n_sel']}/{sp['N']} in SR proxy (ng={sp['ng']}) -> {sp['n_sel']/sp['N']*Nacc:.0f} sel. events (unweighted => N_eff = N_sel)"
        else: prj = f"0/{sp['N']} in SR proxy (ng={sp['ng']}); 95% UL on SR fraction {3/sp['N']:.1e} -> N_sel < {3/sp['N']*(Nacc or 0):.0f}"
    elif r.get("weighted"): prj = weighted_note
    tstat = "PENDING" if not ti else f"cluster {CL.get(s,'?')}, exit 0, LHE={ti['nlhe']}, Delphes={ti['n']} (executor-checked; verifier pending)"
    if s == "B_EW_Waajj_vbs": pass
    rows.append(dict(id=s, role=r["role"], sig=sig, sigsrc=r["sigma_source"], k=k, kf="x".join(r["br_factors_external"]), cuts=r["gen_cuts"], twin=TWIN.get(s, "mmjj>400 cross-check sample (not in b)" if "vbs" in s else "no generator mjj cut / not applicable"),
        need=need, plan=Nacc, nlhe=nl, weight=("fake-factor (probability) weights" if r.get("weighted") else "none (unit weights)") + ("; MLM matched, N = accepted" if acc < 0.9 else ""), prj=prj, seeds=sd, jobs=f"{njobs} x {ev_pj}" if njobs else "PENDING", cpu=cpu, gb=gb, test=tstat, flag=r.get("N_shortfall_flag"), flav=fl))
def fmt(x, f="%.4g"): return "PENDING" if x is None else f % x
L = ["| sample | role (s/b class) | σ (fb), source | BR / k (applied once) | generator cuts; twin evidence | N_required | N_planned (accepted) [LHE gen.] | weighting | projected N_eff in SR | seeds | jobs x ev/job (flavour) | CPU-h | storage GB | test job |", "|---|" + "---|"*13]
for x in rows:
    L.append(f"| {x['id']} | {x['role']} | {fmt(x['sig'])} ({x['sigsrc'][:60]}) | {x['kf']} = {x['k']:.5g} | {x['cuts'][:90]}; {x['twin']} | {fmt(x['need'], '%d')} | {fmt(x['plan'], '%d')} [{fmt(x['nlhe'], '%d')}] {('**flag ' + x['flag'] + '**') if x['flag'] else ''} | {x['weight']} | {x['prj']} | {x['seeds']} | {x['jobs']} ({x['flav'] or '-'}) | {fmt(x['cpu'], '%.1f')} | {fmt(x['gb'], '%.2f')} | {x['test']} |")
open(f"{WH}/work/plan_table.md", "w").write("\n".join(L) + "\n")
# ---- N check on the planned table (br_ledger.nmc_check = SPEC 4.2); pending / weighted rows listed explicitly
chk = {}; pend = []
for x in rows:
    if x["sig"] is None or x["plan"] is None: pend.append(x["id"]); continue
    if "weighted" in x["weight"] or "fake-factor" in x["weight"]: continue
    chk[x["id"]] = dict(N=x["plan"], sig=abs(x["sig"]))
msg = "PASS"
try: B.nmc_check({k: v for k, v in chk.items() if k in B.LEDGER})
except SystemExit as e: msg = "FAIL: " + str(e)
open(f"{WH}/work/plan_nmc.txt", "w").write(f"nmc_check on {len(chk)} planned rows (br_ledger.nmc_check, N >= max(50k, sigma*k*3000)): {msg}\nPENDING (sigma or N not yet known): {', '.join(pend)}\nweighted rows (N_eff>=10 rule in the PEAK region, NOT sigma*L): {'; '.join(x['id'] + ': ' + ('PENDING (no pilot json)' if 'PENDING' in x['prj'] else x['prj'][-80:]) for x in rows if 'fake-factor' in x['weight'])}\n")
open(f"{WH}/work/plan_totals.txt", "w").write(f"planned new production (rows with known N): jobs={tot['jobs']}, CPU-h={tot['cpu']:.0f}, storage={tot['gb']:.1f} GB (budget WH <= 200 GB)\n")
print(open(f"{WH}/work/plan_nmc.txt").read(), open(f"{WH}/work/plan_totals.txt").read())
# ---- machine-readable plan (consumed by make_prod_sub.py after G2) and the frozen-reuse table
json.dump({x["id"]: {k: v for k, v in x.items() if k in ("plan", "nlhe", "jobs", "seeds", "flav", "cpu", "gb")} | {"gp": None} for x in rows}, open(f"{WH}/work/plan.json", "w"), indent=1)
F = ["| frozen ZH sample (read-only reuse) | role | σ (fb), source | k | N available | N_required | generator cuts; correction | status |", "|---|---|---|---|---|---|---|---|"]
for r in M:
    if "path" not in r or r.get("in_bs") is False: continue
    c = r.get("c_gen_cut"); ct = "none" if not c else (f"C = {c['factor']} (stat {100*c['rel_err_stat']:.0f} %, syst = full difference {c['syst_full_difference']}); {c['source'][:90]}" if c.get("factor") else "C PENDING: " + c["source"][:110])
    F.append(f"| {r['id']} | {r['role']} | {r['sigma_fb']:.4g}, {r['sigma_source'][:40]} | {r['k_external']:.5g} | {r['N_available']} | {r['N_required']} | {r['gen_cuts'][:60]}; {ct} | {'N OK' if r.get('N_ok') else 'N SHORT'} |")
open(f"{WH}/work/plan_frozen.md", "w").write("\n".join(F) + "\n")
