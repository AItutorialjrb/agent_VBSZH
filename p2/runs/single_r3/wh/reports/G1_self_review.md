# G1 self-review of WH reports 01–03 (single_r3), written as a referee

- **Date UTC:** 2026-11-09 00:20.
- **Reviewer:** the same single agent that produced the work. This is not independent, which is the protocol for the single arm; that limitation is stated here.
- **Method:** each number in reports 01–03 was traced to its evidence file. The checks were: Delphes level only; BR applied once; N policy; overlap removal; low-count statistics; overclaims; logged deviations.
- **Severity scale:** 1 = changes a result or violates handoff §1; 2 = weakens a claim, must be fixed before Phase 05; 3 = presentation.

## Issues

| # | Sev | Issue | Evidence | Disposition |
|---|---|---|---|---|
| 1 | 1 | The EW and QCD Wγγjj continuum uses an on-shell W chain, which **misses photon radiation from the W-decay lepton**: ×2.02 at 0 jets with identical generator cuts. Every B0 comparison in report 02 is therefore optimistic for the dominant background. | `work/m5/Q_lvaa_0j`, `Q_waa_0j`; report 02 §3.4 | OPEN → **D-WH-3**. Flagged in report 02 §3 and §8; not hidden. |
| 2 | 1 | Delphes stock e→γ (7.5–9.4 % of electrons) produces about 3 background events from Z(ee)γjj at B0, more than the signal. The estimate is untrusted Delphes physics. | report 03 §3; `work/zhreuse/F_*_llajj_vbs*.json` | OPEN → **D-WH-4** (parametrised f_e→γ plus m(eγ) Z-veto). |
| 3 | 1 | W+jets double fake: a direct N ≥ σ×BR×3000 is impossible (9.9·10⁹ events). Meeting handoff §1 requires a declared exception. | report 02 §6 | OPEN → **D-WH-6**. Not relaxed silently. |
| 4 | 1 | Phase 03 is incomplete: QCD Wγγjj and its twin have no σ and no test job yet. | condor 899736.14/15 | Report 03 is marked **PARTIAL**, not PASS. The jobs release automatically; verification is pending. |
| 5 | 2 | B0 used photon pT > 20 GeV, below the pta > 25 generator cut of the photon samples. | `wh_baseline.py` | **FIXED at review:** re-run with pT > 25 (`work/b0_pt20_vs_pt25.txt`). Window yields change by ≤ 6 % (signal), 2 % (EW Wγγ) and 13 % (Zγjj). Conclusions unchanged (report 02 §8b). D-WH-5 fixes 25 GeV for the analysis. |
| 6 | 2 | The QCD-type generator m_jj > 400 cut removes 63 % of the reco-VBS region. The Wγ+jets correction C ≈ 4.3 rests on 24 vs 55 fake combinations, an uncertainty of about 25–30 %. The twin needs 19 M events under the N rule. | `work/test/genmjj_safety.txt`; `work/fakes/*` | Stated; it is a production-design item (D-WH-6, D-WH-7). |
| 7 | 2 | Many background components have 0–5 raw events or combinations at B0 (tt̄H 1ℓ, tt̄γ 1ℓ, tt̄γγ 1ℓ, tWγ 1ℓ, tHW, ZH→ττ, W+jets). A zero MC count is reported as "no MC support" with w_evt, never as zero. | report 02 §2 | Correct handling; the numbers are not usable as yields. |
| 8 | 2 | `wh_baseline.py` applies no n_prompt overlap rule to the reused Zγjj. Possible double counting with Zγγ is ≤ 0.17 events. The reused ZH Zγjj numbers also mix Delphes e→γ with j→γ, and C is not applied to the QCD Zγjj. | report 02 §9 | Stated. Fix in Phase 05 ntupling. |
| 9 | 2 | The W normalisation convention (WF on the chain σ) differs from σ_prod × B_PDG by about 2.8 % (Breit-Wigner truncation and off-shell production). The off-shell (0,5) calculation supports the chain to ±1 %. | report 01 §4 | OPEN → **D-WH-2** (recommended: WF on the chain σ, ±1 % lineshape, +1.8 % universality alternative). |
| 10 | 2 | The σ-closure tolerance (±2 %) was chosen after seeing the results. tWγ (−1.6 %) and tHW (−1.0 %) are the largest deviations. The printed Pythia errors are truncated, so pulls are not meaningful. | `work/test/closure_p03.txt` | Disclosed in report 03 §2; production must use the job-averaged σ. |
| 11 | 2 | The resonant-H inventory is incomplete. ggF H+jj with a non-prompt lepton has no bound (no heft sample). tt̄ semileptonic double fake has no bound. The QCD WH merged (MLM 0–2j) alternative was not studied. | report 02 §2 | OPEN → **D-WH-6/D-WH-7**. The ggF ranking estimate is marked as such. |
| 12 | 2 | The EW×QCD interference was evaluated at parton level from 1000 signed events (−0.11 ± 0.07 % in the VBS region). | report 01 §3 | Small; re-check after selection. |
| 13 | 2 | The lost-lepton backgrounds (ZH reuse) and e→γ scale with the Delphes electron inefficiency (57 %), which is likely pessimistic compared with CMS. They are model-dependent. | report 02 §4 | Goes into the robustness table (Phase 07). Not a data-driven statement. |
| 14 | 2 | Isolation: one `pgrep -af` on the shared node printed other runs' process command lines (multi_r3 card names, a `_to_delete` directory). | `runs/single_r3/PROGRESS.md` | **Logged as an access incident.** The information was not used in any design choice: the no-b/b-complement and Higgsstrahlung analyses were planned before it, per the AGENTS.md requirement on Higgsstrahlung-like contributions. |
| 15 | 3 | Theory weights (7-point scale ⊕ PDF) are stored but not evaluated. | — | Phase 04/05. |
| 16 | 3 | The run is uncommitted. The reports cite base commit e681d9b. | — | **D-WH-9.** |
| 17 | 3 | Observation for the frozen ZH study: its ledger omits the PDG/MG5 W rescale for MG5-decayed top-W's (tt̄H, tt̄γ, tWγ, tt̄γγ; WF² = 0.922, so those yields are about 8 % high). | ZH `FINAL_report.md` §3 table; `wh/scripts/ledger.py` | Reported only (ZH is frozen). **D-WH-8** asks whether to forward it as an erratum. |

## Overclaim check
- No significance, μ₉₅ or sensitivity statement is made.
- "Fakes and continuum exceed the signal at B0" is stated as a validation-level observation with its statistics.
- The ZH reuse is described as covering the lost-lepton phase space only where the run cards show it (§4 of report 02).

## Verdict
- Phases 01 and 02 are acceptable as definition and ledger, conditional on D-WH-1 … D-WH-7.
- Phase 03 is PARTIAL (2 of 18 sample types pending).
- Severity-1 items open at G1: **4** (#1–#4). None was silently relaxed.
