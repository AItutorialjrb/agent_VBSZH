# E (2026-11-03): VH coupling interpretation (lambda_WZ = kappa_W/kappa_Z; CP-odd c_A), executed INSIDE final_analysis.py's
# namespace (exec) so that the selection (OPT), estimation hierarchy, corrections and nuisance model are identical to the SM
# result. A WH analysis reuses this file unchanged with its own POINTS / process names.
#
# Model. EW VHjj amplitude = kZ*A_Z + kW*A_W (massless quarks: the Higgs couples only to W and Z at tree level), so for
# kappa_Z = kZ and lambda = kW/kZ: s(kZ, lambda) = kZ^2 * (a + b*lambda + c*lambda^2), exactly. a, b, c are fitted per bin
# of the observable to DIRECT Delphes samples at lambda in {-1, -0.5, 0, 0.5, 1, 1.5} (HC_NLO_X0_kVV, cards/coupling).
# No MG5 reweighting is used. Closure: (i) leave-one-out prediction of lambda = -1 and 1.5 from the other points;
# (ii) the HC lambda = 1 point vs the SM-model Tier-1 signal (different model + generator mjj cut) at the full selection.
# H -> gamma gamma: headline = production-only interpretation, BR(H->gg) fixed to SM (kappa_gamma treated as a free
# effective coupling constrained by inclusive H->gg data); variant = resolved kappa_gamma(kW, kt=1) and total width.
# QCD ZHjj scales with kZ^2 (Higgsstrahlung-type); ggZH, ttH, tHW kept at SM (stated limitation).
# Statistics: binned Poisson likelihood in the chosen observable inside the signal region (all OPT cuts incl. the m_gg
# window), Asimov data at the SM (lambda = 1, kZ = 1), all nuisances of the main result (per-process normalisation (+) MC
# stat, correlated theory groups incl. signal theory, off-shell, Zgg interference, ggZH x2, generator-mjj correction, lumi).
CPL = {}
KPTS = {"lam_m100": -1.0, "lam_m050": -0.5, "lam_p000": 0.0, "lam_p050": 0.5, "lam_p100": 1.0, "lam_p150": 1.5}
CPPTS = {"cpo_m2": -2.0, "cpo_p2": 2.0}
KREG = {}
for tag in list(KPTS) + list(CPPTS):
    smp = f"K_EW_ZHjj_{tag}"; ch = fin(smp)
    if ch and smp in VER and VER[smp]["ok"] > 0:
        d = load(ch); KREG[tag] = dict(d=d, sig=VER[smp]["sigma_used_fb"], k=ZF*BGG, N=d["N"], w=VER[smp]["sigma_used_fb"]*ZF*BGG/d["N"], sample=smp,
                                       ok=VER[smp]["ok"], expected=VER[smp].get("expected"), closure=VER[smp].get("closure"))
