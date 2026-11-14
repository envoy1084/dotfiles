# Git and parallel work

[← Previous: Files and archives](files.md) · [Docs index](../index.md) · [Next: Projects and tmux →](tmux.md)

## Everyday shortcuts

| Command | Expands to / purpose |
|---|---|
| `gs` | `git status --short --branch` |
| `gd` / `gds` | Unstaged / staged diff |
| `gl` | Last 20 commits with graph and decorations |
| `lg` | LazyGit |
| `gstage file…` | Stage explicit files with `git add` |
| `gcommit "message"` | Commit the staged changes |
| `gnew branch` | Create and switch to a branch |
| `gpull` | Pull using `--ff-only`; stops if merging would be needed |
| `gpush` | Normal `git push` |

```sh
gs
gd
gstage path/to/file
gds
gcommit "Describe the change"
```

Pushing is explicit. The shortcuts do not commit, stage all files, or push automatically.


### LazyGit

[Project / documentation](https://github.com/jesseduffield/lazygit/) · Homebrew: `lazygit`.

Review diffs, stage changes, switch branches, and manage commits through an interactive Git interface.

```sh
lazygit
lazygit -p ~/dotfiles
lazygit --help
```

Use `lg` inside a repository. Tokyo Night colours and delta rendering are configured. Arrow keys navigate, Space stages/unstages the selected file, `c` opens commit entry, and `?` shows contextual help. Review the selected action before confirming.

### delta

[Project / documentation](https://dandavison.github.io/delta/) · Homebrew: `git-delta`.

Display highlighted Git diffs and compare files. Homebrew package: git-delta; executable: delta.

```sh
git -c core.pager=delta diff
git diff | delta --paging=never
delta old.txt new.txt
```

Delta is now the shared Git pager and LazyGit renderer. Diffs use highlighted unified output with line numbers. Press `q` to leave the pager; `n` / `N` move between files with delta navigation. `git --no-pager diff` prints a plain diff.

### Worktrunk

[Project / documentation](https://worktrunk.dev) · Homebrew: `worktrunk`.

Manage Git worktrees for independent branches and parallel agent tasks. Executable: wt.

```sh
wt list
wt switch --help
wt switch --create feature-demo
```

Shell integration is enabled: `wt switch` can change your current directory. `wt list` inspects existing worktrees. The last example creates a branch/worktree when run inside a repository; nothing creates worktrees automatically.

### tokei

[Project / documentation](https://github.com/XAMPPRocky/tokei) · Homebrew: `tokei`.

Summarise source-code size by language.

```sh
tokei .
tokei src
tokei --help
```

---

[← Previous: Files and archives](files.md) · [Docs index](../index.md) · [Next: Projects and tmux →](tmux.md)
