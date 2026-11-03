#!/bin/bash
cd /eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh
# seeds 2110000+J (sample index 0 = smoke tests), J unique per card
declare -A S=( [wp_light_nodec]=2110001 [wm_light_nodec]=2110002 [wp_b_nodec]=2110003 [wp_bnot_nodec]=2110004 [wp_light_wdec]=2110005 [wm_light_wdec]=2110006 [wp_qcd_nodec]=2110007 [wm_qcd_nodec]=2110008 [wp_int_nodec]=2110009 [wp_qcd_wdec]=2110010 [wm_qcd_wdec]=2110011 [wm_light_wdec_rep]=2110026 [wm_light_nodec_rep]=2110027 [wm_light_wdec_bw]=2110029 )
for c in "$@"; do scripts/mg5_run_smoke.sh $c ${S[$c]} 1500; done
