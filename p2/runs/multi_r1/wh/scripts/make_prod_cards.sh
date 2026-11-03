#!/bin/bash
# Writes cards/prod/<sample>.mg5 (gridpack cards, UNVALIDATED until gridpack+test job pass) and cards/smoke/<sample>_smoke.mg5 (sigma-only interactive derivative: no gridpack, 500 ev).
# Conventions follow lib/cards/production_{v2,final}. Both W charges in ONE card via `add process`.  OUTDIR/SEED substituted by the runner.
cd "$(dirname "$0")/.."
HD='# WH production card — UNVALIDATED until its gridpack job + one test job pass (reports/03_generation_validation.md). OUTDIR/SEED substituted by runner.
set automatic_html_opening False
set auto_update 0
set nb_core 4
set run_mode 2
set lhapdf_py3 lhapdf-config
import model sm-no_b_mass'
DEF5='define p = g u c d s b u~ c~ d~ s~ b~
define j = g u c d s b u~ c~ d~ s~ b~'
DEFL='define p = g u c d s u~ c~ d~ s~
define j = g u c d s u~ c~ d~ s~'
DEFX='define l+ = e+ mu+
define l- = e- mu-
define vl = ve vm
define vl~ = ve~ vm~
define q = u c d s u~ c~ d~ s~'
COMMON='set run_card ebeam1 6800
set run_card ebeam2 6800
set run_card pdlabel lhapdf
set run_card lhaid 303600
set run_card maxjetflavor 5
set run_card asrwgtflavor 5
set run_card use_syst True
set run_card cut_decays False'
mk(){ # name, flavour-def, process lines, run_card lines
  { echo "$HD"; echo "$2"; echo "$DEFX"; echo "$3"; echo "output OUTDIR -nojpeg"; echo "launch OUTDIR"; echo 0; echo "$COMMON"
    echo "set run_card gridpack True"; echo "set run_card nevents 2000"; echo "$4"; echo "set run_card iseed SEED"; echo done; } > cards/prod/$1.mg5
  sed -e '/gridpack True/d' -e 's/nevents 2000/nevents 500/' cards/prod/$1.mg5 > cards/smoke/$1_smoke.mg5; }
