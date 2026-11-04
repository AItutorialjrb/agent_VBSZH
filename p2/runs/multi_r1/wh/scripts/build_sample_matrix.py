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
def row(id, role, process, orders, cuts, sig, src, fac, wdec, hdec, overlap, N_plan=None, test=None, status="candidate", note="", in_bs=True, weighted=False):
    k = B.register(id, wdec, hdec, fac) if fac else None
    g = gp(id)
    if g is not None and id != "H_QCD_WH_mlm":      # gridpack init sigma (higher precision) preferred; MLM keeps the matched PY8 sigma
        src = "gridpack init sigma" + (f" (smoke run gave {sig[0]:.5g} +- {sig[1]:.2g} fb)" if sig else "") ; sig = g
    elif sig is not None and not src.startswith("condor"): src = "SMOKE RUN (no gridpack sigma yet): " + src
    if sig is None: sigv, err = None, None
    else: sigv, err = sig
    need = None if sigv is None else max(50000.0, abs(sigv)*k*L)
    inf = need is not None and need > NMAX
    if N_plan == "req": N_plan = None if need is None else int(-(-need // 1000)*1000)      # plan exactly the required N (rounded up to 1000)
    ROWS.append(dict(id=id, idx=reg.get(id), role=role, process=process, orders=orders, gen_cuts=cuts, sigma_fb=sigv, sigma_err_fb=err, sigma_source=src,
        br_factors_external=fac, k_external=k, br_in_ME=wdec, h_decay=hdec, N_required=None if need is None else round(need), N_planned=N_plan,
        infeasible_N=bool(inf), overlap_rule=overlap, condor_test=test, status=status, note=note, in_bs=in_bs, weighted=weighted))
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
    "its 2-jet ME is QCD (2,2); EW (0,4) excluded by order; do NOT add H_QCD_WHjj_fixed",200000,"MLM",note="N_planned = ACCEPTED events (LHE generated = N_planned/0.346 from the test job); DJR validation required in Phase 04 (as ZH)")
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
    smoke("T_tta_1l_smoke"),"smoke T_tta_1l_smoke",["WF","WHAD"],"t->b W->l nu / q q' in MG5 ME","no H","overlap with T_ttaa_1l: events with 2 prompt photons are dropped from T_tta_1l at analysis (as ZH closeout); residual double counting bounded at reco (after b-veto) in report 04 sec. 6, NOT called negligible","req","top")
row("T_ttaa_1l","irreducible prompt","p p > t t~ a a, single-lepton",[2,2],"pta>15,|etaa|<2.5, 90<maa<190",
    smoke("T_ttaa_1l_smoke"),"smoke T_ttaa_1l_smoke",["WF","WHAD"],"t->b W in MG5 ME","no H","full sample kept (>=2 prompt photons); T_tta_1l events with >=2 prompt photons removed","req")
row("T_tWa_1l","1 fake gamma","p p > t w- a $$ t~ + c.c., single-lepton (4 combos), DR",[2,1],"pta>15,|etaa|<2.5",
    smoke("T_tWa_1l_smoke"),"smoke T_tWa_1l_smoke",["WF","WHAD"],"t->b W; W->l nu/qq' in MG5 ME","no H","events with >=2 prompt photons removed (as T_tta_1l); DR vs DS as systematic","req")
row("T_tt_1l","2 fake gammas (bound)","p p > t t~, single-lepton",[2,0],"none",
    smoke("T_tt_1l_smoke"),"smoke T_tt_1l_smoke",["WF","WHAD"],"t->b W in MG5 ME","no H","N_prompt_gamma==0; inclusive tt (jets from PS): CHECK sample only, superseded by T_ttjj_1l in b","req",in_bs=False,note="check only; N_required infeasible (D-WH-2) is why T_ttjj_1l with fake-factor weights replaces it")
# ---- continuum / fake samples. G1 decision D8: NO generator mmjj cut on the nominal samples (twin: mmjj>400 loses 37-48 % of reco-SR QCD events). mmjj>400 samples are kept as CROSS-CHECKS of the twin ratio only.
GCUT = "pta>25,|etaa|<2.5,100<maa<170,ptj>20,|etaj|<5,dR>0.4,cut_decays=False"
row("B_EW_Waajj_nomjj","irreducible continuum (EW), NOMINAL (no generator mjj cut)","p p > w+ a a j j QCD=0 QED=5, w+>l+ vl (+c.c.), on-shell W chain",[0,5],GCUT+", mmjj 0",
    gp("B_EW_Waajj_nomjj") or None,"gridpack init sigma (pending: 884934.13)",["WF"],"W->l nu in MG5 ME","no H","order-exclusive vs QCD; EW-QCD interference I_Waajj: bound/aux, see 04 caveats","req","continuum",
    note="same diagrams as B_EW_Waajj_vbs (20520 diagrams / 44 subprocesses); no mmjj => removes the need for the (unquantified) EW C")
