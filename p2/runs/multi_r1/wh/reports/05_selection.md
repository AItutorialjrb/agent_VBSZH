# 05 Selection (executor-wh FINAL, block 2)

## 0. Pre-declaration (written 2026-11-09T05:10:23Z, BEFORE any selection scan was run)
Inputs: skims of 05a (rows of the VBS block region), table work/sel/table.npz built by scripts/sel_tables.py with the NOMINAL background model of 05a v2.1 (fake factor nominal, f_l nominal, C central, tau factor, no variations). No data exist; the "sidebands/signal window reserved" requirement is honoured by optimising on expected MC yields only and by never using the observed-like quantity.
**Baseline (fixed, not scanned):** exactly one lepton pT>25 (iso<0.15), no second lepton pT>10, MET>30, b-veto, both photons pT>25 (|eta|<2.5, no crack), two leading remaining jets pT>30 (generator-safe for the converted jet, 05a), 100<m_gg<180 stored.
**Scanned grid (cut-based, all combinations):** m_jj > {500,600,700,800,900}; |deta_jj| > {2.5,3.0,3.5,4.0}; pT(gamma gamma) > {0,50,75,100}; MET > {30,40,50}; m_T(l,MET) > {0,40,60}; pT(l) > {25,30,35}; m_gg window half-width around 125.0 GeV {2.5,3.5,5.0} (signal sigma_eff = 2.10 GeV, mean 125.06); Zeppenfeld z* = |eta(gg)-(eta_j1+eta_j2)/2|/|deta_jj| < {none,1.0,0.7}.
**Metric:** Eq. 1 Asimov significance Z = sqrt(2((s+b)ln(1+s/b)-s)) at 500 fb^-1, stat only, s = def. (a) signal (S_EW_WHjj), b = sum of all other classes (QCD WH, tau feed-down, other Higgs, prompt, fakes, non-prompt leptons, lost-lepton/e->gamma) at nominal.
**Admissibility:** total-background MC N_eff >= 30 and relative MC uncertainty of b <= 30 % (no selection driven by an MC fluctuation).
**Choice rule (against noisy maxima):** among admissible cut sets with Z >= 0.97 Z_max (plateau) take the LOOSEST one, i.e. the one with the largest signal yield; ties by larger b N_eff. The chosen set is then frozen; the final significance is computed only afterwards (07).
**MVA (second step):** K = 5 k-fold (fold = hash of (sample, event) mod 5), disjoint training/evaluation, gradient-boosted decision tree on the same variables (m_gg excluded from the inputs, window applied afterwards), 3 seeds; cut on the score chosen by the same plateau rule on the held-out predictions only; adopted only if Z gain > 10 % over the cut-based result AND stable (fold-to-fold and seed-to-seed spread of Z < 10 %, N_eff per fold stated). Both are reported.

## 1. Results (scan run after the pre-declaration above; scripts/sel_tables.py, sel_scan.py, sel_mva.py, sel_final.py; logs work/sel/*.log)
Grid: 19440 cut sets; admissible (N_eff>=30, rel MC<=30 %): 19336; plateau (Z >= 0.97 Zmax): 19 sets.
**Z_max (noisy-scan maximum, NOT chosen):** Z = 0.446 (s = 0.459, b = 0.920, N_eff = 66) with {'mjj': 600, 'deta': 4.0, 'ptgg': 100, 'met': 30, 'mt': 40, 'ptl': 25, 'hw': 3.5, 'zs': 0.7}.
**Chosen cut-based selection (frozen):** {'mjj': 600, 'deta': 4.0, 'ptgg': 75, 'met': 30, 'mt': 0, 'ptl': 25, 'hw': 3.5, 'zs': 99}: s = 0.612, b = 1.793 events at 500 fb^-1, Z(Eq. 1, stat only) = 0.434 (= 97.5 % of Z_max), b N_eff = 134, rel. MC unc. 0.086. The lepton/MET/mT/z* requirements are not binding on the plateau (baseline values retained). Note |deta_jj| > 4.0 is the upper EDGE of the pre-declared grid: the pre-declared grid is kept (extending it after the fact would be a post-hoc scan; not adopted, noted as a limitation).
**MVA (K = 5, xgboost, 3 seeds, held-out predictions, ensemble-mean score):** choice {'s': 0.7290670394973451, 'b': 1.1651028976769422, 'Z': 0.618781385134298, 'neff': 138.9454616437918, 'relmc': 0.08483553773313955, 'thr': 0.7128861207511201, 'hw': 5.0}: s = 0.729, b = 1.165, Z = 0.619, N_eff = 139; per-seed Z = [0.6187, 0.6243, 0.619] (seed spread 0.9 %). Per-fold Z (yields x5) = [0.624, 0.562, 0.681, 0.615, 0.635]: relative RMS 6.1 %, range 19 %; per-fold background N_eff = [19, 24, 63, 38, 49]. Same for the cut-based set: per-fold Z [0.428, 0.44, 0.405, 0.406, 0.51], relative RMS 8.8 %.
**Gain MVA over cut-based: 42.5 %** (> 10 %). Stability: seed-to-seed spread < 10 % and fold-to-fold relative RMS 6.1 % < 10 % (the fold range, 19 %, exceeds 10 %, but the per-fold b N_eff of 19-67 implies a pure-MC-statistics fluctuation of Z of 6-12 %; the cut-based set has the same fold spread). **Decision: MVA adopted as the primary selection, cut-based reported and carried in parallel** (the pre-declared word "spread" is read as the relative RMS; if a reader takes it as the range, the cut-based set stays primary: both are carried through 07, a one-line switch). The MVA models (work/sel/model_seed*_fold*.json) are applied unchanged to the coupling samples (average of the 5 fold models) in the coupling block.
Caveat: threshold, window and hw were chosen on the same held-out predictions that are then used for the yield (no independent test set; the plateau rule limits, but does not remove, optimism: MC N_eff 139 at the MVA point).

