#!/bin/bash
# E1 (2026-11-03): build HC_NLO_X0_kVV = official Higgs Characterisation UFO HC_NLO_X0 (README model version 1.3,
# __init__ 1.2; https://feynrules.irmp.ucl.ac.be/raw-attachment/wiki/HiggsCharacterisation/HC_NLO_X0_UFO.zip,
# zip sha256 b91d8788ed66a12a3eaf9e1f8771f98b789b4b3fc8b10eeb32c9c04f057ae1bd, fetched 2026-11-03) + ONE minimal patch:
# the official model has a single SM-like coupling kSM shared by X0WW (GC_3005h1) and X0ZZ (GC_3007h1). We add two
# external parameters kSMW (FRBlock 40) and kSMZ (FRBlock 41), default 1, multiplying kSM in exactly those two
# couplings, so kappa_W = kSM*kSMW, kappa_Z = kSM*kSMZ, lambda_WZ = kSMW/kSMZ. Nothing else is changed.
set -e
P=/eos/home-r/rjiang/vbs_zh_codex_starter; SRC=$P/software/models_dl/HC_NLO_X0_UFO.zip; OUT=$P/software/models/HC_NLO_X0_kVV
echo "b91d8788ed66a12a3eaf9e1f8771f98b789b4b3fc8b10eeb32c9c04f057ae1bd  $SRC" | sha256sum -c -
T=$(mktemp -d); unzip -q $SRC -d $T; rm -rf $OUT; mkdir -p $(dirname $OUT); mv $T/HC_NLO_X0_UFO $OUT; rm -rf $T
cd $OUT; rm -rf *.pyc __pycache__ py3_model.pkl *~
python3 - <<'PY'
import re
c = open("couplings.py").read()
a = "value = '(complex(0,1)*cosa*kSM*ee**2*vev)/(2.*sw**2)'"
b = "value = 'cosa*ee**2*complex(0,1)*kSM*vev + (cosa*cw**2*ee**2*complex(0,1)*kSM*vev)/(2.*sw**2) + (cosa*ee**2*complex(0,1)*kSM*sw**2*vev)/(2.*cw**2)'"
assert c.count(a) == 1 and c.count(b) == 1 and c.count("kSM") == 4
c = c.replace(a, a.replace("kSM", "kSM*kSMW")).replace(b, b.replace("kSM", "kSM*kSMZ")); open("couplings.py", "w").write(c)
p = open("parameters.py").read(); anchor = "kHtt = Parameter(name = 'kHtt',"; assert p.count(anchor) == 1
new = "".join(f"""{n} = Parameter(name = '{n}',
                nature = 'external',
                type = 'real',
                value = 1,
                texname = '{t}',
                lhablock = 'FRBlock',
                lhacode = [ {k} ])

""" for n, t, k in (("kSMW", "\\\\kappa _{W}", 40), ("kSMZ", "\\\\kappa _{Z}", 41)))
p = p.replace(anchor, new + anchor); open("parameters.py", "w").write(p)
for f in ("restrict_no_b_mass.dat", "restrict_default.dat", "restrict_4Fnoyb.dat", "restrict_heft.dat", "restrict_c_mass.dat",
          "paramcard_no_b_mass.dat", "paramcard_default.dat", "paramcard_4Fnoyb.dat", "paramcard_heft.dat", "paramcard_c_mass.dat"):
    s = open(f).read(); m = re.search(r"(?im)^block\s+frblock.*\n", s); assert m, f
    val = ("1.400000e+00", "1.410000e+00") if f.startswith("restrict") else ("1.000000e+00", "1.000000e+00")
    s = s[:m.end()] + f"   40 {val[0]} # kSMW \n   41 {val[1]} # kSMZ \n" + s[m.end():]; open(f, "w").write(s)
PY
echo "patched: $(grep -c kSMW couplings.py parameters.py restrict_no_b_mass.dat | tr '\n' ' ')"
# tar via a local temp dir (EOS FUSE "file changed as we read it" race)
S=$(mktemp -d); cp -r $OUT $S/ && tar czf $S/m.tgz -C $S HC_NLO_X0_kVV && cp $S/m.tgz $P/software/install/HC_NLO_X0_kVV.tgz && rm -rf $S
sha256sum $P/software/install/HC_NLO_X0_kVV.tgz
