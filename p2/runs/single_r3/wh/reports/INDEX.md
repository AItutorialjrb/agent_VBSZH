# WH single_r3 — report index (Phase 01–03, gate G1)
| Report | Status |
|---|---|
| [01_signal_definition.md](01_signal_definition.md) | PASS, D-WH-1/2 open |
| [02_background_overlap.md](02_background_overlap.md) | PASS as ledger, D-WH-3…7 open |
| [03_generation_validation.md](03_generation_validation.md) | PARTIAL: 16/18 sample types pass; QCD Wγγjj and twin pending (condor 899736.14/15) |
| [G1_self_review.md](G1_self_review.md) | 17 issues, 4 of severity 1 open |

## Reproduction (all from `p2/runs/single_r3/wh`, stack via `p2/lib/scripts/setup_stack.sh`)
```bash
python3 scripts/mkcard.py                                   # regenerate Phase 02/03 cards (Phase 01 smoke cards are files in cards/smoke)
scripts/mg5_smoke.sh <card> $(python3 scripts/seeds.py <card>) 1200   # interactive LO sigma, outputs work/m5/<card>/
scripts/gen_check.sh <card>                                 # generate-only diagram check -> work/gencheck/
scripts/run_py8_delphes.sh <lhe.gz> cards/py8/<cmnd> <N> <seed+1e8> <out.root>
python3 -P scripts/smoke_wh.py <full.root> <sigma_fb> <outdir>          # Delphes object validation
python3 -P scripts/wh_baseline.py <label> <sigma_fb> <k> 500 <files|@list>   # B0 cutflow (GPT=25 for photon pT>25)
python3 -P scripts/fake_bound.py <ff1|ff2|fl> <label> <sigma_fb> <k> 500 <files>
python3 -P scripts/ledger.py                                # BR ledger + nmc_check self-tests
bash -lc 'module load lxbatch/eossubmit; cd /eos/user/r/rjiang/vbs_zh_codex_starter/p2/runs/single_r3/wh/scripts/condor; condor_submit gridpacks_p03.sub; condor_submit test_p03.sub'
python3 -P scripts/lhe_kin.py <lhe.gz ...>                  # parton-level audit (validation only)
```
