#!/usr/bin/env python3
"""Phase-02/M7b sample statistics, MC-stat adequacy, storage and CPU table. Writes reports/04_stats_table.md and
config/production_v2.yaml. Inputs: measured sigma (work/m5/*/status.txt, 03 report) and LABELLED estimates."""
import math, yaml
L=500.0; Baa=0.002270; ZF=0.9783
# id: (sigma_gen_fb, err_fb, source, gen-cuts/decay, br_treatment, br_factor, N_planned, kB_slim, keep_lhe, t_ev_s, SR_yield, eps_SR or None, ff)
S = [
 ("S_EW_ZHjj",       1.298, 0.008, "measured", "pTj>20,|etaj|<5,dRjj>0.4; Z->ee/mumu ME", "x B_gg x ZF (PY8 forced H->gg)", Baa*ZF, 200e3, 2.40, 1, 0.10, 0.105, 0.0727, None),
 ("S_EW_ZHjj_offshell",1.3, None, "ESTIMATE (~on-shell)", "llHjj QED=5, mll>50", "x B_gg", Baa, 50e3, 2.40, 1, 0.10, None, None, None),
 ("H_QCD_ZH_mlm",    48.45, 0.37, "measured 0j LO proxy", "ZH(+0,1,2j MLM), Z->ll ME", "x B_gg x ZF", Baa*ZF, 500e3, 2.77, 1, 0.20, 0.099, 0.099/(48.45*Baa*ZF*L), None),
 ("H_QCD_ZHjj_fixed",10.25, 0.03, "measured", "(2,2) ZHjj, jet cuts as signal", "x B_gg x ZF", Baa*ZF, 100e3, 2.77, 1, 0.10, 0.099, 10/1000*0.87, None),
 ("I_ZHjj",         -0.114, 0.007,"measured (undecayed)", "QCD^2==2 QED^2==6, jet cuts", "x B_ll(PDG) x B_gg", 0.067294*Baa, 50e3, 2.40, 1, 0.10, -0.0006, None, None),
 ("H_ggZH",          9.1, None,  "ESTIMATE YR4 13TeV x1.1 x B_ll", "loop gg->ZH, Z->ll", "x B_gg", Baa, 50e3, 2.5, 1, 0.20, 0.01, 0.01/10.3, None),
 ("H_ttH",          17.98, 0.20, "measured", "dilep e/mu (MG W BR), no jet cuts", "x B_gg", Baa, 100e3, 2.5, 1, 0.10, 0.035, 1/500*0.87, None),
 ("H_tHW",           0.71, None, "ESTIMATE YR4 15.2 fb x 0.0469", "dilep, DR", "x B_gg", Baa, 50e3, 2.5, 1, 0.10, 0.0005, None, None),
 ("H_ZH_tautau",    24.2, 0.2,   "derived from zh_0j (one flavour)", "ZH, Z->tautau ME, PY8 tau decays", "x B_gg", Baa, 50e3, 2.5, 1, 0.10, 0.002, None, None),
 ("B_EW_llaajj",     0.15, None, "ESTIMATE ref 0.426 fb x0.35 (mgg 90-190)", "ref cuts + 90<mgg<190", "none (ll in ME)", 1.0, 100e3, 2.5, 0, 1.00, 0.9, 0.9/75.0, None),
 ("B_QCD_llaa_mlm",  2.893, 0.027,"measured 0j LO proxy", "ref cuts + 90<mgg<190, 0-2j MLM", "none", 1.0, 500e3, 2.5, 0, 1.00, 0.43, 0.43/1447.0, None),
 ("I_llaajj",        0.0085, None,"ESTIMATE ref 0.0244 fb x0.35", "QCD^2==2 QED^2==10", "none (signed)", 1.0, 50e3, 2.5, 0, 1.00, 0.05, None, None),
 ("F_QCD_lla_mlm",1775.0, 6.0,   "measured Zgamma+2j pilot (lower bound for 1-3j MLM)", "ref cuts, 1-3j MLM", "none; x f(j->g) per jet", 1.0, 1.0e6, 1.63, 0, 0.20, 0.59, None, "zg"),
 ("F_EW_llajj",     35.6, 0.31,  "measured", "ref cuts, QED=5", "none; x f(j->g)", 1.0, 200e3, 1.63, 0, 0.15, 0.12, None, None),
 ("F_Zjets_mlm", 211500.0, 919.0,"measured Z+2j pilot (lower bound for 2-4j MLM)", "mll>50, ptj>20, 2-4j MLM", "none; x f1 f2 per jet pair", 1.0, 1.0e6, 1.50, 0, 0.20, 0.19, None, "zj"),
 ("T_ttaa",          0.0949, 0.0013,"measured", "dilep, pTa>15,|eta|<2.5, 90<mgg<190", "none (t,W in ME)", 1.0, 50e3, 2.5, 0, 0.10, 0.005, None, None),
 ("T_tta",          85.67, 1.0,  "measured", "dilep, pTa>15,|eta|<2.5", "none; 2nd photon x f(j->g)", 1.0, 100e3, 2.5, 0, 0.10, 0.05, None, None),
 ("T_tWa",          13.07, 0.16, "measured", "dilep, DR, pTa>15", "none; x f(j->g)", 1.0, 50e3, 2.5, 0, 0.10, 0.01, None, None),
 ("T_tt",        23470.0, 238.0, "measured", "dilep e/mu", "none; x f1 f2", 1.0, 1.0e6, 2.5, 0, 0.10, 0.05, None, None),
 ("V_WZa",           7.0, None,  "ESTIMATE (batch sigma job pending)", "lllv+gamma", "none; x f(e->g)", 1.0, 50e3, 2.5, 0, 0.10, 0.02, None, None),
 ("V_ZZa",           1.0, None,  "ESTIMATE (batch sigma job pending)", "4l+gamma", "none; x f(e->g)", 1.0, 50e3, 2.5, 0, 0.10, 0.005, None, None),
]
# fake-factor pilots (5k events): N_eff per 5k and mean weight at pilot w_evt
pilot = {"zj": dict(w=21150.0, vbs_neff=32.2, vbs_w=0.0600, peak_neff=4.07, peak_w=0.0380),
         "zg": dict(w=177.5,   vbs_neff=11.3, vbs_w=0.3283, peak_neff=None, peak_w=None)}
