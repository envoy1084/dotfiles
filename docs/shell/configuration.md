# Configuration and restore

[← Previous: Core shell and prompt](core.md) · [Docs index](../index.md) · [Next: Shell versions →](versions.md)

## Managed source files

| Source under `configs/` | Destination / role |
|---|---|
| `dot_zprofile` | `~/.zprofile`: Homebrew environment and PATH |
| `dot_zshrc` | `~/.zshrc`: interactive initialization and plugin order |
| `dot_config/shell/helpers.zsh.tmpl` | `~/.config/shell/helpers.zsh`: daily commands and actual checkout path |
| `dot_config/starship.toml` | `~/.config/starship.toml`: prompt |
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

On a new Mac, follow the [repository restore instructions](../../README.md). `Brewfile` records packages, not exact historical versions. Chezmoi fetches the pinned Yazi plugin; initial restore needs network access. No separate symlink manager, plugin manager, or remote cheat collection is required.

## Local choices and state

Keep environment additions in `~/.zprofile.local`, interactive additions in `~/.zshrc.local`, Git overrides in `~/.gitconfig.local`. These remain outside Git. `PROJECTS_DIR` defaults to `~/Projects`; set it in the local profile for another root. Update Yazi's Projects bookmark separately if you change it.

Atuin history, zsh history, zoxide's database, completion caches, Navi state, tmux processes, rclone credentials and runtime installs stay local. Settings restore does not bring back history or resurrect tmux processes. Atuin import is a per-machine step. Agents and cloud services need their own sign-ins; rclone needs a chosen provider and remote.

No runtime selections, cloud account or remote worktree hooks are invented by this setup. Add project `mise.toml` and `justfile` files in each project when useful. Review diffs before committing configuration.

---

[← Previous: Core shell and prompt](core.md) · [Docs index](../index.md) · [Next: Shell versions →](versions.md)
