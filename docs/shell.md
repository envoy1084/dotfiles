# Shell and Starship

Interactive zsh setup for Ghostty, with a compact two-line Starship prompt. The layout draws on Starship's [Pure preset](https://starship.rs/presets/pure-preset), with [Tokyo Night](https://starship.rs/presets/tokyo-night) colours and Nerd Font symbols. Configuration reference: [Starship](https://starship.rs/config/).

## Installed tools

| Tool | Purpose |
|---|---|
| [Starship](https://starship.rs/) | Directory, Git state, relevant runtime versions, command duration, exit status, and background jobs |
| [fzf](https://github.com/junegunn/fzf) | Search history and choose files interactively |
| [zoxide](https://github.com/ajeetdsouza/zoxide) | Jump to frequently visited directories |
| [zsh-autosuggestions](https://github.com/zsh-users/zsh-autosuggestions) | History-based suggestions while typing |
| [zsh-syntax-highlighting](https://github.com/zsh-users/zsh-syntax-highlighting) | Highlight command-line syntax |
| [ripgrep](https://github.com/BurntSushi/ripgrep) | Search project text with `rg` |
| [fd](https://github.com/sharkdp/fd) | Find files and feed the file picker |
| [bat](https://github.com/sharkdp/bat) | Read files with highlighting and line numbers; preview fzf selections |
| [jq](https://jqlang.org/) | Inspect and transform JSON |

## Prompt and behaviour

- Two lines: context first, input arrow second. Green arrow for success; red arrow and exit code for failure.
- Git branch, detached commit, rebase/merge state, changes, and ahead/behind counts. In status brackets, `!` means modified, `+` staged, `?` untracked, and `=` conflicted.
- Node, Bun, Python, Rust, and Go versions appear when detected and available. Runtime installation is separate.
- Command duration appears after two seconds. Remote/root identity and background-job counts appear when relevant.
- JetBrains Mono Nerd Font is configured in [Ghostty](ghostty.md).
- History is shared between terminals, deduplicated, and limited to 50,000 saved entries. A leading space excludes a command from saved history.
- Completion includes Homebrew tools, case-insensitive matching, and grouped menus.
- Prompt/plugins load only in interactive terminals. Non-terminal agent commands keep plain output.
- bat uses the terminal's ANSI palette; fzf uses Tokyo Night colours. Ctrl+T previews files and lists directories. File searches respect ignore files and exclude `.git`.

## Shortcuts

These apply at the shell prompt. Right Command belongs to [OmniWM](omniwm.md); left Command belongs to [Ghostty](ghostty.md).

| Shortcut | Action |
|---|---|
| Control + R | Search history; Enter inserts the selected command, then Enter runs it |
| Control + T | Choose files/directories and insert escaped paths |
| Control + / inside the file picker | Toggle file preview |
| Right Arrow at the end of input | Accept the autosuggestion |
| Up / Down | Search history matching the current input prefix; supports multiline input |
| Tab | Complete commands, paths, and arguments; select ambiguous matches from a menu |
| `**` then Tab | fzf completion where supported; for example `cat **` then Tab |
| Option + Left / Right | Move backward / forward by a word |
| Control + A / E | Start / end of input |
| Control + W | Delete the previous word |
| Control + U | Delete input before the cursor |
| Control + L | Redraw/clear the visible screen |
| Control + C | Cancel current shell input or interrupt the foreground command |

fzf's Option+C directory shortcut is disabled; use `zi` instead. Foreground agents and editors handle their own input.

## Commands and aliases

| Command | Purpose |
|---|---|
| `z dotfiles` | Jump to a visited directory matching `dotfiles` |
| `zi` | Choose among visited directories using fzf |
| `cd -` | Return to the previous directory |
| `..` / `...` | Go up one / two directory levels |
| `ll` | `ls -lah` |
| `gs` | Short Git status including branch |
| `gd` | Git diff |
| `gl` | Last 15 Git commits, one line each |
| `rg TODO .` | Search project text |
| `fd settings` | Find matching paths |
| `bat path/to/file` | Read a file with highlighting |
| `jq '.name' package.json` | Extract a JSON field |

## Configuration and restore

| Source | Destination |
|---|---|
| `configs/dot_zprofile` | `~/.zprofile`; login environment and Homebrew PATH |
| `configs/dot_zshrc` | `~/.zshrc`; interactive behaviour and plugins |
| `configs/dot_config/starship.toml` | `~/.config/starship.toml`; prompt |
| `configs/dot_config/bat/config` | `~/.config/bat/config`; file display |

- `Brewfile` declares all nine packages. Restore through `./bootstrap --write` or `./setup packages --write` followed by `./setup apply --write`.
- Open a new Ghostty window to load shell changes. Starship config changes appear at subsequent prompts.
- Keep machine/work-specific additions in `~/.zprofile.local` or `~/.zshrc.local`, outside Git.
- History, completion caches, and zoxide's directory database stay local. Restore settings through chezmoi rather than copying these runtime files into the repo.
- Preview with `./setup diff`, then apply with `./setup apply --write`. Check shell syntax and config drift with `./doctor`.

## Versions

Recorded 2026-11-14; installed versions, not package pins.

| Component | Version |
|---|---|
| macOS zsh | 5.9 |
| Starship | 1.27.0 |
| fzf | 0.75.0 |
| zoxide | 0.10.0 |
| zsh-autosuggestions | 0.7.1 |
| zsh-syntax-highlighting | 0.8.0 |
| ripgrep | 15.2.0 |
| fd | 10.5.2 |
| bat | 0.26.1 |
| jq | 1.8.2 |
