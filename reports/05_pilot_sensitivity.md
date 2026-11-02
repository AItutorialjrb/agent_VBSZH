# 05 — Pilot sensitivity (expected quantities only, no new bulk MC)

- **Date (UTC):** 2026-11-02
- **Status:** PASS (pilot). The conclusion (signal count s < 1 event at every luminosity considered) holds under every background variation tried. Individual background yields are labelled ESTIMATE wherever MC support is below 10 raw events.
- **Goal:** Before deciding D12 (whether to run `production_v2`), estimate the sensitivity using existing cross sections, the Tier-1 signal and QCD ZHjj samples, and pilot/test samples only.
- **Code:**
  - `scripts/analysis/ntuple.py` → `scripts/analysis/sensitivity.py` → `scripts/analysis/tables05.py`.
  - Outputs: `work/m7_analysis/*.npz` and `work/m7_analysis/sens_final.json`.
- **Detector model:** stock Delphes 3.5.1 CMS card physics (`delphes_card_CMS_slim_v1.tcl`, which only drops output branches, with RandomSeed pinned).
  - D11 b/c is **not adopted**: the electron-priority and isolation changes alter the detector model and are not a fix that restores stock-card behaviour.
  - Keeping the stock card preserves comparability with arXiv:2512.07689.

## 1. Normalisation checks

### 1.1 BR(H→γγ) applied exactly once (forced-decay samples)

| check | evidence | result |
|---|---|---|
| Pythia forces H→γγ with conditional BR = 1 | `cards/phase03_smoke/py8_{ew,qcd}_zhjj_haa.cmnd`: `25:onMode = off`, `25:onIfMatch = 22 22`; the same cmnd is used for ttH. | forced |
| Pythia does **not** fold the BR into σ | Tier-1 job json, `production/v1/ew_zhjj_zll/*_s13611000.json`: LHE σ = 1.3015e-3 pb; Pythia `sum` line = 1.306e-12 mb = 1.306e-3 pb, equal to LHE σ_max. QCD: 1.0157e-2 pb (LHE) vs 1.017e-2 pb (PY8). | σ_PY8 = σ_LHE |
| Every event has H→γγ | Generator record of `production/test/{ew,qcd}_zhjj_zll/*.root`: 2000/2000 events each have last-copy H → γγ. Same check on `work/m7_pilot_reco/ttH_dilep/full.root`: 500/500. | 100 % |
| BR applied in the analysis, once | `scripts/analysis/sensitivity.py` registry: k = ZF × B_γγ for EW and QCD ZHjj, k = B_γγ for ttH, k = 1 for all non-Higgs samples. B_γγ = 0.002270; ZF = 0.9783 (PDG/MG5 Z→ℓℓ). No other factor is applied anywhere in the chain. | once |
| Z→ℓℓ | In the ME (ee+μμ, both flavours). ZF rescales the MG5 width-derived BR to PDG. ττ is not included in the signal definition. | once |

Signal normalisation is σ_EW = 1.2946 ± 0.0009 fb. This is the inverse-variance mean of the 100 Tier-1 jobs and agrees with the test job (1.2964 ± 0.0097 fb).
- σ_EW × ZF × B_γγ × 500 fb⁻¹ = **1.44 events produced**, before any selection.
- QCD ZHjj: σ = 10.212 ± 0.010 fb, giving 11.3 events.

### 1.2 The earlier "exit code 2"

The exit code 2 came from the background shell command "Run σ-only and pilot MG5 jobs, 3 in parallel" (started 2026-11-02T14:23:23Z). It was not an MG5 or physics failure and no output was lost.

- **The failing command.** The command ran the 13 cards through `xargs -P 3 scripts/mg5_smoke.sh`. It ended with `grep -h "rc=\|Cross-section" work/m5/{…,wza,zza,…}/status.txt`.
- **Why grep failed.** GNU/ugrep `grep` returns 2 when an input file is missing. The task output shows exactly `ugrep: warning: work/m5/wza/status.txt: No such file or directory` and the same line for `zza`.
- **Why the files were missing.**
  - The first wza/zza runs (seeds 13630009/13630010) failed with the subprocess-grouping error, and their directories had been renamed to `work/m5/{wza,zza}_fail_grouping/`. Their status.txt files have utc 14:27:36Z and 14:29:11Z, rc = 0, because MG5 exits 0 even on that error.
  - The `set group_subprocesses False` reruns (seeds 13630020/13630021) started at 14:32:04Z and 14:42:07Z.
  - So at the time of the grep (14:38:54Z), `work/m5/wza/status.txt` did not exist yet and `work/m5/zza/` did not exist at all.
- **No output was lost.** The same task output lists `rc=0` and a cross section for all 11 other cards. The status.txt files are on disk: 26 `rc=` lines in `work/m5/*/status.txt`.
- **The wza/zza reruns** later ended with rc = 124 (600 s timeout), which is recorded. This is why V_WZa and V_ZZa use labelled estimates.
- **The failed first attempts** are preserved in `*_fail_grouping/` and were not deleted.

