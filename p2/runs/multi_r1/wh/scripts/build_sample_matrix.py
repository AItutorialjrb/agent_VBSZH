#!/usr/bin/env python3
"""Builds config/sample_matrix.yaml (Phase 02 ledger) + prints the N_MC table. sigma values: measured interactive smoke runs
(work/smoke/*/status.txt, LO MG5 integration error), gridpack init cross sections when present (work/gridpacks/*_status.txt), frozen ZH numbers
(reports/FINAL_report.md tables) or labelled ESTIMATES (never 0). N_req = max(50k, sigma*k*3000 fb^-1) (SPEC 4.2). Infeasible (> NMAX) -> decision."""
import os, re, sys, yaml
sys.path.insert(0, os.path.dirname(__file__)); import br_ledger as B
WH = "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh"; NMAX = 2e7; L = 3000.0
def smoke(name):
    f = f"{WH}/work/smoke/{name}/status.txt"
    if not os.path.exists(f): return None
    m = re.search(r"Cross-section :\s+(\S+) \+- (\S+) pb", open(f).read())
    return (float(m.group(1))*1e3, float(m.group(2))*1e3) if m else None
def gp(name):
    f = f"{WH}/work/gridpacks/{name}_status.txt"
    if not os.path.exists(f): return None
    m = re.search(r"Cross-section :\s+(\S+) \+- (\S+) pb", open(f).read())
    return (float(m.group(1))*1e3, float(m.group(2))*1e3) if m else None
reg = yaml.safe_load(open(f"{WH}/config/sample_registry.yaml"))["samples"]
ROWS = []
def row(id, role, process, orders, cuts, sig, src, fac, wdec, hdec, overlap, N_plan=None, test=None, status="candidate", note=""):
    k = B.register(id, wdec, hdec, fac) if fac else None
    g = gp(id)
    if g is not None and id != "H_QCD_WH_mlm":      # gridpack init sigma (higher precision) preferred; MLM keeps the matched PY8 sigma
        src = "gridpack init sigma" + (f" (smoke run gave {sig[0]:.5g} +- {sig[1]:.2g} fb)" if sig else "") ; sig = g
    elif sig is not None and not src.startswith("condor"): src = "SMOKE RUN (no gridpack sigma yet): " + src
    if sig is None: sigv, err = None, None
    else: sigv, err = sig
    need = None if sigv is None else max(50000.0, abs(sigv)*k*L)
    inf = need is not None and need > NMAX
    ROWS.append(dict(id=id, idx=reg.get(id), role=role, process=process, orders=orders, gen_cuts=cuts, sigma_fb=sigv, sigma_err_fb=err, sigma_source=src,
        br_factors_external=fac, k_external=k, br_in_ME=wdec, h_decay=hdec, N_required=None if need is None else round(need), N_planned=N_plan,
        infeasible_N=bool(inf), overlap_rule=overlap, condor_test=test, status=status, note=note))
J20 = "ptj>20,|etaj|<5,drjj>0.4,drjl>0.4, cut_decays=False (no cuts on decay leptons), scale choice 3"
HD = "H->gg forced in PY8 (25:onMode=off, onIfMatch 22 22; cond. BR=1); B_gg=0.002270 external once"
row("S_EW_WHjj","signal (def a: EW only)","p p > w+ h j j QCD=0 QED=4, w+>l+ vl  (+ w- c.c.); p,j = g u c d s (no b)",[0,4],J20,
    smoke("S_EW_WHjj_smoke"),"smoke S_EW_WHjj_smoke (both charges, W->e/mu in ME)",["WF","BGG"],"W->e nu,mu nu in MG5 ME",HD,
    "order-exclusive vs QCD W H j j; top-resonant b-class excluded by external-flavour definition (tHq/tHW own samples)",200000,"EW fixed-order",
    note="N_planned follows ZH (200k)")
row("S_EW_WHjj_taunu","signal-like feed-down (W->tau nu->l nu nu)","as S_EW_WHjj with w+ > ta+ vt (+c.c.); tau decays in PY8",[0,4],J20,
    smoke("S_EW_WHjj_taunu_smoke"),"smoke S_EW_WHjj_taunu_smoke",["WFTAU","BGG"],"W->tau nu in MG5 ME; tau->l in PY8",HD,"disjoint from S_EW_WHjj by W decay mode",100000)
