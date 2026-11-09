#!/usr/bin/env python3
import json, datetime
WH="/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh"
d=json.load(open(f"{WH}/work/bgmodel/yields.json")); rt=json.load(open(f"{WH}/work/bgmodel/rate_table.json")); clo=json.load(open(f"{WH}/work/bgmodel/rate_closure.json"))
L=[]; A=L.append
A(f"# 05a Background model (executor-wh FINAL, block 1)\n\nDate UTC: {datetime.datetime.utcnow():%Y-%m-%d %H:%M}. Status: **PASS for verification request** (selection NOT started; waiting for verifier/review). Git commit: see orchestrator commit. **Version v2 (reissue after review reviews/wh_05a_background.md, HOLD).**\n")
A("""## Changelog v1 -> v2 (review HOLD, all items)
1. (sev-1) Frozen multi-directory ZH rows: directory label now derived from the file-name prefix (skim metadata held bare file names), N and sum w per directory. Check below: sum w/N equals SAMPLES sigma for every row (ZH_Zajj_eFake 0.08039 vs 0.08051 pb). PEAK eFake before C 2.41 (v1: 1.14), Zaajj EW 0.113 (v1: 0.040).
2. (sev-1) C factors applied in VBS/PEAK (Zajj QCD 1.866 with range [1, 2.732] = the 87 % C systematic; Zaajj EW 0.958 +- 0.061); PRE: C = 1 (lower limit), bound [min(1,C), max(1,C)]. The ZH_Zajj nomjj top-up is NOT generated (human question c).
3. (sev-1) D35: light-misID bounds are x0.3 / x3 of the nominal (D36 envelope; switchable `--nonprompt-lo/--nonprompt-hi`); electron-only and the loose 2e-3 are no longer bounds. 2e-4 / 2e-3 per flavour are reported as labelled robustness variants and the x100 scan is labelled beyond D36. Deviation to log in SPEC section 7 (orchestrator): v1 used low = electron only, high = loose 2e-3 per flavour (contradicts D35); the Q_aajjj D29 trigger (Q_aajj 28-31 % > 10 % of SR background) was evaluated at f_l = 2e-3 (D28 loose); at the D35 nominal the trigger would not fire (Q_aajj fraction <1 %); Q_aajjj remains the nominal row (already produced, harmless).
4. (sev-2) one-sided non-closure systematic x0.4 on the one-fake low bound (measured direct/FF ratio 0.39 PRE, 0.41 VBS, see sec. 2). 5. D39 floor +-20 % is a declared nuisance and is in the bounds. 6. direct count labelled a LOWER LIMIT of the true upper variation (3-jet row only; artefacts lie outside jets, a 2j row would add); converted-jet generator-cut safety (04 sec. 19(2), scripts/convjet_cut_safety.py): weighted fraction of conversions with GenJet pT < 20 GeV 1.4 %, < 25 GeV 3.7 %, < 30 GeV 8.1 % (safe, < 5 % at the generator cut). 7. factorised heavy-flavour variant added (sec. 3), UL kept. 8. see item 3 (D29 trigger at 2e-3). 9. nuisance list below. 10. zero-support ULs in the direct variation are reported (column ULdir), r_tau on Z rows justified (sec. 5), commit placeholder.

## Pre-declared nuisance list for the statistics stage (fixed here, before any selection)
(1) MC statistics per bin (Barlow-Beeston), (2) tau uplift +-100 % of r_tau (D9), (3) QCD 7-point scale envelope per process class, (4) D29 PS-modelling 100 % on V_WWa/WZa/ZZa and on the missing 2j+PS fake topology, (5) D27 two-fake per-photon scenarios x{0.3,1,3} (yield x{0.09,1,9}), (6) generator-cut C systematic (Zajj QCD [1, 2.732], Zaajj EW +-6.4 %), (7) D39 calibration floor +-20 % on the fake-photon rate (correlated one-/two-fake), (8) one-sided fake-photon non-closure -60 % (one-fake), (9) non-prompt light-misID normalisation x0.3-x3 (D36) with robustness variants 2e-4 / 2e-3, (10) heavy-flavour non-prompt-lepton factorised variant +-100 % with the UL as conservative variant, (11) luminosity and theory (combination stage). D36 scans: fake photons and non-prompt leptons separately, x0.3-x3.

## Goal
Background model for pp -> WHjj (W->l nu, H->gamma gamma) at 13.6 TeV, L = 500 fb^-1, Delphes level: class table with lower/upper bounds for fake photons (D34 a'), non-prompt leptons (D35), e->gamma / lost lepton, irreducible and other Higgs; zero-support rows with Poisson ULs. Not the final selection: the regions below are block-level (PRE/VBS/PEAK, scripts/bgmodel.py `regions`).

## Inputs / versions
wh-prod-v1 (p2/production/wh, SAMPLES.csv, FORMAT.md), frozen ZH rows read-only from production/final, production/v1. Stack LCG_110 (scripts/envrun.sh). Normalisation: events = L*1e3*k*sum(w_pb*f)/N_gen (per directory for frozen ZH rows). Seeds: skim RNG seed = file seed + 777. No new samples, no git.

## Commands (all in wh/scripts, outputs in wh/work/bgmodel)
veto_validation.py (login, 5 k-event test files) -> veto_validation.json; rate_genuine.py via condor (cluster 899742, 484 jobs, schedd bigbird103) -> rate_table.py -> rate_table.json, rate_closure.json; skim.py via condor (899730: 761 jobs, 899824: 741 jobs; all 1502 exit 0, 0 missing outputs); bg_yields.py -> yields.json (log bg_yields.log); this report: make_report_05a.py. Failed attempt: cluster 899728 (argument order bug, removed, its 70 good outputs identical to the rerun).

## 1. Artefact veto (D34, validation on *_full.root)
Truth label = sum of E of the unique particles in Photon.Particles / E_reco >= 0.5 (reviewer's test; 575 lepton-free non-prompt-origin photons pT>10 over 35 test files). GenTruth proxy R = sum pT(GenTruth status-1 photons pT>10, within dR<0.2)/pT_reco; veto: artefact if R<0.5. Result: pT>20: 73 of 73 truth-genuine kept, 0 of 123 truth-artefact leaked; pT 10-15: proxy keeps 1/55 genuine (GenTruth threshold is 10 GeV), so the rate numerator and all photon use is restricted to reco pT>20. Cut variants 0.3 and 0.7 give identical purity (0 leaks) and 80 vs 77 kept (all photons). Only 8/575 photons have E_ref/E in (0.1,0.9) (labels are unambiguous). Fraction artefact at pT>25: 87/158 = 55 %.
Finding: photons matched to a GenJet within dR<0.2 are almost all genuine (artefact numerators in the jet cone are 0-4 per bin, table below): the energy-flow artefacts lie outside jets, so the decontaminated per-jet rate is essentially the earlier lepton-decontaminated rate; the artefact class enters only through the direct count (upper variation).

## 2. Fake photons (D34 option a')
Nominal: fake factor f(jet pT, |eta|) from genuine in-jet photons only (W-class from all 465 F_Wjjjj files, TT-class from 19 T_ttjj_1l files; bins with <5 genuine counts use the pooled rate), x = photon pT/jet pT from the measured genuine histogram, jet consumed, photon pT>20, applied to reco jets pT>25 |eta|<2.5 (dR>0.4 to lepton and the real photon). One-fake rows (F_QCD_Wajjj, F_EW_Wajj, T_tta, T_tWa; n_prompt_photons==1) and two-fake rows (F_Wjjjj, T_ttjj_1l; n_prompt_photons==0, weight f_a*f_b). Energy-flow artefact photons never enter the nominal. Variants: stat up/dn (Clopper-Pearson 68 %), veto cut 0.3/0.7, QCD 7-point scale envelope. UPPER variation: direct Delphes count including artefacts (kind 4). Closure test: direct genuine count (kind 3) vs nominal.""")
A("Rate table (genuine in-jet photons), per jet-pT bin [25,35,50,75,100,150,1000] (percent):")
for c in ("W","TT"):
    A(f"- {c} barrel {[round(x*100,5) for x in rt['nom_'+c][0]]}; endcap {[round(x*100,5) for x in rt['nom_'+c][1]]}; genuine counts {rt['num_gen_'+c]}; artefact counts in jet cone {rt['num_art_'+c]}; N_jets (barrel) {[int(x) for x in rt['den_'+c][0]]}")