## 2. Background model (aligned with arXiv:2512.07689 §II.A, plus Higgs backgrounds)

Selection objects follow the reference "good particles" definition (§III):
- ≥2 photons with pT > 20 GeV and |η| < 2.5 (ECAL crack excluded);
- one OSSF ee/μμ pair with pT > 15 GeV, closest to mZ;
- ≥2 jets with pT > 25 GeV and |η| < 4.7;
- ΔR(γ,ℓ) > 0.4 and ΔR(j, γ/ℓ) > 0.4.

Tag jets and photons are the two leading ones. Delphes photons are already isolated by the card.

| class | process | treatment here | reference treatment |
|---|---|---|---|
| signal | EW ZHjj, Z→ℓℓ, H→γγ | Tier-1, 200k events, direct | (signal is EW Zγγjj there) |
| signal (b) / background (a) | QCD ZHjj (fixed order, 2 partons, ptj > 20) | Tier-1, 100k events, direct | — |
| other resonant H→γγ | ttH (tt̄ → dileptonic) | test_v2, 2000 events, fully factorised | — |
| other resonant H→γγ | ggZH, tHW, ZH(Z→ττ); merged QCD ZH (0–2j) as a cross-check | test_v2 where available; reported, not added to b (§2.2) | — |
| prompt γγ | QCD Zγγ+jj | **proxy estimate**: no jj reconstructed sample yet; the heavy B_QCD_llaa_2j gridpacks are running | MLM 0–2j, direct |
| prompt γγ | EW Zγγjj | **proxy estimate** | (its signal) |
| 1 fake γ | QCD Zγ+jets | direct Delphes and fake factor; the FF band is used because direct Delphes has < 10 raw events (§2.1) | MLM 0–2j, direct Delphes fakes |
| 1 fake γ | EW Zγjj | as QCD Zγ | direct |
| 1 fake γ | tt̄γ, tWγ (dileptonic) | fake factor on test_v2 (2000 events each), fully factorised | direct |
| prompt γγ | tt̄γγ | direct on test_v2 (2000 events), fully factorised | — |
| 2 fake γ | Z+jets, tt̄ | order-of-magnitude only, not added to b (§2.2) | neglected |

**Overlap removal (hard vs soft photons).**
- Reference rule: Zγ events with ≥2 hard photons are removed (§III).
- Our implementation: the generator-level count `n_prompt_photons` from `scripts/slim_gentruth.py` (hadron-free ancestry, pT > 15, |η| < 2.5, isolated from leptons, photons and jets).
- The fake-factor modes require exactly 1 prompt photon (Zγ, tt̄γ, tWγ: one real photon plus one jet→γ) or 0 (Z+jets, tt̄: two jet→γ).
- Prompt Zγγ is taken from the γγ samples only, so a Zγ event with a second prompt (ISR/FSR) photon cannot be counted twice.
- Difference from the reference: our "prompt" includes photons radiated from leptons (FSR), which the reference calls "soft". The ΔR(γ,ℓ) > 0.4 requirement and the mℓℓγγ cut make this a minor difference, but it is not yet quantified.

### 2.1 Fake photons: direct Delphes simulation vs the fake-factor cross-check

**Direct Delphes fakes.** The Zγ+2j pilot (5000 events, σ = 1775 fb, so 177 events per MC event at 500 fb⁻¹) has only 2 events passing the loose preselection (OSSF + ≥2 photons + ≥2 jets). None of them survive the VBS + window selection.
- The reference's own Table III implies an initial-selection efficiency of about 1×10⁻⁴ for QCD Zγ with Delphes fakes. That would be 0.5 events expected in 5000. A direct-simulation estimate with ≥10 raw events at the optimum would therefore need about 10⁸ Zγ events. This is the brute-force approach rejected in run 2.
- 126 events have ≥2 photons but no OSSF pair. These are electrons reconstructed as photons, the e→γ component that the stock card does produce. They fail the Z requirement.

**Fake-factor (FF) cross-check.**
- f(j→γ) = 1×10⁻³ (flat) per jet with pT > 20 and |η| < 2.5. The band is 5×10⁻⁴ to 2×10⁻³; a pT-dependent variant uses 1×10⁻³ (pT/50)^−0.5, ×2 in the endcap.
- The fake photon carries x·pT(jet), with x ~ N(0.85, 0.10) truncated to [0.5, 1].
- With this FF, the fraction of Zγ+2j events passing the reference initial selection is 1.5×10⁻⁴. Direct Delphes on our sample gives 4×10⁻⁴ (2 of 5000), and the reference gives about 1×10⁻⁴ (0–2j merged).
- The three agree within the expected order of magnitude, so f = 10⁻³ is a reasonable central value for the stock CMS card. **None of these numbers is data-driven.**
- Because no fake background reaches 10 raw direct-Delphes events at the optimum, the FF band is used for all one-fake backgrounds. This follows the run-3 instruction.

