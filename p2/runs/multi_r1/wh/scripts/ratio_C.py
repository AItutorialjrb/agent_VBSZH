#!/usr/bin/env python3
"""Twin ratio at the WH reco-SR baseline (scripts/srsel.py): C = [sigma_nom*n_sel_nom/N_nom] / [sigma_vbs*n_sel_vbs/N_vbs] = factor by which the mmjj>400 sample under-estimates the no-cut yield
(ZH correction method, repo reports/FINAL_report.md sec. on C). Sigmas: LHE init cross sections in the job json (first/only process line; single-process cards). Binomial errors on selected fractions.
Usage: ratio_C.py <out.json> <ng> <nomjj_dir> <vbs_dir> <max_files_each> [nom_glob vbs_glob]   (directories contain <tag>.root + <tag>.json; read-only)"""
import sys, os, glob, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from srsel import select
out, ng, dn, dv, mx = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4], int(sys.argv[5])
import gzip
SINGLE = os.environ.get("SINGLE_PROCESS") == "1"   # frozen ZH samples have no LHE here: allowed ONLY for single-process cards (checked: one 'generate', no 'add process'), where the first-process sigma is the total
def sigma_total_fb(f):
    """TOTAL generator sigma [fb] = sum of XSECUP over all NPRUP processes of the LHE <init> block (VERIFY #12 item 6: the json field holds only the FIRST process)."""
    lhe = f[:-5] + ".lhe.gz"
    if os.path.exists(lhe):
        with gzip.open(lhe, "rt", errors="replace") as fh:
            for l in fh:
                if l.strip() == "<init>": break
            nprup = int(next(fh).split()[9]); return sum(float(next(fh).split()[0]) for _ in range(nprup))*1e3, nprup
    if not SINGLE: sys.exit(f"{f}: no LHE for the total sigma; refusing the first-process json value (set SINGLE_PROCESS=1 only for single-process cards)")
    j = json.load(open(f[:-5] + ".json")); return float(j["lhe_init_xsec_pb_err_pb_max_lprup"].split()[0])*1e3, 1
def run(d):
    fs = sorted(f for f in glob.glob(d + "/*.root") if not f.endswith(("_gen.root", "_full.root")))[:mx]; n = k = 0; sig = []; npr = set()
    for f in fs:
        s_, np_ = sigma_total_fb(f); sig.append(s_); npr.add(np_); s = select(f, ng); n += len(s); k += int(s.sum())
    return dict(files=len(fs), N=n, n_sel=k, sigma_fb=sum(sig)/len(sig), nprup=sorted(npr))
a, b = run(dn), run(dv); res = {"nomjj": a, "vbs": b, "ng": ng}
ya, yb = a["sigma_fb"]*a["n_sel"]/a["N"], b["sigma_fb"]*b["n_sel"]/b["N"]
if a["n_sel"] and b["n_sel"]:
    res["C"] = ya/yb; res["C_rel_err"] = math.sqrt(1/a["n_sel"]+1/b["n_sel"]); res["loss_frac_of_nomjj_yield"] = 1-yb/ya
json.dump(res, open(out, "w"), indent=1); print(json.dumps(res))
