#!/usr/bin/env python3
"""Figures (PDF+PNG) for 05-07: mgg at the primary selection (stacked classes, raw MC), selection scan summary, D36 scans, expected lambda exclusion."""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from stat_lib import *
t, meta, Y = load(); m0 = selmask(t); F = f"{WH}/figures"; nm = lambda n: next((n+x for x in ("_v12", "_v11") if os.path.exists(f"{WH}/work/stat/{n}{x}.json")), n); ex = lambda n: os.path.exists(f"{WH}/work/stat/{nm(n)}.json"); J = lambda n: json.load(open(f"{WH}/work/stat/{nm(n)}.json"))
def save(fig, n): fig.savefig(f"{F}/{n}.pdf"); fig.savefig(f"{F}/{n}.png", dpi=130); plt.close(fig)
H = {g: hist(t, meta, g, m0) for g in GROUPS}; fig, ax = plt.subplots(figsize=(7, 4.5)); bot = np.zeros(NB); cent = 0.5*(EDGES[:-1]+EDGES[1:])
cols = plt.cm.tab20(np.linspace(0, 1, 20)); order = [g for g in GROUPS if g != "sig"]
for i, g in enumerate(order): ax.bar(cent, H[g][0], width=2.0, bottom=bot, color=cols[i], label=g, linewidth=0); bot += H[g][0]
ax.step(EDGES, np.append(H["sig"][0], H["sig"][0][-1])*10, where="post", color="k", lw=1.5, label="signal x10"); ax.set_xlabel("m_gg [GeV]"); ax.set_ylabel("events / 2 GeV at 500 fb$^{-1}$"); ax.legend(fontsize=5, ncol=3); ax.set_title("Cut-based primary selection, nominal MC (unsmoothed)", fontsize=9); save(fig, "mgg_selection")
if ex("counting"):
    c = J("counting"); L = [500, 1000, 3000]; fig, ax = plt.subplots(figsize=(5, 4)); ax.plot(L, [c[f"L{l}"]["Z_eq1"] for l in L], "o-", label="Eq. 1 counting (a)"); ax.plot(L, [c[f"def_b_L{l}"]["Z_eq1"] for l in L], "s--", label="Eq. 1 counting (b)")
    for d, mk in (("a", "^-"), ("b", "v--")):
        if all(ex(f"pl_{l}_{d}") for l in L): ax.plot(L, [J(f"pl_{l}_{d}")["full_syst_BB"]["Z0"] for l in L], mk, label=f"PL fit, syst+BB ({d})")
    ax.set_xlabel("L [fb$^{-1}$]"); ax.set_ylabel("expected Z"); ax.legend(fontsize=7); save(fig, "Z_vs_lumi")
for kind in ("fake", "npl"):
    for L in (500, 3000):
        if ex(f"d36_{kind}_{L}"):
            d = J(f"d36_{kind}_{L}"); fig, ax = plt.subplots(1, 2, figsize=(9, 3.6)); f = [r["f"] for r in d["scan"]]
            ax[0].semilogx(f, [r["Z0_PL"] for r in d["scan"]], "o-"); ax[0].axvspan(0.3, 3, color="g", alpha=0.1); ax[0].set_xlabel(f"{kind} normalisation factor (D36 range shaded)"); ax[0].set_ylabel("expected Z0 (PL)")
            ax[1].loglog(f, [r["mu95_exp"][1] for r in d["scan"]], "o-"); ax[1].axvspan(0.3, 3, color="g", alpha=0.1); ax[1].set_xlabel("factor"); ax[1].set_ylabel("expected mu95 (median)"); fig.suptitle(f"D36 scan {kind}, {L} fb$^{{-1}}$", fontsize=9); save(fig, f"d36_{kind}_{L}")
for tag in ("", "_nobr"):
    if ex("couplings"+tag):
        c = J("couplings"+tag); fig, ax = plt.subplots(figsize=(5, 4))
        for lab, v in c["expected_exclusion"].items(): ax.plot([float(l) for l in v["q"]], [np.sqrt(q) for q in v["q"].values()], label=lab)
        ax.axhline(2, color="gray", ls=":"); ax.axhline(1, color="gray", ls=":"); ax.set_xlabel("$\\lambda_{WZ}$"); ax.set_ylabel("expected exclusion Z (SM data), 500 fb$^{-1}$"); ax.legend(fontsize=7); ax.set_title("couplings"+tag, fontsize=9); save(fig, "lambda_exclusion"+tag)
print(sorted(os.listdir(F)))
