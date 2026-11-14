# Manual setup and remaining coverage

## Deferred on this Mac

The user will create the GitHub repository later. GitHub CLI sign-in and adding/pushing an origin remote are deferred. SSH authentication already works; local Git commits do not require GitHub API authentication. Do not request a token or create a repository until the user resumes this step.

## After restoring a Mac

- Sign in to GitHub before cloning a private repo. Run `gh auth login` and verify with `gh auth status`.
- Generate/register the new Mac's SSH key if using SSH. Keys are not restored from this repo.
- Open OmniWM and grant the permissions needed for your chosen functions. Set login-item behavior intentionally.
- Open Raycast, Thaw, and Superwhisper, finish onboarding, grant the permissions you choose, and sign in where required.
- Sign in to Claude Code, Codex, T3 Code, and any other adopted agent. Credentials and conversation state are not in dotfiles.
- Review `./doctor` and finish the external application installations below.

## Existing installations outside Homebrew

| Tool | Observed version | Current channel / restore status |
|---|---|---|
| Helium | 0.21.3.1 | Outside Homebrew; reinstall from its official distribution |
| T3 Code (Beta) | 0.1.9 | Outside Homebrew; preserve its distribution/update channel |
| Codex CLI | 0.169.0 | Standalone installer, linked from `~/.local/bin`; authentication separate |
| T3 CLI | 0.1.9 | T3-managed binary linked from `~/.local/bin` |

These entries document existing state. They are not implemented installers. Decide on and verify each installation method before adding automation.

## Application exports to capture next

- Raycast preferences, extensions, shortcuts, and any adopted snippets/quicklinks.
- Thaw's supported layout export.
- Superwhisper modes, recording shortcuts, and model preferences.
- VS Code settings, keybindings, and extensions as they are adopted.
- Other app settings only where a portable supported format exists.

Do not copy entire application databases as an export. They can contain credentials, personal content, and machine-specific state.

## OmniWM style

Celestial 1.1.0 was installed from `github:OmniNull/OmniWM@v0.8.0` with no differences against its manifest at audit time. The active shell profile is `default`. Personal shell settings and wallpaper palette are managed; generated widget code and fonts are not copied to Git. Reinstall the style through OmniWM when needed.

## Scope of the foundation

Phase 1 adds Homebrew/chezmoi/Git foundations and a repeatable config restore. It does not enable OmniWM IPC, clipboard history, the Quake terminal, Remote Login, automatic agent approval, or additional productivity tools. Those remain deliberate future changes.
