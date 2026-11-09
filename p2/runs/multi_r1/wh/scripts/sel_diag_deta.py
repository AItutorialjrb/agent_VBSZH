#!/usr/bin/env python3
"""DIAGNOSTIC ONLY (not adopted): the pre-declared grid has |deta_jj| > 4.0 as its upper edge. Extended grid deta in {2.5..5.5} (met/mt/ptl/z* at baseline, which were not binding), same admissibility and plateau rule.
Writes work/sel/diag_deta.json."""
import json, itertools, numpy as np
WH = "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh"
t = dict(np.load(f"{WH}/work/sel/table.npz")); cid = json.load(open(f"{WH}/work/sel/table_meta.json"))["classes"]; sig = t["cls"] == cid["signal"]
def Z(s, b): return float(np.sqrt(2*((s+b)*np.log1p(s/b)-s))) if s > 0 and b > 0 else 0.0
def ev(mjj, de, pg, hw):
    m = (t["mjj"] > mjj) & (t["deta"] > de) & (t["ptgg"] > pg) & (np.abs(t["mgg"]-125) < hw); s = t["w"][m & sig].sum(); wb = t["w"][m & ~sig]; b = wb.sum()
    return dict(s=float(s), b=float(b), Z=Z(s, b), neff=float(b**2/(wb**2).sum()) if len(wb) else 0.0, relmc=float(np.sqrt((wb**2).sum())/b) if b > 0 else 9.9, cuts=dict(mjj=mjj, deta=de, ptgg=pg, hw=hw))
res = [ev(*c) for c in itertools.product([500, 600, 700, 800, 900], [2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5], [0, 50, 75, 100], [2.5, 3.5, 5.0])]
adm = [r for r in res if r["neff"] >= 30 and r["relmc"] <= 0.3 and r["s"] > 0]; zm = max(r["Z"] for r in adm); ch = max([r for r in adm if r["Z"] >= 0.97*zm], key=lambda r: (r["s"], r["neff"]))
out = dict(Zmax=max(adm, key=lambda r: r["Z"]), plateau_choice=ch, chosen_cuts_with_deta_4p5=ev(600, 4.5, 75, 3.5), chosen_cuts_with_deta_5p0=ev(600, 5.0, 75, 3.5), reference=ev(600, 4.0, 75, 3.5))
json.dump(out, open(f"{WH}/work/sel/diag_deta.json", "w"), indent=1); print(json.dumps({k: (v["Z"], v["cuts"], round(v["neff"])) for k, v in out.items()}))
