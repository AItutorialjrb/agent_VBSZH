"""Shared D49 option-(4) text and the upper-end table (S2): D49 is SETTLED by D50 = option (4). Reads work/d49_floor.json, work/v12_lostlep_neff.json, work/stat/ll4_<L>_v12.json."""
import json, os
WH = "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh"; S = f"{WH}/work/stat"
J = lambda p: json.load(open(p)) if os.path.exists(p) else None
FL = J(f"{WH}/work/d49_floor.json"); LN = J(f"{WH}/work/v12_lostlep_neff.json"); P = LN["QCD_part_poisson"]
Y0 = P["Y"]; I95 = P["interval95"]
# exact central 68.27 % (1 sigma) Garwood interval = work file "interval68" (p = 0.158655 each side); 'exact 68 %' (0.16/0.84) differs in the 3rd digit
I1S = P["interval68"]
LL4 = {L: J(f"{S}/ll4_{L}_v12.json") for L in (500, 1000, 3000)}
def rows(L): return {r["scenario"]: r for r in LL4[L]["rows"]} if LL4[L] else {}
def one_line():
    return (f"D49 SETTLED by D50 = option (4): the QCD lost-lepton / e->gamma part is the one-event estimate {Y0:.3f} events (one selected raw F_QCD_llajj_loose row, 7.5M-event union), "
            f"95 % Garwood interval [{I95[0]:.4f}, {I95[1]:.3f}] (1-sigma central interval [{I1S[0]:.3f}, {I1S[1]:.3f}]); the pre-declared reco-SR twin correction C has a stat floor of {FL['floor_rel_err_C']*100:.0f} % (> 30 %), so no cut sample was produced (work/d49_floor.json); "
            f"the v1 vbs x C estimate (0.176 [0.094, 0.257]) is a CROSS-CHECK, not an independent estimate; the upper-end result is shown with the central one (table in this report). The class still does NOT meet the D42 N_eff >= 10 rule (one-event dominated; stated limitation).")
def _lam(L, sfx, tag):
    c = J(f"{S}/couplings_vh{tag}{'' if L == 500 else '_L%d' % L}{sfx}_v12.json")
    return (c["curves"]["WH"]["Z_lambda_m1"], c["curves"]["VH"]["Z_lambda_m1"]) if c else (None, None)
def table_md():
    out = ["| L (fb-1) | QCD lost-lepton part | Y at 500 fb-1 (window, events; scaled with L in the fit) | Z0 (PL) | mu95 median (-1s, +1s) | lambda=-1 Z WH / VH, kZ-sign (primary) | lambda=-1 Z WH / VH, kW-sign (kW<0, kZ=kt=+1, BR x2.45; D46) |", "|---|---|---|---|---|---|---|"]
    for L in (500, 1000, 3000):
        for lab, sfx in (("lower95", "_ll0.0253"), ("central", ""), ("upper95", "_ll5.57")):
            r = rows(L).get(lab); kz = _lam(L, sfx, "_kzneg"); kw = _lam(L, sfx, "")
            if r: out.append(f"| {L} | {lab} | {r['Y_QCD_llpart']:.4f} | {r['Z0_PL']:.3f} | {r['mu95_exp'][1]:.2f} ({r['mu95_exp'][0]:.2f}, {r['mu95_exp'][2]:.2f}) | {kz[0]:.3f} / {kz[1]:.3f} | {kw[0]:.3f} / {kw[1]:.3f} |")
    return "\n".join(out)
def section_md(h="D49 option (4): central and upper-end result"):
    return f"\n## {h}\n\n{one_line()}\n\nWH alone, definition (a), stand-alone WH workspace, full systematics (task ll4:L, the two QCD groups efake_qcd_ll + efake_qcd_eg scaled to the interval ends, whole m_gg template; the central row reproduces the nominal fit). Y0 uses the gridpack sigma (the closure sigma gives 0.12101, -0.17 %, a normalisation note, not a change of the estimate). The sample ZH_Zaajj_QCD_nomjj_lostlep of the same class has N_eff = 2.0 (yield 0.0029): it too is below the N_eff >= 10 rule.\n\n{table_md()}\n\nThe lambda=-1 exclusion (reduced coupling model, QCD lost-lepton groups scaled to the same interval ends) is INSENSITIVE to the lost-lepton level; the Z0 / mu95 columns move.\n"
