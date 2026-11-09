import json
Z="/eos/home-r/rjiang/vbs_zh_codex_starter/p2/combination/zh_check/out/"; F="/eos/home-r/rjiang/vbs_zh_codex_starter/work/final_ntuples/final.json"
S={"frozen":json.load(open(F)),"repro":json.load(open(Z+"repro_final.json"))}
for n,f in (("uncal","ff_uncal_fix"),("cal","ff_cal_fix"),("clos","ff_closcorr_fix"),("reopt","ff_cal_reopt")): S[n]=json.load(open(Z+f+".json"))
reg=S["frozen"]["registry"]
def grp(d,k):
    g={}
    for sid,c in d["results"][k]["comp"].items(): g[reg[sid]["grp"]]=g.get(reg[sid]["grp"],0)+c["y"]
    return g
print("| class | frozen 500 | corrected 500 | frozen 3000 | corrected 3000 |\n|---|---|---|---|---|")
for G in sorted(grp(S["frozen"],"500_a")):
    print("| %s | %.4f | %.4f | %.4f | %.4f |"%(G,grp(S["frozen"],"500_a")[G],grp(S["cal"],"500_a")[G],grp(S["frozen"],"3000_a")[G],grp(S["cal"],"3000_a")[G]))
rows=[]
out={"changed":True,"description":"ZH inputs for the VH combination. 'corrected' = fake-photon rows F_QCD_Zajj/F_EW_Zajj replaced by the lepton-decontaminated, artefact-excluded fake-factor estimate (D34/D37), CMS-calibrated kappa; all other rows, cuts, nuisances and statistics identical to frozen zh-final-v1.1. Yields are expected events at the given luminosity (fb^-1).","fake_rows_changed":["F_QCD_Zajj","F_EW_Zajj"],"unchanged":["T_tta","T_tWa (direct count, artefact present, <1% of b)"],"results":{}}
for tag in ("frozen","uncal","cal","clos"):
    d=S[tag]; o={}
    for k,r in d["results"].items():
        fit=d["fit"][k]
        o[k]={x:r[x] for x in ("L","sigdef","s","b","s_mc","b_mc","sigma_b","sigma_s","Z_eq1","Z_syst_counting","mu95_cls","mu95_cls_stat")}; o[k]["fit_Z_syst"]=fit["Z_syst"]; o[k]["fit_mu95_syst"]=fit["mu95_syst"]; o[k]["fit_Z_stat"]=fit["Z_stat"]; o[k]["fit_mu95_stat"]=fit["mu95_stat"]
        if "F_QCD_Zajj" in r["comp"]: o[k]["components"]={s:{"y":c["y"],"mcstat":c["mcstat"],"method":c["method"],"raw_win":c["raw_win"],"raw_wide":c["raw_wide"]} for s,c in r["comp"].items()}
    out["results"][{"frozen":"frozen","uncal":"corrected_uncalibrated_kappa1","cal":"corrected_nominal","clos":"corrected_closure_scaled_kappa1.43"}[tag]]=o
out["optimum"]=S["cal"]["optimum"]; out["optimum_reoptimised_same"]=S["reopt"]["optimum"]==S["cal"]["optimum"]
out["kappa"]=json.load(open(Z+"analysis.json"))["calibration"]
json.dump(out,open("/eos/home-r/rjiang/vbs_zh_codex_starter/p2/combination/zh_check/zh_corrected_inputs.json","w"),indent=1)
print("\n| L | def | quantity | frozen | corrected (cal) | uncal kappa=1 | closure-scaled |\n|---|---|---|---|---|---|---|")
for k in ("500_a","1000_a","3000_a","500_b","1000_b","3000_b"):
    for q,nm in (("b","b"),("sigma_b","sigma_b"),("Z_eq1","Z (Eq.1)"),("Z_syst_counting","Z (with sigma_b)"),("mu95_cls","mu95 CLs counting"),("fit_mu95_syst","mu95 mgg fit"),("fit_Z_syst","Z mgg fit")):
        v=[]
        for t in ("frozen","cal","uncal","clos"):
            d=S[t]; r=d["results"][k]; v.append(r[q] if q in r else d["fit"][k][q.replace("fit_","").replace("Z_syst","Z_syst").replace("mu95_syst","mu95_syst")])
        print("| %s | %s | %s | %.4f | %.4f | %.4f | %.4f |"%(k[:-2],k[-1],nm,*v))
