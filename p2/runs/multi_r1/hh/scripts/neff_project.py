#!/usr/bin/env python3
"""Class-resolved N_eff projection of the boosted SR from pilot samples (review item 6; D-HH-4/6).
Per sample, per tagging scenario:
  V = events passing 2 fat jets (pT>=300, lead>=450) + VBS pair (the 'pre-window' stage);  class pair (c1,c2) of the two leading fat jets from truth (l,c,b,bb_nonH,Hbb,top);
  p_win(c) = fraction of selected fat jets of class c with m_SD in [90,150] (own sample; pooled over all samples if <30 jets);   p_i = p_win(c1) p_win(c2)  (factorised window probability)
  tag weight w_i = prod_j p_tag(c_j; scenario).  The hard-window SR statistic has E[sum w] = sum_V p_i w_i, E[sum w^2] = sum_V p_i w_i^2  =>  N_eff_SR(proj) = (sum p w)^2 / (sum p w^2), linear in N_gen.
  direct = actual hard-window SR raw count k and (sum w)^2/sum w^2 in the pilot.   N_needed = N_pilot * 10 / (N_eff_proj,pilot) (x1.5 safety).
  Also: expected SR yield (smoothed) at 500 fb^-1 and its relative MC error; 95 % UL on it: E * Poisson95(n_eff_s)/n_eff_s (class-aware), n_eff_s = (sum p w)^2/sum (p w)^2.
Factorisation assumption (window independent of the VBS pair and of the other jet) is a stated approximation; the direct counts are shown beside the projection.
Usage: neff_project.py <matrix.yaml> <scenarios.yaml> <out.json> <prod_root> sample [sample ...]"""
import sys, json, yaml, numpy as np, os
from scipy.stats import chi2
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hh_reco as R
my, sy, outj, root = sys.argv[1:5]; names = sys.argv[5:]
M = {s["name"]: s for s in yaml.safe_load(open(my))["samples"]}; SC = yaml.safe_load(open(sy))["tagging"]
D = {n: R.load_named(n, root) for n in names}
def pwin_table(d):
    c, m = d["fj_cls_all"], d["fj_msd_all"]; inw = (m > 90) & (m < 150); return {k: (int(((c == k)).sum()), float(inw[c == k].mean()) if (c == k).sum() else 0.0) for k in range(6)}
PT = {n: pwin_table(d) for n, d in D.items()}
pool = {k: (sum(PT[n][k][0] for n in PT), sum(PT[n][k][0] * PT[n][k][1] for n in PT) / max(1, sum(PT[n][k][0] for n in PT))) for k in range(6)}
def poisson95(k): return 0.5 * chi2.ppf(0.95, 2 * (k + 1))
out = {}
for n, d in D.items():
    s = M[n]; sig = s["sigma_x_BR_fb"]; ng = d["n_gen"]; two, lead, V = R.stages(d); win = V & R.window(d)
    c1 = np.where(d["cls1"] < 0, 0, d["cls1"]).astype(int); c2 = np.where(d["cls2"] < 0, 0, d["cls2"]).astype(int)
    pw = np.array([PT[n][k][1] if PT[n][k][0] >= 30 else pool[k][1] for k in range(6)]); used_pool = [k for k in range(6) if PT[n][k][0] < 30 and PT[n][k][0] + 0 >= 0 and (c1[V] == k).any() or False]
    p = pw[c1] * pw[c2]
    r = dict(sigma_x_BR_fb=sig, N_pilot=ng, n_two=int(two.sum()), n_lead=int(lead.sum()), n_V=int(V.sum()), n_SR_direct=int(win.sum()),
             p_win={R.CLS[k]: dict(n_jets=PT[n][k][0], p=float(pw[k]), pooled=bool(PT[n][k][0] < 30)) for k in range(6)}, scen={})
    for sc, q in SC.items():
        w = R.tag_weight(d, q); pwv = (p * w)[V]; w2 = (p * w * w)[V]
        Sw, Sw2 = float(pwv.sum()), float(w2.sum()); neff = Sw**2 / Sw2 if Sw2 > 0 else 0.0
        dw = (w * win); dneff = float(dw.sum())**2 / float((dw**2).sum()) if (dw**2).sum() > 0 else 0.0
        nes = Sw**2 / float((pwv**2).sum()) if (pwv**2).sum() > 0 else 0.0
        yld = sig * 500.0 * Sw / ng
        cls_res = {}
        for a in range(6):
            for b in range(a, 6):
                m_ = V & (((c1 == a) & (c2 == b)) | ((c1 == b) & (c2 == a)))
                if m_.sum() == 0: continue
                x = (p * w)[m_]; x2 = (p * w * w)[m_]
                cls_res[f"{R.CLS[a]}-{R.CLS[b]}"] = dict(n_V=int(m_.sum()), E_sumw_frac=float(x.sum() / Sw) if Sw > 0 else 0.0, neff_proj_pilot=float(x.sum()**2 / x2.sum()) if x2.sum() > 0 else 0.0)
        kd = int(win.sum()); yd = float(sig * 500.0 * dw.sum() / ng); ul_ca = (yld * poisson95(nes) / nes if nes > 0 else None)
        ul_dir = (yd * poisson95(kd) / kd if kd > 0 else None)      # direct hard-window Poisson 95 % UL on the weighted SR yield (raw count kd, mean weight scale)
        ul_final = max(x for x in (ul_ca, ul_dir) if x is not None) if (ul_ca is not None or ul_dir is not None) else None
        out_s = dict(k_direct=kd, yield_direct_500fb=yd, yield_500fb_UL95_classaware=ul_ca, yield_500fb_UL95_direct=ul_dir, neff_proj_pilot=neff, neff_direct_pilot=dneff, E_sumw_pilot=Sw, yield_500fb_smoothed=yld, rel_mc_err=(1 / np.sqrt(nes) if nes > 0 else None),
                     yield_500fb_UL95=ul_final, neff_smoothed_n=nes,
                     N_for_neff10=(ng * 10.0 / neff * 1.5 if neff > 0 else None), per_event_neff=neff / ng, classes=cls_res)
        r["scen"][sc] = out_s
    out[n] = r
json.dump(out, open(outj, "w"), indent=1, default=float)
for n, r in out.items():
    s = r["scen"]["nominal"]; print(f"{n:28s} N={r['N_pilot']:7d} two={r['n_two']:5d} V={r['n_V']:4d} SRraw={r['n_SR_direct']:3d} neff_proj(nom)={s['neff_proj_pilot']:.3g} direct={s['neff_direct_pilot']:.3g} y500={s['yield_500fb_smoothed']:.3g} N_for_10={s['N_for_neff10'] if s['N_for_neff10'] is None else format(s['N_for_neff10'],'.3g')}")
