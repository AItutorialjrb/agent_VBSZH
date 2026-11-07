#!/usr/bin/env python3
"""Builds the production package metadata in p2/production/wh/: SAMPLES.csv, FORMAT.md, SHA256SUMS (brief v2 sec. 2.6 / A2: physics conventions and data only, no analysis recipe, no code).
Run inside the pinned stack. Stages: 'sums' (per-sample signed sum of Event.Weight from the ROOT files -> work/package_sums.json, pool), 'write' (SAMPLES.csv, FORMAT.md), 'sha' (SHA256SUMS over the package ROOT files, pool)."""
import sys, os, json, glob, re, csv, hashlib, yaml, numpy as np
from multiprocessing import Pool
WH = "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh"; PR = "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/production/wh"; META = f"{WH}/work/prod_meta"
def meta_json(s): return sorted(glob.glob(f"{META}/{s}/*.json")) or sorted(glob.glob(f"{PR}/{s}/*.json"))
def rootfiles(s): return sorted(f for f in glob.glob(f"{PR}/{s}/*.root"))
def sumw(f):
    import uproot
    w = np.array([x[0] for x in uproot.open(f)["Delphes"]["Event/Event.Weight"].array(library="np")]); return f, float(w.sum()), int((w < 0).sum()), len(w)
def sha(f):
    h = hashlib.sha256()
    with open(f, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 22), b""): h.update(b)
    return h.hexdigest(), os.path.relpath(f, PR)