### 2.2 Order-of-magnitude arguments (not added to b)

- **Z+jets (two fakes).** σ(Z+2j, ptj > 20) = 211.5 pb, which is 1.06×10⁸ events at 500 fb⁻¹. Each event needs two jet→γ fakes, P ~ f² × N_pairs ≈ 10⁻⁶ × O(3).
  - With the FF at f = 10⁻³ (ff2 mode, zll_jj_pilot), the yield at the optimum is 0.020 events. The FF band moves this by ×0.25 to ×4.
  - This is the same order as the one-fake Zγ yield, not negligible by orders of magnitude. The reference neglects it. It is shown as a robustness row ("incl. Z+jets & tt̄") rather than in the nominal b, consistent with the reference.
  - Caveat: the f² dependence makes this the least certain background.
- **tt̄ (two fakes):** 0.0002 events (FF, fully factorised, 100 % uncertainty).
- **ggZH (Z→ℓℓ, H→γγ):** the gridpack job **failed**: MadSpin cannot decay in gridpack mode (`InvalidCmd: No events file corresponding to run_01`, both attempts, `production/gridpacks/H_ggZH_mg5.log.gz`). Its total σ(gg→ZH, Z undecayed) = 74.5 fb is valid.
  - × B(Z→ℓℓ, PDG) 0.0673 gives 5.0 fb.
  - Scaling with the yield per fb of the merged QCD ZH (0–2j MLM) test sample gives ≈ **0.002 events** at the optimum. This is an ESTIMATE, not added to b.
  - Fix for a later run: decay Z→ℓℓ in the ME (loop-induced `g g > h l+ l-` is not supported) or run MadSpin in the event job.
- **tHW:** test_v2 (2000 events) gives 7×10⁻⁵ events (fully factorised).
- **ZH, Z→ττ:** test_v2 (1317 matched events, σ = 25.1 fb, 28 events produced) has **0 events passing even the loose preselection**. Zero is not used as proof.
  - The bound is: 0/1317 at the preselection, then × Z window × VBS. Applying the QCD-ZH conditional efficiency (Z window × VBS × window ≈ 2 %) gives < 3/1317 × 28 × 0.02 ≈ 1×10⁻³ events.

### 2.3 Prompt Zγγ+jj proxy (no reconstructed jj sample yet)

N = σ_jj,est × L × ε_LG × ε_J, where:
- **σ_jj,est for QCD:** σ(llγγ, 0j; 90 < mγγ < 190) × σ(llγjj)/σ(llγ 0j) = 2.893 × 1775/10080 = **0.509 fb**.
  - Cross-check: × σ(QCD ZHjj)/σ(ZH 0j) gives 0.610 fb.
- **σ_jj,est for EW:** 2.893 fb × (EW/QCD Zγγ ratio of the reference, 0.263/23.0) × 1.4 (QCD 0–2j/0j) = **0.046 fb**.
  - The alternative, 2.893 × σ(EW llγjj)/σ(llγ 0j), gives 0.010 fb. Both appear in T4.
- **ε_LG:** lepton and photon cuts plus the mγγ window, from the reconstructed llγγ 0j sample. The window fraction comes from an exponential fit (the B_QCD_llaa_0j test_v2 sample: 2307 events accepted by matching). Because only the 0-jet multiplicity was generated with nJetMax = 2, this sample is exclusive 0-jet and slightly biased against hard recoil..
- **ε_J:** the VBS-jet cuts (≥2 jets, mjj, |Δη|, b-veto, Zeppenfeld) measured on a proxy with real ME jets.
  - QCD: the Zγ+2j pilot (photon direction as the Zeppenfeld proxy).
  - EW: the EW ZHjj Tier-1 sample.
- **Uncertainty:** ±10 % in the nominal systematics (as instructed for "others"), plus a ±50 % robustness row. The real uncertainty of the proxy is larger, at least a factor 2 for EW. This is the first item that the B_QCD_llaa and B_EW_llaajj test samples (submitted, heavy gridpacks running) will replace.

## 3. Method

- **mγγ resolution.** From the Delphes EW signal: Gaussian core fit in 121–129 GeV gives μ = 124.98 GeV, **σ = 2.07 ± 0.02 GeV**, and σ_eff (smallest 68.3 % interval) = 2.15 GeV.
  - The window ±kσ uses k ∈ {1.5, 2.0}.
  - This is the stock CMS card resolution. Real CMS achieves about 1.5 GeV, so the resolution dependence is shown in T4 (×0.75, ×1.25).
- **Continuum backgrounds in the window.**
  - Yield in 105–165 GeV after all cuts, × f_win.
  - f_win is the fraction of an exponential unbinned-MLE fit to that sample's mγγ at loose selection (Z window + preselection) that lies inside the window. This is the smooth-shape (sideband) assumption.
  - Resonant samples (ZH, ttH) count the window directly.
