# Interface WH <-> ZH executors (written by executor-wh, 2026-11-14)
Files in this directory: nuisance_names_wh.json (WH names, below), correlation_scheme.json (which names are shared), ANALYSIS_COMMIT (orchestrator), zh_channel_inputs.json (ZH executor), nuisance_names_zh.json (ZH executor), orthogonality.json, zh_paper_inputs.json, VH_workspace*.json (WH executor).
## zh_channel_inputs.json: schema expected by wh/scripts/vh_build.py
{ "edges": [..41 edges of the m_gg binning of the ZH SR..], "lumi_ref_fb": 500.0, "ZH_selection": "text",
  "defs": { "a": {"samples": {NAME: SAMPLE}}, "b": {"samples": {NAME: SAMPLE}} },
  "coupling": { "points": {...per-point per-bin templates for EW ZHjj in the ZH SR...}, "quad": {"alpha":[..],"beta":[..],"gamma":[..]} (per bin, events at 500 fb^-1, BR(H->gg) at SM) },
  "wh_signal_in_zh_sr": { "def_a": SAMPLE, "def_b": SAMPLE, "coupling": {"alpha":[..],"beta":[..],"gamma":[..]} } }
SAMPLE = { "role": "signal" | "signal_like" | "background", "mu": "mu_ZH" | "mu_WH" | "none",   (signal = EW ZHjj; signal_like = WH signal in the ZH SR; mu_WH for the latter)
           "nominal": [per-bin events at 500 fb^-1, BR applied once], "mcstat": [per-bin absolute MC uncertainty],
           "nuis": { NAME: {"up": [per-bin events], "down": [per-bin events]}  or  {"norm_up": x, "norm_down": y} } }
Luminosity scaling is linear (events and MC errors x L/500). Signal definition (b) = (a) plus QCD ZHjj (+interference neglected as in WH).
## Names: use the WH names (nuisance_names_wh.json) for every shared nuisance so that pyhf correlates them by name; ZH-only nuisances must carry the prefix zh_ .
