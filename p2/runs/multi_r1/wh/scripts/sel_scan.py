#!/usr/bin/env python3
"""Cut-based selection scan with the criteria pre-declared in reports/05_selection.md sec. 0. Writes work/sel/scan.json. Usage: bash scripts/envrun.sh python3 -P scripts/sel_scan.py"""
import json, itertools, numpy as np
WH = "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh"
t = dict(np.load(f"{WH}/work/sel/table.npz")); meta = json.load(open(f"{WH}/work/sel/table_meta.json")); cid = meta["classes"]
sig = t["cls"] == cid["signal"]
G = dict(mjj=[500, 600, 700, 800, 900], deta=[2.5, 3.0, 3.5, 4.0], ptgg=[0, 50, 75, 100], met=[30, 40, 50], mt=[0, 40, 60], ptl=[25, 30, 35], hw=[2.5, 3.5, 5.0], zs=[99, 1.0, 0.7])
def Zasimov(s, b): return np.sqrt(2*((s+b)*np.log1p(s/b)-s)) if b > 0 and s > 0 else 0.0
def evaluate(c):
    m = (t["mjj"] > c["mjj"]) & (t["deta"] > c["deta"]) & (t["ptgg"] > c["ptgg"]) & (t["met"] > c["met"]) & (t["mt"] > c["mt"]) & (t["ptl"] > c["ptl"]) & (np.abs(t["mgg"]-125.0) < c["hw"]) & (t["zstar"] < c["zs"])
    s = t["w"][m & sig].sum(); mb = m & ~sig; wb = t["w"][mb]; b = wb.sum()
    neff = b**2/(wb**2).sum() if len(wb) and (wb**2).sum() > 0 else 0.0; rel = np.sqrt((wb**2).sum())/b if b > 0 else 9.9
    return dict(s=float(s), b=float(b), Z=float(Zasimov(s, b)), neff=float(neff), relmc=float(rel))
# stepwise precomputation for speed: loop over grid with masks reused per outer cuts
res = []; keys = list(G)
base_m = np.ones(len(t["w"]), bool)
for vals in itertools.product(*[G[k] for k in keys]):
    c = dict(zip(keys, vals)); r = evaluate(c); r["cuts"] = c; res.append(r)
adm = [r for r in res if r["neff"] >= 30 and r["relmc"] <= 0.30 and r["s"] > 0]
zmax = max(r["Z"] for r in adm); plate = [r for r in adm if r["Z"] >= 0.97*zmax]; choice = max(plate, key=lambda r: (r["s"], r["neff"]))
best = max(adm, key=lambda r: r["Z"])
out = dict(n_grid=len(res), n_admissible=len(adm), Zmax=best, plateau_n=len(plate), chosen=choice, grid=G)
json.dump(out, open(f"{WH}/work/sel/scan.json", "w"), indent=1)
json.dump(sorted(adm, key=lambda r: -r["Z"])[:40], open(f"{WH}/work/sel/scan_top40.json", "w"), indent=1)
print("grid", len(res), "admissible", len(adm), "plateau", len(plate)); print("Zmax", best); print("chosen", choice)
