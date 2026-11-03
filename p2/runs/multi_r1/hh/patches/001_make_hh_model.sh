#!/bin/bash
# Build UFO sm_kVk2VkL = MG5 v3.6.3 built-in `sm` UFO + ONE minimal patch (hh/patches/001_sm_kappas_model.md):
# three real external parameters in block KAPPAS (lhacode 1,2,3 = kV,k2V,kl, default 1) multiply exactly the 5 Higgs-gauge/self couplings:
#   GC_72 (HWW) and GC_81 (HZZ) x kV ; GC_34 (HHWW) and GC_65 (HHZZ) x k2V ; GC_69 (HHH) x kl.  Nothing else changes.
# NOTE: restrict defaults are 1.11,1.22,1.33 (NOT 1, and mutually DISTINCT): MG5 restriction fixes parameters equal to 0 or 1 (removed from the card) and MERGES externals with identical values into one card entry; every card sets kV,k2V,kl explicitly.
# Source: MG5_aMC_v3.6.3 upstream tarball sha256 2bb0d085a37b704ef956e8e8ed468bdcfef13e638c82ed3f1c4e968a090ebd98 (ZH install).
set -e
P=/eos/home-r/rjiang/vbs_zh_codex_starter; H=$P/p2/runs/multi_r1/hh
SRC=$P/software/install/MG5_aMC_v3.6.3/models/sm; OUT=${1:-$H/work/models/sm_kVk2VkL}
rm -rf $OUT; mkdir -p $(dirname $OUT); cp -r $SRC $OUT; cd $OUT; rm -rf __pycache__ py3_model.pkl *.pyc
python3 -I - <<'PY'
import re
c = open("couplings.py").read()
for g, k in (("GC_72","kV"),("GC_81","kV"),("GC_34","k2V"),("GC_65","k2V"),("GC_69","kl")):
    m = re.search(r"(%s = Coupling\(name = '%s',\s*value = ')([^']*)(')" % (g, g), c); assert m, g
    c = c[:m.start(2)] + k + "*(" + m.group(2) + ")" + c[m.end(2):]
open("couplings.py", "w").write(c)
p = open("parameters.py").read(); anchor = "MH = Parameter(name = 'MH',"; assert p.count(anchor) == 1
new = "".join(f"""{n} = Parameter(name = '{n}',
                nature = 'external',
                type = 'real',
                value = 1.,
                texname = '{n}',
                lhablock = 'KAPPAS',
                lhacode = [ {k} ])

""" for n, k in (("kV", 1), ("k2V", 2), ("kl", 3)))
open("parameters.py", "w").write(p.replace(anchor, new + anchor))
import glob
for f in glob.glob("restrict_*.dat"):
    s = open(f).read(); s = s.replace("\nBlock SMINPUTS", "\nBlock KAPPAS \n    1 1.110000e+00 # kV \n    2 1.220000e+00 # k2V \n    3 1.330000e+00 # kl \n\nBlock SMINPUTS", 1)
    assert "KAPPAS" in s, f
    open(f, "w").write(s)
PY
sed -i "s/^__author__.*/&/" __init__.py
grep -c "kV\|k2V\|kl" couplings.py parameters.py restrict_no_b_mass.dat
