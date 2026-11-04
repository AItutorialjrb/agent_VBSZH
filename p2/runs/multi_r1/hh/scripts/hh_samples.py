#!/usr/bin/env python3
"""Single source of truth for the HH sample registry (Phase 02/03): emits config/sample_matrix.yaml, config/seeds.yaml and cards/*.mg5 .
Seeds (SPEC 3.4): seed = 1e6*P + 1e4*R + J + 1000*idx, P=3 (HH), R=11 (multi_r1); J=0 gridpack, J=1 test job, J=2 LHE-closure job. Uniqueness asserted.
Usage: python3 -P hh_samples.py            (writes into ../config and ../cards)"""
import os, sys, yaml
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P, R = 3, 11
def seed_old(idx, J): return 1_000_000 * P + 10_000 * R + J + 1000 * idx      # pre-G1 formula (R=11): ONLY for samples produced before G1 (config/seeds_used_preG1.txt)
def seed_new(idx, J): return 3_000_000 + 100_000 * 1 + 1000 * idx + J          # SPEC 3.4 G1 revision, multi_r1 (R=1); J>=3 for new items (0..2 are the pre-G1 gridpack/test/closure slots)
def seed(idx, J, new=False): return seed_new(idx, J) if new else seed_old(idx, J)
# ---- BR inputs (single place; applied ONCE per sample via the ledger 'br' list; entries 'B_x@label' = the same BR for DISTINCT decaying particles (H1,H2 / Z1,Z2), applied once each; br_total stored at full precision) -------------------------------------------------
BR = dict(
  B_bb=(0.5824, "LHC Higgs WG YR4 SM prediction at mH=125.0 GeV (= model mass; not 125.09), B(H->bb)=5.824E-01; PDG has no SM BR, cross-check closed; BR uncertainty = Phase-06 nuisance"),
  B_Zqq=(0.6991, "PDG 2024 B(Z->hadrons)=0.6991 (Z forced to q qbar, q=d,u,s,c,b, in PY8; PDG used directly, no MG5 width involved)"),
  B_Wqq=(0.6741, "PDG 2024 B(W->hadrons)=0.6741 (W forced hadronic in PY8)"),
  one=(1.0, "no BR factor (inclusive PY8 decays, or no decay)"),
)
# ---- generic run-card block -------------------------------------------------------------------------------------------------------
def runcard(c, seed_):
    L = ["set run_card ebeam1 6800", "set run_card ebeam2 6800", "set run_card pdlabel lhapdf", "set run_card lhaid 303600",
         "set run_card maxjetflavor 5", "set run_card asrwgtflavor 5", "set run_card use_syst True", "set run_card gridpack True",
         "set run_card nevents %d" % c.get("nev_gp", 2000), "set run_card iseed %s" % seed_]
    for k, v in c["cuts"].items(): L.append(f"set run_card {k} {v}")
    for k, v in c.get("params", {}).items(): L.append(f"set {k} {v}")
    return L
EWC = dict(ptj=20, etaj=5, drjj=0.4, dynamical_scale_choice=3)
VBS = dict(deltaeta=3.0, xetamin=400)      # any-pair VBS filter (patch 003): exists jet pair, y1*y2<0, |dy|>3.0, mjj>400 GeV  [reco anchor: |dy|>3.5, mjj>500]
S = []   # sample dicts
def add(**k): S.append(k)
BASIS = [(1,1,1),(1.5,0,1),(1.5,0,0),(0.5,2,0),(1,0,2),(1,2,-1)]; CLOS = [(1,0,1),(1,2,1)]
def kn(t): return "_".join(f"{n}{str(v).replace('.','p').replace('-','m')}" for n, v in zip(("kV","k2V","kl"), t))
HHJJ = "generate p p > h h j j QCD=0 QED=4"
for i, t in enumerate(BASIS + CLOS):
    add(idx=1+i, name=f"S_HHjj_{kn(t)}", cls="signal", role="basis" if i < 6 else "closure", model="sm_kVk2VkL-no_b_mass", proc=HHJJ,
        cuts={**EWC, "deltaeta": 2.5, "xetamin": 200}, patch_cuts=True, params=dict(kV=t[0], k2V=t[1], kl=t[2]), py8="py8_hh_bb.cmnd", br=["B_bb@H1", "B_bb@H2"],
        coupling=t, desc="EW pp>HHjj (QCD==0, QED==4), H undecayed in LHE, both H->bb forced in PY8", test=(i == 0), gridpack=True)
