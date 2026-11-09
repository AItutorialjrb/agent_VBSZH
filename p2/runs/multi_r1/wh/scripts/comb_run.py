#!/usr/bin/env python3
"""VH combination task (D32 item 5, D37): comb:<lumi>:<a|b>[:<zh_table.json>]  -> work/stat/comb_<lumi>_<def>.json.
WH = the 07 pyhf model (m_gg shape, all nuisances, BB); ZH = single-bin counting channel per process row from the SWAPPABLE table VH_inputs_zh.json (make_zh_table.py; default variant corrected_nominal = D37 corrected ZH numbers).
Common signal strength mu (WH + ZH, definition a: EW only; b: + QCD). Shared nuisances: lumi, pheff, lepeff, scale_sig (VH theory), scale_prompt_qcd, scale_prompt_ew, scale_hqcd, scale_higgs_other, fakerate; ZH-only nuisances keep the zh_ prefix.
Expected only (Asimov). Results: Z0 and mu95 (median, -1s, +1s) for WH alone, ZH alone, combined."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stat_lib import *
t, meta, Y = load(); _, L, d = sys.argv[1].split(":")[:3]; L = float(L); tabf = sys.argv[1].split(":")[3] if len(sys.argv[1].split(":")) > 3 else os.path.join(WH, "work/stat/VH_inputs_zh.json")
Z = json.load(open(tabf)); tab = Z["tables"][f"{int(L)}_{d}"]["rows"]
def zh_chan(only_bkg_def):
    ch = {}; sig = ["S_EW_ZHjj"] + (["H_QCD_ZHjj"] if d == "b" else []); bs = [n for n in tab if n not in sig]
    def merge(names, label):
        y = sum(tab[n]["y"] for n in names); mc = sum(tab[n]["mcstat"]**2 for n in names)**0.5; mods = {}
        for n in names:
            for (k, v) in tab[n]["nuis"]: mods[k] = mods.get(k, 0.0)+v*tab[n]["y"]/max(y, 1e-12)   # yield-weighted relative magnitude (coherent within the merged sample)
        return label, (y, mc, [(k, 1+v, max(1-v, 0.0001), (0.0, 3.0) if k == "cov" else None) for k, v in mods.items()])
    k, v = merge(sig, "zh_sig"); ch[k] = v; k, v = merge(bs, "zh_bkg"); ch[k] = v; return ch
res = dict(task=sys.argv[1], zh_table=tabf, zh_variant=Z["variant"], lumi=L, definition=d); shp = None
for name, kw in (("WH", dict()), ("combined", dict(zh_channel=zh_chan(d)))):
    mod = build(t, meta, Y, lumi=L, mu_groups=("sig",) if d == "a" else ("sig", "hqcd"), **kw); z, _ = z0_asimov(mod); res[name] = dict(Z0=z, mu95=mu95_expected(mod), npar=len(mod.config.suggested_init()))
# ZH alone: counting channel only (WH channel dropped by building a model with a tiny WH signal is not possible) -> ZH alone from the table (frozen-code numbers) for reference
zt = Z["tables"][f"{int(L)}_{d}"]; res["ZH_alone_table"] = dict(Z_eq1=zt["Z_eq1"], mu95_cls=zt["mu95_cls"], fit_Z_syst=zt["fit_Z_syst"], fit_mu95_syst=zt["fit_mu95_syst"], s=zt["s"], b=zt["b"])
os.makedirs(f"{WH}/work/stat", exist_ok=True); json.dump(res, open(f"{WH}/work/stat/comb_{int(L)}_{d}{SUF}.json", "w"), indent=1, default=float); print(json.dumps(res, default=float)[:800])
