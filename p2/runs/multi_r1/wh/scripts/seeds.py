#!/usr/bin/env python3
"""Seed allocator (SPEC 3.4, G1 revision / D-WH-1): seed = 1e6*P + 1e5*R + 1000*sample_idx + J ; P=2 (WH), R=1 (multi_r1), J<1000.
J convention: 100 gridpack, 101 test job, 110-119 twin jobs, >=200 production jobs. Uniqueness is asserted among all seeds
requested in this run AND against the seeds already used under the old formula (config/seeds_used_preG1.txt)."""
import os, yaml
WH = "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh"
P, R = 2, 1
REG = yaml.safe_load(open(f"{WH}/config/sample_registry.yaml"))["samples"]
def seed(sample, J):
    assert 0 <= J < 1000
    return 1_000_000*P + 100_000*R + 1000*REG[sample] + J
def old_used():
    s = set()
    for l in open(f"{WH}/config/seeds_used_preG1.txt"):
        if l.strip() and not l.startswith("#"): s.add(int(l.split()[0]))
    return s
def check(seeds):
    """seeds: iterable of ints. Fails loudly on duplicates or collision with preG1 seeds."""
    seeds = list(seeds); assert len(set(seeds)) == len(seeds), "duplicate seed in request"
    clash = set(seeds) & old_used(); assert not clash, f"collision with pre-G1 seeds: {sorted(clash)}"
    assert all(0 < v < 900_000_000 for v in seeds)
    return True
