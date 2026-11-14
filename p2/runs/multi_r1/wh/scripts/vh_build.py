#!/usr/bin/env python3
"""Joint VH workspace builder (A3, D47 (1)). One pyhf model: WH channel (m_gg 100-180, 40 bins, all WH nuisances, vh=True: EW ZHjj lost-lepton rows are a SIGNAL-LIKE sample scaled by the ZH signal strength) + ZH channel from p2/combination/vh_ws/zh_channel_inputs.json (per-bin templates by the ZH executor, schema in INTERFACE_wh.md).
Modes: common (one mu_VH on every VH signal sample, WH signal in ZH SR and ZH signal in WH SR included), 2d (mu_WH on WH signals, mu_ZH on ZH signals). Observations in the written workspace = Asimov (SM, mu = 1) expected data.
Usage: STAT_V11=1 STAT_TABLE=table_v11 STAT_YIELDS=yields_v11 python3 vh_build.py <lumi> <a|b> <common|2d> <both|wh|zh> [out.json]"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stat_lib import *
VW = os.environ.get("VH_WS", "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/combination/vh_ws")
def zh_samples(zj, d, lumi, mode, nuis=True):
    k = lumi/float(zj.get("lumi_ref_fb", 500.0)); out = []
    for nm, sm in zj["defs"][d]["samples"].items():
        mods = []
        mu = {"common": "mu", "2d": sm.get("mu", "none")}[mode] if sm.get("mu", "none") != "none" else None
        if sm["role"] in ("signal", "signal_like") and mu: mods.append(dict(name=(mu if mode == "2d" else "mu"), type="normfactor", data=None))
        mods.append(dict(name="mcstat_zh", type="staterror", data=[max(float(x)*k, 1e-12) for x in sm["mcstat"]]))
        if nuis:
            for nn, v in sm.get("nuis", {}).items():
                if "up" in v: mods.append(dict(name=nn, type="histosys", data=dict(hi_data=[float(x)*k for x in v["up"]], lo_data=[float(x)*k for x in v["down"]])))
                else: mods.append(dict(name=nn, type="normsys", data=dict(hi=float(v["norm_up"]), lo=float(v["norm_down"]))))
        out.append(dict(name="zh_"+nm, data=[float(x)*k for x in sm["nominal"]], modifiers=mods))
    return out
def sig_templates(t, meta):
    m0 = selmask(t); mg = t["mgg"]; H = lambda x: hist(t, meta, "sig", m0, mgg=x)[0]; mu = 125.0
    return dict(scale_hi=H(mg*(1+ASSUME["phscale"])), scale_lo=H(mg*(1-ASSUME["phscale"])), res_hi=H(mu+(mg-mu)*(1+ASSUME["phres"])), res_lo=H(mu+(mg-mu)*(1-ASSUME["phres"])))
def make(lumi, d, mode, which, zhfile=None, nuis=True):
    t, meta, Y = load(); zf = zhfile or f"{VW}/zh_channel_inputs.json"
    mug = {"common": {"sig": "mu", "zhjj_ew": "mu"}, "2d": {"sig": "mu_WH", "zhjj_ew": "mu_ZH"}}[mode]
    if d == "b":
        mug = dict(mug); mug["hqcd"] = mug["sig"]; mug["zhjj_qcd"] = mug["zhjj_ew"]
    poi = "mu" if mode == "common" else "mu_WH"; zs = None
    if which in ("both", "zh"): zs = zh_samples(json.load(open(zf)), d, lumi, mode, nuis)
    if which == "zh":
        # ZH-only: build the ZH channel alone through pyhf directly
        spec = dict(channels=[dict(name="ZH", samples=zs)], observations=[dict(name="ZH", data=[0.0]*len(zs[0]["data"]))], measurements=[dict(name="m", config=dict(poi=poi if mode == "common" else "mu_ZH", parameters=[]))], version="1.0.0")
        mod = pyhf.Model(spec, poi_name=poi if mode == "common" else "mu_ZH", validate=False); mod._bounds = mod.config.suggested_bounds(); mod._spec_for_ws = spec
        return mod
    mod = build(t, meta, Y, lumi=lumi, mu_groups=mug, vh=True, poi=poi, zh_samples=zs if which == "both" else None, nuis=nuis, shape_sig=(sig_templates(t, meta) if nuis else None))
    return mod
def write_ws(mod, path):
    spec = dict(mod._spec_for_ws); spec["observations"] = [dict(name=c["name"], data=list(map(float, d_))) for c, d_ in zip(spec["channels"], _split(mod, mod.expected_data(mod.config.suggested_init(), include_auxdata=False)))]
    json.dump(spec, open(path, "w"), indent=0)
def _split(mod, data):
    out = []; i = 0
    for ch in mod.config.channels: n = mod.config.channel_nbins[ch]; out.append(data[i:i+n]); i += n
    return out
if __name__ == "__main__":
    lumi, d, mode, which = float(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4]; out = sys.argv[5] if len(sys.argv) > 5 else None
    m = make(lumi, d, mode, which)
    if out: write_ws(m, out); print("written", out)
