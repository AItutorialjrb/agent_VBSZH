import json, glob, csv, numpy as np, collections
P = "/eos/home-r/rjiang/vbs_zh_codex_starter"; Z = P + "/p2/combination/zh_check/out"
ZF, BGG = 0.9783, 0.00227; BRZLL = 0.033632 + 0.033662
S = {r["sample"]: r for r in csv.DictReader(open(P + "/p2/production/wh/SAMPLES.csv"))}
kZ = {"S_EW_ZHjj": ZF*BGG, "H_QCD_ZHjj": ZF*BGG, "B_EW_zaajj_vbs_is1h": ZF, "B_EW_zaajj_vbs_is2": ZF, "B_EW_zaajj_vbs_is3": ZF, "B_QCD_zaajj_nomjj": ZF, "B_QCD_zaajj_vbs": ZF,
      "H_ZH_tautau": BGG, "H_ggZH_py8dec": BRZLL*BGG, "H_ttH": BGG, "T_ttaa": 1.0, "F_QCD_llajj_vbs": 1.0, "F_EW_llajj_vbs": 1.0, "F_QCD_llajj_nomjj": 1.0, "T_tta": 1.0, "T_tWa": 1.0}
for t in ("lam_m100", "lam_m050", "lam_p000", "lam_p050", "lam_p100", "lam_p150", "cpo_m2", "cpo_p2"): kZ[f"K_EW_ZHjj_{t}"] = ZF*BGG
acc = collections.defaultdict(lambda: dict(n_files=0, n_events=0, c={}, nw=[]))
for f in sorted(glob.glob(Z + "/ortho_*__*.json")):
    d = json.load(open(f)); lab = d["label"].rsplit("__", 1)[0]; a = acc[lab]; a["n_files"] += d["n_files"]; a["n_events"] += d["n_events"]; a["nw"] += d["counts"].get("zh_sr_nowindow_mgg_w", []) if False else d.get("zh_sr_nowindow_mgg_w", [])
    for k, v in d["counts"].items():
        c = a["c"].setdefault(k, [0, 0.0, 0.0]); c[0] += v["raw"]; c[1] += v["sumw_pb"]; c[2] += v["sumw2"]
res = {}
for lab, a in acc.items():
    side, name = lab.split("_", 1); ch = "WH" if side == "WH" else "ZH"
    k = float(S.get(name, {"k": 1.0})["k"]) if ch == "WH" else kZ[name]; N = a["n_events"]; fac = 500*1e3*k/N
    rows = {}
    for fl, (raw, sw, sw2) in a["c"].items():
        rows[fl] = dict(raw=int(raw), yield_500fb=fac*sw, mc_unc_500fb=fac*np.sqrt(sw2), ul95_raw=(3.0 if raw == 0 else None), ul95_yield_500fb=(fac*(sw/max(raw, 1) if raw else (a["c"]["all"][1]/max(a["c"]["all"][0], 1)))*3.0 if raw == 0 else None))
    nw = a["nw"]
    res[lab] = dict(channel_of_sample=ch, sample=name, k=k, n_files=a["n_files"], n_events_processed=N, norm_factor_500fb_per_sum_w_pb=fac, flags=rows,
                    zh_sr_without_window_105_165=dict(raw=len(nw), yield_500fb=fac*sum(w for m, w in nw), mc_unc_500fb=fac*float(np.sqrt(sum(w*w for m, w in nw)))))
