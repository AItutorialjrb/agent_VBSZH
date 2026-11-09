#!/usr/bin/env python3
"""Seed scheme (SPEC_G0 §3.4): seed = 1e6*P + 1e5*R + 1000*index + J. Asserts uniqueness and ranges. Usage: seeds.py <sample> <J>"""
import sys, re, pathlib
REG = pathlib.Path(__file__).resolve().parent.parent / "config" / "samples.yaml"
def load():
    txt = REG.read_text(); P = int(re.search(r"process_code:\s*(\d+)", txt)[1]); R = int(re.search(r"run_index:\s*(\d+)", txt)[1])
    idx = {m[1]: int(m[2]) for m in re.finditer(r"^\s+(\w+):\s*\{index:\s*(\d+)", txt, re.M)}
    vals = list(idx.values()); assert len(vals) == len(set(vals)), "duplicate sample index"; assert all(0 < i < 100 for i in vals)
    assert (P, R) == (2, 5), "single_r2 must be P=2,R=5"
    return P, R, idx
def seed(sample, J):
    P, R, idx = load(); assert 0 <= J < 1000
    return 1_000_000*P + 100_000*R + 1000*idx[sample] + J
if __name__ == "__main__":
    print(seed(sys.argv[1], int(sys.argv[2])))
