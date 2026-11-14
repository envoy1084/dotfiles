# My macOS setup

Native macOS productivity and agent setup, maintained in `~/dotfiles`.

Homebrew installs packages. Chezmoi owns configuration files. Git records changes. The setup wrapper previews changes unless `--write` is provided; it never uninstalls unrelated packages or automatically pushes configuration.

The foundation is currently local-only. GitHub repository creation and GitHub CLI sign-in are deferred at the user's request. Doctor reports those as informational items; no remote has been created or pushed. After creating a private repo later, add its URL as `origin` and push `main`.

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
# Once an origin remote is configured: git push
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

Bootstrap installs the Brewfile packages, initializes chezmoi against this checkout, applies the managed config, then runs doctor. It requires macOS and Command Line Tools, and can find Homebrew in the usual Apple Silicon/Intel locations. If a prerequisite is missing it prints the next step and exits.

Selected macOS preferences are separate, so they are not silently changed during a config restore:

```sh
./setup macos                  # preview
./setup macos --write          # backup selected previous values, then apply
```

No apps are automatically restarted. Some preference changes need a new login or restarting Dock. Finish the application permissions/sign-ins in [docs/manual-steps.md](docs/manual-steps.md).

## Configuration layout

`.chezmoiroot` selects `configs/` as the source-state root. Chezmoi names encode destination paths and permissions: `dot_zprofile` becomes `~/.zprofile`; `private_dot_ssh/private_config` becomes `~/.ssh/config` with owner-only permissions. `private_` does not encrypt a file or keep it out of Git. `private_Library` preserves the existing private permissions on `~/Library`.

Managed configuration:

- `configs/dot_config/omniwm/`: workspace settings, shell layout, wallpaper palette.
- `configs/private_Library/Application Support/com.mitchellh.ghostty/`: current Ghostty config.
- `configs/dot_zprofile`: Homebrew environment, portable local-bin PATH, optional local overrides.
- `configs/private_dot_ssh/private_config`: GitHub client options, no keys.
- `configs/dot_gitconfig.tmpl`: Git identity from `configs/.chezmoidata.toml`.
- `configs/.chezmoi.toml.tmpl`: machine-local chezmoi initialization; resolves the actual checkout path.

The existing desktop choices are preserved: five scrolling/niri workspaces, Tokyo Night shell theme, and currently disabled clipboard history, IPC, and Quake terminal. Ghostty is still using its default template.

## Machine-specific settings

Keep local shell additions in `~/.zprofile.local` and machine/work-specific Git overrides in `~/.gitconfig.local`. Both are read by managed config and stay outside Git. Future host-specific templates should be added only when there is an actual difference to support.

Changing the shared identity in `configs/.chezmoidata.toml` changes the Git template. Per-repository Git config still takes precedence; the initial dotfiles repo has a local identity established from the authenticated GitHub profile.

## Packages and growth

`Brewfile` currently declares chezmoi and GitHub CLI plus the existing seven app casks. `./setup packages --write` installs with `--no-upgrade` and never invokes cleanup. Required dependencies may still be upgraded. A Brewfile records package selection, not exact historical binary versions.

When adopting a tool, add its package declaration and useful config together. To manage another config, use `chezmoi add <specific-path>` and inspect the result. Changes to the desktop should be imported and committed deliberately. Do not enable automatic commit/push of every live app change.

`state/observed.json` records the initial app versions and external installation channels. It is historical inventory, not a lockfile. Missing app exports and outside-Homebrew installs are documented separately; see the manual checklist.

## Recovery and privacy

The baseline commit preserves the pre-chezmoi setup. Review `git log` and a proposed `chezmoi diff` when rolling back to an older configuration. The initial migration and wrapper applies keep backups under `~/Library/Application Support/dotfiles/backups/`, outside Git.

Keep SSH keys, tokens, Keychain material, browser/app databases, and agent conversations out of this repository. Doctor checks obvious forbidden target names and private-key content, but it is not a comprehensive secret scanner; review every diff before pushing, including to a private repo.

Dotfiles are not a backup of personal work or a complete machine image. Privacy permissions, sign-ins, app settings without portable exports, and exact historical binary versions remain separate concerns.
