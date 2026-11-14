#!/bin/bash
# single_r1 WH Phase 05 ntuple job (reads EOS via fuse, writes the .npz to EOS); args: <list file> <0-based line>
# (condor "queue ... from" splits on commas, so the job reads its own line: out modes seed comma-files)
read OUT MODES SEED F <<< "$(sed -n "$(( $2 + 1 ))p" "$1")"; FILES=$(echo $F | tr ',' ' ')
export PROJECT=/eos/user/r/rjiang/vbs_zh_codex_starter/p2/lib; source /eos/user/r/rjiang/vbs_zh_codex_starter/p2/lib/scripts/setup_stack.sh >/dev/null 2>&1 || exit 11
[ -f "$OUT" ] && { echo exists; exit 0; }
python3 -P /eos/user/r/rjiang/vbs_zh_codex_starter/p2/runs/single_r1/wh/scripts/p05/ntuple_wh.py /tmp/nt_$$.npz $MODES $SEED $FILES || exit 12
cp /tmp/nt_$$.npz "$OUT.tmp" && mv "$OUT.tmp" "$OUT" || exit 13
rm -f /tmp/nt_$$.npz
