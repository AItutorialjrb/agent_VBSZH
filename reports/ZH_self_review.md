# ZH — single-agent self-review of FINAL_report.md (referee-style)

- **Date:** 2026-11-03 (UTC).
- **Reviewer:** the same single agent (Claude Code session c6cda945…) that produced the study, with no subagents. This is the paper's single-agent baseline.
- **Method:**
  - Re-read `FINAL_report.md` as generated from the pre-freeze `final.json` (test runs `final_test3.json` and the final run).
  - Cross-check every quantitative claim against its evidence file: `final.json`, `verify.json`, `work/theory/*.json`, the ntuples, condor logs and reports 00–05.
  - Classify each issue by severity, fix the supported ones, and re-generate the report.
- **Severity scale:**
  - **S1:** changes a headline number or conclusion.
  - **S2:** materially incomplete or misleading, without changing the conclusion.
  - **S3:** presentation or traceability.
- **Status values:** FIXED (with evidence of the fix), ACCEPTED-LIMITATION (stated in FINAL_report §8), NOT-A-BUG (verified).

## Issue list

| # | sev. | issue (as a referee would raise it) | evidence | resolution | status |
|---|---|---|---|---|---|
| 1 | S1 | Generator cut mmjj > 400 GeV of the VBS-biased samples was asserted safe for a reco cut mjj > 500 GeV, with no test | `work/theory/mjj_resolution.json`: P(parton mjj < 400 \| reco mjj > 500, \|Δη\| > 3.5) = 1.4 % (EW ZHjj) but **64 % (QCD ZHjj)** | Direct Delphes no-mjj-cut twins of QCD Zγjj and QCD Zγγjj. C(cuts) = Y_twin/Y_biased is applied with its stat. uncertainty as a nuisance (`genmjj` in final.json; FINAL_report §4). EW-type samples are uncorrected (1.4 %). **Final: C = 2.05 ± 3 % (QCD Zγjj) and 2.37 ± 6 % (QCD Zγγjj). b at 500 fb⁻¹ rises 0.455 → 0.516 and Z_Eq1 falls 0.126 → 0.119 (def. a).** | FIXED |
| 2 | S1 | tt̄γ/tWγ: 2000 events each, far below N ≥ σ×BR×3000 fb⁻¹, and estimated only via a transfer factor | Pre-fix registry: N = 2000, σ×BR = 85.58 / 13.04 fb | Regenerated with N = 1.04 M / 160 k (≥ 4× σ×BR×3000 fb⁻¹), reference Table I definitions. They are now direct estimates (L2b). The zero-count UL is a robustness row. `nmc_check()` aborts on any violation. | FIXED |
| 3 | S1 | No theory uncertainty anywhere | Old FINAL_report §7: "Not included: no theory uncertainty" | Scale (7-point) ⊕ PDF (NNPDF3.1 replicas) per process from MG5 weights. Signal and QCD ZHjj use the Tier-1 LHE; the backgrounds use LHE-only reruns of the production gridpacks. Applied in counting (σ_b, σ_s) and fit (correlated groups). | FIXED |
| 4 | S2 | Zγγjj generated with an on-shell Z: missing ℓℓγγjj (FSR / γ*) not quantified | Old §4 / §8 item 3 | MG5 pair ℓℓγγ vs Z(→ℓℓ)γγ after all non-jet cuts: 1.128 ± 0.024 (reference 1.128 after its mℓℓ cut). Applied as a ×1.128 correction with a ±5.7 % nuisance. | FIXED |
| 5 | S2 | EW–QCD interference: ZHjj not included; Zγγjj not discussed | Old §8 item 10 | ZHjj: −0.20 ± 0.02 % of EW in the VBS region, negligible. Zγγjj: dedicated undecayed-Z MG5 runs (3 beam-1 splits × {I, EW}) give **+2.3 ± 0.3 %** of EW in the VBS + photon region (+6.4 % inclusive; reference 9.3 % inclusive). Applied as a ±2.3 % nuisance on EW Zγγ. | FIXED |
| 6 | S2 | Optimum on the mjj = 500 GeV scan boundary; no evidence that nothing is gained below it | Old §5 | Z vs mjj (400–1200 GeV) and vs \|Δη\| (2–5) curves (`figures/z_vs_mjj`, `z_vs_deta`). Delphes mjj resolution σ68 = 8.8 %. Data-driven statement of the gain below 500 GeV. | FIXED |
| 7 | S2 | ZF = 0.9783 stated without derivation; no proof that each BR is applied once | Old §3 | Derivation (MG5 2Γℓℓ/Γ_Z = 0.068784 vs PDG 0.067294). Per-sample BR ledger generated and asserted in code. | FIXED |
| 8 | S2 | Detector model: the Delphes lepton/photon efficiency is low and unquantified | Old §8 item 2 ("up to ×1.7") | Measured Delphes prompt-object efficiencies (`object_eff.json`). CMS-like reweighting row for all L. | FIXED |
| 9 | S2 | ggZH LO with shower jets only; normalisation unconstrained | Old §8 item 5 | ×2/×0.5 log-normal nuisance and robustness rows | FIXED |
| 10 | S2 | No coupling interpretation | prompt 13 | §9: λWZ, κZ, CP-odd c_A from direct HC-model samples; closure tests; 1D/2D scans; comparison with CMS/ATLAS | FIXED |
| 11 | S1 (found in this review) | The draft summary attributed Z(exclude λWZ < 0) to the Δ(−2 ln L) at λWZ = −1. The minimum over λWZ < 0 is at λWZ → 0⁻, where the yield is close to the SM | `final_test3.json` coupling: Z(all λ < 0) = 0.34 vs Z(λ = −1) = 1.07 at 3000 fb⁻¹ | Summary and §9 now quote both, explain the λ → 0⁻ degeneracy, and state that this channel cannot test the sign of λWZ | FIXED |
| 12 | S2 (found in this review) | The CMS-like efficiency row equalled the nominal row; the mjj-resolution row showed 103 % | `theory_summary.json` was built before `object_eff.json` and the corrected `mjj_resolution.json` existed | theory_summary regenerated before the final run. Final: the CMS-like row has s × 2.05 and b × 2.15 (Z_Eq1 0.166 vs 0.119 at 500 fb⁻¹); mjj σ68 = 8.8 %. | FIXED |
| 13 | S2 (found in this review) | Morphing closure χ² ignored the uncertainty of the extrapolated prediction (χ²/ndf up to 35/7) | `coupling_section.py` closure | χ² now includes the covariance of the per-bin quadratic fit. Final mℓℓγγ (fit observable) leave-one-out χ² = 9.0, 5.6, 7.2 for 7 bins; totals within 0.7 %. | FIXED |
| 14 | S3 | κZ scan range [0.5, 1.5] too narrow (intervals at the edge) | `final_test3.json` | κZ ∈ [0, 3]. Interval ends at a scan boundary are marked `*` | FIXED |
| 15 | S2 | The no-mjj-cut twins are below σ×BR×3000 fb⁻¹, which is the same class of issue as #2 | QCD Zγjj twin: σ = 818 fb, N = 200 k | Flagged explicitly as a decision in the N table and in §2. Only the ratio C enters, and its MC-stat uncertainty is a nuisance. | ACCEPTED (flagged) |
| 16 | S3 | "Zeppenfeld z* < 1.0" robustness row identical to the optimum — suspicious | — | Verified: z*(γγ) < 1 for 100 % of preselected signal VBS events (max 0.993). Not a bug. | NOT-A-BUG |
| 17 | S3 | "fake syst 25 %/100 %" rows give the same Z_syst and μ₉₅ as nominal | Uncertainty budget: fake processes are about 0.04 of b = 0.45 | Genuine: b ≪ 1 at 500 fb⁻¹; σ_b is dominated by ggZH, Zγγ interference, theory and off-shell | NOT-A-BUG |
| 18 | S2 | ZH(→ττ) enters with the zero-support convention (central 1.14 w_evt), which is larger than its likely value | Table IV: raw = 0 after the Z window | Conservative; 100 % uncertainty; the effect on b is 1 %. | ACCEPTED-LIMITATION |
| 19 | S2 | Asymptotic fit μ₉₅ quoted at counts where asymptotics fail | §6 | Kept as supplementary and labelled. The exact-Poisson CLs is the primary limit. | ACCEPTED-LIMITATION |
| 20 | S2 | Off-shell/FSR correction measured at 0 jets in QCD and transferred to EW and QCD jj | §4 | The reference's EW-jj ratio (1.078 after all cuts) lies within the ±5.7 % nuisance | ACCEPTED-LIMITATION |
| 21 | S3 | Reference comparisons do not mark the 25 vs 20 GeV photon threshold consistently | prompt 09 A5 | Tag **[γ pT 25 vs 20 GeV]** on every comparison (header, §4, §5, §11, baseline tables and rows) | FIXED |
| 22 | S2 | Coupling: ggZH, ttH, tHW kept at SM; ggZH depends on κZ, κt | §9 | Stated in §8 item 8. ggZH is a background of about 0.05 events at 500 fb⁻¹. | ACCEPTED-LIMITATION |
| 24 | S3 (found in this review) | PROGRESS.md entries of 2026-11-03 carried estimated, not measured, times (twice; up to +2 h off) | `date -u` vs the entry labels; transcript timestamps | All affected entries relabelled with the true window; subsequent entries use `date -u`. The metrics use transcript timestamps, never PROGRESS labels. | FIXED |
| 23 | S3 | One coupling job (cpo_m2 seed 143200002) crashed after LHE | condor log | Dropped (24/25), as for earlier deterministic segfaults. N = 48 000 is used. | ACCEPTED |

