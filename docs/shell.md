# Shell and terminal tools

Reference for the installed zsh setup and terminal tools. Commands use example paths; substitute files, projects, and hosts that exist for your task.

## Contents

- [Current setup](#current-setup)
- [Core shell tools](#core-shell-tools): [Starship](#starship), [fzf](#fzf), [zoxide](#zoxide), [zsh-autosuggestions](#zsh-autosuggestions), [zsh-syntax-highlighting](#zsh-syntax-highlighting), [ripgrep](#ripgrep), [fd](#fd), [bat](#bat), [jq](#jq)
- [Files and navigation](#files-and-navigation): [Yazi](#yazi), [eza](#eza), [dust](#dust), [trash](#trash), [ouch](#ouch)
- [Sessions and Git](#sessions-and-git): [tmux](#tmux), [LazyGit](#lazygit), [delta](#delta), [Worktrunk](#worktrunk), [tokei](#tokei)
- [Development and automation](#development-and-automation): [mise](#mise), [just](#just), [hyperfine](#hyperfine), [shfmt](#shfmt)
- [Help and history](#help-and-history): [tealdeer](#tealdeer), [navi](#navi), [Atuin](#atuin)
- [JSON and YAML](#json-and-yaml): [fx](#fx), [yq](#yq)
- [HTTP networking and cloud files](#http-networking-and-cloud-files): [xh](#xh), [doggo](#doggo), [gping](#gping), [mtr](#mtr), [Trippy](#trippy), [rclone](#rclone)
- [Media images and Markdown](#media-images-and-markdown): [FFmpeg](#ffmpeg), [glow](#glow), [ImageMagick](#imagemagick), [Chafa](#chafa)
- [System and terminal dashboard](#system-and-terminal-dashboard): [btop](#btop), [Fastfetch](#fastfetch)
- [Prompt and behaviour](#prompt-and-behaviour)
- [Shortcuts](#shortcuts)
- [Commands and aliases](#commands-and-aliases)
- [Configuration and restore](#configuration-and-restore)
- [Versions](#versions)

## Current setup

The prompt combines Starship's [Pure layout](https://starship.rs/presets/pure-preset) with [Tokyo Night colours](https://starship.rs/presets/tokyo-night) and the JetBrains Mono Nerd Font configured in [Ghostty](ghostty.md). [OmniWM](omniwm.md) continues handling windows/workspaces.

The 31 new tools are installed and recorded in Brewfile. Existing shell behaviour is preserved: fzf owns Control+R, standard commands/aliases remain unchanged, and new tools do not install global shortcuts. Atuin history recording, mise activation/runtimes, Worktrunk shell integration, cloud remotes, and services are separate configuration steps.

Package-name mappings: delta → git-delta; tealdeer → tldr; Worktrunk → wt; Trippy → trip; ImageMagick → magick. The requested fxx and imageemagisk were interpreted as fx and ImageMagick.

## Core shell tools

### Starship

[Project / documentation](https://starship.rs/). Compact two-line prompt with Tokyo Night colours, Git state, command results, and relevant runtime versions.

```sh
starship explain
starship timings
starship --version
```

### fzf

[Project / documentation](https://github.com/junegunn/fzf). Fuzzy file selection and history search. Control+R and Control+T are already configured.

```sh
fzf
fd --type f | fzf
fzf --help
```

### zoxide

[Project / documentation](https://github.com/ajeetdsouza/zoxide). Jump to frequently visited directories.

```sh
z dotfiles
zi
zoxide query --list
```

### zsh-autosuggestions

[Project / documentation](https://github.com/zsh-users/zsh-autosuggestions). Suggest commands from history while typing. Accept with Right Arrow at the end of input.

Enabled through `configs/dot_zshrc`; no separate executable or global shortcut.

### zsh-syntax-highlighting

[Project / documentation](https://github.com/zsh-users/zsh-syntax-highlighting). Colour command-line syntax while typing. Loaded as the last zsh plugin.

Enabled through `configs/dot_zshrc`; no separate executable or global shortcut.

### ripgrep

[Project / documentation](https://github.com/BurntSushi/ripgrep). Search project text; executable: rg.

```sh
rg TODO .
rg --files
rg -n 'pattern' src
```

### fd

[Project / documentation](https://github.com/sharkdp/fd). Find paths by name; also powers the configured file picker.

```sh
fd settings
fd --type f --extension md
fd --hidden --exclude .git
```

### bat

[Project / documentation](https://github.com/sharkdp/bat). Read files with highlighting and line numbers; uses the terminal ANSI palette.

```sh
bat README.md
bat --paging=never path/to/file
bat --list-themes
```

### jq

[Project / documentation](https://jqlang.org/). Query, format, and transform JSON.

```sh
jq '.' data.json
jq '.name' package.json
printf '{"ok":true}' | jq '.ok'
```

## Files and navigation

### Yazi

[Project / documentation](https://yazi-rs.github.io) · Homebrew: `yazi`.

Browse and manage files with a terminal interface, selection, search, and previews.

```sh
yazi
yazi ~/Downloads
yazi --help
```

Use arrow keys to start navigating and q to quit. Image/video/archive/PDF previews depend on the available helpers; FFmpeg is installed, while optional PDF/archive helpers can be added later.

### eza

[Project / documentation](https://eza.rocks) · Homebrew: `eza`.

Rich directory listings with icons, file metadata, Git state, and tree views.

```sh
eza -lah --icons
eza --tree --level=2
eza -lah --git
```

Run eza explicitly; the existing ll alias remains ls -lah.

### dust

[Project / documentation](https://github.com/bootandy/dust) · Homebrew: `dust`.

Find large files and directories using a readable disk-usage summary.

```sh
dust .
dust -d 2 ~/Downloads
dust --help
```

### trash

[Project / documentation](https://hasseg.org/trash/) · Homebrew: `trash`.

Move selected files into macOS Trash so they can be recovered through Finder.

```sh
"$(brew --prefix trash)/bin/trash" ./unwanted-file.txt
"$(brew --prefix trash)/bin/trash" ./old-folder
```

macOS also provides `/usr/bin/trash`, so Homebrew installs this version keg-only. The examples explicitly select the Homebrew binary. Files can be recovered through Finder; `rm` and your PATH have not been changed.

### ouch

[Project / documentation](https://github.com/ouch-org/ouch) · Homebrew: `ouch`.

Compress, decompress, and inspect archives through one interface.

```sh
ouch compress ./folder archive.tar.gz
ouch decompress archive.tar.gz
ouch list archive.tar.gz
```

Archive commands read or create the named archive and output files. Use your own paths.

## Sessions and Git

### tmux

[Project / documentation](https://tmux.github.io/) · Homebrew: `tmux`.

Keep named terminal sessions available when you detach or close their client window.

```sh
tmux new -s work
tmux ls
tmux attach -t work
```

Default prefix: Control+B, then d to detach, c for a new window, % to split left/right, and " to split top/bottom. Sessions depend on the machine/server remaining running. No auto-start or new global shortcuts are configured.

### LazyGit

[Project / documentation](https://github.com/jesseduffield/lazygit/) · Homebrew: `lazygit`.

Review diffs, stage changes, switch branches, and manage commits through an interactive Git interface.

```sh
lazygit
lazygit -p ~/dotfiles
lazygit --help
```

Run inside a repository; use in-app help for the available actions. Installing does not change your Git settings.

### delta

[Project / documentation](https://dandavison.github.io/delta/) · Homebrew: `git-delta`.

Display highlighted Git diffs and compare files. Homebrew package: git-delta; executable: delta.

```sh
git -c core.pager=delta diff
git diff | delta --paging=never
delta old.txt new.txt
```

The first command selects delta for that invocation only. The shared Git pager has not been changed.

### Worktrunk

[Project / documentation](https://worktrunk.dev) · Homebrew: `worktrunk`.

Manage Git worktrees for independent branches and parallel agent tasks. Executable: wt.

```sh
wt list
wt switch --help
wt switch --create feature-demo
```

wt list works immediately. Parent-shell directory switching needs Worktrunk shell integration, which is not enabled in this install-only phase. The last example creates a branch/worktree when used in a repository.

### tokei

[Project / documentation](https://github.com/XAMPPRocky/tokei) · Homebrew: `tokei`.

Summarise source-code size by language.

```sh
tokei .
tokei src
tokei --help
```

## Development and automation

### mise

[Project / documentation](https://mise.jdx.dev/) · Homebrew: `mise`.

Manage project-specific runtime/tool versions and execute commands with those tools.

```sh
mise ls
mise use --pin node@lts
mise exec -- node --version
```

Only mise itself is installed. The second example downloads a runtime and writes the current project config when you choose to run it; mise exec works without interactive shell activation. No global runtimes or PATH activation were added.

### just

[Project / documentation](https://just.systems) · Homebrew: `just`.

Keep named project commands in a justfile and run them consistently.

```sh
just --list
just --dry-run build
just build
```

Run from a project with a justfile; build is an example recipe name. This does not replace the dotfiles setup wrapper.

### hyperfine

[Project / documentation](https://github.com/sharkdp/hyperfine) · Homebrew: `hyperfine`.

Benchmark commands, including warm-up runs and structured result output.

```sh
hyperfine 'sleep 0.1'
hyperfine --warmup 2 'printf hello'
hyperfine --export-json results.json 'sleep 0.1'
```

Commands are executed repeatedly. Benchmark commands whose repeated execution is appropriate.

### shfmt

[Project / documentation](https://github.com/mvdan/sh) · Homebrew: `shfmt`.

Format shell scripts and inspect formatting differences.

```sh
shfmt -d script.sh
shfmt -w script.sh
shfmt --help
```

-d shows a diff; -w rewrites the file. Continue using zsh -n to validate zsh configuration syntax.

## Help and history

### tealdeer

[Project / documentation](https://tealdeer-rs.github.io/tealdeer/) · Homebrew: `tealdeer`.

Read concise command examples from tldr pages. Executable: tldr.

```sh
tldr --update
tldr tar
tldr --list
```

The update command downloads the local documentation cache.

### navi

[Project / documentation](https://github.com/denisidoro/navi) · Homebrew: `navi`.

Search interactive command cheatsheets and fill their parameters.

```sh
navi
navi --print
navi --query git
```

First use may ask you to choose/add a cheatsheet collection. --print displays the selected command rather than executing it. No shell widget or shortcut has been added.

### Atuin

[Project / documentation](https://atuin.sh/) · Homebrew: `atuin`.

Store and search richer command history, with optional synchronisation.

```sh
atuin --help
atuin search 'git'
atuin stats
```

Installed only: fzf still owns Control+R. Existing zsh history is not imported into Atuin, no history hooks are enabled, and no sync account is configured. Search/stats become useful after an intentional import or activation.

## JSON and YAML

### fx

[Project / documentation](https://fx.wtf) · Homebrew: `fx`.

Interactively browse JSON and apply expressions to structured data. This is the JSON viewer requested as fxx.

```sh
fx package.json
printf '{"name":"Mac","items":[1,2]}' | fx
fx data.json '.name'
```

### yq

[Project / documentation](https://github.com/mikefarah/yq) · Homebrew: `yq`.

Query and transform YAML and convert it to JSON. This is Mike Farah yq.

```sh
yq '.services' compose.yml
yq -o=json '.' config.yaml
yq '.app.port = 8080' config.yaml
```

These examples print results. Add in-place options only when you intend to edit the source file.

## HTTP networking and cloud files

### xh

[Project / documentation](https://github.com/ducaale/xh) · Homebrew: `xh`.

Make HTTP requests with readable request syntax and formatted responses.

```sh
xh GET https://httpbin.org/get
xh POST https://httpbin.org/post name=Mac
xh --help
```

The first two examples contact a public example service when run.

### doggo

[Project / documentation](https://doggo.mrkaran.dev/) · Homebrew: `doggo`.

Inspect DNS records with readable output and explicit resolver selection.

```sh
doggo example.com
doggo example.com MX
doggo example.com @1.1.1.1
```

### gping

[Project / documentation](https://github.com/orf/gping) · Homebrew: `gping`.

Plot ping latency interactively for one or more targets.

```sh
gping 1.1.1.1
gping 1.1.1.1 8.8.8.8
gping --help
```

Use Control+C to stop probing.

### mtr

[Project / documentation](https://www.bitwizard.nl/mtr/) · Homebrew: `mtr`.

Combine ping and traceroute to investigate a network path.

```sh
mtr --help
sudo mtr example.com
sudo mtr --report --report-cycles 10 example.com
```

Packet probing may require elevated privileges on macOS. Installation does not run these probes or change your network settings.

### Trippy

[Project / documentation](https://trippy.rs/) · Homebrew: `trippy`.

Inspect route hops and latency in an interactive diagnostic interface. Executable: trip.

```sh
trip --help
sudo trip example.com
sudo trip example.com -p tcp -P 443
```

Packet probing may require elevated privileges on macOS. These examples are manual diagnostics, not background monitors.

### rclone

[Project / documentation](https://rclone.org/) · Homebrew: `rclone`.

List and transfer files between local directories and supported cloud-storage providers.

```sh
rclone listremotes
rclone config
rclone copy ./folder remote:folder --dry-run
```

Create/authenticate a named remote before using remote:folder. The copy example is a preview. No cloud accounts, sync services, or backup jobs were configured; credentials remain outside Git. This macOS Homebrew build does not include the FUSE `mount` subcommand.

## Media images and Markdown

### FFmpeg

[Project / documentation](https://ffmpeg.org/) · Homebrew: `ffmpeg`.

Inspect, convert, trim, and extract audio/video; includes ffprobe.

```sh
ffprobe input.mp4
ffmpeg -i input.mp4 -vn output.m4a
ffmpeg -ss 00:00:10 -i input.mp4 -t 5 clip.mp4
```

These examples create output files. Codec/container compatibility depends on the input and chosen output.

### glow

[Project / documentation](https://github.com/charmbracelet/glow) · Homebrew: `glow`.

Render Markdown in the terminal.

```sh
glow README.md
glow -p docs/shell.md
printf "# Hello\n" | glow -
```

### ImageMagick

[Project / documentation](https://imagemagick.org) · Homebrew: `imagemagick`.

Batch-convert, resize, and inspect images. Executable: magick.

```sh
magick identify photo.jpg
magick photo.jpg -resize '1600x1600>' resized.jpg
magick input.png output.webp
```

These examples preserve the named input and create separate output files.

### Chafa

[Project / documentation](https://hpjansson.org/chafa/) · Homebrew: `chafa`.

Render images using terminal-supported graphics or character output.

```sh
chafa image.png
chafa --format symbols image.png
chafa --help
```

## System and terminal dashboard

### btop

[Project / documentation](https://github.com/aristocratos/btop) · Homebrew: `btop`.

Inspect CPU, memory, processes, disks, and network activity in a terminal dashboard.

```sh
btop
btop --help
```

Use q to quit. Available metrics depend on macOS and the build; no monitoring service is started.

### Fastfetch

[Project / documentation](https://github.com/fastfetch-cli/fastfetch) · Homebrew: `fastfetch`.

Display system information and a configurable terminal presentation.

```sh
fastfetch
fastfetch --list-presets
fastfetch --help
```

Run explicitly; it is not added to terminal startup.

## Prompt and behaviour

- Two lines: context first, input arrow second. Green arrow for success; red arrow and exit code for failure.
- Git branch, detached commit, rebase/merge state, changes, and ahead/behind counts. In status brackets, `!` means modified, `+` staged, `?` untracked, and `=` conflicted.
- Node, Bun, Python, Rust, and Go versions appear when detected and available. Runtime installation is separate.
- Command duration appears after two seconds. Remote/root identity and background-job counts appear when relevant.
- JetBrains Mono Nerd Font is configured in [Ghostty](ghostty.md).
- History is shared between terminals, deduplicated, and limited to 50,000 saved entries. A leading space excludes a command from saved history.
- Completion includes Homebrew tools, case-insensitive matching, and grouped menus.
- Homebrew API metadata refresh interval is one day (`HOMEBREW_API_AUTO_UPDATE_SECS=86400`); `brew update` remains available for an explicit refresh.
- Prompt/plugins load only in interactive terminals. Non-terminal agent commands keep plain output.
- bat uses the terminal's ANSI palette; fzf uses Tokyo Night colours. Ctrl+T previews files and lists directories. File searches respect ignore files and exclude `.git`.

## Shortcuts

These apply at the shell prompt. Right Command belongs to [OmniWM](omniwm.md); left Command belongs to [Ghostty](ghostty.md).

| Shortcut | Action |
|---|---|
| Control + R | Search history; Enter inserts the selected command, then Enter runs it |
| Control + T | Choose files/directories and insert escaped paths |
| Control + / inside the file picker | Toggle file preview |
| Right Arrow at the end of input | Accept the autosuggestion |
| Up / Down | Search history matching the current input prefix; supports multiline input |
| Tab | Complete commands, paths, and arguments; select ambiguous matches from a menu |
| `**` then Tab | fzf completion where supported; for example `cat **` then Tab |
| Option + Left / Right | Move backward / forward by a word |
| Control + A / E | Start / end of input |
| Control + W | Delete the previous word |
| Control + U | Delete input before the cursor |
| Control + L | Redraw/clear the visible screen |
| Control + C | Cancel current shell input or interrupt the foreground command |

fzf's Option+C directory shortcut is disabled; use `zi` instead. Foreground agents and editors handle their own input.

## Commands and aliases

| Command | Purpose |
|---|---|
| `z dotfiles` | Jump to a visited directory matching `dotfiles` |
| `zi` | Choose among visited directories using fzf |
| `cd -` | Return to the previous directory |
| `..` / `...` | Go up one / two directory levels |
| `ll` | `ls -lah` |
| `gs` | Short Git status including branch |
| `gd` | Git diff |
| `gl` | Last 15 Git commits, one line each |
| `rg TODO .` | Search project text |
| `fd settings` | Find matching paths |
| `bat path/to/file` | Read a file with highlighting |
| `jq '.name' package.json` | Extract a JSON field |

## Configuration and restore

| Source | Destination |
|---|---|
| `configs/dot_zprofile` | `~/.zprofile`; login environment and Homebrew PATH |
| `configs/dot_zshrc` | `~/.zshrc`; interactive behaviour and plugins |
| `configs/dot_config/starship.toml` | `~/.config/starship.toml`; prompt |
| `configs/dot_config/bat/config` | `~/.config/bat/config`; file display |

- `Brewfile` declares the core shell tools and all power tools in this guide. Restore through `./bootstrap --write` or `./setup packages --write` followed by `./setup apply --write`.
- Open a new Ghostty window to load shell changes. Starship config changes appear at subsequent prompts.
- Keep machine/work-specific additions in `~/.zprofile.local` or `~/.zshrc.local`, outside Git.
- History, completion caches, and zoxide's directory database stay local. Restore settings through chezmoi rather than copying these runtime files into the repo.
- Preview with `./setup diff`, then apply with `./setup apply --write`. Check shell syntax and config drift with `./doctor`.

## Versions

Recorded 2026-11-14; installed package versions, not pins. Use `brew list --versions` to inspect later changes.

| Component | Version |
|---|---|
| macOS zsh | 5.9 |
| starship | 1.27.0 |
| fzf | 0.75.0 |
| zoxide | 0.10.0 |
| zsh-autosuggestions | 0.7.1 |
| zsh-syntax-highlighting | 0.8.0 |
| ripgrep | 15.2.0 |
| fd | 10.5.2 |
| bat | 0.26.1 |
| jq | 1.8.2 |
| yazi | 26.9.1 |
| eza | 0.23.5 |
| dust | 1.2.7 |
| trash | 0.9.2 |
| ouch | 0.8.3 |
| tmux | 3.8 |
| lazygit | 0.66.3 |
| git-delta | 0.20.1 |
| worktrunk | 0.81.0 |
| tokei | 15.0.0 |
| mise | 2026.11.8 |
| just | 1.59.0 |
| hyperfine | 2.0.0 |
| shfmt | 3.14.1 |
| tealdeer | 1.9.1 |
| navi | 2.24.0 |
| atuin | 18.24.8 |
| fx | 40.0.1 |
| yq | 4.54.3 |
| xh | 0.26.3 |
| doggo | 1.4.2 |
| gping | 1.21.0 |
| mtr | 0.96 |
| trippy | 0.13.0 |
| rclone | 1.76.0 |
| ffmpeg | 9.0.2_1 |
| glow | 3.0.0 |
| imagemagick | 7.1.2-35 |
| chafa | 1.18.3_1 |
| btop | 1.4.8 |
| fastfetch | 2.71.0 |
