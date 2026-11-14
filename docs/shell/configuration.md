# Configuration and restore

[← Previous: Core shell and prompt](core.md) · [Docs index](../index.md) · [Next: Shell versions →](versions.md)

## Managed source files

| Source under `configs/` | Destination / role |
|---|---|
| `dot_zprofile` | `~/.zprofile`: Homebrew environment and PATH |
| `dot_zshrc` | `~/.zshrc`: interactive initialization and plugin order |
| `dot_config/shell/helpers.zsh.tmpl` | `~/.config/shell/helpers.zsh`: daily commands and actual checkout path |
| `dot_config/starship.toml` | `~/.config/starship.toml`: prompt |
| `dot_config/mise/config.toml` | `~/.config/mise/config.toml`: runtime versions, Rust components and installation settings |
| `dot_config/bat/config` | `~/.config/bat/config`: file display |
| `private_dot_atuin/private_config.toml` | `~/.atuin/config.toml`: local history preferences |
| `dot_config/navi/cheats/daily.cheat` | `~/.config/navi/cheats/daily.cheat`: local recipes |
| `dot_config/yazi/` | `~/.config/yazi/`: manager, keys, theme, plugin initialization |
| `dot_config/lazygit/config.yml` | `~/.config/lazygit/config.yml`: theme and delta renderer |
| `dot_tmux.conf` | `~/.tmux.conf`: session/window behavior and colours |
| `dot_gitconfig.tmpl` | `~/.gitconfig`: identity and delta; local override included last |
| `.chezmoiexternal.toml` | Pinned official Yazi Git plugin and licence |

## Apply and restore

```sh
cd ~/dotfiles
./setup diff
./setup apply --dry-run
./setup apply --write
./doctor
```

Open a new Ghostty window to load the updated shell. Reload tmux with Ctrl+B then `r`; restart Yazi/LazyGit to reload their settings. Starship reads changes at later prompts. Avoid repeatedly sourcing `.zshrc` into an existing shell with active hooks.

On a new Mac, follow the [repository restore instructions](../../README.md). `Brewfile` records packages, not exact historical versions. Chezmoi restores mise's global config; bootstrap then runs `./setup runtimes --write` from your home directory to install the recorded tools and rebuild shims. It also restores missing VS Code extensions. Chezmoi fetches the pinned Yazi plugin; initial restore needs network access.

For runtime changes alone, use `./setup runtimes` to preview and `./setup runtimes --write` to install. Once an intentional `mise use --global ...` completes, capture `~/.config/mise/config.toml` with chezmoi and review the diff. This saves version choices and settings; runtime binaries and Rust/Cargo caches stay outside Git.

The login profile adds mise shims for editors and agent login shells; interactive terminals also activate mise on prompts/directory changes. Agents launched with an unrelated environment can use `mise exec -- <command>`, or inherit the shim PATH after restarting their launcher. `./doctor` checks runtime installation and login-shell access.

## Local choices and state

Keep environment additions in `~/.zprofile.local`, interactive additions in `~/.zshrc.local`, Git overrides in `~/.gitconfig.local`. These remain outside Git. `PROJECTS_DIR` defaults to `~/Projects`; set it in the local profile for another root. Update Yazi's Projects bookmark separately if you change it.

Atuin history, zsh history, zoxide's database, completion caches, Navi state, tmux processes, rclone credentials and runtime installs stay local. Settings restore does not bring back history or resurrect tmux processes. Atuin import is a per-machine step. Agents and cloud services need their own sign-ins; rclone needs a chosen provider and remote.

Personal runtime defaults are saved in mise config. Project-specific versions belong in each project's `mise.toml`; Rust's `rust-toolchain.toml` is enabled as a version source. Cloud accounts and remote worktree hooks remain per-user choices. Review diffs before committing configuration.

---

[← Previous: Core shell and prompt](core.md) · [Docs index](../index.md) · [Next: Shell versions →](versions.md)
