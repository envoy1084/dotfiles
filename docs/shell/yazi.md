# Yazi

[← Previous: Daily commands](daily.md) · [Docs index](../index.md) · [Next: Files and archives →](files.md)

[Documentation](https://yazi-rs.github.io/docs/quick-start/) · Homebrew: `yazi`.

Fast terminal file browsing with selection, previews and Git markers. Use `y` so quitting also changes the shell directory.

```sh
y
y ~/Downloads
```

## Shortcuts

Use arrow keys; the default letter bindings remain available if you later want them. Press `~` or F1 inside Yazi for its full current help.

| Keys | Action |
|---|---|
| Up / Down | Move selection |
| Left / Right | Parent directory / enter directory |
| Enter | Open selected file with its configured opener |
| Shift+Enter | Choose an opener interactively |
| Space | Toggle selection and move down |
| `v` / Escape | Visual selection / cancel selection or active mode |
| `y` | Copy selected files |
| `x` | Cut selected files |
| `p` | Paste copied/cut files |
| `d` | Move selection to Trash; review the confirmation |
| `r` / `a` | Rename / create file or directory (end directory name with `/`) |
| `.` | Toggle hidden files |
| `/` | Find within the current directory |
| `f` | Filter the current directory |
| `z` / Shift+`z` | Jump using fzf / zoxide |
| `q` | Quit; the `y` wrapper enters the final directory |
| `g` then `d` | Downloads |
| `g` then Shift+`d` | Documents |
| `g` then `p` | Projects (`~/Projects`) |
| `g` then `.` | Dotfiles checkout |

## Openers and previews

Text/code opens in VS Code (`code --wait`); audio/video opens in VLC; PDFs and images use macOS default apps. Existing Yazi defaults handle other types, including archives. Explicit opener choices are available with Shift+Enter.

FFmpeg supplies video thumbnails; poppler supplies PDF previews; sevenzip handles archives; resvg renders SVG. Yazi uses the terminal's available graphics protocol, with Chafa available as a fallback. Previews depend on the file type and content; encrypted or unsupported files may not preview.

The theme matches Tokyo Night. Natural sorting puts directories first; hidden files start hidden. The official [Git plugin](https://github.com/yazi-rs/plugins/tree/main/git.yazi) adds state markers. Its Lua file and licence are fetched by chezmoi from immutable commit `1ef5fe02a6122f8f3bb47a41056aab3f4b8598bf`; no plugin manager step is needed during restore.

## Configuration

Managed files: `~/.config/yazi/{yazi.toml,keymap.toml,theme.toml,init.lua}`. Plugin files live under `~/.config/yazi/plugins/git.yazi/`. Edit source files under `configs/dot_config/yazi/`, preview and apply. Bookmarks are rendered for the restoring user's home directory; if you change `PROJECTS_DIR`, update the Projects bookmark too.

---

[← Previous: Daily commands](daily.md) · [Docs index](../index.md) · [Next: Files and archives →](files.md)
