# JSON and YAML

[← Previous: History, recipes and completion](history-help.md) · [Docs index](../index.md) · [Next: Networking and cloud files →](networking.md)

Read, query and transform structured data. Use output redirection to a new file when saving a transformation.

### jq

[Project / documentation](https://jqlang.org/). Query, format, and transform JSON.

```sh
jq '.' data.json
jq '.name' package.json
printf '{"ok":true}' | jq '.ok'
```

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

---

[← Previous: History, recipes and completion](history-help.md) · [Docs index](../index.md) · [Next: Networking and cloud files →](networking.md)
