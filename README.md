# My macOS setup

Native macOS productivity and agent setup, maintained in `~/dotfiles`.

Homebrew installs packages. Chezmoi owns configuration files. Git records changes. The setup wrapper previews changes unless `--write` is provided; it never uninstalls unrelated packages or automatically pushes configuration.

The GitHub remote, SSH authentication and GitHub CLI authentication are configured on this Mac. Sign-in and SSH keys must be established separately on a new Mac. Changes are committed locally and published deliberately.

Browse the [documentation index](docs/index.md) for app shortcuts and the shell guides.

## Daily commands

```sh
cd ~/dotfiles
./doctor                       # read-only foundation and drift checks
./setup diff                   # proposed configuration changes
./setup apply                  # preview; no config changes
./setup apply --write           # backup changed files, then apply via chezmoi
```

Plain `chezmoi` commands also use this repo after initialization:

```sh
chezmoi edit ~/.zprofile
chezmoi diff
chezmoi apply
git -C ~/dotfiles diff
```

Our apply wrapper adds an external backup before invoking chezmoi. Direct `chezmoi apply` uses chezmoi's own conflict handling and does not run that backup helper.

When changing settings through an app, explicitly import the specific file:

```sh
chezmoi add ~/.config/omniwm/settings.toml
git diff
git add .
git commit -m "Update workspace configuration"
# When ready to publish: git push
```

On this configured Mac, the current app configuration is the source of truth for your preferences. During maintenance, capture observed OmniWM/Ghostty/VS Code changes before applying other dotfiles work; keep the docs aligned. On a new Mac, the saved repo configuration supplies the initial settings. This is a maintenance rule; it does not run a background sync service.

VS Code settings, tasks, keybindings when present, snippets and extension choices can be captured together:

```sh
./setup vscode --capture                # preview
./setup vscode --write --capture        # capture your current preferences
```

`./setup capture` previews importing all already-managed configs; `./setup capture --write` imports them. Review the diff, particularly templates, before committing. It does not sweep arbitrary home files, app databases, or credentials into Git.

## New Mac

1. Install Apple's Command Line Tools (`xcode-select --install`) and Homebrew from https://brew.sh.
2. Install GitHub CLI (`brew install gh`) and authenticate (`gh auth login`). A private repo needs authentication before cloning. Register a new SSH key when choosing SSH, or use HTTPS.
3. Clone your private repository into `~/dotfiles`.
4. Preview, then restore:

```sh
cd ~/dotfiles
./bootstrap --dry-run
./bootstrap --write
```

Bootstrap installs the Brewfile packages, initializes chezmoi against this checkout, applies the managed config, installs the captured mise tools, restores missing VS Code extensions, then runs doctor. Runtime installation runs from your home directory so unrelated project configs cannot join the restore. It requires macOS and Command Line Tools, and can find Homebrew in the usual Apple Silicon/Intel locations. If a prerequisite is missing it prints the next step and exits.

Selected macOS preferences are separate, so they are not silently changed during a config restore:

```sh
./setup macos                  # preview
./setup macos --write          # backup selected previous values, then apply
```

No apps are automatically restarted. Some preference changes need a new login or restarting Dock. Finish the application permissions/sign-ins below.

## Configuration layout

`.chezmoiroot` selects `configs/` as the source-state root. Chezmoi names encode destination paths and permissions: `dot_zprofile` becomes `~/.zprofile`; `private_dot_ssh/private_config` becomes `~/.ssh/config` with owner-only permissions. `private_` does not encrypt a file or keep it out of Git. `private_Library` preserves the existing private permissions on `~/Library`.

Managed configuration:

- `configs/dot_config/omniwm/`: workspace settings, shell layout, wallpaper palette.
- `configs/private_Library/Application Support/com.mitchellh.ghostty/`: Ghostty appearance, keyboard, notifications, and window restore settings.
- `configs/dot_zprofile`: Homebrew environment, portable local-bin PATH, optional local overrides.
- `configs/dot_zshrc`: terminal-only interactive shell, completion, history, and plugin setup.
- `configs/dot_config/starship.toml` and `configs/dot_config/bat/config`: prompt and file previews.
- `configs/private_dot_ssh/private_config`: GitHub client options, no keys.
- `configs/dot_gitconfig.tmpl`: Git identity from `configs/.chezmoidata.toml` and delta pager.
- `configs/dot_config/{shell,yazi,navi,lazygit}/`, `configs/private_dot_atuin/` and `configs/dot_tmux.conf`: daily helpers, file manager, local history/recipes, Git UI and terminal sessions.
- `configs/.chezmoiexternal.toml`: immutable official Yazi Git plugin source.
- `configs/dot_config/mise/config.toml`: personal runtime/tool versions and Rust settings; restored by `./setup runtimes --write`.
- `configs/private_Library/Application Support/Code/User/`: VS Code settings, user tasks and snippets; extension versions are in `configs/dot_config/vscode/extensions.txt`.
- `configs/.chezmoi.toml.tmpl`: machine-local chezmoi initialization; resolves the actual checkout path.

