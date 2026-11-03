#!/usr/bin/env python3
"""A1-A4, A7 (2026-11-03): collect the theory / generator studies into work/theory/theory_summary.json (read by
final_analysis.py). Inputs (all produced by scripts/theory/lhe_theory.py, scripts/analysis/{mjj_resolution,object_eff}.py):
  th_<sample>.json  scale (7-point envelope) and PDF (NNPDF3.1 replicas) in region R (or inclusive for samples without
                    a parton-level VBS topology: ggZH, ttH, top) -> symmetrised relative uncertainty max(up, down) and pdf std
  thj_I_ZHjj / thj_S_EW_ZHjj / thj_H_QCD_ZHjj   ZHjj EW x QCD interference in the VBS jet region (Z, H undecayed / decayed)
  th_{I,E}_zaajj_nodec_is{1,2,3}.json            Zgg jj interference vs EW (undecayed Z), summed over beam-1 splits
  th_Q_llaa0j / th_Q_zaa0j                       off-shell/FSR ratio after the non-jet region cuts
  mjj_resolution.json, object_eff.json
Usage: python3 -P scripts/theory/theory_summary.py"""
import json, os, glob, numpy as np
W = "/eos/home-r/rjiang/vbs_zh_codex_starter/work/theory"; L = lambda f: json.load(open(f"{W}/{f}")) if os.path.exists(f"{W}/{f}") else None
S = dict(processes={})
for f in sorted(glob.glob(f"{W}/th_*.json")):
    s = os.path.basename(f)[3:-5]; d = json.load(open(f))
    if s.startswith(("Q_", "I_", "E_")): continue
    key = "R" if d.get("R", {}).get("n", 0) >= 200 and d["kind"] != "incl" else "incl"; o = d[key]
    if "scale_up" not in o: continue
    S["processes"][s] = dict(region=key, n=o["n"], scale_up=o["scale_up"], scale_down=o["scale_down"], scale_sym=max(o["scale_up"], o["scale_down"]),
                             pdf=o.get("pdf_std", 0.0), total=float(np.hypot(max(o["scale_up"], o["scale_down"]), o.get("pdf_std", 0.0))))
# ZHjj interference (VBS jet region): sigma_I(R) = <w> over all events in R / N; EW and QCD Z-undecayed sigma from report 03
I, E, Q = L("thj_I_ZHjj.json"), L("thj_S_EW_ZHjj.json"), L("thj_H_QCD_ZHjj.json")
if I and E and Q:
    sI = I["R"]["sum_w"]/I["n_events"]*1e3; eI = np.sqrt(I["R"]["sum_w2"])/I["n_events"]*1e3   # fb
    SEW_ND, SQCD_LL, BRLL_MG = 18.64, 10.20, None
    epsE = E["R"]["sum_w"]/E["incl"]["sum_w"]; epsQ = Q["R"]["sum_w"]/Q["incl"]["sum_w"]
    sEW = SEW_ND*epsE
    sQCD_nd = 18.64*(Q["incl"]["sum_w"]/Q["n_events"])/(E["incl"]["sum_w"]/E["n_events"])*epsQ   # QCD/EW ratio at equal Z decay
    S["interference_ZHjj"] = dict(sigma_I_incl_fb=I["incl"]["sum_w"]/I["n_events"]*1e3, sigma_I_R_fb=sI, sigma_I_R_err_fb=eI, sigma_EW_R_fb=sEW,
        sigma_QCD_R_fb=sQCD_nd, frac_of_EW=sI/sEW, frac_of_EW_err=eI/sEW, frac_of_EWplusQCD=sI/(sEW + sQCD_nd), n_R=I["R"]["n"],
        note="VBS jet region mjj>500, |deta|>3.5 at parton level; Z and H undecayed in the I sample, EW/QCD R-efficiencies from the Z->ll Tier-1 LHE")
# Zgg jj interference
iz = [(L(f"th_I_zaajj_nodec_is{i}.json"), L(f"th_E_zaajj_nodec_is{i}.json")) for i in (1, 2, 3)]
if all(a and b for a, b in iz):
    sI = sum(a["R"]["sum_w"]/a["n_events"] for a, b in iz)*1e3; sE = sum(b["R"]["sum_w"]/b["n_events"] for a, b in iz)*1e3
    eI = np.sqrt(sum(a["R"]["sum_w2"]/a["n_events"]**2 for a, b in iz))*1e3
    sIi = sum(a["incl"]["sum_w"]/a["n_events"] for a, b in iz)*1e3; sEi = sum(b["incl"]["sum_w"]/b["n_events"] for a, b in iz)*1e3
    S["interference_Zaajj"] = dict(sigma_I_R_fb=sI, sigma_I_R_err_fb=eI, sigma_EW_R_fb=sE, frac_of_EW=sI/sE, frac_of_EW_err=eI/sE,
        frac_of_EW_incl=sIi/sEi, status="computed", note="undecayed on-shell Z, VBS jet + photon cuts (105<mgg<145), summed over beam-1 splits")
else:
    S["interference_Zaajj"] = dict(frac_of_EW=0.0244/0.263, frac_of_EW_err=None, status="reference value (arXiv:2512.07689 Table II, inclusive, on-shell EW signal); own MG5 run pending")
a, b = L("th_Q_llaa0j.json"), L("th_Q_zaa0j.json")
if a and b:
    sa, sb = a["R"]["sum_w"]/a["n_events"], b["R"]["sum_w"]/b["n_events"]; r = sa/sb
    err = r*np.sqrt(a["R"]["sum_w2"]/a["R"]["sum_w"]**2 + b["R"]["sum_w2"]/b["R"]["sum_w"]**2)
    S["offshell_Zaa"] = dict(ratio=r, ratio_err=float(err), n_llaa=a["R"]["n"], n_zaa=b["R"]["n"], ratio_incl=(a["incl"]["sum_w"]/a["n_events"])/(b["incl"]["sum_w"]/b["n_events"]),
        reference_after_mll_cut=6.27/5.56, reference_after_all_cuts=17.55/16.28, applied_factor=r, applied_unc=abs(r - 1)/2,
        note="QCD 0-jet proxy (pp > l+l- aa vs pp > z aa, z > l+l-), all region cuts except jets; transferred to EW and QCD Zgg jj")
S["mjj_resolution"] = L("mjj_resolution.json"); S["object_eff"] = L("object_eff.json")
json.dump(S, open(f"{W}/theory_summary.json", "w"), indent=1, default=float)
for k, v in S["processes"].items(): print(f"{k:24s} {v['region']:4s} scale {v['scale_sym']:.3f} pdf {v['pdf']:.3f} total {v['total']:.3f}")
for k in ("interference_ZHjj", "interference_Zaajj", "offshell_Zaa"): print(k, {kk: (round(vv, 5) if isinstance(vv, float) else vv) for kk, vv in (S.get(k) or {}).items() if kk != "note"})
