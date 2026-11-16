#!/usr/bin/env python3
"""ZH-alone pyhf check of vh_ws/zh_channel_inputs.json (reproduction of the frozen-code mgg fit) and ZH-alone lambda_WZ q-curves (mgg templates, WH convention, both sign conventions; in the q-curves the signal template is replaced by the quadratic coupling template, so the histosys nuisances phscale and phres of the signal are NOT included there: all other nuisances and the MC statistics are).
Usage: python3 -P zh_pyhf.py <out.json>"""
import json, sys, warnings, numpy as np, pyhf
warnings.filterwarnings("ignore"); pyhf.set_backend("numpy", pyhf.optimize.scipy_optimizer())
VW = "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/combination/vh_ws"; Z = json.load(open(VW + "/zh_channel_inputs.json")); NB = len(Z["edges"]) - 1
def spec_for(d, lumi, sig_override=None, mcstat=True, nuis=True, drop=(), hyp=False):
    k = lumi/Z["lref"] if "lref" in Z else lumi/Z["lumi_ref_fb"]; S = []
    for nm, sm in Z["defs"][d]["samples"].items():
        if nm == "whsig_in_zh": continue
        mods = []
        if sm["role"] == "signal": mods.append(dict(name="mu", type="normfactor", data=None))
        y = np.array(sm["nominal"])*k
        if sig_override is not None and nm == "zhjj_ew":
            y = sig_override*k
            if hyp: mods.append(dict(name="hypshape", type="shapefactor", data=None))
        if mcstat: mods.append(dict(name="mcstat_zh", type="staterror", data=[max(x*k, 1e-12) for x in sm["mcstat"]]))
        if nuis:
            for nn, v in sm["nuis"].items():
                if nn in drop: continue
                if "up" in v:
                    if sig_override is not None: continue
                    mods.append(dict(name=nn, type="histosys", data=dict(hi_data=[x*k for x in v["up"]], lo_data=[x*k for x in v["down"]])))
                else: mods.append(dict(name=nn, type="normsys", data=dict(hi=v["norm_up"], lo=v["norm_down"])))
        S.append(dict(name=nm, data=list(map(float, y)), modifiers=mods))
    return dict(channels=[dict(name="ZH", samples=S)], observations=[dict(name="ZH", data=[0.0]*NB)], measurements=[dict(name="m", config=dict(poi="mu", parameters=[]))], version="1.0.0")
def model(spec):
    m = pyhf.Model(spec, poi_name="mu", validate=False); b = m.config.suggested_bounds(); b[m.config.poi_index] = (0.0, 1000.0); m._bounds = b; return m
def fit(m, data, mu=None):
    init = m.config.suggested_init(); fixed = m.config.suggested_fixed()
    if mu is not None: init[m.config.poi_index] = mu; fixed[m.config.poi_index] = True
    r = pyhf.infer.mle.fit(data, m, init_pars=init, par_bounds=m._bounds, fixed_params=fixed, return_fitted_val=True); return r[0], float(r[1])
def asimov(m, mu): p = m.config.suggested_init(); p[m.config.poi_index] = mu; return m.expected_data(p)
def z0(m): d = asimov(m, 1.0); _, n0 = fit(m, d, 0.0); ph, nh = fit(m, d); return float(np.sqrt(max(n0 - nh, 0.0)))
def mu95(m):
    d = asimov(m, 0.0); scan = np.geomspace(2.0, 300.0, 16); c = []
    for mu in scan: c.append(float(pyhf.infer.hypotest(float(mu), d, m, test_stat="qtilde", par_bounds=m._bounds, return_expected_set=True)[1][2]))
    c = np.array(c); return float(np.exp(np.interp(0.05, c[::-1], np.log(scan)[::-1])))
res = dict(repro={}, qcurves={})
for L in (500.0, 1000.0, 3000.0):
    for d in ("a", "b"):
        m = model(spec_for(d, L)); res["repro"][f"{int(L)}_{d}"] = dict(Z0_PL=z0(m), mu95_PL=mu95(m), Z0_PL_nosyst=z0(model(spec_for(d, L, nuis=False))), Z0_PL_nomc=z0(model(spec_for(d, L, mcstat=False))))
        print(L, d, res["repro"][f"{int(L)}_{d}"], flush=True)
# ZH-alone q-curves (def a, MC stat + all nuisances; signal = quadratic template; QCD ZHjj as in def a background fixed)
co = Z["coupling"]["quad"]; al, be, ga = (np.array(co[k]) for k in ("alpha", "beta", "gamma"))
BRSM = dict(bb=0.5824, WW=0.2137, gg=0.0818, tautau=0.0627, cc=0.0289, ZZ=0.0264, gamgam=0.00227, Zgam=0.00154, mumu=0.00022)
def rbr(kW, kZ):
    ag = (-8.32*kW + 1.84)**2/(-8.32 + 1.84)**2; w = sum(BRSM.values()) - BRSM["WW"] - BRSM["ZZ"] - BRSM["gamgam"]; w += BRSM["WW"]*kW**2 + BRSM["ZZ"]*kZ**2 + BRSM["gamgam"]*ag; return ag/(w/sum(BRSM.values()))
def ysig(kW, kZ): return np.maximum(al*kW**2 + be*kW*kZ + ga*kZ**2, 0.0)*rbr(kW, kZ)
LAMS = np.round(np.arange(-2.0, 2.0001, 0.1), 3)
for L in (500.0, 1000.0, 3000.0):
    base = spec_for("a", L)
    out = {}
    for conv, f in (("kZ_sign_primary", lambda lam: (-lam, -1.0)), ("kW_sign_variant", lambda lam: (lam, 1.0))):
        # Asimov data: SM point (kW,kZ)=(1,1) with the HC quad template; same signal normalisation convention in the hypotheses
        ys_sm = np.maximum(ysig(1.0, 1.0), 1e-6)
        m = model(spec_for("a", L, sig_override=ys_sm, hyp=True)); sl = m.config.par_slice("hypshape"); data = asimov(m, 1.0)
        def nll_for(g):
            init = m.config.suggested_init(); fixed = m.config.suggested_fixed(); init[m.config.poi_index] = 1.0; fixed[m.config.poi_index] = True
            for i in range(sl.start, sl.stop): init[i] = float(g[i - sl.start]); fixed[i] = True
            bd = list(m._bounds)
            for i in range(sl.start, sl.stop): bd[i] = (0.0, 1000.0)
            return float(pyhf.infer.mle.fit(data, m, init_pars=init, par_bounds=bd, fixed_params=fixed, return_fitted_val=True)[1])
        n_sm = nll_for(np.ones(NB)); q = []
        for lam in LAMS:
            kW, kZ = f(lam); q.append(max(nll_for(np.maximum(ysig(kW, kZ), 0.0)/ys_sm) - n_sm, 0.0))
        qa = np.array(q); i1 = int(np.argmin(abs(LAMS + 1))); neg = LAMS < 0
        out[conv] = dict(lam=LAMS.tolist(), q=qa.tolist(), Z_lambda_m1=float(np.sqrt(qa[i1])), Z_lambda_neg=float(np.sqrt(qa[neg].min())), R_BR_lambda_m1=rbr(*f(-1.0)))
    res["qcurves"][f"{int(L)}"] = out; print(L, {c: (round(v["Z_lambda_m1"], 4), round(v["Z_lambda_neg"], 4), round(v["R_BR_lambda_m1"], 3)) for c, v in out.items()}, flush=True)
json.dump(res, open(sys.argv[1], "w"), indent=1)
