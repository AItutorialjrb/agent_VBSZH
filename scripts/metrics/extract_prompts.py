#!/usr/bin/env python3
"""C (2026-11-03): every human prompt of the ZH project -> metrics/prompts/ZH/NN_<utc>_<agent>.md + index.csv.
Sources (read-only backups): metrics/raw/claude/*.jsonl (Claude Code), metrics/raw/codex/rollout-*.jsonl (Codex, user
messages excluding the injected AGENTS.md block). Labels (task / decision / corrective-intervention, several allowed;
'interrupt' and 'compaction' for control events) are assigned by hand below, keyed by UTC minute, with the reason.
Usage: python3 -P scripts/metrics/extract_prompts.py"""
import json, glob, os, re, csv
P = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); OUT = f"{P}/metrics/prompts/ZH"
LAB = {  # utc minute -> (labels, classes for corrective items, note)
 "2026-11-02T12:16": ("task", "", "Codex: execute Phase 00"),
 "2026-11-02T12:24": ("task;decision", "", "Codex: continue to Phase 01; new mandatory storage policy (constraint set by human)"),
 "2026-11-02T13:29": ("task", "", "Claude handoff: continue study under handoff rules"),
 "2026-11-02T14:20": ("corrective-intervention;decision;task", "statistics;storage/resources", "Stop bulk plan; require N>=max(50k, sigma*L), filters/fake factors for infeasible samples, MC-stat adequacy, slim Delphes, CPU re-plan"),
 "2026-11-02T15:15": ("compaction", "", "/compact (manual)"),
 "2026-11-02T15:17": ("decision;task", "", "Approve D-S1, D10 (git), D11 policy; submit tier1/gridpacks/test; write Phase 05 pilot"),
 "2026-11-02T16:02": ("compaction", "", "/compact (manual)"),
 "2026-11-02T16:07": ("decision;task;corrective-intervention", "background model", "FINAL RUN: Delphes-level only, no proxy/parton-level estimates in final yields (Phase 05 used proxies)"),
 "2026-11-03T11:25": ("corrective-intervention;task", "statistics;normalisation;background model;other", "Physics completion: scan-boundary optimum, missing theory unc., interference, off-shell, undocumented 0.9783 factor, detector, ggZH"),
 "2026-11-03T11:27": ("interrupt", "", "[Request interrupted by user] then /compact"),
 "2026-11-03T11:29": ("corrective-intervention;decision;task", "constraint violation not flagged;statistics", "Adds A9/A10: ttgamma/tWgamma 2000 events each violate N>=sigma*L (3000 fb-1), not flagged; approves cleanupPeriodDays"),
 "2026-11-03T11:34": ("interrupt", "", "[Request interrupted by user for tool use] (rejected login-node analysis run); '\\compact' typed"),
 "2026-11-03T14:01": ("decision;task;corrective-intervention", "background model;other", "Closeout: option A for ttgamma/tWgamma conditional on a cut-flow cross-check vs the reference; C statistics; explicit limitations; comparison with CMS/ATLAS; tag zh-final-v1.1"),
 "2026-11-03T11:37": ("corrective-intervention;task", "missing deliverable;scope", "Adds E: VH coupling (lambda_WZ) interpretation, planned (FINAL_report outlook) but absent until requested"),
}
def clean(t): return t.replace('<pasted_content id="90a1">', "").replace('</pasted_content id="90a1">', "").strip()
rows = []; EV = []
for f in sorted(glob.glob(f"{P}/metrics/raw/codex/rollout-*.jsonl")):
    for l in open(f):
        d = json.loads(l); p = d.get("payload", {})
        if d.get("type") == "response_item" and p.get("type") == "message" and p.get("role") == "user":
            t = " ".join(x.get("text", "") for x in p.get("content", []) if isinstance(x, dict))
            if t.lstrip().startswith("# AGENTS.md instructions"): continue
            rows.append(("codex", d["timestamp"], os.path.basename(f), t))
for f in sorted(glob.glob(f"{P}/metrics/raw/claude/*.jsonl")):
    for l in open(f):
        d = json.loads(l)
        if d.get("type") != "user" or d.get("isMeta") or d.get("isCompactSummary"): continue
        c = d["message"]["content"]
        if not isinstance(c, str):   # interrupt markers: index.csv only (no prompt text)
            t = " ".join(x.get("text", "") for x in c if isinstance(x, dict) and x.get("type") == "text")
            if t.startswith("[Request interrupted"): EV.append(("claude", d["timestamp"], d.get("sessionId", ""), t))
            continue
        if c.startswith("<local-command-stdout>") or c.startswith("<command-name>") or c.startswith("<task-notification>"): continue
        rows.append(("claude", d["timestamp"], d.get("sessionId", ""), c))
rows.sort(key=lambda r: r[1]); os.makedirs(OUT, exist_ok=True)
with open(f"{OUT}/index.csv", "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["n", "utc", "agent", "session", "labels", "corrective_classes", "chars", "file", "note"])
    for i, (ag, ts, sess, t) in enumerate(rows, 1):
        lab, cls, note = LAB.get(ts[:16], ("UNLABELLED", "", ""))
        if t.strip() in ("/compact", "\\compact"): lab, cls, note = "compaction", "", "manual compaction command" + (" (typed with a backslash: not executed as a command)" if t.strip() != "/compact" else "")
        fn = f"{i:02d}_{ts[:19].replace(':', '')}Z_{ag}.md"
        open(f"{OUT}/{fn}", "w").write(f"<!-- utc={ts} agent={ag} session={sess} labels={lab} classes={cls} -->\n# Prompt {i} ({ag}, {ts[:19]}Z)\n\n**Labels:** {lab}" + (f" — classes: {cls}" if cls else "") + f"\n\n**Note:** {note}\n\n---\n\n" + clean(t) + "\n")
        w.writerow([i, ts, ag, sess, lab, cls, len(t), fn, note])
    for j, (ag, ts, sess, t) in enumerate(EV, 1): w.writerow([f"i{j}", ts, ag, sess, "interrupt", "", len(t), "", t.strip()])
print(f"{len(rows)} prompts + {len(EV)} interrupts -> {OUT}", "| unlabelled:", sum(1 for r in rows if r[1][:16] not in LAB))
