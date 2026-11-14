# Daily apps

[← Previous: VS Code](vscode.md) · [Docs index](index.md) · [Next: Shell guide →](shell/index.md)

## Selected apps

| App | Purpose | Installation declaration |
|---|---|---|
| [Slack](https://slack.com/downloads/mac) | Workspaces, messaging and meetings | `cask "slack"` |
| [Discord](https://discord.com/download) | Communities, messaging and voice | `cask "discord"` |
| [Telegram for macOS](https://macos.telegram.org/) | macOS-focused Telegram client | `cask "telegram"` |
| [Signal](https://signal.org/download/macos/) | Messaging linked to your phone | `cask "signal"` |
| [Shottr](https://shottr.cc/) | Screenshots, annotation and OCR | `cask "shottr"` |
| [Dropover](https://dropoverapp.com/) | Temporary drag-and-drop file shelves | `mas "Dropover", id: 1355679052` |
| [Amphetamine](https://apps.apple.com/app/id937984704) | On-demand keep-awake sessions | `mas "Amphetamine", id: 937984704` |
| [Cap](https://cap.so/) | Screen recording and sharing | `cask "cap"` |

The Homebrew `telegram` cask selects Telegram for macOS. Shottr handles screenshots; Cap handles recordings. Existing login items, notifications and global shortcuts are preserved.

## Restore and updates

```sh
cd ~/dotfiles
./setup packages                         # preview
./setup packages --write                 # install missing Brewfile packages/apps
./doctor                                 # includes App Store app checks
```

Homebrew installs `mas`, the [Mac App Store CLI](https://github.com/mas-cli/mas). Sign in to the Mac App Store on each Mac. The account must have access to the apps; in-app purchases and licences are separate. `brew bundle` processes the App Store IDs in Brewfile. App Store installations may require administrator authentication.

For the two App Store downloads alone:

```sh
mas get 1355679052 937984704
```

Homebrew records package choices rather than exact app versions. Casks can lag official releases: Cap's cask was 0.6.2 when selected while its official download was 0.6.3. Keep the chosen Homebrew channel for reproducibility; review a channel change explicitly. Apps that offer their own updater or App Store updates can update separately.

## First launch

- Sign in to Slack, Discord and Telegram. Link Signal to Signal on your phone.
- Grant Shottr and Cap screen capture permissions when requested; microphone/camera access depends on the recording features you enable.
- Finish Dropover onboarding and choose any in-app licence upgrade yourself.
- Start Amphetamine sessions when needed; login items and automatic triggers remain your choices.

Current app settings are the source of truth during maintenance. Capture adopted preferences through supported exports or specific configuration files. Chat histories, account/session data, uploaded recordings, App Store receipts and credentials stay outside Git. Application preferences will be captured after onboarding and intentional configuration.

## Versions

Observed 2026-11-14 from the installed app bundles; these are not exact-version restore pins.

| App | Version |
|---|---|
| Slack | 4.53.287 |
| Discord | 0.0.422 |
| Telegram | 13.2.0 |
| Signal | 8.35.0 |
| Shottr | 1.10.0 |
| Dropover | 5.4.0 |
| Amphetamine | 5.3.2 |
| Cap | 0.6.2 |

---

[← Previous: VS Code](vscode.md) · [Docs index](index.md) · [Next: Shell guide →](shell/index.md)