## Net effect of the review-driven fixes on the headline (500 fb⁻¹, def. a)

| quantity | pre-review FINAL (commit 2503e4c) | after A + E + review (this freeze) |
|---|---|---|
| s | 0.088 | 0.088 |
| b | 0.420 | 0.516 |
| Z_Eq1 ± MC | 0.131 ± 0.002 | 0.119 ± 0.002 |
| μ₉₅ (CLs, exact Poisson) | 34.1 | 34.5 (incl. theory) |

The main driver is the generator-mjj correction of the QCD-type samples (#1), followed by the off-shell/FSR correction (#4). The conclusions are unchanged: s < 1 at every luminosity, and the limit is the meaningful quantity.

## Items checked and found consistent

- Every yield in Tables III/IV is reproduced from `final.json` by `final_tables.py`. The report generator reads only JSON, with no hand-copied numbers.
- σ closure < 1 % for every final sample and < 1.8 % for the coupling samples.
- The HC-model λWZ = 1 sample agrees with the SM-model Tier-1 signal at the full selection: ratio 0.986 ± 0.017. This validates the model patch and the mmjj > 400 GeV generator cut for EW samples.
- The direct cross sections at λWZ = ±0.5 and 1.5 are predicted from (−1, 0, 1) to within 0.3 %. This confirms the exact quadratic dependence.

## Remaining limitations (not fixable within this study)

These are listed in FINAL_report §8:
- LO only;
- the Delphes card is not CMS;
- the CMS-like efficiencies are assumptions;
- the off-shell transfer is a 0-jet proxy;
- double fakes are not in b;
- 3000 fb⁻¹ is a luminosity scaling;
- the coupling result is a production-only interpretation with BR(H→γγ) fixed to SM.
