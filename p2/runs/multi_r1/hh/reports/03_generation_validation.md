# Phase 03 — Generation validation (boosted VBF HH → bb̄bb̄)

- **Date UTC:** 2026-11-03 (start/end in PROGRESS.md)
- **Status: PASS for the 10 sample types that have a gridpack and a successful test job** (signal SM, ggF HH, VBF H, ZH, ttH, tt̄, Z+jets, ZZjj, Q_bbjj, Q_4j_vbs); σ, BR and morphing closures pass; verifier audits passed. **NOT met:** handoff-listed types W±H, ggH + jj, W + jets, QCD 4b, tt̄jj are planned only (no gridpack, no test job) — required before G2 (D-HH-7, §13). G1 review: PASS-with-conditions (`reviews/hh_01-03.md`); open decisions D-HH-1 … D-HH-12 (02 §9, STATUS.md)
- **git commit:** recorded by orchestrator

## 1. Goal
Smoke tests, σ closure, BR closure, morphing closure on ≥ 2 independent points, Delphes object validation on small samples (large-R jets, groomed mass, VBS jets, truth-tag weights), one HTCondor test job per sample type with EOS stage-out, seeds unique by construction. All numbers are validation numbers, **not yields**.

## 2. Inputs / versions / seeds
Stack, UFOs, cards, seeds: see 01 §2. Delphes card: `cards/delphes/delphes_card_CMS_slim_hh_v1.tcl` (patch 002). Pythia8 settings: `lib/cards/phase03_smoke/py8_common_CP5.cmnd` + `cards/py8/py8_{hh_bb,vh,tt,qcd}.cmnd` (CP5, NNPDF3.1 NNLO; H→bb̄ forced / V hadronic forced; PY8 seed = MG seed + 10⁸; Delphes `RandomSeed` pinned by `run_py8_delphes.sh`). Job wrappers: `scripts/condor/{make_gridpack_hh,run_job_hh}.sh` (patches 004/005). Condor: EosSubmit schedd; `condor_q` checked before each submission (no duplicates; the WH executor's jobs share the user name and were not touched).

## 3. HTCondor jobs, provenance and exit-code hygiene
| Purpose | Cluster | Jobs | Outcome |
|---|---|---|---|
| Gridpacks, first batch (kV/k2V/kl **fixed to 1** by MG5 restriction: UFO bug 1) | 884453 (18), 884454 (3) | 21 | background gridpacks (T, ttH, VBFH, ZH, Zjj, ZZjj, Q_bbjj, Q_4j, ggHH-kl1) valid and **used**; every HH-model gridpack of this batch (S_*, V_*HH*; moved to `work/gridpacks_bad_kappa_fixed/`) **discarded** (σ identical at all points). 884453.009 (G_ggHH_loop_kl1, old model) and 884454.000 (V_HHjj_SM_noSchanV) were `condor_rm`-ed by me (event 009 "aborted"; 884454.000 also logged evicted code 1023) because they depended on the faulty model; no output used. The tarball `work/gridpacks/G_ggHH_loop_kl1_*` (seed 3120000) is the output of 884453.9 (first-batch model, kl fixed to its SM value 1; the removal raced with job completion): σ = 0.01441 pb equals the v2 build, but it is **not used** |
| Rerun after bug 1 (defaults 1.337 → kappas **merged** into one card entry: UFO bug 2) | 884455 (13) | 13 | `condor_rm`-ed by me while running (884455.009 logged "aborted"); outputs not used |
| Rerun after bug 2 (distinct defaults 1.11/1.22/1.33) into `work/gridpacks/` | 884459 (13) | 13 | **did run**, rc 0, wall 38–145 s, corrected model (verified: σ differ with κ). My earlier statement that it "exited at output exists" was wrong. Because of EOS versioned ghost entries the files appeared late and I resubmitted to a new directory |
| Same 13 cards into `work/gridpacks_v2/` (**used for all test jobs**, closure, σ table) | 884461 (13) | 13 | rc 0, σ identical to 884459 for all 13 samples (same seeds, deterministic integration); tarballs differ bytewise (sha256 differ: tar metadata), σ equal |
| ggF HH κλ = 0, 2, 5 gridpacks | 884465 | 3 | rc 0 (σ in §6) |
| LHE closure (5000 ev, J=2) | 884463 | 10 | rc 0 |
| Test jobs (2000 ev; gridpack → LHE → PY8 → Delphes → truth/slim → EOS) | 884462 (7 types), 884464 (Q_bbjj), 884466 (ggF HH), 884577 (Q_4j_vbs) | 10 | first 9 rc 0, LHE = Delphes = 2000; Q_4j see §9 |

**Which tarball each sample uses.** Background samples T_ttbar_boost, H_ttH_bb, H_VBFH_bb, H_ZH_Zqq_bb, V_Zjj_QCD_vbs, V_ZZjj_EW, Q_bbjj_vbs, Q_4j_vbs: `work/gridpacks/` (cluster 884453). All HH-model samples (S_HHjj_* incl. twin, V_HHjj_SM_noSchanV, V_ZHH/V_WHH, G_ggHH_loop_kl{0,1,2,5}): `work/gridpacks_v2/` (884461 / 884465; for G_ggHH_loop_kl1 the `work/gridpacks_v2/` build of seed 3120000 — a second tarball of the same seed with the same σ, 0.01441 pb, also sits in `work/gridpacks/`; it is not used). The copies of the S_*/V_* gridpacks in `work/gridpacks/` (884459) are valid but unused duplicates (σ identical).

**Exit-code hygiene.** 884459 was not a no-op (see above). The real hazard is a rerun that finds an existing (or EOS-ghost) output and exits 0 without doing anything: both wrappers (`make_gridpack_hh.sh`, `run_job_hh.sh`; patches 004/005a) now print `NOOP …` and exit **30**. EOS lessons: (a) `mv` of an output leaves versioned ghost entries (`.sys.a#.v#…`) that `xrdfs stat` matches; (b) MG5 restriction fixes/merges kappa parameters (01 §2.1). The `python3 -I`/`-P` note: scripts here are run after `source setup_stack.sh` (Python 3.13); the login-node system python3 (3.9) lacks `-P` and numpy.

## 4. σ closure (gridpack MG5 integration vs LHE `xsecup` vs Pythia8 σ_gen)
(`scripts/sigma_closure.py` → `work/sigma_closure.md`; 2000-event test jobs)

| sample | test seed | N_req | N_LHE | N_Delphes | σ gridpack [pb] | σ LHE-init [pb] | σ PY8 [pb] | LHE/gridpack | PY8/LHE |
|---|---|---|---|---|---|---|---|---|---|
| G_ggHH_loop_kl1 | 3120001 | 2000 | 2000 | 2000 | 0.01441 | 0.014371 | 0.01437 | 0.997 | 1.000 |
| H_VBFH_bb | 3150001 | 2000 | 2000 | 2000 | 2.461 | 2.5031 | 2.505 | 1.017 | 1.001 |
| H_ZH_Zqq_bb | 3151001 | 2000 | 2000 | 2000 | 0.08438 | 0.08465 | 0.08444 | 1.003 | 0.998 |
| H_ttH_bb | 3154001 | 2000 | 2000 | 2000 | 0.248 | 0.25082 | 0.2507 | 1.011 | 1.000 |
| Q_4j_vbs | 3130001 | 2000 | 2000 | 2000 | 37660 | 37548 | 37580 | 0.997 | 1.001 |
| Q_bbjj_vbs | 3131001 | 2000 | 2000 | 2000 | 725.4 | 720.8 | 721.2 | 0.994 | 1.001 |
| S_HHjj_kV1_k2V1_kl1 | 3111001 | 2000 | 2000 | 2000 | 0.001153 | 0.001135 | 0.001136 | 0.984 | 1.001 |
| T_ttbar_boost | 3140001 | 2000 | 2000 | 2000 | 30.83 | 30.77 | 30.8 | 0.998 | 1.001 |
| V_ZZjj_EW | 3163001 | 2000 | 2000 | 2000 | 0.0765 | 0.076688 | 0.07643 | 1.002 | 0.997 |
| V_Zjj_QCD_vbs | 3160001 | 2000 | 2000 | 2000 | 270 | 269.05 | 269.8 | 0.996 | 1.003 |


All LHE/gridpack ratios within 1–2 σ_MC (2000-event LHE; largest deviation −1.6 % for the signal, 1.7 % for VBF H), PY8/LHE within 0.3 %: the shower step preserves the normalisation, and N_LHE = N_Delphes = N_requested for all samples (no lost events). Closure for all κ-points of the signal at gridpack-vs-LHE level (5000 events): 01 §5.2.

## 5. BR closure
See 01 §7 (`work/br_closure.json`): H→bb̄ = 1.000 in all Higgs-bearing samples; Z→qq̄ forced (b̄b share 0.2115/0.2185/0.2135 vs PDG 0.216); inclusive W→qq̄ in ttH = 0.6845 ± 0.0073 vs 0.6741. The physical BR enters once through the ledger; `nmc_check_hh.py` asserts br_total = product(ledger).

## 6. Morphing closure and generator-cut safety (parton level; validation only)
Details and tables in 01 §5.2 / §3.1: σ closure pulls 0.2 and −0.3 (T1, T2), distribution closure χ²/ndf ≈ 1 for m(HH), pT(H1), m(jj), |Δη(jj)| at both independent points; VBS generator filter twin: anchor-level σ 0.951 ± 0.015 fb (filtered) vs 0.943 ± 0.017 fb (unfiltered twin). `scripts/morph_closure.py`, `work/morph_closure.json`, `work/twin_check.txt`.
**ggF HH kappa-lambda closure (loop_sm_kl, MG5 LO gridpack sigma):** sigma(kl=0,1,2) = 30.09 ± 0.14, 14.41 ± 0.09, 6.80 ± 0.05 fb; quadratic fit sigma = A kl^2 + B kl + C with (A,B,C) = (4.036, -19.716, 30.090) fb; predicted sigma(kl=5) = 32.41 ± 1.63 fb vs direct 33.44 ± 0.14 fb (pull -0.63). The kl-dependence is therefore applied by the patched model (sigma varies with kl as the triangle/box structure requires) and closes on an independent point.


## 7. Delphes object validation (2000 events per sample, `scripts/delphes_validation.py`, `work/delphes_validation.json`, `figures/val_*.png|pdf`)
Large-R jets (anti-kT 0.8, EFlow, pT > 250, |η| < 2.4); "contained" = both b quarks from H→bb̄ within ΔR < 0.8 (truth).

| Sample | ≥ 1 fat jet | ≥ 2 fat jets | H→bb̄ contained / gen H | m_SD of contained H: p16 / p50 / p84 [GeV] | nB = 2 fraction | τ21 median |
|---|---|---|---|---|---|---|
| S_HHjj SM | 6.3 % | 2.55 % | 1.7 % (61 % for 300 < pT(H) < 400, 93 % for pT(H) > 400: 38/62, 25/27) | 89 / 116 / 130 | 0.955 | 0.29 |
| H_ZH_Zqq_bb | — | 12.9 % | 8.3 % | 99 / 118 / 133 | 0.958 | 0.29 |
| H_ttH_bb | — | 14.0 % | 4.7 % | 103 / 126 / 166 | 0.713 | 0.37 |
| H_VBFH_bb | — | 1.1 % | 0.85 % | 88 / 109 / 126 | 1.0 | 0.23 |

Findings: (i) the soft-drop mass peaks at 116–118 GeV for contained H→bb̄ (soft-drop shifts the peak low by ~7–9 GeV; ungroomed median 119–120 GeV), with a width (p84−p16)/2 ≈ 20 GeV — the m_SD window will be set blinded-style in Phase 06; (ii) containment is efficient only for pT(H) ≳ 300 GeV and only 10 % of SM-signal Higgs bosons exceed 200 GeV (399 of 4000): the SM boosted acceptance is small (confirms D-HH-5); (iii) τ21 median 0.29 for contained H→bb̄ (consistent with a 2-prong population; no cut applied).

**VBS jets** (`scripts/vbs_reco_vs_parton.py`): any opposite-hemisphere AK5 pair (pT > 30, |η| < 4.7) with mjj > 500, |Δη| > 3.5: reco 0.763 ± 0.010 vs parton-level 0.834 (LHE, hardest two non-Higgs partons), i.e. 91 % jet-level retention; ≥ 2 AK5 jets not overlapping fat jets in 99.6 % of signal events (`work/vbs_reco_vs_parton.txt`).

**Truth-tag weights** (`scripts/delphes_validation.py` illustrative; `scripts/sr_feasibility.py`): the truth labels (nB, nC, nHb, nVq, nWq, ntb) are filled for every fat jet; fat-jet census for `V_Zjj_QCD_vbs`: 94 light, 19 c, 5 b, 7 bb among 125 selected jets; mechanism check: for the SM signal the weighted sample has N_eff = 2.0 vs N_raw = 2 in the anchor SR. The three scenario weights are applied in `sr_feasibility.py` (02 report §8): they confirm the effective-N problem (N_eff ≈ 1–2 for tt̄/ttH, 0 for QCD) at 2000 generated events; they are **not** yields.

Fat-jet limitations repeated: no JES for fat jets, no fat-jet b-tag, no cleaning of leptons/photons (02 §5).

## 8. Resource and storage
Measured: gridpack build 0.5–2.5 min (signal, 4 cores), 9.5 min (ggF HH loop), 12 min (ZZjj), 25 min (Q_bbjj); test jobs ≈ 2.5 min per 2000 events (PY8+Delphes ≈ 0.06 s/event). Slim output 2.3–5.2 kB/event (Q_4j 5.2); full ROOT (with Particle) ≈ 95 kB/event kept only for tests (`work/test/*_full.root`, 190 MB each for signal-like). Storage estimate: 02 §10.

## 9. Open items at the time of writing
- `Q_4j_vbs`: gridpack rc 0 (43 min, σ = 3.766e4 ± 73 pb), test job 884577 rc 0, LHE = Delphes = 2000, σ closure in §4 (LHE/gridpack 0.997, PY8/LHE 1.001). Fat-jet census: in the 2000 events 153 have ≥ 2 fat jets pT>300, 10 pass the VBS pair, 0 the mass window; fat-jet truth census (pT>250): 1213 light, 168 c, 28 b, 32 bb. Brute-force N for σ·L = 1.1×10¹¹: effective-N policy only.
- Background twin samples for cut safety (ihtmin, VBS filter) not generated (required before G2).

## 10. Exact commands
```
condor_submit scripts/condor/gridpacks_hh_rerun2.sub ; scripts/condor/gridpacks_hh_ggHH.sub ; scripts/condor/lhe_closure.sub
condor_submit scripts/condor/test_hh_A.sub ; test_hh_B.sub ; test_hh_C.sub        # (module load lxbatch/eossubmit; EOS path /eos/user/r/rjiang/...)
python3 -P scripts/sigma_closure.py ; scripts/br_closure.py work/test work/br_closure.json
python3 -P scripts/delphes_validation.py work/test work/delphes_validation.json figures
python3 -P scripts/sr_feasibility.py work/test config/sample_matrix.yaml config/tagging_scenarios.yaml work/sr_feasibility.json
python3 -P scripts/morph_closure.py work/lhe work/morph_closure.json
```

## 11. Caveats and next actions
Small statistics (2000 events); parton-level closure; fat-jet limitations; tagging assumptions; an accidental HEPTools install attempt in the frozen ZH MG5 tree (D-HH-1, removal blocked by a permission rule — needs a human `rm -rf software/install/MG5_aMC_v3.6.3/HEPTools`; partial ninja/oneloop only, no effect on ME generation observed; diagram audits and the loop-model check afterwards ran in a private MG5 copy, `work/mg5priv`, whose file differences to the frozen install are recorded in §14). Next: decisions D-HH-1…12, then (G2) production plan with N and twin proofs.

## 12. Post-audit corrections (verifier items)
1. **BR rounding:** `br_total` is now stored at full precision (`scripts/hh_samples.py`), strict 1e-9 check kept. 2. **Repeated factor:** ledger entries are labelled per decaying particle (`B_bb@H1/@H2`, `B_Zqq@Z1/@Z2`); only an identical repeated label is an error, so ZZ→qq̄qq̄ passes. 3. **Role wiring:** the strict signal rule applies to roles `sig`, `basis`, `closure` (role normalised by the prefix before "(", so `closure(kl)` = G_ggHH_loop_kl5 is checked, N_MC_required 50 000); rows without σ are reported as "planned, unchecked" (6 rows); self-test now checks basis and closure samples with low N and all violations are listed; `python3 scripts/nmc_check_hh.py config/sample_matrix.yaml` passes on the real registry (signal rows evaluated against the planned N). 4. **Provenance** and 5. **exit-code hygiene:** §3. 6. **Q_4j:** §9/§4. 7. **B(H→bb̄):** LHCHWG YR4 SM prediction at mH = 125.0 GeV (model mass), 0.5824; no PDG SM value exists; note closed (01 §7).

## 13. Pre-G2 plan (G1 review items 3, 5, 6, 8; **not run now**)
1. **Morphing closure in the analysis phase space (item 3).** (a) One closure point with κV ≠ 1 **and** κλ ≠ 1 (e.g. (1.25, 1.5, 2)) that probes the κV³κλ, κV²κλ², κVκ2Vκλ monomials; (b) closure at **Delphes level in the SR** (two fat jets + VBS pair + m_SD window, not inclusive parton level), with ≥ 50 k events per basis point from the production samples; (c) tabulate Σ|c_i| and the resulting MC-stat amplification √(Σ c_i² σ_i²/N_i)/σ(κ) over the intended scan ranges (κ2V ∈ [−1, 3], κλ ∈ [−5, 10], κV = 1), noting that basis σ span 1.15–119 fb (cancellations); (d) define the usable κ range from the amplification, not from the nominal grid.
2. **`ul_fb` provenance (item 5).** Extend `nmc_check_hh.py` so a bound is accepted only if it is a structured record (method = Poisson 95 % with the maximum event weight, raw count, weight scale, σ·BR·L) that the checker **recomputes**, and only if the conservative variant (background set to the bound) is produced as a named output of the analysis; a bare number fails.
3. **Class-resolved N_eff (item 6).** For each QCD/tt̄ sample, estimate from the 2000-event tests and the truth classes (top/Hbb/bb_nonH/b/c/l per leading fat jet) the per-class SR fractions and N_eff = (Σw)²/Σw²; pick the generation strategy accordingly (e.g. b-enriched or g→bb̄-enriched PS filter for Q_4j, validated by a twin), instead of scaling raw counts.
4. **Background twins (item 8).** Small twins with looser ihtmin (350 vs 500), no VBS filter, ptheavy variations, compared **in the boosted tail** (two fat jets, VBS pair) at Delphes level for Q_4j, Q_bbjj, T_ttbar_boost, V_Zjj, H_VBFH, H_ZH, ttH; signal twin repeated in the boosted tail (currently only inclusive parton level).
5. **Missing sample types (item 7):** gridpack + test job for W±H, ggH + jj (HEFT), W + jets, QCD 4b, tt̄jj; and the §9b extra backgrounds.

## 14. Private MG5 copy (`work/mg5priv`) and checksums (G1 review item 9)
`work/mg5priv/MG5_aMC_v3.6.3` was unpacked from `software/install/MG5_aMC_v3.6.3_install.tgz` (sha256 recorded in `software/install/MG5_aMC_v3.6.3_install.tgz.sha256`) to run the interactive κ-card test without touching the frozen tree after the HEPTools incident; differences to the frozen install (computed with `diff -rq`, excluding `__pycache__`):
- added directory `models/sm_kVk2VkL/` (only difference in `models/`); tarball sha256 in `config/ufo_checksums.txt` (8e64d068… final build); file sha256 (first 16 hex):
  `__init__.py` 9479d2a94b3768fe; `build_restrict.py` 7ab830b794068cd9; `coupling_orders.py` c89fc6f38d118a50; `couplings.py` 1374d62ef11f7908; `decays.py` 8202bda5e0bbf765; `function_library.py` 10a39383a5494a7a; `lorentz.py` 09f9eb3be5f23099; `object_library.py` 15844c4e89f687c6; `parameters.py` 92b8663b3a377189; `particles.py` 5a18af7aadba847f; `restrict_c_mass.dat` 2e3fb3788662af7b; `restrict_ckm.dat` 2e7707e70469131c; `restrict_default.dat` 9567eda39ddaaae5; `restrict_lepton_masses.dat` 759314bb75df4a79; `restrict_no_b_mass.dat` f70e78f24b4c8ec2; `restrict_no_masses.dat` ef7072565776c624; `restrict_no_tau_mass.dat` 278e9d5ccb3f332f; `restrict_no_widths.dat` d5c1a7e36979d25a; `restrict_zeromass_ckm.dat` 95a1531740b87770; `vertices.py` 0a4d978fb87f2512; `write_param_card.py` e804608eedfdafbc.
- `input/mg5_configuration.txt`: sha256 private 49991edbebf5… vs frozen 257fba1e82a6… (MG5 rewrites this file at every run: lhapdf path etc.; the frozen copy is also changed by every ZH/WH run, so a clean comparison is not possible).
- no `HEPTools` directory in the private copy (the loop gridpacks ran on workers from the tarball, CutTools only). `__pycache__` and the compiled `py3_model.pkl` are excluded.