add(idx=9, name="S_HHjj_SM_twin_loose", cls="signal", role="twin(gen-cut safety)", model="sm_kVk2VkL-no_b_mass", proc=HHJJ, cuts={**EWC}, patch_cuts=False,
    params=dict(kV=1, k2V=1, kl=1), py8="py8_hh_bb.cmnd", br=["B_bb@H1", "B_bb@H2"], coupling=(1,1,1), desc="twin of SM point WITHOUT VBS generator filter (parton-level cut-safety check only)", test=False, gridpack=True)
for j, kl in enumerate((1, 0, 2, 5)):
    add(idx=10+j, name=f"G_ggHH_loop_kl{kl}", cls="ggF_HH", role=("bkg(kl-dep.)" if kl != 5 else "closure(kl)"), model="loop_sm_kl-no_b_mass", proc="generate g g > h h [noborn=QCD]",
        cuts={**EWC, "dynamical_scale_choice": -1}, patch_cuts=False, params=dict(kl=kl), py8="py8_hh_bb.cmnd", br=["B_bb@H1", "B_bb@H2"],
        desc="LO loop-induced ggF HH (loop_sm, full top mass), kl by 3-point quadratic morphing", test=(j == 0), gridpack=True, phase03_loop=True)
BG = dict(dynamical_scale_choice=-1, ptj=20, etaj=5, drjj=0.4)
add(idx=20, name="Q_4j_vbs", cls="QCD_multijet", role="bkg", model="sm-no_b_mass", proc="generate p p > j j j j", cuts={**BG, **VBS, "ihtmin": 500},
    patch_cuts=True, py8="py8_qcd.cmnd", br=["one"], desc="QCD 4-parton (g,u,d,s,c,b) + PS; b/c content from g->bb/cc in PS and ME; fixed-order exclusive, NO merging with 5j (flagged)", test=True, gridpack=True)
add(idx=21, name="Q_bbjj_vbs", cls="QCD_multijet", role="bkg", model="sm-no_b_mass", proc="generate p p > b b~ j j", cuts={**BG, **VBS, "ihtmin": 500},
    patch_cuts=True, py8="py8_qcd.cmnd", br=["one"], desc="QCD b bbar + 2 jets (ME-level b content) + PS", test=True, gridpack=True)
add(idx=30, name="T_ttbar_boost", cls="ttbar", role="bkg", model="sm-no_b_mass", proc="generate p p > t t~", cuts={**BG, "ptheavy": 250, "dynamical_scale_choice": 3},
    patch_cuts=False, py8="py8_tt.cmnd", br=["one"], desc="tt-bar inclusive, PY8 inclusive decays (all-had + semilep + dilep in one sample), >=1 top pT>250 GeV filter", test=True, gridpack=True)
add(idx=40, name="H_VBFH_bb", cls="single_H", role="bkg", model="sm-no_b_mass", proc="generate p p > h j j QCD=0 QED=3", cuts={**EWC, "deltaeta": 2.5, "xetamin": 200}, patch_cuts=True,
    py8="py8_hh_bb.cmnd", br=["B_bb"], desc="VBF H, H->bb forced in PY8", test=True, gridpack=True)
add(idx=41, name="H_ZH_Zqq_bb", cls="single_H", role="bkg", model="sm-no_b_mass", proc="generate p p > z h", cuts={**BG, "ptheavy": 150, "dynamical_scale_choice": 3}, patch_cuts=False,
    py8="py8_vh.cmnd", br=["B_Zqq", "B_bb"], desc="ZH (QCD DY-like), Z->qq (incl. bb), H->bb forced in PY8; >=1 heavy boson pT>150", test=True, gridpack=True)
