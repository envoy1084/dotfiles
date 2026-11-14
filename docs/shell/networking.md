# Networking and cloud files

[← Previous: JSON and YAML](structured-data.md) · [Docs index](../index.md) · [Next: Media, images and Markdown →](media.md)

## Small daily helpers

| Command | Purpose |
|---|---|
| `ports` | Listening TCP ports and visible processes |
| `lanip` / `copyip` | Show / copy IPv4 on the default route's interface |
| `serve [port]` | Share the current directory over localhost HTTP; default 8000 |

Use `tools network` or `tools dns` for recipes. `serve` stops with Ctrl+C.


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

## Before using a cloud remote

Configure the provider you actually use with `rclone config`; keep credentials local. Start with listing and a dry-run, then choose whether to run the copy. macOS Homebrew rclone does not provide FUSE `mount` support.

```sh
rclone listremotes
rclone lsd remote:
rclone copy ./folder remote:backup/folder --dry-run --progress
```

Network probing tools may require elevated privileges. Run them against a host you choose; no privileged helper/service is installed by these dotfiles.

---

[← Previous: JSON and YAML](structured-data.md) · [Docs index](../index.md) · [Next: Media, images and Markdown →](media.md)
