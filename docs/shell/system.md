# System overview

[← Previous: Media, images and Markdown](media.md) · [Docs index](../index.md) · [Next: Core shell and prompt →](core.md)

Open monitoring tools when needed; none auto-starts in every shell.

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

---

[← Previous: Media, images and Markdown](media.md) · [Docs index](../index.md) · [Next: Core shell and prompt →](core.md)