add(idx=44, name="H_ttH_bb", cls="single_H", role="bkg", model="sm-no_b_mass", proc="generate p p > t t~ h", cuts={**BG, "dynamical_scale_choice": 3, "ptheavy": 150}, patch_cuts=False,
    py8="py8_hh_bb.cmnd", br=["B_bb"], desc="ttH, H->bb forced, tops decay inclusively in PY8; >=1 heavy pT>150", test=True, gridpack=True)
add(idx=50, name="V_Zjj_QCD_vbs", cls="V+jets", role="bkg", model="sm-no_b_mass", proc="generate p p > z j j QED=1", cuts={**BG, **VBS}, patch_cuts=True,
    py8="py8_vh.cmnd", br=["B_Zqq"], desc="Z+2j QCD (Z undecayed in LHE, Z->qq forced in PY8) with VBS filter; W+2j analogous (idx 51 planned)", test=True, gridpack=True)
add(idx=53, name="V_ZZjj_EW", cls="VBS_VV", role="bkg", model="sm-no_b_mass", proc="generate p p > z z j j QCD=0", cuts={**EWC, "deltaeta": 2.5, "xetamin": 200}, patch_cuts=True,
    py8="py8_vh.cmnd", br=["B_Zqq@Z1", "B_Zqq@Z2"], desc="EW ZZjj (VBS), both Z->qq forced in PY8 (ZH Z->bb lives in H_ZH_Zqq_bb)", test=True, gridpack=True)

# ---- extra backgrounds (G1 review item 12): sigma-only gridpacks in Phase 03 (no test job), ledgered in 02 section 9b
add(idx=70, name="X_tW_boost", cls="extra_bkg", role="bkg(sigma only)", model="sm-no_b_mass", proc="generate p p > t w-\nadd process p p > t~ w+", cuts={**BG, "ptheavy": 250, "dynamical_scale_choice": 3}, patch_cuts=False,
    py8="py8_tt.cmnd", br=["one"], desc="single-top tW (5F LO), inclusive PY8 decays, >=1 heavy pT>250", test=False, gridpack=True)
add(idx=71, name="X_ttZ_boost", cls="extra_bkg", role="bkg(sigma only)", model="sm-no_b_mass", proc="generate p p > t t~ z", cuts={**BG, "ptheavy": 250, "dynamical_scale_choice": 3}, patch_cuts=False,
    py8="py8_tt.cmnd", br=["one"], desc="ttZ, inclusive PY8 decays (Z->bb included), >=1 heavy pT>250", test=False, gridpack=True)
add(idx=72, name="X_ttW_boost", cls="extra_bkg", role="bkg(sigma only)", model="sm-no_b_mass", proc="generate p p > t t~ w+\nadd process p p > t t~ w-", cuts={**BG, "ptheavy": 250, "dynamical_scale_choice": 3}, patch_cuts=False,
    py8="py8_tt.cmnd", br=["one"], desc="ttW+- , inclusive PY8 decays, >=1 heavy pT>250", test=False, gridpack=True)
add(idx=73, name="X_Zjj_EW_vbs", cls="extra_bkg", role="bkg(sigma only)", model="sm-no_b_mass", proc="generate p p > z j j QCD=0", cuts={**EWC, "deltaeta": 2.5, "xetamin": 200}, patch_cuts=True,
    py8="py8_vh.cmnd", br=["B_Zqq"], desc="EW (VBF) Zjj, Z->qq forced in PY8", test=False, gridpack=True)
add(idx=74, name="X_ZZ_QCD_boost", cls="extra_bkg", role="bkg(sigma only)", model="sm-no_b_mass", proc="generate p p > z z", cuts={**BG, "ptheavy": 250, "dynamical_scale_choice": 3}, patch_cuts=False,
    py8="py8_vh.cmnd", br=["B_Zqq@Z1", "B_Zqq@Z2"], desc="QCD ZZ (0 ME jets), both Z->qq forced; WZ analogous (not generated)", test=False, gridpack=True)

