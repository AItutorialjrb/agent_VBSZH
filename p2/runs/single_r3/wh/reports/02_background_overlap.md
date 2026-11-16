# WH Phase 02 — background matrix and overlap ledger, single_r3

- **Date UTC:** 2026-11-08 20:30 → 2026-11-09 00:20.
- **Status: PASS as a ledger with quantitative first estimates; four physics decisions open (D-WH-3 … D-WH-6).**
- **Git:** base commit `e681d9b`, uncommitted.
- **Inputs:** report 01, test-job samples (report 03), frozen ZH samples under `production/{v1,final}` (read-only), the PDG/YR4 inputs of report 01 §4. Seeds as in report 01.
- **Scope note:** every number below is a validation-level estimate at a **pre-declared, non-optimised baseline B0**, computed at 500 fb⁻¹ from 1k–5k-event test jobs or from frozen ZH samples. None of them is a final yield. A zero MC count is never read as a zero background.

## 1. Final state and baseline B0
- **Reco target:** exactly one isolated e/μ, MET, two photons with m_γγ near 125 GeV, two VBS tag jets, and a b-veto.
- **B0** (`wh/scripts/wh_baseline.py`, fixed before any background was examined; evaluated at Delphes level):
  - leptons: e pT > 15, |η| < 2.5; μ pT > 15, |η| < 2.4; veto on a second lepton with pT > 10;
  - photons: ≥ 2 with pT > 20, |η| < 2.5 excluding the crack, ΔR(γ,ℓ) > 0.4; 100 < m_γγ < 180 GeV;
  - jets: ≥ 2 with pT > 25, |η| < 4.7, cleaned against the lepton and photons;
  - MET > 30 GeV; 0 b-tags (|η| < 2.5);
  - VBS: m_jj > 500 GeV, |Δη_jj| > 2.5; window 120 < m_γγ < 130 GeV.
- **Sidebands:** 105–120 and 130–165 GeV are reserved for Phase 06. No cut was tuned here.
- **Signal at B0 (signal test job, 2000 events):** **1.17** events in the window at 500 fb⁻¹ (155 raw), and 1.28 ± 0.10 in the interactive smoke run. Validation only.

## 2. Ledger
Columns: window yield at B0 and 500 fb⁻¹ (raw MC count in brackets) and the method. Machine-readable version: `wh/config/sample_matrix_wh.yaml`.