row("H_QCD_WH_mlm","resonant bkg (def a) / signal component of def b","p p > w+ h @0 ; +j @1 ; +j j @2 (+ w- c.c.), MLM xqcut 10, PY8 qCut 19",[2,2],"xqcut=10, ptj>10, scale -1",
    (302.3, 5.3),"condor test job H_QCD_WH_mlm_s2113001: PY8 sigma after MLM matching (4000 LHE ev, 1386 accepted = 34.6 %); cf. 0j proxy 280.3 fb, pre-matching gridpack 879.6 fb",["WF","BGG"],"W->l nu in MG5 ME",HD,
    "its 2-jet ME is QCD (2,2); EW (0,4) excluded by order; do NOT add H_QCD_WHjj_fixed",1000000,"MLM",note="DJR validation required in Phase 04 (as ZH)")
row("H_QCD_WHjj_fixed","cross-check only (VBS-region efficiency)","p p > w+ h j j QCD=2 QED=2, w+>l+ vl (+c.c.)",[2,2],J20,
    smoke("H_QCD_WHjj_fixed_smoke"),"smoke H_QCD_WHjj_fixed_smoke",["WF","BGG"],"W->l nu in MG5 ME",HD,"ALTERNATIVE to H_QCD_WH_mlm 2-jet bin; never added",100000)
row("I_WHjj","signed EW x QCD interference (def b); sigma is NEGATIVE (computed sign, not structural) (-0.264 +- 0.013 fb undecayed = -0.43 % of EW); enters s/b only as a signed signal-model systematic, never as events","p p > w+ h j j QCD^2==2 QED^2==6 (+ w-), W,H undecayed",[ "sq 2","sq 6"],J20,
    smoke("I_WHjj_smoke"),"smoke I_WHjj_smoke (W,H undecayed, both charges)",["BR_WLL","BGG"],"W undecayed in ME: physical B_PDG(l nu) applied externally (sigma-ONLY use; if events are ever showered the W must be decayed in PY8 with forced e/mu, cond. BR 1, and this k is then still applied once)",HD,"signed; separate component",50000,note="N_planned raised 20000->50000 (>= N_required, G1 item 1)")
row("H_ttH_1l","resonant bkg","p p > t t~ h, one t->b l nu, other t->b q q' (both assignments); p,j incl. b",[2,1],"no jet cuts, scale 3",
    smoke("H_ttH_1l_smoke"),"smoke H_ttH_1l_smoke",["WF","WHAD","BGG"],"t->b W, W->l nu / q q' in MG5 ME",HD,"external tops; distinct from WH",200000,"top")
row("H_tHq_lep","resonant bkg","p p > t h j $$ t~, t>b l+ vl (+ t~ c.c.), j light",[ "tHq", "t-channel"],"no jet cuts",
    smoke("H_tHq_lep_smoke"),"smoke H_tHq_lep_smoke (5F, j light)",["WF","BGG"],"t->b W->l nu in MG5 ME",HD,"disjoint from S_EW_WHjj (b-class excluded there)",100000)
row("H_tHW_1l","resonant bkg","p p > t w- h $$ t~ (DR-like s-channel veto), one W->l nu, other W->q q' (4 combos)",["tHW"],"no jet cuts",
    smoke("H_tHW_1l_smoke"),"smoke H_tHW_1l_smoke",["WF","WHAD","BGG"],"t->b W; W->l nu/qq' in MG5 ME",HD,"overlap with ttH by $$ t~ (DR); DS as systematic",100000)
row("T_tta_1l","1 fake gamma (+ prompt gamma)","p p > t t~ a, single-lepton (2 assignments)",[2,1],"pta>15,|etaa|<2.5, no jet cuts",
    smoke("T_tta_1l_smoke"),"smoke T_tta_1l_smoke",["WF","WHAD"],"t->b W->l nu / q q' in MG5 ME","no H","NOT overlap-removed (ZH closeout convention: 2nd photon mostly from top-decay products absent in the ttgg chain ME); double counting with T_ttaa_1l bounded by the T_ttaa_1l yield",None,"top")
row("T_ttaa_1l","irreducible prompt","p p > t t~ a a, single-lepton",[2,2],"pta>15,|etaa|<2.5, 90<maa<190",
    smoke("T_ttaa_1l_smoke"),"smoke T_ttaa_1l_smoke",["WF","WHAD"],"t->b W in MG5 ME","no H","full sample kept (sets the double-counting bound for T_tta_1l)",None)