- **Low-MC-support fallback.**
  - If < 10 raw events remain: N(all cuts except mjj/Δη/Zeppenfeld) × ε(VBS cuts | loose).
  - If either factor has < 3 events: a fully factorised product of single-cut efficiencies relative to the preselection, with zero-count cuts set to 0.5/(n+1) and a **100 % uncertainty**.
  - Every number in T2 states its method and raw count.
- **Optimisation.**
  - Objective: Z_syst at 500 fb⁻¹, signal definition (a). Expected yields only; no pseudo-data.
  - Procedure: coordinate descent, up to 3 passes. Each pass does a joint 2D (mjj ∈ 200–1000 GeV, |Δηjj| ∈ 0–4.0) step, then one-dimensional scans of:
    - the window k;
    - pT(γ1)/mγγ > 1/3 and pT(γ2)/mγγ > 1/4 (on/off);
    - |mℓℓ − mZ| < {reference 70–120, 25, 20, 15, 10} GeV;
    - Zeppenfeld centrality of γγ and of Z < {none, 1.0, 0.7, 0.5};
    - mℓℓγγ > {100, 200, 250} GeV;
    - b-veto (on/off);
    - pT(γ1) > {20, 25, 30, 35} and pT(γ2) > {20, 25} GeV.
  - **Plateau rule** against noise-driven optima: among the scan points with Z ≥ 0.97 Z_max, the one with the largest signal yield (loosest cut) is chosen.
  - MC-stat uncertainty enters σ_b, so low-support points are penalised.
- **Statistics.**
  - Z_stat is reference Eq. (1): Z = √(2[(s+b) ln(1+s/b) − s]).
  - Z_syst is the Asimov formula with background uncertainty σ_b (Cowan et al.), where σ_b² = Σ(r_i b_i)² + Σ(MC-stat_i)², with r = 50 % for fakes and 10 % for the rest.
  - The expected limit is the median CLs upper limit on μ for a Poisson counting experiment. b is marginalised over a log-normal with width σ_b/b. The median is taken over the background-only count distribution.
  - When the median count is 0, the limit is μ = 3.0/s, independent of b and its uncertainty.
  - No signal systematic is included.

## 4. Results

**Optimum** (500 fb⁻¹, definition (a), plateau rule):
- 2γ (pT > 20 GeV) with pT(γ1)/mγγ > 1/3 and pT(γ2)/mγγ > 1/4;
- |mℓℓ − mZ| < 25 GeV;
- mℓℓγγ > 250 GeV;
- b-veto (no b-tagged jet with |η| < 2.5);
- no Zeppenfeld cut (no gain within the 3 % plateau);
- mjj > 700 GeV and |Δηjj| > 3.0;
- 120.8 < mγγ < 129.1 GeV (±2σ, σ = 2.07 GeV).

The same cuts are used for definition (b) and for all luminosities.

**s < 1 event at every luminosity and for both signal definitions, so Z alone is not a meaningful sensitivity measure.** The CLs limit is the relevant quantity.

### T1 — Expected results (13.6 TeV; 3000 fb^-1 = luminosity scaling only, not HL-LHC)

| L [fb^-1] | signal def. | s | b | sigma_b (syst+MC) | b MC-stat | Z_stat (Eq. 1) | Z_syst | median n_obs (b-only) | mu_95 (CLs, syst) | mu_95 (CLs, stat) |
|---|---|---|---|---|---|---|---|---|---|---|
| 500 | (a) EW ZHjj; QCD ZHjj in b | 0.067 | 0.094 | 0.020 | 0.029 | 0.199 | 0.198 | 0 | 44.6 | 44.6 |
| 500 | (b) EW+QCD ZHjj | 0.090 | 0.071 | 0.019 | 0.029 | 0.288 | 0.287 | 0 | 33.4 | 33.4 |
| 1000 | (a) EW ZHjj; QCD ZHjj in b | 0.134 | 0.187 | 0.039 | 0.057 | 0.281 | 0.280 | 0 | 22.3 | 22.3 |
| 1000 | (b) EW+QCD ZHjj | 0.179 | 0.142 | 0.039 | 0.057 | 0.408 | 0.405 | 0 | 16.7 | 16.7 |
| 3000 | (a) EW ZHjj; QCD ZHjj in b | 0.403 | 0.562 | 0.117 | 0.171 | 0.487 | 0.480 | 0 | 7.4 | 7.4 |
| 3000 | (b) EW+QCD ZHjj | 0.538 | 0.427 | 0.116 | 0.171 | 0.706 | 0.691 | 0 | 5.6 | 5.6 |

### T2 — Per-process expected yield at the optimum, 500 fb^-1 (events), with raw MC support and method

