# WH Phase 02 - background and overlap ledger (multi_r3)
- Date UTC: 2026-11-09. **Status: PASS as a ledger/design** (every row has a generator definition, overlap rule and evidence class); quantitative yields are NOT claimed. Sign-off of overlap/merging validation and of N_MC for fake-type samples is deferred to Phase 04 / decision D-WH-2.
- Goal: background matrix with overlap removal, reuse of frozen ZH samples, quantitative bounds for fakes. Machine-readable: `config/sample_matrix_wh.yaml`, `config/br_ledger.json`.
- Git commit: HEAD `e7f51f7`; run files uncommitted.
- Inputs: Phase 01, frozen ZH reports 02/03 and samples (read only), `work/smoke/xs_summary.json`, `work/lostlep/*.json`, `work/pilots/*`. Seeds: registry `config/sample_registry.py` (pilots J=900 range, PY8 seed = MG seed + 1e8).

## 1. Measurement definition
Reco target: exactly one isolated e/mu, MET, >=2 isolated photons with m_gg in a Higgs window (sidebands reserved for Phase 06), >=2 VBS tag jets, b-veto. Signal = EW (0,4) WHjj only (def. a). Everything with a resonant m_gg peak but not EW WHjj is a resonant background fitted with the signal shape; continuum is sideband-constrained. Photon p_T/m_gg cuts in the later selection make a generator cut pT(gamma)>20 GeV safe; ZH was forced to 25 GeV by VBS-biased generation (D-WH-3: keep 20, costs statistics).

## 2. Ledger
| ID | Role | Generator / order | Decays / BR ledger | Overlap rule | Evidence class and numbers |
|---|---|---|---|---|---|
| S_EW_WHjj | signal | MG5 LO (0,4) w+- h j j, W chain, fixed 2j + PY8 dipole recoil | WF once, B_gg once (PY8 forced) | order-exclusive vs QCD | measured: 28.32 +- 0.19 fb chain; 0.0617 fb physical |
| H_QCD_WHjj | resonant bkg (a)/inclusive (b) | LO (2,2); fixed 2j (ZH precedent: MLM 0/1/2j variant is a cross-check, never added) | same | never add MLM and fixed-2j | measured 59.42 +- 0.33 fb; 0.1295 fb phys; VBS-like parton fraction 4.6% vs 47% (EW) |
| I_WHjj | signed interference | QCD^2==2 QED^2==6 | sigma only | separate signed term | -0.258 +- 0.012 fb undecayed (-0.2% of EW) |
| S_offshell | pole-approx syst | (0,5) l v H j j | B_gg only | alternative, never added | 25.11 +- 0.33 fb; 0.89 x on-shell chain (D-WH-5) |
| H_ttH_1l | resonant | LO ttH, t->bW in ME, one W leptonic | WF_tt, B_gg | distinct external tops | measured 108.17 +- 0.75 fb; 0.238 fb phys = 119 ev at 500 fb^-1 pre-cut |
| H_tHW_1l, H_tHq_1l | resonant small | MG5 LO | WF_tt, B_gg | distinct | TBD Phase 04; proxy: frozen ZH H_tHW 0.787 fb (dilepton). Not declared negligible |
| ZHjj / ggZH / ZH->tautau with one lost lepton | resonant | REUSE frozen ZH samples (Z->ll in ME, no lepton cuts, cut_decays False, jets pT>20: phase space of a lost lepton covered) | ZF 0.9783 x B_gg as in ZH ledger | none needed (distinct from WH final state) | measured on subsets, section 3 |
| ttH dilepton, one lepton lost | resonant | REUSE frozen ZH H_ttH | as ZH | tt-like overlap with H_ttH_1l: different W decay configuration (disjoint) | section 3 |
| B_EW_Waajj | continuum | (0,5) on-shell W chain, 4F beam-split as ZH is1-3 | WF | order-exclusive vs QCD | NOT measured: interactive sigma timed out at 1200 s (46516 diagrams, rc=124) -> gridpack in Phase 04, as ZH Zgg jj (2.9 h, 16 cores). Not zero |
| B_QCD_Waajj | continuum | (2,3) on-shell W chain, or W gamma gamma +0,1,2j MLM | WF | defines N_prompt_gamma>=2 | NOT measured (timeout 1200 s, 15348 diagrams) -> gridpack |
| I_Waajj | signed continuum | QCD^2==2 | - | separate | TBD; absorbed by sideband fit, quote size |
| B_QCD_Waa_0j | sample-type test | W gamma gamma 0j | WF | - | measured 4.681 +- 0.033 fb (pTg>20, 90<mgg<190); only a condor sample-type test |
| F_Wajj | 1 fake gamma | W gamma +2j fixed order (+0..3j MLM in production) | WF, f_jet->gamma | veto events with >=2 prompt gamma (N_prompt_gamma==1) | pilot 8389 +- 27 fb, section 4 |
| F_Wjj | 2 fake gamma | W +2j fixed order (production: W+0..4j MLM) | WF, f^2 | veto >=1 prompt gamma | pilot 2.403e6 +- 0.010e6 fb, section 4 |
| F_Zajj_ee | e->gamma | Z(ee) gamma + 2j | f_e->gamma | N_prompt_gamma==1 | pilot 589.3 +- 1.9 fb, section 4 |
| X_aajj (non-prompt lepton) | bound | gamma gamma + 2j | f_lep | - | sigma 6308 +- 66 fb (pTg>20, 90<mgg<190); bound only, section 4 |
| T_tta_1l / T_ttaa_1l / T_tWa_1l | prompt/fake gamma | MG5 LO, t decays in ME, one leptonic W | WF_tt | photon-count vetoes as ZH | smoke sigma 414.6 / 0.4689 / 61.66 fb; N_req table section 5 |
| T_tt_1l | 2 fakes | LO semileptonic tt | WF_tt | N_prompt_gamma==0 | TBD; bound via f^2 |
| V_WZgamma, WWgamma | e->gamma | LO | in ME | photon-count veto | TBD (Delphes has no pixel-seed veto -> parametrised f_e->gamma) |
| WH other H modes (ggF/VBF H with fake lepton) | documented | - | - | - | needs f_lep <= 1e-3 and MET: expected << 1e-2 ev; to be bounded with the aajj-style arithmetic, not assumed zero |