Ntot_SR = sum(max(r[11] or 0,0) for r in S if not r[0].endswith(("offshell","_fixed")))
data_unc = math.sqrt(Ntot_SR)
rows=[]; out={}
tot_N=tot_GB=tot_h=0
for (sid,sg,er,src,cuts,brt,brf,N,kb,klhe,tev,ysr,eps,ff) in S:
    sphys=sg*brf; sL=sphys*L; w=abs(sL)/N
    kbt=kb+(1.25 if klhe else 0.0); GB=N*kbt/1e6
    h=N*tev/3600; tot_N+=N; tot_GB+=GB; tot_h+=h
    if ff:
        p=pilot[ff]; scale=N/5000.0; w_raw=sg*L/N
        neff_sr = (p["peak_neff"]*scale) if p["peak_neff"] else 0.1*p["vbs_neff"]*scale
        mcrel = 1/math.sqrt(neff_sr); wvbs=p["vbs_w"]*w_raw/p["w"]
        ffinfo=f"VBS: N_eff={p['vbs_neff']*scale:,.0f}, <w>={wvbs:.1e}; PEAK: N_eff={neff_sr:,.0f}{' (est. 10% of VBS)' if not p['peak_neff'] else ''}, <w>={(p['peak_w'] or p['vbs_w'])*w_raw/p['w']:.1e}"
    elif eps:
        neff_sr=N*eps; mcrel=1/math.sqrt(neff_sr); ffinfo=""
    else:
        neff_sr=None; mcrel=None; ffinfo=""
    ratio = (abs(ysr)*mcrel/data_unc) if (mcrel and ysr) else None
    rows.append((sid,sg,er,src,brt,sL,N,w,kbt,GB,h,ysr,neff_sr,ratio,ffinfo,cuts))
    out[sid]=dict(sigma_gen_fb=sg, sigma_err_fb=er, sigma_source=src, gen_cuts_decay=cuts, br_treatment=brt,
                  sigma_phys_x_L_events=round(sL,4), N_planned=int(N), raw_event_weight=float(f"{w:.3g}"),
                  kB_per_event=kbt, storage_GB=round(GB,2), core_h=round(h,1), SR_yield_est=ysr,
                  SR_mc_eff_events=(round(neff_sr) if neff_sr else None), mcstat_over_datastat=(round(ratio,4) if ratio else None))
fmt=lambda x,p=3: "—" if x is None else (f"{x:.{p}g}")
md=["| Sample | σ_gen [fb] (± MC) | source | BR / decay treatment | σ_phys×L [ev] | N_planned | raw weight | kB/ev | GB | core-h | SR yield (est.) | MC eff. events in SR | MC/data stat |","|"+"---|"*13]
for (sid,sg,er,src,brt,sL,N,w,kbt,GB,h,ysr,neff,ratio,ffi,cuts) in rows:
    md.append(f"| {sid} | {fmt(sg,4)} ± {fmt(er,2)} | {src} | {brt} | {sL:.3g} | {N/1e3:.0f}k | {w:.2g} | {kbt:.2f} | {GB:.2f} | {h:.1f} | {fmt(ysr,2)} | {fmt(neff,3)} | {fmt(ratio,2)} |")
md.append(f"| **Total** | | | | | **{tot_N/1e6:.2f} M** | | | **{tot_GB:.1f}** | **{tot_h:.0f}** | **{Ntot_SR:.2f}** (data stat ±{data_unc:.2f}) | | |")
ff=[f"- {r[0]}: {r[14]}" for r in rows if r[14]]
open('/eos/home-r/rjiang/vbs_zh_codex_starter/reports/04_stats_table.md','w').write("\n".join(md)+"\n\nFake-factor samples (scaled from 5k-event pilots, nominal f0=1e-3):\n"+"\n".join(ff)+"\n")
yaml.safe_dump({"production_v2":{"generated_by":"scripts/plan/stats_table.py","lumi_fb":L,"B_gg":Baa,"Z_BR_PDG_over_MG":ZF,
  "SR_definition":"illustrative VBS (mjj>500,|deta|>2.5) + 120<mgg<130; NOT optimised","data_stat_SR_events":round(data_unc,3),"samples":out}},
  open('/eos/home-r/rjiang/vbs_zh_codex_starter/config/production_v2.yaml','w'),sort_keys=False,width=200)
print("\n".join(md)); print("\n".join(ff))
