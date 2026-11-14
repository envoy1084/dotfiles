# Files and archives

[← Previous: Yazi](yazi.md) · [Docs index](../index.md) · [Next: Git and parallel work →](git.md)

Use `ll`, `lt`, `y`, `toss`, `pack` and `unpack` for frequent tasks. Use the underlying commands when you need extra options.

### eza

[Project / documentation](https://eza.rocks) · Homebrew: `eza`.

Rich directory listings with icons, file metadata, Git state, and tree views.

```sh
eza -lah --icons
eza --tree --level=2
eza -lah --git
```

`ll` lists details, hidden files, icons and Git state; `lt` shows a two-level tree. Standard `ls` keeps its usual behavior.

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

## Preview helpers

| Package | Purpose | Reference |
|---|---|---|
| poppler | PDF text and preview rendering (`pdftoppm`, `pdftotext`) | [Poppler](https://poppler.freedesktop.org/) |
| sevenzip | Archive listing/extraction (`7zz`) | [7-Zip](https://www.7-zip.org/) |
| resvg | SVG rendering | [resvg](https://github.com/linebender/resvg) |

```sh
pdftotext document.pdf -         # extract text to stdout
7zz l archive.zip               # list archive contents
resvg drawing.svg drawing.png   # render to a new PNG
```

These also support [Yazi previews](yazi.md). For text/path searching and highlighted reading, see [ripgrep, fd and bat](core.md).

---

[← Previous: Yazi](yazi.md) · [Docs index](../index.md) · [Next: Git and parallel work →](git.md)