## 3. Reuse of frozen ZH samples (lost lepton)
Script `scripts/zh_lostlepton.py` (read-only on `production/{v1,final}`): pre-selection exactly 1 lepton pT>25, MET>30, >=2 photons pT>20, >=2 jets pT>25 with m_jj>500 and |d eta|>2.5 (no b-veto, no m_gg window). Yield = counts x sigma x BR ledger x 500 fb^-1 / N_used; MC error sqrt(N). JSONs `work/lostlep/*.json`.
| Sample (files, N used) | counts: 1l+gg / +MET / +VBS | VBS yield at 500 fb^-1 |
|---|---|---|
| ew_zhjj_zll (6, 12k of 200k) | 2576 / 682 / 323 | 0.0387 +- 0.0022 |
| qcd_zhjj_zll (6, 12k of 100k) | 2026 / 467 / 41 | 0.0387 +- 0.0060 |
| H_ggZH_py8dec (2, 4k of 20k) | 878 / 176 / 19 | 0.0270 +- 0.0062 |
| H_ZH_tautau (4, 5.2k of 6.6k) | 246 / 163 / 3 | 0.016 +- 0.009 |
| H_ttH dilepton (8, 16k of 42k) | 3008 / 2701 / 148 | 0.190 +- 0.016 |
| T_ttaa dilepton (10, 20k of 22k) | 3490 / 3139 / 190 | 0.461 +- 0.033 |
| T_tWa dilepton (10, 20k of 160k) | 416 / 361 / 19 | 6.2 +- 1.4 (direct-Delphes fakes; no b-veto) |
| T_tta dilepton (20, 40k of 1.04M) | 579 / 494 / 33 | 35 +- 6 (direct-Delphes fakes; no b-veto) |
Reading: Higgs-resonant lost-lepton backgrounds from ZH are each ~0.02-0.2 events pre m_gg-window (vs signal-like ~0.6 events after the same type of illustrative cuts, Phase 03), i.e. a few percent to tens of percent; the dileptonic tt gamma / tW gamma lost-lepton classes are large before b-veto and m_gg window and need the full production samples and the b-veto to quantify. These are subsets: not final yields. Phase space is covered because the ZH samples apply no lepton cuts in the decay (cut_decays False) and loose jet cuts; the VBS-biased ZH continuum samples are NOT reused for lost-lepton (their generation cuts are Z-specific).

