# My macOS setup

Native macOS desktop and agent tools, captured on 14 November 2026. The repository lives at `~/dotfiles`.

## What is managed

- `Brewfile`: the seven currently installed Homebrew casks.
- `configs/omniwm/`: settings, shell layout, and custom wallpaper palette.
- `configs/ghostty/`: current Ghostty configuration (still the default template).
- `configs/zsh/zprofile`: Homebrew setup and a portable `$HOME/.local/bin` PATH.
- `configs/ssh/config`: GitHub SSH client configuration; no keys.
- `macos-defaults.json`: the selected existing dark-mode, scrolling, and Dock preferences.
- `state/observed.json`: observed versions, external installations, and remaining manual setup.

OmniWM currently uses scrolling/niri layouts, five workspaces, and the Tokyo Night shell theme. Its clipboard history, IPC, and Quake terminal are currently disabled. These existing choices are preserved, not redesigned by this repository.

Configuration files are copied instead of symlinked because desktop apps can rewrite them. Saving settings inside an app does not automatically update Git; capture them afterward.

## Inspect and validate

```sh
cd ~/dotfiles
./setup status
./setup check
./setup apply --dry-run
```

All mutation commands preview by default. Only `--write` applies changes. Running `./setup` by itself reports file status.

## Restore on another Mac

Install Apple's Command Line Tools and Homebrew first. On this Mac they are already present. No additional Python package is required; the scripts use the system Python 3 and standard library.

```sh
cd ~/dotfiles
./setup packages --write
./setup apply --write
./setup macos --write
```

Packages installs missing Brewfile entries without requesting upgrades of existing packages, and never runs cleanup. Homebrew may still upgrade dependencies if installation requires it. Brewfile selections are not exact binary/version locks.

Apply backs up changed files under `~/Library/Application Support/dotfiles/backups/` before copying them. SSH's directory/config receive restrictive permissions. Re-running apply when file contents and permissions match makes no changes.

The macOS command backs up the selected previous preference values, then writes only the settings in `macos-defaults.json`. It does not restart apps automatically. Some changes require a new login or restarting Dock.

Open OmniWM, Raycast, Superwhisper, and Thaw after installation and complete their permission/login prompts. The scripts do not grant Accessibility, Screen Recording, microphone, or other privacy permissions.

## Keep it current

After changing an app's managed config:

```sh
./setup capture --dry-run
./setup capture --write
git diff
git add .
git commit -m "Update desktop configuration"
```

Capture copies only the files listed in `manifest.json`. It normalizes your home-directory path in the shell profile and backs up previous repository files. It rejects obvious private-key or credential assignments, but always inspect the diff before publishing.

After intentionally adding a Homebrew package, add its declaration to `Brewfile`. To regenerate the list from the whole machine, use `brew bundle dump --file=/tmp/mac-Brewfile` and review it before replacing the tracked file. Capture does not automatically import every installed package or preference.

New managed dotfiles need an explicit source/target entry in `manifest.json`; unrelated files are never swept into the repo.

## Separate manual items

Helium, T3 Code, Codex CLI, and T3 CLI are installed outside Homebrew. Their observed versions and locations are recorded in `state/observed.json`; they do not yet have restore automation here. Keep their existing distribution/update channels until explicitly choosing a managed alternative.

Celestial 1.1.0 is installed from `github:OmniNull/OmniWM@v0.8.0`, with no changes against its manifest at capture time. The active shell profile is `default`. The style source is recorded instead of committing its fonts and generated widget code. Reinstall the style through OmniWM if needed; only the personal shell overrides/palette are managed here.

Raycast preferences/extensions, Thaw layouts, and Superwhisper modes/model settings still need app-supported exports. Their databases and credentials are not copied. No custom VS Code extensions were detected at capture time. The old AeroSpace setup is deliberately excluded.

## Git and secrets

This is a local Git repository with no remote. A Git name/email were not configured at creation, so no initial commit was fabricated. Set your own identity, then commit:

```sh
git config user.name "Your Name"
git config user.email "your-email@example.com"
git add .
git commit -m "Capture current macOS setup"
```

These settings apply only to this repository unless you add `--global`.

Never commit private SSH keys, API tokens, agent auth files, Keychain data, browser profiles, conversations, or app databases. `.gitignore` excludes common secret/local/export paths. SSH public keys and account sign-ins remain separately managed; a new Mac can generate a new key.

## Files versus runtime state

This repository captures selected configuration and package selection. It is not a full machine image, personal-file backup, or exact reproduction of app versions. App permissions, login items, sign-ins, and settings without exports remain manual until explicitly automated.
