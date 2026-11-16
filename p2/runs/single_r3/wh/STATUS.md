# WH single_r3 STATUS (G1), 2026-11-09T00:20Z
- Done: Phase 01 PASS (decisions open); Phase 02 ledger PASS; Phase 03 PARTIAL (16/18 test jobs OK); G1 self-review written.
- Running: condor 899736.14/15 (QCD Waajj gridpacks + twin), test jobs 899737.14/15 held until those exist (auto-release).
- Signal: σ(EW W±Hjj, W→eν/μν) = 13.79 fb → σ·WF·B_γγ = 0.0301 fb (15 ev / 500 fb⁻¹ before acceptance); B0 window 1.10 ev (validation).
- Blockers (sev-1): D-WH-3 lepton-FSR gap in Wγγ (×2.02); D-WH-4 Delphes e→γ; D-WH-6 W+jets N policy; Phase 03 incomplete.
- Decisions needed:
  D-WH-1 flavour scheme: signal without external b; b-complement (tHq-like) as background [recommended] | 5F signal
  D-WH-2 W normalisation: WF=0.9601 on chain σ, ±1% lineshape, +1.8% LU alt. [recommended] | σ_prod×B_PDG
  D-WH-3 Wγγ lepton radiation: (iii) off-shell lνaajj for QCD + proxy factor for EW [recommended] | (i) both off-shell | (ii) factor only
  D-WH-4 e→γ: parametrised f_e→γ {1,2,5}% + m(eγ) Z-veto + MT cut [recommended] | Delphes intrinsic
  D-WH-5 photon pT ≥ 25 GeV in the analysis (as ZH) [recommended] | regenerate with pta>20
  D-WH-6 W+jets (and ggF H+jj, tt̄ 2-fake): fake-factor weighting on VBS-biased samples with N_eff≥10 exception to SPEC §1.5 [recommended] | direct N (infeasible)
  D-WH-7 QCD WHjj: fixed-order (2,2) as ZH [recommended] | MLM WH+0–2j
  D-WH-8 forward the ZH ledger W-rescale observation (WF²=0.922 missing on MG5 top-W's) as ZH erratum? yes/no
  D-WH-9 commit this run directory on main? yes/no
- Next: on answers, re-verify 899736/7.14/15 and close Phase 03; single arm stops at G1 (no production).