## 4. Fake and non-prompt bounds (parametrised, NOT data-driven)
Fake model as frozen ZH: f(j->gamma)=1e-3 (pT/50)^-0.5 (x2 endcap) with scenario factors {0.3,1,3}; fake pT = x pT_jet, x~N(0.85,0.10); f_e->gamma in {1,2,5}%. Scripts: `scripts/fakefactor_pilot_wh.py` (WH variant of lib), `scripts/efake_zgamma_pilot.py`. Samples: 5000 fixed-order events, PY8 + slim Delphes + GenTruth (`work/pilots/*`). Overlap rule N_prompt_gamma=0 (W+jets) / =1 (W gamma+jets) from GenTruth. Regions (illustrative, not optimised): PRE = 1 lepton pT>25 + MET>30 + 2 (fake/real) photons + >=2 tag jets pT>30; VBS = + m_jj>500, |d eta|>2.5; PEAK = + 120<m_gg<130. Events at 500 fb^-1, nominal scenario.
| Pilot | PRE | VBS | PEAK | notes |
|---|---|---|---|---|
| W+2j, 2 fakes (sigma 2.403e6 fb) | 440 (N_eff 100) | 27.9 (N_eff 18) | **1.68** (N_eff 4.7, 6 MC ev) | lower bound: only 2 ME partons, extra tag jets only from shower; weights x0.3..x3 scenario scale as f^2: 0.15..15 |
| W gamma+2j, 1 fake (8389 fb) | 994 (N_eff 269) | 92.5 (N_eff 42) | **6.4** (N_eff 5.8, 7 MC ev) | lower bound; one prompt gamma; scenario scale f: 1.9..19 |
| Z(ee) gamma+2j, e->gamma (589.3 fb) | 77 MC ev | 9 MC ev -> 10.6 at f_e=2% (5.3-26.5 for 1-5%) | 2.4 at 2% (2 MC ev) | one e is lepton, other e fakes a photon; MET>30 kept |
Lost by parton-level HT filters in W+2j VBS: 32% (HT>100), 54% (>150): generator-level HT filters would NOT be safe for the fake samples. Conclusion: the reducible backgrounds with jet->gamma and e->gamma fakes are, at the nominal fake rates and BEFORE b-veto, photon-ID pT/m_gg cuts and a tight m_gg window, of order 1-10 events at 500 fb^-1 in the PEAK region versus an illustrative signal ~0.6 events: they cannot be neglected and are stat-limited (N_eff<10). Non-prompt lepton, gamma gamma+jets: sigma 6308 fb x 500 fb^-1 x f_lep(<=1e-3) = <=3.2e3 events if EVERY event had a fake lepton and no MET requirement: this is a trivial upper bound, not a result; MET>30 with a fake lepton is a tail effect that needs MC (D-WH-2/Phase 04). No zero is claimed for any of these.
Decay-level caveat: Delphes jet->gamma/e->gamma are not trusted (no pixel-seed veto, simplified pi0 isolation), hence the parametrisation.

## 5. N_MC requirement (N >= max(50k, sigma x BR x 3000 fb^-1); `config/br_ledger.json`)
| Sample | sigma x k [fb] | N_req | Status |
|---|---|---|---|
| S_EW_WHjj | 0.0617 | 50 000 | feasible |
| H_QCD_WHjj | 0.1295 | 50 000 | feasible |
| H_ttH_1l | 0.2384 | 50 000 | feasible |
| T_ttaa_1l | 0.455 | 50 000 | feasible |
| T_tWa_1l | 59.9 | 179 617 | feasible, direct Delphes |
| T_tta_1l | 402.6 | **1 207 739** | feasible only as ZH (1.04M, 520 jobs); decision D-WH-2 |
| F_Wajj (fixed 2j) | 8054 | 2.4e7 | **brute force infeasible** (D-WH-2) |
| F_Wjj (fixed 2j) | 2.31e6 | 6.9e9 | **impossible** (D-WH-2) |
Required: a pre-declared effective-N policy for fake-type samples (extend handoff 5.3 to WH) or VBS-biased generation proven safe by twin samples; raised as D-WH-2, not relaxed silently.

## 6. Overlap-removal contract
As frozen ZH 02 section 3: N_prompt_gamma partition (W+jets: 0; W gamma+jets: 1; W gamma gamma+jets: >=2), prompt = no hadron ancestor after PY8 (ME + QED shower photons), same pT/eta/dR as the ME cuts of the higher-multiplicity sample, QED shower ON everywhere; stability test 15->20 GeV and photon-pT/dR continuity at boundaries are Phase 04 validation (not done here). tt/ttgamma/ttgammagamma and tW likewise. EW vs QCD by coupling order; interference signed. W gamma gamma: on-shell W chain, beam-split as ZH. Generator-cut safety by twin samples (looser generation cut) is a Phase 04 deliverable per sample; not demonstrated yet.

## 7. Checks / caveats / next
Checked: reuse coverage numerically; pilot machinery reproduces ZH conventions; sigma sources are labelled. Not done (honest): B_EW/QCD Waajj sigma (timeouts), tHq/tHW/tt_1l cards and sigma, MLM merging validation, twin samples. Heavy: all deferred to Phase 04 after decisions D-WH-2/3. Next: Phase 04 production plan with N table above.
