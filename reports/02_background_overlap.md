# Phase 02 — background matrix and overlap ledger

Date UTC: 2026-11-02. **Status: BLOCKED (ledger complete as design; sign-off requires executed overlap/merging validation in Phase 04).** Author: Claude Code (Opus 5.5), single session.
Machine-readable matrix: [`config/sample_matrix_phase02.yaml`](../config/sample_matrix_phase02.yaml). Candidate cards: [`cards/phase02_candidates/`](../cards/phase02_candidates/README.md) (UNVALIDATED). Signal definition and BR inputs: [01_signal_process.md](01_signal_process.md) + [01_addendum_claude.md](01_addendum_claude.md). Executed cross sections cited here come from [03_generation_validation.md](03_generation_validation.md).

## 1. Final state and measurement definition
Reco target: OS-SF ee/μμ with m_ll in a Z window, ≥2 isolated photons with m_γγ in a Higgs window (sidebands reserved, Phase 06), ≥2 VBS tag jets. **Signal = EW (0,4) ZHjj only** (D1). Everything producing a resonant m_γγ peak but not EW ZHjj is a *resonant background* and is fitted with the signal shape; continuum processes are constrained by m_γγ sidebands.

## 2. Ledger (one row per component; details/cuts/targets in the YAML)

| ID | Role | Generator / order | Jets & merging | Decays / BR ledger | Overlap rule | Relevance (justification) |
|---|---|---|---|---|---|---|
| S_EW_ZHjj | signal | MG5 LO (0,4) `z h j j`, Z→ll ME chain | fixed 2j + PS (dipole recoil) | Z in ME (rescale to PDG B_l); B_γγ external once, PY8 forced γγ | order-exclusive vs QCD ZH | σ_prod=18.64±0.19 fb (loose jets) → ≤1.43 events×acc at 500 fb⁻¹ |
| S_..._offshell | systematic | (0,5) `l+ l- h j j` | as above | B_γγ only | alternative, never added | pole-approx check |
| H_QCD_ZH_mlm | resonant bkg | MG5 LO ZH+0,1,2j | MLM (xqcut 15 / qCut 25, TBV) | as signal | contains only QCD-order 2j ME; do not add fixed ZHjj | fixed-order (2,2) ZHjj→ll = 10.25 fb ≈ 8× EW at loose cuts — **dominant resonant bkg**; VBS cuts are the discriminant |
| I_ZHjj | signed interf. | MG5 `QCD^2==2 QED^2==6` | fixed | as signal | separate signed term | −0.61% of EW at loose cuts (03); re-evaluate in VBS region |
| H_ggZH | resonant bkg | MG5 loop_sm `g g > z h [noborn=QCD]` | 0j + PS | as signal | distinct initial state; no tree overlap | O(10–15%) of inclusive ZH, VBS-jet tail suppressed; must be estimated |
| H_ttH | resonant bkg | MG5 LO (2,1) dileptonic | 0j + PS | t→blν in ME; B_γγ external | distinct (external tops) | σ·B_γγ·B(dilep SF)≈1.2 fb·0.0235 → O(1) evt pre-cut — comparable to signal; b-veto + m_ll |
| H_tHW, H_ZH→ττ | resonant, small | as YAML | — | — | distinct | O(0.05–2) evt pre-cut, mostly removed by m_ll window; estimate with small samples |
| ggF/VBF/WH/bbH/tHq | documented negligible | — | — | — | — | ≤1 prompt lepton; needs fake lepton with m_ll≈m_Z (f_ℓ≲1e-3) → <1e-2 evt |
| B_EW_llaajj | continuum | MG5 LO (0,6) | fixed 2j | ll in ME; no BR | order-exclusive vs QCD | reference signal; smooth in m_γγ |
| B_QCD_llaa_mlm | continuum | MG5 LO llγγ+0,1,2j | MLM xqcut 10 / qCut 20 | — | defines ≥2-prompt-γ region | expected largest continuum |
| I_llaajj | signed continuum | `QCD^2==2 QED^2==10` | fixed | — | separate | smooth → absorbed by sideband fit; quote size |
| F_QCD_lla_mlm, F_EW_llajj | 1 fake γ | MG5 llγ+0..3j MLM / EW (0,5) | MLM | — | **veto events with ≥2 prompt γ** | fake-rate scenarios |
| F_Zjets_mlm | 2 fake γ | MG5 ll+0..4j MLM | MLM | — | **veto ≥1 prompt γ** | f²·σ(Z+≥4j) not negligible a priori (reference neglected it without justification) |
| T_ttaa / T_tta / T_tWa / T_tt | prompt / 1 / 1 / 2 fakes | MG5 LO dileptonic | 0j+PS | t decays in ME | photon-count vetoes as above; tWγ DR (DS as syst) | b-veto, m_ll window |
| V_WZa / ZZa | e→γ | MG5 LO | 0j+PS | in ME | photon-count veto | Delphes lacks pixel-seed veto → parametrised f_e→γ |
| W/γγ + fake ℓ | documented negligible | — | — | — | — | <1e-2 evt |