| process | role | sigma used [fb] | x BR | yield | MC-stat | raw MC events | method | source |
|---|---|---|---|---|---|---|---|---|
| S_EW_ZHjj | signal | 1.295 | 0.002221 | 0.0672 | 0.0007 | 9346 | direct | Tier-1 v1, 100 jobs, LHE-init sigma (weighted mean) |
| H_QCD_ZHjj | bkg (a) / signal (b) | 10.21 | 0.002221 | 0.0226 | 0.0016 | 199 | direct | Tier-1 v1, 50 jobs |
| H_ttH | background | 18.11 | 0.00227 | 0.0021 | 0.0021 | 103 | fully-factorised (100% unc.) | test_v2 H_ttH (2000 ev, seed 137599999); sigma MG5 gridpack total [replaces: work/m5/ttH_dilep LHE (500 ev) + PY8/Delphes slim_v1] |
| B_QCD_Zaajj | background | 0.5094 | 1 | 0.0065 | 0.0034 | 4 | proxy | ESTIMATE: sigma(llaa_0j)*sigma(llajj)/sigma(lla_0j); eps_LG llaa_0j reco; eps_J llajj_pilot |
| B_EW_Zaajj | background | 0.04631 | 1 | 0.0288 | 0.0043 | 44 | proxy | ESTIMATE: ref. EW/QCD Zaa ratio x sigma(llaa_0j); eps_LG llaa_0j; eps_J EW ZHjj |
| F_QCD_Za | background | 1775 | 1 | 0.0260 | 0.0099 | 8 | ff+factorised | llajj_pilot 5000 ev (Za+2j fixed order) |
| F_EW_Za | background | 35.6 | 1 | 0.0072 | 0.0072 | 9 | ff+fully-factorised (100% unc.) | work/m5/ew_llajj LHE 200 ev |
| T_tta | background | 85.58 | 1 | 0.0003 | 0.0003 | 86 | ff+fully-factorised (100% unc.) | test_v2 T_tta (2000 ev, seed 139599999); sigma MG5 gridpack total [replaces: work/m5/tta_dilep LHE 200 ev] |
| T_tWa | background | 13.04 | 1 | 0.0000 | 0.0000 | 57 | ff+fully-factorised (100% unc.) | test_v2 T_tWa (2000 ev, seed 139699999); sigma MG5 gridpack total [replaces: work/m5/twa_dilep LHE 200 ev] |
| F_Zjets | order-of-magnitude only (not in b) | 2.115e+05 | 1 | 0.0199 | 0.0037 | 39 | ff+factorised | zll_jj_pilot 5000 ev (Z+2j); order-of-magnitude only |
| T_tt | order-of-magnitude only (not in b) | 2.363e+04 | 1 | 0.0002 | 0.0002 | 73 | ff+fully-factorised (100% unc.) | test_v2 T_tt (2000 ev, seed 139799999); sigma MG5 gridpack total [replaces: work/m5/tt_dilep LHE 200 ev] |
| T_ttaa | background | 0.097 | 1 | 0.0002 | 0.0002 | 78 | direct+fully-factorised (100% unc.) | test_v2 T_ttaa (2000 ev, seed 139499999); sigma MG5 gridpack total [replaces: work/m5/ttaa_dilep LHE 200 ev] |
| X_QCD_ZH_mlm | cross-check only (not in b) | 50.99 | 0.002221 | 0.0248 | 0.0248 | 28 | fully-factorised (100% unc.) | test_v2 H_QCD_ZH_mlm (1335 ev, seed 137299999); sigma PY8 matched |
| H_ZH_tautau | cross-check only (not in b) | 25.06 | 0.00227 | 0.0000 | 0.0000 | 0 | NO MC SUPPORT (presel empty) | test_v2 H_ZH_tautau (1317 ev, seed 137799999); sigma PY8 matched |
| H_tHW | cross-check only (not in b) | 0.7868 | 0.00227 | 0.0001 | 0.0001 | 109 | fully-factorised (100% unc.) | test_v2 H_tHW (2000 ev, seed 137699999); sigma MG5 gridpack total |

### T3 — Cutflow at the optimum, 500 fb^-1: expected events (raw MC events)

