#!/usr/bin/env python3
"""WH single_r2: cross-section collector + per-sample BR ledger with assertions (SPEC_G0 §1.6).
Reads every work/smoke/*/status.txt and work/gp_condor/*_status.txt, writes config/xsec_br_ledger.json and prints a markdown table.
BR rules (asserted, abort on violation):
  * BGG (H->gg) at most once, only for samples with an undecayed H forced to gg in PY8;
  * WF exactly once per leptonic W whose decay is computed by MG5 (decay chain or l-nu in the ME); HF once per hadronic W in an MG5
    decay chain; TF once per top decayed in MG5; no factor for decays done by PY8 with its own tables except the forced H.
Usage: python3 xsec_br_ledger.py"""
import glob, json, math, re, pathlib, sys
WH = pathlib.Path(__file__).resolve().parent.parent
# ---------------- physical inputs (sources in reports/01_signal_definition.md §4)
B_PDG = dict(e=0.1071, mu=0.1063, tau=0.1138, l_univ=0.1086, had=0.6741)       # PDG 2025 W listing (config/sources/pdg2025_w.txt l.413-417)
aEW, Gf, MZ, MT, WW, WT = 1/132.507, 1.16639e-5, 91.188, 173.0, 2.0476, 1.4915  # MG5 sm-no_b_mass restriction
MW = math.sqrt(MZ**2/2 + math.sqrt(MZ**4/4 - aEW*math.pi*MZ**2/(Gf*math.sqrt(2)))); SW2 = 1 - MW**2/MZ**2
G_LNU = 4*math.pi*aEW*MW/(48*math.pi*SW2)                                       # MG5-LO Gamma(W->l nu) per lepton flavour
B_MG5_LNU = G_LNU/WW; B_MG5_HAD = 6*G_LNU/WW                                    # massless quarks, diagonal CKM, no QCD correction
X = MW**2/MT**2; G_TBW = 4*math.pi*aEW/SW2*MT**3/(64*math.pi*MW**2)*(1 - X)**2*(1 + 2*X)
F = dict(BGG=0.002270,                                  # LHCHWG YR4, mH=125 GeV (as ZH)
         WF=B_PDG["l_univ"]/B_MG5_LNU,                  # nominal: lepton-universal PDG fit (D-WH-2); per W->e/mu/tau nu in MG5
         HF=B_PDG["had"]/B_MG5_HAD,                     # per W->jj in an MG5 decay chain
         TF=1.0/(G_TBW/WT),                             # per t->bW in an MG5 decay chain (physical B(t->Wb)=1)
         ZF=0.9783, BR_ZLL=0.067294, one=1.0)           # frozen ZH ledger (reuse samples only)
ALT = dict(WF_nonuniv=(B_PDG["e"] + B_PDG["mu"])/(2*B_MG5_LNU))
# ---------------- per-sample ledger: (W/t decay, H decay, factor list, n_lepW_MG5, n_hadW_MG5, n_top_MG5, has_forced_H)
L = {
 "S_EW_WHjj":          ("W->l nu (e,mu) MG5 decay chain", "H->gg forced PY8 (cond. BR 1)", ["WF", "BGG"], 1, 0, 0, True),
 "S_EW_WHjj_nodecay":  ("undecayed", "undecayed", [], 0, 0, 0, False),
 "S_EW_WHjj_5F_nodecay": ("undecayed", "undecayed", [], 0, 0, 0, False),
 "S_EW_WHjj_5Fnotop_nodecay": ("undecayed", "undecayed", [], 0, 0, 0, False),
 "S_EW_WHjj_offshell": ("l nu in ME (no chain)", "H->gg forced PY8", ["WF", "BGG"], 1, 0, 0, True),
 "H_QCD_WHjj":         ("W->l nu (e,mu) MG5 decay chain", "H->gg forced PY8 (cond. BR 1)", ["WF", "BGG"], 1, 0, 0, True),
 "H_QCD_WHjj_nodecay": ("undecayed", "undecayed", [], 0, 0, 0, False),
 "I_WHjj":             ("undecayed (signed)", "undecayed", [], 0, 0, 0, False),
 "H_EW_WHjj_tau":      ("W->tau nu MG5 chain, tau in PY8", "H->gg forced PY8", ["WF", "BGG"], 1, 0, 0, True),
 "B_EW_Waajj":         ("W->l nu MG5 decay chain", "no H", ["WF"], 1, 0, 0, False),
 "B_QCD_Waajj":        ("W->l nu MG5 decay chain", "no H", ["WF"], 1, 0, 0, False),
 "B_QCD_Waajj_vbs":    ("W->l nu MG5 decay chain", "no H", ["WF"], 1, 0, 0, False),
 "F_QCD_Wajj":         ("l nu in ME (no chain)", "no H", ["WF"], 1, 0, 0, False),
 "F_QCD_Wajj_nomjj":   ("l nu in ME (no chain)", "no H", ["WF"], 1, 0, 0, False),
 "F_EW_Wajj":          ("l nu in ME (no chain)", "no H", ["WF"], 1, 0, 0, False),
 "F_Wjj":              ("l nu in ME (no chain)", "no H", ["WF"], 1, 0, 0, False),
 "F_aajj":             ("none (fake lepton x f_l)", "no H", ["one"], 0, 0, 0, False),
 "T_tta_1l":           ("t->bW, W->l nu + W->jj MG5 chains", "no H", ["TF", "TF", "WF", "HF"], 1, 1, 2, False),
 "T_tta_2l":           ("t->bW, both W->l nu MG5 chains", "no H", ["TF", "TF", "WF", "WF"], 2, 0, 2, False),
 "T_ttaa_1l":          ("t->bW, W->l nu + W->jj MG5 chains", "no H", ["TF", "TF", "WF", "HF"], 1, 1, 2, False),
 "T_tWa_1l":           ("t->bW + W, one l nu one jj, MG5 chains", "no H", ["TF", "WF", "HF"], 1, 1, 1, False),
 "H_ttH_1l":           ("t->bW, W->l nu + W->jj MG5 chains", "H->gg forced PY8", ["TF", "TF", "WF", "HF", "BGG"], 1, 1, 2, True),
 "H_ttH_2l":           ("t->bW, both W->l nu MG5 chains", "H->gg forced PY8", ["TF", "TF", "WF", "WF", "BGG"], 2, 0, 2, True),
 "H_tHq":              ("t->b l nu MG5 chain", "H->gg forced PY8", ["TF", "WF", "BGG"], 1, 0, 1, True),
 "H_tHW":              ("t->bW + W, one l nu one jj, MG5 chains", "H->gg forced PY8", ["TF", "WF", "HF", "BGG"], 1, 1, 1, True),
 "Q_W_aa_0j_offshell": ("l nu in ME", "no H", ["WF"], 1, 0, 0, False),
 "Q_W_aa_0j_onshell":  ("W->l nu MG5 chain", "no H", ["WF"], 1, 0, 0, False),
}
def check(sid, row):
    _, _, fac, nl, nh, nt, fh = row
    assert fac.count("BGG") == (1 if fh else 0), f"{sid}: BGG count"
    assert fac.count("WF") == nl and fac.count("HF") == nh and fac.count("TF") == nt, f"{sid}: per-decay factor count"
    assert not ({"ZF", "BR_ZLL"} & set(fac)), f"{sid}: Z factor in a W sample"
    return math.prod(F[f] for f in fac)
