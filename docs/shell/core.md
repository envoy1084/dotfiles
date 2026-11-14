# Core shell and prompt

[← Previous: System overview](system.md) · [Docs index](../index.md) · [Next: Configuration and restore →](configuration.md)

## Prompt and behaviour

The compact Pure-style Starship prompt uses Tokyo Night colours: context on one line, an input arrow on the next. Green means success; red plus an exit code means failure. Git state includes branch, changes and ahead/behind counts. Runtime versions appear when relevant and available; command durations appear after two seconds.

JetBrains Mono Nerd Font is configured in [Ghostty](../ghostty.md). bat follows the terminal ANSI palette and fzf uses Tokyo Night colours. History is shared, deduplicated and capped at 50,000 saved zsh entries. Plugins and the prompt load only in interactive terminals; non-terminal agent commands have plain startup output.

Homebrew's API refresh interval is one day (`HOMEBREW_API_AUTO_UPDATE_SECS=86400`); use `brew update` for an explicit refresh.


### Starship

[Project / documentation](https://starship.rs/). Compact two-line prompt with Tokyo Night colours, Git state, command results, and relevant runtime versions.

```sh
starship explain
starship timings
starship --version
```

### fzf

[Project / documentation](https://github.com/junegunn/fzf). Fuzzy file selection, directory picking and completion. Ctrl+T opens the file picker; Atuin owns Ctrl+R history search.

```sh
fzf
fd --type f | fzf
fzf --help
```

### zoxide

[Project / documentation](https://github.com/ajeetdsouza/zoxide). Jump to frequently visited directories.

```sh
z dotfiles
zi
zoxide query --list
```

### zsh-autosuggestions

[Project / documentation](https://github.com/zsh-users/zsh-autosuggestions). Suggest commands from history while typing. Accept with Right Arrow at the end of input.

Enabled through `configs/dot_zshrc`; no separate executable or global shortcut.

### zsh-syntax-highlighting

[Project / documentation](https://github.com/zsh-users/zsh-syntax-highlighting). Colour command-line syntax while typing. Loaded as the last zsh plugin.

Enabled through `configs/dot_zshrc`; no separate executable or global shortcut.

### ripgrep

[Project / documentation](https://github.com/BurntSushi/ripgrep). Search project text; executable: rg.

```sh
rg TODO .
rg --files
rg -n 'pattern' src
```

### fd

[Project / documentation](https://github.com/sharkdp/fd). Find paths by name; also powers the configured file picker.

```sh
fd settings
fd --type f --extension md
fd --hidden --exclude .git
```

### bat

[Project / documentation](https://github.com/sharkdp/bat). Read files with highlighting and line numbers; uses the terminal ANSI palette.

```sh
bat README.md
bat --paging=never path/to/file
bat --list-themes
```

---

[← Previous: System overview](system.md) · [Docs index](../index.md) · [Next: Configuration and restore →](configuration.md)
