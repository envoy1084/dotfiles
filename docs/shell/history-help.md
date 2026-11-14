# History, recipes and completion

[← Previous: Development and automation](development.md) · [Docs index](../index.md) · [Next: JSON and YAML →](structured-data.md)

## Find instead of memorising

- `how topic` reads our guides, for example `how git` or `how media`.
- `tools [words]` finds local recipes. Ctrl+G does the same using the current input as its query.
- Ctrl+R searches local command history through Atuin.
- `tldr command` shows short upstream usage examples.

Recipe selection fills named inputs, then inserts the completed command at your shell prompt. Read it, edit if needed, and press Enter yourself. File paths containing a literal single quote need that quote escaped when inserted into the single-quoted recipe placeholder; the daily shell functions accept normally quoted arguments directly.


### tealdeer

[Project / documentation](https://tealdeer-rs.github.io/tealdeer/) · Homebrew: `tealdeer`.

Read concise command examples from tldr pages. Executable: tldr.

```sh
tldr --update
tldr tar
tldr --list
```

The update command downloads the local documentation cache.

### navi

[Project / documentation](https://github.com/denisidoro/navi) · Homebrew: `navi`.

Search interactive command cheatsheets and fill their parameters.

```sh
tools
tools git
navi --path ~/.config/navi/cheats --print
```

Use `tools` or Ctrl+G for our local recipes. Both place your selection at the prompt for review. No remote collections are loaded. Running bare `navi` uses its own defaults and can execute a selected snippet; prefer `tools`.

### Atuin

[Project / documentation](https://atuin.sh/) · Homebrew: `atuin`.

Store and search richer command history, with optional synchronisation.

```sh
atuin --help
atuin search 'git'
atuin stats
```

Local history recording and Ctrl+R search are enabled. Enter selects a command into the shell; a second Enter runs it. Up/Down retain prefix search. Sync, the daemon and the AI keybinding are disabled. Existing zsh history was imported on this Mac; new Macs start with their own local history.

## Local Atuin data

History stays on this Mac; `auto_sync=false`, daemon disabled, no AI key. A leading space excludes a command from both histories. Atuin's secret filter is enabled but is not a guarantee that every sensitive command is recognised. Histories and SQLite databases stay outside Git.

The existing zsh history was imported once on this Mac. On another Mac, import its own history if wanted:

```sh
atuin import zsh
atuin stats
```

## Tab completion

[zsh-completions](https://github.com/zsh-users/zsh-completions) supplies extra command completions; [fzf-tab](https://github.com/Aloxaf/fzf-tab) presents native completion candidates through fzf. Both load from Homebrew; the completion cache stays local.

Type a command or partial path and press Tab. Type to filter candidates; arrows choose, Enter accepts. Ctrl+T opens the dedicated file picker. fzf's `**` Tab binding is replaced by fzf-tab so there is one Tab owner. Up/Down retain the existing input-prefix search.

Insecure completion directories are skipped rather than blocking shell startup. If expected completions are missing, run `autoload -Uz compaudit; compaudit` and inspect ownership/permissions. On this Mac, removing group/world write permission from the user-owned Homebrew `share` directory resolved the audit.

Our recipes live in `configs/dot_config/navi/cheats/daily.cheat`. Add a category line (`% category`), a description (`# Description`) and its command; apply through chezmoi. `tools` explicitly selects this local directory and uses `--print`.

---

[← Previous: Development and automation](development.md) · [Docs index](../index.md) · [Next: JSON and YAML →](structured-data.md)