| ID | Role | Generator / order (card) | BR ledger k | Overlap rule | σ_gen [fb] | B0 window [ev] | Method / note |
|---|---|---|---|---|---|---|---|
| S_EW_WHjj_lv | signal | MG5 (0,4) no-b, W→ℓν chain | WF·B_γγ | order-exclusive vs QCD; flavour-exclusive vs bcomp | 13.79 | **1.17** (155) | direct |
| H_QCD_WHjj_lv | resonant (def. a) / signal (def. b) | (2,2) no-b, W→ℓν chain | WF·B_γγ | — | 58.6 | 0.58 (18) | direct; fixed order, MLM alternative open (D-WH-7) |
| I_WHjj | signed | `QCD^2==2 QED^2==6` | — | separate signed term | −0.238 | −0.11 % of EW (parton VBS) | quoted, not added |
| H_EW_WHjj_bcomp_lv | resonant (tHq-like) | (0,4) with ≥1 external b | WF·B_γγ | flavour partition (report 01) | 14.54 | 0.33 (41) | direct; b-veto keeps 36 %, so the b-veto matters (Phase 05) |
| H_EW_WHjj_taunu | resonant (τ feed-down) | (0,4) W→τν, τ in PY8 | WF_τ·B_γγ | distinct W decay | 6.83 | 0.14 (34) | direct |
| H_ttH_semilep | resonant | tt̄H, one t→bℓν (e,μ,τ) | WF3·WF_had·B_γγ | distinct external tops | 161.8 | 0 (0 of 2000; w_evt 0.09) | **no MC support**. Need production N; upper value 3.0·w_evt = 0.27 |
| ZH:H_ttH (dilep, lost ℓ) | resonant | frozen ZH final | WF²·B_γγ | dilep vs semilep exclusive by decay | 18.09 | 0.031 (65) | direct, reused |
| H_tHW_1l | resonant | tHW (DR), one leptonic W | WF3·WF_had·B_γγ | DR vs tt̄H | 7.04 | 0.012 (3) | direct, low statistics |
| ZH:S_EW_ZHjj (lost ℓ) | resonant | frozen ZH v1, 200k | ZF·B_γγ | Z vs W exclusive by final state | 1.295 | 0.032 (4406) | direct, reused; coverage verified (§4) |
| ZH:H_QCD_ZHjj (lost ℓ) | resonant | frozen ZH v1, 100k | ZF·B_γγ | — | 10.21 | 0.026 (234) | direct, reused |
| ZH:H_ggZH (lost ℓ) | resonant | frozen ZH final | BR_ZLL·B_γγ | — | 75.0 | 0.023 (80) | direct, reused |
| ZH:H_ZH_tautau | resonant | frozen ZH final (MLM) | B_γγ | — | 25.0 | 0.011 (2) | direct, low statistics |
| H_VBFH_nolep | resonant + non-prompt ℓ | (0,3) Hjj | B_γγ | requires 0 reco leptons | 4152 | 0.006 (f_ℓ = 1e-4; ×0.3–10) | parametrised f_ℓ (fl mode) |
| ggF H+jj | resonant + non-prompt ℓ | not generated | — | — | (ranking: ~σ_ggF·B_γγ·10⁻²) | bound pending | heft sample needed (D-WH-6) |
| B_EW_Waajj_wp/wm | continuum | (0,5) Wγγjj, on-shell W chain, VBS-biased | WF | n_prompt ≥ 2 | 0.129 / 0.0737 | **2.67** (58) | direct; **misses ℓ→γ radiation**: D-WH-3 |
| B_QCD_Waajj_lv (+nomjj twin) | continuum | (2,3), chain, VBS-biased | WF | n_prompt ≥ 2; twin for generator-m_jj correction | gridpacks building | — | Phase 03 pending |
| ZH:Zγγjj EW (is1h/2/3), lost ℓ | continuum | frozen ZH final | ZF | — | 0.0392 | 0.140 (440) | direct, reused |
| ZH:Zγγjj QCD, lost ℓ | continuum | frozen ZH final, VBS-biased | ZF | twin C (ZH: 2.37) | 0.0356 | 0.033 (187) × C | direct, reused |
| T_ttaa_semilep | continuum | tt̄γγ 1ℓ | WF3·WF_had | — | 0.869 | 0 (0; w_evt 0.21) | no MC support; production N |
| ZH:T_ttaa (dilep) | continuum | frozen ZH | WF² | — | 0.097 | 0.013 (6) | direct, reused |
| F_QCD_lvajj_vbs (+nomjj) | 1 fake γ | (2,3) ℓνγjj, VBS-biased | 1 | n_prompt ≤ 1 | 696 / 6381 | **1.61 ± 0.63** (vbs); 10.3 ± 4.8 (nomjj twin) | fake factor, f×{0.3,1,3}; **C ≈ 4.3 at VBS level** |
| F_EW_lvajj_vbs | 1 fake γ | (0,5) | 1 | n_prompt ≤ 1 | 81.9 | 0.30 ± 0.15 | fake factor |
| F_Wjj_pilot | 2 fake γ | W(→ℓν)+2 partons, fixed order | WF | n_prompt = 0 | 3.45·10⁶ | **1.51 ± 0.95** (3 combinations); f²×{0.09,1,9} | fake factor; lower bound (jets beyond 2 come from the shower) |
| T_tta_semilep | 1 fake γ | tt̄γ 1ℓ | WF3·WF_had | none (ZH lesson) | 773 | 0 combinations in window; 0.66 at VBS | fake factor; bound from production N |
| T_tWa_1l | 1 fake γ | tWγ 1ℓ (DR) | WF3·WF_had | none | 118 | 0 in window; 0.25 at VBS | fake factor |
| ZH:T_tWa (dilep) | 1 fake γ / lost ℓ | frozen ZH | WF² | — | 13.07 | 0.038 (1) | direct Delphes |
| ZH:T_tta (dilep) | | frozen ZH | WF² | — | 85.6 | pending (job still running at writing) | direct Delphes |
| tt̄ semileptonic, 2 fakes | 2 fake γ | not generated | WF3·WF_had | n_prompt = 0 | ~4·10⁵ (ranking) | bound pending | f²·b-veto; pilot needed |
| **ZH:Zγjj EW, e→γ + "lost" e** | e→γ fake | frozen ZH final, 500k | 1 | — | 11.05 | **1.71 ± 0.14** (156) | **direct Delphes e→γ (stock card, no pixel veto)** |
| **ZH:Zγjj QCD, e→γ** | e→γ fake | frozen ZH final, 600k of 6M | 1 | — | 69.46 | **1.39 ± 0.28** (24) × C | as above; D-WH-4 |
| γγjj + non-prompt ℓ | non-prompt ℓ | QCD (2,2) γγjj, VBS + 115–135 window (Q_aajj_vbs, 1k events through PY8+Delphes) | 1 | requires 0 reco leptons | 52.3 | 0.050 ± 0.011 (f_ℓ = 1e-4; ×0.3–10) | parametrised f_ℓ |
| W/γ+jets + non-prompt ℓ, multijet | | not generated | | | | f³ or f_ℓ·f², ranked negligible at order of magnitude | order-of-magnitude statement only |

