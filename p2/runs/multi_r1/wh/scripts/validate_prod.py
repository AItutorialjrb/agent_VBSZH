#!/usr/bin/env python3
"""Production validation (reads the per-job json written by run_job.sh in p2/production/wh/<sample>/): per sample jobs done vs submitted, LHE = Delphes per job, sum n_lhe / n_delphes,
PY8 sigma (sum line, mb -> fb) mean +- spread vs the gridpack sigma of the plan, seeds unique and inside the submitted seed list. Writes work/prod_validation.csv and prints failures."""
import glob, json, os, re, csv, yaml, collections
WH = "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh"; PR = "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/production/wh"
m = {r["id"]: r for r in yaml.safe_load(open(f"{WH}/config/sample_matrix.yaml"))["samples"]}
sub = collections.defaultdict(lambda: {"seeds": [], "ev": 0})
for f in glob.glob(f"{WH}/work/condor/prod/prod_*.sub"):
    s = re.sub(r"_(topup|resub\d+)$", "", os.path.basename(f)[5:-4])
    if not os.path.exists(os.path.join(os.path.dirname(f), ".submitted_" + os.path.basename(f)[5:-4])): continue
    for l in open(f):
        if l.startswith("  ") and "tar.gz" in l: t = l.split(); sub[s]["seeds"].append(int(t[7])); sub[s]["ev"] += int(t[3])
rows = []; bad = []
for s in sorted(sub):
    js = [f for f in glob.glob(f"{PR}/{s}/*.json")]; nl = nd = 0; sg = []; seeds = []; mism = 0
    for f in js:
        j = json.load(open(f)); nl += j["n_lhe"]; nd += j["n_delphes"]; seeds.append(j["mg_seed"]); mism += j["n_lhe"] != j["n_delphes"]
        mm = re.search(r"\|\s+sum\s+\|\s+\d+\s+\d+\s+\d+\s+\|\s+(\S+)\s+(\S+)\s+\|", j["pythia_sum_line"]); 
        if mm: sg.append(float(mm.group(1))*1e12)
    sig_pl = m[s].get("sigma_fb"); sgm = sum(sg)/len(sg) if sg else None
    clos = (sgm/sig_pl-1) if (sgm and sig_pl) else None
    dup = len(seeds) != len(set(seeds)); out = [x for x in seeds if x not in set(sub[s]["seeds"])]
    rows.append([s, len(js), len(sub[s]["seeds"]), nl, nd, sub[s]["ev"], mism, "%.4g" % sgm if sgm else "", "%.4g" % sig_pl if sig_pl else "", "%+.2f %%" % (100*clos) if clos is not None else "", dup, len(out)])
    if mism or dup or out: bad.append((s, mism, dup, out[:3]))
with open(f"{WH}/work/prod_validation.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["sample", "jobs_done", "jobs_submitted", "n_lhe", "n_delphes", "events_submitted", "jobs_LHE_ne_Delphes", "PY8_sigma_mean_fb", "plan_sigma_fb", "closure", "dup_seeds", "seeds_outside_submitted"]); w.writerows(rows)
done = sum(r[1] for r in rows); tot = sum(r[2] for r in rows)
print(f"{done}/{tot} jobs with json; samples with problems: {bad or 'none'}")
for r in rows:
    if r[1]: print(r[0], r[1], "/", r[2], "closure", r[9], "LHE!=Delphes jobs:", r[6])
