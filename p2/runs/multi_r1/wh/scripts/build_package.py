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
        ROLE = {"S_EW_WHjj": "signal", "S_EW_WHjj_taunu": "signal-like feed-down (W->tau nu->l nu nu), in b", "H_QCD_WHjj_fixed": "cross-check only (not in s, b)",
                "Q_aajj": "cross-check after the D29 trigger (non-prompt lepton, gamma gamma + 2 jets); the row after the trigger is Q_aajjj",
                "Q_aajjj": "non-prompt lepton row after the D29 trigger of Q_aajj (cluster 897588): ME with exactly three outgoing partons pT>20 (gamma gamma + 3 jets), no 2-jet+PS component, no merging",
                "F_QCD_Wajjj_nomjj": "background: one prompt photon + converted jet; ME with exactly three outgoing partons pT>20 (W gamma + 3 jets), no 2-jet+PS component, no merging (the 2-jet row F_QCD_Wajj_nomjj was withdrawn)"}
        def neutral(x): return str(x).replace("(NOMINAL, D8; G2 item 2)", "(primary sample)").replace("CROSS-CHECK of the nomjj nominal; twin C", "CROSS-CHECK of the nomjj primary sample; twin C").replace("the nomjj sample is nominal", "the nomjj sample is the primary one").replace("nominal (no generator mjj cut)", "primary sample, no generator mjj cut").replace("NOMINAL", "primary")
        rows = []
        for s in samples:
            js = [json.load(open(f)) for f in meta_json(s)]
            if not js: continue
            r = m[s]; ng = sum(j["n_lhe"] for j in js); nd = sum(j["n_delphes"] for j in js); seeds = sorted(j["mg_seed"] for j in js); sm = sums.get(s, {})
            role = ROLE.get(s) or ("coupling-study variant of the signal (HC_NLO_X0_kVV), NOT in s" if s.startswith("K_EW_WHjj") else "background: " + r["role"].split(" -- ")[0].replace("NOMINAL (no generator mjj cut)", "primary sample, no generator mjj cut").replace("NOMINAL", "primary sample"))
            ratio = sm.get("sumw_pb", float("nan"))/(ng*r["sigma_fb"]/1e3)
            rows.append([s, r["process"], role, "%.6g" % (r["sigma_fb"]/1e3), r["sigma_source"].split(" (")[0], "*".join(r["br_factors_external"]) + " = %.6g" % r["k_external"], "%.6g" % r["k_external"], ng, nd,
                         "%.8g" % sm.get("sumw_pb", float("nan")), sm.get("n_neg", ""), "%.4f" % ratio, "sigma_x_BR[fb] = 1e3*k*sum(Event.Weight[pb])/N_generated (cross-section times BR in fb; events at luminosity L = L[fb^-1] x this)", r["gen_cuts"], "%d-%d" % (seeds[0], seeds[-1]), len(js),
                         f"{s}/{s}_s*.root (+ _gen.root)", "SHA256SUMS", ""])
        rows.append(["F_QCD_Wajj_nomjj", "p p > w+- a j j (2-jet LO, PS third jet)", "WITHDRAWN as production row (D29/D30 decision of 2026-11-06); test job + 40k twins are cross-checks outside this package; whether it is restored depends on the open question H1", "5.683", "gridpack init sigma", "WF = 0.96008", "0.96008", 0, 0, "", "", "", "", "", "", 0, "", "", "not produced"])
        rows.append(["H_ggF_jj", "p p > h j j [noborn=QCD] (loop_sm, LO loop-induced)", "non-prompt lepton row (D31); PENDING: gridpack 893012 still running (fallback D-WH-14), later row", "", "pending", "BGG = 0.00227", "0.00227", 0, 0, "", "", "", "", "", "", 0, "", "", "pending"])
        # frozen ZH rows: read-only, not copied
        ZHNOTE = {"ZH_Zaajj_EW_lostlep": "C(generator mmjj>400 -> none) = 0.958 +- 0.061 from the W EW twin proxy", "ZH_Zaajj_QCD_nomjj_lostlep": "nominal (no generator mjj cut), frozen twin", "ZH_Zajj_eFake": "Z(ll) gamma jj with e->gamma, QCD+EW vbs samples (mmjj>400); C = 1.866 +- 0.095 (QCD part, 200k-event nomjj twin; the nomjj frozen sample has 200 000 of the ~2.45e6 events required)",
                  "ZH_EW_ZHjj_lostlep": "ZHjj EW with Z->ll, one lepton lost", "ZH_QCD_ZHjj_lostlep": "ZHjj QCD (2,2) with Z->ll, one lepton lost", "ZH_Zaajj_QCD_lostlep": "mmjj>400 cross-check of the nomjj row (C = 1.955 +- 0.131)"}
        zs = json.load(open(f"{WH}/work/zh_frozen_sums.json"))   # READ-ONLY pass over the frozen ZH files (scripts/zh_frozen_sums.py)
        ZMAP = {"ZH_Zaajj_QCD_nomjj_lostlep": ["final/B_QCD_zaajj_nomjj"], "ZH_Zaajj_EW_lostlep": ["final/B_EW_zaajj_vbs_is1h", "final/B_EW_zaajj_vbs_is2", "final/B_EW_zaajj_vbs_is3"], "ZH_Zajj_eFake": ["final/F_QCD_llajj_vbs", "final/F_EW_llajj_vbs"],
                "ZH_EW_ZHjj_lostlep": ["v1/ew_zhjj_zll"], "ZH_QCD_ZHjj_lostlep": ["v1/qcd_zhjj_zll"], "ZH_Zaajj_QCD_lostlep": ["final/B_QCD_zaajj_vbs"]}
        ZSIG = {"ZH_Zaajj_QCD_nomjj_lostlep": (0.2739, "gridpack-initialisation sigma 2.739e-4 pb: production/gridpacks/B_QCD_zaajj_nomjj_status.txt:2 (the auxiliary row of reports/FINAL_report.md:80 lists 0.268 fb, a different value; the chunk mean of the delivered files is 2.728e-4 pb)"),
                "ZH_Zaajj_EW_lostlep": (0.03921, "reports/FINAL_report.md:49-51 (sum of the beam-1 splits is1+is2+is3 = 0.01666 + 0.01575 + 0.0068 fb)"),
                "ZH_Zajj_eFake": (80.51, "reports/FINAL_report.md:53-54 (F_QCD_Zajj 69.46 fb + F_EW_Zajj 11.05 fb)"),
                "ZH_EW_ZHjj_lostlep": (1.295, "reports/FINAL_report.md:42 (S_EW_ZHjj 1.295 fb)"),
                "ZH_QCD_ZHjj_lostlep": (10.21, "reports/FINAL_report.md:43 (H_QCD_ZHjj 10.21 fb)"),
                "ZH_Zaajj_QCD_lostlep": (0.0356, "reports/FINAL_report.md:48 (B_QCD_Zaajj_vbs 0.0356 fb)")}   # file:line in the frozen ZH tree /eos/home-r/rjiang/vbs_zh_codex_starter
        ZCONV = "SAME convention as the WH samples (checked on the files: |Event.Weight[0]| = chunk sigma in pb, signed): sigma_x_BR[fb] = 1e3*k*sum(Event.Weight[pb])/N_generated; events at L = L[fb^-1] x this; the ZH files are read-only and unchanged"
        for sid in ("ZH_Zaajj_QCD_nomjj_lostlep", "ZH_Zaajj_EW_lostlep", "ZH_Zajj_eFake", "ZH_EW_ZHjj_lostlep", "ZH_QCD_ZHjj_lostlep", "ZH_Zaajj_QCD_lostlep"):
            r = m[sid]; role = "FROZEN ZH-study sample, READ-ONLY, not copied: " + ("cross-check only (not in b)" if sid == "ZH_Zaajj_QCD_lostlep" else "background (lost lepton / e->gamma)")
            D = [zs[d] for d in ZMAP[sid]]
            r = dict(r); r["sigma_fb"], zsrc = ZSIG[sid]; ng = sum(x["N_generated"] for x in D); nd = sum(x["N_delphes"] for x in D); sw = sum(x["sumw_pb"] for x in D); nn = sum(x["n_neg"] for x in D)
            per = "; ".join(f"{d}: {zs[d]['files']} files, N_gen {zs[d]['N_generated']}, sum w {zs[d]['sumw_pb']:.5g} pb, mean |w| {zs[d]['mean_abs_w_pb']:.5g} pb, {zs[d]['n_neg']} negative" for d in ZMAP[sid])
            rows.append([sid, neutral(r.get("process", r["role"])), role, "%.6g" % (r["sigma_fb"]/1e3), zsrc, "*".join(r["br_factors_external"]) + " = %.6g" % r["k_external"], "%.6g" % r["k_external"], ng, nd, "%.8g" % sw, nn, "", ZCONV, r["gen_cuts"], "", sum(x["files"] for x in D), r["path"].replace("frozen ZH (zh-final-v1.1), ", ""), "frozen ZH export: p2/lib/SHA256SUMS (production files not hashed here)", neutral(ZHNOTE.get(sid, "")) + " | per directory: " + per])
        with open(f"{PR}/SAMPLES.csv", "w", newline="") as f:
            w = csv.writer(f); w.writerow(["sample", "process", "role", "sigma_pb_pre_decay", "sigma_source", "BR_k_factors_applied_once", "k", "N_generated_LHE", "N_Delphes", "sum_weights_pb_signed", "N_negative_weight_events", "sumw_over_Ngen_sigma", "normalisation_formula", "generator_cuts", "mg_seed_range", "n_files", "files_glob", "sha256_list", "notes"]); w.writerows(rows)
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