| step | S_EW_ZHjj | H_QCD_ZHjj | H_ttH | B_QCD_Zaajj | B_EW_Zaajj | F_QCD_Za | F_EW_Za | T_tta | T_tWa | F_Zjets | T_tt | T_ttaa | X_QCD_ZH_mlm | H_ZH_tautau | H_tHW |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| presel: OSSF + 2gamma(20) + 2jets(25) | 0.199 (27635) | 1.09 (9590) | 1.06 (103) | 61.7 (222) | 6.28 (222) | 135 (291) | 1.6 (8) | 5.73 (86) | 0.434 (57) | 27.5 (288) | 2.07 (72) | 1.87 (77) | 1.15 (27) | 0 (0) | 0.0487 (109) |
| Z window | 0.195 (27108) | 1.07 (9400) | 0.329 (32) | 38 (133) | 3.76 (133) | 96.9 (205) | 1.6 (8) | 1.58 (23) | 0.104 (12) | 26.2 (275) | 0.49 (19) | 0.533 (22) | 1.15 (27) | 0 (0) | 0.0129 (29) |
| m_llgg | 0.174 (24166) | 0.857 (7554) | 0.247 (24) | 24.3 (85) | 2.41 (85) | 52.9 (148) | 1.42 (8) | 1.11 (19) | 0.0685 (11) | 18.1 (226) | 0.301 (15) | 0.315 (13) | 0.933 (22) | 0 (0) | 0.00938 (21) |
| photon pT / pT/m | 0.151 (21004) | 0.745 (6571) | 0.216 (21) | 12.6 (44) | 1.24 (44) | 29.3 (96) | 0.712 (6) | 0.599 (16) | 0.0456 (8) | 11 (192) | 0.165 (12) | 0.267 (11) | 0.763 (18) | 0 (0) | 0.00759 (17) |
| b-veto | 0.139 (19378) | 0.662 (5836) | 0.0514 (5) | 11.2 (44) | 1.15 (44) | 25.2 (87) | 0.712 (6) | 0.128 (6) | 0.0228 (7) | 9.69 (179) | 0.0768 (9) | 0.0728 (3) | 0.721 (17) | 0 (0) | 0.00179 (4) |
| Zeppenfeld | 0.139 (19378) | 0.662 (5836) | 0.0514 (5) | 11.2 (44) | 1.15 (44) | 25.2 (87) | 0.712 (6) | 0.128 (6) | 0.0228 (7) | 9.69 (179) | 0.0768 (9) | 0.0728 (3) | 0.721 (17) | 0 (0) | 0.00179 (4) |
| mjj, |deta_jj| | 0.0724 (10070) | 0.0239 (211) | 0 (0) | 0.131 (4) | 0.581 (44) | 0.71 (3) | 0.356 (3) | 0 (0) | 0.00326 (1) | 0.825 (24) | 0 (0) | 0 (0) | 0.0424 (1) | 0 (0) | 0 (0) |
| m_gg window +-2.0 sigma | 0.0672 (9346) | 0.0226 (199) | 0.00212 (103) | 0.0065 (4) | 0.0288 (44) | 0.026 (8) | 0.00721 (9) | 0.000324 (86) | 4.97e-05 (57) | 0.0199 (39) | 0.00016 (73) | 0.000151 (78) | 0.0248 (28) | 0 (0) | 6.87e-05 (109) |

Before the window, fake-factor rows are sums of f-weighted combinations (raw = distinct MC events); proxy rows are the factorised estimate (raw = min of the two factors).

### T4 — Robustness at 500 fb^-1, definition (a)

| variation | s | b | Z_stat | Z_syst |
|---|---|---|---|---|
| nominal | 0.067 | 0.094 | 0.199 | 0.198 |
| fake syst 25% | 0.067 | 0.094 | 0.199 | 0.199 |
| fake syst 100% | 0.067 | 0.094 | 0.199 | 0.198 |
| proxy Zgg syst 50% | 0.067 | 0.094 | 0.199 | 0.198 |
| m_gg resolution x0.75 | 0.067 | 0.077 | 0.216 | 0.216 |
| m_gg resolution x1.25 | 0.067 | 0.111 | 0.185 | 0.185 |
| fake rate pT-dependent | 0.067 | 0.095 | 0.198 | 0.197 |
| incl. Z+jets & tt (2 fakes) | 0.067 | 0.114 | 0.183 | 0.183 |
| incl. other H (ggZH, tHW, ZH(tautau)) where available | 0.067 | 0.094 | 0.199 | 0.198 |
| f=5e-4 | 0.067 | 0.077 | 0.216 | — |
| f=2e-3 | 0.067 | 0.127 | 0.175 | — |
| reference-like cuts | 0.087 | 0.296 | 0.153 | 0.152 |
| EW Zaajj sigma low (0.010 fb) | 0.067 | 0.071 | 0.223 | 0.222 |
| QCD Zaajj sigma alt (ZH ratio, 0.61 fb) | 0.067 | 0.095 | 0.198 | 0.197 |

### T5 — Joint (mjj, |deta_jj|) scan of Z_syst at 500 fb^-1, other cuts at the optimum

| mjj \ deta | 0.0 | 0.5 | 1.0 | 1.5 | 2.0 | 2.5 | 3.0 | 3.5 | 4.0 |
|---|---|---|---|---|---|---|---|---|---|
| >200 | 0.103 | 0.103 | 0.107 | 0.112 | 0.119 | 0.125 | 0.139 | 0.158 | 0.168 |
| >300 | 0.128 | 0.130 | 0.130 | 0.134 | 0.139 | 0.145 | 0.153 | 0.165 | 0.171 |
| >400 | 0.147 | 0.151 | 0.152 | 0.153 | 0.157 | 0.160 | 0.168 | 0.173 | 0.173 |
| >500 | 0.166 | 0.168 | 0.169 | 0.171 | 0.173 | 0.177 | 0.185 | 0.189 | 0.187 |
| >600 | 0.171 | 0.174 | 0.175 | 0.177 | 0.180 | 0.183 | 0.190 | 0.191 | 0.188 |
| >700 | 0.180 | 0.180 | 0.181 | 0.183 | 0.186 | 0.188 | 0.198 | 0.201 | 0.199 |
| >800 | 0.180 | 0.180 | 0.180 | 0.182 | 0.183 | 0.183 | 0.191 | 0.193 | 0.193 |
| >1000 | 0.183 | 0.183 | 0.183 | 0.185 | 0.186 | 0.187 | 0.187 | 0.191 | 0.190 |