## 3. Overlap removal (phase-space partition, as ZH, plus WH additions)
1. Prompt photons are counted from GenTruth (`lib/scripts/slim_gentruth.py`): pT > 15, |η| < 2.5, isolated. Wγγ keeps n_prompt ≥ 2, Wγ+jets keeps n_prompt ≤ 1, W+jets keeps n_prompt = 0.
2. **tt̄γ/tWγ are not overlap-removed** (the ZH A9 lesson: ME photons from top-decay products are missing). Double counting with tt̄γγ is bounded by the tt̄γγ yield.
3. EW/QCD are separated by coupling order. Signal and b-complement are separated by external flavour, with closure shown (report 01).
4. **WH-specific gap (D-WH-3).** On-shell W decay chains miss photons radiated by the W-decay lepton. At 0 jets with Wγγ generator cuts, σ(ℓνγγ)/σ(W(→ℓν)γγ chain) = 2.485/1.230 = **2.02 ± 0.02** (`Q_lvaa_0j`, `Q_waa_0j`, identical lepton and photon cuts). For ZH the analogous after-cut factor was only 1.128, because the m_ℓℓ and m_ℓℓγγ cuts removed FSR. WH has no such handle, so the dominant continuum may be underestimated by up to ×2.
   - The Wγ+jets ME (`l vl a j j`) does contain lepton radiation. Its n_prompt = 2 events (second photon from the shower) are discarded by rule 1, which leaves the configuration covered by neither sample.
   - **Options:**
     - (i) generate ℓνγγjj without the chain: QCD has 41 248 diagrams and looks feasible; EW has 67 536 diagrams for W+ alone and is heavy;
     - (ii) keep the on-shell chain and apply an analysis-level ratio from 0j/1j proxies with a conservative nuisance (the ZH approach);
     - (iii) both, with (i) for QCD.
   - **Recommended:** (iii).
5. **e→γ (D-WH-4).** The stock Delphes CMS card turns 7.5 % (signal) to 9.4 % (QCD WH) of generator electrons into photons (report 03 §3). This makes Z(→ee)γjj a 1ℓ + 2γ background of about 3 events at B0, more than the signal.
   - **Recommended:** (a) replace the intrinsic Delphes e→γ with a parametrised f(e→γ) ∈ {1, 2, 5} % (the ZH scenarios), and (b) add an m(eγ) Z-veto (|m_eγ − m_Z| > 10 GeV) and an M_T cut to the selection in Phase 05. Both are standard in Wγ analyses.

## 4. Lost-lepton coverage of the frozen ZH samples (handoff requirement)
- **Coverage inspected in the gridpack run cards:**
  - ZHjj and Zγγjj use an on-shell Z decay chain with `cut_decays = False`, so no generator lepton cuts apply. In the reused samples, 22–27 % of the 1-lepton events have the extra prompt lepton outside pT > 10 / |η| < 2.5, which shows that this region is populated. **Covered.**
  - Zγjj (`l+ l- a j j`, no chain) applies ptl > 10 and |η_ℓ| < 2.5. It covers only leptons lost through ID or isolation, which are 98 % of its 1-lepton events, and not out-of-acceptance leptons. **Partially covered.** A WH-specific sample would be needed if the out-of-acceptance component matters; in the other samples it is ≤ 27 % of lost-lepton events.
- **Delphes inefficiency dominates the "lost" leptons:** 70–75 % of ZH 1-lepton events have the second lepton in acceptance but not reconstructed (electron 57 %, muon 80 % efficiency in signal-like events, report 03). The ZH lost-lepton background therefore scales roughly with (1 − ε_ℓ) and is model-dependent. It goes into the robustness table (Phase 07).
- **Frozen-ZH constraints on the WH selection:** photon pT > 25 GeV and m_jj > 500 GeV (ZH Zγγ generation cuts pta > 25, mmjj > 400).

