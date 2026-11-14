# VS Code

[← Previous: Ghostty](ghostty.md) · [Docs index](index.md) · [Next: Shell guide →](shell/index.md)

[VS Code](https://code.visualstudio.com/) · Homebrew: `visual-studio-code`.

The captured setup uses your existing EnvoyOS theme, Material Icon Theme, Oxc TypeScript formatter, Rust extensions, TypeScript Native Preview, and other selected extensions. Existing preferences and snippets are preserved. Both editor and integrated terminal use **JetBrainsMono Nerd Font**; ligatures are enabled. Homebrew installs the font through `font-jetbrains-mono-nerd-font`.

## Settings and extensions

| Source under `configs/` | Destination |
|---|---|
| `private_Library/Application Support/Code/User/settings.json` | `~/Library/Application Support/Code/User/settings.json` |
| `private_Library/Application Support/Code/User/tasks.json` | User tasks |
| `private_Library/Application Support/Code/User/snippets/` | Your four user snippet files |
| `dot_config/vscode/extensions.txt` | `~/.config/vscode/extensions.txt`: extension IDs and captured versions |

Custom user keybindings were absent when captured. The capture command includes `keybindings.json` once you create it, and stops managing preference/snippet files you remove. Settings remain JSON with comments/trailing commas, as VS Code supports. The extension manifest records 32 installed extensions, including [EnvoyOS Theme](https://marketplace.visualstudio.com/items?itemName=envoy1084.envoyos-theme).

After editing settings, snippets, keybindings or extensions in VS Code:

```sh
cd ~/dotfiles
./setup vscode --capture                 # preview
./setup vscode --write --capture         # capture the current app configuration
git diff
```

Live app configuration is the source of truth on this Mac. Capture changes before applying other dotfiles work. Sign-in, Settings Sync state, WakaTime credentials, extension storage, workspace state and databases stay local. Settings Sync can update these files after sign-in; capture that resulting state when maintaining dotfiles.

## Restore

Bootstrap restores configuration, mise tools and missing extensions:

```sh
./bootstrap --dry-run
./bootstrap --write
```

For extensions alone:

```sh
./setup vscode                          # preview missing extensions
./setup vscode --write                  # install missing extensions at recorded versions
```

Existing installed versions and additional extensions are preserved. Capture again after updating or removing extensions. Restore needs network access and the recorded Marketplace releases to remain available. VS Code sign-in remains a per-Mac step.

Runtime discovery uses mise shims in the login profile and full mise activation in interactive terminals. Restart VS Code after the login environment changes. Use `mise exec -- <command>` in scripts or agents whose launcher does not inherit that environment. See [mise editor integration](https://mise.jdx.dev/ide-integration.html).

## Versions

Recorded 2026-11-14: VS Code 1.146.0, JetBrains Mono Nerd Font 3.5.1. Individual extension versions are in `configs/dot_config/vscode/extensions.txt`.

---

[← Previous: Ghostty](ghostty.md) · [Docs index](index.md) · [Next: Shell guide →](shell/index.md)
