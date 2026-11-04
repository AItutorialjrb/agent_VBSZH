#!/usr/bin/env python3
"""Exit codes from the HTCondor user logs (work/condor/*.log) -> work/exit_codes.txt: cluster.proc, last event (005 terminated / 009 aborted / 012 held), return value, #starts."""
import re, glob, collections
ev = collections.OrderedDict()
for lg in sorted(glob.glob("work/condor/*.log")):
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
bad = [k for k, d in ev.items() if d["last"] != "005" or d["rv"] != 0]; print(len(ev), "procs;", len(bad), "not (terminated, rv 0):", bad[:30])
