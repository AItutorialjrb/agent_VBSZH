#!/usr/bin/env python3
"""Fills the generated tables into reports/0[23]_*.md from the *.in templates (run after build_sample_matrix.py and audit_test_jobs.py)."""
import subprocess, os
WH = "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh"; os.chdir(WH)
subprocess.run(["python3", "scripts/build_sample_matrix.py"], capture_output=True); subprocess.run(["python3", "scripts/audit_test_jobs.py"], capture_output=True)
r = lambda f: open(f).read()
t2 = r("reports/02_background_overlap.md.in").replace("@@TABLE@@", r("work/matrix_table.md")).replace("@@BOUNDS@@", "```\n" + r("work/bounds.txt") + "```")
open("reports/02_background_overlap.md", "w").write(t2)
tw = r("work/twin_note.txt") if os.path.exists("work/twin_note.txt") else "no twin test-job output available yet (gridpacks still building at the time of writing)."
t3 = r("reports/03_generation_validation.md.in").replace("@@SMOKE@@", r("work/smoke_table.md")).replace("@@TESTS@@", r("work/test_summary.md")).replace("TWIN_PLACEHOLDER", tw)
open("reports/03_generation_validation.md", "w").write(t3)
print("ok")
