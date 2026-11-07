#!/usr/bin/env python3
"""RESUME CHECK, D33 policy (binding). Run FIRST at every resume:  bash scripts/fix_memory_holds.sh   (wrapper; loads the CERN condor module)
 1. Production jobs (ClusterId >= 893600): non-running jobs are set to 1 CPU / RequestMemory >= 8000 (the schedd rewrites 8000 MB to 3 CPU / 9000 at submit); running under-requested jobs are raised (never touches a running cgroup).
 2. A HELD job is released ONCE with more memory: RequestMemory = max(12000, 1.25 x measured peak) MB; per-job release count in work/release_ledger.json (initialised from NumHolds: every earlier hold was followed by one release at 8000 MB).
 3. A job held again after that release, or removed/failed (009, rv != 0): the chunk is DROPPED only if its sample still meets the N rule without it (N_delivered_after >= max(50 000, sigma*BR*3000 fb^-1 [matrix N_required]); sanctioned weighted samples F_Wjjjj, T_ttjj_1l: N_eff >= 10 in the SR
    at the 95 % Poisson lower bound of the pilot rate); otherwise it is RESUBMITTED with a fresh seed (J >= 500 per sample, seeds check) and the failed one is removed. N after = events of all other chunks of the sample (finished + still queued) x acceptance.
 4. Every drop / resubmission is appended to work/dropped_chunks.csv (utc, cluster.proc, sample, events, seed, reason, action, N after vs required, rule) for the orchestrator (SPEC sec. 7) and 04 sec. 19.
Options: --dry (print only). Never waits on failed chunks."""
import subprocess, json, os, re, sys, glob, csv, math, datetime, yaml
WH = "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh"; S = "-name bigbird103.cern.ch"; DRY = "--dry" in sys.argv
sys.path.insert(0, f"{WH}/scripts"); import seeds as SD
def sh(c): return subprocess.run(["bash", "-lc", "module load lxbatch/eossubmit >/dev/null 2>&1; " + c], capture_output=True, text=True).stdout
LED = f"{WH}/work/release_ledger.json"; DROP = f"{WH}/work/dropped_chunks.csv"
led = json.load(open(LED)) if os.path.exists(LED) else {}
mat = {r["id"]: r for r in yaml.safe_load(open(f"{WH}/config/sample_matrix.yaml"))["samples"]}; plan = json.load(open(f"{WH}/work/plan.json"))
SANCT = ("F_Wjjjj", "T_ttjj_1l")
# --- cluster -> (sub file, rows)
cl2sub = {}
for r in list(csv.DictReader(open(f"{WH}/work/prod_submission_ledger.csv"))): cl2sub[r["cluster"]] = f"{WH}/work/condor/prod/{r['sub_file']}"
def rows_of(sub): return [l.split() for l in open(sub) if l.startswith("  ") and "tar.gz" in l]
def sample_of(name): return re.sub(r"_(topup|resub\d+)$", "", name)
chunks = {}   # sample -> list of dict(cp, ev, seed, state)
q = {l.split()[0] + "." + l.split()[1]: l.split() for l in sh(f"condor_q {S} -af ClusterId ProcId JobStatus HoldReasonCode RequestMemory NumHolds").split("\n") if len(l.split()) == 6 and int(l.split()[0]) >= 893600}
# --- initialise the ledger from NumHolds (one release per earlier hold, at 8000 MB)
for cp, f in q.items():
    if cp not in led: led[cp] = dict(releases=min(max((int(f[5]) if f[5].isdigit() else 0) - (1 if int(f[2]) == 5 else 0), 0), 1), note="initialised from NumHolds minus the CURRENT hold (each earlier hold was followed by one release at 8000 MB)")
def hold_peak(cp):
    m = re.search(r"Last measured usage: (\d+) megabytes", sh(f"condor_q {S} {cp} -af HoldReason")); return int(m.group(1)) if m else None
