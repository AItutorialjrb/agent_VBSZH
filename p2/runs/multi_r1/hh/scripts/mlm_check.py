#!/usr/bin/env python3
"""MLM matching-scale variation check for tt+0,1,2j (D-HH-3).  Compares xqcut = 20 / 30 (nominal) / 45 GeV (PY8 qCut = 1.3 xqcut) at Delphes level:
  sigma_matched = sigma_MG5(xqcut) x (accepted/processed LHE events);  AK5-jet multiplicity (pT>30, |eta|<4.7), pT of the 1st..4th AK5 jet, >=2 fat jet / VBS-pair stage fractions, rates in fb.
The merged sample should be insensitive to xqcut: ratio to the nominal within statistics (chi2/ndf of the bin-wise ratio).  NOT a DJR plot (Delphes slim files carry no hadron-level particles): this is a matching-scale
VARIATION check on physical observables; its limits are stated in the report.  Usage: mlm_check.py <matrix.yaml> <out.json> <prod_root> <nominal> <var1> <var2> ...  ; optional reference sample (PS-only tt) last after '--'"""
import sys, json, yaml, numpy as np, os, glob, uproot, awkward as ak
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hh_reco as R
my, outj, root, nom = sys.argv[1:5]; rest = sys.argv[5:]; ref = None
if "--" in rest: ref = rest[rest.index("--") + 1]; rest = rest[:rest.index("--")]
M = {s["name"]: s for s in yaml.safe_load(open(my))["samples"]}
def jets(name):
    out = []
    for f in R.sample_files(f"{root}/{name}"):
        t = uproot.open(f)["Delphes"]; pt = t["Jet/Jet.PT"].array(); eta = t["Jet/Jet.Eta"].array()
        pt = pt[(pt > 30) & (abs(eta) < 4.7)]; pt = pt[ak.argsort(pt, ascending=False)]; out.append(pt)
    return ak.concatenate(out)
def summ(name):
    d = R.load(R.sample_files(f"{root}/{name}")); pt = jets(name); sig = M[name]["sigma_x_BR_fb"]; ng = d["n_gen"]; ne = d["n_entries"]; two, lead, v = R.stages(d)
    nj = ak.to_numpy(ak.num(pt)); r = dict(name=name, sigma_MG5_fb=sig, n_lhe=ng, n_accepted=ne, match_eff=ne / ng, sigma_matched_fb=sig * ne / ng, scale=sig / ng,
                                          nj_hist=np.bincount(np.minimum(nj, 8), minlength=9).tolist(), stages=dict(two=int(two.sum()), lead=int(lead.sum()), vbs=int(v.sum())))
    for i in range(4):
        x = ak.to_numpy(ak.fill_none(ak.pad_none(pt, 4, axis=1)[:, i], 0.0)); r[f"pt{i+1}_hist"] = np.histogram(x[x > 0], [30, 50, 80, 120, 200, 300, 500, 1e5])[0].tolist()
    return r
res = {n: summ(n) for n in [nom] + rest + ([ref] if ref else [])}
out = dict(samples=res, ratios={})
a = res[nom]
for n in rest:
    b = res[n]; row = {"sigma_matched_ratio": b["sigma_matched_fb"] / a["sigma_matched_fb"]}
    for key in ["nj_hist", "pt1_hist", "pt2_hist", "pt3_hist", "pt4_hist"]:
        x, y = np.array(a[key], float) * a["scale"], np.array(b[key], float) * b["scale"]; ex, ey = np.sqrt(np.maximum(a[key], 1)) * a["scale"], np.sqrt(np.maximum(b[key], 1)) * b["scale"]
        m = (np.array(a[key]) >= 5) & (np.array(b[key]) >= 5); chi = float((((x - y) ** 2) / (ex ** 2 + ey ** 2))[m].sum()); row[key] = dict(chi2=chi, ndf=int(m.sum()), ratio=[(float(yy / xx) if xx > 0 else None) for xx, yy in zip(x, y)])
    for st in ("two", "lead", "vbs"):
        ra = a["stages"][st] * a["scale"]; rb = b["stages"][st] * b["scale"]; ea = np.sqrt(max(a["stages"][st], 1)) * a["scale"]; eb = np.sqrt(max(b["stages"][st], 1)) * b["scale"]
        row[f"stage_{st}"] = dict(nominal_fb=ra, variant_fb=rb, ratio=rb / ra if ra > 0 else None, ratio_err=(rb / ra) * np.hypot(ea / ra, eb / rb) if ra > 0 and rb > 0 else None)
    out["ratios"][n] = row
json.dump(out, open(outj, "w"), indent=1, default=float)
for n in [nom] + rest + ([ref] if ref else []): r = res[n]; print(n, "N_lhe=%d acc=%d eff=%.3f sigma_matched=%.4g fb stages=%s" % (r["n_lhe"], r["n_accepted"], r["match_eff"], r["sigma_matched_fb"], r["stages"]))
for n, row in out["ratios"].items(): print(n, "sigma ratio %.3f" % row["sigma_matched_ratio"], {k: "%.1f/%d" % (v["chi2"], v["ndf"]) for k, v in row.items() if isinstance(v, dict) and "chi2" in v}, {k: (round(v["ratio"], 2) if v["ratio"] else None) for k, v in row.items() if k.startswith("stage_")})