## 2. Final tables (events at 500 fb^-1, nominal background model of 05a v2.1, MC stat only; raw N and N_eff per class)
| class | cut-based Y | stat | raw N | N_eff | MVA Y | stat | raw N | N_eff |
|---|---|---|---|---|---|---|---|---|
| signal | 0.6122 | 0.0068 | 8157 | 8053 | 0.7291 | 0.0074 | 9704 | 9600 |
| prompt_irreducible | 0.9767 | 0.13 | 193 | 53 | 0.6226 | 0.083 | 164 | 56 |
| fake_photon_1 | 0.02938 | 0.00064 | 2577 | 2090 | 0.01771 | 0.00052 | 1402 | 1150 |
| fake_photon_2 | 0.0007642 | 9.5e-06 | 12874 | 6461 | 0.0004892 | 7.2e-06 | 7207 | 4600 |
| nonprompt_lepton | 0.01267 | 0.00027 | 2204 | 2123 | 0.006174 | 0.00019 | 1169 | 1102 |
| lost_lepton_egamma | 0.507 | 0.076 | 130 | 45 | 0.2398 | 0.052 | 73 | 22 |
| other_higgs | 0.2151 | 0.013 | 2774 | 288 | 0.2226 | 0.013 | 2867 | 306 |
| tau_feeddown | 0.05162 | 0.002 | 650 | 634 | 0.05572 | 0.0021 | 701 | 685 |

| cutflow step | s | b | raw s | raw b |
|---|---|---|---|---|
| VBS block region (baseline, 100<mgg<180) | 1.02 | 66.28 | 13573 | 852592 |
| mjj>600 | 0.9356 | 55.48 | 12459 | 654521 |
| |deta|>4.0 | 0.8407 | 28.2 | 11198 | 333225 |
| pT(gg)>75 | 0.6799 | 15.74 | 9059 | 185181 |
| MET>30 | 0.6799 | 15.74 | 9059 | 185181 |
| mT>0 | 0.6798 | 15.74 | 9058 | 185168 |
| pT(l)>25 | 0.6798 | 15.74 | 9058 | 185168 |
| z*<99 | 0.6798 | 15.74 | 9058 | 185168 |
| |mgg-125|<3.5 | 0.6122 | 1.793 | 8157 | 21402 |

## 3. Checks and caveats
- Baseline of the optimisation: the VBS block region of 05a (same lepton/photon/jet definitions); the sidebands (100-120, 130-180) are kept in the table for the fit and were not used to tune anything beyond the mgg window half-width.
- F_QCD_Wajjj / Q_aajjj conditions (>= 3 reco jets incl. the converted jet) hold by construction of the rows (05a).
- The optimisation used the nominal backgrounds including C central for ZH_Zajj_eFake; the dedicated loose-cut sample (05a sec. 9, cluster 899916) and H_ggF_jj will change the lost-lepton and non-prompt-lepton yields but the selection stays frozen; their effect on Z is reported in 07.
- Remaining background after the MVA selection: prompt irreducible (Waajj) and lost-lepton/e->gamma dominate (table); fake photons and non-prompt leptons are < 3 % of b at nominal (their bounds and the D36 scan are in 07).
- Signal definition (b) (adding QCD WHjj and interference) is evaluated in 07 with the same selection.

