# Project source-control isolation proposal

Date UTC: 2026-11-02. Status: PROPOSED; no Git initialization or commit performed.

The actual working directory and reports directory resolve to `/eos/home-r/rjiang/vbs_zh_codex_starter` and its `reports` child. `git rev-parse --show-toplevel` gives `/eos/home-r/rjiang`; its HEAD is `6ea6cb9462533bbc1b209f7d4b4b67fd49b4d737`. Correctly scoped `git ls-files -- .` is empty, and `git status --short -- .` returns `?? ./`. The project has no `.git` entry. The initial `git ls-files -- vbs_zh_codex_starter` issued from inside the project was not the correct scope; the subsequent `-- .` check supplies the evidence. See 01_environment_evidence.txt.

Recommended solution: initialize a nested standalone repository with its Git directory at `/eos/home-r/rjiang/vbs_zh_codex_starter/.git`. This creates no parent commit, submodule, worktree link, ignore entry, or parent metadata modification. Normal Git discovery from within the project then stops at its own `.git`. The parent still sees an untracked nested directory; do not stage it there. A parent-backed worktree would modify parent Git metadata and is therefore unsuitable under the requested boundary.

Concrete non-destructive command proposal (NOT EXECUTED):

```bash
test "$(realpath /eos/home-r/rjiang/vbs_zh_codex_starter)" = /eos/home-r/rjiang/vbs_zh_codex_starter
test ! -e /eos/home-r/rjiang/vbs_zh_codex_starter/.git
git -C /eos/home-r/rjiang/vbs_zh_codex_starter init --initial-branch=main
git -C /eos/home-r/rjiang/vbs_zh_codex_starter rev-parse --show-toplevel --absolute-git-dir
```

Run the checks as fail-fast preconditions, stopping if either fails. Before an eventual first commit, review a project-only `.gitignore` for MC/build/cache/software directories, inspect file sizes and secrets, then stage only named reproducibility inputs/code/cards/reports. Do not use an unreviewed recursive add. Preserve reference sources with hashes and respect distribution restrictions. No remote or credential change is needed. EOS locking/atomic update behavior needs a small local Git verification before depending on it; if that fails, stop this subtask and choose another explicitly identified EOS directory. Never fall back to AFS or move/delete the parent `.git`.

This turn implements the requested inspection and proposal only. Project commit: **unavailable**. The parent hash is not a project snapshot. SHA256SUMS_01.txt provides interim file provenance. No parent files were edited and no parent Git mutation command was issued.