row("B_EW_Waajj_vbs","EW twin cross-check (mmjj>400)","p p > w+ a a j j QCD=0 QED=5, w+>l+ vl (+c.c.)",[0,5],GCUT+", mmjj 400",
    gp("B_EW_Waajj_vbs") or None,"gridpack init sigma if available (884456.3 still running)",["WF"],"W->l nu in MG5 ME","no H","cross-check of the EW twin ratio only; never added to b","req","continuum",in_bs=False,
    note="20520 diagrams / 44 subprocesses (generate+output 155 s); D-WH-6: waiting for 884456.3")
row("B_QCD_Waajj_nomjj","irreducible continuum (QCD), NOMINAL (no generator mjj cut)","p p > w+ a a j j QCD=2 QED=3 ,w+>l+ vl (+c.c.)",[2,3],GCUT+", mmjj 0",
    gp("B_QCD_Waajj_nomjj") or None,"gridpack init sigma",["WF"],"W->l nu in MG5 ME","no H","fixed order; nominal by D8","req","continuum",note="6984 diagrams / 52 subprocesses")
row("B_QCD_Waajj_vbs","QCD twin cross-check (mmjj>400)","as B_QCD_Waajj_nomjj + mmjj 400",[2,3],GCUT+", mmjj 400",
    gp("B_QCD_Waajj_vbs") or None,"gridpack init sigma",["WF"],"W->l nu in MG5 ME","no H","cross-check of the twin ratio only; never added to b",100000,"continuum",in_bs=False)
row("F_EW_Wajj_nomjj","1 fake gamma (EW), NOMINAL (no generator mjj cut)","p p > w+ a j j QCD=0 QED=4, w+>l+ vl (+c.c.)",[0,4],"pta>25,ptj>20,..., mmjj 0",
    gp("F_EW_Wajj_nomjj") or None,"gridpack init sigma (pending: 884934.9)",["WF"],"W->l nu in MG5 ME","no H","drop events with >=2 prompt photons (-> B_*)","req","1 fake gamma",note="2700 diagrams")
row("F_EW_Wajj_vbs","EW twin cross-check (mmjj>400)","as F_EW_Wajj_nomjj + mmjj 400",[0,4],"pta>25,mmjj 400,...",
    gp("F_EW_Wajj_vbs") or None,"gridpack init sigma",["WF"],"W->l nu in MG5 ME","no H","cross-check only","req","1 fake gamma",in_bs=False)
row("F_QCD_Wajj_nomjj","1 fake gamma (QCD), NOMINAL (no generator mjj cut)","p p > w+ a j j QCD=2 QED=2, w+>l+ vl (+c.c.)",[2,2],"pta>25,ptj>20,..., mmjj 0",
    gp("F_QCD_Wajj_nomjj") or None,"gridpack init sigma",["WF"],"W->l nu in MG5 ME","no H","drop events with >=2 prompt photons","req","1 fake gamma",note="1024 diagrams; N_required 1.64e7 events (~520 core-h, ~40 GB)")
row("F_QCD_Wajj_vbs","QCD twin cross-check (mmjj>400)","as F_QCD_Wajj_nomjj + mmjj 400",[2,2],"pta>25,mmjj 400,...",
    gp("F_QCD_Wajj_vbs") or None,"gridpack init sigma",["WF"],"W->l nu in MG5 ME","no H","cross-check only",100000,"1 fake gamma",in_bs=False)
row("F_Wjjjj","2 fake gammas (weighted; replaces the W+2j pilot)","p p > w+ j j j j QCD=4 QED=1, w+>l+ vl (+c.c.), light-flavour j",[4,1],"ptj>20,|etaj|<5,dR>0.4, no bias cut (no safe bias cut established)",
    gp("F_Wjjjj") or None,"gridpack init sigma (pending: 884934.14)",["WF"],"W->l nu in MG5 ME","no H","N_prompt_gamma==0; photons from jets by Delphes-j->gamma-rate probability weights (D-WH-2)",None,"fake weighted",weighted=True,
    note="N_planned set by N_eff>=10 in the SR (from test job) in report 04, not by sigma*L")
