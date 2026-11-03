#!/bin/bash
# loop_sm_kl = MG5 v3.6.3 built-in loop_sm UFO + ONE patch: real external kl (block KAPPAS code 3, default 1) multiplies the HHH coupling GC_30 only
# (triangle diagrams g g > H* > H H scale with kl; box unchanged) -> ggF HH kl-dependence by 3-point quadratic morphing (sigma = A kl^2 + B kl + C).
set -e
P=/eos/home-r/rjiang/vbs_zh_codex_starter; H=$P/p2/runs/multi_r1/hh
SRC=$P/software/install/MG5_aMC_v3.6.3/models/loop_sm; OUT=${1:-$H/work/models/loop_sm_kl}
rm -rf $OUT; mkdir -p $(dirname $OUT); cp -r $SRC $OUT; cd $OUT; rm -rf __pycache__ py3_model.pkl *.pyc
python3 -I - <<'PY'
import re, glob
c = open("couplings.py").read()
m = re.search(r"(GC_30 = Coupling\(name = 'GC_30',\s*value = ')([^']*)(')", c); assert m
c = c[:m.start(2)] + "kl*(" + m.group(2) + ")" + c[m.end(2):]; open("couplings.py", "w").write(c)
p = open("parameters.py").read(); anchor = "MH = Parameter(name = 'MH',"; assert p.count(anchor) == 1
new = """kl = Parameter(name = 'kl',
                nature = 'external',
                type = 'real',
                value = 1.,
                texname = 'kl',
                lhablock = 'KAPPAS',
                lhacode = [ 3 ])

"""
open("parameters.py", "w").write(p.replace(anchor, new + anchor))
for f in glob.glob("restrict_*.dat"):
    s = open(f).read(); assert "\nBlock SMINPUTS" in s or "\nBLOCK SMINPUTS" in s.upper(), f
    s = s.replace("\nBlock SMINPUTS", "\nBlock KAPPAS \n    3 1.330000e+00 # kl \n\nBlock SMINPUTS", 1); assert "KAPPAS" in s, f
    open(f, "w").write(s)
PY
