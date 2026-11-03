# Brief — executor-wh, multi_r1, pre-G2 and Phase 04+ (orchestrator, G1 decision D19)
Read this brief, not the full handoff. Binding sources, in order: p2/SPEC.md §1 and §6 (decision log), this brief, reviews/wh_01-03.md.
Your directory: p2/runs/multi_r1/wh/. Shared canonical samples: p2/production/wh/<sample>/ (create it). Never write elsewhere.
ZH tree, p2/lib and software/ are read-only. Never `rm` anything outside your directory. New installs only under p2/software/.

## 0. Rules that stay binding (SPEC §1)
- N_MC ≥ max(50k, σ×BR×3000 fb⁻¹) per sample entering s or b, enforced by nmc_check (fails loudly). The only exceptions are
  the G1 decisions below (biased + weighted samples with N_eff ≥ 10 in the SR; twin-corrected samples), each logged as
  a deviation in your report and STATUS.
- BR applied exactly once (BR ledger, WF = 0.9601 for MG5-decayed W). Final yields at Delphes level only.
- HTCondor: a successful test job first; check for duplicates before submitting; stage out to EOS.
- **No bulk production before G2.** Allowed now: gridpacks, test jobs, twin samples and pilot samples at validation size
  (≤ 100k events per sample unless a twin test statistically needs more; state why).
- Seeds (SPEC §3.4, G1 revision): seed = 2 000 000 + 100 000×1 + 1000×sample_idx + J. Write the seeds already used,
  config/seeds_used_preG1.txt (old formula, kept, unchanged), and make the uniqueness assertion cover them.

## 1. Human decisions at G1 (verbatim in SPEC §6). Implement them.
- D-WH-0 Accepted (light-flavour signal). The top-resonant b class (tHq/tHW-like) is a resonant background. Check that
  it is in the sample matrix (H_tHq/H_tHW or equivalent) and say so in 02.
- D-WH-1 Seeds as above. Record the mapping old→new in config/ and 03.
- D-WH-2 W+jets (double fake) and tt̄ 1ℓ: VBS-biased samples with fake-factor (probability) weighting using the Delphes
  j→γ rate, N_eff ≥ 10 in the SR. Only biasing cuts shown safe by a twin test (loss ≤ 5 % within stat at reco SR).
- D-WH-3 Top up ggZH, ttH dilep and ZH→ττ to ≥ 50k as NEW samples under p2/production/wh/. Never modify ZH files.
  Pre-G2: cards + one test job each; bulk after G2.
- D-WH-4 f_lepton: a parametrised range from published CMS tight-ID lepton fake rates (cite paper and table). Report
  both ends. Relabel the non-prompt "UPPER-BOUND" as an estimate (review 6).
- D-WH-5 WZγ/WWγ/ZZγ (e→γ, lost-lepton): dedicated samples, batch generation with `group_subprocesses False`, after
  one successful test job. Pre-G2: gridpack + test job.
- D-WH-6 B_EW_Waajj_vbs gridpack 884456.3: wait; no condor_rm. When it finishes, release 884457.3.
- Twin result (D8): **no generator mjj cut on QCD-type samples.** Nominal = no-mjj samples, or a looser cut shown safe
  by a twin (≤ 5 % loss within stat at reco SR). If N is infeasible, use the ZH twin-correction method
  (stat + full-difference syst) and log it as a deviation. Also apply this to the frozen ZH QCD-type samples you reuse
  (ZH_Zaajj_QCD lost-lepton, F_*_llajj QCD part). Run EW twins for B_EW_Waajj_vbs / F_EW_Wajj_vbs (reviewer 7b).
  Twin selection = the reco SR baseline (lepton, MET, b-veto, 2γ, VBS jets), not the loose one (review 7c).
- D9 τ (not answered; orchestrator default, to be confirmed at G2): the handoff signal is W→eν/μν, so
  S_EW_WHjj_taunu stays in b (no deviation). Quantify the τ feed-down into the W-decaying backgrounds at reco SR:
  either include τ in the production cards, or use an uplift measured on the τ samples with ±100 % uncertainty. State
  which, per sample.
- D10 (orchestrator default): one condor test job per sample type before G2, including all new types above. Bound
  the tt̄γ/tt̄γγ overlap after the b-veto at reco level, or remove it as in ZH; drop "negligible" (review 4). Fix the
  I_WHjj BR (undecayed W must not get BR_WLL unless a PY8 card forces W→eν/μν; review 9).

## 2. Reviewer conditions (reviews/wh_01-03.md), binding before G2
Items 1–2 (sev-1): keep the loud N flag; restate the lost-lepton yields with the twin-correction/no-mjj rule above.
Items 3–9 as above (3: pilot wording; 5: give a tt̄ two-fake number and the Z→νν H bound; 6: relabel; 7: N_req of
F_QCD_Wajj_nomjj flagged). Items 11–14 (sev-3): fix the text (systematic sign +5 %/−0, t:t̄ 2:1 reasoning, the W⁺/W⁻
bwcutoff closure cause stated as not established, combination nuisance correlation for shared samples defined,
H_ZH_tautau N corrected from the ZH record, interference sign "computed", INDEX status labels, W→ℓνγ caveat).
Item 10 is done by the orchestrator (SPEC §6/§7).

## 3. Deliverable for G2 — `reports/04_production_plan.md` + INDEX update
The G2 reviewer judges this file. For each sample entering s or b, a table row with:
sample | role (s/b class) | σ (fb) and source | BR and k as applied once | generator cuts and twin evidence (loss ± stat, at
reco SR) | N_required | N_planned | weighting (fake factor / twin C) | projected N_eff in SR (from pilot/test job) |
seeds (range) | jobs × events | CPU-h | storage (GB) | status of test job (cluster, exit 0, verified).
Plus: total storage (WH ≤ 200 GB of the 400 GB p2 budget, slim Delphes), total CPU-h, the output of `nmc_check` on
the planned table (it must pass, or name the decision that covers each exception), the list of deviations, and the
condor submission plan (one cluster per sample, no duplicates). Keep Phase 03 report and INDEX labels accurate:
Phase 03 PASS only when every sample type has a verified test job.

## 4. Working protocol
- Verifier: for every new finished test job, gridpack or twin result, write VERIFY_REQUEST.md (paths, cluster IDs,
  expected σ/BR/N) and say so in STATUS. The orchestrator runs the verifier, which reports back to you via the
  orchestrator.
- STATUS.md ≤ 25 lines (done; running clusters; blockers; decisions needed D-WH-N; next action). Your final reply is a
  pointer to STATUS.md only.
- If a new human-level physics decision is needed (not covered here), raise D-WH-10+ in STATUS and stop that branch;
  continue the other work.
- Long waits: do not idle-poll. If only condor jobs remain, set STATUS "waiting on clusters X" and return; you will
  be resumed.
- Prefix the first line of your work log with ROLE=executor-wh PHASE=PRE-G2.
