# Ghostty

[Ghostty](https://ghostty.org/) is the terminal used for development and agents. References: [configuration](https://ghostty.org/docs/config), [options](https://ghostty.org/docs/config/reference), [shortcut actions](https://ghostty.org/docs/config/keybind/reference), [shell integration](https://ghostty.org/docs/features/shell-integration).

## Setup

| Setting | Value |
|---|---|
| Font | JetBrainsMono Nerd Font Mono, 14 pt; regular/bold/italic variants |
| Theme | TokyoNight Night; solid background |
| Padding | 10 pt horizontal, 8 pt vertical |
| Mouse | Hide pointer while typing |
| Option | Left Option sends Alt; right Option keeps macOS character input |
| Notifications | Quiet desktop notification after commands lasting over 30 seconds finish in an unfocused terminal |
| Window restore | Save window/tab/split structure and working directories |
| Shell integration | Automatic detection; new windows/tabs/splits inherit the current directory by default |
| Scrollback | Ghostty default: 50 MB |

Window restoration does not keep running commands or agents alive after quitting. Command-finish notifications require shell integration and a command returning to the shell; agent approval prompts need their own integration. Starship and other shell tools are configured separately.

## Modifiers and permissions

**Command below means left Command.** Right Command (`R`) is OmniWM's Hyper trigger: Control + Option + Command. Keep Control shortcuts available to the shell and agents.

- Grant Ghostty **Accessibility** in System Settings → Privacy & Security for its global shortcut. Keep Ghostty running to use it.
- Allow Ghostty notifications in System Settings → Notifications when macOS requests permission.
- [OmniWM](omniwm.md) owns workspace/window management and the Quake terminal placement.
- New bindings were checked against OmniWM and Ghostty. Raycast's custom global shortcuts could not be inspected; review them in Raycast if a shortcut is intercepted.

## Shortcuts

### Global and custom

| Shortcut | Action |
|---|---|
| R + Return | New Ghostty window from any app |
| Command + Shift + E | Equalise split sizes |
| Command + Shift + R | Rename current tab |
| Command + Shift + L | Export scrollback to a temporary file and open it in the default text editor |

The last three shortcuts apply inside Ghostty.

### Windows, tabs, and splits

These are retained Ghostty defaults.

| Shortcut | Action |
|---|---|
| Command + N / T | New window / tab |
| Command + 1–8 / 9 | Select tab 1–8 / last tab |
| Command + Shift + [ / ] | Previous / next tab |
| Control + Shift + Tab / Control + Tab | Previous / next tab |
| Command + D | Split right |
| Command + Shift + D | Split down |
| Command + [ / ] | Previous / next split |
| Command + Option + Arrow | Focus split in that direction |
| Command + Control + Arrow | Resize split in that direction |
| Command + Control + Equal | Equalise split sizes; alternative to Command + Shift + E |
| Command + Shift + Return | Zoom / unzoom focused split |
| Command + W | Close current terminal surface |
| Command + Shift + W | Close current window |
| Command + Q | Quit Ghostty |
| Command + Return | Toggle native fullscreen; use R + F for OmniWM fullscreen |

### Text, output, and settings

| Shortcut | Action |
|---|---|
| Command + C / V | Copy / paste |
| Command + F | Search output |
| Command + E | Search selected text |
| Command + G / Command + Shift + G | Next / previous search result |
| Command + Shift + F | Close search |
| Command + Up / Down | Jump to previous / next command prompt |
| Option + Left / Right | Move backward / forward by a word at the shell prompt |
| Command + Left / Right | Move to start / end of shell input |
| Command + Plus / Minus / 0 | Increase / decrease / reset font size |
| Command + Shift + P | Ghostty command palette |
| Command + comma | Open config |
| Command + Shift + comma | Reload config |
| Command + triple-click | Select a command's output; requires shell integration |
| Option + click | Move cursor at the shell prompt; requires shell integration |

## Configuration and restore

- Source: `configs/private_Library/Application Support/com.mitchellh.ghostty/config.ghostty`.
- Installed file: `~/Library/Application Support/com.mitchellh.ghostty/config.ghostty`.
- `Brewfile` declares `ghostty` and `font-jetbrains-mono-nerd-font`; `./setup packages --write` installs them.
- Preview with `./setup diff`; back up and apply with `./setup apply --write`, then reload Ghostty with Command + Shift + comma. Some settings apply to newly created terminals.
- Verify syntax with `ghostty +validate-config` and font discovery with `ghostty +list-fonts --family='JetBrainsMono Nerd Font Mono'`.
- If the installed font is missing from discovery, activate it through macOS Font Book. This Mac needed explicit Core Text registration of its regular/bold/italic/bold-italic files after the Homebrew install.
- Capture direct config edits with `chezmoi add "$HOME/Library/Application Support/com.mitchellh.ghostty/config.ghostty"`, then review `git diff`.

## Versions

Recorded 2026-11-14; installed versions, not package pins.

| Component | Version |
|---|---|
| Ghostty | 1.4.0 |
| JetBrains Mono Nerd Font Homebrew cask / Nerd Fonts release | 3.5.1 |
| OmniWM | 0.8.0 |
