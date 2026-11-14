#!/usr/bin/env python3
"""Joint VH likelihood tasks (A3). Usage (env STAT_V12=1 STAT_TABLE=table_v12 STAT_YIELDS=yields_v12):
  ws                       : write VH_workspace.json (common mu_VH, def a), VH_workspace_2d.json, WH_/ZH_workspace.json (+ def b variants) into p2/combination/vh_ws/ at 500 fb^-1 (observations = SM Asimov)
  z0mu:<L>:<d>:<which>     : expected Z0 and asymptotic mu95 (median, -1s, +1s) for which in wh|zh|both (common mu), yields of the signal-like rows
  map2d:<L>:<d>            : 2D (mu_WH, mu_ZH) profile-likelihood map on the SM Asimov data, best fit, expected compatibility q(mu_WH = mu_ZH) and the expected sensitivity to incompatibility
Results work/stat/vh_<task>_v12.json."""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vh_build import *
task = sys.argv[1]; res = dict(task=task); VW = "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/combination/vh_ws"
def z0_mu(m):
    z, mh = z0_asimov(m); return z
def mu95(m, poi_name):
    d = asimov(m, 0.0); scan = np.geomspace(0.3, 80.0, 16); E = []
    for mu in scan:
        r = pyhf.infer.hypotest(float(mu), d, m, test_stat="qtilde", par_bounds=m._bounds, return_expected_set=True); E.append([float(x) for x in r[1]])
    E = np.array(E); out = []
    for idx in (1, 2, 3):
        c = E[:, idx]; lm = np.log(scan); out.append(float(np.exp(np.interp(0.05, c[::-1], lm[::-1]))) if c.min() < 0.05 < c.max() else (float(scan[-1]) if c.min() > 0.05 else float(scan[0])))
    return out
if task == "ws":
    for d in "ab":
        for which in ("wh", "zh", "both"):
            m = make(500.0, d, "common", which); nm = {"wh": "WH", "zh": "ZH", "both": "VH"}[which]; write_ws(m, f"{VW}/{nm}_workspace{'' if d == 'a' else '_defb'}.json")
        m = make(500.0, d, "2d", "both"); write_ws(m, f"{VW}/VH_workspace_2d{'' if d == 'a' else '_defb'}.json")
    print("workspaces written")
elif task.startswith("z0mu"):
    _, L, d, which = task.split(":"); L = float(L); m = make(L, d, "common", which); m._bounds = m.config.suggested_bounds() if which == "zh" else m._bounds
    b = list(m._bounds) if which != "zh" else m.config.suggested_bounds()
    for n_ in m.config.par_map:
        if n_.startswith("mu"): b[m.config.par_slice(n_).start] = (0.0, 100.0)
    m._bounds = b
    res.update(lumi=L, definition=d, which=which, Z0=z0_mu(m), mu95=mu95(m, "mu"), npar=len(m.config.suggested_init()))
elif task.startswith("map2d"):
    _, L, d = task.split(":"); L = float(L); m = make(L, d, "2d", "both"); b = m.config.suggested_bounds()
    for n_ in m.config.par_map:
        if n_.startswith("mu"): b[m.config.par_slice(n_).start] = (0.0, 80.0)
    m._bounds = b; data = asimov(m, 1.0); iw = m.config.par_slice("mu_WH").start; iz = m.config.par_slice("mu_ZH").start
    def nll(fix):
        init = list(m.config.suggested_init()); fixed = m.config.suggested_fixed()
        for i, v in fix.items(): init[i] = v; fixed[i] = True
        r = pyhf.infer.mle.fit(data, m, init_pars=init, par_bounds=b, fixed_params=fixed, return_fitted_val=True); return float(r[1]), r[0]
    n0, pars0 = nll({}); gw = [0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0]; gz = [0.0, 0.5, 1.0, 2.0, 4.0, 8.0, 16.0, 32.0]
    q = [[max(nll({iw: a, iz: c})[0]-n0, 0.0) for c in gz] for a in gw]
    # compatibility: common mu (iw tied to iz is not available in a 2d model): scan the diagonal mu_WH = mu_ZH = x and take the minimum
    diag = [max(nll({iw: x, iz: x})[0]-n0, 0.0) for x in (0.5, 1.0, 1.5, 2.0)]
    res.update(lumi=L, definition=d, best_fit=dict(mu_WH=float(pars0[iw]), mu_ZH=float(pars0[iz])), grid_mu_WH=gw, grid_mu_ZH=gz, q=q, q_diag_common=dict(zip(["0.5", "1.0", "1.5", "2.0"], diag)),
               compatibility_note="SM Asimov data: mu_hat_WH = mu_hat_ZH = 1, so the expected channel-compatibility q (common mu vs separate) is 0 and p = 1 by construction; the sensitivity to incompatibility is read from the map (q at (mu_WH, mu_ZH) = (1, 4), (1, 8), (2, 1), ...)")
os.makedirs(f"{WH}/work/stat", exist_ok=True); json.dump(res, open(f"{WH}/work/stat/vh_{task.replace(':', '_')}{SUF}.json", "w"), indent=1, default=float); print(json.dumps(res, default=float)[:600])
