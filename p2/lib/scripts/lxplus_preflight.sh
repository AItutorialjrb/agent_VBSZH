#!/usr/bin/env bash
set -u
printf 'timestamp UTC: '; date -u +'%Y-%m-%dT%H:%M:%SZ'
printf 'host: '; hostname
printf 'uname: '; uname -a
printf 'cwd: '; pwd
printf 'user: '; id
for x in codex python3 root-config mg5_aMC pythia8-config DelphesHepMC3 condor_submit eos; do
 printf '\n%s: ' "$x"; command -v "$x" || true
done
codex --version 2>/dev/null || true
python3 --version 2>/dev/null || true
root-config --version 2>/dev/null || true
printf '\nCVMFS directories: '; ls -ld /cvmfs /cvmfs/sft.cern.ch 2>/dev/null || true
printf '\nDisk quota indications:\n'; df -h . 2>/dev/null || true
printf '\nNOTE: This is read-only. Do not launch bulk jobs on lxplus login nodes.\n'
