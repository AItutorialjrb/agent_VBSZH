#!/usr/bin/env python3
"""ONE authoritative SR-like background total with its components and every D29 fraction recomputed from it (04 sec. 20(6)); writes work/background_total.json.
Region: pilot PEAK region (1 lepton pT>25, MET>30, two photons pT>25, >=2 tag jets pT>30, b-veto, mjj>500, |deta|>2.5, 120<m_gg<130), events at 500 fb^-1, production files, MC-statistical only.
Rows in the total: every delivered row in b (S_EW_WHjj_taunu included; S_EW_WHjj signal, the cross-check H_QCD_WHjj_fixed, the coupling samples K_*, and the frozen ZH rows excluded: the denominator is therefore a LOWER bound on the true total and the fractions are UPPER bounds).
Three bases for the one-fake and two-fake photon rows (the nominal method is the open question H1; no choice is made here):
  A 'fake_factor'   : per-jet fake factor (production table, class-specific) for all converted-jet rows (postprod_checks.json);
  B 'direct_1fake'  : direct Delphes counts (work/postprod/direct_all.json) for the one-fake rows F_QCD_Wajjj, F_EW_Wajj, T_tta, T_tWa (count 0 -> central 0), fake factor for the two-fake rows F_Wjjjj, T_ttjj_1l (no closure factor applied; their direct-count 95 % UL is in direct_twofake.json);
  C 'assumed_form'  : fake factor with the assumed form 1e-3 (pT/50)^-0.5 (x2 endcap).
Non-prompt lepton rows Q_aajj, H_VBFH_jj: nominal f_l = 2e-4; 'upper' = f_l 2e-3 for Q_aajj only (the D29 test point). Usage: python3 scripts/background_total.py"""
import json
WH = "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh"
pc = json.load(open(f"{WH}/work/postprod_checks.json")); da = json.load(open(f"{WH}/work/postprod/direct_all.json"))
rows = pc["D29"]["rows"]; PH = ["F_QCD_Wajjj_nomjj", "F_EW_Wajj_nomjj", "T_tta_1l", "T_tWa_1l", "F_Wjjjj", "T_ttjj_1l"]; ONE = PH[:4]
fixed = {s: v for s, v in rows.items() if s not in PH and s != "Q_aajjj"}   # prompt rows + Q_aajj + H_VBFH_jj (nominal f_l); Q_aajjj (ME+1-jet replacement of Q_aajj) is NOT added (it would double count Q_aajj): its yield is reported separately
qjjj = pc["pilots"].get("Q_aajjj", {}).get("yield_variants", {})
ff = {s: pc["pilots"][s]["yield_PEAK"] for s in PH}; asm = {s: pc["pilots"][s]["yield_variants"]["assumed"] for s in PH}; direct = {s: da[s]["PEAK"]["yield_500"] for s in ONE}
q_nom = fixed["Q_aajj"]; q_up = pc["pilots"]["Q_aajj"]["yield_variants"]["f2e-3"]
bases = {}
for name, ph in (("A_fake_factor", ff), ("B_direct_1fake", {**ff, **direct}), ("C_assumed_form", asm)):
    tot = sum(fixed.values()) + sum(ph.values()); tot_up = tot - q_nom + q_up
    bases[name] = dict(total=tot, components={**fixed, **ph}, total_with_Q_aajj_at_f_l_2e_3=tot_up,
                       F_QCD_Wajjj_fraction=ph["F_QCD_Wajjj_nomjj"]/tot, Q_aajj_fraction_nominal=q_nom/tot, Q_aajj_fraction_at_f_l_2e_3=q_up/tot_up,
                       Q_aajj_fraction_at_f_l_2e_3_wrong_denominator_for_reference=q_up/(tot-q_nom+q_up) if False else None)
    bases[name].pop("Q_aajj_fraction_at_f_l_2e_3_wrong_denominator_for_reference")
out = dict(definition=__doc__.split("Usage")[0].strip(), signal_PEAK=pc["D29"]["signal_PEAK"], Q_aajjj_yield_variants_not_in_total=qjjj, bases=bases)
json.dump(out, open(f"{WH}/work/background_total.json", "w"), indent=1)
for n, b in bases.items(): print(n, "total %.3f" % b["total"], "| F_QCD_Wajjj %.1f %%" % (100*b["F_QCD_Wajjj_fraction"]), "| Q_aajj nominal %.1f %%, f_l=2e-3 %.1f %% (total with Q at 2e-3: %.3f)" % (100*b["Q_aajj_fraction_nominal"], 100*b["Q_aajj_fraction_at_f_l_2e_3"], b["total_with_Q_aajj_at_f_l_2e_3"]))
