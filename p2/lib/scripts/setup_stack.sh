#!/bin/bash
# Pinned software stack for the VBS ZHjj (H->gamma gamma) study.  Usage:  source scripts/setup_stack.sh
# Single coherent environment: CVMFS LCG_110 view (x86_64-el9-gcc13-opt) + upstream (unpatched) MG5_aMC 3.6.3
# installed under $PROJECT/software.  Do NOT mix with the system ROOT/Python or other LCG views.
# Versions verified in reports/03_stack.md.
export PROJECT=${PROJECT:-/eos/home-r/rjiang/vbs_zh_codex_starter}
export LCG_VIEW=/cvmfs/sft.cern.ch/lcg/views/LCG_110/x86_64-el9-gcc13-opt
if [ ! -r "$LCG_VIEW/setup.sh" ]; then echo "setup_stack: CVMFS view $LCG_VIEW not readable" >&2; return 1 2>/dev/null || exit 1; fi
# shellcheck disable=SC1091
source "$LCG_VIEW/setup.sh"
# MG5 location: on batch nodes the wrapper may point MG5_HOME at a local copy.
export MG5_HOME=${MG5_HOME:-$PROJECT/software/install/MG5_aMC_v3.6.3}
export PATH="$MG5_HOME/bin:$PATH"
export DELPHES_DIR=/cvmfs/sft.cern.ch/lcg/releases/LCG_110/delphes/3.5.1/x86_64-el9-gcc13-opt
export DELPHES_CMS_CARD=$DELPHES_DIR/cards/delphes_card_CMS.tcl
# Pinned PDF: NNPDF31_nnlo_as_0118 (LHAPDF id 303600), read-only from CVMFS (LHAPDF_DATA_PATH set by the view).
export VBSZH_LHAID=303600
export VBSZH_STACK_TAG="LCG_110/x86_64-el9-gcc13-opt+MG5_aMC_v3.6.3(upstream)"
# Keep the project's MG5 install read-mostly: no auto-update, no telemetry.
export MG5_NO_AUTO_UPDATE=1
