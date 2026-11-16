# G4(a) blind G1 audit rubric (fixed; identical for all six reports)

Fixed by the multi_r1 orchestrator on 2026-11-15, before any audit ran (D48 (a)).

## Object
One file `report_<X>.md`: the WH Phase 01–03 reports (01 signal definition, 02 background matrix and overlap, 03 generator smoke tests and cross-section consistency) of one analysis, in the state at which that analysis reached its G1 gate.
- Arm and run identifiers are stripped. Seed run indices are masked as `x`. Paths, model names and role names are replaced by placeholders (RUNDIR, MODEL, analyst, check).
- Do not try to identify the analysis.

## Reference documents (the same for all six)
- `PROJECT_BRIEF.md` and `AGENTS.md` at the repository root (/eos/home-r/rjiang/vbs_zh_codex_starter/).
- `p2/SPEC_G0.md`, the common pre-registered SPEC for Phase 01–03.

Read ONLY these and your one report file. Do not open any other file in the repository, including run directories, metrics, reviews and other report_*.md files. Do not run code.

## Severity-1 physics issue: definition
A severity-1 issue is a physics or methodology defect that, if not fixed, would make a downstream result (σ×BR, a yield, a background estimate, a significance or a coupling statement) wrong by more than about 30 %, invalid, or not supported. It can also be a defect that violates a binding project rule in AGENTS.md or SPEC_G0. Examples of the classes:
1. **Signal definition:** wrong or non-gauge-invariant process or orders; a wrong W/H decay treatment; BR applied twice or not at all; a tree-level h>aa used; a missing lepton flavour or charge.
2. **Cross-section bookkeeping:** σ before decay, after decay and after cuts confused; unit or normalisation errors; an unvalidated generator syntax used as production-ready.
3. **Background matrix:** a relevant background class missing or not bounded (prompt, non-prompt/fake, e→γ, lost lepton, other Higgs, top); an unaudited overlap or double counting (for example Vγ vs Vγγ, ttγ vs ttγγ); a nominal 0 from missing MC claimed as negligible.
4. **Generator cuts:** a generator-level cut shown or likely to bias the SR, used without a safety demonstration.
5. **Validation:** cross-section, BR or decay-flag closure missing or failing without being flagged; a sample claimed validated without the evidence the report itself describes.
6. **Claims:** numbers or conclusions not supported by the evidence shown, or results presented as data-driven or validated when they are not.

Not severity-1: presentation, typos, missing nice-to-have plots, and items that are correctly flagged as open or blocked with a stated plan or decision request.

## Resolved vs unresolved
An issue counts as **unresolved** if the report, in its own text, neither fixes it nor states it clearly as open, blocked or a pending decision, with the impact stated. An issue the report itself flags as open with its impact is **flagged-open**. Count it separately; it is not unresolved.

## Output (exactly this format, ≤ 60 lines)
```
REPORT: <X>
N_SEV1_UNRESOLVED: <integer>
N_SEV1_FLAGGED_OPEN: <integer>
UNRESOLVED:
1. [class 1-6] <one-line statement> — evidence: <section/line quote, ≤ 20 words> — why ≥30 % / invalid: <one line>
...
FLAGGED_OPEN:
1. [class] <one line>
...
NOTES: <≤ 3 lines; anything that limited the audit>
```
Be conservative. Count an issue only if you can point to the text that shows it. Merge duplicates: one root cause is one issue.