A(f"- disjoint even/odd closure of the W rate: {clo}")
A("""
**2j F_QCD row (brief 2a): not needed.** The nominal fake consumes a jet; one-fake topologies with two tag jets plus the converted jet need three hard jets, which F_QCD_Wajjj (3 ME jets, regions with >=3 reco jets incl. the converted jet: automatic here) covers; two-fake topologies need four jets (F_Wjjjj, W+4j). The Delphes artefact class, which would have needed the 2j sample, is excluded from the nominal. The remaining missing 2j+PS-jet topology is covered by the pre-declared 100 % PS-modelling uncertainty of D29 (statistics stage, not folded into the bounds below).
**Calibration to CMS (D34, open decision D39 = D-WH-17).** Record verified: CMS-SMP-19-013, JHEP 10 (2021) 174, arXiv:2105.12780, Table 2: misidentified-jet background 918 +- 23 (stat) +- 180 (syst) (e nu gamma gamma), 1441 +- 27 +- 280 (mu nu gamma gamma) of 2052 / 2334 predicted events (45 % / 62 %); Z channels 42 +- 4 +- 9 and 98 +- 5 +- 27; HEPData ins1865855 (DOI 10.17182/hepdata.113759.v1), Fig. 2 gives the pT(gamma gamma) distribution per process. No comparison with this model is possible: the frozen samples contain no inclusive (no-VBS-cut, <=2-jet) W+jets / W gamma+jets sample, the CMS selection is inclusive in jets, and F_Wjjjj / F_QCD_Wajjj are exclusive 4- and 3-parton rows. Default: calibration factor c = 1 (switch `--ccal-photon`, one-fake x c, two-fake x c^2), systematic floor +-20 % (CMS syst/yield 19.6 %), the D36 scan x0.3-x3, and the direct-count upper variation. A human answer (or a new inclusive sample) is a re-run of bg_yields.py with a different c, not a redesign.""")
A("""
## 3. Non-prompt leptons (D35, D40 = D-WH-18)
Heavy-flavour leptons: directly from the Delphes MC (rows with a reco lepton in Q_aajjj / H_VBFH_jj, weight 1, lepton isolation <0.15). Light-hadron misID: each jet pT>25, |eta|<2.4 of the sample's own jets is the lepton with weight f_l, lepton pT = x*pT_jet (x~N(0.85,0.1) truncated [0.5,1]: an uncited assumption), events without a reco lepton, jet consumed. Nominal rows: Q_aajjj (gamma gamma + 3 jets, replaces Q_aajj per D29), H_VBFH_jj; H_ggF_jj missing (gridpack 893012 still running; D38 fallback). Q_aajj is a cross-check, not in the class. f_e = 2e-5 (tight, ATLAS EPJC 72 (2012) 1909, arXiv:1110.3174 sec. 4.4, jet rejection about 5e4, identification only); f_mu = 2e-5 is a PLACEHOLDER equal to the electron value (D40: no citable per-jet muon value found; the CMS per-hadron value 0.1-0.5 % of arXiv:1804.04528 cannot be converted without an invented multiplicity); switches `--f-electron --f-muon --f-high`. Bounds (v2): low = x0.3, nominal = 4e-5 total (e + mu placeholder), high = x3 (D36 envelope, human question a pending). Robustness variants, NOT bounds: 2e-4 and 2e-3 per flavour (D35: 2e-3 is not an upper bound) and the x100 scan (beyond D36). Calibration to a published CMS non-prompt-lepton fraction: none found in a comparable final state (CMS Wgg/Zgg lists only misid jets, misid electrons, others). Heavy flavour: nominal = direct Delphes rows; factorised variant = direct PRE rate x (kind-5 yield region/PRE), +-100 % (about 0.055 in PEAK for Q_aajjj, entering the high bound as 2x); the zero-raw-row UL (0.47 + 0.28) is kept as the conservative variant.""")
A("""
## 4. e->gamma and lost lepton
Direct Delphes MC (V_WWa/WZa/ZZa without ME jets, frozen ZH_Zaajj lost-lepton rows, ZH_Zajj_eFake with the Delphes e->gamma object, photon class cls1 = within dR<0.2 of a prompt generator lepton). The measured Delphes e->gamma rate of FORMAT.md 6b (3.8-15 % for electrons, 0.5-0.7 % for muons) is the rate the direct MC already contains (cross-check in work/postprod/egamma_rate.json); no extra weighting. Generator-cut factors C (vbs rows mmjj>400; measured at the WH reco-SR proxy mjj>500, |deta|>2.5, 04 sec. 15(7)): Zajj QCD part 1.866 (range [1, 2.732] = full difference, the 87 % systematic), Zaajj EW 0.958 +- 0.061, applied in VBS/PEAK; the EW part of ZH_Zajj_eFake gets C = 1 (EW twin loss 2.4 +- 0.3 %). PRE has no mjj cut (the skim superset has mjj>300): C = 1 (lower limit) with bound [min(1,C), max(1,C)]. The Zaajj nomjj row needs none. Bounds: 7-point scale envelope and tau factor; V_* rows additionally carry the D29 100 % PS-modelling uncertainty (statistics stage).

## 5. Tau factor (D9)
r_tau = Y(S_EW_WHjj_taunu)/Y(S_EW_WHjj) per region (about 0.082). W/Z-containing classes: nominal x(1+r_tau), bounds [1, 1+2 r_tau]. S_EW_WHjj_taunu is listed separately as a signal-like feed-down.

## 6. Class tables (events at 500 fb^-1, Delphes level, BR applied once)
Bounds are low/high of the declared variations (bg_yields.py docstring); stat = weighted-MC uncertainty of the nominal; UL0 = sum of 95 % Poisson ULs (2.996 x unit weight x f) of rows with zero raw support. Raw N and N_eff per sample follow.""")
for rn in ("PRE","VBS","PEAK"):
    R=d["regions"][rn]; A(f"\n### {rn} (r_tau {R['r_tau']:.3f}; lepton iso<0.15)\n\n| class | nominal | low | high | MC stat | UL0 (nominal rows) | UL direct variation | missing |\n|---|---|---|---|---|---|---|---|")
    for c,v in R["classes"].items(): A(f"| {c} | {v['nom']:.4g} | {v['low']:.3g} | {v['high']:.3g} | {v['stat']:.2g} | {v['UL95_sum_zero_support_rows']:.3g} | {v['UL95_sum_direct_variation']:.3g} | {','.join(v['missing_samples']) or '-'} |")
    A("\n| sample | nominal Y | raw N | N_eff | variants / UL |\n|---|---|---|---|---|")
    for s,r in R["samples"].items():
        if "direct_all_kind4" in r:
            k3,k4=r["direct_genuine_kind3"],r["direct_all_kind4"]
            A(f"| {s} | {r['nom']['Y']:.4g} | {r['nom']['nraw']} | {r['nom']['neff']:.0f} | dn {r['dn']['Y']:.3g} up {r['up']['Y']:.3g} R0.7 {r['r07']['Y']:.3g}; direct genuine {k3['Y']:.3g} (raw {k3['nraw']}, UL {k3.get('UL95',0):.3g}); direct incl. artefact {k4['Y']:.3g} (raw {k4['nraw']}, UL {k4.get('UL95',0):.3g}) |")
        elif "fakelep_nom" in r:
            h=r["heavy_flavour_direct"]; f=r["fakelep_nom"]
            A(f"| {s} | {f['Y']+h['Y']:.4g} | {f['nraw']} + {h['nraw']} direct | {f['neff']:.0f} | misID nominal {f['Y']:.3g} (low {r['fakelep_low']['Y']:.3g}, high {r['fakelep_high']['Y']:.3g}); heavy-flavour direct {h['Y']:.3g} (UL {h.get('UL95',0):.3g}) |")
        else:
            n=r["nom"]; A(f"| {s} | {n['Y']:.4g} | {n['nraw']} | {n['neff']:.0f} | {'UL95 %.3g'%n['UL95'] if 'UL95' in n else ''} |")