## 4. Next
Verification of this block; statistics (06 systematics, 07 sensitivity incl. D36 scans), couplings, combination; production: F_QCD_llajj_loose 899916, H_ggF_jj 893012.

## 5. Addendum v2 (after the focused review, binding: reviews/wh_05_selection.md; orchestrator decisions D44/D45)
**Decisions (orchestrator defaults pending human D44/D45):** the CUT-BASED selection is the PRIMARY. The MVA is NOT adopted; it is an alternative result only. Deviation to log (SPEC section 7): section 1 read the pre-declared word "spread" as relative RMS after seeing a fold range of 19 %; that reading was post-hoc and is withdrawn (with the range reading the MVA fails the 10 % criterion). **Pre-declaration integrity:** section 0 was written in the same command that created the scan script (not committed before the scan, no independent timestamp); the selection ran on the 05a v2.1 weights before the 05a recheck conclusions were relayed; blinding itself holds (no data, expected yields only).
**Retraining trigger (D45, pre-declared now):** cuts and models are FROZEN and only re-evaluated when the v1.1 rows (F_QCD_llajj_loose, H_ggF_jj) arrive. Retraining only if the lost-lepton or the non-prompt-lepton share of the selected background b changes by more than 30 % (relative); then retrain with nested CV only. The primary (cut-based) is NOT re-decided.
**Fix 1 (m_gg leak, reduced, NOT removed):** pt1, pt2, ptgg, drgg rebuilt m_gg exactly; v2 inputs are pt1/m_gg, pt2/m_gg, ptgg/m_gg. The background m_gg sculpting is reduced but remains: background efficiency of the ensemble score cut by m_gg range (weighted MC, with MC errors): 100-110: 0.089 +- 0.009; 110-120: 0.078 +- 0.008; 120-130: 0.105 +- 0.009; 130-150: 0.088 +- 0.009; 150-180: 0.049 +- 0.005; sideband mean 0.076; the 120-130 GeV efficiency is +38 % relative to the sideband mean (3.2 sigma of its MC error), and the range over the other bins is 0.049-0.089 (v1 leak: 0.10-0.15 in 120-128 against 0.06-0.10 in the sidebands). Residual dependence of the score on m_gg (through mjj/mT/etc. correlations with the diphoton mass in the prompt background) means an MVA-based fit would need a sideband-validated shape; this is a further reason for D44 (alternative only).
**Fix 2 (nested threshold):** threshold and m_gg half-width chosen on 4 folds, applied to the 5th, summed: nested Z = 0.602 (s 0.709, b 1.172, N_eff 115); the ensemble (non-nested) point is Z = 0.621 (s 0.703, b 1.066, N_eff 142); per-seed non-nested Z [0.618, 0.612, 0.614] (the first-run value 0.621 quoted earlier belonged to the previous table). MVA nested gain over the cut-based set: 39 % (against the extended-grid diagnostic 0.456: 32 %).
**Fix 3 (|deta_jj| grid edge):** the declared grid ends at |deta_jj| > 4.0 and the primary sits on the edge. Diagnostic only (declared grid kept): deta > 4.5 gives Z = 0.456 (N_eff 110), deta > 5.0 gives 0.445; the extended-grid plateau rule picks {'mjj': 600, 'deta': 4.5, 'ptgg': 50, 'hw': 3.5} (Z 0.443): the cut-based reference is under-optimised by about 5 %.
**Fix 4 (rows carried as variants for 07):** (i) H_ggF_jj not yet produced (893012 running; the loop skips a missing skim, now logged here; D38 fallback UL until v1.1); (ii) heavy flavour: nominal = factorised variant (0.055 events in PEAK for Q_aajjj), direct-row variant (0 raw rows) and UL (0.474 + 0.283) are sensitivity variants (this removes the v1 difference 0.803 vs 0.8433); (iii) V_WWa/WZa/ZZa: zero MC rows at the selection (raw N = 0), UL 0.467 at PEAK, D29 100 % PS uncertainty acts on zero events: logged deviation, UL variant in 06 sec. 5; (iv) F_QCD_llajj_loose (899916) replaces the eFake QCD part when delivered.
**Fix 5 (disclosures):** fold = (evt + 3*sid) mod 5 (the hash reduces to this because 2654435761 = 1 mod 5); evt is not unique within a sample (fakes: several rows per event): rows of one event share (evt, sid) and therefore the fold, so event-level disjointness holds. Training uses |w| (1138 negative-weight rows in the table). Per-seed per-fold background N_eff {"11": [21.7, 23.2, 72.1, 22.4, 47.7], "22": [20.4, 27.0, 83.2, 42.2, 53.0], "33": [14.1, 24.7, 61.9, 25.9, 50.5]} (two folds < 30 in each seed); signal N_eff per fold {"11": [1936, 1844, 1787, 1798, 1895], "22": [2027, 1950, 1863, 1901, 1985], "33": [1991, 1944, 1853, 1864, 1969]}.
**Fix 6:** Barlow-Beeston (per-bin MC-stat nuisance, and with/without MC stat) is MANDATORY in 07: cut-based b = 1.801 has N_eff = 135.

