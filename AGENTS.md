# Working on this Mac setup

This thread and repo are the ongoing native macOS productivity and agent setup. The user wants a small, understandable, reproducible configuration that grows with actual needs.

- Start with `./setup status` and `./setup check`; use `./doctor` for the full foundation check.
- Chezmoi is the only configuration manager. `configs/` is selected by `.chezmoiroot`; never reintroduce a parallel copy/symlink manifest.
- Use `./setup diff` and `./setup apply --dry-run` before applying. Repository edits alone do not authorize live changes. Apply live settings when the user's task requests them.
- `./setup apply --write` backs up changed existing managed files outside Git, then uses chezmoi's conflict checks. Never silently force conflicting local changes.
- Preserve existing settings when adding packages or migrating config unless the user requests a behavior change.
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
- The user has configured the GitHub remote. GitHub CLI sign-in is still separate; do not request a token or push unless the user resumes that work.
