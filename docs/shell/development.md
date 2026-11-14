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

Personal Node, pnpm, Go and Rust defaults belong in the captured global mise config. Homebrew installs mise; mise owns these runtimes. Login shells expose shims for editors/agents, and interactive shells activate mise. Choose versions per project with `mise use --pin`, review its `mise.toml`, and commit that file alongside the code. Rust projects can declare their toolchain and components in `rust-toolchain.toml`.

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

Review a project's mise configuration before trusting it; project tasks and hooks can execute code. Hyperfine runs benchmark commands repeatedly, so benchmark commands should be suitable for repetition.

## Predictable project commands

This means keeping the commands to run a project in that project's own files, so people and agents can discover them. It does not require adding more global tools.

| Project | Example entry points |
|---|---|
| TypeScript | `pnpm dev`, `pnpm build`, `pnpm check`, `pnpm test`, defined in `package.json` |
| Rust | `cargo check`, `cargo test`, `cargo fmt`; an optional project `justfile` can group multiple checks |
| Go | `go build ./...`, `go test ./...`, `go vet ./...` |

Use the scripts and conventions the repository already has. When maintaining a project, document missing entry points and add a recipe only when it serves an actual workflow. No project repositories are modified as part of the Mac setup.

---

[← Previous: Projects and tmux](tmux.md) · [Docs index](../index.md) · [Next: History, recipes and completion →](history-help.md)