# ---- validation-only samples (diagram-class / interference evidence; never enter yields)
add(idx=60, name="V_HHjj_SM_noSchanV", cls="validation", role="validation(diagram class)", model="sm_kVk2VkL-no_b_mass", proc="generate p p > h h j j QCD=0 QED=4 $$ w+ w- z", cuts={**EWC, "deltaeta": 2.5, "xetamin": 200},
    patch_cuts=True, params=dict(kV=1, k2V=1, kl=1), py8="py8_hh_bb.cmnd", br=["B_bb@H1", "B_bb@H2"], coupling=(1,1,1), desc="SM EW HHjj WITHOUT any s-channel W/Z diagram (t-channel/VBF-like topologies only); same cuts as S_HHjj SM; parton-level validation", test=False, gridpack=True)
add(idx=61, name="V_ZHH_Zjj_SM", cls="validation", role="validation(diagram class)", model="sm_kVk2VkL-no_b_mass", proc="generate p p > z h h QCD=0, z > j j", cuts={**EWC}, patch_cuts=False,
    params=dict(kV=1, k2V=1, kl=1), py8="py8_hh_bb.cmnd", br=["B_bb@H1", "B_bb@H2"], coupling=(1,1,1), desc="Higgsstrahlung-like ZHH, Z->jj inside MG5 (sigma x MG5 BR(Z->jj)); inclusive, no VBS filter; parton-level validation", test=False, gridpack=True)
add(idx=62, name="V_WHH_Wjj_SM", cls="validation", role="validation(diagram class)", model="sm_kVk2VkL-no_b_mass", proc="generate p p > w+ h h QCD=0, w+ > j j", cuts={**EWC}, patch_cuts=False,
    params=dict(kV=1, k2V=1, kl=1), py8="py8_hh_bb.cmnd", br=["B_bb@H1", "B_bb@H2"], coupling=(1,1,1), desc="Higgsstrahlung-like W+HH, W->jj inside MG5; (W- by charge symmetry up to PDFs, not generated); parton-level validation", test=False, gridpack=True)


# ======================= PRE-G2 additions (seeds: SPEC 3.4 G1 revision; J>=3) =========================================================================
OLD = {s["idx"] for s in S}
def addn(**k): k["new"] = True; S.append(k)
VBSL = dict(deltaeta=2.0, xetamin=200)     # loose VBS twin filter (nominal 3.0/400)
# --- samples of handoff types not yet generated in Phase 03
addn(idx=42, name="H_WH_Wqq_bb", cls="single_H", role="bkg", model="sm-no_b_mass", proc="generate p p > w+ h\nadd process p p > w- h", cuts={**BG, "ptheavy": 150, "dynamical_scale_choice": 3}, patch_cuts=False,
     py8="py8_vh.cmnd", br=["B_Wqq", "B_bb"], desc="W+H and W-H (QCD, DY-like), W->qq' forced and H->bb forced in PY8; >=1 heavy boson pT>150 (same filter as ZH)", test=True, gridpack=True)
addn(idx=45, name="H_ggH_jj_heft", cls="single_H", role="bkg", model="heft", proc="generate p p > h j j HIG=1 QCD=2", cuts={**BG, **VBS}, patch_cuts=True,
     py8="py8_hh_bb.cmnd", br=["B_bb"], desc="ggH + 2 jets in the HEFT (mt->inf), LO ME (26 diagrams gg>hgg), VBS any-pair filter 3.0/400, H->bb forced in PY8; no K-factor (flagged)", test=True, gridpack=True)
addn(idx=51, name="V_Wjj_QCD_vbs", cls="V+jets", role="bkg", model="sm-no_b_mass", proc="generate p p > w+ j j QED=1\nadd process p p > w- j j QED=1", cuts={**BG, **VBS}, patch_cuts=True,
     py8="py8_vh.cmnd", br=["B_Wqq"], desc="W+2j and W-2j QCD (W undecayed in LHE, W->qq' forced in PY8), VBS any-pair filter", test=True, gridpack=True)
addn(idx=22, name="Q_4b_ht", cls="QCD_multijet", role="bkg", model="sm-no_b_mass", proc="generate p p > b b~ b b~", cuts={**BG, "ihtmin": 500}, patch_cuts=False,
     py8="py8_qcd.cmnd", br=["one"], desc="QCD bbbb, HT>500 filter, no VBS filter (VBS jets from PS); b-enriched bound/shape sample for the bb_nonH/Hbb-like classes", test=True, gridpack=True)