row("T_tWa_1l","1 fake gamma","p p > t w- a $$ t~ + c.c., single-lepton (4 combos), DR",[2,1],"pta>15,|etaa|<2.5",
    smoke("T_tWa_1l_smoke"),"smoke T_tWa_1l_smoke",["WF","WHAD"],"t->b W; W->l nu/qq' in MG5 ME","no H","NOT overlap-removed (as T_tta_1l); DR vs DS as systematic",None)
row("T_tt_1l","2 fake gammas (bound)","p p > t t~, single-lepton",[2,0],"none",
    smoke("T_tt_1l_smoke"),"smoke T_tt_1l_smoke",["WF","WHAD"],"t->b W in MG5 ME","no H","N_prompt_gamma==0; bound by fake-factor pilot",None,note="N_required infeasible: DECISION D-WH-2")
row("B_EW_Waajj_vbs","irreducible continuum (EW)","p p > w+ a a j j QCD=0 QED=5, w+>l+ vl (+c.c.), on-shell W chain",[0,5],
    "pta>25,|etaa|<2.5,100<maa<170,mjj>400,ptj>20,|etaj|<5,dR>0.4,cut_decays=False",
    gp("B_EW_Waajj_vbs") or None,"gridpack init sigma if available else pending (ESTIMATE ~0.4 fb from ZH analogue x10.6)",["WF"],"W->l nu in MG5 ME","no H","order-exclusive vs QCD; ZH-style VBS-biased generation; interference I_Waajj via twin/aux",None,"continuum",
    note="20520 diagrams / 44 subprocesses (generate+output 155 s)")
row("B_QCD_Waajj_vbs","irreducible continuum (QCD)","p p > w+ a a j j QCD=2 QED=3 ,w+>l+ vl (+c.c.)",[2,3],"as B_EW + mjj>400",
    gp("B_QCD_Waajj_vbs") or None,"gridpack init sigma if available else pending (ESTIMATE ~0.4 fb)",["WF"],"W->l nu in MG5 ME","no H","fixed order; mjj>400 gen cut safe for reco mjj>500 only if twin ratio C holds",None,note="6984 diagrams / 52 subprocesses")
row("B_QCD_Waajj_nomjj","aux twin (ratio C only)","as B_QCD_Waajj_vbs with mmjj=0",[2,3],"as above, mmjj 0",
    gp("B_QCD_Waajj_nomjj") or None,"gridpack init sigma if available",["WF"],"W->l nu in MG5 ME","no H","never added to b: correction factor C only (as ZH)",None)
row("F_EW_Wajj_vbs","1 fake gamma (EW)","p p > w+ a j j QCD=0 QED=4, w+>l+ vl (+c.c.)",[0,4],"pta>25,mjj>400,...",
    gp("F_EW_Wajj_vbs") or None,"gridpack init sigma if available (ESTIMATE ~30 fb)",["WF"],"W->l nu in MG5 ME","no H","drop events with >=2 prompt photons (-> B_*)",None,note="2700 diagrams")
row("F_QCD_Wajj_vbs","1 fake gamma (QCD)","p p > w+ a j j QCD=2 QED=2, w+>l+ vl (+c.c.)",[2,2],"pta>25,mjj>400,...",
    gp("F_QCD_Wajj_vbs") or None,"gridpack init sigma if available (ESTIMATE ~200 fb)",["WF"],"W->l nu in MG5 ME","no H","drop events with >=2 prompt photons",None,note="1024 diagrams")
row("F_QCD_Wajj_nomjj","aux twin (ratio C only)","as F_QCD_Wajj_vbs, mmjj 0",[2,2],"mmjj 0",
    gp("F_QCD_Wajj_nomjj") or None,"gridpack init sigma if available",["WF"],"W->l nu in MG5 ME","no H","ratio C only",None)
row("F_Wjj_pilot","2 fake gammas (bound) pilot","p p > w+ j j , w+>l+ vl (+c.c.), fixed 2 partons",[2,1],"ptj>20,|etaj|<5,dR>0.4",
    smoke("F_Wjj_pilot_smoke"),"smoke F_Wjj_pilot_smoke",["WF"],"W->l nu in MG5 ME","no H","N_prompt_gamma==0; fake-factor weights (not Delphes fakes)",None,"fake pilot",note="N_required infeasible: DECISION D-WH-2")
