#!/usr/bin/env python3
"""Toy validation of the asymptotic headline numbers (A4, D47 (2)). Operates on a pyhf workspace JSON (p2/combination/vh_ws/*_workspace.json: WH, ZH, VH; observations are the SM Asimov data).
Tasks (one condor job each; results npz in work/toys/):
  q0   <ws> <poi> <seed> <ntoys>                : q0 of s+b toys (mu = 1, nuisances at their nominal value, auxiliary data thrown) -> median Z0 = sqrt(median q0), compared with the Asimov sqrt(q0_A)
  qmu  <ws> <poi> <mu> <seed> <ntoys> <hyp>     : qtilde_mu of toys generated under hyp = 'sb' (mu) or 'b' (mu = 0): CLs(mu) = p_sb / p_b from the two distributions; the expected mu95 is the mu where the median-b CLs = 0.05
Usage: python3 toys.py q0|qmu ...   Aggregation: toys.py agg <ws-tag> """
import sys, os, json, numpy as np, pyhf
pyhf.set_backend("numpy", pyhf.optimize.scipy_optimizer())
WH = os.environ.get("STAT_WH", "/eos/home-r/rjiang/vbs_zh_codex_starter/p2/runs/multi_r1/wh"); OUT = f"{WH}/work/toys"; os.makedirs(OUT, exist_ok=True)
def load(wsf, poi):
    ws = pyhf.Workspace(json.load(open(wsf))); m = ws.model(measurement_name="m", modifier_settings={}); 
    return ws, m
def prep(wsf, poi):
    spec = json.load(open(wsf)); ws = pyhf.Workspace(spec); m = ws.model(); b = m.config.suggested_bounds(); 
    for n_ in m.config.par_map:
        if n_.startswith("mu"): b[m.config.par_slice(n_).start] = (0.0, 50.0)
    return m, b
def run_q0(wsf, poi, seed, nt):
    m, b = prep(wsf, poi); rng = np.random.default_rng(seed); pyhf.set_backend("numpy", pyhf.optimize.scipy_optimizer()); init = m.config.suggested_init(); pars = list(init); pars[m.config.par_slice(poi).start] = 1.0
    pdf = m.make_pdf(pyhf.tensorlib.astensor(pars)); out = []
    for i in range(nt):
        d = pdf.sample((1,))[0]; q = pyhf.infer.test_statistics.q0(0.0, d, m, init, b, m.config.suggested_fixed()); out.append(float(q))
    np.save(f"{OUT}/q0_{os.path.basename(wsf)[:-5]}_{poi}_s{seed}.npy", np.array(out))
def run_qmu(wsf, poi, mu, seed, nt, hyp):
    m, b = prep(wsf, poi); init = m.config.suggested_init(); pars = list(init); pars[m.config.par_slice(poi).start] = (mu if hyp == "sb" else 0.0)
    pdf = m.make_pdf(pyhf.tensorlib.astensor(pars)); out = []
    for i in range(nt):
        d = pdf.sample((1,))[0]; out.append(float(pyhf.infer.test_statistics.qmu_tilde(mu, d, m, init, b, m.config.suggested_fixed())))
    np.save(f"{OUT}/qmu_{os.path.basename(wsf)[:-5]}_{poi}_mu{mu}_{hyp}_s{seed}.npy", np.array(out))
if __name__ == "__main__":
    t = sys.argv[1]
    if t == "q0": run_q0(sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]))
    elif t == "qmu": run_qmu(sys.argv[2], sys.argv[3], float(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), sys.argv[7])
