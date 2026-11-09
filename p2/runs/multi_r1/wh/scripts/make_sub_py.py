#!/usr/bin/env python3
"""Write a condor submit file for job_py.sh. Usage: make_sub_py.py <mode skim|rate> <out.sub> <outdir> <memMB> <flavour> <sample[:every_k]> ...   (files: production/wh/<sample>/*.root without _gen)
Skips files whose output exists (idempotent)."""
import sys, glob, os
mode, sub, outdir, mem, flav = sys.argv[1:6]; WH = "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh"; PR = "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/production/wh"
ZF = "/eos/home-r/rjiang/vbs_zh_codex_starter/production"
ZH = {"ZH_Zaajj_QCD_nomjj_lostlep": [f"{ZF}/final/B_QCD_zaajj_nomjj"], "ZH_Zaajj_EW_lostlep": [f"{ZF}/final/B_EW_zaajj_vbs_is{x}" for x in ("1h", "2", "3")],
      "ZH_Zajj_eFake": [f"{ZF}/final/F_QCD_llajj_vbs", f"{ZF}/final/F_EW_llajj_vbs"], "ZH_EW_ZHjj_lostlep": [f"{ZF}/v1/ew_zhjj_zll"], "ZH_QCD_ZHjj_lostlep": [f"{ZF}/v1/qcd_zhjj_zll"]}
GROUP = {"ZH_Zajj_eFake": 30, "ZH_Zaajj_QCD_nomjj_lostlep": 4, "ZH_Zaajj_EW_lostlep": 4, "ZH_EW_ZHjj_lostlep": 4, "ZH_QCD_ZHjj_lostlep": 4, "H_QCD_WHjj_fixed": 2}
os.makedirs(outdir, exist_ok=True); ext = {"skim": "npz", "rate": "json"}[mode]; q = []
for sp in sys.argv[6:]:
    s, k = (sp.split(":") + ["1"])[:2]
    dirs = [f"{PR}/{s}"] if s not in ZH else ZH[s]
    files = sorted(f for d in dirs for f in glob.glob(f"{d}/*.root") if not f.endswith("_gen.root") and not f.endswith("_full.root"))[::int(k)]
    todo = [f for f in files if not os.path.exists(f"{outdir}/{mode}_{s}__{os.path.basename(f)[:-5]}.json")]
    G = GROUP.get(s, 1)
    for j in range(0, len(todo), G): q.append(f"{s} " + ",".join(todo[j:j+G]))
tr = f"{WH}/scripts/job_py.sh, /eos/home-r/rjiang/vbs_zh_codex_starter/p2/lib/scripts/setup_stack.sh, {WH}/scripts/skim.py, {WH}/scripts/rate_genuine.py" + (f", {WH}/work/bgmodel/rate_table.json" if mode == "skim" else "")
open(sub, "w").write(f"""universe = vanilla
should_transfer_files = YES
when_to_transfer_output = ON_EXIT
executable = {WH}/scripts/job_py.sh
arguments = {mode} $(s) {outdir} $(f)
transfer_input_files = {tr[tr.index(',')+2:]}
output = {WH}/work/condor/py_{mode}_$(Cluster).$(Process).out
error = {WH}/work/condor/py_{mode}_$(Cluster).$(Process).err
log = {WH}/work/condor/py_{mode}.log
request_cpus = 1
request_memory = {mem}
+JobFlavour = "{flav}"
max_retries = 2
queue s, f from (
""" + "\n".join("  " + x for x in q) + "\n)\n")
print(len(q), "jobs ->", sub)
