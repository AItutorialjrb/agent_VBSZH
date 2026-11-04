#!/usr/bin/env python3
"""Pilot reuse audit (G2 review item 2): for every sample, compare the gridpack_sha256 recorded in each pilot job JSON with the sha256 in production/hh/MANIFEST.tsv; list sha256 of the MG5 card and PY8 cmnd currently in cards/ and whether they are older than the first pilot job (mtime vs job utc). Output markdown."""
import glob, json, os, hashlib, datetime, yaml
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); P = os.path.normpath(f"{H}/../../../production/hh")
man = {l.split("\t")[0]: l.rstrip("\n").split("\t") for l in open(f"{P}/MANIFEST.tsv").read().splitlines()[1:]}
gen = {s["name"]: s for s in yaml.safe_load(open(f"{H}/config/sample_matrix_gen.yaml"))["samples"]}
sh = lambda f: hashlib.sha256(open(f, "rb").read()).hexdigest()[:12]
print("| sample | jobs | gridpack sha256 (MANIFEST, 12) | jobs with identical gridpack sha | card sha256 (cards/*.mg5) | py8 cmnd sha256 | card older than first job |\n|---|---|---|---|---|---|---|")
allok = True
for n, m in man.items():
    js = [json.load(open(f)) for f in sorted(glob.glob(f"{P}/{n}/{n}_s[0-9]*.json"))]
    if not js: continue
    ok = sum(1 for j in js if j["gridpack_sha256"] == m[2]); allok &= (ok == len(js))
    cf = f"{H}/cards/{n}.mg5"; pf = f"{H}/cards/py8/{gen[n]['pythia_cmnd']}"; t0 = min(j["utc"] for j in js)
    older = os.path.exists(cf) and datetime.datetime.utcfromtimestamp(os.path.getmtime(cf)).strftime("%Y-%m-%dT%H:%M:%SZ") <= t0
    print(f"| {n} | {len(js)} | {m[2][:12]} | {ok}/{len(js)} | {sh(cf) if os.path.exists(cf) else 'n/a'} | {sh(pf)} | {'yes' if older else 'no/unknown'} |")
print("\nALL pilot jobs use the MANIFEST gridpack:", allok)
