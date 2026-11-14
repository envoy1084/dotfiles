# OmniWM

[← Previous: Mac setup documentation](index.md) · [Docs index](index.md) · [Next: Ghostty →](ghostty.md)

[OmniWM](https://github.com/OmniNull/OmniWM) is the native macOS window manager used here with five scrolling **niri** workspaces. Upstream: [shortcuts](https://github.com/OmniNull/OmniWM/blob/v0.8.0/website/src/content/docs/guides/keyboard-shortcuts.md), [settings](https://github.com/OmniNull/OmniWM/blob/v0.8.0/website/src/content/docs/config/settings-reference.md).

## Modifier

**R = hold right Command**, configured as OmniWM's Hyper trigger: Control + Option + Command. Shift is separate. Use **left Command** for normal Mac shortcuts; Option + Arrow and Option + Shift + Arrow are available for text navigation. R + Space is unassigned.

Grant OmniWM **Accessibility** and **Input Monitoring** in System Settings → Privacy & Security. On a new Mac, these permissions must be granted again. Ghostty's global new-window shortcut also needs **Ghostty Accessibility** permission and Ghostty running. Reload Ghostty's config with left Command + Shift + comma after editing it.

## Shortcuts

### Focus and workspaces

| Shortcut | Action |
|---|---|
| R + W / A / S / D | Focus up / left / down / right |
| R + Tab | Focus previous window |
| R + 1–5 | Switch to workspace 1–5 |
| R + Shift + 1–5 | Move window to workspace 1–5 |
| R + 0 | Return to previous workspace |
| R + O | Toggle overview |

### Move and arrange

| Shortcut | Action |
|---|---|
| R + Shift + A / D | Move the whole column left / right |
| R + Shift + W / S | Move window up / down within its column |
| R + [ / ] | Move window left / right across columns; consume/expel with stacking enabled |
| R + T | Toggle column tabs |
| R + Z / X | Previous / next column width preset: 33%, 50%, 67% |
| R + Minus / Equal | Shrink / grow column width by 5% |
| R + Shift + Minus / Equal | Shrink / grow window height by 5% |
| R + F | Toggle OmniWM fullscreen |
| R + Shift + F | Toggle full-width column |
| R + C | Center focused column |
| R + Shift + C | Center visible columns |
| R + Shift + B | Balance sizes |

### Floating and quick access

| Shortcut | Action |
|---|---|
| R + V | Toggle focused window between floating and tiled |
| R + Shift + V | Switch focus between floating and tiled windows |
| R + Q | Show / hide scratchpad 1 |
| R + Shift + Q | Assign focused window to scratchpad 1 |
| R + Grave (backtick) | Show / hide the built-in Ghostty Quake terminal |
| R + Escape | Pause / resume OmniWM shortcuts |

### Applications

| Shortcut | Action |
|---|---|
| R + Return | New Ghostty window; handled by Ghostty's global shortcut |
| R + E | Open / focus Visual Studio Code |
| R + B | Open / focus Helium |
| R + G | Open / focus T3 Code (Beta) |

Left Command + Space remains available for Raycast. Use left Command + W / Q for normal close / quit.

### Monitors and recovery

| Shortcut | Action |
|---|---|
| R + M / R + Shift + M | Focus next / previous monitor |
| R + Shift + Arrow | Move window to monitor in that direction |
| R + Shift + R | Rescue off-screen windows |

## Configuration and restore

- OmniWM: `configs/dot_config/omniwm/settings.toml` → `~/.config/omniwm/settings.toml`; changes reload automatically.
- Ghostty shortcut: `configs/private_Library/Application Support/com.mitchellh.ghostty/config.ghostty`.
- Preview with `./setup diff`; back up and apply with `./setup apply --write`.
- After changing OmniWM through its UI, capture with `chezmoi add ~/.config/omniwm/settings.toml` and review `git diff`.
- Current app settings are the source of truth on this Mac. Capture observed UI changes before applying other dotfiles work. The shell layout is also managed at `~/.config/omniwm/shell/shell.toml`; capture that specific file after changing shell widgets or the workspace bar.
- Keep all five workspaces on niri. Clipboard history and IPC remain disabled.
- Shell style: Celestial 1.1.0 from `github:OmniNull/OmniWM@v0.8.0`, profile `default`, Tokyo Night theme. Reinstall the style through OmniWM on a new Mac; generated widget code/fonts are outside this repo.
- Helium and T3 Code currently need separate installation; see the README restore notes.

## Versions

Recorded 2026-11-14; these describe the configured machine, not pinned package versions.

| Component | Version |
|---|---|
| OmniWM / config schema | 0.8.0 / 5 |
| Ghostty | 1.4.0 |
| Helium | 0.21.3.1 |
| T3 Code (Beta) | 0.1.9 |

---

[← Previous: Mac setup documentation](index.md) · [Docs index](index.md) · [Next: Ghostty →](ghostty.md)
