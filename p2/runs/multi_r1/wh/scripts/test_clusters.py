#!/usr/bin/env python3
"""sample -> condor cluster.proc of the test job that produced its test output (terminated, rv 0), from the submit-file queue order and the condor event logs (replaces the hand-written CL table; recheck item 10: no 'cluster ?')."""
import glob, re, json, os
C = "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh/work/condor"
res = {}
for sub in sorted(glob.glob(f"{C}/*.sub")):
    t = open(sub).read(); lg = re.search(r"^log\s*=\s*(\S+)", t, re.M)
    if not lg or "test" not in os.path.basename(sub) or "twins" in sub: continue
    lgp = f"{C}/" + os.path.basename(lg.group(1))
    if not os.path.exists(lgp): continue
    rows = []; inq = False
    for l in t.split("\n"):
        if l.startswith("queue"): inq = True; continue
        if inq and l.startswith("  "): rows.append(l.split()[0])
    L = open(lgp, errors="replace").read().replace("\x00", "")
    blocks = re.split(r"\n\.\.\.\n", L); st = {}
    for b in blocks:
        m = re.search(r"^(\d{3}) \((\d+)\.(\d+)\.\d+\)", b.strip("\n"), re.M)
        if not m: continue
        code, cl, pr = m.group(1), m.group(2), int(m.group(3))
        if code == "005" and re.search(r"return value 0", b): st[(cl, pr)] = "ok"
    for (cl, pr), v in st.items():
        if v == "ok" and pr < len(rows): res[rows[pr]] = f"{cl}.{pr}"
json.dump(res, open("/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh/work/test_clusters.json", "w"), indent=1, sort_keys=True); print(len(res), "samples with a terminated rv-0 test job")
