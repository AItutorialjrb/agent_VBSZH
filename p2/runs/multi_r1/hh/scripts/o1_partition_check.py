#!/usr/bin/env python3
"""O1 flavour-partition equality (02 report): sigma(Q_4j) x f(bb-bar in hard final state) must equal sigma(Q_bbjj) for the same generator filter. Fraction f from the hard-process flavour record (status-23 partons), binomial error.
Usage: o1_partition_check.py <matrix.yaml> <prod_root> <out.json> 4j:bbjj [4j:bbjj ...]"""
import sys, json, yaml, numpy as np, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hh_reco as R
my, root, outj = sys.argv[1:4]; M = {s["name"]: s for s in yaml.safe_load(open(my))["samples"]}; res = {}
for pr in sys.argv[4:]:
    a, b = pr.split(":"); d = R.load(R.sample_files(f"{root}/{a}")); n = d["n_gen"]; k = int(d["bbbar_hard"].sum()); f = k / n; ef = np.sqrt(f * (1 - f) / n)
    sa, sb = M[a]["sigma_pb"], M[b]["sigma_pb"]; esa, esb = M[a]["sigma_err_pb"], M[b]["sigma_err_pb"]; sub = sa * f; esub = sub * np.hypot(ef / f if f > 0 else 0, esa / sa)
    res[a] = dict(N=n, k_bbbar=k, f=f, sigma_4j_pb=sa, sigma_sub_pb=sub, sigma_sub_err_pb=esub, sigma_bbjj_pb=sb, sigma_bbjj_err_pb=esb, ratio=sub / sb, pull=(sub - sb) / np.hypot(esub, esb))
    print(a, f"N={n} k={k} f={f:.4f}  sigma_4j*f = {sub:.5g} +- {esub:.2g} pb  vs sigma_bbjj({b}) = {sb:.5g} +- {esb:.2g} pb  ratio {sub/sb:.3f} pull {res[a]['pull']:+.1f}")
json.dump(res, open(outj, "w"), indent=1)
