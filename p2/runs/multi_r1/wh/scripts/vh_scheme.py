#!/usr/bin/env python3
"""Writes p2/combination/vh_ws/correlation_scheme.json from the committed joint workspace: every nuisance parameter, the channels/samples it acts on, and whether it is correlated (acts in both channels with the same name) or channel-specific."""
import json, sys
VW = "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/combination/vh_ws"; ws = json.load(open(f"{VW}/VH_workspace.json")); par = {}
for ch in ws["channels"]:
    for sm in ch["samples"]:
        for m in sm["modifiers"]:
            e = par.setdefault(m["name"], dict(type=m["type"], channels=set(), samples={}))
            e["channels"].add(ch["name"]); e["samples"].setdefault(ch["name"], []).append(sm["name"])
COMMON = {"lumi", "pheff", "lepeff", "phscale", "phres", "scale_sig", "pdf_sig", "scale_hqcd", "scale_prompt_qcd", "scale_prompt_ew", "scale_higgs_other", "fakerate", "mu", "mu_WH", "mu_ZH"}
out = {"description": "Correlation scheme of the joint WH+ZH pyhf likelihood (A3, D47 (1)). correlated = one parameter acting in both channels (same name); uncorrelated = acts in one channel only (names carry the channel: mcstat = WH per-bin, mcstat_zh = ZH per-bin, zh_* ZH-only; WH-only names listed).",
       "rule": "correlated: luminosity, photon efficiency, lepton efficiency, photon energy scale and m_gg resolution (histosys on the real-photon signal samples), QCD scale and PDF of the common processes (EW VH signal family WH/ZH EW, QCD VH, QCD/EW V gamma gamma, ggZH/ttH/tH 'other Higgs'); fake-photon rate (D39 floor) correlated across the fake-photon rows of both channels; uncorrelated: MC statistics (per bin, per channel), channel-specific background normalisations (class norms, PS, C factors, coverage, non-closure, non-prompt, ZH-only theory/normalisations) unless the same process in both channels.",
       "tau": "tau_r (W rows, WH) and tau_r_zrows (Z-lepton rows in the WH SR) are WH-only; the ZH channel has no tau nuisance (Z->tautau->ll is 0.31 %); ZH rows in the WH SR (EW/QCD ZHjj lost lepton) are SIGNAL-LIKE samples: scaled by mu_ZH (2D) or the common mu (mu_VH), share scale_sig / scale_hqcd with the ZH channel.",
       "wh_signal_in_zh_sr": "not in the fit: 0 raw events of 300k in the ZH SR, UL95 4.65e-4 events (zh_channel_inputs.json['wh_signal_in_zh_sr']); would carry mu_WH.", "parameters": {}}
for n, e in sorted(par.items()):
    ch = sorted(e["channels"]); out["parameters"][n] = dict(type=e["type"], channels=ch, status=("correlated" if len(ch) == 2 else "channel-specific"), samples=e["samples"], declared_common=(n in COMMON))
json.dump(out, open(f"{VW}/correlation_scheme.json", "w"), indent=1); print({n: v["status"] for n, v in out["parameters"].items() if v["status"] == "correlated"}); print(len(out["parameters"]), "parameters")
