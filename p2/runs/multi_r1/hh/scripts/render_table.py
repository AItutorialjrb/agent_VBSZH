#!/usr/bin/env python3
"""Replace @@MATRIX@@ / @@FEAS@@ tokens in reports/*.src.md -> reports/*.md using config/sample_matrix.yaml and work/sr_feasibility.json."""
import yaml, json, sys, os, glob
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
m = yaml.safe_load(open(f"{H}/config/sample_matrix.yaml"))["samples"]
def f(x, p=4): return "n/a" if x is None else (f"{x:.{p}g}")
rows = ["| idx | sample | class/role | ME process (model) | generator cuts | σ_MG5-LO [pb] | BR ledger (total) | brute-force N for σ·BR·3000 fb⁻¹ | N policy / plan |", "|---|---|---|---|---|---|---|---|---|"]
for s in m:
    if s["cls"] == "validation": continue
    cut = ", ".join(f"{k}={v}" for k, v in s["generator_cuts"].items()) + (" +any-pair VBS filter" if s["vbs_anypair_patch"] else "")
    sg = "pending" if s.get("sigma_pb") is None else f"{f(s['sigma_pb'])} ± {f(s['sigma_err_pb'],2)}"
    nb = f(s.get("brute_force_N_for_3000fb"), 3) if s.get("brute_force_N_for_3000fb") else "-"
    pol = f"N≥{s['N_MC_required']:,}" if s.get("N_MC_required") else ("effective-N" if s["cls"] != "signal" else "-")
    if not s["phase03_gridpack"]: pol += " (planned, no Phase-03 gridpack)"
    rows.append(f"| {s['idx']} | {s['name']} | {s['cls']}/{s['role']} | `{s['process'].replace(chr(10), '; ')}` ({s['model']}) | {cut} | {sg} | {'×'.join(s['br_ledger'])} ({s['br_total']}) | {nb} | {pol} |")
T = "\n".join(rows)
fe = json.load(open(f"{H}/work/sr_feasibility.json")) if os.path.exists(f"{H}/work/sr_feasibility.json") else {}
def cell(d):
    if d.get("interval95_500fb"): lo, hi = d["interval95_500fb"]; return f"{d['expected_SR_events_at_500fb']:.3g} [{lo:.2g}, {hi:.2g}]"
    return f"< {d['ul95_500fb']:.2g} (95% UL)"
fr = ["| test sample (2000 ev) | ≥2 fat jets | +lead≥450 | +VBS pair | +both m_SD∈[90,150] (raw SR) | N_eff (nominal) | expected SR events at 500 fb⁻¹, pessimistic | nominal | optimistic |", "|---|---|---|---|---|---|---|---|---|"]
for s, r in fe.items():
    w = r["weighted"]; fr.append(f"| {s} | {r['raw']['two_fatjets']} | {r['raw']['plus_lead450']} | {r['raw']['plus_vbs']} | {r['raw']['plus_msd_window']} | {w['nominal']['neff']:.1f} | {cell(w['pessimistic'])} | {cell(w['nominal'])} | {cell(w['optimistic'])} |")
F = "\n".join(fr)
x = ["| sample | ME process | cuts | σ_LO [pb] | BR | brute N (3000 fb⁻¹) |", "|---|---|---|---|---|---|"]
for s in m:
    if s["cls"] == "extra_bkg": x.append(f"| {s['name']} | `{s['process'].replace(chr(10), '; ')}` | {', '.join(f'{k}={v}' for k,v in s['generator_cuts'].items())} | {'pending' if s.get('sigma_pb') is None else f(s['sigma_pb'])} | {'×'.join(s['br_ledger'])} | {f(s.get('brute_force_N_for_3000fb'),3) if s.get('brute_force_N_for_3000fb') else '-'} |")
X = "\n".join(x)
for src in glob.glob(f"{H}/reports/*.src.md"):
    open(src.replace(".src.md", ".md"), "w").write(open(src).read().replace("@@MATRIX@@", T).replace("@@FEAS@@", F).replace("@@EXTRA@@", X).replace("@@MG5DIFF@@", open(f"{H}/config/mg5priv_diff.md").read()).replace("@@SIGMA@@", open(f"{H}/work/sigma_closure.md").read()).replace("@@GGHH_MORPH@@", open(f"{H}/work/gghh_morph.md").read() if os.path.exists(f"{H}/work/gghh_morph.md") else "ggF HH kappa-lambda morphing closure: PENDING (gridpacks kl=0,2,5 not finished)."))
print("rendered")
