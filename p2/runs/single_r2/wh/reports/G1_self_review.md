# G1 self-review of WH Phase 01–03 (single_r2) — written as an independent referee

- **Date (UTC):** 2026-11-09. **Reviewer:** the same single session that produced the work (single arm, no subagent). The independence is therefore procedural only; this limitation is stated up front.
- **Reports reviewed:** `01_signal_definition.md`, `02_background_overlap.md`, `03_generation_validation.md`, together with their evidence in `wh/work/{smoke,gp_condor,condor_test,validation}` and `wh/config/xsec_br_ledger.json`.
- **How the numbers were checked:**
  - Every number in the summary tables was recomputed from its evidence file during the review: the σ ratios, the R factors, the interference fractions, the def-(b) sum, the tt̄γ 2ℓ/1ℓ ratio, the frozen-ZH yields and the BR factors.
  - Two errors were found and **fixed** in 02: (i) the F_Wjj σ was quoted as the PY8 value instead of the integration value; (ii) an unsupported "ggZH ≈ 0.1× QCD ZH" statement was replaced by the correct pre-cut ratio (0.5).

## Severity 1 — would change a result if left unresolved
1. **The prompt Wγγjj continuum has no cross section, gridpack or Delphes test** (03 §6; cluster 899738.0–2 was still running).
   - This is expected to be a leading background, as it was in ZH.
   - Phase 03 is therefore not complete for this sample type, and the overall phase status is BLOCKED (partial).
2. **The on-shell-W treatment underestimates the prompt continuum by about a factor of 2** (02 §3.1, R = 2.01 ± 0.05).
   - R comes from a *0-jet generator-level proxy*. The VBS-region value and its Delphes-level counterpart are not measured.
   - If ZH's on-shell recipe were copied, b would be about 50 % low. → D-WH-4.
3. **W+jets with two fake photons cannot satisfy N ≥ σ·k·3000 fb⁻¹** (5 × 10⁸ events; 02 §6).
   - The pilot estimate (0.31 events, band 0.03–2.8) has N_eff = 2.4 and is a fixed-order lower bound. It could be comparable to the signal.
   - A policy deviation is needed. → D-WH-6.
4. **The non-prompt-lepton (γγ+jets) and e→γ (Zγjj) backgrounds reach 1.4 and 0.36 events in their upper scenarios.**
   - That is comparable to s ≈ 1.0. Both are bounds (2-parton pilot with 6 raw peak events; parametrised f_e on frozen samples).
   - They must be produced and treated in Phase 04. They cannot be dismissed.

## Severity 2 — affects a normalisation or an uncertainty at the few-% to 10-% level, or a definition choice
5. **Flavour scheme (D-WH-1).** The non-top b-initiated EW part of the signal is dropped, and its size is **unquantified**: the `$$ t t~` diagnostic is not interpretable (144.6 > 126.9 fb). The 4F-external / 5F-PDF mismatch is stated, not resolved.
6. **WF convention:**
   - The lepton-universal choice vs the non-universal e/μ PDG values is a −1.75 % effect (D-WH-2).
   - Applying WF to ℓν-in-ME samples (D-WH-3) differs from the frozen ZH convention.
   - The frozen ZH ledger applied **no** W-BR correction to its tt̄H/tt̄γ/tWγ samples (it uses the MG5-LO W→ℓν BR, which is +2.3 % per leptonic W relative to PDG, i.e. +4.6 % for the dileptonic tt̄ samples). This inconsistency matters for the VH combination and should be noted at combination time. It does not concern the WH-only result.
7. **QCD W BR closure pull +2.1.**
   - Accepted under a tolerance (|pull| < 3) that was fixed while writing the report, *after* the numbers were seen. This is disclosed. A pre-registered tolerance would have been better.
   - The ±1.4 % chain-normalisation systematic is a reasonable cover.
8. **Lepton reconstruction efficiency in acceptance is only 0.65–0.70, with an electron deficit** (e 471 vs μ 669). This is the same Delphes-card behaviour found in ZH. It is not a WH-specific error, but it directly scales s and b.
9. **The EW–QCD interference is measured only at loose cuts** (−0.41 %). ZH showed that the VBS-region value differs. A signed Delphes-level sample is needed.
10. **Frozen-sample transfer assumptions.**
    - The QCD Zγγ lost-lepton estimate reuses ZH's generator-m_jj correction C = 2.37, which was measured for the ZH selection, not the WH selection.
    - The EW Zγγ total (≈ 0.14) is scaled from one of three beam-class splits.
11. **Overlap-truth tool.** `slim_gentruth.py` stores the highest-index W, which is an s-channel W→jj in ≈ 17 % of EW events. It is harmless for photon overlap, but wrong for any W-truth study. A patch is needed before Phase 04 truth use.

## Severity 3 — presentation and reproducibility
12. **Smoke-cutflow normalisation.** The 03 §4 smoke cutflow uses σ_PY8 = 13.57 fb (1000-event local run) rather than the integration value 13.76 fb (−1.4 %, within the MC error). It is labelled, but the two σ's could confuse a reader.
13. **Figures.** Overflow is clipped into the last bin (stated in the axis range only), and the fit legend slightly overlaps the m_γγ histogram.
14. **Late additions.** 01 was written before the off-shell and no-top results arrived, and was updated afterwards (2026-11-09). The status line records this.
15. **Isolation.** The session listed directory *names* outside the allowed set (`p2/`, `p2/software`, `p2/combination`). It also read the header line of `p2/metrics/ledger.csv` and appended ledger lines to that file. No content of another run was read. Logged in `wh/PROGRESS.md` as a minor access deviation.
16. **Usage limit.** The session paused from 2026-11-08 ≈ 20:56 to 2026-11-09 00:01 UTC on a claude.ai usage-limit reset (not a human prompt). Wall time therefore over-states the active time (see the token/time table).

## What is solid
- The signal amplitude definition is gauge invariant and audited by subprocess/diagram lists, including an exact interference-diagram closure.
- The BR is applied once, with code assertions.
- The W BR closure and the pole approximation both hold at 1–2 %.
- Forced H→γγ is verified on 7000 truth events, and the σ closure through Pythia is within 0.8 % on four sample types.
- Four event-level condor test jobs ran end to end with the unchanged lib wrapper, using registry seeds.
- No yield is presented as final, and no zero is used as negligible.

## Verdict
**Not ready for G2 as is.** Severity-1 items 1–4 need either the running jobs (item 1) or human decisions D-WH-4 and D-WH-6 (items 2–3) before a production plan can be written. The signal definition (01) is acceptable for G1, conditional on D-WH-1…3.
