#!/bin/bash
# Writes cards/smoke/*.mg5 (sigma-only interactive runs; LO, 13.6 TeV, NNPDF31_nnlo_as_0118, ZH-identical jet cuts). OUTDIR/SEED substituted by mg5_run_smoke.sh
cd "$(dirname "$0")/.."
LIGHT='define p = g u c d s u~ c~ d~ s~
define j = g u c d s u~ c~ d~ s~'
WITHB='define p = g u c d s b u~ c~ d~ s~ b~
define j = g u c d s b u~ c~ d~ s~ b~'
LD='define l+ = e+ mu+
define l- = e- mu-
define vl = ve vm
define vl~ = ve~ vm~'
mk(){ # name flavourblock generate-line [extra run_card lines]
  n=$1; { cat <<HD
# WH smoke card (sigma-only, interactive). UNVALIDATED until the corresponding report passes.
set automatic_html_opening False
set auto_update 0
set nb_core 4
set run_mode 2
set lhapdf_py3 lhapdf-config
import model sm-no_b_mass
$2
$LD
generate $3
output OUTDIR -nojpeg
launch OUTDIR
0
set run_card ebeam1 6800
set run_card ebeam2 6800
set run_card pdlabel lhapdf
set run_card lhaid 303600
set run_card maxjetflavor 5
set run_card asrwgtflavor 5
set run_card use_syst True
set run_card nevents 2000
set run_card ptj 20
set run_card etaj 5
set run_card drjj 0.4
set run_card drjl 0.4
set run_card dynamical_scale_choice 3
set run_card cut_decays False
set run_card iseed SEED
done
HD
  } > cards/smoke/$n.mg5; }
mk wp_light_nodec "$LIGHT" "p p > w+ h j j QCD=0 QED=4"
mk wm_light_nodec "$LIGHT" "p p > w- h j j QCD=0 QED=4"
mk wp_b_nodec     "$WITHB" "p p > w+ h j j QCD=0 QED=4"
mk wp_bnot_nodec  "$WITHB" "p p > w+ h j j QCD=0 QED=4 / t t~"
mk wp_light_wdec  "$LIGHT" "p p > w+ h j j QCD=0 QED=4, w+ > l+ vl"
mk wm_light_wdec  "$LIGHT" "p p > w- h j j QCD=0 QED=4, w- > l- vl~"
mk wp_qcd_nodec   "$LIGHT" "p p > w+ h j j QCD=2 QED=2"
mk wm_qcd_nodec   "$LIGHT" "p p > w- h j j QCD=2 QED=2"
mk wp_int_nodec   "$LIGHT" "p p > w+ h j j QCD^2==2 QED^2==6"
mk wp_qcd_wdec    "$LIGHT" "p p > w+ h j j QCD=2 QED=2, w+ > l+ vl"
mk wm_qcd_wdec    "$LIGHT" "p p > w- h j j QCD=2 QED=2, w- > l- vl~"
