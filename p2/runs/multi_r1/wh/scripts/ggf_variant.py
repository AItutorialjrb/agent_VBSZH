#!/usr/bin/env python3
"""Z0 / counting Z with the D38 H_ggF_jj UL added as extra background (shape = nominal smooth background, window +-3.5 GeV holds the UL). Writes work/stat/ggf_variant_v11.json. Env STAT_V11=1 STAT_TABLE=table_v11 STAT_YIELDS=yields_v11."""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stat_lib import *
t, meta, Y = load(); ul = json.load(open(f"{WH}/work/ggf_ul.json"))["selected_window"]["UL95"]; m0 = selmask(t)
Hs, _ = smooth_hists({g: hist(t, meta, g, m0) for g in GROUPS}); bsum = sum(Hs[g][0] for g in Hs if g != "sig"); win = np.abs(CENT-125.0) < 3.5; shape = bsum/bsum[win].sum(); extra = ul*shape; out = dict(UL_events_in_window_500=ul, rows=[])
s_w = float(t["w"][selmask(t, window=True) & (t["cls"] == meta["classes"]["signal"])].sum()); b_w = float(bsum[win].sum())
for L in (500.0, 1000.0, 3000.0):
    k = L/500.0; base = build(t, meta, Y, lumi=L); z0 = z0_asimov(base)[0]; mod = build(t, meta, Y, lumi=L, extra_bkg=extra*k); z1 = z0_asimov(mod)[0]; mod3 = build(t, meta, Y, lumi=L, extra_bkg=3*extra*k); z3 = z0_asimov(mod3)[0]
    out["rows"].append(dict(lumi=L, Z0_nominal=z0, Z0_with_ggF_UL=z1, Z0_with_proxy_x3_D36=z3, Z_eq1_smoothb_nominal=eq1(s_w*k, b_w*k), Z_eq1_smoothb_with_UL=eq1(s_w*k, (b_w+ul)*k)))
json.dump(out, open(f"{WH}/work/stat/ggf_variant_v11.json", "w"), indent=1); print(json.dumps(out))
