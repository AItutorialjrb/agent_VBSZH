#!/bin/bash
# Wait for the heavy gridpacks; release each held test job when its gridpack exists; exit when all test outputs exist.
cd /eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/single_r1/wh
declare -A P=([B_EW_wpaajj]=4 [B_EW_wmaajj]=5 [B_QCD_lvaajj]=6 [B_QCD_lvaajj_nomjj]=7 [T_ttaa_1l]=12)
end=$((SECONDS+16*3600)); declare -A REL; empty=0
while [ $SECONDS -lt $end ]; do
  done_n=0
  for s in "${!P[@]}"; do
    ls work/test/$s/*.json >/dev/null 2>&1 && { done_n=$((done_n+1)); continue; }
    if [ -s work/gridpacks/${s}_status.txt ] && [ -z "${REL[$s]}" ]; then
      grep -q "rc=0" work/gridpacks/${s}_status.txt || echo "$(date -u +%T) $s gridpack rc != 0: $(head -1 work/gridpacks/${s}_status.txt)"
      bash -lc "module load lxbatch/eossubmit >/dev/null 2>&1; condor_release 900136.${P[$s]}" >/dev/null 2>&1; REL[$s]=1; echo "$(date -u +%T) released test for $s"
    fi
  done
  [ $done_n -eq 5 ] && { echo "$(date -u +%T) all 5 heavy test jobs done"; exit 0; }
  q=$(bash -lc 'module load lxbatch/eossubmit >/dev/null 2>&1; condor_q 900134 900136 -af JobStatus' 2>/dev/null | wc -l)
  if [ "$q" = 0 ]; then empty=$((empty+1)); else empty=0; fi   # a single empty condor_q reply can be transient
  [ $empty -ge 3 ] && [ $done_n -lt 5 ] && { echo "$(date -u +%T) queue empty (3 checks) but only $done_n/5 done"; exit 1; }
  sleep 300
done
echo "timeout"; exit 2