**Refresh note:** after the table fix (factorised HF nominal, leak-free inputs) the pre-declared scan was re-run on the new table: the chosen cut set is unchanged ({mjj>600, |deta|>4.0, pT(gg)>75, hw 3.5}), s = 0.612, b = 1.801 (was 1.793), Z = 0.433, N_eff = 135. Sections 1-2 above quote the first run (b = 1.793, Z = 0.434).
**Final tables (current inputs, nominal = 05a v2.1; work/sel/selection_tables.md):**
| class | cut-based Y | stat | raw N | N_eff | MVA Y | stat | raw N | N_eff |
|---|---|---|---|---|---|---|---|---|
| signal | 0.6122 | 0.0068 | 8157 | 8053 | 0.7032 | 0.0073 | 9359 | 9259 |
| prompt_irreducible | 0.9767 | 0.13 | 193 | 53 | 0.5646 | 0.074 | 156 | 58 |
| fake_photon_1 | 0.02938 | 0.00064 | 2577 | 2090 | 0.01524 | 0.00049 | 1203 | 986 |
| fake_photon_2 | 0.0007642 | 9.5e-06 | 12874 | 6461 | 0.0004247 | 6.7e-06 | 6136 | 4017 |
| nonprompt_lepton | 0.02067 | 0.00046 | 2204 | 1989 | 0.008464 | 0.00029 | 1062 | 880 |
| lost_lepton_egamma | 0.507 | 0.076 | 130 | 45 | 0.2134 | 0.048 | 65 | 19 |
| other_higgs | 0.2151 | 0.013 | 2774 | 288 | 0.2101 | 0.012 | 2725 | 288 |
| tau_feeddown | 0.05162 | 0.002 | 650 | 634 | 0.05362 | 0.0021 | 675 | 659 |

| cutflow step | s | b | raw s | raw b |
|---|---|---|---|---|
| VBS block region (baseline, 100<mgg<180) | 1.02 | 66.33 | 13573 | 852590 |
| mjj>600 | 0.9356 | 55.43 | 12459 | 654519 |
| |deta|>4.0 | 0.8407 | 28.16 | 11198 | 333224 |
| pT(gg)>75 | 0.6799 | 15.82 | 9059 | 185181 |
| MET>30 | 0.6799 | 15.82 | 9059 | 185181 |
| mT>0 | 0.6798 | 15.82 | 9058 | 185168 |
| pT(l)>25 | 0.6798 | 15.82 | 9058 | 185168 |
| z*<99 | 0.6798 | 15.82 | 9058 | 185168 |
| |mgg-125|<3.5 | 0.6122 | 1.801 | 8157 | 21402 |

## 6. v1.1 re-evaluation with the FROZEN cuts and models (loose-cut eFake sample, D45)
Table work/sel/table_v11.npz (F_QCD_llajj_loose replaces the QCD part of ZH_Zajj_eFake; EW part kept). Cut-based (frozen): s = 0.612, b = 1.797 (before 1.801), Z (Eq. 1) = 0.434 (before 0.433), b N_eff = 63 (before 135; rel. MC 13 %). Frozen MVA (average of the 15 models, in-sample for the training rows, ratio only): Z 0.650 -> 0.667. **D45 trigger NOT fired** (lost-lepton share 28.1 % -> 28.0 %, non-prompt share 1.15 % -> 1.15 %; threshold 30 % relative): no retraining; the primary stays cut-based. H_ggF_jj not yet included (893012).
**Disclosure:** in v1.1 the lost-lepton class at the selection has N_eff = 7.6 (116 raw rows), Y = 0.503 +- 0.182 (36 % MC stat) and holds 64 % of the sum of squared weights of b; the loose-sample per-event weight is 27 x that of the replaced vbs QCD rows, and its QCD part rests on 1 raw row at the selection. The b N_eff drop 135 -> 63 is entirely this. Cross-check table (vbs twin x C range against the loose direct): 05a sec. 11. The nominal is not changed (final reviewer decides).