A("""
## 7. Checks and caveats
- All 1502 skim jobs and 484 rate jobs exit 0 (counts match make_sub_py.py 'todo = 0'). Skim superset cuts (mjj>300, |deta|>2, mgg 100-180) are looser than the regions here.
- One-fake closure (direct genuine / nominal) is poor at the available statistics (see F_QCD_Wajjj: direct genuine 0.95 events (6 raw rows) in PRE vs 2.4 nominal, 0 in PEAK (UL shown)): not a validation of the nominal; the direct count with artefacts (upper variation) is 3-4x the nominal in PRE/PEAK and is carried only in the high bound.
- Two-fake: direct counts have zero raw support, UL (31.8 / 292 events) is far above the fake-factor prediction (0.05 / 0.01): uninformative, as the prediction is 3 orders below it.
- Non-prompt-lepton nominal is a parametrisation with uncited x distribution and a placeholder muon rate (D40); heavy-flavour direct has 5 raw rows in PRE and zero in PEAK (UL carried). H_ggF_jj missing.
- Region PRE/VBS/PEAK are block-level; b-veto uses at most the 6 stored remaining jets; no lepton isolation variation here; K-factors not applied (LO), no EW-QCD interference for Waajj.
- ZH_Zajj_eFake dominates the lost-lepton class; its C range is wide (the 87 % systematic); human question (c) (top-up) open.
- PS-modelling (D29 100 %) and D27 f-scenarios are statistics-stage nuisances, not in low/high.

## 8. Next
Wait for verification/review of this block; then selection (05_selection.md). H_ggF_jj when 893012 ends (D38 fallback UL otherwise).
""")
open(f"{WH}/reports/05a_background_model.md","w").write("\n".join(L))