# ---------------- cross sections
def read_status(p):
    t = open(p).read(); m = re.search(r"Cross-section :\s*([-0-9.e+]+) \+- ([0-9.e+-]+) pb", t)
    s = re.search(r"sample=(\S+)", t)[1]; seed = int(re.search(r"seed=(\d+)", t)[1]); rc = int(re.search(r"rc=(\d+)", t)[1])
    d = re.findall(r"Total: (\d+) processes with (\d+) diagrams", t)
    return s, dict(seed=seed, rc=rc, sigma_fb=float(m[1])*1e3 if m else None, err_fb=float(m[2])*1e3 if m else None,
                   diagrams_total=int(d[-1][1]) if d else None, source=str(pathlib.Path(p).relative_to(WH)))
XS = {}
for p in sorted(glob.glob(str(WH/"work/smoke/*/status.txt")) + glob.glob(str(WH/"work/gp_condor/*_status.txt"))):
    s, r = read_status(p)
    if s in XS and XS[s]["sigma_fb"] is not None: continue
    XS[s] = r
out = dict(inputs=dict(B_PDG=B_PDG, MW_MG5=MW, sw2_MG5=SW2, Gamma_lnu_MG5=G_LNU, B_MG5_lnu=B_MG5_LNU, B_MG5_had=B_MG5_HAD,
                       Gamma_tbW_MG5=G_TBW, WT=WT, WW=WW), factors=F, alternatives=ALT, samples={})
rows = []
for sid, row in L.items():
    k = check(sid, row); x = XS.get(sid, {})
    sb = x["sigma_fb"]*k if x.get("sigma_fb") is not None else None
    out["samples"][sid] = dict(decay=row[0], hdecay=row[1], factors=row[2], k=k, **x, sigmaBR_fb=sb,
                               sigmaBR_3000=sb*3000 if sb is not None else None,
                               nmc_required=max(50000, sb*3000) if sb is not None else None)
    rows.append(f"| {sid} | {row[0]} | {row[1]} | {' x '.join(row[2]) or '-'} | {k:.6g} | "
                + (f"{x['sigma_fb']:.5g} ± {x['err_fb']:.2g}" if x.get('sigma_fb') is not None else "pending")
                + f" | {x.get('diagrams_total') or '-'} | " + (f"{sb:.4g}" if sb is not None else "-") + " | "
                + (f"{max(50000, sb*3000):.3g}" if sb is not None else "-") + " |")
json.dump(out, open(WH/"config/xsec_br_ledger.json", "w"), indent=1)
print("factors:", {k: round(v, 6) for k, v in F.items()}, "alt:", {k: round(v, 6) for k, v in ALT.items()})
print("| sample | W/t decay | H decay | factors | k | σ_gen [fb] (MG5 int. err.) | diagrams | σ×k [fb] | N_MC req. = max(50k, σk·3000) |")
print("|---|---|---|---|---|---|---|---|---|")
print("\n".join(rows))
missing = [s for s in XS if s not in L]
if missing: sys.exit(f"samples with sigma but no ledger row: {missing}")
