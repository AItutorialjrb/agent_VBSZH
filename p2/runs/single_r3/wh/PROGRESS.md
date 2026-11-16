# WH single_r3 process PROGRESS
- [x] 01 signal definition, σ/diagram/closure tests (work/m5)
- [x] 02 ledger, ZH reuse at Delphes level (work/zhreuse), fake bounds (work/fakes), generator-cut safety
- [~] 03 condor: 16/18 test jobs verified; 899736.14/15 + 899737.14/15 pending
- [x] G1 self-review
Resume: check `condor_q 899736 899737`; then run closure (python block in reports/03 §2 source: work/test/closure_p03.txt generator) + wh_baseline on the two new test outputs.