if all(t in KREG for t in KPTS):
    # N_MC >= sigma x BR x 3000 for the BSM samples too (fails loudly)
    NCHECK_K = nmc_check({f"K_EW_ZHjj_{t}": dict(sig=v["sig"], k=v["k"], N=v["N"]) for t, v in KREG.items()})
    NCHECK.update(NCHECK_K)
    def sr_mask(d, c=OPT):
        pre, lg, jb, vbs, win, wide = masks(d, c); return pre & lg & jb & vbs & win
    OBS = {"mllgg": ("m_llgg", np.array([100., 300., 400., 500., 650., 850., 1200., 1e5])),
           "ptgg": ("pT_gg", np.array([0., 60., 100., 150., 220., 320., 500., 1e5]))}
    # background templates per observable bin (events at 1 fb^-1): window yield x bin fractions (all cuts except window,
    # wide m_gg; resonant processes: window; fall back to dropping the VBS cuts if < 10 raw events)
    def bkg_templates(var, edges, sigdef="a"):
        out = []
        for sid, r in REG.items():
            if r.get("missing") or r["role"] == "sig" or (sigdef == "b" and r["role"] == "qcdzh"): continue
            y, e, *_ = estimate(sid, OPT); gc = genmjj_corr(sid, OPT); y *= SCALE.get(sid, 1.0)*gc[0]; e *= SCALE.get(sid, 1.0)*gc[0]
            d = AUX[sid]["d"] if sid in AUX else DATA[sid]
            pre, lg, jb, vbs, win, wide = masks(d, OPT)
            for m in ((pre & lg & jb & vbs & (win if r["kind"] == "res" else wide)), (pre & lg & jb & (win if r["kind"] == "res" else wide)), (pre & lg & jb), pre):
                if m.sum() >= 10: break
            h = np.histogram(d[var][m], bins=edges)[0].astype(float); fr = h/m.sum() if m.sum() > 0 else np.full(len(h), 1/len(h))   # fraction of ALL selected events (clipping-safe)
            gr = dict(NUIS[sid]); gr.update({f"genmjj_{sid}": gc[1]} if sid in AUX else {})
            out.append(dict(id=sid, role=r["role"], nu=y*fr, syst=(0.5 if r["syst"] == "fake" else 0.10), mc=min(e/y if y > 0 else 1.0, 1.0), groups=gr))
        return out
    def sig_hist(tag, var, edges):
        d = KREG[tag]["d"]; m = sr_mask(d); return np.histogram(d[var][m], bins=edges)[0]*KREG[tag]["w"], np.histogram(d[var][m], bins=edges)[0]
    def morph_fit(var, edges, pts, cov=False):
        lam = np.array([KPTS[t] for t in pts]); Y = np.array([sig_hist(t, var, edges)[0] for t in pts]); N = np.array([sig_hist(t, var, edges)[1] for t in pts])
        A = np.vstack([np.ones_like(lam), lam, lam**2]).T; coef = []; wp = np.array([KREG[t]["w"] for t in pts])
        for j in range(Y.shape[1]):
            wgt = 1/(np.sqrt(np.maximum(N[:, j], 1))*wp)
            Aw = A*wgt[:, None]; coef.append((np.linalg.lstsq(Aw, Y[:, j]*wgt, rcond=None)[0], np.linalg.inv(Aw.T @ Aw)))
        if cov: return np.array([c for c, _ in coef]), [v for _, v in coef]
        return np.array([c for c, _ in coef])   # (nbins, 3): s_bin(lambda) = c0 + c1 lambda + c2 lambda^2 at kZ = 1 (per fb^-1)
    # closure tests
    CLO = {}
    for var, (lab, edges) in OBS.items():
        allp = list(KPTS); co = morph_fit(var, edges, allp)
        for t in ("lam_m100", "lam_p150", "lam_p000"):
            c1, cv = morph_fit(var, edges, [p for p in allp if p != t], cov=True); lam = KPTS[t]; x = np.array([1, lam, lam**2])
            pred = c1 @ x; y, n = sig_hist(t, var, edges); vpred = np.array([x @ v @ x for v in cv])
            CLO[f"{var}|leave-out {t}"] = dict(pred_total=float(pred.sum()), direct_total=float(y.sum()), ratio=float(pred.sum()/y.sum()),
                                               direct_rel_mcstat=float(1/np.sqrt(max(n.sum(), 1))), chi2=float(((pred - y)**2/((np.maximum(n, 1))*KREG[t]["w"]**2 + vpred)).sum()), nbins=len(y))
    ysm = estimate("S_EW_ZHjj", OPT)[0]; ysm_k = sig_hist("lam_p100", "mllgg", OBS["mllgg"][1])[0].sum()
    CLO["HC lambda=1 vs SM Tier-1 signal (full selection, per fb^-1)"] = dict(HC=float(ysm_k), SM=float(ysm), ratio=float(ysm_k/ysm),
        rel_mcstat=float(np.hypot(1/np.sqrt(max(sig_hist("lam_p100", "mllgg", OBS["mllgg"][1])[1].sum(), 1)), 1/np.sqrt(max(RESULTS["500_a"]["comp"]["S_EW_ZHjj"]["raw_win"], 1)))))
    # kappa_gamma (resolved) for the BR variant: YR4 kappa framework at 125.09 GeV, kt = 1
    def br_scale(kZ, kW):
        kg2 = 1.59*kW**2 + 0.07 - 0.67*kW; G = 0.2152*kW**2 + 0.02641*kZ**2 + (1 - 0.2152 - 0.02641 - 0.00227) + 0.00227*kg2
        return kg2/G
    def make_nll(var, edges, L, sigdef="a", br_mode="fixed", clip=None, cp=False):
        B = bkg_templates(var, edges, sigdef); co = morph_fit(var, edges, list(KPTS))
        if cp:
            y0 = sig_hist("lam_p100", var, edges)[0]; yp = sig_hist("cpo_p2", var, edges)[0]; ym = sig_hist("cpo_m2", var, edges)[0]
            cq = np.vstack([y0, (yp - ym)/4.0, (yp + ym - 2*y0)/8.0]).T   # s(cA) = y0 + b cA + c cA^2 from cA = 0, +-2
        qcd = None
        if sigdef == "b":
            dq = DATA["H_QCD_ZHjj"]; mq = sr_mask(dq); qcd = np.histogram(dq[var][mq], bins=edges)[0]*REG["H_QCD_ZHjj"]["w_evt_fb"]
        keep = np.ones(len(edges) - 1, bool) if clip is None else (edges[1:] <= clip)
        GL = sorted({g for t in B for g in t["groups"]} | set(NUIS["S_EW_ZHjj"]) | set(NUIS["H_QCD_ZHjj"]))
        nbk = len(B)
        def expected(par, theta):
            th = dict(zip(GL, theta[nbk:]))
            mod = lambda grp: np.exp(sum(np.log(1 + v)*th[g] if g != "ggzh_norm" else v*th[g] for g, v in grp.items()))
            if cp: s = (cq @ np.array([1, par[0], par[0]**2]))
            else:
                kZ, lam = par; s = kZ**2*(co @ np.array([1, lam, lam**2]))
                if br_mode == "resolved": s = s*br_scale(kZ, lam*kZ)
            lamv = L*s*mod(NUIS["S_EW_ZHjj"])
            if qcd is not None: lamv = lamv + L*qcd*(par[0]**2 if not cp else 1.0)*mod(NUIS["H_QCD_ZHjj"])
            for i, t in enumerate(B):
                sg = np.sqrt(np.log(1 + t["syst"]**2 + t["mc"]**2)); lamv = lamv + L*t["nu"]*mod(t["groups"])*np.exp(sg*theta[i])
            return np.maximum(lamv[keep], 1e-12)
        ntheta = nbk + len(GL)
        asimov = expected((0.0,) if cp else (1.0, 1.0), np.zeros(ntheta))
        def nll(par, prof=True):
            f = lambda th: (expected(par, th) - asimov*np.log(expected(par, th))).sum() + 0.5*np.dot(th, th)
            if not prof: return f(np.zeros(ntheta))
            return optimize.minimize(f, np.zeros(ntheta), method="L-BFGS-B").fun
        n0 = nll((0.0,) if cp else (1.0, 1.0))
        return (lambda par, prof=True: 2*(nll(par, prof) - n0)), co
    # choose the observable by expected sensitivity to lambda = -1 (3000 fb^-1, def. a, profiled)
    SENS = {}
    for var in OBS:
        q, _ = make_nll(var, OBS[var][1], 3000.); SENS[var] = q((1.0, -1.0))
    VAR = max(SENS, key=SENS.get); EDG = OBS[VAR][1]
    LAMS = np.round(np.arange(-2.0, 2.0001, 0.05), 3); KZS = np.round(np.arange(0.0, 2.5001, 0.1), 3)
    def interval(xs, qs, thr):
        ok = xs[qs <= thr]; return [float(ok.min()), float(ok.max())] if len(ok) else None
    def intervals_disjoint(xs, qs, thr):
        segs, cur = [], None
        for x, qq in zip(xs, qs):
            if qq <= thr: cur = [x, x] if cur is None else [cur[0], x]
            elif cur is not None: segs.append(cur); cur = None
        if cur is not None: segs.append(cur)
        return [[float(a), float(b)] for a, b in segs]
    for L in (500., 1000., 3000.):
        for brm in ("fixed", "resolved"):
            q, co = make_nll(VAR, EDG, L, br_mode=brm)
            qs = np.array([q((1.0, l)) for l in LAMS])
            qneg = min(qs[LAMS < 0]);
            CPL[f"lambda|{int(L)}|{brm}"] = dict(lam=LAMS.tolist(), q=qs.tolist(), int68=intervals_disjoint(LAMS, qs, 1.0), int95=intervals_disjoint(LAMS, qs, 3.84),
                                                 Z_excl_lambda_neg=float(np.sqrt(max(qneg, 0))), q_lambda_m1=float(qs[np.argmin(abs(LAMS + 1))]),
                                                 Z_excl_lambda_m1=float(np.sqrt(max(qs[np.argmin(abs(LAMS + 1))], 0))), lambda_at_min_q_neg=float(LAMS[LAMS < 0][np.argmin(qs[LAMS < 0])]))
        if L in (500., 3000.):
            q, co = make_nll(VAR, EDG, L)
            Q2 = np.array([[q((kz, l)) for l in LAMS[::2]] for kz in KZS])
            CPL[f"2d|{int(L)}"] = dict(kZ=KZS.tolist(), lam=LAMS[::2].tolist(), q=Q2.tolist(), profiled=True)
        # kappa_Z alone (lambda = 1)
        q, co = make_nll(VAR, EDG, L); ks = np.round(np.arange(0.0, 3.0001, 0.05), 3); qk = np.array([q((k, 1.0)) for k in ks])
        CPL[f"kappaZ|{int(L)}"] = dict(kZ=ks.tolist(), q=qk.tolist(), int68=intervals_disjoint(ks, qk, 1.0), int95=intervals_disjoint(ks, qk, 3.84))
        # definition (b): QCD ZHjj also scales with kZ^2
        q, co = make_nll(VAR, EDG, L, sigdef="b"); qs = np.array([q((1.0, l)) for l in LAMS])
        CPL[f"lambda_defb|{int(L)}"] = dict(lam=LAMS.tolist(), q=qs.tolist(), int68=intervals_disjoint(LAMS, qs, 1.0), int95=intervals_disjoint(LAMS, qs, 3.84),
                                            Z_excl_lambda_neg=float(np.sqrt(max(min(qs[LAMS < 0]), 0))))
    # CP-odd c_A (Lambda = 1 TeV), linear + quadratic, with and without energy clipping
    if all(t in KREG for t in CPPTS):
        CAS = np.round(np.arange(-4, 4.0001, 0.1), 2)
        for L in (500., 1000., 3000.):
            for clip in (None, 500.):
                cv = "mllgg"; ed = OBS[cv][1] if clip is None else np.array([e for e in OBS[cv][1] if e <= clip] + ([clip] if clip not in OBS[cv][1] else []))
                q, _ = make_nll(cv, ed, L, cp=True, clip=None)
                qs = np.array([q((c,)) for c in CAS])
                CPL[f"cA|{int(L)}|{'clip500' if clip else 'noclip'}"] = dict(cA=CAS.tolist(), q=qs.tolist(), int68=intervals_disjoint(CAS, qs, 1.0), int95=intervals_disjoint(CAS, qs, 3.84))
        y0 = sig_hist("lam_p100", "mllgg", OBS["mllgg"][1])[0].sum(); yp = sig_hist("cpo_p2", "mllgg", OBS["mllgg"][1])[0].sum(); ym = sig_hist("cpo_m2", "mllgg", OBS["mllgg"][1])[0].sum()
        CPL["cA_rates"] = dict(s0=float(y0), s_p2=float(yp), s_m2=float(ym), linear_over_quad=float(abs(yp - ym)/max(abs(yp + ym - 2*y0), 1e-12)))
    CPL["choice"] = dict(observable=VAR, q_lambda_m1_3000=SENS, edges=EDG.tolist())
    CPL["closure"] = CLO
    CPL["points"] = {t: dict(sample=v["sample"], sigma_fb=v["sig"], N=v["N"], jobs_ok=v["ok"], sigma_closure=v["closure"],
                             s_SR_500=float(sr_mask(v["d"]).sum()*v["w"]*500), raw_SR=int(sr_mask(v["d"]).sum())) for t, v in KREG.items()}
    CPL["morph_total_coef_per_fb"] = morph_fit(VAR, EDG, list(KPTS)).sum(0).tolist()
    print("coupling: observable", VAR, {k: v.get("int95") for k, v in CPL.items() if k.startswith("lambda|")})
else:
    CPL["status"] = "coupling samples not yet available: " + ", ".join(t for t in KPTS if t not in KREG)
