#!/usr/bin/env python3
"""Builds the SWAPPABLE ZH input table of the VH combination: p2/combination/VH_inputs_zh.json from p2/combination/zh_check/zh_corrected_inputs.json (variant selectable: corrected_nominal default, or frozen)
and the per-row nuisance magnitudes of the frozen ZH final.json (read-only). Usage: python3 make_zh_table.py [variant]. Row = {y, mcstat, nuis:[[name, rel]]} per lumi/def; names shared with the WH model are renamed (correlation map in 'name_map')."""
import json, sys
var = sys.argv[1] if len(sys.argv) > 1 else "corrected_nominal"
Z = json.load(open("/eos/home-r/rjiang/vbs_zh_codex_starter/p2/combination/zh_check/zh_corrected_inputs.json")); F = json.load(open("/eos/home-r/rjiang/vbs_zh_codex_starter/work/final_ntuples/final.json"))
MAP = {"lumi": "lumi", "th_sig": "scale_sig", "th_ewzaa": "scale_prompt_ew", "th_qcdzaa": "scale_prompt_qcd", "th_qcdzh": "scale_hqcd", "th_ggzh": "scale_higgs_other", "th_tth": "scale_higgs_other", "th_zhtt": "scale_higgs_other"}
out = dict(variant=var, source="zh_corrected_inputs.json results[%s] (+ nuisance magnitudes of frozen final.json 'nuisances')" % var, name_map=MAP, shared_assumed=dict(pheff=0.04, lepeff=0.02, fakerate=0.2), tables={})
for key, r in Z["results"][var].items():
    rows = {}; comp = r.get("components"); sc = 1.0
    if comp is None: comp = Z["results"][var]["500_" + key.split("_")[1]]["components"]; sc = float(r["L"])/500.0   # 1000 fb^-1: linear luminosity scaling of the 500 fb^-1 components (the ZH study does the same)
    for nm, c in comp.items():
        nu = [[MAP.get(k, "zh_"+k), v] for k, v in F["nuisances"].get(nm, F["nuisances"].get("B_EW_Zaajj_vbs_is1" if nm.startswith("B_EW") else nm, {})).items()] if nm in F["nuisances"] else []
        if nm in ("F_QCD_Zajj", "F_EW_Zajj"): nu = [["fakerate", 0.2], ["zh_fakecal", 0.26]]+[[k, v] for k, v in nu if k == "lumi"]
        nu += [["pheff", 0.04], ["lepeff", 0.02]]
        rows[nm] = dict(y=c["y"]*sc, mcstat=c["mcstat"]*sc, nuis=nu)
    out["tables"][key] = dict(rows=rows, s=r["s"], b=r["b"], Z_eq1=r["Z_eq1"], mu95_cls=r["mu95_cls"], fit_Z_syst=r["fit_Z_syst"], fit_mu95_syst=r["fit_mu95_syst"])
json.dump(out, open("/eos/home-r/rjiang/vbs_zh_codex_starter/p2/combination/VH_inputs_zh.json", "w"), indent=1); print("rows", {k: len(v["rows"]) for k, v in out["tables"].items()})
