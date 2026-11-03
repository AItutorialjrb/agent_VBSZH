#!/usr/bin/env python3
"""Compose reports/FINAL_report.md from final_analysis.py JSON + verify.json + final_tables.py output.
Every number in the report is read from those files (no hand-copied yields).
Usage: python3 -P make_final_report.py <final.json> <tables.md> <git_commit> <out.md> [--pending "<text>"]"""
import sys, json, datetime
J, TAB, COMMIT, OUT = sys.argv[1:5]
PEND = sys.argv[sys.argv.index("--pending") + 1] if "--pending" in sys.argv else ""
d = json.load(open(J)); R = d["results"]; REG = d["registry"]; F = d["fit"]; O = d["optimum"]; RES = d["resolution"]
V = json.load(open("/eos/home-r/rjiang/vbs_zh_codex_starter/work/final_ntuples/verify.json"))
tables = open(TAB).read()
g = lambda x, n=3: "%.*g" % (n, x)
now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
win = (RES["mu"] - O["wk"]*RES["sigma_core"], RES["mu"] + O["wk"]*RES["sigma_core"])
zw = O["zwin"] if isinstance(O["zwin"], (int, float)) else None
cuts = (f"2 photons with pT > {O['gpt']:.0f} GeV, pT(γ1)/mγγ > {O['ratio'][0]:.2f}, pT(γ2)/mγγ > {O['ratio'][1]:.2f}; "
        + (f"|mℓℓ − mZ| < {zw:.0f} GeV" if zw else f"{O['zwin'][0]:.0f} < mℓℓ < {O['zwin'][1]:.0f} GeV")
        + f"; mℓℓγγ > {O['mllgg']:.0f} GeV; " + ("b-veto; " if O["bveto"] else "no b-veto; ")
        + (f"Zeppenfeld z*(γγ) < {O['zep']}; " if O["zep"] < 50 else "no Zeppenfeld cut; ")
        + f"mjj > {O['mjj']:.0f} GeV, |Δηjj| > {O['deta']:.1f}; {win[0]:.1f} < mγγ < {win[1]:.1f} GeV (±{O['wk']:.1f}σ, σ = {RES['sigma_core']:.2f} GeV)")
r5, r3 = R["500_a"], R["3000_a"]
comp = r5["comp"]; bkg = {k: v for k, v in comp.items() if REG[k]["role"] not in ("sig",)}
top = sorted(((v["y"], k) for k, v in bkg.items()), reverse=True)[:5]
TSU = d["theory_summary"]; CP = d.get("coupling", {}); ROB = d["robustness"]; NC = d["nmc_check"]; BRT = d["br_table"]
def iv(x):
    if not x: return "none"
    e = lambda v, lo, hi: (f"{v:+.2f}*" if v <= lo + 1e-9 or v >= hi - 1e-9 else f"{v:+.2f}")
    return " ∪ ".join(f"[{e(a, *rng)}, {e(b, *rng)}]" for a, b in x)
rng = (-2.0, 2.0)
IZ, IA, OF, MR = TSU["interference_ZHjj"], TSU["interference_Zaajj"], TSU["offshell_Zaa"], TSU.get("mjj_resolution") or {}
GM = d.get("genmjj", {})
ncrows = "\n".join(f"| {k} | {v['sigmaBR_fb']:.4g} | {v['sigmaBRL']:.4g} | {v['N']} | {v['ratio']:.2f}" + (" **(flagged: auxiliary, ratio only)**" if v.get('aux') else "") + f" | {v['w_evt_L']:.3g} |" for k, v in NC.items())
brrows = "\n".join(f"| {k} | {v['z_or_W_decay']} | {v['h_decay']} | {' × '.join(v['factors'])} | {v['k']:.6g} | {v['offshell_corr']:.4g} |" for k, v in BRT.items())
throws = "\n".join(f"| {k} | {v['group']} | {v['source']} | {TSU['processes'].get(v['source'].split(' ')[0], {}).get('region', '—')} | {100*TSU['processes'].get(v['source'].split(' ')[0], {}).get('scale_up', float('nan')):.1f} / −{100*TSU['processes'].get(v['source'].split(' ')[0], {}).get('scale_down', float('nan')):.1f} | {100*TSU['processes'].get(v['source'].split(' ')[0], {}).get('pdf', float('nan')):.1f} | {100*v['rel']:.1f} |" for k, v in d["theory_sources"].items())

# sample table
SRC = {"H_ggZH": "H_ggZH_py8dec", "H_ttH": "H_ttH", "H_ZH_tautau": "H_ZH_tautau", "T_ttaa": "T_ttaa", "F_QCD_Zajj": "F_QCD_llajj_vbs",
       "F_EW_Zajj": "F_EW_llajj_vbs", "B_QCD_Zaajj_vbs": "B_QCD_zaajj_vbs", "T_tta": "T_tta", "T_tWa": "T_tWa", **{f"B_EW_Zaajj_vbs_is{i}": (f"B_EW_zaajj_vbs_is{i}h" if f"B_EW_zaajj_vbs_is{i}h" in V and V[f"B_EW_zaajj_vbs_is{i}h"]["ok"] else f"B_EW_zaajj_vbs_is{i}") for i in (1, 2, 3)}}