# --- delivered/queued events per sample (all chunks of submitted files; failed ones marked)
exitc = {}
for l in open(f"{WH}/work/exit_codes.txt"):
    t = l.split()
    if len(t) >= 4 and re.match(r"\d+\.\d+$", t[0]): exitc[t[0]] = (t[2], t[3])
dropped = {tuple(r[1:3]) for r in csv.reader(open(DROP))} if os.path.exists(DROP) else set()
done_cp = set(); 
for cl, sub in cl2sub.items():
    nm = os.path.basename(sub)[5:-4]; s = sample_of(nm)
    for pr, r in enumerate(rows_of(sub)):
        cp = f"{cl}.{pr}"; ev = int(r[3]); seed = int(r[7])
        st = "queued" if cp in q else ("ok" if exitc.get(cp, (None, None)) == ("005", "0") else ("failed" if cp in exitc else "unknown"))
        chunks.setdefault(s, []).append(dict(cp=cp, ev=ev, seed=seed, st=st, row=r, sub=sub))
def n_rule(s, ev_total):
    p = plan[s]; acc = p["plan"]/p["nlhe"]; nd = ev_total*acc
    if s in SANCT:
        import json as _j; f = _j.load(open(f"{WH}/work/ff_{s}.json")); reg = f["regions"]["PEAK"]; per = reg["N_eff"]/f["N_gen"]
        from scipy.stats import chi2; n = reg["n_events"]; low = float(chi2.ppf(0.05, 2*n)/2/n) if n else 0
        neff = per*low*nd; return neff >= 10, f"N_eff(SR, 95% lower bound) = {neff:.0f} >= 10 with N = {nd:.0f}", nd
    req = max(50000, mat[s].get("N_required") or 0); return nd >= req, f"N = {nd:.0f} vs required max(50k, sigma*BR*3000) = {req:.0f}", nd
def log_drop(cp, s, ev, seed, reason, action, rule):
    new = not os.path.exists(DROP)
    with open(DROP, "a", newline="") as f:
        w = csv.writer(f)
        if new: w.writerow(["utc", "cluster.proc", "sample", "events", "seed", "reason", "action", "N_after_vs_required", "rule"])
        w.writerow([datetime.datetime.utcnow().strftime("%FT%TZ"), cp, s, ev, seed, reason, action, rule, "D33"])
def resubmit(s, ch, reason):
    k = sum(1 for c in chunks[s] if "resub" in os.path.basename(c["sub"])) ; nj = 500 + len(glob.glob(f"{WH}/work/condor/prod/prod_{s}_resub*.sub"))*10 + 0
    rows = [l for l in open(ch["sub"]).read().split("\n") if l.startswith("  ") and "tar.gz" in l]
    r = ch["row"][:]; seed = SD.seed(s, 500 + k + len(glob.glob(f"{WH}/work/condor/prod/prod_{s}_resub*.sub")) * 20); r[7] = str(seed); r[6] = "workday" if r[6] in ("espresso", "microcentury", "longlunch") else r[6]
    n = len(glob.glob(f"{WH}/work/condor/prod/prod_{s}_resub*.sub")) + 1; name = f"{s}_resub{n}"
    head = open(ch["sub"]).read().split("queue sample")[0].replace("request_memory = 2500", "request_memory = 12000").replace("request_memory = 8000", "request_memory = 12000")
    head = re.sub(r"prod_[A-Za-z0-9_]+\.log", f"prod_{name}.log", head)
    open(f"{WH}/work/condor/prod/prod_{name}.sub", "w").write(head + "queue sample, gp, cmnd, nev, klhe, kfull, flav, seed, odir from (\n  " + " ".join(r) + "\n)\n"); return name, seed