row("F_Wajj_pilot","1 fake gamma pilot","p p > w+ a j j, w+>l+ vl (+c.c.)",[2,2],"ptj>20,pta>15",
    smoke("F_Wajj_pilot_smoke"),"smoke F_Wajj_pilot_smoke",["WF"],"W->l nu in MG5 ME","no H","N_prompt_gamma==1",None,"fake pilot")
# ---- frozen ZH samples (read-only reuse; sigma from reports/FINAL_report.md)
FZ = "frozen ZH (zh-final-v1.1), /eos/home-r/rjiang/vbs_zh_codex_starter/production/"
def frozen(id, role, sig, N, fac, path, cover, cuts):
    k = B.register(id, "frozen", "frozen", fac); need = max(50000.0, sig*k*L)
    ROWS.append(dict(id=id, role=role, sigma_fb=sig, sigma_source="FINAL_report.md table (ZH, LO MG5 init)", br_factors_external=fac, k_external=k, N_available=N,
        N_required=round(need), N_ok=bool(N >= need), path=FZ+path, coverage=cover, gen_cuts=cuts, status="frozen reuse"))
LL = "Z->ll in ME with cut_decays=False => NO generator cut on the decay leptons: a lost lepton (acceptance/ID) is fully covered"
frozen("ZH_EW_ZHjj_lostlep","ZHjj EW, Z->ll, 1 lepton lost",1.295,200000,["ZF","BGG"],"v1/ew_zhjj_zll (Tier-1, 100 jobs)",LL,"ptj>20,|etaj|<5,drjj>0.4")
frozen("ZH_QCD_ZHjj_lostlep","ZHjj QCD (2,2), Z->ll, 1 lepton lost",10.21,100000,["ZF","BGG"],"v1/qcd_zhjj_zll (Tier-1, 50 jobs)",LL,"ptj>20,|etaj|<5,drjj>0.4")
frozen("ZH_ggZH_lostlep","ggZH loop, Z->ee/mumu (PY8), 1 lepton lost",74.33,20000,["BR_ZLL","BGG"],"final/H_ggZH_py8dec",
    "Z decayed in PY8 (no cuts): covered","none")
frozen("ZH_ttH_dilep_lostlep","ttH dilepton, 1 lepton lost",18.11,40000+2000,["WF","WF","BGG"],"final/H_ttH + test_v2/H_ttH",
    "t->b l nu both in ME, cut_decays False: covered. NOTE: ZH ledger used k=B_gg (MG tree W BR); here WF^2 applied (physical W BR) - differs by 7.8% from ZH convention","none")
frozen("ZH_Zaajj_EW_lostlep","Zgg jj EW (on-shell Z->ll), 1 lepton lost",0.0393,60000,["ZF"],"final/B_EW_zaajj_vbs_is{1h,2,3}",
    LL+"; BUT gen cuts pta>25, 100<maa<170, mjj>400 bound the WH baseline (see report 02 sec. 3)","pta>25,etaa<2.5,100<maa<170,mjj>400")
frozen("ZH_Zaajj_QCD_lostlep","Zgg jj QCD (on-shell Z->ll), 1 lepton lost",0.0356,100000,["ZF"],"final/B_QCD_zaajj_vbs (+ twin B_QCD_zaajj_nomjj, ratio C)",
    LL+"; same generator-cut bounds","pta>25,etaa<2.5,100<maa<170,mjj>400")
frozen("ZH_Zajj_eFake","Z(ll)gamma jj with e->gamma (QCD+EW), lepton+photon pairs",80.51,5989548+500000,["one"],"final/F_QCD_llajj_vbs, F_EW_llajj_vbs",
    "l+l- in ME: ptl>10,|etal|<2.5,mmll>50 apply: lost-lepton (outside acceptance) NOT covered -> PARTIAL; e->gamma param. as ZH","ptl>10,mmll>50,mjj>400,pta>25")