if __name__ == "__main__":
    st = sys.argv[1]; samples = sorted(d for d in os.listdir(PR) if os.path.isdir(f"{PR}/{d}"))
    if st == "sums":
        fs = [f for s in samples for f in rootfiles(s) if not f.endswith("_gen.root")]
        with Pool(8) as p: R = p.map(sumw, fs, chunksize=4)
        out = {}
        for f, w, n, N in R:
            s = os.path.basename(os.path.dirname(f)); o = out.setdefault(s, dict(sumw_pb=0.0, n_neg=0, n=0)); o["sumw_pb"] += w; o["n_neg"] += n; o["n"] += N
        json.dump(out, open(f"{WH}/work/package_sums.json", "w"), indent=1); print(len(fs), "files")
    if st == "sha":
        fs = [f for s in samples for f in rootfiles(s)]
        with Pool(8) as p: R = p.map(sha, fs, chunksize=4)
        open(f"{PR}/SHA256SUMS", "w").write("".join(f"{h}  {r}\n" for h, r in sorted(R, key=lambda x: x[1]))); print(len(R), "sha256 lines")
    if st == "write":
        m = {r["id"]: r for r in yaml.safe_load(open(f"{WH}/config/sample_matrix.yaml"))["samples"]}; sums = json.load(open(f"{WH}/work/package_sums.json"))
        ROLE = {"S_EW_WHjj": "signal", "S_EW_WHjj_taunu": "signal-like feed-down (W->tau nu->l nu nu), in b", "H_QCD_WHjj_fixed": "cross-check only (not in s, b)"}
        rows = []
        for s in samples:
            js = [json.load(open(f)) for f in meta_json(s)]
            if not js: continue
            r = m[s]; ng = sum(j["n_lhe"] for j in js); nd = sum(j["n_delphes"] for j in js); seeds = sorted(j["mg_seed"] for j in js); sm = sums.get(s, {})
            role = ROLE.get(s) or ("coupling-study variant of the signal (HC_NLO_X0_kVV), NOT in s" if s.startswith("K_EW_WHjj") else
                                   ("background (replaces the withdrawn 2-jet row F_QCD_Wajj_nomjj, D29): valid only with >= 3 reco jets incl. the converted jet" if s == "F_QCD_Wajjj_nomjj" else "background: " + r["role"].split(" -- ")[0]))
            rows.append([s, r["process"], role, "%.6g" % (r["sigma_fb"]/1e3), r["sigma_source"].split(" (")[0], "*".join(r["br_factors_external"]) + " = %.6g" % r["k_external"], "%.6g" % r["k_external"], ng, nd,
                         "%.8g" % sm.get("sumw_pb", float("nan")), sm.get("n_neg", ""), "signed Event.Weight (pb), |w| = sigma_pb; yield[fb] = 1e3*k*sum(w)/N_generated", r["gen_cuts"], "%d-%d" % (seeds[0], seeds[-1]), len(js),
                         f"{s}/{s}_s*.root (+ _gen.root)", "SHA256SUMS"])
        rows.append(["F_QCD_Wajj_nomjj", "p p > w+- a j j (2-jet LO, PS third jet)", "WITHDRAWN as production row (D29 supersedes D30); test job + 40k twins are a cross-check outside s and b, not in this package", "5.683", "gridpack init sigma", "WF = 0.96008", "0.96008", 0, 0, "", "", "", "", "", 0, "", ""])
        with open(f"{PR}/SAMPLES.csv", "w", newline="") as f:
            w = csv.writer(f); w.writerow(["sample", "process", "role", "sigma_pb_pre_decay", "sigma_source", "BR_k_factors_applied_once", "k", "N_generated_LHE", "N_Delphes", "sum_weights_pb_signed", "N_negative_weight_events", "weight_convention", "generator_cuts", "mg_seed_range", "n_files", "files_glob", "sha256_list"]); w.writerows(rows)
        print(len(rows), "rows")
    if st == "format":
        rj = json.load(open(f"{WH}/work/postprod/rate_all.json")); eg = json.load(open(f"{WH}/work/postprod/egamma_rate.json")); PT = rj["pt_edges"]
        def pct(x): return "%.4f" % (100*x)
        def tbl(cls):
            rows = ["| jet pT [GeV] | barrel rate [%] | barrel stat. err [%] | endcap rate [%] | endcap stat. err [%] | barrel N_match / N_jets | endcap N_match / N_jets |", "|---|---|---|---|---|---|---|"]
            for j in range(len(PT)-1):
                rows.append(f"| {PT[j]}-{PT[j+1]} | {pct(rj['rate_'+cls][0][j])} | {pct(rj['err_stat_'+cls][0][j])} | {pct(rj['rate_'+cls][1][j])} | {pct(rj['err_stat_'+cls][1][j])} | {int(rj['num_fake_'+cls][0][j])} / {int(rj['den_'+cls][0][j])} | {int(rj['num_fake_'+cls][1][j])} / {int(rj['den_'+cls][1][j])} |")
            return "\n".join(rows)
        xm = lambda h: [round(float((np.array(hh)*(np.array(rj['x_edges'][1:])+np.array(rj['x_edges'][:-1]))/2).sum()/max(np.array(hh).sum(), 1)), 2) for hh in h]
        egt = ["| gen lepton pT [GeV] | e: barrel | e: endcap | mu: barrel | mu: endcap |", "|---|---|---|---|---|"]
        for j in range(len(eg["pt_edges"])-1):
            egt.append(f"| {eg['pt_edges'][j]}-{eg['pt_edges'][j+1]} | " + " | ".join("%.2f %%" % (100*eg[fl]["rate_lepton_lost_photon"][ie][j]) for fl in ("e", "mu") for ie in (0, 1)).replace("%  |", "%|") + " |")
        egt = [egt[0], egt[1]] + [r for r in egt[2:]]
        pe = json.load(open(f"{WH}/work/postprod/photon_rate_per_event.json")); pr_ = ["| photon pT [GeV] | W+jets barrel | W+jets endcap | tt̄ barrel | tt̄ endcap |", "|---|---|---|---|---|"]
        for j in range(len(pe["pt_edges"])-1): pr_.append(f"| {pe['pt_edges'][j]}-{pe['pt_edges'][j+1]} | " + " | ".join("%.2e ± %.1e" % (pe[c]["per_event"][ie][j], pe[c]["err"][ie][j]) for c in ("W", "TT") for ie in (0, 1)) + " |")
        fm = open(f"{WH}/work/format_template.md").read()
        fm = fm.replace("@@RATE_W@@", tbl("W")).replace("@@RATE_TT@@", tbl("TT")).replace("@@XMEAN_W@@", str(xm(rj["x_hist_per_ptbin_W"]))).replace("@@XMEAN_TT@@", str(xm(rj["x_hist_per_ptbin_TT"]))).replace("@@EGAMMA@@", "\n".join(egt)).replace("@@PHOTON_PE@@", "\n".join(pr_)).replace("@@PE_NW@@", str(pe["W"]["n_events"])).replace("@@PE_NT@@", str(pe["TT"]["n_events"])).replace("@@NFILES@@", f"{rj['n_files']['W']} W+4j files (every 6th of the delivered files) and {rj['n_files']['TT']} ttbar+jj files")
        open(f"{PR}/FORMAT.md", "w").write(fm); print("FORMAT.md written")