The desktop uses five scrolling/niri workspaces, a Tokyo Night shell theme, right-Command/WASD shortcuts, and an enabled Ghostty Quake terminal. Clipboard history and IPC remain disabled. See [OmniWM shortcuts and settings](docs/omniwm.md).

Ghostty uses JetBrains Mono Nerd Font, TokyoNight Night, and local shortcuts that complement OmniWM. See [Ghostty shortcuts and settings](docs/ghostty.md).

VS Code preserves your EnvoyOS theme, existing extensions/formatters and snippets, with JetBrains Mono Nerd Font for editor and terminal. See [VS Code configuration and restore](docs/vscode.md).

The shell uses a compact Pure-style Starship prompt in Tokyo Night colours, local Atuin history, fuzzy file search/completion, autosuggestions, syntax highlighting, and zoxide navigation. The installed terminal toolkit also covers files, Git, sessions, development, networking, media, and monitoring. See [shell tools and shortcuts](docs/shell/index.md).

## Machine-specific settings

Keep local environment additions in `~/.zprofile.local`, interactive customisations in `~/.zshrc.local`, and machine/work-specific Git overrides in `~/.gitconfig.local`. These are read by managed config and stay outside Git. Future host-specific templates should be added only when there is an actual difference to support.

Changing the shared identity in `configs/.chezmoidata.toml` changes the Git template. Per-repository Git config still takes precedence; the initial dotfiles repo has a local identity established from the authenticated GitHub profile.

## Packages and growth

`Brewfile` declares chezmoi and GitHub CLI, 45 shell/CLI tools, eight app casks (including VLC), and JetBrains Mono Nerd Font. `./setup packages --write` installs with `--no-upgrade` and never invokes cleanup. Required dependencies may still be upgraded. A Brewfile records package selection, not exact historical binary versions.

When adopting a tool, add its package declaration and useful config together. To manage another config, use `chezmoi add <specific-path>` and inspect the result. Changes to the desktop should be imported and committed deliberately. Do not enable automatic commit/push of every live app change.

Homebrew owns mise; mise owns Node, pnpm, Rust, Go and other adopted developer runtimes/tools. After changing a global runtime selection, let the installer finish, then capture `~/.config/mise/config.toml`. `./setup runtimes` previews missing tools; `./setup runtimes --write` installs and rebuilds shims. Project-specific versions stay in the project repository. Agent login shells and editors discover tools through mise shims; launchers with a separate environment can use `mise exec -- <command>`.

`state/observed.json` records the initial app versions and external installation channels. It is historical inventory, not a lockfile. See the manual restore notes below for missing app exports and outside-Homebrew installs.

## Manual restore notes

Grant OmniWM Accessibility and Input Monitoring permissions and Ghostty Accessibility for its global shortcut; see [OmniWM](docs/omniwm.md). Set login-item behavior intentionally. Finish Raycast, Thaw, and Superwhisper onboarding and permissions. Sign in separately to agents and services; credentials and conversation state stay outside dotfiles. Register a new SSH key on each Mac rather than restoring a private key from Git.

Existing tools outside Homebrew need their original installation channels restored:

| Tool | Observed version | Restore |
|---|---|---|
| Helium | 0.21.3.1 | Official distribution |
| T3 Code (Beta) | 0.1.9 | Its existing distribution/update channel |
| Codex CLI | 0.169.0 | Standalone installer; linked from `~/.local/bin` |
| T3 CLI | 0.1.9 | T3-managed binary; linked from `~/.local/bin` |

Portable application exports still to capture: Raycast preferences/extensions/shortcuts, Thaw layout, and Superwhisper modes/model preferences. VS Code settings, user tasks, four snippet files and 32 extension versions are captured; custom user keybindings were absent. VS Code sign-in/Settings Sync and extension credentials remain separate. Use supported exports; avoid copying entire app databases. Run `./doctor` after restoring.

## Research and scratch work

Use `research/` for temporary notes, audits, proposals, and scratch files. Git ignores that folder. Keep `docs/` for concise, maintained references such as `omniwm.md`, `ghostty.md`, and the category guides in `shell/`.

## Recovery and privacy

The baseline commit preserves the pre-chezmoi setup. Review `git log` and a proposed `chezmoi diff` when rolling back to an older configuration. Setup-time file backups were cleared at the user's request on 2026-11-14. Future wrapper applies can create new recovery copies under `~/Library/Application Support/dotfiles/backups/`, outside Git. A backup of the completed Mac setup is deferred until setup is finished.

Keep SSH keys, tokens, Keychain material, browser/app databases, and agent conversations out of this repository. Doctor checks obvious forbidden target names and private-key content, but it is not a comprehensive secret scanner; review every diff before pushing, including to a private repo.

Dotfiles are not a backup of personal work or a complete machine image. Privacy permissions, sign-ins, app settings without portable exports, and exact historical binary versions remain separate concerns.