MLM = dict(use_syst="False", ickkw=1, drjj=0, etaj=-1, ptj=20, dynamical_scale_choice=-1, ptheavy=250)
TTP = "generate p p > t t~ @0\nadd process p p > t t~ j @1\nadd process p p > t t~ j j @2"
for idx, xq, nm in ((31, 30, "T_ttbar_mlm"), (32, 20, "T_ttbar_mlm_xq20"), (33, 45, "T_ttbar_mlm_xq45")):
    addn(idx=idx, name=nm, cls="ttbar", role="bkg" if idx == 31 else "validation(MLM scale variation)", model="sm-no_b_mass", proc=TTP, cuts={**BG, **MLM, "xqcut": xq}, patch_cuts=False,
         py8=f"py8_tt_mlm_xq{xq}.cmnd", br=["one"], desc=f"tt+0,1,2j MLM (ickkw=1, xqcut={xq}, kT-MLM qCut in PY8 cmnd), >=1 top pT>250, inclusive PY8 top decays" + ("" if idx == 31 else "; matching-scale variation only"), test=(idx == 31), gridpack=True)
# --- extra backgrounds still lacking a bound (D-HH-11): gg->ZH (loop), EW Wjj, QCD WZ : sigma + 20k-event pilot; bounds computed from the pilot
addn(idx=75, name="X_ggZH_loop", cls="extra_bkg", role="bkg(bound)", model="loop_sm", proc="generate g g > z h [noborn=QCD]", cuts={**BG, "ptheavy": 150, "dynamical_scale_choice": 3}, patch_cuts=False,
     py8="py8_vh.cmnd", br=["B_Zqq", "B_bb"], desc="gg->ZH loop-induced (LO, loop_sm, full top+b loop), Z->qq and H->bb forced in PY8, ptheavy>150 (same filter as qq->ZH)", test=False, gridpack=True)
addn(idx=76, name="X_Wjj_EW_vbs", cls="extra_bkg", role="bkg(bound)", model="sm-no_b_mass", proc="generate p p > w+ j j QCD=0\nadd process p p > w- j j QCD=0", cuts={**EWC, "deltaeta": 2.5, "xetamin": 200}, patch_cuts=True,
     py8="py8_vh.cmnd", br=["B_Wqq"], desc="EW (VBF) W+-jj, W->qq' forced in PY8, VBS any-pair filter 2.5/200", test=False, gridpack=True)
addn(idx=77, name="X_WZ_QCD_boost", cls="extra_bkg", role="bkg(bound)", model="sm-no_b_mass", proc="generate p p > w+ z\nadd process p p > w- z", cuts={**BG, "ptheavy": 250, "dynamical_scale_choice": 3}, patch_cuts=False,
     py8="py8_vh.cmnd", br=["B_Wqq", "B_Zqq"], desc="QCD W+-Z, W->qq' and Z->qq forced, >=1 heavy boson pT>250", test=False, gridpack=True)
# --- more closure point: kV != 1 AND kl != 1 (review item 3)
addn(idx=14, name="S_HHjj_kV1p25_k2V1p5_kl2", cls="signal", role="closure", model="sm_kVk2VkL-no_b_mass", proc=HHJJ, cuts={**EWC, "deltaeta": 2.5, "xetamin": 200}, patch_cuts=True,
     params=dict(kV=1.25, k2V=1.5, kl=2), py8="py8_hh_bb.cmnd", br=["B_bb@H1", "B_bb@H2"], coupling=(1.25, 1.5, 2), desc="closure point with kV!=1 and kl!=1 (probes kV^3 kl, kV^2 kl^2, kV k2V kl monomials)", test=False, gridpack=True)
addn(idx=15, name="S_HHjj_kV1_k2V0_kl1_twin", cls="signal", role="twin(gen-cut safety)", model="sm_kVk2VkL-no_b_mass", proc=HHJJ, cuts={**EWC}, patch_cuts=False,
     params=dict(kV=1, k2V=0, kl=1), py8="py8_hh_bb.cmnd", br=["B_bb@H1", "B_bb@H2"], coupling=(1, 0, 1), desc="twin of the kappa_2V=0 point WITHOUT VBS generator filter (hard-tail enhanced; Delphes-level boosted-tail twin)", test=False, gridpack=True)
