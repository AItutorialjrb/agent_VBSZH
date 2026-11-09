#!/usr/bin/env python3
"""Library for the background model (05a) and later blocks: load skims, regions, weights, yields with MC uncertainty.
Normalisation (SAMPLES.csv): events at L = L[fb^-1] * 1e3 * k * sum(w_pb * f) / N_generated.  For the frozen ZH rows that combine several directories (different sigma),
N_generated and the sum of weights are taken PER DIRECTORY (N from the n_events of the skim json files of that directory; all files of the directory must be skimmed, checked by the driver)."""
import csv, glob, json, os, re, numpy as np
WH = "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh"; PR = "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/production/wh"
SK = f"{WH}/work/bgmodel/skim"; LUMI = 500.0
FC = {"nom": 0, "up": 1, "dn": 2, "all": 3, "r03": 4, "r07": 5}
SAMP = {r["sample"]: r for r in csv.DictReader(open(f"{PR}/SAMPLES.csv"))}
def dkey(path):
    """directory label of a skimmed file: skim metadata stores the (local) file name only, so the directory is identified by the file-name prefix (name without _s<seed>.root); review wh_05a item 1"""
    return re.sub(r"_s\d+\.root$", "", os.path.basename(path))
# pre-declared generator-cut factors C (04 sec. 15(7), SAMPLES.csv notes): (central, low, high) multiplicative on rows of the directory; applied in VBS/PEAK only (measured at the mjj>500,|deta|>2.5 proxy)
CFAC = {"F_QCD_llajj_vbs": (1.866, 1.0, 2.732),      # Z gamma jj QCD, nomjj/vbs ratio 1.866, syst = full difference 0.866 (87 %): range [1, 2.732]
        "F_EW_llajj_vbs": (1.025, 1.0, 1.05),      # EW part: C >= 1 from the twin loss fraction (W EW proxy 1.025); range [1, 1+2*0.025] (v2.1, review N2; v2 had C=1)
        "B_EW_zaajj_vbs_is1h": (1.016, 1.0, 1.032), "B_EW_zaajj_vbs_is2": (1.016, 1.0, 1.032), "B_EW_zaajj_vbs_is3": (1.016, 1.0, 1.032)}   # twin loss 1.56 % -> 1.016 (v2.1; v2 used 0.958 < 1, unphysical for nomjj containing vbs)
def load(sample):
    """-> dict of concatenated arrays + per-row norm array 'norm' (= 1e3*k/N_gen_of_its_directory, fb per pb), and cutflow sums."""
    fs = sorted(glob.glob(f"{SK}/skim_{sample}__*.npz")); k = float(SAMP[sample]["k"]); D = {}; nd = {}; metas = []
    for f in fs:
        m = json.load(open(f[:-4] + ".json")); metas.append(m); key = dkey(m["file"]); nd[key] = nd.get(key, 0) + m["cutflow"]["n_events"]
    if not fs: return None
    parts = [np.load(f) for f in fs]
    for key in parts[0].files: D[key] = np.concatenate([p[key] for p in parts])
    wsrc = SAMP[sample]["files_glob"].startswith("/")   # frozen ZH rows: per-directory N
    Ngen = float(SAMP[sample]["N_generated_LHE"])
    norm = []; cf = []; dn = []
    for p, m in zip(parts, metas):
        n = len(p["w"]); norm.append(np.full(n, 1e3*k/(nd[dkey(m["file"])] if wsrc else Ngen)))
        dn.append(np.full(n, dkey(m["file"])))
        cf.append(np.tile(np.array(CFAC.get(dkey(m["file"]), (1.0, 1.0, 1.0)))[None, :], (n, 1)))
    D["norm"] = np.concatenate(norm); D["cfac"] = np.concatenate(cf); D["dirname"] = np.concatenate(dn); D["n_files"] = len(fs); D["n_events_skimmed"] = sum(m["cutflow"]["n_events"] for m in metas)
    sw = {}
    for m in metas: sw[dkey(m["file"])] = sw.get(dkey(m["file"]), 0.0) + m["cutflow"]["sum_w"]
    D["sumw_over_N_pb"] = float(sum(sw[kk]/(nd[kk] if wsrc else Ngen) for kk in sw)); D["N_by_dir"] = nd
    D["cutflow"] = {kk: (np.sum([m["cutflow"][kk] for m in metas], axis=0).tolist() if isinstance(metas[0]["cutflow"][kk], list) else sum(m["cutflow"][kk] for m in metas)) for kk in metas[0]["cutflow"] if kk != "rows_by_kind"}
    D["rows_by_kind"] = {kk: sum(m["cutflow"]["rows_by_kind"][kk] for m in metas) for kk in metas[0]["cutflow"]["rows_by_kind"]}
    return D
def derived(D):
    j = D["jets"]; pt, eta, phi, m, bt = (j[:, :, i] for i in range(5)); E = np.sqrt((pt*np.cosh(eta))**2+m**2); px, py, pz = pt*np.cos(phi), pt*np.sin(phi), pt*np.sinh(eta)
    s = lambda a: a[:, 0]+a[:, 1]; mjj = np.sqrt(np.maximum(s(E)**2-s(px)**2-s(py)**2-s(pz)**2, 0)); deta = np.abs(eta[:, 0]-eta[:, 1])
    ph = D["ph"]; q, e, f = ph[:, :, 0], ph[:, :, 1], ph[:, :, 2]; Eg = q*np.cosh(e); gx, gy, gz = q*np.cos(f), q*np.sin(f), q*np.sinh(e)
    mgg = np.sqrt(np.maximum(s(Eg)**2-s(gx)**2-s(gy)**2-s(gz)**2, 0))
    nb = ((bt > 0) & (pt > 30) & (np.abs(eta) < 2.5)).sum(1); crack = ((np.abs(e) > 1.4442) & (np.abs(e) < 1.566)).any(1)
    return dict(mjj=mjj, deta=deta, mgg=mgg, nb=nb, crack=crack)
def regions(D, iso=True, ptg=25.0):
    d = derived(D); lep = D["lep"]; ph = D["ph"]
    base = (lep[:, 0] > 25) & ((lep[:, 5] == 1) | (D["kind"] == 5)) & (D["met"][:, 0] > 30) & (ph[:, :, 0] > ptg).all(1) & ~d["crack"] & (d["nb"] == 0)
    if iso: base &= lep[:, 4] < 0.15
    vbs = base & (d["mjj"] > 500) & (d["deta"] > 2.5) & (d["mgg"] > 100) & (d["mgg"] < 180)
    return {"PRE": base, "VBS": vbs, "PEAK": vbs & (d["mgg"] > 120) & (d["mgg"] < 130)}, d
def ysum(w, mask, unit=None):
    """-> dict(Y, stat, nraw, neff, wmax, UL95 (if nraw==0: 2.996*unit))"""
    x = w[mask]; n = int(mask.sum())
    r = dict(Y=float(x.sum()), stat=float(np.sqrt((x**2).sum())), nraw=n, neff=float(x.sum()**2/(x**2).sum()) if n and (x**2).sum() > 0 else 0.0, wmax=float(np.abs(x).max()) if n else 0.0)
    if n == 0 and unit is not None: r["UL95"] = float(2.996*unit)
    return r