## 5. D12 recommendation: is `production_v2` worth its cost?

**Recommendation: no, do not run the full `production_v2` (2461 jobs, about 375 core-h, about 13 GB).** Run the reduced campaign below instead, and decide on scope first.

1. **The signal is the limiting factor, not the background model.**
   - Before any selection, 1.44 EW ZHjj events are produced at 500 fb⁻¹. The optimised selection keeps s = 0.067 (4.7 %).
   - The VBS cuts alone keep 52 % of the preselected signal, and the stock-card dilepton efficiency is about 36 %.
   - Even at 3000 fb⁻¹, s = 0.40 (definition a) or 0.54 (definition b). **s < 1 at every luminosity, so the significance alone is not meaningful.** Z ≤ 0.7 in every robustness variant (T4).
2. **The expected limit does not depend on b.**
   - The median background-only count is 0 at all three luminosities, so μ₉₅ = 3.0/s exactly: 44.6 (500 fb⁻¹), 22.3 (1000 fb⁻¹), 7.4 (3000 fb⁻¹), definition (a).
   - This is unchanged whether b is scaled ×0.5 or ×2 (T4: fake syst 25–100 %, f band, alternative proxy σ). It changes only if b exceeds ln 2 ≈ 0.69 events, which is 7× the present 500 fb⁻¹ estimate; at that point the median count becomes 1.
   - More background MC therefore cannot change any reported number by more than the proxy-σ spread already shown.
3. **The signal and QCD ZHjj MC are already sufficient.**
   - Tier-1 gives 9346 and 199 raw events at the optimum, so MC-stat/data-stat ≈ 0.01. The 2000-event test_v2 samples cover ttH, tt̄γ, tWγ, tt̄γγ, tHW and ZH(ττ).

**Reduced campaign proposal**, only if the project continues with the current scope, to replace the two remaining ESTIMATE backgrounds by direct MC. The gridpacks are already being built by `gridpacks_v2`; no bulk is needed beyond this.

| item | why | jobs | events | core-h (est.) |
|---|---|---|---|---|
| test_v2 jobs already queued (held until gridpacks finish) | σ + 2000-event tests for QCD llγγ 1j/2j, EW llγγjj, Zγ MLM, Z+jets MLM, EW llγjj, WZγ/ZZγ | 16 (submitted) | 32k | ≈ 20 + heavy gridpacks (≈ 400, already running) |
| B_QCD_llaa_2j_is1–4 + B_EW_llaajj_is1–4 | replace the proxy Zγγjj (largest b component: EW proxy 0.029) | 8 × 10 jobs × 500 | 40k | ≈ 40 |
| F_QCD_lla_mlm | raise the one-fake Zγ FF support from 8 to ≥ 10 raw events at the optimum | 25 × 4000 | 100k | ≈ 30 |
| **total** | | **≈ 105 + 16** | **≈ 170k** | **≈ 90 (+ heavy gridpacks already committed)** |

This is about 4 % of the `production_v2` job count and ≤ 1 GB on EOS.

**Scope (D12) options for you:**
- (i) Report the analysis as an expected-limit study: μ₉₅ ≈ 45 at 500 fb⁻¹ and ≈ 7 at 3000 fb⁻¹ (13.6 TeV luminosity scaling), with the reduced campaign.
- (ii) Widen the signal, e.g. definition (b) plus Z→νν or a different H decay. That needs a new Phase 01.
- (iii) Stop at this pilot.

The analysis, not the MC budget, sets the reach.

## 6. Checks performed

- **BR ledger:** σ_PY8 = σ_LHE; 2000/2000 forced H→γγ; one k-factor per sample (§1.1).
- **Tier-1 integrity:** 150/150 jobs exit 0; Σ n_lhe = Σ n_delphes = 200000 (EW) and 100000 (QCD).
  - Per-job σ spread is consistent with the per-job error (EW 1.29 ± 0.01 fb); the weighted mean agrees with the test job.
- **Tier-1 timing and size:** mean job time 188 s (EW) and 197 s (QCD). Output is 690 MB and 389 MB on EOS (3.45 / 3.89 kB/event including LHE).
- **Merged vs fixed-order QCD ZH:** at the optimum, the merged QCD ZH (0–2j MLM, test_v2) gives 0.025 events (fully factorised, 100 %), vs 0.023 from fixed-order QCD ZHjj. They agree.
- **Fake-rate cross-check:** FF (f = 10⁻³) initial-selection fraction 1.5×10⁻⁴ vs direct Delphes 4×10⁻⁴ (2 events) vs reference 1×10⁻⁴ (§2.1).
- **Proxy σ cross-check:**
  - QCD Zγγjj: 0.509 fb (Zγ ratio) vs 0.610 fb (ZH ratio). This moves b by 0.001 (T4).
  - EW Zγγjj: 0.046 vs 0.010 fb. This moves b from 0.094 to 0.071 (T4).