row("T_ttjj_1l","tt 1l, 2 fake gammas (weighted)","p p > t t~ j j, single-lepton (2 assignments), light j",[4,0],"ptj>20,|etaj|<5,dR>0.4, no bias cut",
    gp("T_ttjj_1l") or None,"gridpack init sigma (pending: 884934.15)",["WF","WHAD"],"t->b W in MG5 ME","no H","N_prompt_gamma==0; weights as F_Wjjjj; b-veto kept in the selection",None,"fake weighted",weighted=True,
    note="gluon-splitting/ISR double counting with PS jets of T_tt_1l is irrelevant: T_tt_1l is not in b")
row("F_Wjj_pilot","pilot (exploratory bound), superseded by F_Wjjjj","p p > w+ j j , w+>l+ vl (+c.c.), fixed 2 partons",[2,1],"ptj>20,|etaj|<5,dR>0.4",
    smoke("F_Wjj_pilot_smoke"),"smoke F_Wjj_pilot_smoke",["WF"],"W->l nu in MG5 ME","no H","pilot only; never in b",None,"fake pilot",in_bs=False,note="superseded: VBS jets had to come from the PS")
row("F_Wajj_pilot","pilot (exploratory), covered by F_*_Wajj_nomjj","p p > w+ a j j, w+>l+ vl (+c.c.)",[2,2],"ptj>20,pta>15",
    smoke("F_Wajj_pilot_smoke"),"smoke F_Wajj_pilot_smoke",["WF"],"W->l nu in MG5 ME","no H","pilot only; never in b",None,"fake pilot",in_bs=False,note="same process as F_QCD_Wajj (QCD part)")
# ---- WZ/WW/ZZ gamma with lost lepton / e->gamma (D-WH-5): final state defined directly (e/mu in ME), no resonant BR (k=1)
VL = "ptl>5,|etal|<3.5,mmll>10,dRll>0.1,pta>15,|etaa|<2.5; NO ME jets (jets from PS only)"
row("V_WZa_WH","WZ gamma -> l l l nu gamma, lost lepton / e->gamma","p p > l+ l- l+ vl a (+ l- vl~), group_subprocesses False",[0,5],VL,gp("V_WZa_WH") or None,"gridpack init sigma (pending: 884934.10)",["one"],"leptons in ME (e,mu final state; k=1, fiducial sigma)","no H","V gamma: ME jets absent => VBS SR yield from PS jets only (lower bound-like, see 04)","req","V gamma",note="D-WH-5")
row("V_WWa_WH","WW gamma / ZZ(llnunu) gamma -> l nu l nu gamma","p p > l+ vl l- vl~ a, group_subprocesses False",[0,5],VL,gp("V_WWa_WH") or None,"gridpack init sigma (pending: 884934.11)",["one"],"leptons in ME (k=1)","no H","as V_WZa_WH","req","V gamma",note="D-WH-5")
row("V_ZZa_WH","ZZ gamma -> 4l gamma, 3 leptons lost","p p > l+ l- l+ l- a, group_subprocesses False",[0,5],VL,gp("V_ZZa_WH") or None,"gridpack init sigma (pending: 884934.12)",["one"],"leptons in ME (k=1)","no H","as V_WZa_WH","req","V gamma",note="D-WH-5")
# ---- D-WH-3 top-ups (NEW samples, reuse ZH gridpacks read-only with new seeds); the frozen ZH samples of the same process are SUPERSEDED (not mixed)
row("H_ggZH_wh","ggZH loop, Z->ee/mumu (PY8), 1 lepton lost (D-WH-3 top-up)","gg > Z H [noborn=QCD] (ZH gridpack H_ggZH_py8dec_s1363200, read-only), Z->ee/mumu and H->gg forced in PY8",["loop"],"none (PY8 decay, no cuts)",
    (74.33,0.7),"ZH FINAL_report table (same gridpack)",["BR_ZLL","BGG"],"Z undecayed in LHE; forced to e/mu in PY8","H->gg forced in PY8","Z lepton lost covered; independent seeds from the frozen sample","req","resonant bkg")
row("H_ttH_dilep_wh","ttH dilepton, 1 lepton lost (D-WH-3 top-up)","p p > t t~ h, both t->b l nu ... (ZH gridpack H_ttH_s1360500, read-only)",[2,1],"no jet cuts, scale 3",
    (18.11,0.2),"ZH FINAL_report table (same gridpack)",["WF","WF","BGG"],"t->b W->l nu in MG5 ME (ZH H_ttH gridpack: dilepton)",HD,"ttH 1l is H_ttH_1l; this is the dilepton topology","req","resonant bkg")
