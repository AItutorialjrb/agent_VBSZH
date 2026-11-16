

## Limitations (D47 (3), also Table T11)
* **ZH input (ZH erratum), 1**: no Z gamma + 3 jets ME row (D43): the corrected fake component may be low; the frozen direct count (+5 % Z at most) is the upper variation
* **ZH input (ZH erratum), 2**: calibration reference mismatch (D39/D43): CMS inclusive in jets vs ZH >= 2 ME partons; kappa 0.5-1 moves Z by < 1 %
* **ZH input (ZH erratum), 3**: other-Higgs, Zgg, top and fake rows are not rescaled under coupling hypotheses
* **ZH input (ZH erratum), 4**: templates: pheff, lepeff, phscale, phres are assumptions (no Delphes scale factors), new relative to the frozen ZH study
* **ZH input (ZH erratum), 5**: per-bin MC errors of the continuum rows use err_bin = sqrt(nu e^2/y) (Poisson-equivalent)
* **calibration mismatch**: the fake-photon calibration reference (CMS, inclusive in jets) differs from the ZH ME definition (>= 2 partons): kappa 0.5-1 moves Z by < 1 % (D39/D43); and the CMS-calibrated fake-factor scale is not re-derived for 13.6 TeV Delphes
* **other Higgs modes not rescaled**: other-Higgs, Z gamma gamma, top and fake rows are NOT rescaled under coupling hypotheses (lambda / kappa scans rescale only the EW ZHjj / WHjj signal rows and the H->gamma gamma BR)
* **no Z gamma + 3 jets ME row in ZH**: the corrected fake-photon component may be low (no Z gamma + 3 jets matrix-element row, D43); the frozen direct count (+5 % in Z at most) is the upper variation
* **lepton misID rate f_mu**: the WH light-hadron lepton misID uses a PLACEHOLDER muon rate f_mu = 2e-5 (= the electron value, D40; no cited value); the D36 x0.3-x3 band covers it (Table T6)
* **D49: QCD lost-lepton one-event estimate**: settled by D50 = option 4: yield 0.121 events, 95 % interval [0.0031, 0.675]; the D42 N_eff >= 10 rule is NOT met for that part; upper end in Table T4c; the v1 vbs x C value is a cross-check
* **VH nuisance ranking not delivered**: vh_run.py rankvh (913470.001) was removed once by SYSTEM_PERIODIC_REMOVE after about 24 h; 913470.000 (WH rank) rc 0; not rerun; Table T5-VH is a placeholder row
* **ZH non-prompt-lepton class**: no MC exists and none will be produced (D50): unestimated and unbounded, NOT negligible (Tables T3-ZH, T6)
* **toys**: mu95 toys reuse the same seeds at every mu point (fit errors understated); the WH/ZH/VH toy sets share seeds; the lambda toys were generated on the pre-W1 stack but the coupling inputs reproduce bit-identically with the current code and the rebuilt workspaces are byte-identical to the committed ones
* **H_ggF_jj**: D38 substitution (scaled VBF-proxy; no ggF H + jets sample)
* **expected-only**: all results are Asimov expectations at Delphes level, 13.6 TeV, LO, no data, assumed photon / lepton scales and resolution (no Delphes scale factors)

D49 is settled by D50 = option 4 (Table T4c shows the central and upper-end result). The VH nuisance ranking is not delivered (T5-VH is a placeholder row). Basis: T4 = joint-workspace code; T4c, T5-WH, T6 = stand-alone WH model.
