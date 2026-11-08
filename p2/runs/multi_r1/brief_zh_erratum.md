# Brief: ZH inheritance check / erratum, multi_r1 (orchestrator, 2026-11-08; human decision D37)

Read this brief, then the binding sources: p2/SPEC.md §6 D4, D34, D35 and D37, and p2/production/wh/FORMAT.md (the corrected rate, the artefact definition, Delphes facts).

## Rules
- The ZH tree is frozen at tag zh-final-v1.1. It is read-only: reports/, cards/, config/, scripts/, work/, production/ and figures/ at the repository root. Never modify, move or create anything there.
- You write only in p2/combination/ (ZH_erratum.md, plus a working subdirectory p2/combination/zh_check/ for scripts, outputs and figures). The orchestrator commits; you do not run git.
- Never touch p2/runs/* (other runs are active), p2/production/, ~/.codex or /eos/home-r/rjiang/.git.
- Anything above about 10 min of CPU goes to condor (schedd bigbird103.cern.ch). Use your own submit files in zh_check/. Pick seeds only if MC generation is needed, and none should be.
- No API tokens in files or logs.

## Questions (D37)
1. **Inheritance.** Did the ZH fake-factor cross-check, or any ZH systematic, use the contaminated j→γ table or code?
   - The contaminated table came from the WH multi_r1 work and was lepton-contaminated: 98.8 % of numerator photons lay within ΔR < 0.2 of the prompt lepton.
   - Trace the ZH code and reports (and p2/lib, a ZH export) for how ZH built its j→γ rate or fake factor.
   - Check whether lepton removal was applied, whether the ZH rate used electron-induced photon objects, and whether any WH table entered ZH. Cite file:line.
2. **Artefact.** Do the ZH direct-count fake photons contain the Delphes energy-flow artefact? That is a reco photon of 27–49 GeV whose referenced gen particles carry only ~0.05–0.4 GeV, and no gen photon of pT > 10 within ΔR < 0.1. Quantify the fraction on the frozen ZH samples, using GenTruth or Particle where available.
3. **Re-evaluation with the H1 method (D34).** Compute the ZH fake-photon component with the fake-factor method using a lepton-decontaminated per-jet rate from genuine in-jet photons only, with the artefact excluded.
   - Build the rate on the ZH samples in the same way as WH: the same definitions, stated explicitly, and a disjoint-split closure.
   - Apply the same CMS calibration and systematic as the WH executor. Cite the same record; the orchestrator relays the WH choice, or you choose it and state it.
   - Give the direct count as the upper variation.
4. **Impact.** Report the change in ZH b, Z and μ95 at 500, 1000 and 3000 fb⁻¹, using the frozen ZH statistical method and code read-only, reproduced first to the frozen numbers as a closure check.

## Deliverable: p2/combination/ZH_erratum.md
It contains:
- date and status;
- answers 1–4 with evidence (file:line, numbers, raw counts, MC uncertainties);
- a table of frozen against corrected values for b per class, total b, Z and μ95;
- the reproduction closure;
- caveats;
- a machine-readable p2/combination/zh_check/zh_corrected_inputs.json for the VH combination (the same structure as the frozen ZH inputs, with a flag saying whether anything changed).

If a human-level decision is needed, put it at the top of ZH_erratum.md under "DECISION NEEDED", stop that branch, and finish the rest. Then write p2/combination/zh_check/VERIFY_REQUEST.md and reply with a pointer to ZH_erratum.md only.
First line of your work log: ROLE=executor-zh-erratum PHASE=FINAL.