row("H_ZH_tautau_wh","ZH, Z->tautau (MLM 0-2j), tau->l feed-down (D-WH-3 top-up)","p p > z h (+j,+jj), z>ta+ ta- (ZH gridpack H_ZH_tautau_s1360700, read-only), MLM",[2,2],"xqcut as ZH",
    (24.97,0.3),"ZH FINAL_report table (sigma after matching)",["BGG"],"Z->tautau in MG5 ME","H->gg forced in PY8","tau->e/mu nu nu feed-down; MLM accepted events counted","req","resonant bkg")
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
import json
def _ratio(fn):
    f = f"{WH}/work/{fn}"
    if not os.path.exists(f): return None
    j = json.load(open(f)); return None if "C" not in j else j
CGEN = {}   # frozen ZH QCD-type samples with mmjj>400: C = nomjj/vbs yield ratio at the WH reco-SR proxy (scripts/ratio_C.py) on the FROZEN ZH twin pairs
for sid, fn, what in (("ZH_Zaajj_QCD_lostlep", "ratioC_ZH_Zaajj_QCD.json", "frozen ZH twin pair B_QCD_zaajj_nomjj/_vbs (100k+100k ev) at the WH SR proxy, ng=2"),
                      ("ZH_Zajj_eFake", "ratioC_ZH_Zajj_QCD.json", "frozen ZH twin pair F_QCD_llajj_nomjj/_vbs (first 200k ev each), ng=1; QCD part only, EW part uses the W EW twin proxy")):
    j = _ratio(fn)
    if j: CGEN[sid] = dict(factor=round(j["C"], 3), rel_err_stat=round(j["C_rel_err"], 3), syst_full_difference=round(j["C"]-1, 3), source=what)
    else: CGEN[sid] = dict(factor=None, source=what + " -- RESULT PENDING")
for r in ROWS:
    c = CGEN.get(r["id"])
    if c: r["c_gen_cut"] = c
    elif r["id"] in ("ZH_Zaajj_EW_lostlep",): r["c_gen_cut"] = dict(factor=None, source="EW part: ZH measured 1.4 % loss at the ZH selection; W EW twin (B_EW_Waajj_nomjj vs _vbs) pending as proxy; syst = full difference")
# ---- N rule: flag EVERY shortfall; unflagged shortfall fails loudly (G1 item 1)
ACK = {"F_Wjjjj": "D-WH-2 (N_eff rule, N set in report 04)", "T_ttjj_1l": "D-WH-2 (N_eff rule, N set in report 04)"}
bad = []
for r in ROWS:
    if r["id"].startswith("ZH_ggZH") or r["id"].startswith("ZH_ttH"): r["in_bs"] = False; r["role"] += " -- SUPERSEDED by the D-WH-3 top-up sample (not mixed)"
    if r.get("in_bs") is False:
        r["N_shortfall_flag"] = "NOT IN s/b (cross-check/pilot/superseded): N rule n/a; test job only, no production"
        if "path" not in r: r["N_planned"] = None
        else: r["N_shortfall_flag"] = "SUPERSEDED frozen ZH sample (D-WH-3 top-up used instead): not in b"
        continue
    need = r.get("N_required"); have = r.get("N_planned") if r.get("N_planned") is not None else r.get("N_available")
    short = (need is not None and have is not None and have < need) or r.get("infeasible_N") or (r.get("N_ok") is False) or (need is not None and need > NMAX) or (need is None and r["id"] in ACK) or (need is not None and have is None and not r.get("weighted"))
    r["N_shortfall_flag"] = ACK.get(r["id"]) if short else None
    if short and r["id"] not in ACK: bad.append(f"{r['id']}: N_planned/available={have} < N_required={need}")
for r in ROWS:   # any row below the N rule must carry a flag (in or out of s/b); fail loudly otherwise
    need, have = r.get("N_required"), r.get("N_planned") if r.get("N_planned") is not None else r.get("N_available")
    if need is not None and have is not None and have < need and not r.get("N_shortfall_flag"): bad.append(f"{r['id']}: shortfall without flag")
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
        cg = r.get("c_gen_cut"); cc = "" if not cg else (("C=%.2f" % cg["factor"]) if cg.get("factor") else "C pending")
        fl = (fl + " " + cc).strip()
        f.write(f"| {r['id']} | {r['role'][:44]} | {'pending' if s is None else '%.4g'%s} ({src}) | {'×'.join(r['br_factors_external'])}={k:.5g} | {sk} | {r['N_required'] if r['N_required'] is not None else 'pending'} | {n} | {fl} |\n")
