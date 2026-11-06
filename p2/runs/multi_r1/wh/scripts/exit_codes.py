#!/usr/bin/env python3
"""Exit codes from the HTCondor user logs (work/condor/*.log) -> work/exit_codes.txt: cluster.proc, last event (005 terminated / 009 aborted / 012 held), return value, #starts."""
import re, glob, collections
ev = collections.OrderedDict()
for lg in sorted(glob.glob("work/condor/*.log") + glob.glob("work/condor/prod/*.log")):
    txt = open(lg).read(); 
    for blk in txt.split("\n...\n"):
        m = re.match(r"(\d{3}) \((\d+)\.(\d+)\.\d+\)", blk.strip())
        if not m: continue
        code, cl, pr = m.group(1), m.group(2), int(m.group(3)); d = ev.setdefault((cl, pr, lg.split('/')[-1]), dict(starts=0, last=None, rv=None))
        if code == "001": d["starts"] += 1
        if code in ("005", "009", "012", "004"): d["last"] = code
        r = re.search(r"return value (\d+)", blk)
        if code == "005" and r: d["rv"] = int(r.group(1))
with open("work/exit_codes.txt", "w") as f:
    f.write("# cluster.proc log last_event(005=terminated,012=held,009=aborted) return_value starts\n")
    for (cl, pr, lg), d in ev.items(): f.write(f"{cl}.{pr} {lg} {d['last']} {d['rv']} {d['starts']}\n")
LABEL = {   # every non-(terminated, rv 0) proc must carry an explicit reason (VERIFY #12 item 4); unlabelled ones are listed as UNLABELLED
 "884934.12": "removed/aborted (009); superseded by a later successful job per the verifier resume audit; no output from this proc is used",
 "884934.13": "NO TERMINAL EVENT in the (corrupt/interleaved) log; B_EW_Waajj_nomjj gridpack finished (status rc=0 11/05 02:16Z, tar ok) then held and removed 11/06 03:17Z by SYSTEM_PERIODIC_REMOVE; result used only after test 893009 (LHE=Delphes)",
 "884935.10": "removed/aborted (009); superseded by a later successful job per the verifier resume audit; no output from this proc is used",
 "884935.14": "removed/aborted (009); superseded by a later successful job per the verifier resume audit; no output from this proc is used",
 "884935.15": "removed/aborted (009); superseded by a later successful job per the verifier resume audit; no output from this proc is used",
 "884935.16": "removed/aborted (009); superseded by a later successful job per the verifier resume audit; no output from this proc is used", "884935.17": "removed/aborted (009); superseded by a later successful job per the verifier resume audit; no output from this proc is used",
 "885044.0": "NO TERMINAL rv: V_ZZa_WH gridpack, output-transfer eviction (Kerberos, code 12) after the script finished (status rc=0, tar ok); test 893010 closed it",
 "885043.3": "removed/aborted (009); superseded by a later successful job per the verifier resume audit; no output from this proc is used",
 "885122.2": "NO TERMINAL EVENT: H_ggF_jj gridpack failed on wall time (1-day flavour), no tarball; resubmitted as 893012 (seed 2133103)",
 "893011.0": "removed by the executor before any output: seed 2133101 collided with the H_ggF_jj test seed (J=101); replaced by 893012",
 "893012.0": "RUNNING at the time of writing (H_ggF_jj gridpack, testmatch); not an error",
 "884457.3": "removed/aborted (009); superseded by a later successful job per the verifier resume audit; no output from this proc is used"}
import subprocess
_q = subprocess.run(["bash", "-lc", "module load lxbatch/eossubmit >/dev/null 2>&1; condor_q -name bigbird103.cern.ch -af ClusterId ProcId JobStatus"], capture_output=True, text=True).stdout.split("\n")
QUEUE = {f"{l.split()[0]}.{l.split()[1]}": {"1": "IDLE", "2": "RUNNING", "5": "HELD"}.get(l.split()[2], "status " + l.split()[2]) for l in _q if len(l.split()) == 3}
bad = [k for k, d in ev.items() if (d["last"] != "005" or d["rv"] != 0) and f"{k[0]}.{k[1]}" not in QUEUE]
inq = [k for k in ev if f"{k[0]}.{k[1]}" in QUEUE and f"{k[0]}.{k[1]}" not in LABEL]
with open("work/exit_codes.txt", "a") as f:
    f.write("# NON-ZERO / NOT TERMINATED, with reasons:\n")
    for (cl, pr, lg) in bad: f.write(f"{cl}.{pr} {LABEL.get(f'{cl}.{pr}', 'UNLABELLED')}\n")
print(len(inq), "procs in queue (IDLE/RUNNING/HELD, not errors); HELD:", [f"{c}.{p}" for c, p, _ in inq if QUEUE[f"{c}.{p}"] == "HELD"]); print(len(ev), "procs;", len(bad), "not (terminated, rv 0); unlabelled:", [f"{c}.{p}" for c, p, _ in bad if f"{c}.{p}" not in LABEL])
