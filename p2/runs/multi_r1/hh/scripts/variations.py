#!/usr/bin/env python3
"""Pre-declared variations (config/g2_predeclared.yaml) exercised on the pilot samples at Delphes level (illustrative, NOT results):
 trigger lead-fat-jet pT >= 450 (baseline) / 500 / 550 ; m_SD scale x0.95 / 1.05 on the window [90,150] ; m(HH)-proxy clip < 1500 and < 1000 GeV ; multijet normalisation x0.5 / x2 (applied to Q_4j, Q_bbjj, Q_4b).
Per sample: expected SR events at 500 fb-1 (nominal tagging) from the class-aware smoothed estimator of neff_project (window probability per class, recomputed for the varied window), for signal points the hard raw count too.
Usage: variations.py <matrix.yaml> <scenarios.yaml> <out.json> <prod_root> sample ..."""
import sys, json, yaml, numpy as np, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hh_reco as R
my, sy, outj, root = sys.argv[1:5]; names = sys.argv[5:]
M = {s["name"]: s for s in yaml.safe_load(open(my))["samples"]}; SCN = yaml.safe_load(open(sy))["tagging"]["nominal"]
VAR = {"baseline": dict(), "trigger500": dict(lead=500.0), "trigger550": dict(lead=550.0), "mSD_x0.95": dict(scale=0.95), "mSD_x1.05": dict(scale=1.05), "mHH<1500": dict(clip=1500.0), "mHH<1000": dict(clip=1000.0)}
def est(d, sig, lead=450.0, scale=1.0, clip=None):
    two, ld, V = R.stages(d, lead=lead)
    if clip is not None: V = V & (d["mHH"] < clip)
    c, m = d["fj_cls_all"], d["fj_msd_all"] * scale; inw = (m > 90) & (m < 150)
    pw = np.array([inw[c == k].mean() if (c == k).sum() >= 30 else (inw[c >= 0].mean()) for k in range(6)])
    c1 = np.where(d["cls1"] < 0, 0, d["cls1"]).astype(int); c2 = np.where(d["cls2"] < 0, 0, d["cls2"]).astype(int)
    w = R.tag_weight(d, SCN); p = pw[c1] * pw[c2]; ng = d["n_gen"]
    hard = V & R.window(d, scale=scale)
    pwv = (p * w)[V]; nes = float(pwv.sum() ** 2 / (pwv ** 2).sum()) if (pwv ** 2).sum() > 0 else 0.0
    return dict(smoothed_500fb=float(sig * 500.0 * (p * w)[V].sum() / ng), neff_smoothed_pilot=nes, N_pilot=int(ng), hard_raw=int(hard.sum()), hard_500fb=float(sig * 500.0 * (w * hard).sum() / ng), n_V=int(V.sum()))
out = {}
for n in names:
    d = R.load_named(n, root); sig = M[n]["sigma_x_BR_fb"]; out[n] = {v: est(d, sig, **kw) for v, kw in VAR.items()}
    b = out[n]["baseline"]["smoothed_500fb"]
    print(f"{n:28s} base={b:.4g} " + " ".join(f"{v}:{(out[n][v]['smoothed_500fb']/b if b>0 else float('nan')):.2f}" for v in list(VAR)[1:]))
json.dump(out, open(outj, "w"), indent=1)
