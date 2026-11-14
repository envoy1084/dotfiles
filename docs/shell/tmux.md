# Projects and tmux

[← Previous: Git and parallel work](git.md) · [Docs index](../index.md) · [Next: Development and automation →](development.md)

[tmux documentation](https://github.com/tmux/tmux/wiki) · Homebrew: `tmux`.

Keep terminal sessions running while you detach. `work` creates or resumes a named project session with three windows: `main`, `agent`, `server`. All start in that project directory with an ordinary shell. Launch your chosen tools yourself.

```sh
work                        # choose dotfiles or a direct child of ~/Projects
work dotfiles
work my-project             # ~/Projects/my-project
work "/path/to/my project"  # an existing directory
tmux ls
```

Projects default to `~/Projects`. Set `export PROJECTS_DIR="$HOME/Developer"` in `~/.zprofile.local` for a different root, then open a new terminal. The picker lists direct child directories, including hidden ones; deep projects can be opened by path. Session names start with `work-`; name collisions get a path hash. Re-running `work` attaches to the existing session. Inside tmux it switches the current client.

## Keys

Press Ctrl+B, release, then press the listed key. This avoids taking shell or OmniWM shortcuts.

| After Ctrl+B | Action |
|---|---|
| `d` | Detach; session keeps running |
| `1` / `2` / `3` | Main / agent / server window |
| `c` | New window in the current directory |
| `n` / `p` | Next / previous window |
| `,` | Rename current window |
| `%` | Split left/right |
| `"` | Split top/bottom |
| Arrow | Select pane |
| `z` | Zoom/unzoom pane |
| `[` | Scroll/copy mode; `q` exits |
| `r` | Reload `~/.tmux.conf` |
| `?` | Full key help |

Mouse selection and scrolling are enabled. The status bar shows the session and windows in Tokyo Night colours. Windows start at 1. To finish a pane, exit its shell; Ctrl+B then `d` only detaches.

Sessions survive closing a terminal client; they do not survive a reboot or tmux server termination. There is no global tmux auto-start, session resurrection plugin, or automatic agent launch. Configuration: `configs/dot_tmux.conf` → `~/.tmux.conf`.

---

[← Previous: Git and parallel work](git.md) · [Docs index](../index.md) · [Next: Development and automation →](development.md)
