#!/usr/bin/env python3
"""Direct-fake closure of the measured Delphes j->gamma parametrisation on the PRODUCTION W+4j files (04 sec. 20; scope 1a): the fake-factor prediction (fakefactor_pilot_w.py, class W, nfake = 2) with the rate table measured on the OPPOSITE job-seed-parity half
(even-seed files use the table of the odd half and vice versa: disjoint split) is compared with the DIRECTLY counted yield of events that contain two real reco photons of fake origin (pT>25, |eta|<2.5, no crack, no prompt gen photon within dR<0.1, GenTruth gph_prompt) in the same regions PRE / VBS / PEAK
(1 lepton pT>25, no 2nd lepton pT>15, MET>30; tag jets pT>30, |eta|<4.7, dR>0.4 from both photons; b-veto; VBS = mjj>500 and |deta|>2.5; PEAK = VBS + 120<m_gg<130).  Events: n_prompt_photons == 0.
Default sample F_QCD_Wajjj_nomjj (env DSAMPLE, NFAKE, DK = every DK-th file). Stages: pilots | direct | compare   (bash scripts/envrun.sh python3 -P scripts/postprod_direct.py <stage>)"""
import sys, os, json, glob, re, subprocess, numpy as np, uproot, awkward as ak
from multiprocessing import Pool
WH = "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh"; PR = "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/production/wh"; OUT = f"{WH}/work/postprod_clo"
DS = os.environ.get("DSAMPLE", "F_QCD_Wajjj_nomjj"); NF = int(os.environ.get("NFAKE", "1"))   # nfake = 1: one real prompt photon + one fake-origin photon (default, F_QCD_Wajjj); nfake = 2: two fake-origin photons (W+4j, no direct events expected)
SIG = json.load(open(f"{WH}/work/ff_{DS}.json"))["sigma_fb"]; L = 500.0
FILES = sorted(f for f in glob.glob(f"{PR}/{DS}/*.root") if not f.endswith("_gen.root"))[::int(os.environ.get("DK", "4"))]
def par(f): return int(re.search(r"_s(\d+)\.root", f).group(1)) % 2
def pil(f):
    o = f"{OUT}/pil_{os.path.basename(f)[:-5]}.json"
    if os.path.exists(o): return o
    tab = f"{WH}/work/postprod/rate_{'odd' if par(f) == 0 else 'even'}.json"
    env = dict(os.environ, RATE_CLASS="W", BVETO="1", PHOTON_PT="25", RATE_FILE=tab); stem = f[:-5]
    r = subprocess.run([sys.executable, "-P", f"{WH}/scripts/fakefactor_pilot_w.py", f, stem + "_gen.root", "-", str(SIG), str(NF), o], env=env, capture_output=True, text=True)
    return o if r.returncode == 0 else None
