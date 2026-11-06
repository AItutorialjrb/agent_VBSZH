#!/bin/bash
# Bulk production submit: ONE cluster per sample, no duplicates (marker file + queue + existing outputs), seeds.check first. Usage: submit_bulk.sh <sample> [<sample> ...]
WH=/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh; cd $WH/work/condor/prod || exit 1
python3 $WH/scripts/check_sub_seeds.py || exit 2
LED=$WH/work/prod_submission_ledger.csv; [ -e $LED ] || echo "utc,sample,cluster,n_jobs,sub_file,schedd" > $LED
for s in "$@"; do
  [ -e .submitted_$s ] && { echo "$s already submitted (marker)"; continue; }
  [[ "$s" != *_topup ]] && [ -n "$(ls /eos/home-r/rjiang/vbs_zh_codex_starter/p2/production/wh/$s 2>/dev/null | head -1)" ] && { echo "$s output dir not empty: refusing"; continue; }
  n=$(bash -lc "module load lxbatch/eossubmit; condor_q -name bigbird103.cern.ch -nobatch 2>/dev/null | grep -c ' $s '" ); [ "${n:-0}" != "0" ] && { echo "$s already in queue"; continue; }
  out=$(bash -lc "module load lxbatch/eossubmit; condor_submit prod_$s.sub" 2>&1); cl=$(echo "$out" | grep -o "cluster [0-9]*" | awk '{print $2}'); nj=$(echo "$out" | grep -o "^[0-9]* job" | awk '{print $1}')
  [ -z "$cl" ] && { echo "$s SUBMIT FAILED: $out"; continue; }
  touch .submitted_$s; echo "$(date -u +%FT%TZ),$s,$cl,$nj,prod_$s.sub,bigbird103.cern.ch" >> $LED; echo "$s -> cluster $cl ($nj jobs)"
done
