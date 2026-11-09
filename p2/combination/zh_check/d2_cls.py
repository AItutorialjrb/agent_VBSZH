import json, numpy as np
from scipy import stats, optimize
def cls_limit(s, b, sb, alpha=0.05, ss=0.0, nfix=None):
    gx, gw = np.polynomial.hermite_e.hermegauss(30); gw = gw/gw.sum()
    def ln(x, rel):
        if rel <= 0: return np.full(1, x), np.ones(1)
        v = np.log(1 + rel**2); return x*np.exp(np.sqrt(v)*gx - 0.5*v), gw
    bs, wb = ln(b, sb/b if b > 0 else 0); s_, ws = ln(s, ss/s if s > 0 else 0)
    BS, SS = np.meshgrid(bs, s_); W2 = np.outer(ws, wb)
    cdf = lambda n, mu: (W2*stats.poisson.cdf(n, mu*SS + BS)).sum(); cdf0 = lambda n: (wb*stats.poisson.cdf(n, bs)).sum()
    nn = np.arange(0, int(b + 10*np.sqrt(b + 1) + 10*sb + 20)); c0 = np.array([cdf0(k) for k in nn]); nmed = nn[np.searchsorted(c0, 0.5)]
    if nfix is not None: nmed = nfix
    f = lambda mu: cdf(nmed, mu)/cdf0(nmed) - alpha; hi = 1.0
    while f(hi) > 0: hi *= 2
    return float(optimize.brentq(f, 0, hi)), int(nmed), float(cdf0(nmed)), (c0[:6].tolist())
def asimov(s, b, sb):
    """smooth Asimov (data = b) 95% limit, q_mu = 2[(b+mu s)... ] with b-uncertainty folded in as Gaussian constraint on b (profile): continuous in b"""
    def q(mu):
        sm = mu*s
        # profile b-hat for data n=b with constraint (b0=b, sigma=sb): minimise (b'+sm - n ln(b'+sm)) + (b'-b)^2/(2 sb^2)
        r = optimize.minimize_scalar(lambda bp: (bp + sm) - b*np.log(bp + sm) + 0.5*((bp - b)/sb)**2, bounds=(1e-6, 10*b + 10), method="bounded")
        r0 = (r.fun - (b - b*np.log(b)))
        return 2*r0
    return optimize.brentq(lambda mu: q(mu) - 3.841, 1e-6, 1e4)
if __name__ == "__main__":
    import sys
    S = {"frozen": "/eos/home-r/rjiang/vbs_zh_codex_starter/work/final_ntuples/final.json", **{k: f"out/{k}.json" for k in sys.argv[1:]}}
    for n, f in S.items():
        d = json.load(open(f)); 
        for L in ("500", "1000", "3000"):
            r = d["results"][L+"_a"]; m, nm, c0, cs = cls_limit(r["s"], r["b"], r["sigma_b"], ss=r["sigma_s"])
            print(f"{n:12s} {L:5s} s={r['s']:.4f} b={r['b']:.4f} sigma_b={r['sigma_b']:.4f} n_med={nm} P(n<=nmed|b)={c0:.3f} mu95_CLs={m:.2f} (json {r['mu95_cls']:.2f}) mu95_Asimov_smooth={asimov(r['s'], r['b'], r['sigma_b']):.2f}")
