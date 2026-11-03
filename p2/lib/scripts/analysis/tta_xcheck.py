#!/usr/bin/env python3
"""Closeout check 1 (2026-11-03): tt̄γ / tWγ cut flow at 500 fb^-1 compared with arXiv:2512.07689 (Table III: tt̄γ
initial selection 6.44e-2 fb, after mllgg 6.40e-2 fb, after mll 1.76e-2 fb; Table IV: 0.15 +- 0.10 events at 500 fb^-1
after the full cut flow, no m_gg window). Uses the final Delphes ntuples (work/final_ntuples/T_tta__c*.npz, T_tWa__c*.npz),
with and without our hard/soft-photon overlap removal (n_prompt_photons <= 1), with photon pT > 20 GeV (reference) and
> 25 GeV (ours). Each step: raw events, yield at 500 fb^-1, efficiency relative to the previous step. Zero-count bounds
are Poisson 68 % (1.14 w) / 95 % (3 w). Output: work/final_ntuples/tta_xcheck.json (+ markdown table on stdout).
Usage: python3 -P scripts/analysis/tta_xcheck.py"""
import glob, json, numpy as np
P = "/eos/home-r/rjiang/vbs_zh_codex_starter"; NT = f"{P}/work/final_ntuples"
V = json.load(open(f"{NT}/verify.json")); MZ = 91.1876
REF = {"initial selection": 6.44e-2*500, "+ m_llgg > 100": 6.40e-2*500, "+ 70 < m_ll < 120": 1.76e-2*500, "+ mjj > 700, |deta| > 2.0 (full ref. cut flow)": 0.15}
REF_ERR_FINAL = 0.10
def load(s):
    A = {}; N = 0
    for c in sorted(glob.glob(f"{NT}/{s}__c[0-9][0-9][0-9].npz")):
        d = np.load(c); N += int(d["nev_total"])
        for k in d.files:
            if k != "nev_total": A.setdefault(k, []).append(d[k])
    return {k: np.concatenate(v) for k, v in A.items()}, N
OUT = {}
for s in ("T_tta", "T_tWa"):
    d, N = load(s); w = V[s]["sigma_used_fb"]*500/N
    for ovl in (True, False):
        for gpt in (20., 25.):
            with np.errstate(invalid="ignore"):
                keep = (d["npr"] <= 1) if ovl else np.ones(len(d["mll"]), bool)
                steps = [("initial selection", keep & np.isfinite(d["mll"]) & (d["ng"] >= 2) & (d["nj"] >= 2) & (d["g1pt"] > gpt) & (d["g2pt"] > gpt))]
                steps.append(("+ m_llgg > 100", steps[-1][1] & (d["mllgg"] > 100)))
                steps.append(("+ 70 < m_ll < 120", steps[-1][1] & (d["mll"] > 70) & (d["mll"] < 120)))
                steps.append(("+ mjj > 700, |deta| > 2.0 (full ref. cut flow)", steps[-1][1] & (d["mjj"] > 700) & (d["detajj"] > 2.0)))
                steps.append(("[ours] + pT1/mgg > 1/3, pT2/mgg > 1/4", steps[-1][1] & (d["g1pt"]/d["mgg"] > 1/3) & (d["g2pt"]/d["mgg"] > 1/4)))
            rows = []; prev = None
            for name, m in steps:
                n = int(len(np.unique(d["evt"][m]))); y = n*w
                rows.append(dict(step=name, raw=n, y500=y, eff_rel=(n/prev if prev else None), y500_ul68=1.14*w if n == 0 else None, y500_ul95=3*w if n == 0 else None, ref=REF.get(name)))
                prev = n if n else prev
            # factorised (pre-VBS level x VBS efficiency measured on the initial selection)
            n_init = rows[0]["raw"]; n_vbs_init = int(len(np.unique(d["evt"][steps[0][1] & (d["mjj"] > 700) & (d["detajj"] > 2.0)])))
            eps = n_vbs_init/n_init if n_init else 0.0
            fac = rows[2]["raw"]*w*eps
            OUT[f"{s}|ovl={ovl}|gpt={gpt:g}"] = dict(N=N, w500=w, rows=rows, eps_vbs_initial=eps, n_vbs_initial=n_vbs_init, factorised_y500=fac,
                                                     factorised_rel_err=float(np.hypot(1/np.sqrt(max(rows[2]["raw"], 1)), 1/np.sqrt(max(n_vbs_init, 1)))) if n_vbs_init else None)
json.dump(OUT, open(f"{NT}/tta_xcheck.json", "w"), indent=1)
for k, v in OUT.items():
    print(f"\n{k}: w500 = {v['w500']:.4f}, eps(VBS | initial) = {v['eps_vbs_initial']:.3f} ({v['n_vbs_initial']} raw), factorised final = {v['factorised_y500']:.4f}")
    for r in v["rows"]:
        print(f"  {r['step']:50s} raw={r['raw']:5d} y500={r['y500']:.4f} eff_rel={r['eff_rel'] if r['eff_rel'] is None else round(r['eff_rel'], 3)} ref={r['ref']}")