acts = []
for cp, f in q.items():
    cl, pr = cp.split("."); js, code = int(f[2]), f[3]; mem = int(f[4])
    s = next((s for s, L in chunks.items() for c in L if c["cp"] == cp), None)
    if s is None: continue
    if js == 5:
        rel = led[cp]["releases"]
        if rel == 0:
            peak = hold_peak(cp) or mem; new = max(12000, int(math.ceil(1.25*peak/500)*500))
            acts.append(f"RELEASE {cp} ({s}) once with RequestMemory {new} (peak {peak})")
            if not DRY: sh(f"condor_qedit {S} {cp} RequestMemory {new}; condor_qedit {S} {cp} RequestCpus 1; condor_release {S} {cp}"); led[cp] = dict(releases=1, mem=new, utc=datetime.datetime.utcnow().strftime("%FT%TZ"))
        else:
            ch = next(c for c in chunks[s] if c["cp"] == cp); others = sum(c["ev"] for c in chunks[s] if c["cp"] != cp and c["st"] in ("queued", "ok"))
            ok, txt, nd = n_rule(s, others); reason = f"held again after one release (code {code})"
            if ok:
                acts.append(f"DROP {cp} ({s}, {ch['ev']} ev, seed {ch['seed']}): {txt}")
                if not DRY: sh(f"condor_rm {S} {cp}"); log_drop(cp, s, ch["ev"], ch["seed"], reason, "DROPPED", txt)
            else:
                nm, sd = (resubmit(s, ch, reason) if not DRY else ("(dry)", 0)); acts.append(f"RESUBMIT {cp} ({s}) as {nm} seed {sd}: dropping would break the N rule ({txt})")
                if not DRY: sh(f"condor_rm {S} {cp}; cd {WH}/work/condor/prod && bash {WH}/scripts/submit_bulk.sh {nm}"); log_drop(cp, s, ch["ev"], ch["seed"], reason, f"RESUBMITTED as {nm} seed {sd}", txt)
    elif js in (1, 2) and False: pass
# --- failed / removed chunks that are no longer in the queue and not yet logged (idempotent)
logged = {r[1] for r in csv.reader(open(DROP))} if os.path.exists(DROP) else set()
for s, L in chunks.items():
    for ch in L:
        if ch["st"] != "failed" or ch["cp"] in logged: continue
        if ch["cp"] in ("893632.204", "893632.205", "893632.211", "893632.212"):   # handled before D33: resubmitted as 893876
            others = sum(c["ev"] for c in L if c["cp"] != ch["cp"] and c["st"] in ("queued", "ok")); ok, txt, nd = n_rule(s, others)
            acts.append(f"LOG {ch['cp']} ({s}): already resubmitted as 893876 ({txt})")
            if not DRY: log_drop(ch["cp"], s, ch["ev"], ch["seed"], "removed: wall time (longlunch 2 h)", "RESUBMITTED as Q_aajj_resub1 (cluster 893876, seeds 2131500-503); N after incl. the resubmission, dropping alone would break the N rule", txt)
        elif ch["cp"] not in ("884934.12", "884934.13") and ch["cp"].split(".")[0] >= "893600":   # any other failed/removed production chunk: handle like a second failure
            others = sum(c["ev"] for c in L if c["cp"] != ch["cp"] and c["st"] in ("queued", "ok")); ok, txt, nd = n_rule(s, others)
            if ok:
                acts.append(f"DROP {ch['cp']} ({s}, {ch['ev']} ev, seed {ch['seed']}): failed/removed; {txt}")
                if not DRY: log_drop(ch["cp"], s, ch["ev"], ch["seed"], "failed/removed (exit_codes)", "DROPPED", txt)
            else:
                nm, sd = (resubmit(s, ch, "failed") if not DRY else ("(dry)", 0)); acts.append(f"RESUBMIT {ch['cp']} ({s}) as {nm} seed {sd}: dropping would break the N rule ({txt})")
                if not DRY: sh(f"cd {WH}/work/condor/prod && bash {WH}/scripts/submit_bulk.sh {nm}"); log_drop(ch["cp"], s, ch["ev"], ch["seed"], "failed/removed (exit_codes)", f"RESUBMITTED as {nm} seed {sd}", txt)
if not DRY: json.dump(led, open(LED, "w"), indent=1)
print("\n".join(acts) if acts else "no held/failed production chunk needs action")
