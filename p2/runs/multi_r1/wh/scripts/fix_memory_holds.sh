#!/bin/bash
# RESUME CHECK (part of every resume): production jobs with >= 30 000 events/job need 8000 MB; the schedd (CERN eossubmit policy) may turn a request of 8000 MB / 1 CPU into RequestCpus 3 / RequestMemory 9000 at submit time, and jobs that started with 2500/3000 MB are held (code 34).
# NOTE: "Failed to set attribute ... No attributes were set" / "Couldn't find/release" means that no job matched the constraint (benign).
# This script (1) qedits RequestMemory 8000 and RequestCpus 1 on every NOT-running job of the production clusters >= 893600 whose request differs, (2) qedits RequestMemory 8000 on still-running jobs with a smaller request (so a later hold cannot happen), (3) releases all code-34 holds, (4) prints the resulting table. Never touches a running job's cgroup.
module load lxbatch/eossubmit
S="-name bigbird103.cern.ch"
condor_qedit $S -constraint 'ClusterId>=893600 && JobStatus!=2 && (RequestMemory!=8000 || RequestCpus!=1)' RequestMemory 8000
condor_qedit $S -constraint 'ClusterId>=893600 && JobStatus!=2 && RequestCpus!=1' RequestCpus 1
condor_qedit $S -constraint 'ClusterId>=893600 && JobStatus==2 && RequestMemory<8000' RequestMemory 8000
condor_release $S -constraint 'JobStatus==5 && HoldReasonCode==34'
condor_q $S -af ClusterId JobStatus RequestCpus RequestMemory | awk '$1>=893600' | awk '{k[$2" cpus="$3" mem="$4]++} END{for(x in k) print k[x], x}' | sort -rn
