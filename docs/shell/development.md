# Development and automation

[← Previous: Projects and tmux](tmux.md) · [Docs index](../index.md) · [Next: History, recipes and completion →](history-help.md)

Project runtimes belong in project config. General terminal helpers are installed globally through Homebrew.

### mise

[Project / documentation](https://mise.jdx.dev/) · Homebrew: `mise`.

Manage project-specific runtime/tool versions and execute commands with those tools.

```sh
mise ls
mise use --pin node@lts
mise exec -- node --version
```

Shell activation is enabled. No global runtimes are selected. Choose versions per project with `mise use`, review its `mise.toml`, and commit that project file alongside its code.

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

## Project setup example

```sh
cd ~/Projects/example
mise use node@lts            # installs/selects Node and writes project mise.toml
mise current
just --list                 # available tasks when the project has a justfile
```

Choose a runtime when a project needs it. No global Node/Python version is selected by these dotfiles. Review a project's mise configuration before trusting it; project tasks and hooks can execute code. Hyperfine runs benchmark commands repeatedly, so benchmark commands should be suitable for repetition.

---

[← Previous: Projects and tmux](tmux.md) · [Docs index](../index.md) · [Next: History, recipes and completion →](history-help.md)