JETS='set run_card ptj 20
set run_card etaj 5
set run_card drjj 0.4
set run_card drjl 0.4
set run_card dynamical_scale_choice 3'
NOJ='set run_card ptj 0
set run_card drjj 0
set run_card drjl 0
set run_card draj 0
set run_card dynamical_scale_choice 3'
# ---- signal / resonant H
mk S_EW_WHjj "$DEFL" "generate p p > w+ h j j QCD=0 QED=4, w+ > l+ vl
add process p p > w- h j j QCD=0 QED=4, w- > l- vl~" "$JETS"
mk S_EW_WHjj_taunu "$DEFL" "generate p p > w+ h j j QCD=0 QED=4, w+ > ta+ vt
add process p p > w- h j j QCD=0 QED=4, w- > ta- vt~" "$JETS"
mk H_QCD_WH_mlm "$DEFL" "generate p p > w+ h, w+ > l+ vl @0
add process p p > w+ h j, w+ > l+ vl @1
add process p p > w+ h j j, w+ > l+ vl @2
add process p p > w- h, w- > l- vl~ @0
add process p p > w- h j, w- > l- vl~ @1
add process p p > w- h j j, w- > l- vl~ @2" "set run_card ickkw 1
set run_card xqcut 10
set run_card ptj 10
set run_card drjj 0
set run_card dynamical_scale_choice -1"
mk H_QCD_WHjj_fixed "$DEFL" "generate p p > w+ h j j QCD=2 QED=2, w+ > l+ vl
add process p p > w- h j j QCD=2 QED=2, w- > l- vl~" "$JETS"
mk I_WHjj "$DEFL" "generate p p > w+ h j j QCD^2==2 QED^2==6
add process p p > w- h j j QCD^2==2 QED^2==6" "$JETS"
# ---- other Higgs
mk H_ttH_1l "$DEF5" "generate p p > t t~ h, (t > b w+, w+ > l+ vl), (t~ > b~ w-, w- > q q)
add process p p > t t~ h, (t > b w+, w+ > q q), (t~ > b~ w-, w- > l- vl~)" "$NOJ"
mk H_tHq_lep "$DEF5" "generate p p > t h j \$\$ t~, (t > b w+, w+ > l+ vl)
add process p p > t~ h j \$\$ t, (t~ > b~ w-, w- > l- vl~)" "$NOJ"
mk H_tHW_1l "$DEF5" "generate p p > t w- h \$\$ t~, (t > b w+, w+ > l+ vl), w- > q q
add process p p > t w- h \$\$ t~, (t > b w+, w+ > q q), w- > l- vl~
add process p p > t~ w+ h \$\$ t, (t~ > b~ w-, w- > l- vl~), w+ > q q
add process p p > t~ w+ h \$\$ t, (t~ > b~ w-, w- > q q), w+ > l+ vl" "$NOJ"
# ---- top + photons (single lepton)
PHO='set run_card pta 15
set run_card etaa 2.5
set run_card draa 0
set run_card dral 0'
mk T_tta_1l "$DEF5" "generate p p > t t~ a, (t > b w+, w+ > l+ vl), (t~ > b~ w-, w- > q q)
add process p p > t t~ a, (t > b w+, w+ > q q), (t~ > b~ w-, w- > l- vl~)" "$NOJ
$PHO"
mk T_ttaa_1l "$DEF5" "generate p p > t t~ a a, (t > b w+, w+ > l+ vl), (t~ > b~ w-, w- > q q)
add process p p > t t~ a a, (t > b w+, w+ > q q), (t~ > b~ w-, w- > l- vl~)" "$NOJ
$PHO
set run_card mmaa 90
set run_card mmaamax 190"
mk T_tWa_1l "$DEF5" "generate p p > t w- a \$\$ t~, (t > b w+, w+ > l+ vl), w- > q q
add process p p > t w- a \$\$ t~, (t > b w+, w+ > q q), w- > l- vl~
add process p p > t~ w+ a \$\$ t, (t~ > b~ w-, w- > l- vl~), w+ > q q
add process p p > t~ w+ a \$\$ t, (t~ > b~ w-, w- > q q), w+ > l+ vl" "$NOJ
$PHO"
mk T_tt_1l "$DEF5" "generate p p > t t~, (t > b w+, w+ > l+ vl), (t~ > b~ w-, w- > q q)
add process p p > t t~, (t > b w+, w+ > q q), (t~ > b~ w-, w- > l- vl~)" "$NOJ"
# ---- continuum prompt photons (on-shell W chain, ZH-final-style VBS-biased generation)
VBSG='set run_card ptl 10
set run_card etal 2.5
set run_card ptj 20
set run_card etaj 5
set run_card pta 25
set run_card etaa 2.5
set run_card drjj 0.4
set run_card drjl 0.4
set run_card draa 0.4
set run_card draj 0.4
set run_card dral 0.4
set run_card mmaa 100
set run_card mmaamax 170
set run_card dynamical_scale_choice 3'
mk B_EW_Waajj_vbs "$DEFL" "generate p p > w+ a a j j QCD=0 QED=5, w+ > l+ vl
add process p p > w- a a j j QCD=0 QED=5, w- > l- vl~" "$VBSG
set run_card mmjj 400"
mk B_QCD_Waajj_vbs "$DEFL" "generate p p > w+ a a j j QCD=2 QED=3, w+ > l+ vl
add process p p > w- a a j j QCD=2 QED=3, w- > l- vl~" "$VBSG
set run_card mmjj 400"
mk B_QCD_Waajj_nomjj "$DEFL" "generate p p > w+ a a j j QCD=2 QED=3, w+ > l+ vl
add process p p > w- a a j j QCD=2 QED=3, w- > l- vl~" "$VBSG
set run_card mmjj 0"
mk F_EW_Wajj_vbs "$DEFL" "generate p p > w+ a j j QCD=0 QED=4, w+ > l+ vl
add process p p > w- a j j QCD=0 QED=4, w- > l- vl~" "$VBSG
set run_card mmaa 0
set run_card mmaamax -1
set run_card mmjj 400"
mk F_QCD_Wajj_vbs "$DEFL" "generate p p > w+ a j j QCD=2 QED=2, w+ > l+ vl
add process p p > w- a j j QCD=2 QED=2, w- > l- vl~" "$VBSG
set run_card mmaa 0
set run_card mmaamax -1
set run_card mmjj 400"
mk F_QCD_Wajj_nomjj "$DEFL" "generate p p > w+ a j j QCD=2 QED=2, w+ > l+ vl
add process p p > w- a j j QCD=2 QED=2, w- > l- vl~" "$VBSG
set run_card mmaa 0
set run_card mmaamax -1
set run_card mmjj 0"
# ---- pilots (fixed 2-parton) for fake-photon bounds; sigma-only here
mk F_Wjj_pilot "$DEFL" "generate p p > w+ j j, w+ > l+ vl
add process p p > w- j j, w- > l- vl~" "set run_card ptj 20
set run_card etaj 5
set run_card drjj 0.4
set run_card dynamical_scale_choice 3"
mk F_Wajj_pilot "$DEFL" "generate p p > w+ a j j, w+ > l+ vl
add process p p > w- a j j, w- > l- vl~" "set run_card ptj 20
set run_card etaj 5
set run_card drjj 0.4
set run_card pta 15
set run_card etaa 2.5
set run_card draj 0.4
set run_card dral 0.4
set run_card dynamical_scale_choice 3"
# ---- sigma-only proxy: inclusive LO W(->l nu)H, 0 jets (proxy for the matched MLM cross section; cf. ZH zh_0j)
mk H_QCD_WH_0j "$DEFL" "generate p p > w+ h, w+ > l+ vl
add process p p > w- h, w- > l- vl~" "set run_card dynamical_scale_choice 3"
# ---- sigma-only: prompt QCD gamma gamma (+jj) used for the non-prompt-lepton bound (no lepton in ME)
mk Q_aa_0j "$DEFL" "generate p p > a a" "set run_card pta 25
set run_card etaa 2.5
set run_card draa 0.4
set run_card mmaa 100
set run_card mmaamax 170
set run_card dynamical_scale_choice 3"
mk Q_aajj "$DEFL" "generate p p > a a j j" "set run_card pta 25
set run_card etaa 2.5
set run_card draa 0.4
set run_card draj 0.4
set run_card mmaa 100
set run_card mmaamax 170
set run_card ptj 20
set run_card etaj 5
set run_card drjj 0.4
set run_card dynamical_scale_choice 3"