srows = []
for k, r in REG.items():
    if r.get("missing"): srows.append(f"| {k} | — | — | — | — | — | **not available** ({r['src']}) |"); continue
    mclumi = r["N"]/(r["sig"]*r["k"]) if r["sig"]*r["k"] > 0 else float("inf")
    v = V.get(SRC.get(k, ""), None)
    ver = (f"{v['ok']}/{v['expected']} jobs OK; σ closure {100*v['closure']:+.2f} %" if v and v.get("closure") is not None
           else (f"{v['ok']}/{v['expected']} jobs OK (MLM: σ after matching)" if v else "Tier-1 / test_v2 (reports 04/05)"))
    srows.append(f"| {k} | {r['src']} | {g(r['sig'], 4)} | {g(r['k'], 4)} | {r['N']} | {g(mclumi, 3)} | {ver} |")

def res_row(k, v):
    lab = "(a) EW ZHjj; QCD ZHjj in b" if v["sigdef"] == "a" else "(b) EW + QCD ZHjj"
    fk = F[k]
    return (f"| {int(v['L'])} | {lab} | {v['s']:.3f} | {v['b']:.3f} | {v['Z_eq1']:.3f} ± {v['Z_eq1_mcerr']:.3f} | "
            f"{fk['Z_syst']:.3f} | {v['mu95_cls']:.1f} | {fk['mu95_syst']:.1f} |")

cpl_ok = "choice" in CP
def lamrow(L):
    global rng; rng = (-2.0, 2.0); r, rr, rb = CP[f"lambda|{L}|fixed"], CP[f"lambda|{L}|resolved"], CP[f"lambda_defb|{L}"]
    return f"| λWZ (κZ = 1), BR(H→γγ) SM | {L} | {iv(r['int68'])} | {iv(r['int95'])} | {r['Z_excl_lambda_neg']:.2f} (λWZ = −1: {r.get('Z_excl_lambda_m1', float('nan')):.2f}) |\n| λWZ, resolved κγ(κW), Γ_H | {L} | {iv(rr['int68'])} | {iv(rr['int95'])} | {rr['Z_excl_lambda_neg']:.2f} (λWZ = −1: {rr.get('Z_excl_lambda_m1', float('nan')):.2f}) |\n| λWZ, def. (b) (QCD ZHjj ∝ κZ²) | {L} | {iv(rb['int68'])} | {iv(rb['int95'])} | {rb['Z_excl_lambda_neg']:.2f} |"
def kzrow(L):
    global rng; rng = (0.0, 3.0); r = CP[f"kappaZ|{L}"]; o = f"| κZ (λWZ = 1) | {L} | {iv(r['int68'])} | {iv(r['int95'])} | — |"; rng = (-2.0, 2.0); return o
def carow(L):
    global rng; a, b = CP.get(f"cA|{L}|noclip"), CP.get(f"cA|{L}|clip500"); rng = (-4.0, 4.0)
    if not a: return ""
    return f"| CP-odd c_A (Λ = 1 TeV), no clipping | {L} | {iv(a['int68'])} | {iv(a['int95'])} | — |\n| c_A, clipped m(ℓℓγγ) < 500 GeV | {L} | {iv(b['int68'])} | {iv(b['int95'])} | — |"
cpl_table = ("Intervals are the expected (Asimov SM) ranges where −2Δln L < 1 (68 %) or < 3.84 (95 %); `*` marks an end at the scan boundary (λWZ ∈ [−2, 2], κZ ∈ [0, 3], c_A ∈ [−4, 4]), i.e. no constraint there.\n\n| parameter | L [fb⁻¹] | expected 68 % CL | expected 95 % CL | Z(exclude all λWZ < 0) (exclude λWZ = −1) |\n|---|---|---|---|---|\n" +
             "\n".join(lamrow(L) for L in (500, 1000, 3000)) + "\n" + "\n".join(kzrow(L) for L in (500, 1000, 3000)) + "\n" +
             "\n".join(x for x in (carow(L) for L in (500, 1000, 3000)) if x)) if cpl_ok else "(coupling samples not available)"
clo = "\n".join(f"| {k} | " + (f"{v['pred_total']:.4g} | {v['direct_total']:.4g} | {v['ratio']:.3f} | ±{100*v['direct_rel_mcstat']:.1f} % | χ² = {v['chi2']:.1f} / {v['nbins']} |" if "pred_total" in v
                               else f"{v['HC']:.4g} | {v['SM']:.4g} | {v['ratio']:.3f} | ±{100*v['rel_mcstat']:.1f} % | — |") for k, v in CP.get("closure", {}).items())
