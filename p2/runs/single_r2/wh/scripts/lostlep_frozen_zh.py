#!/usr/bin/env python3
"""Phase-02 relevance estimate (NOT a final yield): frozen ZH Delphes samples (read-only, zh-final-v1.1 production) passed through
the same ILLUSTRATIVE WH smoke selection as scripts/validate_delphes_wh.py (>=2 photons, ==1 lepton pT>15 with lead pT>25, MET>30,
>=2 jets, b-veto, mjj>500 & |deta|>2.5, 120<mgg<130).  Normalisation: sigma (ZH FINAL_report §2) x k (ZH BR ledger) x L / N_used.
Usage: python3 -P lostlep_frozen_zh.py <out.json> [nfiles_max]"""
import sys, glob, json, math
import numpy as np, uproot, awkward as ak
ZH = "/eos/home-r/rjiang/vbs_zh_codex_starter/production"
ZF, BGG = 0.9783, 0.002270
# sigma [fb] and k from ZH FINAL_report.md §2/§3 (frozen); offcorr = ZH off-shell/FSR factor for on-shell-Z Zaajj (1.128)
SAMPLES = {"S_EW_ZHjj": (f"{ZH}/v1/ew_zhjj_zll/*_s*[0-9].root", 1.295, ZF*BGG, 1.0),
           "H_QCD_ZHjj": (f"{ZH}/v1/qcd_zhjj_zll/*_s*[0-9].root", 10.21, ZF*BGG, 1.0),
           "B_QCD_Zaajj_vbs": (f"{ZH}/final/B_QCD_zaajj_vbs/*_s*[0-9].root", 0.0356, ZF, 1.128),
           "B_EW_Zaajj_vbs_is2": (f"{ZH}/final/B_EW_zaajj_vbs_is2/*_s*[0-9].root", 0.01575, ZF, 1.128)}
NMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 40
BR = ["Photon.PT", "Photon.Eta", "Photon.Phi", "Electron.PT", "Electron.Eta", "Muon.PT", "Muon.Eta",
      "Jet.PT", "Jet.Eta", "Jet.Phi", "Jet.Mass", "Jet.BTag", "MissingET.MET"]
def sel(O):
    g = O[["Photon.PT", "Photon.Eta", "Photon.Phi"]]
    gm = (O["Photon.PT"] > 20) & (abs(O["Photon.Eta"]) < 2.5) & ~((abs(O["Photon.Eta"]) > 1.4442) & (abs(O["Photon.Eta"]) < 1.566))
    gpt, geta, gphi = O["Photon.PT"][gm], O["Photon.Eta"][gm], O["Photon.Phi"][gm]
    ng = ak.num(gpt)
    le = (O["Electron.PT"] > 15) & (abs(O["Electron.Eta"]) < 2.5); lm = (O["Muon.PT"] > 15) & (abs(O["Muon.Eta"]) < 2.5)
    nl = ak.sum(le, axis=1) + ak.sum(lm, axis=1)
    lead = ak.fill_none(ak.max(ak.concatenate([O["Electron.PT"][le], O["Muon.PT"][lm]], axis=1), axis=1), 0)
    jm = (O["Jet.PT"] > 25) & (abs(O["Jet.Eta"]) < 4.7)
    jpt, jeta, jphi, jms, jb = (O[k][jm] for k in ("Jet.PT", "Jet.Eta", "Jet.Phi", "Jet.Mass", "Jet.BTag"))
    nj = ak.num(jpt); nb = ak.sum(jb[abs(jeta) < 2.5] > 0, axis=1)
    met = ak.firsts(O["MissingET.MET"])
    def p4(pt, eta, phi, m, k):
        pt, eta, phi, m = (ak.fill_none(ak.pad_none(x, 2)[:, k], 0.0) for x in (pt, eta, phi, m))
        return pt*np.cos(phi), pt*np.sin(phi), pt*np.sinh(eta), np.sqrt((pt*np.cosh(eta))**2 + m**2)
    def mass(a, b):
        px, py, pz, e = (a[i] + b[i] for i in range(4)); return np.sqrt(np.maximum(e**2 - px**2 - py**2 - pz**2, 0))
    z0 = ak.zeros_like(gpt)
    mgg = mass(p4(gpt, geta, gphi, z0, 0), p4(gpt, geta, gphi, z0, 1))
    mjj = mass(p4(jpt, jeta, jphi, jms, 0), p4(jpt, jeta, jphi, jms, 1))
    deta = abs(ak.fill_none(ak.pad_none(jeta, 2)[:, 0], 0) - ak.fill_none(ak.pad_none(jeta, 2)[:, 1], 0))
    steps = [(">=2 photons", ng >= 2), ("+ ==1 lepton", nl == 1), ("+ lead lepton pT>25", lead > 25), ("+ MET>30", met > 30),
             ("+ >=2 jets", nj >= 2), ("+ b-veto", nb == 0), ("+ mjj>500,|deta|>2.5", (mjj > 500) & (deta > 2.5)),
             ("+ 120<mgg<130", (mgg > 120) & (mgg < 130))]
    return [(n, ak.to_numpy(m)) for n, m in steps]
res = {}
for sid, (pat, sig, k, oc) in SAMPLES.items():
    files = sorted(glob.glob(pat))[:NMAX]
    if not files: res[sid] = dict(error="no files", pattern=pat); continue
    cnt = None; N = 0
    for f in files:
        O = uproot.open(f)["Delphes"].arrays(BR, library="ak"); N += len(O)
        st = sel(O); cum = np.ones(len(O), bool); c = []
        for n, m in st: cum = cum & m; c.append(int(cum.sum()))
        cnt = c if cnt is None else [a + b for a, b in zip(cnt, c)]
    names = [n for n, _ in sel(uproot.open(files[0])["Delphes"].arrays(BR, library="ak", entry_stop=10))]
    wev = sig*k*oc*500.0/N
    res[sid] = dict(files_used=len(files), files_available=len(glob.glob(pat)), N_used=N, sigma_fb=sig, k=k, offshell_corr=oc,
                    events_500_before_cuts=sig*k*oc*500.0, w_evt_500=wev,
                    cutflow=[dict(step=n, n_raw=c, yield_500=c*wev, err_500=math.sqrt(c)*wev, ul95_500_if_zero=3.0*wev if c == 0 else None)
                             for n, c in zip(names, cnt)])
    print(sid, N, [(n, c) for n, c in zip(names, cnt)][-4:], "w_evt", wev)
json.dump(res, open(sys.argv[1], "w"), indent=1)
