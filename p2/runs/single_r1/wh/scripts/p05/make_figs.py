#!/usr/bin/env python3
"""single_r1 WH Phase 05-07 figures (PNG + PDF) from the Store and work/p05/{p05,bdt,p07}.json.
Palette: dataviz reference categorical order (blue, orange, aqua, yellow, magenta, green, violet, red)."""
import sys, os, json, glob, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import whana as A
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
C = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"]
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e4e3df"
plt.rcParams.update({"font.size": 10, "axes.edgecolor": INK2, "axes.labelcolor": INK, "xtick.color": INK2, "ytick.color": INK2,
                     "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "axes.spines.top": False, "axes.spines.right": False,
                     "legend.frameon": False, "figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb"})
W = f"{A.WH}/work/p05"; FIG = f"{A.WH}/figures"; os.makedirs(FIG, exist_ok=True)
P5, B, P7 = (json.load(open(f"{W}/{n}.json")) for n in ("p05", "bdt", "p07"))
tup = lambda c: {k: (tuple(v) if isinstance(v, list) else v) for k, v in c.items()}
FINAL = tup(P7["final_cuts"])
def save(fig, name):
    fig.tight_layout(); [fig.savefig(f"{FIG}/{name}.{e}", dpi=150) for e in ("png", "pdf")]; plt.close(fig)

# 1) m_gg at the final selection (fit range), 500 /fb, stacked by source class
S = A.Store(verbose=False); S.ceg = {k: tuple(v) for k, v in P5["eg_closure_factor"].items()}
for f in glob.glob(f"{W}/bdt_scores/*.npz"):
    k, t = os.path.basename(f)[:-4].split("__")
    if k in S.T and S.T[k].get(t): S.T[k][t]["bdt"] = np.load(f)["score"]
GRP = [("EW W±Hjj signal", lambda k, t: A.R[k]["role"] == "sig"), ("other H→γγ (QCD WH, tH, tt̄H, ZH, τν)", lambda k, t: A.is_res(k) and A.R[k]["role"] != "sig" and t == "D"),
       ("prompt Wγγjj, Zγγjj, tt̄γγ", lambda k, t: (not A.is_res(k)) and t == "D"), ("non-prompt γ (j→γ)", lambda k, t: t in ("F1", "F2")),
       ("e→γ", lambda k, t: t == "EG"), ("non-prompt ℓ (j→ℓ)", lambda k, t: t == "FL")]
edg = np.arange(105, 161, 2.5); L = 500.; H = []
for name, fn in GRP:
    h = np.zeros(len(edg) - 1)
    for k in S.T:
        if A.R[k]["role"] in ("xcheck", "coup"): continue
        for t in ("D", "F1", "F2", "FL", "EG"):
            if not fn(k, t): continue
            T, w, use = S.rows(k, t, A.SC0)
            if T is None: continue
            m = A.sel(T, FINAL, window=False) & use
            if A.R[k]["cls"] == "FL" and t == "D": m &= T["cat"] != "NPL"
            h += np.histogram(T["mgg"][m], bins=edg, weights=w[m]*L)[0]
    H.append(h)
fig, ax = plt.subplots(figsize=(6.4, 4.2)); bot = np.zeros(len(edg) - 1); cen = 0.5*(edg[1:] + edg[:-1])
order = [2, 3, 4, 5, 1, 0]
for j, i in enumerate(order):
    ax.bar(cen, H[i], width=2.5*0.92, bottom=bot, color=C[i], label=GRP[i][0], edgecolor="#fcfcfb", linewidth=1.0); bot += H[i]
ax.axvspan(*FINAL["win"], color=GRID, alpha=0.5, zorder=0)
ax.set_xlabel("m$_{γγ}$ [GeV]"); ax.set_ylabel("expected events / 2.5 GeV  (500 fb$^{-1}$)")
ax.set_title("WH final selection (BDT), Delphes level; shaded: m$_{γγ}$ window", fontsize=9, color=INK2)
h_, l_ = ax.get_legend_handles_labels(); ax.legend(h_[::-1], l_[::-1], fontsize=7.5, loc="upper right"); save(fig, "p07_mgg_final")
json.dump(dict(edges=edg.tolist(), groups=[g[0] for g in GRP], counts=[h.tolist() for h in H]), open(f"{W}/fig_mgg_final.json", "w"))

