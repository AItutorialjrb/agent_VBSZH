#!/usr/bin/env python3
"""Skim a direct-mode ntuple.py output to events with an OSSF pair, >=1 photon and >=2 jets (the loosest
denominator used by the final analysis); nev_total is kept so normalisation is unchanged.
Usage: python3 -P skim_npz.py <in.npz> <out.npz>"""
import sys, numpy as np
d = np.load(sys.argv[1]); R = {k: d[k] for k in d.files}
with np.errstate(invalid="ignore"):
    keep = np.isfinite(R["mll"]) & (R["ng"] >= 1) & (R["nj"] >= 2)
n = len(R["npr"])
O = {k: (v[keep] if (v.ndim >= 1 and len(v) == n and k != "nev_total") else v) for k, v in R.items()}
np.savez_compressed(sys.argv[2], **O)
print(f"skim {sys.argv[1]}: {n} -> {keep.sum()} rows (nev_total={int(R['nev_total'])})")
