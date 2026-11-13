#!/usr/bin/env python3
"""D38 fallback (D-WH-14: gridpack 893012 produced nothing): conservative SCALED CENTRAL PROXY (R x VBF-proxy yield; NOT a statistical 95 % UL) for the H_ggF_jj non-prompt-lepton row.
No ggF H + jets sample exists (the only gluon-initiated Higgs row, H_ggZH_wh, is gg->ZH, a different final state). Method: the H_VBFH_jj non-prompt-lepton yield (light-misID x (1+factorised HF), same selection, same per-jet misID) is a proxy for a Higgs+2-jet event topology with jets -> lepton;
proxy = R x max(Y_VBFH, 2.996 x per-row weight) with R = sigma_ggF,incl / sigma(H_VBFH_jj row) = 52.23 pb / 4.124 pb = 12.66 (the SAMPLE sigma 4.124 pb is used because the yield being scaled is proportional to the sample sigma; with the LHCHWG VBF 4.078 pb R would be 12.81, +1 %) (LHCHWG 13.6 TeV, mH=125: ggF N3LO 52.23 pb, VBF 4.078 pb, https://twiki.cern.ch/twiki/bin/view/LHCPhysics/LHCHWG136TeVxsec_extrap).
R is an OVER-estimate by construction in the kinematic sense (qualitative, not quantified: no ggF H+jj sample exists), but gluon jets may fake leptons MORE than the quark-jet-dominated VBF rows, so the sign of the net bias is not established; the D36 npl x3 scan is applied to it (ggf_variant.py): it assumes every inclusive ggF event has the two jets of the VBFH row and the VBF efficiency of the selection (ggF H+jj is softer: lower m_jj/|deta| efficiency). Writes work/ggf_ul.json."""
import sys, json, numpy as np
sys.path.insert(0, "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh/scripts")
WH = "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh"; R = 52.23/4.124
Y = json.load(open(f"{WH}/work/bgmodel/yields_v11.json")); out = dict(R=R, method=__doc__, regions={})
for rn in ("PRE", "VBS", "PEAK"):
    s = Y["regions"][rn]["samples"]["H_VBFH_jj"]; y = s["fakelep_nom"]["Y"]+s["heavy_flavour_factorised"]["Y"]; w1 = s["unit_event_weight"]*4e-5   # per-row weight of a misID row ~ unit event weight x f_l (nominal)
    ul = R*max(y, 2.996*w1); out["regions"][rn] = dict(Y_VBFH_proxy=y, raw_rows=s["fakelep_nom"]["nraw"], UL95=ul)
cb = json.load(open(f"{WH}/work/sel/selection_final.json"))["cut_based"]["cuts"]; t = dict(np.load(f"{WH}/work/sel/table_v11.npz")); meta = json.load(open(f"{WH}/work/sel/table_v11_meta.json")); i = meta["samples"].index("H_VBFH_jj")
m = (t["sid"] == i) & (t["mjj"] > cb["mjj"]) & (t["deta"] > cb["deta"]) & (t["ptgg"] > cb["ptgg"]) & (t["met"] > cb["met"]) & (t["ptl"] > cb["ptl"]) & (np.abs(t["mgg"]-125) < cb["hw"])
w = t["w"][m]; wrow = float(np.abs(t["w"][t["sid"] == i]).mean()); y = float(w.sum()); out["selected_window"] = dict(Y_VBFH_proxy=y, raw_rows=int(m.sum()), mean_abs_row_weight=wrow, UL95=R*max(y, 2.996*wrow))
json.dump(out, open(f"{WH}/work/ggf_ul.json", "w"), indent=1); print(json.dumps({k: v for k, v in out.items() if k != "method"}))
