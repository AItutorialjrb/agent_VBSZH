#!/bin/bash
# RESUME CHECK (D33): see scripts/fix_memory_holds.py. Step 1 (resource normalisation) then step 2-4 (held jobs: release once with more memory; second failure: drop if the N rule holds, else resubmit with a fresh seed; log).
module load lxbatch/eossubmit
S="-name bigbird103.cern.ch"
# NOTE: "Failed to set attribute ... No attributes were set" / "Couldn't find/release" means that no job matched the constraint (benign).
condor_qedit $S -constraint 'ClusterId>=893600 && JobStatus==1 && (RequestMemory<8000 || RequestCpus!=1)' RequestMemory 8000 2>/dev/null
condor_qedit $S -constraint 'ClusterId>=893600 && JobStatus==1 && RequestCpus!=1' RequestCpus 1 2>/dev/null
condor_qedit $S -constraint 'ClusterId>=893600 && JobStatus==2 && RequestMemory<8000' RequestMemory 8000 2>/dev/null
cd /eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh && python3 scripts/exit_codes.py | tail -2 && python3 scripts/fix_memory_holds.py "$@"
condor_q $S -af ClusterId JobStatus RequestCpus RequestMemory | awk '$1>=893600' | awk '{k[$2" cpus="$3" mem="$4]++} END{for(x in k) print k[x], x}' | sort -rn
