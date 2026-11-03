#!/usr/bin/env python3
"""A2/A3 (2026-11-03): scale/PDF variations and signed-weight (interference) yields from MG5 LHE files.
Usage: python3 -P lhe_theory.py <kind> <out.json> <lhe1> [<lhe2> ...]
kind: zaajj_nodec (undecayed Z: jets + photon cuts) | zaa0 (zaajj region without jet cuts) | jets (VBS jet cuts only; e.g. undecayed Z/H) | zhjj (H undecayed, Z->ll in ME) | zaajj (on-shell Z->ll + 2 photons) | llajj (ll + 1 photon) | incl (no region)
Region R = parton-level proxy of the signal region (two leading final-state partons pT>25, |eta|<4.7: mjj>500, |deta|>3.5;
  66<mll<116; photons pT>25, pT1/mgg>1/3, pT2/mgg>1/4, 105<mgg<145 (window widened for statistics), mllgg>100).
Weights: central = event weight (XWGTUP); 7-point scale = (MUR,MUF) in {0.5,1,2}^2 minus (0.5,2),(2,0.5) at the nominal
dynamical scale (no DYN_SCALE attribute); PDF = NNPDF3.1 replicas 1-100 (std. dev.). IDs read from <initrwgt>."""
import sys, gzip, re, json, numpy as np
kind, OUT, files = sys.argv[1], sys.argv[2], sys.argv[3:]
MZ = 91.1876
def p4(t): return np.array([float(t[9]), float(t[6]), float(t[7]), float(t[8])])
def m(*ps): s = sum(ps); return np.sqrt(max(s[0]**2 - s[1]**2 - s[2]**2 - s[3]**2, 0))
def pt(p): return np.hypot(p[1], p[2])
def eta(p): return np.arcsinh(p[3]/max(pt(p), 1e-9))
def region(parts):
    q = sorted([p for i, p in parts if (abs(i) <= 5 or i == 21)], key=lambda p: -pt(p))
    q = [p for p in q if pt(p) > 25 and abs(eta(p)) < 4.7]
    if kind == "incl": return True
    if len(q) < 2 and kind in ("jets", "zaajj_nodec"): return False
    if kind == "zaa0": q = [None, None]   # 0-jet off-shell/FSR proxy: all region cuts except the jet cuts
    if kind == "jets": return m(q[0], q[1]) > 500 and abs(eta(q[0]) - eta(q[1])) > 3.5   # VBS jet cuts only (undecayed Z)
    if kind == "zaajj_nodec":   # undecayed on-shell Z: VBS jet cuts + photon cuts (no lepton cuts)
        a = sorted([p for i, p in parts if i == 22], key=lambda p: -pt(p))
        if m(q[0], q[1]) < 500 or abs(eta(q[0]) - eta(q[1])) < 3.5 or len(a) < 2: return False
        mg = m(a[0], a[1]); return pt(a[1]) > 25 and pt(a[0])/mg > 1/3 and pt(a[1])/mg > 1/4 and 105 < mg < 145
    if kind != "zaa0" and (len(q) < 2 or m(q[0], q[1]) < 500 or abs(eta(q[0]) - eta(q[1])) < 3.5): return False
    l = [p for i, p in parts if abs(i) in (11, 13)]
    if len(l) < 2 or not (66 < m(l[0], l[1]) < 116): return False
    a = sorted([p for i, p in parts if i == 22], key=lambda p: -pt(p))
    if kind in ("zaajj", "zaa0"):
        if len(a) < 2: return False
        mg = m(a[0], a[1])
        return pt(a[1]) > 25 and pt(a[0])/mg > 1/3 and pt(a[1])/mg > 1/4 and 105 < mg < 145 and m(l[0], l[1], a[0], a[1]) > 100
    if kind == "llajj": return len(a) >= 1 and pt(a[0]) > 25
    return True
ids = None; S = {}; n = 0; nR = 0
for f in files:
    txt_hdr = []; ev = None; w = None
    for line in gzip.open(f, "rt"):
        if ids is None:
            txt_hdr.append(line)
            if "</initrwgt>" in line or line.startswith("<event"):
                H = "".join(txt_hdr); ids = dict(scale={}, pdf=[])
                for mm in re.finditer(r"<weight id=['\"]?(\w+)['\"]?\s+([^>]*)>", H):
                    wid, attr = mm.group(1), mm.group(2)
                    a = dict(re.findall(r"(\w+)=\"([^\"]*)\"", attr))
                    if "DYN_SCALE" in a: continue
                    if a.get("PDF", "303600") == "303600" and "MUR" in a: ids["scale"][(float(a["MUR"]), float(a["MUF"]))] = wid
                    elif a.get("PDF", "").isdigit() and 303601 <= int(a["PDF"]) <= 303700: ids["pdf"].append(wid)
        if line.startswith("<event"): ev = []; w = {}; hdr = None; continue
        if ev is None: continue
        if line.startswith("</event"):
            n += 1; r = region(ev); x0 = hdr
            for key in ["incl"] + (["R"] if r else []):
                d = S.setdefault(key, dict(n=0, w0=0.0, w0sq=0.0, wpos=0.0, scale={}, pdf=np.zeros(len(ids["pdf"]))))
                d["n"] += 1; d["w0"] += x0; d["w0sq"] += x0*x0; d["wpos"] += x0 > 0
                for k, wid in ids["scale"].items(): d["scale"][str(k)] = d["scale"].get(str(k), 0.0) + w.get(wid, np.nan)
                if len(ids["pdf"]): d["pdf"] += np.array([w.get(wid, np.nan) for wid in ids["pdf"]])
            ev = None; continue
        t = line.split()
        if hdr is None and len(t) >= 6 and not line.lstrip().startswith("<"): hdr = float(t[2]); continue
        if line.lstrip().startswith("<wgt"):
            mm = re.match(r"\s*<wgt id=['\"]?(\w+)['\"]?>\s*([-+0-9.eE]+)", line)
            if mm: w[mm.group(1)] = float(mm.group(2))
            continue
        if len(t) == 13 and int(t[1]) == 1: ev.append((int(t[0]), p4(t)))
res = dict(kind=kind, files=len(files), n_events=n, weight_ids=dict(scale={str(k): v for k, v in ids["scale"].items()}, n_pdf=len(ids["pdf"])))
for key, d in S.items():
    o = dict(n=d["n"], sum_w=d["w0"], sum_w2=d["w0sq"], frac_pos=d["wpos"]/max(d["n"], 1))
    if d["w0"] != 0:
        sv = {k: v/d["w0"] for k, v in d["scale"].items()}
        seven = [v for k, v in sv.items() if k not in ("(0.5, 2.0)", "(2.0, 0.5)")]
        if seven: o["scale_ratios"] = sv; o["scale_up"] = max(seven) - 1; o["scale_down"] = 1 - min(seven)
        if len(d["pdf"]): pr = d["pdf"]/d["w0"]; o["pdf_std"] = float(np.std(pr)); o["pdf_mean"] = float(np.mean(pr))
    res[key] = o
json.dump(res, open(OUT, "w"), indent=1, default=float); print(json.dumps({k: (v if not isinstance(v, dict) else {kk: vv for kk, vv in v.items() if kk != "scale_ratios"}) for k, v in res.items()}))