# 2) lambda_WZ scan
fig, ax = plt.subplots(figsize=(6.0, 4.0))
for i, Ls in enumerate(("500", "1000", "3000")):
    c = P7["coupling"][Ls]; ax.plot(c["scan_lam"]["lam"], c["scan_lam"]["q"], color=C[i], lw=2, label=f"{Ls} fb$^{{-1}}$")
for y, t in ((1, "68 %"), (3.84, "95 %")): ax.axhline(y, color=INK2, lw=0.8, ls="--"); ax.text(2.85, y + 0.3, t, fontsize=8, color=INK2, ha="right")
ax.axvline(0, color=INK2, lw=0.8)
ax.set_ylim(0, 30); ax.set_xlim(-2, 3); ax.set_xlabel("λ$_{WZ}$ = κ$_W$/κ$_Z$  (κ$_Z$ = 1)"); ax.set_ylabel("−2 Δln L  (Asimov SM, counting, syst.)")
ax.set_title("EW WHjj rate vs λ$_{WZ}$; BR(H→γγ) fixed to SM", fontsize=9, color=INK2); ax.legend(fontsize=8, loc="upper left"); save(fig, "p07_lambdaWZ_scan")
# 3) (kW, kZ) contours
fig, ax = plt.subplots(figsize=(5.6, 4.6))
for i, Ls in enumerate(("500", "3000")):
    c = P7["coupling"][Ls]["scan2d"]; X, Y = np.meshgrid(c["kw"], c["kz"]); Q = np.array(c["q"])
    ax.contour(X, Y, Q, levels=[2.30, 5.99], colors=[C[i], C[i]], linestyles=["-", "--"], linewidths=2)
    ax.plot([], [], color=C[i], lw=2, label=f"{Ls} fb$^{{-1}}$: 68 % (solid), 95 % (dashed)")
ax.plot([1], [1], marker="*", ms=12, color=INK, ls="none", label="SM"); ax.plot([-1], [1], marker="x", ms=9, color=C[7], ls="none", label="λ$_{WZ}$ = −1")
ax.set_xlabel("κ$_W$"); ax.set_ylabel("κ$_Z$"); ax.legend(fontsize=7.5, loc="lower left")
ax.set_title("(κ$_W$, κ$_Z$) from the EW WHjj rate (counting, syst.)", fontsize=9, color=INK2); save(fig, "p07_kappa_contours")
# 4) BDT threshold scan
fig, ax = plt.subplots(figsize=(6.0, 3.8)); sc = B["scan"]
ax.plot([x["t"] for x in sc], [x["Z"] for x in sc], color=C[0], lw=2, marker="o", ms=4, label="BDT (k-fold scores)")
ax.axhline(B["Z_cut"], color=C[1], lw=2, ls="--", label="cut-based optimum"); ax.axvline(B["t_best"], color=INK2, lw=0.8)
ax.set_xlabel("BDT score threshold"); ax.set_ylabel("Z (with σ$_b$), 500 fb$^{-1}$, def. a"); ax.legend(fontsize=8)
ax.set_title("BDT threshold scan on expected quantities", fontsize=9, color=INK2); save(fig, "p05_bdt_scan")
# 5) j->gamma closure: m_jj shape of Delphes direct non-prompt photons vs per-jet weighting (W+jets)
fig, ax = plt.subplots(figsize=(6.0, 3.8)); cj = P5["closure_jg"]["F_Wjjjj"]["by_mjj"]; x = np.arange(4)
d = np.array(cj["direct"]); p6 = np.array(cj["pred_delphes6a"]); ps = np.array(cj["pred_scenario"]); dr = np.array(cj["direct_raw"])
ax.errorbar(x, d/d.sum(), yerr=d/d.sum()/np.sqrt(np.maximum(dr, 1)), fmt="o", ms=8, color=INK, label="Delphes direct non-prompt γ")
ax.plot(x - 0.12, p6/p6.sum(), "s", ms=8, color=C[0], label="per-jet weighting, Delphes rate (FORMAT 6a)")
ax.plot(x + 0.12, ps/ps.sum(), "D", ms=8, color=C[1], label="per-jet weighting, nominal scenario")
ax.set_xticks(x, ["0-200", "200-500", "500-1000", ">1000"]); ax.set_xlabel("m$_{jj}$ of the two leading other jets [GeV]"); ax.set_ylabel("fraction")
ax.set_title("j→γ closure (W+4j, one-fake level): shapes; normalisations in 05 §4", fontsize=9, color=INK2); ax.legend(fontsize=7.5); save(fig, "p05_closure_jg_mjj")
print("figures written to", FIG)
