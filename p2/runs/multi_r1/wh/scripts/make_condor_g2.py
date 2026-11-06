#!/usr/bin/env python3
"""G2-prep submit files (pre-G2 allowed: gridpacks, ONE test job per sample type, twin/pilot samples). Does NOT submit.
Writes work/condor/g2_gridpacks.sub, g2_tests.sub, g2_twins_qcd.sub, g2_twins_ew.sub and config/seeds_g2.txt. Seeds: scripts/seeds.py (uniqueness asserted incl. preG1 list).
Usage: python3 scripts/make_condor_g2.py"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__)); import seeds as S
WH = S.WH; E = "/eos/user/r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh"; LIB = "/eos/user/r/rjiang/vbs_zh_codex_starter/p2/lib"
ZHGP = "/eos/user/r/rjiang/vbs_zh_codex_starter/production/gridpacks"
# new gridpack builds: sample: (ncore, mem MB, flavour)
GP = {"S_EW_WHjj_taunu": (4, 8000, "workday"), "H_QCD_WHjj_fixed": (4, 8000, "workday"), "I_WHjj": (4, 8000, "workday"), "H_tHq_lep": (4, 8000, "workday"),
      "H_tHW_1l": (4, 8000, "workday"), "T_tta_1l": (4, 8000, "workday"), "T_ttaa_1l": (4, 8000, "workday"), "T_tWa_1l": (4, 8000, "workday"), "T_tt_1l": (4, 8000, "workday"),
      "F_EW_Wajj_nomjj": (4, 8000, "workday"), "V_WZa_WH": (4, 8000, "workday"), "V_WWa_WH": (4, 8000, "workday"), "V_ZZa_WH": (4, 8000, "workday"),
      "B_EW_Waajj_nomjj": (8, 16000, "testmatch"), "F_Wjjjj": (8, 16000, "testmatch"), "T_ttjj_1l": (8, 16000, "testmatch")}
def gpfile(s):  # gridpack location
    if s in GP or s.startswith("K_EW_WHjj") or s in ("F_QCD_Wajjj_nomjj", "Q_aajjj") or s in ("Q_aajj", "H_VBFH_jj", "H_ggF_jj", "F_QCD_llajj_loose"): return f"{E}/work/gridpacks/{s}_gridpack_s{S.seed(s,100)}.tar.gz"
    return {"H_ggZH_wh": f"{ZHGP}/H_ggZH_py8dec_gridpack_s1363200.tar.gz", "H_ttH_dilep_wh": f"{ZHGP}/H_ttH_gridpack_s1360500.tar.gz", "H_ZH_tautau_wh": f"{ZHGP}/H_ZH_tautau_gridpack_s1360700.tar.gz"}.get(s) \
        or f"{E}/work/gridpacks/{s}_gridpack_s{ {'F_EW_Wajj_vbs':2126000,'F_QCD_Wajj_vbs':2127000}[s] }.tar.gz"
# ONE test job per type: sample: (cmnd, nev, flavour)
TEST = {"S_EW_WHjj_taunu": ("py8_whjj_haa.cmnd", 2000, "microcentury"), "H_QCD_WHjj_fixed": ("py8_h_haa.cmnd", 2000, "microcentury"), "I_WHjj": ("py8_whjj_haa.cmnd", 2000, "microcentury"),
        "H_tHq_lep": ("py8_h_haa.cmnd", 2000, "microcentury"), "H_tHW_1l": ("py8_h_haa.cmnd", 2000, "microcentury"),
        "T_tta_1l": ("py8_generic.cmnd", 2000, "microcentury"), "T_ttaa_1l": ("py8_generic.cmnd", 2000, "microcentury"), "T_tWa_1l": ("py8_generic.cmnd", 2000, "microcentury"),
        "T_tt_1l": ("py8_generic.cmnd", 2000, "microcentury"), "T_ttjj_1l": ("py8_generic.cmnd", 5000, "longlunch"), "F_Wjjjj": ("py8_generic.cmnd", 5000, "longlunch"),
        "F_EW_Wajj_vbs": ("py8_generic_dipole.cmnd", 2000, "longlunch"), "F_QCD_Wajj_vbs": ("py8_generic.cmnd", 2000, "longlunch"),
        "F_EW_Wajj_nomjj": ("py8_generic_dipole.cmnd", 2000, "longlunch"), "B_EW_Waajj_nomjj": ("py8_generic_dipole.cmnd", 2000, "longlunch"),
        "V_WZa_WH": ("py8_generic.cmnd", 2000, "microcentury"), "V_WWa_WH": ("py8_generic.cmnd", 2000, "microcentury"), "V_ZZa_WH": ("py8_generic.cmnd", 2000, "microcentury"),
        "H_ggZH_wh": ("py8_ggzh_zll_haa.cmnd", 2000, "microcentury"), "H_ttH_dilep_wh": ("py8_h_haa.cmnd", 2000, "microcentury"), "H_ZH_tautau_wh": ("py8_mlm_zh_haa.cmnd", 4000, "longlunch")}
# large twin pilot (QCD twins have gridpacks): sample: (cmnd, nev/job, njobs); jobs J=110..
TW_QCD = {"B_QCD_Waajj_nomjj": ("py8_generic.cmnd", 8000, 5, 2125000), "F_QCD_Wajj_nomjj": ("py8_generic.cmnd", 8000, 5, 2128000)}
allseeds = []
os.makedirs(f"{WH}/work/condor", exist_ok=True)
hdr = "universe = vanilla\nshould_transfer_files = YES\nwhen_to_transfer_output = ON_EXIT\n"
g = hdr + f"""executable = {LIB}/scripts/condor/make_gridpack.sh
arguments = $(card) $(gseed) {E}/work/gridpacks $(ncore)
transfer_input_files = {LIB}/scripts/setup_stack.sh, {E}/cards/prod/$(card).mg5
output = {E}/work/condor/gp_$(card).out
error = {E}/work/condor/gp_$(card).err
log = {E}/work/condor/g2_gridpacks.log
request_cpus = $(ncore)
request_memory = $(mem)
request_disk = 20000000
+JobFlavour = "$(flav)"
max_retries = 1
queue card, gseed, ncore, mem, flav from (
"""
rows = []
for s, (nc, mem, fl) in GP.items():
    sd = S.seed(s, 100); allseeds.append(sd); rows.append(f"gridpack {s} {sd}"); g += f"  {s} {sd} {nc} {mem} {fl}\n"
open(f"{WH}/work/condor/g2_gridpacks.sub", "w").write(g + ")\n")
def tsub(rows_, log):
    return hdr + f"""executable = {LIB}/scripts/condor/run_job.sh
arguments = $(sample) $(gp) $(nev) $(seed) $(cmnd) {E}/work/$(odir)/$(sample) $(klhe) $(kfull)
transfer_input_files = {LIB}/scripts/setup_stack.sh, {LIB}/scripts/run_py8_delphes.sh, {LIB}/scripts/slim_gentruth.py, {LIB}/cards/phase03_smoke/py8_common_CP5.cmnd, {E}/cards/$(cmnd), {LIB}/cards/phase04_candidates/delphes_card_CMS_slim_v1.tcl
output = {E}/work/condor/$(odir)_$(sample)_$(seed).out
error = {E}/work/condor/$(odir)_$(sample)_$(seed).err
log = {E}/work/condor/{log}
request_cpus = 1
request_memory = 2500
+JobFlavour = "$(flav)"
max_retries = 2
success_exit_code = 0
on_exit_hold = (ExitCode =?= 19)
on_exit_hold_reason = "gridpack not yet available"
periodic_release = (HoldReasonCode =?= 3) && ((time() - EnteredCurrentStatus) > 1800) && (NumJobStarts < 200)
queue sample, gp, cmnd, nev, klhe, kfull, flav, seed, odir from (
""" + "".join(rows_) + ")\n"
t = []
for s, (cm, nev, fl) in TEST.items():
    sd = S.seed(s, 101); allseeds.append(sd); rows.append(f"test {s} {sd}"); os.makedirs(f"{WH}/work/test/{s}", exist_ok=True)
    t.append(f"  {s} {gpfile(s)} {cm} {nev} 1 1 {fl} {sd} test\n")
open(f"{WH}/work/condor/g2_tests.sub", "w").write(tsub(t, "g2_tests.log"))
tw = []
for s, (cm, nev, nj, gs) in TW_QCD.items():
    os.makedirs(f"{WH}/work/twin/{s}", exist_ok=True)
    for j in range(nj):
        sd = S.seed(s, 110 + j); allseeds.append(sd); rows.append(f"twin {s} {sd}")
        tw.append(f"  {s} {E}/work/gridpacks/{s}_gridpack_s{gs}.tar.gz {cm} {nev} 1 0 longlunch {sd} twin\n")
open(f"{WH}/work/condor/g2_twins_qcd.sub", "w").write(tsub(tw, "g2_twins_qcd.log"))
# EW twins (production-size, LHE kept): submit only after the EW test jobs (884935) succeeded; gridpacks are the nomjj ones built in 884934
TW_EW = {"F_EW_Wajj_nomjj": ("py8_generic_dipole.cmnd", 8000, 5), "B_EW_Waajj_nomjj": ("py8_generic_dipole.cmnd", 8000, 5)}
tw = []
for s, (cm, nev, nj) in TW_EW.items():
    os.makedirs(f"{WH}/work/twin/{s}", exist_ok=True)
    for j in range(nj):
        sd = S.seed(s, 110 + j); allseeds.append(sd); rows.append(f"twin {s} {sd}")
        tw.append(f"  {s} {gpfile(s)} {cm} {nev} 1 0 longlunch {sd} twin\n")
open(f"{WH}/work/condor/g2_twins_ew.sub", "w").write(tsub(tw, "g2_twins_ew.log"))
S.check(allseeds)
open(f"{WH}/config/seeds_g2.txt", "w").write("# G2-prep seeds (kind sample seed); uniqueness asserted by scripts/seeds.py incl. preG1 list\n" + "\n".join(rows) + "\n")
if __name__ == "__main__": print(len(allseeds), "seeds unique, no preG1 collision")