# ---- generator-cut (mmjj>400) correction from the twins: lost fraction f of reco-selected (m_jj>500) events -> yield multiplier C = 1/(1-f)
CGEN = {  # id: (loss f, err, source)
 "B_QCD_Waajj_vbs": (0.476, 0.055, "W gamma gamma QCD twin B_QCD_Waajj_nomjj (82 selected events, loose selection)"),
 "F_QCD_Wajj_vbs": (0.370, 0.093, "W gamma QCD twin F_QCD_Wajj_nomjj (27 selected events, loose selection)"),
 "ZH_Zaajj_QCD_lostlep": (0.476, 0.055, "PROXY: W gamma gamma QCD twin (same QCD-type topology); ZH itself needed C=2.37 at the ZH selection; to be re-derived at the WH selection (Phase 05)"),
 "ZH_Zajj_eFake": (0.370, 0.093, "PROXY (QCD part only): W gamma QCD twin; EW part unquantified"),
}
for r in ROWS:
    c = CGEN.get(r["id"])
    if c: f, e, src = c; r["c_gen_cut"] = dict(factor=round(1/(1-f), 3), up=round(1/(1-f-e)-1/(1-f), 3), down=round(1/(1-f)-1/(1-f+e), 3), loss_fraction=f, loss_err=e, source=src)
    elif r["id"] in ("B_EW_Waajj_vbs", "F_EW_Wajj_vbs", "ZH_Zaajj_EW_lostlep"): r["c_gen_cut"] = dict(factor=None, note="EW-type: NO twin for W; ZH measured 1.4 % loss at its selection (placeholder only) -> D-WH-7")
# ---- N rule: flag EVERY shortfall; unflagged shortfall fails loudly (G1 item 1)
ACK = {"ZH_ggZH_lostlep": "D-WH-3", "ZH_ttH_dilep_lostlep": "D-WH-3", "F_Wjj_pilot": "D-WH-2", "F_Wajj_pilot": "D-WH-2", "T_tt_1l": "D-WH-2", "F_QCD_Wajj_nomjj": "D-WH-7"}
bad = []
for r in ROWS:
    need = r.get("N_required"); have = r.get("N_planned") if r.get("N_planned") is not None else r.get("N_available")
    short = (need is not None and have is not None and have < need) or r.get("infeasible_N") or (r.get("N_ok") is False) or (r["id"] in ("F_QCD_Wajj_nomjj",) and need and need > NMAX)
    r["N_shortfall_flag"] = ACK.get(r["id"]) if short else None
    if short and r["id"] not in ACK: bad.append(f"{r['id']}: N_planned/available={have} < N_required={need}")
if bad: raise SystemExit("N_MC shortfall WITHOUT decision flag:\n  " + "\n  ".join(bad))
yaml.safe_dump(dict(lumi_fb=500, N_policy="N >= max(50k, sigma*k*3000 fb^-1)", NMAX_feasible=NMAX, B_gg=B.BGG, WF=B.WF, WFTAU=B.WFTAU, WHAD=B.WHAD, samples=ROWS),
               open(f"{WH}/config/sample_matrix.yaml", "w"), sort_keys=False, width=200)
print(f"{'id':24s}{'sigma[fb]':>12s}{'k':>10s}{'N_req':>12s}  flags")
for r in ROWS:
    s = r.get("sigma_fb"); print(f"{r['id']:24s}{('%.4g'%s) if s is not None else 'pending':>12s}{r['k_external'] or 0:10.5f}{r['N_required'] if r['N_required'] is not None else 'pending':>12}  {'INFEASIBLE' if r.get('infeasible_N') else ''}{'' if r.get('N_ok', True) else ' N_AVAIL<REQ'}")
# ---- markdown table for the report
with open(f"{WH}/work/matrix_table.md", "w") as f:
    f.write("| ID | role | σ_MG [fb] (source) | k = ext. BR factors | σ·k [fb] | N_required | N planned / avail. | flag / generator-cut C |\n|---|---|---|---|---|---|---|---|\n")
    for r in ROWS:
        s = r.get("sigma_fb"); k = r["k_external"]; src = r["sigma_source"].split(" (")[0][:34]
        sk = "pending" if s is None else f"{s*k:.4g}"
        n = r.get("N_planned") or r.get("N_available") or ""
        fl = (r.get("N_shortfall_flag") or "") + (" (N>feasible)" if r.get("infeasible_N") else "")
        cg = r.get("c_gen_cut"); cc = "" if not cg else (("C=%.2f" % cg["factor"]) if cg.get("factor") else "C unquantified")
        fl = (fl + " " + cc).strip()
        f.write(f"| {r['id']} | {r['role'][:44]} | {'pending' if s is None else '%.4g'%s} ({src}) | {'×'.join(r['br_factors_external'])}={k:.5g} | {sk} | {r['N_required'] if r['N_required'] is not None else 'pending'} | {n} | {fl} |\n")
