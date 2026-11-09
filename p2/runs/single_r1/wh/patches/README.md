# single_r1 WH patches to p2/lib (ZH tag zh-final-v1.1); lib itself is never modified
| # | file | rationale |
|---|---|---|
| 001 | scripts/mg5_smoke.sh | WH paths (cards from wh/cards, outputs wh/work/m5), setup from p2/lib, own /tmp scratch removed after staging, refuse to overwrite an existing status |
| 002 | scripts/condor/make_gridpack.sh | unpack a transferred heft.tgz (MG5 database UFO, sha256 in work/models/heft.tgz.sha256) into the job-local MG5 models dir for H_ggF_Hjj; software/ untouched |
