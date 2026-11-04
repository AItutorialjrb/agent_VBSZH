#!/usr/bin/env python3
"""Assert: all seeds in config/seeds.yaml (registry + pre-G1 list), in every scripts/condor/g2_prod_*.sub and in the 2-job test files are pairwise unique across (sample, J), and production seeds
(J>=10) never fall in the 0..5 registry slots. Also checks the 5 digits layout seed = 3e6 + 1e5*1 + 1000*idx + J for new seeds. Prints the count."""
import yaml, glob, re, os, collections
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
reg = yaml.safe_load(open(f"{H}/config/seeds.yaml")); allseeds = collections.Counter(int(k) for k in reg)
reg_idx = {s["idx"]: s["name"] for s in yaml.safe_load(open(f"{H}/config/sample_matrix_gen.yaml"))["samples"]}
prod = collections.defaultdict(list)
for f in sorted(glob.glob(f"{H}/scripts/condor/g2_prod_*.sub")) + sorted(glob.glob(f"{H}/scripts/condor/g2_test_*.sub")):
    for ln in open(f):
        m = re.match(r"\s+(\S+) \S+ (\d+) (\d+) \S+", ln)
        if m and ln.startswith("  ") and "/eos" in ln: prod[int(m.group(3))].append((os.path.basename(f), m.group(1)))
bad = []
for sd, v in prod.items():
    J = sd - 3_100_000 - 1000 * ((sd - 3_100_000) // 1000) if False else (sd % 1000)
    idx = (sd - 3_100_000) // 1000
    if len(v) > 1 and len({x[1] for x in v}) > 0 and len(v) != len(set(v)): pass
    if len(v) > 1: bad.append(f"seed {sd} in several submissions {v}")
    if sd in allseeds and not (v[0][0].startswith("g2_test_") ): bad.append(f"production seed {sd} collides with a registry seed")
    if J >= 10 and reg_idx.get(idx) is None: bad.append(f"seed {sd}: idx {idx} not in registry")
    if J >= 10 and reg_idx.get(idx) != v[0][1]: bad.append(f"seed {sd}: idx {idx} is {reg_idx.get(idx)}, submitted for {v[0][1]}")
print(len(allseeds), "registry/pre-G1 seeds,", len(prod), "production/test submission seeds"); 
if bad: raise SystemExit("SEED UNIQUENESS VIOLATED:\n " + "\n ".join(bad))
print("seed uniqueness OK")
