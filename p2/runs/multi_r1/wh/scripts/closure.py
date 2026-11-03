#!/usr/bin/env python3
"""BR / sigma closure from the smoke runs: sigma(decayed)/sigma(undecayed) vs analytic MG5 tree B (scripts/br_ledger.py). Prints pulls."""
import re, os, math, sys
sys.path.insert(0, os.path.dirname(__file__)); import br_ledger as B
W = "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh/work/smoke"
def s(n):
    f = f"{W}/{n}/status.txt"
    if not os.path.exists(f): return None
    m = re.search(r"Cross-section :\s+(\S+) \+- (\S+) pb", open(f).read()); return (float(m.group(1))*1e3, float(m.group(2))*1e3) if m else None
def comb(names):
    v = [s(n) for n in names if s(n)]; w = [1/e**2 for _, e in v]; return sum(x*wi for (x, _), wi in zip(v, w))/sum(w), 1/math.sqrt(sum(w))
def ratio(a, b): return a[0]/b[0], a[0]/b[0]*math.hypot(a[1]/a[0], b[1]/b[0])
rows = [("W+ (e,mu)", ["wp_light_wdec"], ["wp_light_nodec"], B.B_MG_LL), ("W- (e,mu)", ["wm_light_wdec", "wm_light_wdec_rep"], ["wm_light_nodec", "wm_light_nodec_rep"], B.B_MG_LL),
        ("W- (e,mu), bwcutoff=1000", ["wm_light_wdec_bw"], ["wm_light_nodec", "wm_light_nodec_rep"], B.B_MG_LL)]
for n, d, u, e in rows:
    if not all(s(x) for x in d): continue
    r, er = ratio(comb(d), comb(u)); print(f"{n:28s} sigma_dec/sigma_undec = {r:.4f} +- {er:.4f}   expected {e:.4f}   pull {(r-e)/er:+.2f}")
# both charges: S_EW_WHjj_smoke (single card, both charges decayed) vs sum undecayed
tot = (comb(["wp_light_nodec"])[0]+comb(["wm_light_nodec", "wm_light_nodec_rep"])[0], math.hypot(comb(["wp_light_nodec"])[1], comb(["wm_light_nodec", "wm_light_nodec_rep"])[1]))
r, er = ratio(s("S_EW_WHjj_smoke"), tot); print(f"{'S_EW_WHjj card, both charges':28s} {r:.4f} +- {er:.4f}   expected {B.B_MG_LL:.4f}   pull {(r-B.B_MG_LL)/er:+.2f}   (undecayed sum {tot[0]:.2f} +- {tot[1]:.2f} fb)")
r, er = ratio(s("S_EW_WHjj_taunu_smoke"), tot); print(f"{'taunu card, both charges':28s} {r:.4f} +- {er:.4f}   expected {B.B_MG_L:.4f}   pull {(r-B.B_MG_L)/er:+.2f}")
allr = [(comb(d), comb(u)) for n, d, u, e in rows[:2]]
d = (allr[0][0][0]+allr[1][0][0], math.hypot(allr[0][0][1], allr[1][0][1])); u = (allr[0][1][0]+allr[1][1][0], math.hypot(allr[0][1][1], allr[1][1][1]))
r, er = ratio(d, u); print(f"{'W+ and W- combined':28s} {r:.4f} +- {er:.4f}   expected {B.B_MG_LL:.4f}   pull {(r-B.B_MG_LL)/er:+.2f}")
print(f"EW sigma(W+Hjj)={comb(['wp_light_nodec'])[0]:.2f}, sigma(W-Hjj)={comb(['wm_light_nodec','wm_light_nodec_rep'])[0]:.2f} fb ; QCD/EW (W+) = {s('wp_qcd_nodec')[0]/s('wp_light_nodec')[0]:.2f}; int/EW (W+) = {s('wp_int_nodec')[0]/s('wp_light_nodec')[0]*100:+.3f}%")
