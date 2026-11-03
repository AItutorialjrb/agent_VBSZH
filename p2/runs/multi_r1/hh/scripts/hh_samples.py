#!/usr/bin/env python3
"""Single source of truth for the HH sample registry (Phase 02/03): emits config/sample_matrix.yaml, config/seeds.yaml and cards/*.mg5 .
Seeds (SPEC 3.4): seed = 1e6*P + 1e4*R + J + 1000*idx, P=3 (HH), R=11 (multi_r1); J=0 gridpack, J=1 test job, J=2 LHE-closure job. Uniqueness asserted.
Usage: python3 -P hh_samples.py            (writes into ../config and ../cards)"""
import os, sys, yaml
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P, R = 3, 11
def seed(idx, J): return 1_000_000 * P + 10_000 * R + J + 1000 * idx
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
add(idx=22, name="Q_4b_ht", cls="QCD_multijet", role="bkg(planned)", model="sm-no_b_mass", proc="generate p p > b b~ b b~", cuts={**BG, "ihtmin": 500},
    patch_cuts=False, py8="py8_qcd.cmnd", br=["one"], desc="QCD bbbb, HT-filtered, no VBS filter (VBS jets would come from PS only) -> bound/shape sample; planned", test=False, gridpack=False)
add(idx=30, name="T_ttbar_boost", cls="ttbar", role="bkg", model="sm-no_b_mass", proc="generate p p > t t~", cuts={**BG, "ptheavy": 250, "dynamical_scale_choice": 3},
    patch_cuts=False, py8="py8_tt.cmnd", br=["one"], desc="tt-bar inclusive, PY8 inclusive decays (all-had + semilep + dilep in one sample), >=1 top pT>250 GeV filter", test=True, gridpack=True)
add(idx=31, name="T_ttbar_boost_vbs", cls="ttbar", role="bkg(planned)", model="sm-no_b_mass", proc="generate p p > t t~ j j", cuts={**BG, **VBS, "ptheavy": 250},
    patch_cuts=True, py8="py8_tt.cmnd", br=["one"], desc="tt-bar + 2 jets with VBS filter (VBS-jet topology from ME); planned", test=False, gridpack=False)
add(idx=40, name="H_VBFH_bb", cls="single_H", role="bkg", model="sm-no_b_mass", proc="generate p p > h j j QCD=0 QED=3", cuts={**EWC, "deltaeta": 2.5, "xetamin": 200}, patch_cuts=True,
    py8="py8_hh_bb.cmnd", br=["B_bb"], desc="VBF H, H->bb forced in PY8", test=True, gridpack=True)
add(idx=41, name="H_ZH_Zqq_bb", cls="single_H", role="bkg", model="sm-no_b_mass", proc="generate p p > z h", cuts={**BG, "ptheavy": 150, "dynamical_scale_choice": 3}, patch_cuts=False,
    py8="py8_vh.cmnd", br=["B_Zqq", "B_bb"], desc="ZH (QCD DY-like), Z->qq (incl. bb), H->bb forced in PY8; >=1 heavy boson pT>150", test=True, gridpack=True)
add(idx=42, name="H_WpH_Wqq_bb", cls="single_H", role="bkg(planned)", model="sm-no_b_mass", proc="generate p p > w+ h", cuts={**BG, "ptheavy": 150, "dynamical_scale_choice": 3}, patch_cuts=False,
    py8="py8_vh.cmnd", br=["B_Wqq", "B_bb"], desc="W+H, W->qq', H->bb", test=False, gridpack=False)
add(idx=43, name="H_WmH_Wqq_bb", cls="single_H", role="bkg(planned)", model="sm-no_b_mass", proc="generate p p > w- h", cuts={**BG, "ptheavy": 150, "dynamical_scale_choice": 3}, patch_cuts=False,
    py8="py8_vh.cmnd", br=["B_Wqq", "B_bb"], desc="W-H, W->qq', H->bb", test=False, gridpack=False)
add(idx=44, name="H_ttH_bb", cls="single_H", role="bkg", model="sm-no_b_mass", proc="generate p p > t t~ h", cuts={**BG, "dynamical_scale_choice": 3, "ptheavy": 150}, patch_cuts=False,
    py8="py8_hh_bb.cmnd", br=["B_bb"], desc="ttH, H->bb forced, tops decay inclusively in PY8; >=1 heavy pT>150", test=True, gridpack=True)
