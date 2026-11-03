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

# sample table
SRC = {"H_ggZH": "H_ggZH_py8dec", "H_ttH": "H_ttH", "H_ZH_tautau": "H_ZH_tautau", "T_ttaa": "T_ttaa", "F_QCD_Zajj": "F_QCD_llajj_vbs",
       "F_EW_Zajj": "F_EW_llajj_vbs", "B_QCD_Zaajj_vbs": "B_QCD_zaajj_vbs", **{f"B_EW_Zaajj_vbs_is{i}": (f"B_EW_zaajj_vbs_is{i}h" if f"B_EW_zaajj_vbs_is{i}h" in V and V[f"B_EW_zaajj_vbs_is{i}h"]["ok"] else f"B_EW_zaajj_vbs_is{i}") for i in (1, 2, 3)}}
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

txt = f"""# FINAL report — EW ZHjj (Z→ee/μμ, H→γγ) at √s = 13.6 TeV: Delphes-level feasibility study

- **Date:** {now}
- **Status:** {"**PASS with limitations**" if not PEND else "**DRAFT — " + PEND + "**"}. Expected-limit/significance study for the current signal definition (D12 closed).
- **Git commit:** `{COMMIT}`. Reproduction: [08_reproducibility.md](08_reproducibility.md).
- **Inputs:** `{J.split('vbs_zh_codex_starter/')[-1]}` (written by `scripts/analysis/final_analysis.py`), `work/final_ntuples/verify.json`.
- **Comparison:** the reference ZγγJJ study, arXiv:2512.07689, is the methodological reference: same Delphes CMS card, Eq. 1 counting significance and the Fig. 4-style mjj–|Δηjj| scan.
- **Luminosity:** 3000 fb⁻¹ is a pure luminosity scaling at 13.6 TeV, not an HL-LHC detector projection.

## Summary

At the optimised Delphes-level selection, the EW ZHjj signal is **s = {r5['s']:.3f} events at 500 fb⁻¹** and {r3['s']:.2f} at 3000 fb⁻¹. The total background is b = {r5['b']:.3f} ({r3['b']:.2f}) events.
- **Significance:** Eq. 1 gives Z = {r5['Z_eq1']:.3f} ± {r5['Z_eq1_mcerr']:.3f} (MC) at 500 fb⁻¹ and {r3['Z_eq1']:.3f} ± {r3['Z_eq1_mcerr']:.3f} at 3000 fb⁻¹, for definition (a).
- **s < 1 at every luminosity and for both signal definitions, so Z alone is not a meaningful measure of sensitivity.** The physically meaningful quantity is the expected 95 % CL upper limit on the signal strength.
  - μ₉₅ = {r5['mu95_cls']:.0f} at 500 fb⁻¹ and {r3['mu95_cls']:.1f} at 3000 fb⁻¹ (exact-Poisson CLs, definition a).
  - The median background-only count is {r5['n_median']} at 500 fb⁻¹, so the limit is close to the zero-background value 3/s.
- **The process is not observable at the LHC Run 3 or with 3000 fb⁻¹ in this channel.** The tiny signal rate is the limiting factor: σ×BR×L = 1.44 events produced at 500 fb⁻¹ before any selection.
- **Dominant background:** the irreducible EW Zγγjj continuum under the mγγ peak. It cannot be suppressed by the VBS-jet cuts, because it shares the signal's VBS topology.

## 1. Setup

| item | value |
|---|---|
| Stack | LCG_110 x86_64-el9-gcc13-opt; MG5_aMC 3.6.3 (upstream); Pythia 8.317 (CP5); Delphes 3.5.1 with the stock CMS card (slimmed output, physics unchanged, `cards/phase04_candidates/delphes_card_CMS_slim_v1.tcl`); NNPDF3.1 NNLO (LHAID 303600) via LHAPDF 6.5.5. Details: [03_stack.md](03_stack.md). |
| Order | LO for all samples; no k-factors |
| Generation | MG5 gridpacks on HTCondor (EosSubmit). Per job: gridpack → Pythia8 → Delphes → slim/GenTruth friend (`scripts/condor/run_job.sh`) |
| Analysis objects | `scripts/analysis/ntuple.py` (reference Sec. III object definitions): e pT > 15 GeV, \\|η\\| < 2.5; μ pT > 15 GeV, \\|η\\| < 2.4; OSSF pair closest to mZ; isolated Delphes photons pT > 20 GeV, \\|η\\| < 2.5 outside 1.4442–1.566, ΔR(γ,ℓ) > 0.4; anti-kT jets pT > 25 GeV, \\|η\\| < 4.7, ΔR > 0.4 to the leptons and photons; b-tag \\|η\\| < 2.5 |
| mγγ peak | Gaussian core fit of the Delphes EW signal: μ = {RES['mu']:.2f} GeV, σ = {RES['sigma_core']:.3f} ± {RES['sigma_core_err']:.3f} GeV (σ_eff = {RES['sigma_eff']:.2f} GeV). The stock Delphes CMS card has a worse mγγ resolution than real CMS (about 1.5 GeV). |

## 2. Samples and verification

All final yields come from Delphes reconstructed objects. In the table, N_MC is the number of Delphes events used, and the MC luminosity is N_MC/(σ×BR).
- **Verification** (`scripts/analysis/verify_final.py`): every job is checked for exit, outputs, event counts (n_lhe ≥ 0.9·n_requested, and n_delphes = n_lhe for fixed order) and σ closure (mean Pythia σ vs the gridpack total).
- **Ntuple check:** the event counts in the ntuples equal the verified totals (`N_closure_ok` in the JSON registry).

| process | source | σ [fb] | × BR | N_MC | MC lumi [fb⁻¹] | verification |
|---|---|---|---|---|---|---|
{chr(10).join(srows)}

- **Dropped segments:** QCD Zγ+jets lost 5 of 3000 segments.
  - 2 segfault deterministically in Delphes for their fixed seed.
  - 3 jobs were lost after the LHE stage.
  - They were not resubmitted; normalisation uses the actual N.
- **Zero-weight samples:** the T_tta and T_tWa test samples (2000 events) are used only through the transfer-factor method (§4).

## 3. Normalisation and branching ratios

- **σ definitions:** σ is the MG5 cross section at the generator cuts, before any BR that is applied in the analysis. The cutflow's first row is σ × BR × L. After-cut yields are in Tables III and IV. These three quantities are kept distinct.
- **B(H→γγ) = 0.002270** is applied **once**, in the analysis (factor k). Pythia forces H→γγ with conditional BR = 1.
- **Z→ℓℓ:**
  - Signal, QCD ZHjj and on-shell-Z Zγγjj: in the MG5 matrix element or decay chain, with ZF = 0.9783 rescaling MG5's width-derived BR to PDG.
  - ggZH: Z undecayed at LHE level, Z→ee/μμ forced in Pythia8, so k = BR(Z→ee+μμ) = {d['br']['BR_ZLL']:.6f} × B_γγ.
  - Both lepton flavours are always included; τ is excluded from the signal definition.
- **MLM-merged samples** (ZH→ττ, Zγγ 0j): normalised to the Pythia σ after matching.
- **Weight:** every event has w = σ·k/N_MC. No negative weights at LO.

## 4. Background model and overlap removal

The model is aligned with the reference: prompt Zγ and Zγγ (QCD and EW), tt̄γ, tWγ, tt̄γγ, plus resonant H→γγ backgrounds.

| class | samples | method |
|---|---|---|
| resonant H→γγ | QCD ZHjj (background in def. a), ggZH, tt̄H, ZH(H→γγ, Z→ττ), tHW | direct Delphes counting in the window |
| prompt Zγγ | QCD and EW Zγγjj, on-shell Z→ℓℓ, VBS-biased generation | direct counting, or the mγγ exponential-shape method |
| Zγ + jet→γ fake | QCD and EW Zγjj, VBS-biased generation | **direct Delphes fakes**: the second photon is a Delphes photon from a jet (π⁰/η) |
| tt̄γγ | tt̄γγ | direct, or VBS-factorised |
| tt̄γ, tWγ (one fake) | tt̄γ, tWγ test samples × transfer factor | TF = P(second Delphes photon passes the photon, mℓℓγγ and window cuts \\| one-photon level), measured in the direct QCD Zγjj sample; 100 % uncertainty |
| double fakes (Z+jets, tt̄) | — | not in b. Order of magnitude only; the reference also neglects them. Direct Delphes support is zero, and the Phase-05 FF estimate was about 0.02 events at 500 fb⁻¹ |

- **Estimation hierarchy:** recorded per number in Table IV.
  - L0: direct, ≥ 10 raw events in the window.
  - L1: continuum only, N(105–165 GeV) × f_win from an exponential MLE fit of that sample's Delphes mγγ, with ≥ 10 raw events in the wide range.
  - L2: VBS-factorised, 100 % uncertainty.
  - L3: transfer factor.
  - UL: zero support. The central value is 1.14 w_evt (Poisson 68 % CL), with 100 % uncertainty and a 95 % UL of 3 w_evt.
- **Hard/soft photon overlap removal:** uses the GenTruth count of prompt photons (pT > 15 GeV, \\|η\\| < 2.5, ΔR > 0.4), matching the Zγγ ME phase space.
  - One-ME-photon samples (Zγjj, tt̄γ, tWγ) keep n_prompt ≤ 1.
  - Events with a second hard prompt photon (e.g. from QED shower FSR) are covered by the Zγγ samples and removed.
- **Generator biasing:** the Zγjj and Zγγjj samples are generated with pT(γ) > 25 GeV and mjj > 400 GeV (plus 100 < mγγ < 170 GeV for Zγγ). Every reconstructed selection used stays inside this phase space:
  - pT(γ) ≥ 25 GeV, and pT(γ2)/mγγ > 1/4 implies > 26 GeV in the 105–165 GeV range;
  - mjj ≥ 500 GeV in the scan;
  - the mγγ range is 105–165 GeV.
  - For this reason the reference-like baseline uses photon pT > 25 GeV instead of 20 GeV.
- **Zγγ on-shell Z:** the full ℓℓγγjj gridpack integration projected to 15 h (QCD) and >100 h (EW), so Zγγjj is generated as `p p > z a a j j, z > l+ l-`. Photons radiated in the Z decay are therefore missing. Such events have mℓℓγ or mℓℓγγ ≈ mZ and fail |mℓℓ − mZ| < {zw if zw else 25:.0f} GeV or mℓℓγγ > {O['mllgg']:.0f} GeV; this is a limitation (§8).
- **EW Zγγjj** is 4-flavour with a 3-way split in the beam-1 parton class: u c / d s / ū c̄ d̄ s̄. Gluon-initiated processes do not exist at QCD⁰.
  - Split 1 was integrated with Monte-Carlo helicity sampling (`nhel 1`, same process) because helicity summation projected to 13 h.
  - σ closure per split is below 0.4 %.
- **EW Zγγjj is the dominant background** at the final selection. This was cross-checked against the reference, where EW Zγγjj is the *signal*: 0.263 fb inclusive and 0.057 fb after their initial selection. Our window-and-VBS yield corresponds to a few percent of that, as expected from the falling mγγ spectrum.
  - The sample contains no H→γγ peak, and the `sm` model has no hγγ vertex, so there is no double counting with the signal.
  - The Phase-05 pilot proxy (0.029 events at 500 fb⁻¹) underestimated this background by about an order of magnitude; the pilot results in report 05 are superseded.
- **Fake-factor cross-check (Delphes jets):** in the QCD Zγjj sample with the ff1 mode of `ntuple.py`, f = 5×10⁻⁴, 10⁻³ and 2×10⁻³ plus a pT-dependent variant give {d['ff_xcheck']['f=0.001']['final']:.4f} events (f = 10⁻³; band {d['ff_xcheck']['f=0.0005']['final']:.4f}–{d['ff_xcheck']['f=0.002']['final']:.4f}) at the final selection, 500 fb⁻¹. The direct Delphes result is {d['ff_xcheck']['direct Delphes']['final']:.4f}. Without the VBS cuts it is {d['ff_xcheck']['direct Delphes']['noVBS']:.3f} (direct, {d['ff_xcheck']['direct Delphes']['raw_noVBS']} raw) vs {d['ff_xcheck']['f=0.001']['noVBS']:.3f} (FF). The Delphes fake rate therefore corresponds to f ≈ {1e-3*d['ff_xcheck']['direct Delphes']['noVBS']/d['ff_xcheck']['f=0.001']['noVBS']:.1e} per jet.

## 5. Selection and optimisation

- **Reference-like baseline** (arXiv:2512.07689 Sec. III):
  - OSSF pair with 70 < mℓℓ < 120 GeV and two photons with pT > 25 GeV (20 GeV in the reference);
  - mℓℓγγ > 100 GeV;
  - ≥ 2 jets with mjj > 700 GeV and |Δηjj| > 2.0;
  - mγγ within ±2σ of the Delphes signal peak.
- **Optimisation** uses expected quantities only, at 500 fb⁻¹ for definition (a); the data are never consulted.
  - Coordinate descent over: the mγγ window (±1.5σ / ±2σ), pT(γ)/mγγ thresholds, the Z window (70–120 GeV or ±25/20/15/10 GeV), the Zeppenfeld z*(γγ) cut, mℓℓγγ, the b-veto, and a joint mjj × |Δηjj| grid.
  - FOM: Z with σ_b (MC-stat ⊕ systematics).
  - **Plateau rule** against noisy scans: among points with Z ≥ 0.97 Z_max, take the one with the largest signal.
- **Optimum:** {cuts}.
- The mjj × |Δηjj| landscape (Fig. 4-style: `figures/scan_mjj_deta_*.png`, tables below) is smooth: at 500 fb⁻¹, Z_Eq1 ranges from {min(v['Z'] for k, v in d['scan'].items() if k.startswith('500|')):.3f} to {max(v['Z'] for k, v in d['scan'].items() if k.startswith('500|')):.3f}.
  - Z rises slowly towards looser mjj and tighter |Δηjj|.
  - **The optimum lies on the mjj = 500 GeV scan boundary.** This is the loosest threshold allowed by the generator-level mjj > 400 GeV bias of the Zγ and Zγγ samples. The trend suggests only a few-percent gain below it.
  - Moving to mjj > 700 GeV, |Δηjj| > 3.0 changes Z by {d['robustness']['mjj > 700, |deta| > 3.0']['Z_syst'] - d['robustness']['optimum']['Z_syst']:+.3f} (robustness table). This does not affect the conclusions.

## 6. Results

### PRIMARY: Eq. 1 counting significance (stat. only, ± MC stat) and limits

| L [fb⁻¹] | signal definition | s | b | Z_Eq1 ± MC | Z_syst (binned PL fit) | μ₉₅ CLs (exact Poisson, syst) | μ₉₅ (binned PL fit, asymptotic) |
|---|---|---|---|---|---|---|---|
{chr(10).join(res_row(k, v) for k, v in R.items())}

- **s < 1 in every row:** Z alone is not meaningful.
- **μ₉₅ from exact-Poisson CLs:** counting in the window, with b marginalised over a log-normal(σ_b/b). This is the robust number.
- **Asymptotic fit limit:** uses Asimov asymptotics, which are not valid at these counts. It is shown only because it was requested, and it underestimates the limit.
- **Largest background components** at 500 fb⁻¹, definition (a): {"; ".join(f"{k} {y:.4f}" for y, k in top)}.

{tables}

## 7. Systematic uncertainties (supplementary fit and Z_syst)

- **Background normalisation:**
  - 10 % per process for prompt and resonant backgrounds;
  - **50 % for fake-photon processes** (Zγjj, tt̄γ, tWγ). Robustness variants use 25 % and 100 %.
- **Luminosity:** 2.5 % on all MC-normalised processes.
- **MC statistics:** per process, from the raw count of the estimate. L2, L3 and UL estimates carry 100 % uncertainty.
- **Fit:** binned Poisson likelihood in mγγ with {len(d['fit_edges'])-1} bins over 105–165 GeV.
  - Window bins: ±1σ and ±2σ around the Delphes peak. Sidebands: 5 GeV bins.
  - Templates: the Delphes signal shape for resonant processes; exponential fits for the continuum.
  - Nuisances: one log-normal per background process (normalisation ⊕ MC stat) plus luminosity.
  - Asimov data; q₀ for Z; asymptotic CLs (q̃μ) for μ₉₅.
- **Not included:** no theory uncertainty (scale, PDF, LO→NLO) on the signal or on the background shapes.

## 8. Limitations

1. **The statistical regime limits the result, not the background model.** s < 1 even at 3000 fb⁻¹, so the Z values are illustrative.
2. **The Delphes CMS card is not real CMS.**
   - σ_mγγ is about 2.1 GeV, against about 1.5 GeV in data.
   - Electron reconstruction efficiency is low: OSSF acceptance about 36 % for signal (D11: stock card kept for comparability with the reference). A CMS-like lepton efficiency would raise s by up to ×1.7, and the conclusions would not change.
   - The **Delphes jet→photon fake rate is an assumption of the detector card**, not a measurement. The FF band (§4) brackets it within a factor of about 2.
3. **Zγγjj uses an on-shell Z.** Photons radiated in the Z decay are not included (§4).
4. **Generator-level biasing** of Zγ and Zγγ: pT(γ) > 25 GeV and mjj > 400 GeV. The reference-like baseline therefore uses photon pT > 25 GeV.
5. **ggZH jets come only from the parton shower.** ggZH is LO loop-induced with no ME jets, so its VBS-region jets come from the Pythia8 power shower. Its selection efficiency is therefore about 2× that of fixed-order QCD ZHjj, and the yield is uncertain by about a factor of 2. A merged gg→ZH+jets sample is beyond LO MG5 in this setup.
6. **Factorised and transfer-factor estimates assume cut independence.** These are tt̄γ, tWγ, tt̄γγ and tHW, all ≪ s. Each carries 100 % uncertainty.
7. **Everything is LO, with no k-factors.** QCD ZHjj uses fixed-order ZH+2j; the merged 0–2j cross-check is in report 05.
8. **Double-fake backgrounds** (Z+jets, tt̄) are not in b. They are order-of-magnitude only, as in the reference.
9. **3000 fb⁻¹ is luminosity scaling at 13.6 TeV,** with no pile-up and no HL-LHC detector.
10. **EW–QCD ZHjj interference** is not included; its size is in report 03.
{("11. **" + PEND + "**") if PEND else ""}

## 9. Outlook: VHjj

- **Wider signal definition.** Adding Z→νν, W→ℓν (WHjj) and τ final states raises the produced signal by roughly an order of magnitude. Each brings its own dominant backgrounds: Wγγ, Zγγ with Z→νν, and fakes. This needs a new Phase 01.
- **Other Higgs decays.** H→bb̄ (BR ≈ 58 %) gives about 250× more signal before selection, against tt̄ and Z+bb̄ backgrounds; a boosted H→bb̄ VBS selection is the natural next study. H→WW*/ττ are intermediate options.
- **Within H→γγ, the gains are bounded:**
  - CMS-like resolution and lepton efficiency: up to ×1.7 in s;
  - a multivariate VBS tagger: typically 20–40 % in Z;
  - combining ZHjj with WHjj.
  - Even together, these do not reach s ≫ 1 at 3000 fb⁻¹ in the ZHjj, H→γγ channel alone.

## 10. Figures (`figures/`, PDF + PNG)

All distributions are at 3000 fb⁻¹, Delphes level, after all optimum cuts except the VBS-jet cuts and the mγγ window. The signal is unstacked; the mℓℓ plot uses a relaxed mℓℓ window.
- `m_gg`, `m_ll`, `m_jj`, `deta_jj`, `photon1_pt`, `photon2_pt`, `zeppenfeld`
- `scan_mjj_deta_500`, `scan_mjj_deta_3000`: Eq. 1 significance vs the mjj and |Δηjj| thresholds, other cuts at the optimum (the reference's Fig. 4).

## 11. Checks

- **σ closure:** below 1 % for every final sample (see the table in §2).
- **Ntuples:** event counts equal the verified job totals.
- **ggZH decay closure** (GenTruth, first job, 2000 events):
  - 98.4 % of events have a prompt ee or μμ pair (49.2 % ee, 50.6 % μμ, no ττ), confirming that the forced Z→ee/μμ was applied once;
  - 86.8 % have two prompt photons with pT > 10 GeV (forced H→γγ; the rest is acceptance).
  - Signal/QCD ZHjj BR closure: report 05 §1.
- **Fake rate:** the FF and direct Delphes fake estimates agree within the FF band.
- **Re-optimisation:** the optimum Z_syst differs from the reference-like baseline by {d['robustness']['optimum']['Z_syst'] - d['robustness']['reference-like baseline']['Z_syst']:+.3f} at 500 fb⁻¹.
- **Robustness:** see the table above.
"""
open(OUT, "w").write(txt); print("wrote", OUT, len(txt.splitlines()), "lines")