# --- background twins: looser generator filter than the nominal sample (SPEC 4.3(1)); compared to the nominal sample at Delphes level in the boosted tail
def twin(base_idx, newidx, name=None, **over):
    b = next(s for s in S if s["idx"] == base_idx)
    s = dict(b); s.update(idx=newidx, name=name or (b["name"] + "_twin"), role="twin(gen-cut safety)", new=True, test=False, gridpack=True, twin_of=b["name"])
    s["cuts"] = {**b["cuts"], **over.get("cuts", {})}; s["desc"] = "TWIN of " + b["name"] + " with looser generator filter " + str(over.get("cuts")) + "; Delphes-level boosted-tail comparison only"
    if "patch_cuts" in over: s["patch_cuts"] = over["patch_cuts"]
    S.append(s)
twin(20, 80, cuts={**VBSL, "ihtmin": 350})
twin(21, 81, cuts={**VBSL, "ihtmin": 350})
twin(30, 82, cuts={"ptheavy": 150})
twin(40, 83, cuts={"deltaeta": 1.5, "xetamin": 100})
twin(41, 84, cuts={"ptheavy": 100})
twin(44, 85, cuts={"ptheavy": 100})
twin(50, 86, cuts=VBSL)
twin(53, 87, cuts={"deltaeta": 1.5, "xetamin": 100})
twin(45, 88, cuts=VBSL)
twin(42, 89, cuts={"ptheavy": 100})
twin(51, 90, cuts=VBSL)
twin(31, 91, cuts={"ptheavy": 150})
# --- G2-FIX: further-loosened QCD twins (D-HH-14a option 1): measure the residual loss of the production (twin1) filter.  PREPARED ONLY, never submitted without the human's choice.
twin(80, 92, name="Q_4j_vbs_twin2", cuts={"deltaeta": 1.5, "xetamin": 100, "ihtmin": 250})
twin(81, 93, name="Q_bbjj_vbs_twin2", cuts={"deltaeta": 1.5, "xetamin": 100, "ihtmin": 250})
for s_ in S:
    if s_["name"].endswith("_twin2"): s_["twin_of"] = s_["name"].replace("_twin2", "_twin"); s_["desc"] = "TWIN2 of the production QCD filter (" + s_["twin_of"] + "): ihtmin 250, VBS 1.5/100; measures the residual generator-filter loss of the production sample (D-HH-14a option 1)"
# --- G2-FIX: t-channel single top (review item 12): sigma-ratio bound; sigma-only gridpack card prepared
addn(idx=78, name="X_tchan_boost", cls="extra_bkg", role="bkg(bound)", model="sm-no_b_mass", proc="generate p p > t j $$ w+ w-\nadd process p p > t~ j $$ w+ w-", cuts={**BG, "ptheavy": 250, "dynamical_scale_choice": 3}, patch_cuts=False,
     py8="py8_tt.cmnd", br=["one"], desc="t-channel single top (5F, forward light jet + boosted top), inclusive PY8 decays, >=1 heavy pT>250; sigma-only bound sample", test=False, gridpack=True)
for s in S:
    s.setdefault("new", False)
    s["gseed"], s["tseed"], s["cseed"] = (seed_new(s["idx"], 3), seed_new(s["idx"], 4), seed_new(s["idx"], 5)) if s["new"] else (seed_old(s["idx"], 0), seed_old(s["idx"], 1), seed_old(s["idx"], 2))

def check_seeds():
    seen = {}
    for v, k in OLD_PRE.items(): seen[v] = (k[0] + "(pre-G1)", k[1])
    for s in S:
        Js = (0, 1, 2) if not s["new"] else (3, 4, 5)
        for J in Js:
            v = seed(s["idx"], J, s["new"])
            if not s["new"]:
                assert v in OLD_PRE and OLD_PRE[v][0] == s["name"], f"old-formula seed {v} of {s['name']} not in seeds_used_preG1.txt"; continue
            assert v not in seen, f"seed collision {v}: {s['name']} J={J} vs {seen[v]}"; seen[v] = (s["name"], J)
    assert len({s["idx"] for s in S}) == len(S) and len({s["name"] for s in S}) == len(S), "duplicate idx/name"
    return seen
