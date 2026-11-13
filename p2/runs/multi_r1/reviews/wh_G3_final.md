# G3 FINAL review, WH + VH (reviewer, opus, read-only; 2026-11-13; recorded by orchestrator)
**Verdict: HOLD.** There is one sev-1. Fixing it means relabelling and rewording existing numbers; no rerun is needed. Hand-recomputed: Eq.1 Z 0.434 / 1.063; exact-Poisson μ95 8.04; R_BR(−1/0/0.5) = 2.45 / 0.103 / 0.153; μ95(140) 17.3.

## Sev-1
1. **The λ=−1 headline depends on a sign convention.**
   - 6.2σ puts the sign on κW, with κZ = κt = +1. For the yield, (κW,κZ) = (−1,1) and (1,−1) are the same point, but at κZ = −1, R_BR = 1, which gives 3.76σ.
   - The extra 6.2 − 3.8 comes from the H→γγ sign of κW·κt, not from λWZ.
   - **Fix:** make 3.8σ primary (or quote both), state the convention, and drop the "samples as is" label.
   - λ<0 (0.37σ) is robust: with κZ<0 the γγ zero moves to λ ≈ −0.22. The noBR 1.61σ is not physical.
   - VH 14.1σ needs the same relabel.

## Sev-2
2. **Other-Higgs backgrounds** (12 % of b) are not rescaled under the coupling hypothesis; only the signal gets κ and R_BR. tHq grows ≈×10 at κW·κt<0. Probably conservative, but untested and unstated.
3. **The comparison paragraph contradicts the headline.**
   - It says the >5σ exclusions are "not reproducible" while the headline has 6.2σ.
   - It uses the asymptotic μ95 at 140 fb⁻¹ (b ≈ 0.5); use exact-Poisson.
   - It blames only the BR; √s, signal definition, LO and Delphes also differ.
   - For context: λ=−1 at 140 fb⁻¹ is ≈3σ; λ<0 is <1σ.
4. **The λ result is over-precise.**
   - Quote "expected ≈6σ (5.1–7.1 under ±30 % closure), asymptotic".
   - There are 4 bins with O(1) events and no toy or exact check of the 6σ tail.
   - The ±30 % closure is not shown to cover the 3.3σ LOO pulls.

## Sev-3
5. **Stale v2.1 labels:**
   - 07:2 says "v2.1";
   - N_eff 135 (should be 63);
   - 06 still lists C_eFake/cov_eFake (replaced by ps_qcd in v1.1);
   - the 06 §3 ranking is v2.1;
   - final.json /selection b 1.801 / neff 135;
   - ggf_variant Z_eq1 0.453 uses a different window.
6. **ZH channel:** described as one bin per process but merged into one sample in the code; "ZH alone" is copied, not refit. Small effect (0.444 vs 0.447).
7. **λ combination:** stated and acceptable. Document that the ZH curve uses the same κW-sign convention as #1.
8. **(κW,κZ):** computed (map2d) but not reported. c_A: not done, cost stated (acceptable).
9. **Independent reproduction is partial:** only s/b/Z counting. PL, couplings and combination are reproduced by the verifier only.
10. **ggF proxy:** acceptably conservative. Rename it from "95 % UL" to "scaled proxy"; note that gluon jets may fake more; include it in the D36 npl ×3 scan.
11. **ZH erratum:** conclusions hold and are used consistently. Inconsistency: ZH calibrates to CMS-SMP-19-013 (κ 0.956) while WH D39 calls it non-comparable (c=1). Negligible.

**Q2, v1 vs v1.1:** keep v1.1 nominal (pre-declared by 04:139 and D45; agrees with v1). Add v1 (vbs×C) as a robustness row in 06 §5, and disclose that the lost-lepton N_eff 7.6 is below the SPEC §4.3 N_eff ≥ 10.

**Conditions to lift the HOLD:** #1 and #3 relabel/rewording; #4 wording; state #2. The rest is sev-3 cleanup.

**Open human decisions:** D39-D42, D43 (missing from STATUS) and D45 cannot change a headline. D44 (MVA, +35-40 % Z) can. NEW: the λWZ sign convention can (6.2σ vs 3.8σ).

## G3 recheck (reviewer, opus, read-only; 2026-11-13; recorded by orchestrator)
**Verdict: APPROVE-with-conditions.** No sev-1 remains, so the gate auto-passes under D20.

1. **#1 resolved.**
   - Convention stated (07:84). 3.8σ is primary; ≈6σ (5.1–7.1) is labelled convention-dependent and "NOT the headline". R_BR = 1 is labelled unphysical.
   - λ<0: 0.35σ (κZ convention) / 0.37σ (κW convention), matching the JSON values (0.347 / 0.370; Z(λ=−1) 3.764 / 6.197).
   - VH 3.8/5.3/8.9σ is plausible and ZH was not dropped: 3.764² + 0.429² → 3.788 = stored 3.79.
   - The ZH fixed-BR curve slightly overstates the ZH term for −1<λ<0 (<0.02σ, labelled).
2. **#2–#4 resolved:**
   - other-Higgs statement (07:90, FINAL:16);
   - comparison: exact-Poisson 17.5 at 140 fb⁻¹, 2.0σ / 3.3σ by √L, no tension;
   - precision wording (07:91).
3. **#5–#11 and Q2 resolved:** v1 robustness row; N_eff 7.6<10 disclosure; VH md matches code; ggF relabelled with the npl×3 variant; 08 v1.1 chain.
4. **Remaining sev-3** (labels only, to fix before the freeze):
   - (a) The closure_sensitivity block in couplings_kzneg is κW-convention, so the 3.8σ primary lacks its ±30 % band; the κZ λ D36 scan is missing from 07.
   - (b) Stale or legacy keys in final.json.
   - (c) 07:87: the γγ zero is at λ≈−0.22 in the κZ convention.
   - (d) Stale "UL" and v2.1 labels in 07:144, 05a:226 and 06:6.
   - (e) Disclosed limitations: reproduction covers counting only; additive-q combination without WH–ZH correlation.

**Open human decisions:**
- Can change a headline: D46 (3.8σ vs ≈6σ at λ=−1; VH 8.9σ vs 14.1σ at 3000 fb⁻¹) and D44 (+35–40 % Z if the MVA is primary).
- Cannot: D39, D40, D41, D42, D43, D45, and the D38 substitution.