## 5. Generator-cut safety (twins, as ZH)
- **EW-type samples:** generator m_jj > 400 removes 2.1 ± 0.5 % of the reco-VBS region (signal, which has no generator m_jj cut; LHE–Delphes 1:1, `work/test/genmjj_safety.txt`). Safe, with a 2 % correction or uncertainty.
- **QCD-type samples:** 63 ± 7 % removed (QCD WHjj). **Unsafe.** Twins without the m_jj cut (`B_QCD_Waajj_nomjj`, `F_QCD_lvajj_nomjj`) provide the correction C = Y(twin)/Y(biased). At test-job statistics C ≈ 4.3 for Wγ+jets at VBS level. ZH found 2.05.
- **Photon pT:** the Wγγ/Wγ samples are generated with pta > 25, so the analysis must use pT(γ) ≥ 25 GeV. B0's 20 GeV is a validation baseline only (D-WH-5, recommended 25 GeV as in ZH).

## 6. MC-statistics requirement (handoff §1; `ledger.nmc_check`, N ≥ max(50k, σ·k·3000 fb⁻¹))
- Most samples need the 50k floor.
- The large requirements are F_QCD_lvajj_vbs 2.1 M, its nomjj twin 19 M (auxiliary), F_EW_lvajj 0.25 M, T_tta_semilep 2.3 M, T_tWa_1l 0.35 M and γγjj 0.16 M.
- **W+jets direct: 9.9·10⁹ events, infeasible (D-WH-6).**
  - **Proposed:** fake-factor weighting (no Delphes fakes) on a VBS-biased W+jets sample (m_jj, H_T generator filters proven with twins), declared as an exception with N_eff ≥ 10 in the SR. This mirrors the HH effective-N policy and would be a deviation from SPEC_G0 §1.5 requiring human approval.
- The single arm does not produce bulk samples (handoff §2.2). This table is the design record for the diff against the canonical arm.

## 7. Fake-rate parametrisation (NOT data-driven)
- f(j→γ) = 10⁻³ (pT/50)^−0.5, ×2 in the endcap, with fake pT = 0.85·pT(jet); scenarios ×{0.3, 1, 3}, squared for double fakes.
- f_ℓ (jet → isolated lepton) ∈ [3·10⁻⁵, 10⁻³], nominal 10⁻⁴.
- f(e→γ) ∈ {1, 2, 5} %.
- These are the ZH scenarios (ZH report 02 §4). Code: `wh/scripts/fake_bound.py`. Delphes jet→γ fakes are recorded but not used for the estimate.

## 8. Summary of first estimates at B0, 500 fb⁻¹ (validation level)
- Signal: 1.17.
- Prompt EW Wγγjj: 2.67 (×≤2 for D-WH-3).
- Fakes: Wγ+jets 1.6 (twin suggests up to ×4 more), W+jets 1.5, e→γ from Zγjj 3.1.
- Resonant: QCD WHjj 0.58, tHq-like 0.33, other H and lost-lepton ZH ≈ 0.3.
- The continuum and the fakes are smooth in m_γγ and are constrained by sidebands; the resonant terms are not. Feasibility will hinge on the m_γγ resolution (σ ≈ 2.1 GeV), the fake rates and the e→γ suppression. **No significance is claimed.**

## 8b. Photon pT 25 GeV re-evaluation (added at self-review)
B0 uses photon pT > 20 GeV, below the pta > 25 generator cut of the Wγγ/Wγ/Zγγ samples. Re-running all B0 numbers with pT(γ) > 25 GeV (`GPT=25`, `wh/work/b0_pt20_vs_pt25.txt`) changes the window yields as follows:

| Sample | pT > 20 | pT > 25 |
|---|---|---|
| signal | 1.17 | 1.10 |
| EW Wγγjj | 2.67 | 2.63 |
| QCD WHjj | 0.58 | 0.58 |
| Zγjj e→γ (EW + QCD) | 3.10 | 2.71 |
| frozen ZH lost-lepton | 0.23 | 0.22 |

The photons from a 125 GeV decay are hard, so the conclusions of §8 are unchanged. The fake bounds already used 25 GeV.

## 9. Caveats and next actions
- The test-job statistics are small (several components have ≤ 5 raw events or combinations). The ttH and tt̄γ semileptonic samples have no window support.
- The ggF H+jets and tt̄-double-fake bounds are not yet computed.
- `wh_baseline.py` does not apply the n_prompt overlap rule. The reused ZH Zγjj numbers may therefore double count events with two prompt photons, which belong to Zγγ; this is ≤ the Zγγ yield (0.17). The ZH Zγjj direct-Delphes numbers mix Delphes-intrinsic e→γ and j→γ, both untrusted, and the QCD-type generator-m_jj correction C is not applied to them.
- The QCD Wγγjj σ is pending (Phase 03).
- **Next:** human answers D-WH-3 … D-WH-7; then Phase 04 (canonical arm only).