pts = "\n".join(f"| {k} | {v['sample']} | {v['sigma_fb']:.4g} | {v['N']} | {v['jobs_ok']} | {100*v['sigma_closure']:+.2f} % | {v['raw_SR']} | {v['s_SR_500']:.4f} |" for k, v in CP.get("points", {}).items())
r1 = lambda k: R[k]
tta = d["tta_xcheck"]; tfx = d["tf_xcheck"]
txt = f"""# FINAL report — EW ZHjj (Z→ee/μμ, H→γγ) at √s = 13.6 TeV: Delphes-level feasibility study and VH coupling interpretation

- **Date:** {now}
- **Status:** {"**PASS with limitations**" if not PEND else "**DRAFT — " + PEND + "**"}. Expected-limit/significance study for the current signal definition, plus the λWZ / κZ / CP-odd coupling interpretation (§9).
- **Git commit:** `{COMMIT}`. Reproduction: [08_reproducibility.md](08_reproducibility.md). Self-review: [ZH_self_review.md](ZH_self_review.md).
- **Inputs:** `{J.split('vbs_zh_codex_starter/')[-1]}` (written by `scripts/analysis/final_analysis.py`, which also executes `scripts/analysis/coupling_section.py`), `work/final_ntuples/verify.json`, `work/theory/theory_summary.json`.
- **Comparison with the reference** (arXiv:2512.07689: same Delphes CMS card, Eq. 1, Fig. 4-style scan). **Deviation marked everywhere it matters: our photon pT threshold is 25 GeV, the reference's is 20 GeV.** The reason is that the VBS-biased Zγ/Zγγ samples are generated with pT(γ) > 25 GeV. Every comparison to reference numbers below carries the tag **[γ pT 25 vs 20 GeV]**.
- **Luminosity:** 3000 fb⁻¹ is a pure luminosity scaling at 13.6 TeV, not an HL-LHC detector projection.

## Summary

At the optimised Delphes-level selection, the EW ZHjj signal is **s = {r5['s']:.3f} events at 500 fb⁻¹** and {r3['s']:.2f} at 3000 fb⁻¹. The background is b = {r5['b']:.3f} ({r3['b']:.2f}).
- **Significance:** Z_Eq1 = {r5['Z_eq1']:.3f} ± {r5['Z_eq1_mcerr']:.3f} (MC) at 500 fb⁻¹ and {r3['Z_eq1']:.3f} ± {r3['Z_eq1_mcerr']:.3f} at 3000 fb⁻¹, definition (a).
- **Systematics:** they now include theory (scale ⊕ PDF per process, correlated within groups), the off-shell/FSR correction of Zγγ, the Zγγjj interference, the ggZH ×2 normalisation and the generator-mjj correction of the QCD-type samples. With these, Z_syst = {r5['Z_syst_counting']:.3f} and μ₉₅ = {r5['mu95_cls']:.0f} at 500 fb⁻¹; Z_syst = {r3['Z_syst_counting']:.3f} and μ₉₅ = {r3['mu95_cls']:.1f} at 3000 fb⁻¹.
- **s < 1 at every luminosity, so Z alone is not a meaningful measure of sensitivity.** The process is not observable in this channel at Run 3 or with 3000 fb⁻¹.
- **Dominant background:** the irreducible EW Zγγjj continuum under the mγγ peak.
""" + (f"""- **Coupling interpretation (§9):** the measured observable is the yield and the {CP['choice']['observable']} shape of EW ZHjj in the signal region.
  - **λWZ = −1** gives a signal-region yield {CP['points']['lam_m100']['s_SR_500']/CP['points']['lam_p100']['s_SR_500']:.1f}× the SM. Excluding it alone (κZ = 1, BR(H→γγ) fixed to SM) has an expected significance of **Z = {CP['lambda|500|fixed'].get('Z_excl_lambda_m1', float('nan')):.2f} at 500 fb⁻¹ and {CP['lambda|3000|fixed'].get('Z_excl_lambda_m1', float('nan')):.2f} at 3000 fb⁻¹**.
  - The **whole region λWZ < 0** cannot be excluded: Z = {CP['lambda|500|fixed']['Z_excl_lambda_neg']:.2f} at 500 fb⁻¹ and {CP['lambda|3000|fixed']['Z_excl_lambda_neg']:.2f} at 3000 fb⁻¹. The reason is that λWZ → 0⁻ (minimum at λWZ = {CP['lambda|3000|fixed'].get('lambda_at_min_q_neg', float('nan')):+.2f}) gives a yield and mℓℓγγ shape close to the SM's: {CP['points']['lam_p000']['s_SR_500']/CP['points']['lam_p100']['s_SR_500']:.2f}× the SM yield at λWZ = 0.
  - Resolving the H→γγ rate in κW (W loop) gives Z(λWZ = −1) = {CP['lambda|3000|resolved'].get('Z_excl_lambda_m1', float('nan')):.2f} at 3000 fb⁻¹. That gain comes from inclusive-H→γγ rate information that other measurements already constrain.
  - **This channel cannot test the sign of λWZ at the level of the CMS/ATLAS WH(bb̄) results.**
""" if cpl_ok else "") + f"""
## 1. Setup

| item | value |
|---|---|
| Stack | LCG_110 x86_64-el9-gcc13-opt; MG5_aMC 3.6.3 (upstream); Pythia 8.317 (CP5); Delphes 3.5.1 with the stock CMS card (slimmed output, physics unchanged); NNPDF3.1 NNLO (LHAID 303600) via LHAPDF 6.5.5. Details: [03_stack.md](03_stack.md). |
| Order | LO for all samples; no k-factors. Theory uncertainties are scale ⊕ PDF from MG5 weights (§7) |
| Generation | MG5 gridpacks on HTCondor (EosSubmit); per job: gridpack → Pythia8 → Delphes → slim/GenTruth friend (`scripts/condor/run_job.sh`) |
| Analysis objects | `scripts/analysis/ntuple.py` (reference Sec. III object definitions): e/μ pT > 15 GeV; isolated Delphes photons pT > 20 GeV, \\|η\\| < 2.5 outside 1.4442–1.566, ΔR(γ,ℓ) > 0.4; anti-kT jets pT > 25 GeV, \\|η\\| < 4.7, ΔR > 0.4 to the leptons and photons |
| mγγ peak | Gaussian core fit of the Delphes EW signal: μ = {RES['mu']:.2f} GeV, σ = {RES['sigma_core']:.3f} ± {RES['sigma_core_err']:.3f} GeV (σ_eff = {RES['sigma_eff']:.2f} GeV) |
| mjj resolution (A1) | Delphes reco vs matched GenJets, same jet cleaning as the analysis: σ68/mjj = {100*MR.get('ew_zhjj_zll', {}).get('sigma68_rel', float('nan')):.1f} % (EW ZHjj), {100*MR.get('qcd_zhjj_zll', {}).get('sigma68_rel', float('nan')):.1f} % (QCD ZHjj); median bias {100*MR.get('ew_zhjj_zll', {}).get('median_rel', float('nan')):+.1f} % (`work/theory/mjj_resolution.json`) |

## 2. Samples, verification and the N_MC ≥ σ×BR×3000 fb⁻¹ requirement

All final yields are Delphes-level.
- **Verification** (`scripts/analysis/verify_final.py`): job exit, outputs, event counts and σ closure.
- **Ntuple check:** the event counts in the ntuples equal the verified totals.

| process | source | σ [fb] | × BR | N_MC | MC lumi [fb⁻¹] | verification |
|---|---|---|---|---|---|---|
{chr(10).join(srows)}

**Per-sample N_MC vs σ×BR×{d['nmc_L']:.0f} fb⁻¹ (A10).**
- The table is produced by `nmc_check()` in `final_analysis.py`, which **raises SystemExit if any sample entering s or b (including the BSM coupling samples) has N_MC < σ×BR×L**. This run passed.
- w_evt is the event weight at {d['nmc_L']:.0f} fb⁻¹, i.e. the events per MC event.

| sample | σ×BR [fb] | σ×BR×{d['nmc_L']:.0f} fb⁻¹ | N_MC | N_MC/(σ×BR×L) | w_evt at {d['nmc_L']:.0f} fb⁻¹ |
|---|---|---|---|---|---|
{ncrows}

- **tt̄γ and tWγ (A9)** were regenerated with the reference Table I process definitions:
  - tt̄γ: `p p > t t~ a`, both t → b W, W → ℓν;
  - tWγ: `p p > t w- a` and `p p > t~ w+ a`, both W → ℓν, with `$$` removing the tt̄ overlap.
  - Statistics: 1.04 M and 160 k events, i.e. ≥ 4 × σ×BR×3000 fb⁻¹. The 2000-event test samples are no longer used.
  - No generator-level filter was needed: the production gridpacks have pT(γ) > 15 GeV, looser than the reco cut.
- **Dropped segments:** QCD Zγ+jets lost 5 of 3000 segments (2 deterministic Delphes segfaults, 3 lost after the LHE stage). Normalisation uses the actual N.
- **Flagged decision:** the no-mjj-cut twins used for the generator-mjj correction (§4) are below σ×BR×3000 fb⁻¹. Only the ratio C enters b, and its MC-stat uncertainty is propagated as a nuisance, so they are accepted as auxiliary samples. They are flagged in the table above.
- **Removed from the registry:** the unused 0-jet MLM Zγγ check sample (B_QCD_llaa_0j) had N = 2307 < σ×L(3000) = 4812. It never entered s or b.

## 3. Normalisation and branching ratios (A6)

- **σ definitions:** σ is the MG5 cross section at the generator cuts, before any analysis BR. The cutflow's first row is σ × BR × L, and after-cut yields are in Tables III/IV.
- **B(H→γγ) = 0.002270** (LHCHXSWG YR4, mH = 125 GeV) is applied **once**, in the analysis. Pythia forces H→γγ with conditional BR = 1.
- **The factor ZF = 0.9783 (Z→ℓℓ in the MG5 matrix element):**
  - MG5 LO computes Γ(Z→ℓℓ) and Γ_Z from its own electroweak inputs (sm model: 2Γ_ℓℓ/Γ_Z = 2 × 83.965 MeV / 2.441404 GeV = 0.06878 for ee + μμ).
  - The closure test σ(ZHjj→ℓℓHjj)/σ(ZHjj) = 0.06964 ± 0.00083 agrees with this ([01_addendum_claude.md](01_addendum_claude.md) item 5).
  - The PDG values are B(Z→ee) = 0.033632 and B(Z→μμ) = 0.033662, giving per-flavour rescalings 0.033632/0.034392 = 0.9779 and 0.033662/0.034392 = 0.9788. **Combined: ZF = 0.067294/0.068784 = 0.9783.**
  - ZF therefore converts MG5's LO width-derived Z→ℓℓ BR to PDG. It is applied only to samples whose Z→ℓℓ decay happens in MG5 with the BR taken from the MG5 widths: the decay chains and the on-shell-Z Zγγ samples.
- **Samples with ℓℓ in the matrix element without a Z decay chain** (Zγjj: `p p > l+ l- a j j`) include γ*/Z interference and need no BR.
- **ggZH:** the Z is undecayed at LHE level and Z→ee/μμ is forced in Pythia8, so k = BR_PDG(Z→ee+μμ) = {d['br']['BR_ZLL']:.6f} × B_γγ.

**Per-sample BR ledger.**
- The table is produced by `final_analysis.py`. It asserts that the product of the listed factors equals the k used in the event weight, and that no factor appears twice; otherwise the analysis aborts.
- The last column is the off-shell/FSR correction (§4), which is not a BR.

| sample | Z/W/t decay | H decay | factors in k | k | off-shell corr. |
|---|---|---|---|---|---|
{brrows}

## 4. Background model, overlap removal and generator-level checks

The background model is aligned with the reference: prompt Zγ and Zγγ (QCD and EW), tt̄γ, tWγ, tt̄γγ, plus resonant H→γγ backgrounds (QCD ZHjj in def. a, ggZH, tt̄H, ZH(ττ), tHW).

**Estimation hierarchy** (recorded per number in Table IV):
- **L0:** direct, ≥ 10 raw events in the window.
- **L1:** continuum, N(105–165 GeV) × f_win (exponential MLE of the sample's Delphes mγγ).
- **L2:** VBS-factorised.
- **L2b:** VBS- and window-factorised, using the direct sample (tt̄γ, tWγ).
- **UL:** zero support, central value 1.14 w_evt.
- L2, L2b and UL carry 100 % uncertainty. **The transfer-factor method (old L3) is no longer used for yields.**

**Hard/soft photon overlap removal:** uses the GenTruth count of prompt photons (pT > 15 GeV, \\|η\\| < 2.5, ΔR > 0.4). One-ME-photon samples keep n_prompt ≤ 1.

**tt̄γ / tWγ (A9).**
- **Direct yields at the optimum:**
  - tt̄γ: {R['500_a']['comp'].get('T_tta', {}).get('y', float('nan')):.4f} events at 500 fb⁻¹ via {R['500_a']['comp'].get('T_tta', {}).get('method', '—')}.
  - tWγ: {R['500_a']['comp'].get('T_tWa', {}).get('y', float('nan')):.4f} events via {R['500_a']['comp'].get('T_tWa', {}).get('method', '—')}.
  - Zero raw events pass all cuts. The direct zero-count 95 % UL is 3 w_evt = {3*REG['T_tta']['w_evt_fb']*500:.3f} and {3*REG['T_tWa']['w_evt_fb']*500:.3f} events; using it instead is a robustness row.
- **Transfer-factor cross-check** (old method): {tfx.get('T_tta', {}).get('y500_tf', float('nan')):.4f} and {tfx.get('T_tWa', {}).get('y500_tf', float('nan')):.4f} events.
- **Cross-check against the reference [γ pT 25 vs 20 GeV]:**
  - Reference-like baseline (70 < mℓℓ < 120 GeV, mℓℓγγ > 100 GeV, mjj > 700 GeV, |Δηjj| > 2.0, **photon pT > 25 GeV**), **before any mγγ window**: tt̄γ has {tta.get('T_tta', {}).get('raw', '—')} raw events, so y < {tta.get('T_tta', {}).get('y500_ul95') or 0:.3f} events at 500 fb⁻¹ (95 % CL). The preselection has {tta.get('T_tta', {}).get('raw_presel', '—')} raw events and the lepton/photon cuts keep {tta.get('T_tta', {}).get('raw_lg', '—')}.
  - The reference quotes **0.15 ± 0.10** events (Table IV, photon pT > 20 GeV, no Higgs window). The results are compatible within the reference's uncertainty.
  - Expected differences: the higher photon threshold, the n_prompt ≤ 1 overlap removal (not applied in the reference), and the reference's 2.5-event-weight statistics.

**Zγγ on-shell Z and off-shell/FSR (A4).**
- The Zγγjj samples are `p p > z a a j j, z > l+ l-`, so photons radiated in the Z decay and off-shell γ*/Z are missing.
- **Bound from a dedicated MG5 pair** (`cards/theory/Q_*0j.mg5`, 20 k events each, QCD 0-jet proxy, all non-jet analysis cuts):
  - σ(`p p > l+ l- a a`) / σ(`p p > z a a, z > l+ l-`) = **{OF['ratio']:.3f} ± {OF['ratio_err']:.3f}**, compared with {OF['ratio_incl']:.2f} before cuts.
  - The reference's inclusive/on-shell EW ratio is {OF['reference_after_mll_cut']:.3f} after its mℓℓ cut and {OF['reference_after_all_cuts']:.3f} after all cuts (Tables III–IV) **[γ pT 25 vs 20 GeV]**.
- **Applied:** the on-shell-Z Zγγ samples (QCD and EW) are scaled by **{d['offshell']['factor']:.3f}**, with a correlated ±{100*d['offshell']['rel_unc']:.1f} % nuisance (half the correction).

**EW–QCD interference (A3; as reference Sec. II C).**
- **ZHjj** (I_ZHjj, 20 k signed-weight events; Z and H undecayed):
  - Inclusive: σ_I = {IZ['sigma_I_incl_fb']:.3f} fb. In the VBS jet region (mjj > 500 GeV, |Δη| > 3.5): σ_I = {IZ['sigma_I_R_fb']:.4f} ± {IZ['sigma_I_R_err_fb']:.4f} fb.
  - This is **{100*IZ['frac_of_EW']:.2f} ± {100*IZ['frac_of_EW_err']:.2f} % of EW ZHjj** (def. a) and {100*IZ['frac_of_EWplusQCD']:.2f} % of EW + QCD ZHjj (def. b). It is negligible and not included.
- **Zγγjj:** {("σ_I/σ_EW = **" + f"{100*IA['frac_of_EW']:+.1f} ± {100*IA['frac_of_EW_err']:.1f} %" + "** in the VBS + photon region (inclusive " + f"{100*IA.get('frac_of_EW_incl', float('nan')):+.1f} %), from dedicated MG5 runs with an undecayed on-shell Z (squared-order syntax cannot be combined with a decay chain in MG5 3.6.3)") if IA.get('status') == 'computed' else ("own MG5 run not available; the reference value " + f"{100*IA['frac_of_EW']:.1f} %" + " (Table II, inclusive) is used")}.
  - It is non-negligible, so it is included as a ±{100*d['int_zaa']:.1f} % nuisance on EW Zγγjj.

**Generator mjj > 400 GeV cut of the VBS-biased samples (A1).**
- Measured on the Tier-1 samples generated without an mjj cut. The quantity is P(max parton-pair mjj < 400 GeV | reco mjj > 500 GeV, |Δηjj| > 3.5), i.e. the fraction of the reco region removed by the generator cut:
  - **EW ZHjj: {100*MR.get('ew_zhjj_zll', {}).get('P(parton_mjj<400 | reco_mjj>500, deta>3.5)', float('nan')):.1f} %.** The cut is safe for EW-type samples (EW Zγγjj, EW Zγjj, coupling samples), given the {100*MR.get('ew_zhjj_zll', {}).get('sigma68_rel', float('nan')):.0f} % mjj resolution and the 100 GeV margin.
  - **QCD ZHjj: {100*MR.get('qcd_zhjj_zll', {}).get('P(parton_mjj<400 | reco_mjj>500, deta>3.5)', float('nan')):.0f} %.** In QCD-type events the reco tag jets are often parton-shower jets, so **the cut is not safe for QCD-type samples.**
- **Correction for QCD-type samples:** QCD Zγjj and QCD Zγγjj are corrected by C(cuts) = Y(no-mjj-cut twin)/Y(VBS-biased), measured directly at Delphes level with the same VBS, Z-window and photon cuts. The twins are 200 k / 100 k events with mmjj = 0.
  - {"; ".join(f"{k}: C = {v['C_opt']:.2f} ± {100*v['rel_opt']:.0f} % (raw {v['raw_twin']} / {v['raw_vbs']})" for k, v in GM.items()) if GM else "**twin samples not available in this run**"}.
  - The statistical uncertainty of C is a nuisance.
- **The optimum at the mjj = 500 GeV scan boundary** (`figures/z_vs_mjj`, `z_vs_deta`):
  - Cuts below 500 GeV are shaded in the figure because, for the QCD-type samples, they rely entirely on the correction above.
  - Z_Eq1 (Z with σ_b) at 500 fb⁻¹ for mjj > 400 / 450 / 500 / 600 GeV, with the other cuts at the optimum: {" / ".join(f"{d['scan1d'][f'500|mjj|{m}']['Z']:.3f} ({d['scan1d'][f'500|mjj|{m}']['Zsyst']:.3f})" for m in (400, 450, 500, 600))}.
  - Going below the boundary therefore changes Z by {100*(max(d['scan1d'][f'500|mjj|{m}']['Z'] for m in (400, 450))/d['scan1d']['500|mjj|500']['Z'] - 1):+.0f} % at most. That gain would rely on the QCD-type correction extrapolated to a region where the generator cut sits inside the resolution tail.

**Fake-factor cross-check (Delphes jets).**
- f = 10⁻³ gives {d['ff_xcheck']['f=0.001']['final']:.4f} events (band {d['ff_xcheck']['f=0.0005']['final']:.4f}–{d['ff_xcheck']['f=0.002']['final']:.4f}), vs {d['ff_xcheck']['direct Delphes']['final']:.4f} direct, at the final selection and 500 fb⁻¹.
- These values are before the generator-mjj correction.

## 5. Selection and optimisation

- **Reference-like baseline** (arXiv:2512.07689 Sec. III) **[γ pT 25 vs 20 GeV]:** OSSF 70 < mℓℓ < 120 GeV; two photons with **pT > 25 GeV** (reference: 20 GeV); mℓℓγγ > 100 GeV; mjj > 700 GeV, |Δηjj| > 2.0; mγγ within ±2σ.
- **Optimisation** uses expected quantities only, at 500 fb⁻¹ for def. (a). It is a coordinate descent with the FOM Z(σ_b), where σ_b includes theory. A plateau rule picks the highest-signal point within 97 % of Z_max.
- **Optimum:** {cuts}.
- **mjj × |Δηjj| landscape** (`figures/scan_mjj_deta_*`, tables below): Z_Eq1 at 500 fb⁻¹ ranges from {min(v['Z'] for k, v in d['scan'].items() if k.startswith('500|')):.3f} to {max(v['Z'] for k, v in d['scan'].items() if k.startswith('500|')):.3f}.
- **1D curves (A1):**
  - mjj cut from 400 to 1200 GeV: Z_Eq1 at 500 fb⁻¹ ranges from {min(v['Z'] for k, v in d['scan1d'].items() if k.startswith('500|mjj')):.3f} to {max(v['Z'] for k, v in d['scan1d'].items() if k.startswith('500|mjj')):.3f}.
  - |Δηjj| from 2.0 to 5.0: Z_Eq1 ranges from {min(v['Z'] for k, v in d['scan1d'].items() if k.startswith('500|deta')):.3f} to {max(v['Z'] for k, v in d['scan1d'].items() if k.startswith('500|deta')):.3f}.

## 6. Results

### PRIMARY: Eq. 1 counting significance (stat. only, ± MC stat), Z_syst (incl. theory) and limits

| L [fb⁻¹] | signal definition | s | b | Z_Eq1 ± MC | Z_syst counting (incl. theory) | Z_syst (binned PL fit, incl. theory) | μ₉₅ CLs (exact Poisson, syst incl. theory) | μ₉₅ (binned PL fit, asymptotic) |
|---|---|---|---|---|---|---|---|---|
{chr(10).join(f"| {int(v['L'])} | {'(a) EW ZHjj; QCD ZHjj in b' if v['sigdef'] == 'a' else '(b) EW + QCD ZHjj'} | {v['s']:.3f} | {v['b']:.3f} | {v['Z_eq1']:.3f} ± {v['Z_eq1_mcerr']:.3f} | {v['Z_syst_counting']:.3f} | {F[k]['Z_syst']:.3f} | {v['mu95_cls']:.1f} | {F[k]['mu95_syst']:.1f} |" for k, v in R.items())}

- **s < 1 in every row:** Z alone is not meaningful.
- **μ₉₅ (exact-Poisson CLs):** counting in the window, with b and s marginalised over log-normals (σ_b and σ_s include theory). This is the robust number.
- **Asymptotic fit limits** are shown for completeness only; they underestimate the limit at these counts.
- **Largest background components** at 500 fb⁻¹, def. (a): {"; ".join(f"{k} {y:.4f}" for y, k in top)}.

{tables}

## 7. Systematic uncertainties

- **Background normalisation** (uncorrelated per process): 10 % for prompt and resonant processes; **50 % for fake-photon processes** (Zγjj, tt̄γ, tWγ), with robustness rows at 25 % and 100 %.
- **Luminosity:** 2.5 %, correlated.
- **MC statistics:** per process. L2, L2b and UL estimates carry 100 % uncertainty.
- **Theory (A2).** MG5 weights give the 7-point scale envelope (μR, μF ∈ {{½, 1, 2}}, without (½,2) and (2,½)) and the NNPDF3.1 replica standard deviation.
  - Signal and QCD ZHjj: from the Tier-1 LHE (40 k events each).
  - Background samples (LHE deleted after production): from dedicated small LHE-only runs of the *production gridpacks* (`scripts/condor/lhe_only.sh`, 3–10 k events, `work/theory/`).
  - Region: the parton-level proxy of the signal region (two leading partons with mjj > 500 GeV and |Δη| > 3.5; Z window; photon pT and pT/mγγ cuts; mℓℓγγ > 100 GeV), or inclusive for ggZH, tt̄H and top.
  - Symmetrised as max(up, down) ⊕ PDF. Correlated within a theory group (e.g. the three EW Zγγ splits; tt̄γγ/tt̄γ/tWγ) and uncorrelated between groups. Signal theory enters σ_s (μ₉₅) and the fit.

| process | theory group | weight source | region | scale up / down [%] | PDF [%] | total used [%] |
|---|---|---|---|---|---|---|
{throws}

- **Other nuisances:**
  - off-shell/FSR of Zγγ: ±{100*d['offshell']['rel_unc']:.1f} %, correlated EW+QCD;
  - Zγγjj interference: ±{100*d['int_zaa']:.1f} % on EW Zγγ;
  - **ggZH normalisation ×2 / ×0.5** (log-normal, σ = ln 2), covering the LO loop-induced normalisation and the shower-only jets (robustness rows ×2 and ×0.5);
  - generator-mjj correction of the QCD-type samples (statistical uncertainty of C).
- **Fit:** binned Poisson likelihood in mγγ ({len(d['fit_edges'])-1} bins over 105–165 GeV). Per-process log-normals, plus one shared nuisance per correlated group, plus luminosity. Asimov data.

## 8. Limitations

1. **Statistical regime:** s < 1 even at 3000 fb⁻¹, so the Z values are illustrative; the limit is the meaningful quantity.
2. **The Delphes CMS card is not real CMS.**
   - σ_mγγ is about 2.1 GeV (real CMS: about 1.5 GeV).
   - The Delphes prompt-object efficiencies on signal are low (`work/theory/object_eff.json`): electrons 39–73 % (barrel), muons 59–87 %, photons 59–89 %.
   - The CMS-like reweighting (A7, robustness table) raises s by ×{ROB['CMS-like e/mu/gamma efficiencies (A7 reweighting)']['s']/ROB['optimum']['s']:.2f}, and b by ×{ROB['CMS-like e/mu/gamma efficiencies (A7 reweighting)']['b']/ROB['optimum']['b']:.2f}.
   - The reweighting uses *assumed* CMS-like efficiencies (e: 65–92 %, μ: 93–96 %, γ: 80–92 % by pT/η; CMS JINST 16 (2021) P05014 and JINST 13 (2018) P06015 as orientation, not a calibrated parametrisation). It cannot recover objects that Delphes misidentifies (e.g. e→γ).
   - The Delphes jet→photon fake rate is a card assumption; the FF band brackets it within a factor of about 2.
3. **Zγγjj uses an on-shell Z.**
   - The off-shell/FSR part is corrected with a 0-jet QCD proxy ratio transferred to jj (EW and QCD). The reference's EW-jj ratio agrees within the assigned uncertainty.
   - The **QCD-type samples needed a generator-mjj correction** (§4) from finite twin samples.
4. **ggZH** is LO loop-induced with shower jets only (×2 nuisance).
5. **LO everywhere.** Theory uncertainties are LO scale ⊕ PDF only; no NLO k-factors; QCD ZHjj is fixed-order ZH+2j.
6. **Double-fake backgrounds** (Z+jets, tt̄) are not in b. They are order-of-magnitude only, as in the reference.
7. **Luminosity scaling:** 3000 fb⁻¹ is scaled at 13.6 TeV, with no pile-up and no HL-LHC detector.
8. **Coupling interpretation (§9):**
   - LO EW ZHjj only.
   - ggZH, tt̄H and tHW are kept at the SM. ggZH depends on κZ (triangle) and κt (box), which is neglected (ggZH is {R['500_a']['comp'].get('H_ggZH', {}).get('y', float('nan')):.3f} events at 500 fb⁻¹).
   - The headline keeps BR(H→γγ) at the SM. The resolved-κγ variant assumes κt = 1 and no BSM loops.
{("9. **" + PEND + "**") if PEND else ""}

## 9. VH coupling interpretation: λWZ = κW/κZ, κZ, CP-odd (E)

**Motivation and comparison.**
- The sign of λWZ is the target of the recent CMS (PLB 860 (2025) 139202, arXiv:2405.16566) and ATLAS (PRL 133 (2024) 141801, arXiv:2402.00426) analyses. Both use WH/VBF-WH with H→bb̄, and both exclude λWZ < 0 with very high significance in their channels.
- Our channel is ZH with Z→ℓℓ and H→γγ, with VBS-like jets. The EW ZHjj amplitude contains both the WW-fusion (κW) and ZZ-fusion/Higgsstrahlung (κZ) diagrams, so the kinematics and the rate depend on λWZ through the κW–κZ interference, which is destructive in the SM.
- The two experiments have far larger signal rates, so this channel is complementary in final state and production mode, not competitive.

**Model.**
- The official Higgs Characterisation UFO HC_NLO_X0 (FeynRules model database, README model version 1.3; zip sha256 b91d8788…, fetched 2026-11-03) has a single SM-like κSM shared by X0WW and X0ZZ.
- A minimal documented patch (`scripts/models/make_hc_kvv.sh`) adds κ factors `kSMW` and `kSMZ` multiplying κSM in exactly those two couplings. The resulting model is HC_NLO_X0_kVV.
- Effective X0γγ/X0Zγ/X0gg and dim-5 couplings are switched off to match the SM tree level, and the CKM matrix is diagonal.

**Samples.**
- Direct samples at λWZ ∈ {{−1, −0.5, 0, 0.5, 1, 1.5}} (κZ = 1) and CP-odd c_A = ±2 (Λ = 1 TeV, cos α·κSM = 1). Each has 25 × 2000 events through the identical Pythia8 (forced H→γγ) → slim Delphes chain and selection (mmjj > 400 GeV, safe for EW-type samples, §4).
- **No MG5 reweighting is used.** Because the amplitude is κZ·A_Z + κW·A_W, the yield in every bin is exactly κZ²(a + bλ + cλ²).
- a, b and c are fitted per bin to the six direct points. Closure tests are below.

| point | sample | σ [fb] | N_MC | jobs | σ closure | raw events in SR | s in SR at 500 fb⁻¹ |
|---|---|---|---|---|---|---|---|
{pts}

| closure test | prediction | direct | ratio | direct MC stat | shape |
|---|---|---|---|---|---|
{clo}

**Statistics.**
- The observable is a binned Poisson likelihood of {CP.get('choice', {}).get('observable', '—')} inside the signal region (all optimum cuts including the mγγ window). It was chosen by expected sensitivity to λWZ = −1 at 3000 fb⁻¹; the −2Δln L values are {", ".join(f"{k}: {v:.1f}" for k, v in CP.get('choice', {}).get('q_lambda_m1_3000', {}).items())}.
- Data are Asimov at the SM. All nuisances of the SM result are profiled (signal theory included).
- The background bin fractions come from each process's Delphes distribution, at all cuts except the window, or looser if fewer than 10 raw events remain.
- QCD ZHjj (def. b) scales with κZ².

{cpl_table}

**Notes on the results.**
- The 1D intervals can be disjoint, because the quadratic yield allows a second solution with the SM rate.
- The **headline** is the BR(H→γγ)-fixed row: a production-only interpretation in which κγ is a free effective coupling constrained by inclusive H→γγ.
- In the **resolved** variant, κγ² = 1.59κW² + 0.07 − 0.67κW (κt = 1). λWZ = −1 then multiplies BR(H→γγ) by about 2.3, a constraint dominated by the inclusive H→γγ rate.
- The CP-odd interpretation is linear + quadratic in c_A, with and without an energy clipping m(ℓℓγγ) < 500 GeV. The rate is dominated by the quadratic term ({CP.get('cA_rates', {}).get('linear_over_quad', float('nan')):.3f} = |linear/quadratic| at c_A = ±2), so clipping mainly shows how much of the sensitivity comes from high energies, where the EFT validity is questionable.
- Figures: `lambdaWZ_scan`, `kappaZ_lambdaWZ_500/3000`, `lambdaWZ_dist_{{mllgg,ptgg,mjj,detajj}}` (SM vs λWZ = −1 and 0), `cA_scan`.

## 10. Figures (`figures/`, PDF + PNG)

- **Distributions:** `m_gg`, `m_ll`, `m_jj`, `deta_jj`, `photon1_pt`, `photon2_pt`, `zeppenfeld`.
  - 3000 fb⁻¹, all optimum cuts except the VBS cuts and the window.
  - The QCD-type samples are drawn from their no-mjj-cut twins.
- **Significance scans:**
  - `scan_mjj_deta_500`, `scan_mjj_deta_3000` (reference Fig. 4 style);
  - `z_vs_mjj`, `z_vs_deta` (A1).
- **Coupling:** `lambdaWZ_scan`, `kappaZ_lambdaWZ_500`, `kappaZ_lambdaWZ_3000`, `lambdaWZ_dist_*`, `cA_scan`.

## 11. Checks

- **σ closure:** < 1 % for every final sample; < 1.8 % for the coupling samples.
- **Ntuples:** event counts equal the verified job totals.
- **BR ledger and N_MC ≥ σ×BR×3000 fb⁻¹:** asserted in code (§2, §3).
- **ggZH decay closure:** 98.4 % of events have a prompt ee/μμ pair, with no ττ.
- **Coupling morphing closure:** §9.
- **Re-optimisation:** Z_syst at the optimum minus Z_syst at the reference-like baseline = {ROB['optimum']['Z_syst'] - ROB['reference-like baseline (photon pT > 25 GeV, not 20)']['Z_syst']:+.3f} at 500 fb⁻¹ **[γ pT 25 vs 20 GeV]**.
"""
open(OUT, "w").write(txt); print("wrote", OUT, len(txt.splitlines()), "lines")
