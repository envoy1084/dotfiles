# Working on these dotfiles

This repository manages the user's native macOS productivity and agent setup.

- Start with `./setup status` and `./setup check`.
- Read `manifest.json` before changing managed paths.
- Preview with `./setup apply --dry-run`; do not apply live settings just to validate a repository edit.
- Keep scope explicit. Do not install new tools, replace an app's installation channel, or enable disabled desktop features without a user request.
- Use the copy-and-backup workflow; desktop apps may rewrite config files and should not be assumed to preserve symlinks.
- Do not copy credentials, SSH keys, app databases, histories, browser profiles, agent sessions, or Keychain material.
- Keep personal paths portable. Record manual gaps honestly; a Brewfile is not a version lock.
- Keep AeroSpace out unless the user explicitly asks to restore it.
- Do not commit with an invented Git identity or create/push a remote without the user's request.
