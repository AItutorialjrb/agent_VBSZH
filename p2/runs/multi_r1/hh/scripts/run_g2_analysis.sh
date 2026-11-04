#!/bin/bash
# Re-runs the whole pre-G2 analysis chain on the pilot samples in p2/production/hh (login-node safe: reads ROOT files, a few minutes).  Usage: bash scripts/run_g2_analysis.sh
set -e
cd "$(dirname "$0")/.."; source ../../../lib/scripts/setup_stack.sh >/dev/null 2>&1
P=../../../production/hh; C=config/sample_matrix.yaml; S=config/tagging_scenarios.yaml; G=work/g2; mkdir -p $G
python3 -P scripts/hh_samples.py; python3 -P scripts/make_matrix.py > $G/matrix_print.txt
python3 -P scripts/pilot_check.py $C $P $G/pilot.json > $G/pilot.md
BK="Q_4j_vbs Q_bbjj_vbs Q_4j_vbs_twin Q_bbjj_vbs_twin Q_4b_ht T_ttbar_mlm T_ttbar_boost H_VBFH_bb H_ZH_Zqq_bb H_WH_Wqq_bb H_ttH_bb H_ggH_jj_heft V_Zjj_QCD_vbs V_Wjj_QCD_vbs V_ZZjj_EW G_ggHH_loop_kl1 G_ggHH_loop_kl0 G_ggHH_loop_kl2 G_ggHH_loop_kl5 X_tW_boost X_ttZ_boost X_ttW_boost X_Zjj_EW_vbs X_Wjj_EW_vbs X_ZZ_QCD_boost X_WZ_QCD_boost X_ggZH_loop"
SG="S_HHjj_kV1_k2V1_kl1 S_HHjj_kV1p5_k2V0_kl1 S_HHjj_kV1p5_k2V0_kl0 S_HHjj_kV0p5_k2V2_kl0 S_HHjj_kV1_k2V0_kl2 S_HHjj_kV1_k2V2_klm1 S_HHjj_kV1_k2V0_kl1 S_HHjj_kV1_k2V2_kl1 S_HHjj_kV1p25_k2V1p5_kl2"
python3 -P scripts/neff_project.py $C $S $G/neff.json $P $BK $SG > $G/neff.txt
python3 -P scripts/twin_check_hh.py $C $S $G/twins.json $P Q_4j_vbs:Q_4j_vbs_twin Q_bbjj_vbs:Q_bbjj_vbs_twin T_ttbar_mlm:T_ttbar_mlm_twin T_ttbar_boost:T_ttbar_boost_twin H_VBFH_bb:H_VBFH_bb_twin H_ZH_Zqq_bb:H_ZH_Zqq_bb_twin H_ttH_bb:H_ttH_bb_twin V_Zjj_QCD_vbs:V_Zjj_QCD_vbs_twin V_ZZjj_EW:V_ZZjj_EW_twin H_ggH_jj_heft:H_ggH_jj_heft_twin H_WH_Wqq_bb:H_WH_Wqq_bb_twin V_Wjj_QCD_vbs:V_Wjj_QCD_vbs_twin S_HHjj_kV1_k2V1_kl1:S_HHjj_SM_twin_loose S_HHjj_kV1_k2V0_kl1:S_HHjj_kV1_k2V0_kl1_twin > $G/twins.md
python3 -P scripts/morph_delphes.py $C $G/morph_delphes.json $P $G/signal_planned_N.json > $G/morph.txt
python3 -P scripts/mlm_check.py $C $G/mlm_check.json $P T_ttbar_mlm T_ttbar_mlm_xq20 T_ttbar_mlm_xq45 -- T_ttbar_boost > $G/mlm.txt
python3 -P scripts/variations.py $C $S $G/variations.json $P S_HHjj_kV1_k2V1_kl1 S_HHjj_kV1p5_k2V0_kl1 S_HHjj_kV1_k2V2_kl1 Q_4j_vbs_twin Q_bbjj_vbs_twin T_ttbar_mlm H_ttH_bb H_ZH_Zqq_bb V_ZZjj_EW G_ggHH_loop_kl1 > $G/variations.txt
python3 -P scripts/g2_plan.py > $G/plan.txt
echo "analysis chain finished"
