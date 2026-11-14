# Daily commands

[← Previous: Shell guide](index.md) · [Docs index](../index.md) · [Next: Yazi →](yazi.md)

Learn these first: `y`, `z`, `ll`, `lg`, `work`, `tools`, `how`, and Ctrl+R. Everything else stays in the guides and recipe picker.

## Navigation and help

| Command | Action |
|---|---|
| `how` / `how yazi` / `how git` | Read the daily guide or a topic in a Markdown pager; `q` quits |
| `how unknown-topic` | Search guide filenames with fzf |
| `tools` / `tools image` | Choose a local recipe, fill in its inputs, then review it at the prompt |
| `y [directory]` | Browse files; quitting returns the shell to the chosen directory |
| `z dotfiles` / `zi` | Jump to a visited directory / choose one |
| `cd -` / `..` / `...` | Previous directory / up one / up two levels |
| `ll` | Detailed listing with hidden files, icons and Git state |
| `lt` | Directory tree, two levels deep |
| `take "new project"` | Create a directory and enter it |
| `work` / `work dotfiles` | Choose or resume a project in tmux |

## Files and local utilities

| Command | Action |
|---|---|
| `pack archive.tar.gz ./folder` | Compress paths into the named archive |
| `unpack archive.tar.gz` | Extract using ouch’s automatic output folder; inspect with `ouch list` first |
| `toss ./unwanted.txt` | Move a selected path to macOS Trash with Homebrew trash |
| `ports` | Show listening TCP ports; process visibility depends on permissions |
| `lanip` / `copyip` | Show / copy IPv4 on the default network interface |
| `copypath [path]` | Copy an absolute path; defaults to the current directory |
| `serve [port]` | Serve the current directory at `http://127.0.0.1:8000`; Ctrl+C stops it |

`serve` uses available `python3` and binds to localhost. `lanip` reports the default interface, which may be a VPN interface; IPv6-only connections may have no IPv4 result. `toss` leaves `rm` unchanged. See [Git](git.md) for the complete Git shortcut table.

## Shell keyboard shortcuts

These belong to the shell prompt. Right Command belongs to [OmniWM](../omniwm.md); left Command belongs to [Ghostty](../ghostty.md). Foreground apps handle their own keys.

| Keys | Action |
|---|---|
| Ctrl+R | Atuin history search; Enter inserts, another Enter runs |
| Ctrl+G | Search local recipes and insert one for review |
| Ctrl+T | Select files/directories and insert escaped paths |
| Ctrl+/ in the file picker | Toggle preview |
| Tab | Complete commands, arguments and paths with fzf-tab |
| Up / Down | Search history matching the typed prefix |
| Right Arrow at end of input | Accept the autosuggestion |
| Option+Left / Right | Move a word backward / forward |
| Ctrl+A / E | Start / end of input |
| Ctrl+W / U | Delete previous word / input before cursor |
| Ctrl+L | Clear/redraw visible screen |
| Ctrl+C | Cancel input or interrupt foreground command |

Option+C is available; directory selection uses `zi`. Tab is owned by fzf-tab; use Ctrl+T for the dedicated file picker.

## First-day workflow

```sh
work dotfiles        # main, agent and server windows; no tools auto-launch
gs                   # check repository status
lg                   # review and stage work visually
how yazi             # read the file-manager shortcuts
tools                # find recipes by intent
```

Use Ctrl+B then `d` to leave a tmux session running. Learn a new tool when a task calls for it; the guide and picker remain your memory aid.

---

[← Previous: Shell guide](index.md) · [Docs index](../index.md) · [Next: Yazi →](yazi.md)