def seed_job(s, k):
    """production job seed (k = 0,1,2,...): J = 10 + k, J < 1000 -> at most 990 jobs per sample; never collides with J in 0..5 slots; asserted against all other seeds by uniqueness test"""
    assert 0 <= k < 990
    return seed_new(s["idx"], 10 + k)
def card(s):
    L = ["# hh card, UNVALIDATED until reports/03 says otherwise. OUTDIR substituted by scripts/condor/make_gridpack_hh.sh",
         "set automatic_html_opening False", "set auto_update 0", "set nb_core 4", "set run_mode 2", "set lhapdf_py3 lhapdf-config",
         f"import model {s['model']}"]
    if s["model"].startswith("sm"):
        L += ["define p = g u c d s b u~ c~ d~ s~ b~", "define j = g u c d s b u~ c~ d~ s~ b~"]
    L += s["proc"].split("\n") + ["output OUTDIR -nojpeg", "launch OUTDIR", "0"]
    L += runcard(s, s["gseed"])
    L += ["done"]
    return "\n".join(L) + "\n"
if __name__ == "__main__":
    import json
    pre = f"{H}/config/seeds_used_preG1.txt"
    if not os.path.exists(pre):
        raise SystemExit("config/seeds_used_preG1.txt missing (it is written once from the pre-G1 registry and kept unchanged)")
    OLD_PRE = {}
    for ln in open(pre):
        if ln.startswith("#") or not ln.strip(): continue
        v, n, J = ln.split(); OLD_PRE[int(v)] = (n, int(J))
    seen = check_seeds()
    os.makedirs(f"{H}/cards", exist_ok=True); os.makedirs(f"{H}/config", exist_ok=True)
    for s in S:
        if s["gridpack"] and s["new"]: open(f"{H}/cards/{s['name']}.mg5", "w").write(card(s))
    m = dict(meta=dict(process="HH(boosted VBF HH->4b)", run="multi_r1", seed_scheme="OLD samples (pre-G1): 1e6*3+1e4*11+J+1000*idx (J=0,1,2; config/seeds_used_preG1.txt). NEW: seed = 3e6 + 1e5*1 + 1000*idx + J, J=3 gridpack,4 test,5 twin/closure, 10+k production job k",
                       n_mc_rule="signal and D-HH-12 samples: N>=max(50k, sigma*BR*3000/fb); other backgrounds: effective-N policy (SPEC 4.3)"),
             br_inputs={k: dict(value=v[0], source=v[1]) for k, v in BR.items()},
             samples=[dict(idx=s["idx"], name=s["name"], cls=s["cls"], role=s["role"], model=s["model"], process=s["proc"], generator_cuts=s["cuts"],
                           vbs_anypair_patch=s["patch_cuts"], pythia_cmnd=s["py8"], br_ledger=s["br"], br_total=__import__("math").prod(BR[b.split("@")[0]][0] for b in s["br"]),
                           seed_gridpack=s["gseed"], seed_test=s["tseed"], seed_lhe_closure=s["cseed"], seeds_new_formula=s["new"],
                           phase03_gridpack=s["gridpack"], phase03_test_job=s["test"], description=s["desc"], twin_of=s.get("twin_of"), **({"coupling_kV_k2V_kl": list(s["coupling"])} if "coupling" in s else {}))
                      for s in S])
    yaml.safe_dump(m, open(f"{H}/config/sample_matrix_gen.yaml", "w"), sort_keys=False, width=200)
    yaml.safe_dump({v: dict(sample=k[0], J=k[1]) for v, k in seen.items()}, open(f"{H}/config/seeds.yaml", "w"))
    print(len(S), "samples;", sum(s["gridpack"] for s in S), "gridpacks;", sum(s["test"] for s in S), "test jobs; seeds unique (incl. pre-G1 list):", len(seen))
