#!/usr/bin/env python3
"""D49 pre-declared check (written BEFORE any production): stat floor on the reco-SR twin correction C of the QCD lost-lepton part.
C DEFINITION (ZH twin-correction method; frozen reports/FINAL_report.md:245 'C(cuts) = Y(no-mjj-cut twin)/Y(VBS-biased), measured directly at Delphes level with the same cuts', and wh/reports/02_background_overlap.md:94 'C = [sigma*n_sel/N]_nomjj / [sigma*n_sel/N]_mmjj>400'; uncertainty on C = stat (+) full difference (C-1)); here: the region is the reco SR (frozen cut-based SR incl. the H mass window, class lost_lepton_egamma), numerator = no-cut twin (F_QCD_llajj_loose union, 7.5M events), denominator = the future mmjj>400 loose-lepton sample.
STAT FORMULA: rel.err(C)^2 = 1/n_twin + 1/n_cut (raw counts, unit-weight-like rows) >= 1/n_twin, so the floor is fixed by the twin alone, whatever the cut sample size. Also quoted: Garwood 68 % interval of the twin count.
Writes work/d49_floor.json."""
import json, numpy as np
from scipy.stats import chi2
WH = "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh"; cb = json.load(open(f"{WH}/work/sel/selection_final.json"))["cut_based"]["cuts"]
t = dict(np.load(f"{WH}/work/sel/table_v12.npz")); meta = json.load(open(f"{WH}/work/sel/table_v12_meta.json")); cid = meta["classes"]; i = meta["samples"].index("F_QCD_llajj_loose")
base = (t["sid"] == i) & (t["cls"] == cid["lost_lepton_egamma"])
def n(**drop):
    m = base.copy()
    for k, op, key in (("mjj", ">", "mjj"), ("deta", ">", "deta"), ("ptgg", ">", "ptgg"), ("met", ">", "met"), ("mt", ">", "mt"), ("ptl", ">", "ptl")):
        if k not in drop: m &= t[key] > cb[k]
    if "hw" not in drop: m &= np.abs(t["mgg"]-125) < cb["hw"]
    return int(m.sum())
def row(lab, nn):
    lo, hi = (chi2.ppf(0.1587, 2*nn)/2 if nn else 0.0), chi2.ppf(0.8413, 2*(nn+1))/2
    return dict(region=lab, n_twin=nn, rel_err_sqrtn=(1/np.sqrt(nn) if nn else None), garwood68=[lo, hi], rel_interval68=[(lo-nn)/nn if nn else None, (hi-nn)/nn if nn else None])
rows = [row("reco SR (all frozen cut-based cuts incl. H window) [the D49 region]", n()), row("SR without the H mass window (information only)", n(hw=1)), row("SR without mjj, deta, window (information only)", n(hw=1, mjj=1, deta=1))]
out = dict(n_sample_events="7.5e6", rows=rows, floor_rel_err_C=rows[0]["rel_err_sqrtn"], threshold=0.30, verdict="floor %s 0.30 -> %s" % (">=" if rows[0]["rel_err_sqrtn"] and rows[0]["rel_err_sqrtn"] > 0.3 else "<", "option (4) (one-event estimate), no cut sample produced" if rows[0]["rel_err_sqrtn"] and rows[0]["rel_err_sqrtn"] > 0.3 else "produce the cut sample"))
json.dump(out, open(f"{WH}/work/d49_floor.json", "w"), indent=1, default=float); print(json.dumps(out, default=float, indent=1))
