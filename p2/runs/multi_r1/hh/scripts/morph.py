#!/usr/bin/env python3
"""Six-point (kV,k2V,kl) morphing for EW pp->HHjj.  sigma(k) = sum_i c_i(k) sigma_i, with monomials
 m = (kV^4, k2V^2, kV^2 kl^2, kV^3 kl, kV k2V kl, kV^2 k2V)   [HVV^2-t-channel, HHVV^2, (HVV+HHH)^2, interf. HVV^2xHHH, HHVVxHHH, HVV^2xHHVV]
Matrix M_ij = m_j(basis point i); c(k) = m(k) M^-1.  Used for sigma and (bin-wise or event-wise) distributions."""
import numpy as np, itertools
def mono(k):
    kv, k2, kl = k
    return np.array([kv**4, k2**2, kv**2*kl**2, kv**3*kl, kv*k2*kl, kv**2*k2], float)
def mat(basis): return np.array([mono(b) for b in basis])
def coeffs(basis, k): return np.linalg.solve(mat(basis).T, mono(k))      # c_i : sum_i c_i m(b_i) = m(k)
def morph(basis, sig, k): return float(coeffs(basis, k) @ np.asarray(sig))
if __name__ == "__main__":
    rng = np.random.default_rng(1)
    cand = [(kv,k2,kl) for kv in (0.5,1,1.5) for k2 in (0,0.5,1,2,3) for kl in (-1,0,1,2,5) if (kv,k2,kl)!=(1,1,1)]
    best = []
    for _ in range(40000):
        idx = rng.choice(len(cand), 5, replace=False); b = [(1,1,1)] + [cand[i] for i in idx]
        c = np.linalg.cond(mat(b)); best.append((c, b))
    best.sort(key=lambda x: x[0])
    for c, b in best[:5]: print(f"cond={c:.3g}", b)
