#!/usr/bin/env python3
"""Generator-cut safety from a twin (mmjj=0) sample at the RECO SR BASELINE (review 7c; D8): exactly 1 e/mu (pT>25,|eta|<2.5, no 2nd lepton pT>10), MET>30, 0 b-tags (jets pT>30,|eta|<2.5),
photons pT>25,|eta|<2.5 (NG=2 with 100<m_gg<170 for 'aa' samples, NG>=1 for 'a' samples: 2nd photon is a jet fake, modelled by weights), >=2 jets pT>30,|eta|<4.7 (dR>0.4 from selected photons/leptons)
with m_jj>500 and |deta_jj|>2.5. For each production generator cut X: fraction of reco-selected events whose parton-level m_jj (LHE outgoing partons j j; first two final-state partons) is < X, with binomial error.
Usage (pinned env): source p2/lib/scripts/setup_stack.sh; python3 -P twin_safety2.py <out.json> <ng:1|2> <slim1.root> <lhe1.lhe.gz> [<slim2> <lhe2> ...]
Criterion in code: 'safe_le_5pct_within_stat' = (loss - 1*err) <= 0.05, i.e. the loss is <= 5 % within one statistical sigma; loss, err and n are always reported."""
import sys, os, gzip, json, math, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from srsel import select
out, ng = sys.argv[1], int(sys.argv[2]); files = list(zip(sys.argv[3::2], sys.argv[4::2]))
def lhe_mjj(path):
    res = []; ev = None
    for l in gzip.open(path, "rt"):
        if l.startswith("<event>"): ev = []; first = True; continue
        if l.startswith("</event>"):
            p = [e for e in ev if e[5] == 1 and (abs(e[4]) <= 5 or e[4] == 21)][:2]  # outgoing light partons (jets); W/H/a/leptons excluded
            s = [p[0][i]+p[1][i] for i in range(4)] if len(p) == 2 else [0, 0, 0, 0]
            res.append(math.sqrt(max(s[3]**2-s[0]**2-s[1]**2-s[2]**2, 0))); ev = None; continue
        if ev is None: continue
        if first: first = False; continue
        x = l.split()
        if len(x) >= 13: ev.append((float(x[6]), float(x[7]), float(x[8]), float(x[9]), int(x[0]), int(x[1])))
    return np.array(res)
MG, SEL = [], []
for sl, lh in files:
    mg = lhe_mjj(lh); sel = select(sl, ng); assert len(sel) == len(mg), (len(sel), len(mg)); N = len(mg)
    MG.append(mg); SEL.append(sel)
mg = np.concatenate(MG); sel = np.concatenate(SEL); n = int(sel.sum()); res = {"N_events": int(len(mg)), "n_selected_reco_SR_baseline": n, "ng_required": ng, "cuts": {}}
for X in (100, 150, 200, 250, 300, 400):
    k = int((sel & (mg < X)).sum()); f = k/n if n else None; e = math.sqrt(k*(n-k)/n)/n if n else None
    res["cuts"][str(X)] = {"n_lost": k, "loss": f, "err": e, "safe_le_5pct_within_stat": (f is not None and (f - 1.0*e) <= 0.05)}
json.dump(res, open(out, "w"), indent=1); print(json.dumps(res))
