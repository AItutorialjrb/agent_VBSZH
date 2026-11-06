#!/usr/bin/env python3
"""Coupling-study cards for WH (brief v2 step 2): HC_NLO_X0_kVV (patched, ZH lib scripts/models/make_hc_kvv.sh), same generator cuts as S_EW_WHjj.
kappa_W = kSM*kSMW, kappa_Z = kSM*kSMZ, lambda_WZ = kSMW/kSMZ. Param block copied from the ZH coupling cards (lib/cards/coupling)."""
import re, os
WH="/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh"; LIB="/eos/home-r/rjiang/vbs_zh_codex_starter/p2/lib/cards/coupling"
S=open(f"{WH}/cards/prod/S_EW_WHjj.mg5").read().split("\n")
runset=[l for l in S if l.startswith("set run_card")]
r2=2**0.5
PTS={ # name: (cosa,kSM,kSMZ,kSMW,kAzz,kAww)
 "lam_m100":(1,1,1,-1,0,0),"lam_m050":(1,1,1,-0.5,0,0),"lam_p000":(1,1,1,0,0,0),"lam_p050":(1,1,1,0.5,0,0),
 "lam_p100":(1,1,1,1,0,0),"lam_p150":(1,1,1,1.5,0,0),
 "kap_W15_Z075":(1,0.75,1,2,0,0),          # kW=1.5 kZ=0.75 (lambda=2)  closure point
 "kap_W05_Z15":(1,1.5,1,1/3,0,0),          # kW=0.5 kZ=1.5 (lambda=1/3) closure point
 "cpo_p2":(r2/2,r2,1,1,2*r2,2*r2),"cpo_m2":(r2/2,r2,1,1,-2*r2,-2*r2)}  # as ZH cpo cards (cosa=1/sqrt2, kSM=sqrt2, kAzz=kAww=+-2sqrt2)
for n,(cosa,ksm,kz,kw,azz,aww) in PTS.items():
    t=f"""# WH coupling point {n}: EW W+- X0 j j (QCD=0), W->l nu in ME (e,mu), X0=H undecayed, H->gamma gamma forced in PY8 like S_EW_WHjj. kW=kSM*kSMW={ksm*kw:.6g}, kZ=kSM*kSMZ={ksm*kz:.6g}.
# UNVALIDATED until diagram check + gridpack + test job + lambda=1 sigma closure to S_EW_WHjj (reports/04 sec. 10). p/j without b as S_EW_WHjj (closure to SM). Generator cuts = S_EW_WHjj (no mjj cut).
set automatic_html_opening False
set auto_update 0
set nb_core 4
set run_mode 2
set lhapdf_py3 lhapdf-config
import model HC_NLO_X0_kVV-no_b_mass
define p = g u c d s u~ c~ d~ s~
define j = g u c d s u~ c~ d~ s~
define l+ = e+ mu+
define l- = e- mu-
define vl = ve vm
define vl~ = ve~ vm~
generate p p > w+ x0 j j QCD=0, w+ > l+ vl
add process p p > w- x0 j j QCD=0, w- > l- vl~
output OUTDIR -nojpeg
launch OUTDIR
0
"""+"\n".join(runset)+f"""
set param_card kHaa 0
set param_card kAaa 0
set param_card kHza 0
set param_card kAza 0
set param_card kHzz 0
set param_card kHww 0
set param_card kHda 0
set param_card kHdz 0
set param_card kHdwR 0
set param_card kHdwI 0
set param_card cosa {cosa!r}
set param_card kSM {ksm!r}
set param_card kSMZ {kz}
set param_card kSMW {kw!r}
set param_card kAzz {azz!r}
set param_card kAww {aww!r}
done
"""
    open(f"{WH}/cards/coupling/K_EW_WHjj_{n}.mg5","w").write(t)
print(len(PTS),"cards")
