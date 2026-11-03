#!/usr/bin/env python3
"""Generate HTCondor submit files for gridpack builds and ONE test job per sample type (wrappers reused unmodified from p2/lib/scripts/condor).
Seeds per SPEC 3.4 with uniqueness asserted. Usage: make_condor.py   (writes work/condor/*.sub, prints seed table). Does NOT submit."""
import yaml, os, sys, itertools
WH = "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh"; E = "/eos/user/r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh"
LIB = "/eos/user/r/rjiang/vbs_zh_codex_starter/p2/lib"
P, R = 2, 11
reg = yaml.safe_load(open(f"{WH}/config/sample_registry.yaml"))["samples"]
def seed(idx, J): return 1_000_000*P + 10_000*R + J + 1000*idx
GP = ["S_EW_WHjj", "H_QCD_WH_mlm", "H_ttH_1l", "B_EW_Waajj_vbs", "B_QCD_Waajj_vbs", "B_QCD_Waajj_nomjj", "F_EW_Wajj_vbs", "F_QCD_Wajj_vbs", "F_QCD_Wajj_nomjj", "F_Wjj_pilot", "F_Wajj_pilot"]
# sample: (cmnd, nev, flavour, keep_lhe, keep_full)
TEST = {"S_EW_WHjj": ("py8_whjj_haa.cmnd", 2000, "microcentury", 1, 1), "H_QCD_WH_mlm": ("py8_mlm_wh_haa.cmnd", 4000, "longlunch", 1, 1),
        "H_ttH_1l": ("py8_h_haa.cmnd", 2000, "microcentury", 1, 1), "B_EW_Waajj_vbs": ("py8_generic_dipole.cmnd", 2000, "longlunch", 1, 1),
        "F_Wjj_pilot": ("py8_generic.cmnd", 5000, "longlunch", 1, 1), "F_Wajj_pilot": ("py8_generic.cmnd", 5000, "longlunch", 1, 1),
        "B_QCD_Waajj_nomjj": ("py8_generic.cmnd", 2000, "longlunch", 1, 1), "F_QCD_Wajj_nomjj": ("py8_generic.cmnd", 2000, "longlunch", 1, 1)}  # last two: twins for generator-cut safety (submitted separately as test_wh_twins.sub)
NC = {"B_EW_Waajj_vbs": (8, 16000, "testmatch"), "B_QCD_Waajj_vbs": (8, 16000, "testmatch"), "B_QCD_Waajj_nomjj": (8, 16000, "testmatch")}
seeds = {}
for s in GP: seeds[(s, "gridpack")] = seed(reg[s], 0)
for s in TEST: seeds[(s, "test")] = seed(reg[s], 1)
assert len(set(seeds.values())) == len(seeds), "seed collision"
assert all(0 < v < 900_000_000 for v in seeds.values())
os.makedirs(f"{WH}/work/condor", exist_ok=True)
for d in ("gridpacks", "test"): os.makedirs(f"{WH}/work/{d}", exist_ok=True)
for s in TEST: os.makedirs(f"{WH}/work/test/{s}", exist_ok=True)
hdr = "universe = vanilla\nshould_transfer_files = YES\nwhen_to_transfer_output = ON_EXIT\n"
g = hdr + f"""executable = {LIB}/scripts/condor/make_gridpack.sh
arguments = $(card) $(gseed) {E}/work/gridpacks $(ncore)
transfer_input_files = {LIB}/scripts/setup_stack.sh, {E}/cards/prod/$(card).mg5
output = {E}/work/condor/gp_$(card).out
error = {E}/work/condor/gp_$(card).err
log = {E}/work/condor/gridpacks_wh.log
request_cpus = $(ncore)
request_memory = $(mem)
request_disk = 20000000
+JobFlavour = "$(flav)"
max_retries = 1
queue card, gseed, ncore, mem, flav from (
"""
for s in GP:
    nc, mem, fl = NC.get(s, (4, 8000, "workday")); g += f"  {s} {seeds[(s,'gridpack')]} {nc} {mem} {fl}\n"
open(f"{WH}/work/condor/gridpacks_wh.sub", "w").write(g + ")\n")
t = hdr + f"""executable = {LIB}/scripts/condor/run_job.sh
arguments = $(sample) {E}/work/gridpacks/$(sample)_gridpack_s$(gseed).tar.gz $(nev) $(seed) $(cmnd) {E}/work/test/$(sample) $(klhe) $(kfull)
transfer_input_files = {LIB}/scripts/setup_stack.sh, {LIB}/scripts/run_py8_delphes.sh, {LIB}/scripts/slim_gentruth.py, {LIB}/cards/phase03_smoke/py8_common_CP5.cmnd, {E}/cards/$(cmnd), {LIB}/cards/phase04_candidates/delphes_card_CMS_slim_v1.tcl
output = {E}/work/condor/test_$(sample).out
error = {E}/work/condor/test_$(sample).err
log = {E}/work/condor/test_wh.log
request_cpus = 1
request_memory = 2500
+JobFlavour = "$(flav)"
max_retries = 2
success_exit_code = 0
on_exit_hold = (ExitCode =?= 19)
on_exit_hold_reason = "gridpack not yet available"
periodic_release = (HoldReasonCode =?= 3) && ((time() - EnteredCurrentStatus) > 1800) && (NumJobStarts < 200)
queue sample, gseed, cmnd, nev, klhe, kfull, flav, seed from (
"""
for s, (cm, nev, fl, kl, kf) in TEST.items():
    if "nomjj" not in s: t += f"  {s} {seeds[(s,'gridpack')]} {cm} {nev} {kl} {kf} {fl} {seeds[(s,'test')]}\n"
open(f"{WH}/work/condor/test_wh.sub", "w").write(t + ")\n")
lines = t.split("queue sample")[0] + "queue sample, gseed, cmnd, nev, klhe, kfull, flav, seed from (\n" + "".join(f"  {s} {seeds[(s,'gridpack')]} {cm} {nev} {kl} {kf} {fl} {seeds[(s,'test')]}\n" for s, (cm, nev, fl, kl, kf) in TEST.items() if "nomjj" in s) + ")\n"
open(f"{WH}/work/condor/test_wh_twins.sub", "w").write(lines)
print("seeds (unique, asserted):"); [print(f"  {k[0]:20s} {k[1]:9s} {v}") for k, v in seeds.items()]
# range-overlap warning vs other runs of the same formula (SPEC 3.4): R spacing is 10000, J+1000*idx exceeds it for idx>=10
mx = max(1000*i + 1 for i in reg.values()); print("max J-part =", mx, "(> 10000 => seed ranges of R=11 and R=12.. overlap numerically; see D-WH-1)" if mx >= 10000 else "")
