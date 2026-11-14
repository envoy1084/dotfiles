# Working on this Mac setup

This thread and repo are the ongoing native macOS productivity and agent setup. The user wants a small, understandable, reproducible configuration that grows with actual needs.

- Start with `./setup status` and `./setup check`; use `./doctor` for the full foundation check.
- Chezmoi is the only configuration manager. `configs/` is selected by `.chezmoiroot`; never reintroduce a parallel copy/symlink manifest.
- Use `./setup diff` and `./setup apply --dry-run` before applying. Repository edits alone do not authorize live changes. Apply live settings when the user's task requests them.
- `./setup apply --write` backs up changed existing managed files outside Git, then uses chezmoi's conflict checks. Never silently force conflicting local changes.
- Preserve existing settings when adding packages or migrating config unless the user requests a behavior change.
- On this configured Mac, live application configuration is the source of truth for user preferences. When you notice changes in managed app settings (including OmniWM, Ghostty and VS Code), capture those specific files into chezmoi and update affected docs before applying other work. This standing instruction authorizes capture; do not overwrite newer app settings with stale repo values. Preserve unrelated changes. On a new Mac, restore the saved repo settings normally.
- Capture VS Code settings, tasks, keybindings, snippets and extension choices with `./setup vscode --write --capture`. Keep sign-ins, Settings Sync state, extension storage, databases and credentials outside Git. Respect the user's selected extensions, theme and formatters.
- Raycast code, scripts, reviewed Quicklinks/Snippets, and choice manifests live under `configs/dot_config/raycast/`. Native preferences, aliases and hotkeys are app-managed: capture newer live choices through supported exports or an in-app inventory before updating manifests. `settings.json` records helper paths and desired UI settings; applying it does not configure the app. Never edit/copy Raycast databases or encryption keys. Full encrypted exports stay outside Git.
- Homebrew owns mise; mise owns language runtimes and versioned developer tools. After a runtime change, capture `~/.config/mise/config.toml` once the installer finishes. Keep bootstrap's runtime/extension restore steps current; use shims for login shells and full activation for interactive terminals.
- Add intentional package installs to Brewfile and their config to chezmoi in the same change. Do not replace an app's install/update channel without a request.
- Keep one owner per runtime and one clearly chosen app per overlapping desktop function.
- No test framework or test scripts: the user explicitly removed them. Use check/doctor, syntax validation, dry runs, and disposable verification when needed.
- Never copy SSH keys, tokens, auth files, app/browser databases, histories, or agent sessions into Git. Review diffs before pushing.
- Local shell/Git overrides live outside Git in `~/.zprofile.local`, `~/.zshrc.local`, and `~/.gitconfig.local`.
- Keep paths portable; private chezmoi attributes mean filesystem permissions, not encryption.
- Keep AeroSpace out unless explicitly requested again.
- Read the README manual restore notes for remaining exports and sign-ins. Do not claim those are automated.
- Keep maintained references in `docs/`; `docs/index.md` links every page, and shell category guides live under `docs/shell/`. Keep Previous / Docs index / Next navigation at the top and bottom of each page. Put research, proposals, and scratch work in Git-ignored `research/`.
- Git identity must come from user-provided or authenticated profile information, never invention. Do not create another remote or publish changes without user authorization.
- The GitHub remote, SSH and GitHub CLI authentication are configured on this Mac. Authentication must be established separately on a new Mac; do not request a token or push unless the user asks.