def dphi(a, b): return (a-b+np.pi) % (2*np.pi)-np.pi
def lv(q, e, p): return np.array([q*np.cos(p), q*np.sin(p), q*np.sinh(e), q*np.cosh(e)])
def mm(a, b): s = a+b; return float(np.sqrt(max(s[3]**2-s[0]**2-s[1]**2-s[2]**2, 0)))
def dirc(f):
    T = uproot.open(f)["Delphes"]; G = uproot.open(f[:-5] + "_gen.root")["GenTruth"]
    a = T.arrays(["Jet.PT", "Jet.Eta", "Jet.Phi", "Jet.BTag", "Photon.PT", "Photon.Eta", "Photon.Phi", "Electron.PT", "Electron.Eta", "Muon.PT", "Muon.Eta", "MissingET.MET"], library="np")
    g = G.arrays(["n_prompt_photons", "gph_eta", "gph_phi", "gph_prompt"], library="ak"); npr = ak.to_numpy(g["n_prompt_photons"]); gE = ak.to_list(g["gph_eta"]); gP = ak.to_list(g["gph_phi"]); gR = ak.to_list(g["gph_prompt"]); N = len(npr)
    cnt = {"PRE": 0, "VBS": 0, "PEAK": 0}
    for i in range(N):
        if npr[i] != (0 if NF == 2 else 1) or a["MissingET.MET"][i][0] <= 30: continue
        nl = [q for q, e in zip(a["Electron.PT"][i], a["Electron.Eta"][i]) if q > 15 and abs(e) < 2.5]+[q for q, e in zip(a["Muon.PT"][i], a["Muon.Eta"][i]) if q > 15 and abs(e) < 2.4]
        if len(nl) != 1 or nl[0] <= 25: continue
        gp = [(ge, gf) for ge, gf, pr in zip(gE[i], gP[i], gR[i]) if pr]
        allph = [(q, e, p) for q, e, p in zip(a["Photon.PT"][i], a["Photon.Eta"][i], a["Photon.Phi"][i]) if q > 25 and abs(e) < 2.5 and not (1.4442 < abs(e) < 1.566)]
        isreal = lambda x: any(np.hypot(x[1]-ge, dphi(x[2], gf)) < 0.1 for ge, gf in gp)
        fk = sorted([x for x in allph if not isreal(x)], reverse=True)
        if NF == 2:
            if len(fk) < 2: continue
            ph = fk[:2]
        else:
            rl = [x for x in allph if isreal(x)]
            if not rl or not fk: continue
            ph = [max(rl), fk[0]]
        J = [(q, e, p) for q, e, p, b in zip(a["Jet.PT"][i], a["Jet.Eta"][i], a["Jet.Phi"][i], a["Jet.BTag"][i]) if q > 30 and abs(e) < 4.7 and all(np.hypot(e-x[1], dphi(p, x[2])) > 0.4 for x in ph)]
        if any(b > 0 and q > 30 and abs(e) < 2.5 for q, e, b in zip(a["Jet.PT"][i], a["Jet.Eta"][i], a["Jet.BTag"][i])): continue
        if len(J) < 2: continue
        J = sorted(J, reverse=True); cnt["PRE"] += 1
        if mm(lv(*J[0]), lv(*J[1])) > 500 and abs(J[0][1]-J[1][1]) > 2.5:
            cnt["VBS"] += 1
            if 120 < mm(lv(*ph[0]), lv(*ph[1])) < 130: cnt["PEAK"] += 1
    return dict(file=f, N=N, par=par(f), **cnt)
if __name__ == "__main__":
    st = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
    if st == "pilots":
        with Pool(8) as p: r = p.map(pil, FILES, chunksize=1)
        print("pilots done, failed:", sum(x is None for x in r))
    if st == "direct":
        with Pool(8) as p: r = p.map(dirc, FILES, chunksize=1)
        json.dump(r, open(f"{OUT}/direct.json", "w")); print("direct done")
    if st == "compare":
        D = json.load(open(f"{OUT}/direct.json")); res = {}
        for half in ("even", "odd", "all"):
            sel = [d for d in D if half == "all" or d["par"] == (0 if half == "even" else 1)]
            if not sel: continue
            Nsub = sum(d["N"] for d in sel); row = {}
            for reg in ("PRE", "VBS", "PEAK"):
                dc = sum(d[reg] for d in sel); dy = SIG*L*dc/Nsub; de = SIG*L*np.sqrt(max(dc, 1))/Nsub
                Y = 0.0; sw2 = 0.0
                for d in sel:
                    j = json.load(open(f"{OUT}/pil_{os.path.basename(d['file'])[:-5]}.json")); r = j["regions"][reg]; y = r.get("yield_events_at_lumi", 0.0); ne = r.get("N_eff", 0.0)
                    Y += y*d["N"]/Nsub; sw2 += (y**2/ne if ne > 0 else 0.0)*(d["N"]/Nsub)**2
                pe = np.sqrt(sw2); z = (dy-Y)/np.sqrt(de**2+pe**2) if (de**2+pe**2) > 0 else 0.0
                row[reg] = dict(direct_count=dc, direct_yield=dy, direct_err=de, predicted=Y, predicted_err=pe, ratio_direct_over_pred=(dy/Y if Y else None), pull=float(z))
            res[half] = dict(n_files=len(sel), N=Nsub, regions=row)
        json.dump(res, open(f"{OUT}/closure.json", "w"), indent=1)
        for h, v in res.items(): print(h, v["n_files"], {k: (v2["direct_count"], round(v2["direct_yield"], 2), round(v2["predicted"], 2), round(v2["pull"], 2)) for k, v2 in v["regions"].items()})
