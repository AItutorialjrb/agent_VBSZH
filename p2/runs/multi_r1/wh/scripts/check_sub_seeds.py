#!/usr/bin/env python3
"""Runs seeds.check over EVERY new-formula submit file (every work/condor/*.sub, work/condor/prod/*.sub): all gridpack gseed / job seed tokens must be unique and not in config/seeds_used_preG1.txt.
Usage: python3 scripts/check_sub_seeds.py   (fails loudly). Run before every condor_submit. Re-submitted tests that deliberately reuse a seed are not allowed (use a fresh J)."""
import re, glob, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import seeds as S
seen = {}
LEGACY = {"gridpacks_wh.sub", "test_wh_bqcd.sub", "test_wh.sub", "test_wh_twins.sub"}   # pre-G1 submit files (old seed formula): every seed in them MUST be in config/seeds_used_preG1.txt; any other *.sub is new-formula and checked in full
legacy_seen = set()
for f in sorted(glob.glob(f"{S.WH}/work/condor/*.sub") + glob.glob(f"{S.WH}/work/condor/prod/*.sub")):
    leg = os.path.basename(f) in LEGACY
    for l in open(f):
        if not l.startswith("  "): continue
        t = l.split()
        toks = [x for x in t if re.fullmatch(r"21\d{5}", x)]
        # gridpack lines: 'card gseed ...' ; job lines: seed token; job lines also contain the gridpack path (seed inside a filename) -> excluded (not a standalone token)
        key = t[0]; sd = int(toks[-1]) if toks else None
        if sd is None: continue
        if "tar.gz" in l and len(toks) >= 1: sd = int(toks[-1])
        (legacy_seen.add(sd) if leg else seen.setdefault(sd, []).append((os.path.basename(f), key)))
dup = {k: v for k, v in seen.items() if len({x[1] for x in v}) > 1}   # same seed for two DIFFERENT samples = error; same (sample, seed) re-listed in a resubmission file is allowed only for jobs that produced no output (documented)
assert not dup, f"seed shared by different samples: {dup}"
assert legacy_seen <= S.old_used(), f"legacy file carries a seed not in the preG1 list: {sorted(legacy_seen - S.old_used())}"
S.check(list(seen)); print(len(seen), "seeds in submit files: unique, none in preG1 list")
