# Isolation / permission enforcement record (multi_r1 orchestrator, 2026-11-03 UTC)

Claude Code 2.1.316. Syntax verified against https://code.claude.com/docs/en/permissions (fetched 2026-11-03):
`//abs/path/**` = absolute gitignore-style path; Read deny also blocks Edit/Write on the same path; Edit deny covers built-in
edit tools, recognised Bash file commands (cat/head/tail/sed/tee) and redirection targets; project rules live in
`<primary working dir>/.claude/settings.json`. Each run has its own `runs/<run>/.claude/settings.json` (deny list).

## Enforced (tested in multi_r1 session unless noted)
| Rule | Test | Result |
|---|---|---|
| Read deny on other runs' dirs (`Read(//…/p2/runs/<other>/**)`) via Read tool | Read multi_r2/.claude/agents/verifier.md | BLOCKED |
| same, via Bash `cat` | `cat …/multi_r2/…` | BLOCKED |
| same, via Bash `grep -r <dir>` naming the dir | grep -rc … multi_r2/… | BLOCKED |
| Settings hot-reload (rules written mid-session) | above tests, written after session start | applied without restart |
| Edit deny on ZH frozen dirs, p2/lib, handoff, root metrics/, software/, /eos/home-r/rjiang/.git | rule present; p2/lib additionally `chmod -R a-w` (OS-level) | rule present (not exercised destructively) |
| Bash deny: git push --force/-f, reset --hard, tag -d, push --delete, codex | rule present | not exercised |
| single arm: bare `Agent` deny (removes subagent tool = "no subagents") | rule present in single_r*/settings.json | to be verified at single-run start |

## NOT enforceable / not enforced (logged per handoff §1, §2.2)
1. **Indirect reads/writes bypass deny rules**: `python3 -c "open('…/multi_r2/…')"` succeeded (514 bytes). Per docs, rules do not cover
   subprocesses that open files themselves or `grep -r` run from a parent directory without naming the path. OS-level
   enforcement would need the Claude Code sandbox (not enabled; would also restrict EOS/condor/CVMFS access needed by executors).
   Mitigation: instruction-level rule + post-hoc audit of transcripts for paths of other runs (`grep runs/<other>` over metrics/raw).
2. **Per-role write scopes** (executor-wh only wh/, executor-hh only hh/, reviewer only reviews/, verifier nothing): permission
   rules are per session, not per subagent; subagent frontmatter restricts tools, not paths. Instruction-level only;
   verifier/reviewer still hold Bash (can write). Audited post hoc via git diff per phase.
3. **Custom agent definitions not loadable this session**: `.claude/agents/` has no live reload (docs: "Subagents … Yes, without
   live reload"); the files were created after session start, so the Agent tool does not list executor-wh/-hh, verifier, reviewer.
   Deviation (SPEC §7): multi_r1 spawns `general-purpose` subagents with the model override from the definition file
   (sonnet/haiku/opus) and the definition body pasted verbatim into the spawn prompt plus a `ROLE=` tag. Consequence: the
   `tools:` restriction is not applied (general-purpose has all tools, incl. Write for verifier/reviewer). Runs r2/r3 started in
   a fresh session will load the files natively. Fix for multi_r1: restart the session (`claude --resume`) or `/agents`.
4. Isolation of the single arm from multi_r1 outputs relies on the same rules; same bypass caveat (1).
