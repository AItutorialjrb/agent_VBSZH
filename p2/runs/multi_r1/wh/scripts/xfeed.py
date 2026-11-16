#!/usr/bin/env python3
"""Cross-feed yields with explicit region/window (W1): EW ZHjj lost-lepton rows in the WH SR (workspace sample zhjj_ew = ZH_EW_ZHjj_lostlep, 200k frozen events; coupling-fit template K_EW_ZHjj_lam_p100 = HC UFO SM point, 50k events) and the WH signal. 500 fb^-1, cut-based selection mjj>600, |deta|>4, pT(gg)>75."""
import json, numpy as np
WH = "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh"; VW = "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/combination/vh_ws"
ws = json.load(open(f"{VW}/VH_workspace.json")); wr = [c for c in ws["channels"] if c["name"] == "SR"][0]; edges = np.arange(100.0, 180.01, 2.0); cen = 0.5*(edges[:-1]+edges[1:]); out = {}
for g in ("zhjj_ew", "zhjj_qcd", "sig"):
    y = np.array([x for x in wr["samples"] if x["name"] == g][0]["data"]); out[g] = dict(workspace_sum_100_180=float(y.sum()), workspace_bins_122_128_centres_123_125_127=float(y[np.abs(cen-125) < 3.5].sum()), workspace_bins_120_130=float(y[np.abs(cen-125) < 5.0].sum()), workspace_bins_pm2sigma_eff_2p1_centre_in=float(y[np.abs(cen-125.06) < 4.2].sum()))
sel = json.load(open(f"{WH}/work/sel/selection_final.json"))["cut_based"]["cuts"]; t = dict(np.load(f"{WH}/work/sel/table_v12.npz")); meta = json.load(open(f"{WH}/work/sel/table_v12_meta.json")); m = (t["mjj"] > sel["mjj"]) & (t["deta"] > sel["deta"]) & (t["ptgg"] > sel["ptgg"]) & (t["met"] > sel["met"]) & (t["ptl"] > sel["ptl"])
for s_ in ("ZH_EW_ZHjj_lostlep", "S_EW_WHjj"):
    k = m & (t["sid"] == meta["samples"].index(s_)); out[s_ + "_table_unbinned_|mgg-125|<3.5"] = float(t["w"][k & (np.abs(t["mgg"]-125) < 3.5)].sum()); out[s_ + "_table_unbinned_100_180"] = float(t["w"][k].sum())
c = json.load(open(f"{WH}/work/stat/couplings_vh_kzneg_v12.json")); out["K_EW_ZHjj_template_in_mT_bins_window_pm3p5"] = c["wh_zhjj_in_whSR_SM_events"]; out["K_EW_WHjj_template_window_pm3p5"] = c["wh_signal_SM_events"]
out["note"] = "The workspace (m_gg 100-180, 2 GeV bins) and the unbinned +-3.5 GeV window are different regions: the window convention matters (bin edges 122-128 vs the exact |m-125|<3.5, vs +-2 sigma_eff = +-4.2 GeV); the coupling-fit number is a different ZHjj sample (HC SM point) in the +-3.5 GeV window."
json.dump(out, open(f"{WH}/work/stat/xfeed_v12.json", "w"), indent=1); print(json.dumps(out)[:900])