- **Optimisation stability:**
  - The Z landscape is flat: Z_syst lies within 0.17–0.20 for mjj > 500 GeV and |Δη| > 2.5 (T5). The plateau rule picks (700 GeV, 3.0).
  - The reference-like cuts (700, 2.0, mℓℓ 70–120 GeV, mℓℓγγ > 100 GeV) give Z = 0.15, so the optimisation gains about 30 %. That gain is not significant given the MC uncertainty of the proxies.
- **Resolution dependence:** Z = 0.216 / 0.198 / 0.185 for σ_mγγ × 0.75 / 1.0 / 1.25.
- **Systematics dependence:** Z_syst − Z_stat ≤ 0.002 at 500 fb⁻¹ and ≤ 0.02 at 3000 fb⁻¹, because b ≪ 1 makes the result statistics-dominated.

## 7. Caveats

1. **Two ESTIMATE components dominate b:** the EW Zγγjj proxy (0.029, 31 % of b) and the QCD Zγ fake-factor estimate (0.026; 8 raw events, which is below the 10-event rule, so the FF band is used). The proxy σ values are not measurements.
2. **The fake rate is assumed, not measured** (f = 10⁻³, band ×0.5–×2). It is not data-driven.
3. **Fully factorised estimates** (ttH, tt̄γ, tWγ, tt̄γγ, tHW) assume independent cuts and carry 100 % uncertainty. Their "raw" count in T2 is the preselection count, not the count at the optimum. All of them are below 0.003 events.
4. **Detector model:**
   - Stock Delphes CMS gives σ_mγγ = 2.07 GeV (real CMS is about 1.5 GeV).
   - Its OSSF efficiency of 36 % for signal events is low because of electron losses (D11). Some electrons are reconstructed as photons: 126 of 5000 Zγ+2j events have ≥2 photons but no OSSF pair.
   - A real-CMS-like lepton efficiency would increase s by up to about ×1.7. That still gives s < 1 at 3000 fb⁻¹ (definition a).
5. **The prompt-photon overlap definition** counts lepton-FSR photons as prompt, unlike the reference's "soft" class (§2).
6. **No signal systematic or theory uncertainty** is included. All rates are LO.
7. **3000 fb⁻¹ is a pure luminosity scaling at 13.6 TeV,** not an HL-LHC detector projection.
8. **The ggZH gridpack failed** (MadSpin in gridpack mode). Its contribution is estimated at about 0.002 events.

## 8. Next actions

1. Decide D12 (scope) and whether to run the reduced campaign (§5).
2. When the heavy gridpacks finish, the held test_v2 jobs release automatically within 30 min. Then:
   - rerun `ntuple.py` → `override_test_v2.py` → `sensitivity.py`;
   - replace the Zγγjj proxy (extend `override_test_v2.py` with B_QCD_llaa_{1j,2j}, B_EW_llaajj, F_QCD_lla_mlm, F_EW_llajj);
   - check the 4-way split closure (PLAUSIBLE, −1.4 %).
3. The H_ggZH test_v2 job was removed in this run because its gridpack failed. Fix ggZH only if the scope continues.

## 9. Reproduce

```bash
cd /eos/home-r/rjiang/vbs_zh_codex_starter && source scripts/setup_stack.sh
O=work/m7_analysis
python3 -P scripts/analysis/ntuple.py $O/S_EW_ZHjj.npz direct $(ls production/v1/ew_zhjj_zll/*.root | grep -v _gen | paste -sd,)
python3 -P scripts/analysis/ntuple.py $O/H_QCD_ZHjj.npz direct $(ls production/v1/qcd_zhjj_zll/*.root | grep -v _gen | paste -sd,)
#  pilots: work/m7_pilot_reco/<s>/<s>.root (PY8+Delphes slim_v1 on work/m5/<s>/unweighted_events.lhe.gz, seeds 137900001-7)
#  test_v2: production/test_v2/<id>/<id>_s<seed>.root -> $O/tv2_<id>.npz (direct; T_tta/T_tWa also ff1, T_tt ff2)
python3 -P scripts/analysis/override_test_v2.py $O $O/override_tv2.json
python3 -P scripts/analysis/sensitivity.py $O $O/sens_final.json $O/override_tv2.json
python3 -P scripts/analysis/tables05.py $O/sens_final.json
```

Seeds:
- Tier-1: 13611000–13611099 (EW) and 13621000–13621049 (QCD).
- test_v2: base + 99999 per sample.
- Interactive pilots: 137900001–137900007; the FF smearing RNG seed is 13600555.