add(idx=45, name="H_ggH_jj_heft", cls="single_H", role="bkg(planned)", model="heft", proc="generate p p > h j j HIG=1 QCD=2", cuts={**BG, **VBS}, patch_cuts=True,
    py8="py8_hh_bb.cmnd", br=["B_bb"], desc="ggH+2j (HEFT, MLM/exclusive decision pending); planned, not a Phase-03 type", test=False, gridpack=False)
add(idx=50, name="V_Zjj_QCD_vbs", cls="V+jets", role="bkg", model="sm-no_b_mass", proc="generate p p > z j j QED=1", cuts={**BG, **VBS}, patch_cuts=True,
    py8="py8_vh.cmnd", br=["B_Zqq"], desc="Z+2j QCD (Z undecayed in LHE, Z->qq forced in PY8) with VBS filter; W+2j analogous (idx 51 planned)", test=True, gridpack=True)
add(idx=51, name="V_Wjj_QCD_vbs", cls="V+jets", role="bkg(planned)", model="sm-no_b_mass", proc="generate p p > w+ j j QED=1", cuts={**BG, **VBS}, patch_cuts=True,
    py8="py8_vh.cmnd", br=["B_Wqq"], desc="W+ + 2j (and W-) planned", test=False, gridpack=False)
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

def check_seeds():
    seen = {}
    for s in S:
        for J in (0, 1, 2):
            v = seed(s["idx"], J); assert v not in seen, f"seed collision {v}: {s['name']} J={J} vs {seen[v]}"; seen[v] = (s["name"], J)
        assert seed(s["idx"], 2) < seed(s["idx"] + 1, 0) and 0 <= 2 < 1000
    assert len({s["idx"] for s in S}) == len(S) and len({s["name"] for s in S}) == len(S)
    return seen
def card(s):
    L = ["# hh Phase-03 card, UNVALIDATED until reports/03 says otherwise. OUTDIR substituted by scripts/condor/make_gridpack_hh.sh",
         "set automatic_html_opening False", "set auto_update 0", "set nb_core 4", "set run_mode 2", "set lhapdf_py3 lhapdf-config",
         f"import model {s['model']}"]
    if s["model"].startswith("sm"):
        L += ["define p = g u c d s b u~ c~ d~ s~ b~", "define j = g u c d s b u~ c~ d~ s~ b~"]
    L += s["proc"].split("\n") + ["output OUTDIR -nojpeg", "launch OUTDIR", "0"]
    L += runcard(s, seed(s["idx"], 0))
    L += ["done"]
    return "\n".join(L) + "\n"
if __name__ == "__main__":
    seen = check_seeds()
    os.makedirs(f"{H}/cards", exist_ok=True); os.makedirs(f"{H}/config", exist_ok=True)
    for s in S:
        if s["gridpack"]: open(f"{H}/cards/{s['name']}.mg5", "w").write(card(s))
    m = dict(meta=dict(process="HH(boosted VBF HH->4b)", run="multi_r1", seed_scheme="1e6*3+1e4*11+J+1000*idx; J=0 gridpack,1 test,2 LHE closure",
                       n_mc_rule="signal: N>=max(50k, sigma*BR*3000/fb); backgrounds: effective-N policy (SPEC 4.3)"),
             br_inputs={k: dict(value=v[0], source=v[1]) for k, v in BR.items()},
             samples=[dict(idx=s["idx"], name=s["name"], cls=s["cls"], role=s["role"], model=s["model"], process=s["proc"], generator_cuts=s["cuts"],
                           vbs_anypair_patch=s["patch_cuts"], pythia_cmnd=s["py8"], br_ledger=s["br"], br_total=__import__("math").prod(BR[b.split("@")[0]][0] for b in s["br"]),
                           seed_gridpack=seed(s["idx"], 0), seed_test=seed(s["idx"], 1), seed_lhe_closure=seed(s["idx"], 2),
                           phase03_gridpack=s["gridpack"], phase03_test_job=s["test"], description=s["desc"], **({"coupling_kV_k2V_kl": list(s["coupling"])} if "coupling" in s else {}))
                      for s in S])
    yaml.safe_dump(m, open(f"{H}/config/sample_matrix_gen.yaml", "w"), sort_keys=False, width=200)
    yaml.safe_dump({v: dict(sample=k[0], J=k[1]) for v, k in seen.items()}, open(f"{H}/config/seeds.yaml", "w"))
    print(len(S), "samples;", sum(s["gridpack"] for s in S), "gridpacks;", sum(s["test"] for s in S), "test jobs; seeds unique:", len(seen))