## 3. Overlap-removal contract (phase-space partition, not ancestry labels)
1. **Prompt photon** defined once (YAML `prompt_photon_def`) at particle level after PY8 (ME + QED-shower photons, no hadron ancestor), with the *same* p_T/η/ΔR thresholds as the ME generator cuts of the higher-multiplicity sample.
2. Let N_pγ be the number of such photons. Z+jets keeps N_pγ=0; Zγ(+jets) keeps N_pγ=1; Zγγ(+jets) keeps N_pγ≥2 (it is generated with those cuts, so events failing them after shower are kept only if N_pγ≥2 — residual migration quantified). Same rule for tt/ttγ/ttγγ.
3. Shower QED emission must be ON in all samples (otherwise FSR photons below/above ME cuts are double-missing). The partition is validated (Phase 04) by (a) continuity of photon p_T and ΔR(γ,ℓ) at the 15 GeV / 0.4 boundaries in the stitched sum, (b) varying the threshold 15→20 GeV and checking stitched-sum stability.
4. EW vs QCD: separated by coupling order (verified by diagram counts, 01_addendum). Interference terms carried as signed separate components; never as positive unweighted events.
5. MLM: xqcut/qCut validated by differential jet rates (DJR) and σ stability (Phase 04). Fixed-order ZHjj/llγγjj only as cross-checks, never added to merged samples.
6. Resonant vs continuum: no SM tree H→γγ vertex, so H-pole/continuum interference is absent from the generated samples; physical effect (mass shift ~O(100 MeV), rate O(1%) in ggF literature) is quoted as a caveat, not modelled.

## 4. Fake-rate parametrisation (NOT data-driven)
Per-object probabilities applied as event weights to jets/electrons **not** matched to prompt photons; Delphes' intrinsic object fakes are recorded but not trusted (no pixel-seed veto, simplified π⁰ isolation). Scenarios (YAML `fake_scenarios`): f_j→γ = 1e-3·(p_T/50)^-0.5 (×2 endcap), multiplied by {0.3, 1, 3}; f_e→γ ∈ {1, 2, 5}%; f_ℓ ∈ [3e-5, 1e-3]. Double fakes scale as f². Fake-photon p_T = x·p_T(jet), x~N(0.85,0.10). Ranges chosen to span typical published tight-ID LHC fake rates within ~±0.5 decades; they are **scenarios**, the result must be quoted per scenario.

## 5. MC statistics targets
Rule: effective MC events in the final signal window ≥ max(100, 10·N_exp) per component so MC-stat ≤ 30% of the expected Poisson error; components failing this receive an MC-stat nuisance (Barlow–Beeston-lite) and are flagged. Concrete per-sample event counts: [04_production_plan.md](04_production_plan.md).

## 6. Checks done / required
Done (executed, see 03): order separation by diagram count (EW 1344 + QCD 520 = combined 1864 diagrams); LO σ for EW, QCD, interference ZHjj; candidate cards parse in MG5 3.6.3. Required before PASS: prompt-photon partition test (§3), DJR plots, ttH/ggZH σ, fake-weight code unit test, Delphes photon/fake inspection.

## Caveats / next
No yields after selection exist yet. Relevance column uses executed σ (ZHjj) or order-of-magnitude σ·BR arithmetic with stated inputs (YR4 13 TeV inclusive Higgs σ, used **only** for ranking; 13.6 TeV values to be archived before use in yields). Next: Phase 04 overlap/merging validation on batch samples.
