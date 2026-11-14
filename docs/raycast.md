# Raycast

[← Previous: VS Code](vscode.md) · [Docs index](index.md) · [Next: Daily apps →](daily-apps.md)

[Raycast](https://www.raycast.com/) is the launcher, clipboard manager and entry point for local Mac utilities. OmniWM owns windows and right Command; Shottr owns screenshots, Cap recording, Amphetamine keep-awake and Superwhisper dictation.

## Start here

The six favorites are Mac Setup, Clipboard History, Search Files, Open Project, Search Tabs and Search Snippets. Open Raycast and search these command names. The local extension adds keywords, so `ip`, `projects`, `json`, `awake`, `record`, `docs` and `doctor` also help find the relevant command.

| Command | What it does |
|---|---|
| **Mac Setup** | Categories, daily apps, built-ins and system actions |
| **Network Information** | Local IP, active interface, router, DNS, hostname, ports and on-demand diagnostics |
| **Open Project** | Projects in `~/Projects`, plus dotfiles; open in VS Code, Ghostty, GitHub or `work`/tmux |
| **Developer Tools** | Local JSON/YAML, encoding, JWT, UUID, date and case transformations; text diff |
| **Keep Awake** | Amphetamine status, 30/60-minute sessions and explicit end |
| **Capture and Record** | Shottr, Cap and Dropover controls |
| **Dotfiles and Help** | Read-only status/diff/doctor/package checks, configuration and guides |

Use arrows and Enter to navigate, Escape to go back and **Command K** for actions. Output views offer Copy and Paste separately. Use Command Y for Quick Look where supported.

## Native settings

| Setting | Chosen setup |
|---|---|
| Launcher | **Command Space**, verified in the hotkey recorder |
| Clipboard shortcut | **Control Command V**, verified in the hotkey recorder |
| Appearance | Follow System disabled; Raycast Dark |
| Login | Open at Login enabled |
| File scopes | `~/Projects`, `~/dotfiles`, `~/Downloads`, `~/Documents`, `~/Desktop` |
| File content search / hidden files | Off |
| Ignore files | On; managed `~/.rayignore` adds private and build-output exclusions |
| Clipboard | OCR enabled; Fast recognition; one-week retention |
| Clipboard exclusions | Preserve Passwords, Keychain Access and any additional personal exclusions |
| Universal Clipboard immediate collection | Off |
| Script folder | `~/.config/raycast/scripts` |

Calendar's Auto Join and Auto Transcribe were verified off. My Schedule remains available for accounts configured in macOS Calendar; calendar permissions and account setup are per Mac.

The settings JSON under `~/.config/raycast` supplies helper paths and records desired preferences; it does **not** directly change Raycast's app-managed settings. Native selections and the clipboard hotkey were set through the interface; on a new Mac, restore them through supported import or the settings UI. Do not enable Raycast Hyper/window shortcuts over OmniWM.

## Aliases

| Type in Raycast | Command |
|---|---|
| `clip` | Clipboard History |
| `files` | Search Files |
| `prs` | My Pull Requests |
| `setup` | Mac Setup |
| `ip` | Network Information |
| `projects` | Open Project |
| `devtools` | Developer Tools |
| `awake` | Keep Awake |
| `record` | Capture and Record |
| `docs` | Dotfiles and Help |
| `tabs` | Search Tabs |
| `gh` | Search Repositories |
| `snip` | Search Snippets |
| `links` | Search Quicklinks |
| `reviews` | GitHub Review Requests |
| `npm` | npm Package Search |
| `crates` | Crates Search |
| `rustdoc` | Rust API Search |
| `godoc` | Go Package Search |
| `mdn` | MDN Search |
| `ts` | TypeScript Handbook |
| `node` | Node Documentation |
| `pnpm` | pnpm Documentation |
| `rust` | Rust Book |
| `cargo` | Cargo Book |
| `mise` | mise Documentation |
| `ghostty` | Ghostty Documentation |
| `dotfiles` | Dotfiles Repository |
| `downloads` | Downloads |

Aliases were configured in the app. `aliases.json` records the choices for review and manual restore; it does not write Raycast databases.

## Clipboard, snippets and Quicklinks

Search **Clipboard History** to recover copied text, links, images and files. Use its action panel for plain-text paste, pause and clear commands. Normal paste preserves formatting. Clipboard history stays outside Git.

The imported Quicklinks include npm/crates/docs.rs/pkg.go.dev/MDN searches; TypeScript, Node, pnpm, Rust, Cargo, mise and Ghostty documentation; GitHub queues; dotfiles, Downloads, projects and local guides. Query links request `Query`. Web links use Helium; local Markdown/configuration opens in VS Code.

Imported short expansions:

| Keyword | Content |
|---|---|
| `;;email` | Captured Git identity email |
| `;;gh` | GitHub profile |
| `;;date` | ISO date |
| `;;time` | Timestamp |

Bug Report, Pull Request Summary, Review Request, Agent Handoff, Meeting Notes and Debugging Context are search-only templates, with no automatic expansion keyword. Code snippets remain in VS Code.

Quicklinks and Snippets were imported through Raycast's supported JSON import commands. Their source is rendered for the current Mac. After editing either in-app, use **Export Quicklinks** / **Export Snippets**, review the JSON, and capture portable changes into their templates. Preserve existing unrelated entries; imports can add duplicates if repeated carelessly.

## Installed extensions

| Extension | Useful commands / setup |
|---|---|
| [GitHub](https://www.raycast.com/raycast/github) | Repositories, PRs, issues and reviews. Authenticate separately; select SSH cloning and your project directory in-app. |
| [VS Code](https://www.raycast.com/thomas/visual-studio-code) | Recent projects and opening folders. Existing editor preferences are preserved. |
| [Helium](https://www.raycast.com/islamtayeb/helium) | Tabs, bookmarks, history and web search. Test tab switching with OmniWM before using workarounds. |
| [Shottr](https://www.raycast.com/fernando_barrios/shottr) | Area/window/scrolling/delayed screenshots, OCR and editing a clipboard image. **URL Scheme API** was enabled in Shottr → Advanced; keep Close Main Window enabled in the extension. |
| [Dropover](https://www.raycast.com/jag-k/dropover) | Add selected Finder files or clipboard content to a shelf. |
| [Can I Use](https://www.raycast.com/thomaslombart/can-i-use) | Browser feature support lookup. |

Store installation is verified from installed extension manifests. App-specific permissions, authenticated GitHub operations and browser/capture behavior need their own checks; installation alone does not verify these integrations end to end.

## Network and files

**Network Information** detects the default-route interface instead of assuming `en0`; it supports interface IPv4 fallback for tunnels. Local IP, interface, router, DNS and hostname have Copy actions. Public IP explicitly contacts `api.ipify.org`; Network Quality Test uses bandwidth and asks before running. Listening ports are read-only and never kill processes.

Standalone scripts add **Copy LAN IP**, **Copy Public IP**, **Copy Hostname**, **Copy Selected Finder Paths**, **Show Listening Ports** and **Setup Doctor** to Root Search. Select files in Finder before copying paths. The shell's `lanip` / `copyip` share the network backend when installed.

`~/.rayignore` excludes credentials, agent state, Library, research, caches, node_modules, Rust target and build outputs. File Search has content search disabled. Review per-folder privacy permissions after restoring.

## Development and projects

Developer Tools accepts manually entered text or an explicit **Use Clipboard as Input** action. It never automatically reads clipboard input or sends transformations to a cloud service.

- JSON format, minify and validate; JSON ↔ YAML through the existing `yq`.
- Base64 and URL encode/decode.
- JWT header/payload decode, labelled **UNVERIFIED**: no signature, issuer, audience or expiry validation.
- UUID generation.
- Unix seconds/milliseconds ↔ ISO date; ISO input must include a timezone.
- Upper/lower/camel/snake/kebab case and slugify.
- Two-text comparison in VS Code. Local comparison files are overwritten on the next comparison and remain outside Git under `~/Library/Application Support/dotfiles/raycast/` until removed.

Opening a project in Ghostty was exercised successfully. Project actions use the existing shell `work` helper for tmux sessions; they do not launch agents or services. Project command standardization remains deferred. Helper processes set a minimal Homebrew/mise PATH and do not source interactive shell initialization.

## Capture and keep-awake

**Capture and Record** links to Shottr and Dropover and exposes the bundled Cap CLI. Choose a screen/window from the target picker, and choose microphone/system audio explicitly. List Microphones provides the device names. Camera and upload are absent. Local Studio projects are written to `~/Movies/Cap`.

**Stop Our Recording** uses the ID tracked by these commands, not an arbitrary recording. If Cap returns an unrecognized ID shape or a recording is stopped elsewhere, inspect status and finish cleanup in Cap. Clear Stale Recording Tracking removes only our metadata and only when Cap reports no active CLI recordings. Recording start/stop/export are implemented but were not exercised against your screen during setup. Export preserves existing MP4 files and renders beside the chosen `.cap` project.

**Keep Awake** shows session status and offers 30/60 minutes with display sleep allowed. Starting while another session is active asks before replacing it. End Session also asks; an Amphetamine trigger can start a new session afterward. Status was checked without starting a session during setup.

## Reproducibility

| Source under `configs/` | Purpose |
|---|---|
| `dot_config/raycast/mac-setup/` | Seven-command local extension, assets, pinned dependencies and lockfile |
| `dot_config/raycast/executable_mac-tools.py` | Shared local backend |
| `dot_config/raycast/scripts/` | Searchable executable script commands |
| `dot_config/raycast/{settings,quicklinks,snippets}.json.tmpl` | Portable helper settings and content |
| `dot_config/raycast/extensions.json` | Selected Store extension manifest |
| `dot_rayignore` | File Search exclusions |

```sh
cd ~/dotfiles
./setup raycast                 # preview local extension restore
./setup raycast --write         # locked install, typecheck, build/import; stops watcher
./setup raycast --check         # portable files and installed extension inventory
./doctor
```

Bootstrap includes local extension restoration after mise/VS Code. First launch Raycast and finish onboarding on a new Mac. Restore Store extensions from the manifest, register the script folder, import Quicklinks/Snippets, and restore or configure native settings through the supported interface. Finish service sign-ins and macOS permissions separately.

For native preferences, aliases, hotkeys and other app-managed state, use **Export Settings & Data** / **Import Settings & Data**. Full `.rayconfig` exports are encrypted and can include clipboard, notes and AI data: store them outside Git and keep the passphrase separately. Scheduled exports and custom themes are Pro features; the setup does not purchase a plan. No Raycast databases, encryption keys, histories or credentials are managed. See [Raycast export documentation](https://manual.raycast.com/import-export).

During setup, full private machine backup remains deferred as requested. Research, audit captures and disposable checks stay in ignored `research/`.

## Versions and verification

2026-11-14: Raycast 2.12.1.0; local extension uses `@raycast/api` 2.12.1, React 19.3.1 and TypeScript 5.9.3. Exact dependency graph is in `pnpm-lock.yaml`. Setup validates TypeScript and the production build; doctor inspects portable files and installed extension names without reading app databases.

---

[← Previous: VS Code](vscode.md) · [Docs index](index.md) · [Next: Daily apps →](daily-apps.md)
