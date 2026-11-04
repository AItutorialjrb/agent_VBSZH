#!/usr/bin/env python3
"""Twin ratio at the WH reco-SR baseline (scripts/srsel.py): C = [sigma_nom*n_sel_nom/N_nom] / [sigma_vbs*n_sel_vbs/N_vbs] = factor by which the mmjj>400 sample under-estimates the no-cut yield
(ZH correction method, repo reports/FINAL_report.md sec. on C). Sigmas: LHE init cross sections in the job json (first/only process line; single-process cards). Binomial errors on selected fractions.
Usage: ratio_C.py <out.json> <ng> <nomjj_dir> <vbs_dir> <max_files_each> [nom_glob vbs_glob]   (directories contain <tag>.root + <tag>.json; read-only)"""
import sys, os, glob, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from srsel import select
out, ng, dn, dv, mx = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4], int(sys.argv[5])
def run(d):
    fs = sorted(f for f in glob.glob(d + "/*.root") if not f.endswith(("_gen.root", "_full.root")))[:mx]; n = k = 0; sig = []
    for f in fs:
        j = json.load(open(f[:-5] + ".json")); sig.append(float(j["lhe_init_xsec_pb_err_pb_max_lprup"].split()[0])*1e3); s = select(f, ng); n += len(s); k += int(s.sum())
    return dict(files=len(fs), N=n, n_sel=k, sigma_fb=sum(sig)/len(sig))
a, b = run(dn), run(dv); res = {"nomjj": a, "vbs": b, "ng": ng}
ya, yb = a["sigma_fb"]*a["n_sel"]/a["N"], b["sigma_fb"]*b["n_sel"]/b["N"]
if a["n_sel"] and b["n_sel"]:
    res["C"] = ya/yb; res["C_rel_err"] = math.sqrt(1/a["n_sel"]+1/b["n_sel"]); res["loss_frac_of_nomjj_yield"] = 1-yb/ya
json.dump(res, open(out, "w"), indent=1); print(json.dumps(res))
