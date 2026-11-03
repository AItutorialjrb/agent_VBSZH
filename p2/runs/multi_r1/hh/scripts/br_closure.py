#!/usr/bin/env python3
"""BR closure from the generator record (Particle branch of *_full.root of the test jobs). Usage: br_closure.py <test_dir> <out_json>
 - H: fraction of last-copy Higgs with a b bbar daughter pair (forced -> must be 1.0);  Z/W: fraction hadronic (forced -> 1.0);  tops (inclusive PY8 decays): W hadronic fraction vs PDG 0.6741."""
import sys, glob, os, json, numpy as np, awkward as ak, uproot
td, outj = sys.argv[1], sys.argv[2]; res = {}
for f in sorted(glob.glob(f"{td}/*/*_full.root")):
    s = os.path.basename(os.path.dirname(f)); t = uproot.open(f)["Delphes"]
    pid = t["Particle/Particle.PID"].array(); d1 = t["Particle/Particle.D1"].array(); d2 = t["Particle/Particle.D2"].array()
    ap = abs(pid); idx = ak.local_index(pid); r = {}
    def decay_fracs(code):
        d1p = abs(pid[ak.where(d1 >= 0, d1, 0)]); d2p = abs(pid[ak.where(d2 >= 0, d2, 0)])
        last = (ap == code) & (d1p != code) & (d1 >= 0)
        return last, d1p, d2p
    for code, nm in ((25, "H"), (23, "Z"), (24, "W")):
        last, a, b = decay_fracs(code); n = int(ak.sum(last))
        if n == 0: continue
        had = last & (a >= 1) & (a <= 5) & (b >= 1) & (b <= 5); bb = last & (a == 5) & (b == 5)
        r[nm] = dict(n=n, frac_qq=float(ak.sum(had) / n), frac_bb=float(ak.sum(bb) / n))
    res[s] = r
json.dump(res, open(outj, "w"), indent=1); print(json.dumps(res, indent=1))
