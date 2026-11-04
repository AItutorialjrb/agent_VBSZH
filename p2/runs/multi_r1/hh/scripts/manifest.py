#!/usr/bin/env python3
"""Writes p2/production/hh/MANIFEST.tsv: for every sample the gridpack (path, sha256), the job-seed list and the complete-job count/N_LHE/bytes. Usage: manifest.py"""
import glob, os, json, hashlib, yaml
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); P = os.path.normpath(f"{H}/../../../production/hh")
m = {s["name"]: s for s in yaml.safe_load(open(f"{H}/config/sample_matrix_gen.yaml"))["samples"]}
def sha(f):
    h = hashlib.sha256()
    with open(f, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 24), b""): h.update(b)
    return h.hexdigest()
out = ["sample\tgridpack\tgridpack_sha256\tseed_gridpack\tjobs\tN_lhe\tbytes\tseeds"]
for n, s in m.items():
    gp = [f for d in (f"{P}/gridpacks", f"{H}/work/gridpacks_v2", f"{H}/work/gridpacks") for f in glob.glob(f"{d}/{n}_gridpack_s{s['seed_gridpack']}.tar.gz")]
    gp = gp[0] if gp else ""
    js = sorted(glob.glob(f"{P}/{n}/{n}_s[0-9]*.json")); N = 0; B = 0; seeds = []
    for f in js:
        if not os.path.exists(f[:-5] + ".root"): continue
        j = json.load(open(f)); N += j["n_lhe"]; seeds.append(j["mg_seed"]); B += os.path.getsize(f[:-5] + ".root") + os.path.getsize(f[:-5] + "_gen.root")
    out.append("\t".join([n, gp, sha(gp) if gp else "", str(s["seed_gridpack"]), str(len(seeds)), str(N), str(B), ",".join(map(str, seeds))]))
open(f"{P}/MANIFEST.tsv", "w").write("\n".join(out) + "\n"); print(len(out) - 1, "samples ->", f"{P}/MANIFEST.tsv")