tot_both_sr = sum(r["flags"]["both_sr"]["raw"] for r in res.values()); tot_both_pre = sum(r["flags"]["both_pre"]["raw"] for r in res.values())
ZH_in_WH_SR = {k: v for k, v in res.items() if v["channel_of_sample"] == "ZH"}
out = dict(
 description="Event-level orthogonality of the frozen ZH SR and the WH SR (cut-based primary). Selections: see zh_check/ortho.py docstring (ZH: frozen optimum of final.json; WH: 05_selection.md primary re-implemented on Delphes objects; the re-implementation reproduces the WH signal selection efficiency 829/20000 on the first file against 8157/200000 from the WH table).",
 samples_note="All files for the WH package samples and the ZH signal/shared-background samples; F_QCD_llajj_vbs, F_EW_llajj_vbs, T_tta, T_tWa, F_QCD_llajj_nomjj: first 100 files only (each ~200k events), yield estimated as the subset rate x full normalisation (subset weighted yield = what 100 files would contribute if they were the full sample: factor N_full/N_processed not applied; compare raw counts).",
 yield_definition="yield_500fb = 500 * 1e3 * k * sum(Event.Weight[pb]) / N_processed (subset normalisation for samples with a subset)",
 flags={"zh_pre": "OSSF pair (pT>15) + >=2 photons (pT>20) + >=2 jets", "zh_sr": "full frozen ZH SR incl. the m_gg window", "wh_pre": "one lepton block (exactly one lepton pT>10, pT>25, iso<0.15) + MET>30 + 2 photons pT>25 + b-veto + 2 jets pT>30", "wh_sr": "full WH SR incl. the m_gg window", "both_pre": "zh_pre and wh_pre", "both_sr": "zh_sr and wh_sr", "zh_sr_nl10eq1": "ZH SR events with exactly one lepton pT>10 (must be 0)", "zh_pre_nl10eq1": "same at the pre-selection level"},
 total_overlap=dict(both_sr_raw=int(tot_both_sr), both_pre_raw=int(tot_both_pre), n_samples=len(res), n_events=int(sum(r["n_events_processed"] for r in res.values()))),
 notes=["F_QCD_llajj_loose (WH v1.1 loose-cut Z gamma jj sample, the WH lost-lepton class at about 64 % of b) and the v1.2 WH-package F_QCD_llajj_nomjj are included (labels WH_F_QCD_llajj_loose, WH_F_QCD_llajj_nomjj); the frozen ZH F_QCD_llajj_vbs, F_EW_llajj_vbs and F_QCD_llajj_nomjj (first 100 files) are included under ZH_.",
 "The fake-photon rows (F_*, T_tta, T_tWa) were tested with the real-photon selection: at least 2 reco photons in the preselection (zh_pre) and in the SR. In the fake-factor method the second photon is a converted jet (weights), so the one-photon level matters too. The exclusivity argument does not use photons: both SRs are defined on the lepton collection (ZH: two OSSF leptons pT>15; WH: exactly one lepton pT>10), so it holds identically for the one-photon fake-method rows; zh_pre_nl10eq1 and zh_sr_nl10eq1 are the explicit counts (0).",
 "The WH lepton veto counts every lepton with pT>10 (e |eta|<2.5, mu |eta|<2.4) without an isolation requirement (skim.py nlep10 and bgmodel.regions lep[5]==1, reproduced in ortho.py); the text of 05_selection.md reads 'pT>25 (iso<0.15), no second lepton pT>10'. The veto in the code is therefore stricter than a veto restricted to isolated leptons; the overlap is zero by the code definition. If the veto were ever made isolation-dependent the exclusivity must be re-checked (a ZH event with a non-isolated second lepton would then no longer be vetoed)."], orthogonal_by_construction="WH SR requires exactly one lepton with pT>10 (electron |eta|<2.5, muon |eta|<2.4); the ZH SR requires two opposite-sign same-flavour leptons with pT>15 within the same eta ranges; the two requirements are mutually exclusive for any event (lepton multiplicity), so the overlap is zero for every sample, including the shared backgrounds. The event-level count confirms it.",
 samples=res)
json.dump(out, open(P + "/p2/combination/vh_ws/orthogonality.json", "w"), indent=1)
print("overlap both_sr", tot_both_sr, "both_pre", tot_both_pre, "events", out["total_overlap"]["n_events"], "samples", len(res))
for lab, r in sorted(res.items()):
    f = r["flags"]; print(f"{lab:32s} N={r['n_events_processed']:8d} zh_pre={f['zh_pre']['raw']:6d} zh_sr={f['zh_sr']['raw']:6d} wh_pre={f['wh_pre']['raw']:6d} wh_sr={f['wh_sr']['raw']:6d} both_pre={f['both_pre']['raw']} both_sr={f['both_sr']['raw']} nl10eq1={f['zh_pre_nl10eq1']['raw']} | ZH-SR(no win) {r['zh_sr_without_window_105_165']['raw']}")
