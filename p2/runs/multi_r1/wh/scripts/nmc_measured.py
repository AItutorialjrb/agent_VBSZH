#!/usr/bin/env python3
"""N rule on the MEASURED delivered N, from the package SAMPLES.csv (writes work/nmc_measured.txt; refuses zero rows; fails loudly):
for every row with N_generated > 0 (WH production rows and the READ-ONLY frozen ZH rows): need = max(50 000, sigma_pb*1e3 * k * 3000 fb^-1) against the measured N_Delphes (accepted events; for the matched rows H_QCD_WH_mlm / H_ZH_tautau_wh the accepted N, as in the plan);
exempt (named): F_Wjjjj and T_ttjj_1l (human-sanctioned D4/D27, gated by N_eff, see 04 sec. 20). The need INCLUDES the x1.05 sigma margin of the plan (need = max(50 000, 1.05 x sigma x k x 3000 fb^-1)). Rows NOT checked are named in the output: F_QCD_Wajj_nomjj (WITHDRAWN, N = 0) and H_ggF_jj (pending, v1.1).
Usage: python3 scripts/nmc_measured.py"""
import csv, sys
PR = "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/production/wh"; WH = "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh"
EXEMPT = ("F_Wjjjj", "T_ttjj_1l"); rows = [r for r in csv.DictReader(open(f"{PR}/SAMPLES.csv")) if int(r["N_generated_LHE"] or 0) > 0]
if not rows: sys.exit("nmc_measured: ZERO rows: refusing to report PASS")
out = []; npass = nex = 0; bad = []; marg = []
for r in rows:
    s = r["sample"]; N = int(r["N_Delphes"]); sig = float(r["sigma_pb_pre_decay"])*1e3*float(r["k"])*3000.0; need = max(50000.0, sig*1.05); need_m = need   # the need INCLUDES the 5 % sigma margin of the plan (sigma_N = sigma x 1.05)
    if s in EXEMPT: st = "EXEMPT (human-sanctioned D4/D27; N_eff gate)"; nex += 1
    elif N >= need: st = "PASS"; npass += 1
    else: st = "FAIL"; bad.append(s)
    if s not in EXEMPT and N < need_m: marg.append(s)
    out.append(f"{s:30s} N_Delphes {N:>10d}  need(incl. 1.05) {need:>12.0f}  {st}")
head = f"nmc_check on the MEASURED delivered N (SAMPLES.csv): {len(rows)} rows checked = {npass} PASS + {nex} EXEMPT ({', '.join(EXEMPT)}) + {len(bad)} FAIL; N >= max(50k, 1.05*sigma*k*3000 fb^-1) (the x1.05 margin of the plan is INCLUDED), N = N_Delphes (accepted events). NOT CHECKED (named): F_QCD_Wajj_nomjj (WITHDRAWN, N = 0) and H_ggF_jj (pending, v1.1); Q_aajjj is checked."
tail = "rows with N = 0 listed in SAMPLES.csv and therefore not checked: " + ", ".join(r["sample"] for r in csv.DictReader(open(f"{PR}/SAMPLES.csv")) if int(r["N_generated_LHE"] or 0) == 0)
open(f"{WH}/work/nmc_measured.txt", "w").write(head + "\n" + "\n".join(out) + "\n" + tail + "\n"); print(head); print(tail)
if bad: sys.exit("N_MC policy VIOLATED: " + ", ".join(bad))
