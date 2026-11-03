#!/usr/bin/env python3
"""Morphing closure for EW HHjj (PARTON-LEVEL VALIDATION ONLY - not a result).
 (a) sigma closure: sigma(k_T) predicted from the 6 basis sigmas (MG5 gridpack/LHE init cross sections) vs direct MG5 sigma at the closure points.
 (b) distribution closure: m(HH), pT(H1), m(jj), |d eta(jj)| histograms from LHE of the 6 basis points morphed to each closure point vs the direct LHE.
Usage: morph_closure.py <lhe_dir> <out_json>   with <lhe_dir>/<sample>_s<seed>.lhe.gz named after config/sample_matrix_gen.yaml samples (J=2 seeds)."""
import sys, os, json, gzip, yaml, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from morph import coeffs, mono
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
m = yaml.safe_load(open(f"{H}/config/sample_matrix_gen.yaml"))["samples"]
S = {s["name"]: s for s in m if s["cls"] == "signal" and s["role"] in ("basis", "closure")}
def read_lhe(path):
    """returns sigma_pb (init xsecup), nev, dict of arrays"""
    obs = dict(mHH=[], ptH1=[], mjj=[], deta=[]); xs = None; n = 0
    with gzip.open(path, "rt") as f:
        inev = False; pl = []; hdr = False
        for line in f:
            if xs is None and line.startswith("<init>"):
                f.readline(); xs = float(f.readline().split()[0]); continue
            if line.startswith("<event>"): inev = True; hdr = True; pl = []; continue
            if line.startswith("</event>"):
                inev = False; n += 1
                hs = [p for p in pl if p[0] == 25 and p[1] == 1]; js = [p for p in pl if p[1] == 1 and p[0] != 25]
                if len(hs) == 2 and len(js) >= 2:
                    P = lambda ps: np.sum([[p[5 + 3], p[5], p[5 + 1], p[5 + 2]] for p in ps], axis=0)   # E,px,py,pz
                    def mass(ps): v = P(ps); return np.sqrt(max(v[0]**2 - v[1]**2 - v[2]**2 - v[3]**2, 0))
                    obs["mHH"].append(mass(hs)); obs["ptH1"].append(max(np.hypot(p[5], p[6]) for p in hs))
                    j = sorted(js, key=lambda p: -np.hypot(p[5], p[6]))[:2]; obs["mjj"].append(mass(j))
                    y = lambda p: 0.5 * np.log((p[8] + p[7]) / (p[8] - p[7])); obs["deta"].append(abs(y(j[0]) - y(j[1])))
                continue
            if inev:
                if hdr: hdr = False; continue
                t = line.split()
                if len(t) >= 11 and not line.startswith("#") and not line.startswith("<"): pl.append([int(t[0]), int(t[1]), 0, 0, 0] + [float(x) for x in t[6:10]] + [float(t[10])])
    return xs, n, {k: np.array(v) for k, v in obs.items()}
if __name__ == "__main__":
    d, outj = sys.argv[1], sys.argv[2]
    data = {}
    for nme, s in S.items():
        p = f"{d}/{nme}_s{s['seed_lhe_closure']}.lhe.gz"
        if not os.path.exists(p): print("MISSING", p); continue
        data[nme] = read_lhe(p)
    basis = [n for n, s in S.items() if s["role"] == "basis"]; clos = [n for n, s in S.items() if s["role"] == "closure"]
    B = [tuple(S[n]["coupling_kV_k2V_kl"]) for n in basis]; out = {"basis": basis, "closure": {}}
    bins = dict(mHH=np.linspace(250, 2250, 11), ptH1=np.linspace(0, 1000, 11), mjj=np.linspace(0, 3000, 11), deta=np.linspace(0, 10, 11))
    for c in clos:
        if c not in data or any(b not in data for b in basis): continue
        k = tuple(S[c]["coupling_kV_k2V_kl"]); cf = coeffs(B, k)
        sig_pred = float(sum(ci * data[b][0] for ci, b in zip(cf, basis)))
        # error on prediction: basis sigmas have MG5 integration errors only in the init block (not read here) -> report MC-stat error from event weights instead
        r = dict(k=k, coeffs=cf.tolist(), sigma_pred_pb=sig_pred, sigma_direct_pb=data[c][0], ratio=sig_pred / data[c][0], hist={})
        for v, bn in bins.items():
            hp = np.zeros(len(bn) - 1); vp = np.zeros_like(hp)
            for ci, b in zip(cf, basis):
                xs, n, ob = data[b]; h, _ = np.histogram(ob[v], bins=bn); w = ci * xs / n
                hp += w * h; vp += (w**2) * h
            xs, n, ob = data[c]; hd, _ = np.histogram(ob[v], bins=bn); wd = xs / n
            diff = hp - wd * hd; err = np.sqrt(vp + wd**2 * hd); ok = err > 0
            chi2 = float(np.sum((diff[ok] / err[ok])**2)); r["hist"][v] = dict(bins=bn.tolist(), morph=hp.tolist(), direct=(wd * hd).tolist(), err=err.tolist(), chi2=chi2, ndf=int(ok.sum()))
        out["closure"][c] = r
    json.dump(out, open(outj, "w"), indent=1); print(json.dumps({c: {kk: v[kk] for kk in ("sigma_pred_pb", "sigma_direct_pb", "ratio")} for c, v in out["closure"].items()}, indent=1))
