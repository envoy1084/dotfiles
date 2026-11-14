import { Action, ActionPanel, Alert, Clipboard, closeMainWindow, confirmAlert, Detail, Form, Icon, List, open, showToast, Toast, useNavigation } from "@raycast/api";
import { execFile } from "node:child_process";
import { readFileSync } from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";
import { useEffect, useState } from "react";

const config = join(homedir(), ".config/raycast");
const settings = JSON.parse(readFileSync(join(config, "settings.json"), "utf8")) as { dotfiles_root: string };
const root = settings.dotfiles_root;

export function backend<T = unknown>(command: string, action = "", payload: object = {}, flags: string[] = []): Promise<T> {
  return new Promise((resolve, reject) => {
    const child = execFile("/usr/bin/python3", [join(config, "mac-tools.py"), command, ...(action ? [action] : []), ...flags],
      { timeout: 660_000, maxBuffer: 8 * 1024 * 1024 }, (error, stdout, stderr) => {
        try {
          const result = JSON.parse(stdout) as { ok: boolean; data: T; error?: string };
          if (!result.ok) reject(new Error(result.error || "Command failed"));
          else resolve(result.data);
        } catch { reject(new Error(error?.message || stderr || "Invalid helper response")); }
      });
    child.stdin?.end(JSON.stringify(payload));
  });
}

const text = (value: unknown) => typeof value === "string" ? value : JSON.stringify(value, null, 2);
export async function perform(action: () => Promise<unknown>): Promise<void> {
  try { await action(); }
  catch (error) { await showToast({ style: Toast.Style.Failure, title: "Action failed", message: String(error) }); }
}

function useData<T>(load: () => Promise<T>, dependency = "") {
  const [data, setData] = useState<T>();
  const [error, setError] = useState("");
  const [generation, setGeneration] = useState(0);
  useEffect(() => {
    let active = true;
    load().then(value => { if (active) setData(value); }).catch(e => { if (active) setError(String(e)); });
    return () => { active = false; };
  }, [generation, dependency]);
  return { data, error, reload: () => { setData(undefined); setError(""); setGeneration(g => g + 1); } };
}

export function Output({ title, load }: { title: string; load: () => Promise<unknown> }) {
  const { data, error, reload } = useData(load);
  const value = data === undefined ? "" : text(data);
  return <Detail navigationTitle={title} isLoading={data === undefined && !error}
    markdown={error ? `**Action failed**\n\n${error}` : "```text\n" + value.replace(/```/g, "ˋˋˋ") + "\n```"}
    actions={<ActionPanel>
      <Action.CopyToClipboard title="Copy Result" content={value} />
      <Action.Paste title="Paste Result" content={value} />
      <Action title="Refresh" icon={Icon.ArrowClockwise} onAction={reload} shortcut={{ modifiers: ["cmd"], key: "r" }} />
    </ActionPanel>} />;
}

function Command({ title, command, action = "", payload = {}, confirm = false }: { title: string; command: string; action?: string; payload?: object; confirm?: boolean }) {
  const { push } = useNavigation();
  return <Action title={title} icon={Icon.Terminal} onAction={() => perform(async () => {
    if (confirm && !await confirmAlert({ title, message: "Run this action now?", primaryAction: { title: "Run", style: Alert.ActionStyle.Default } })) return;
    push(<Output title={title} load={() => backend(command, action, payload)} />);
  })} />;
}

function Link({ title, url }: { title: string; url: string }) {
  return <Action title={title} icon={Icon.Link} onAction={() => perform(async () => { await closeMainWindow(); await open(url); })} />;
}

export function Network() {
  const { data, error, reload } = useData(() => backend<Record<string, string>>("network"));
  return <List navigationTitle="Network" isLoading={!data && !error}>
    {error && <List.Item title="Could not inspect network" subtitle={error} />}
    {Object.entries(data || {}).map(([key, value]) => <List.Item key={key} title={({ ipv4: "Local IPv4", interface: "Active Interface", router: "Router", dns: "DNS Servers", hostname: "Hostname" } as Record<string, string>)[key]} subtitle={value} icon={Icon.Network}
      actions={<ActionPanel><Action.CopyToClipboard title="Copy Value" content={value} /><Action title="Refresh" onAction={reload} /></ActionPanel>} />)}
    <List.Section title="On Demand">
      <List.Item title="Public IP" subtitle="Makes a request to api.ipify.org" icon={Icon.Globe} actions={<ActionPanel><Command title="Get Public IP" command="public-ip" /></ActionPanel>} />
      <List.Item title="Listening TCP Ports" subtitle="Read-only process and port list" icon={Icon.Terminal} actions={<ActionPanel><Command title="Show Ports" command="ports" /></ActionPanel>} />
      <List.Item title="Network Quality Test" subtitle="Uses bandwidth; run only when needed" icon={Icon.Gauge} actions={<ActionPanel><Command title="Run Network Quality Test" command="quality" confirm /></ActionPanel>} />
      <List.Item title="Wi-Fi Settings" icon={Icon.Gear} actions={<ActionPanel><Link title="Open Wi-Fi Settings" url="x-apple.systempreferences:com.apple.wifi-settings-extension" /></ActionPanel>} />
      <List.Item title="Copy Selected Finder Paths" icon={Icon.Finder} actions={<ActionPanel><Action title="Copy Paths" onAction={() => perform(async () => { const value = await backend<string>("finder-paths"); await Clipboard.copy(value); await showToast({ title: "Paths copied" }); })} /></ActionPanel>} />
    </List.Section>
  </List>;
}

export function Projects() {
  const { data, error } = useData(() => backend<{ name: string; path: string }[]>("projects"));
  return <List navigationTitle="Projects" searchBarPlaceholder="Search projects…" isLoading={!data && !error}>
    {error && <List.Item title="Could not list projects" subtitle={error} />}
    {(data || []).map(p => <List.Item key={p.path} title={p.name} subtitle={p.path.replace(homedir(), "~")} icon={Icon.Folder}
      actions={<ActionPanel>
        {[["code", "Open in VS Code"], ["terminal", "Open in Ghostty"], ["work", "Open work/tmux Session"], ["github", "Open GitHub Repository"]].map(([action, title]) => <Action key={action} title={title} onAction={() => perform(async () => { await backend("project", action, { path: p.path }); await closeMainWindow(); })} />)}
        <Action.CopyToClipboard title="Copy Project Path" content={p.path} />
        <Action.ShowInFinder path={p.path} />
      </ActionPanel>} />)}
  </List>;
}

const transforms = [
  ["json-format", "JSON: Format"], ["json-minify", "JSON: Minify"], ["json-validate", "JSON: Validate"],
  ["json-yaml", "JSON → YAML"], ["yaml-json", "YAML → JSON"],
  ["base64-encode", "Base64: Encode"], ["base64-decode", "Base64: Decode"], ["url-encode", "URL: Encode"], ["url-decode", "URL: Decode"],
  ["jwt-decode", "JWT: Decode (UNVERIFIED)"], ["uuid", "Generate UUID"],
  ["unix-seconds", "Unix Seconds → UTC Date"], ["unix-milliseconds", "Unix Milliseconds → UTC Date"],
  ["date-seconds", "ISO Date → Unix Seconds"], ["date-milliseconds", "ISO Date → Unix Milliseconds"],
  ["upper", "UPPERCASE"], ["lower", "lowercase"], ["camel", "camelCase"], ["snake", "snake_case"], ["kebab", "kebab-case"], ["slug", "Slugify"], ["diff", "Compare Text in VS Code"],
];

export function Developer() {
  const [kind, setKind] = useState("json-format");
  const [input, setInput] = useState("");
  const [right, setRight] = useState("");
  const { push } = useNavigation();
  return <Form navigationTitle="Local Developer Tools" actions={<ActionPanel>
    <Action.SubmitForm title={kind === "diff" ? "Open Comparison" : "Transform"} onSubmit={() => perform(async () => {
      if (kind === "diff") {
        await backend("diff", "", { left: input, right }); await closeMainWindow();
      } else {
        const value = await backend("transform", kind, { text: input });
        push(<Output title={transforms.find(t => t[0] === kind)?.[1] || kind} load={() => Promise.resolve(value)} />);
      }
    })} />
    <Action title="Use Clipboard as Input" icon={Icon.Clipboard} onAction={() => perform(async () => { setInput(await Clipboard.readText() || ""); })} />
  </ActionPanel>}>
    <Form.Dropdown id="kind" title="Operation" value={kind} onChange={setKind}>{transforms.map(([value, title]) => <Form.Dropdown.Item key={value} value={value} title={title} />)}</Form.Dropdown>
    {kind !== "uuid" && <Form.TextArea id="input" title={kind === "diff" ? "Left Text" : "Input"} value={input} onChange={setInput} />}
    {kind === "diff" && <Form.TextArea id="right" title="Right Text" value={right} onChange={setRight} />}
    <Form.Description title="Local Processing" text="Input stays on this Mac. Copy or paste the result explicitly. JWT decoding does not verify the token. Diff files remain locally outside Git." />
  </Form>;
}

export function Awake() {
  const { data, error, reload } = useData(() => backend<{ active: boolean; remaining: string }>("awake", "status"));
  const remaining = Number(data?.remaining);
  const duration = remaining > 0 ? `${Math.ceil(remaining / 60)} minutes remaining` : remaining === 0 ? "Indefinite session" : remaining === -1 ? "Trigger-based session" : "App/date-based session";
  return <List navigationTitle="Amphetamine — Keep Awake" isLoading={!data && !error}>
    <List.Item title={error ? "Could not read status" : data?.active ? "Session Active" : "No Active Session"} subtitle={error || (data?.active ? duration : "")} icon={Icon.Info}
      actions={<ActionPanel><Action title="Refresh Status" onAction={reload} /></ActionPanel>} />
    {[30, 60].map(minutes => <List.Item key={minutes} title={`Keep Awake for ${minutes} Minutes`} subtitle="Display can sleep" icon={Icon.Moon}
      actions={<ActionPanel><Action title="Start Session" onAction={() => perform(async () => {
        const status = await backend<{ active: boolean }>("awake", "status");
        if (status.active && !await confirmAlert({ title: "Replace active Amphetamine session?", message: "Starting a new session ends the current session, including a trigger session.", primaryAction: { title: "Replace Session" } })) return;
        await backend("awake", String(minutes), {}, status.active ? ["--replace"] : []); reload(); await showToast({ title: `Awake for ${minutes} minutes` });
      })} /></ActionPanel>} />)}
    <List.Item title="End Current Session" subtitle="Triggers may start a new session" icon={Icon.Stop} actions={<ActionPanel><Action title="End Session" onAction={() => perform(async () => {
      if (!await confirmAlert({ title: "End the current Amphetamine session?", primaryAction: { title: "End Session", style: Alert.ActionStyle.Destructive } })) return;
      await backend("awake", "end"); reload();
    })} /></ActionPanel>} />
  </List>;
}

function RecordingForm() {
  const [kind, setKind] = useState("screen");
  const [target, setTarget] = useState("");
  const { data, error } = useData(() => backend<string>("cap", "targets", { kind: kind + "s" }), kind);
  let targets: { id: string; name?: string; title?: string }[] = [];
  try { const parsed = JSON.parse(data || "[]"); if (Array.isArray(parsed)) targets = parsed.filter(t => t.id !== undefined); } catch { /* Display an empty target list and the helper error. */ }
  useEffect(() => { try { const list = JSON.parse(data || "[]"); setTarget(Array.isArray(list) && list[0]?.id !== undefined ? String(list[0].id) : ""); } catch { setTarget(""); } }, [data, kind]);
  const { push } = useNavigation();
  return <Form navigationTitle="Start Cap Recording" actions={<ActionPanel>
    <Action.SubmitForm title="Start Recording" onSubmit={(values: { target: string; mic: string; systemAudio: boolean }) => perform(async () => {
      if (!values.target.trim()) throw new Error("Choose an available target; check Cap's screen recording permission if none appear.");
      if (!await confirmAlert({ title: "Start recording this target?", message: `${kind} ${values.target}. Microphone: ${values.mic || "off"}. System audio: ${values.systemAudio ? "on" : "off"}.`, primaryAction: { title: "Start Recording" } })) return;
      const output = await backend("cap", "start", { ...values, kind });
      await showToast({ title: "Recording started" });
      push(<Output title="Cap Recording" load={() => Promise.resolve(output)} />);
    })} />
  </ActionPanel>}>
    <Form.Dropdown id="kind" title="Target Type" value={kind} onChange={setKind}><Form.Dropdown.Item value="screen" title="Screen" /><Form.Dropdown.Item value="window" title="Window" /></Form.Dropdown>
    <Form.Dropdown id="target" title="Capture Target" value={target} onChange={setTarget}>{targets.map(t => <Form.Dropdown.Item key={String(t.id)} value={String(t.id)} title={t.name || t.title || `Target ${t.id}`} />)}</Form.Dropdown>
    {error && <Form.Description title="Target Error" text={error} />}
    <Form.TextField id="mic" title="Microphone" placeholder="Blank = off; enter a name from List Microphones" />
    <Form.Checkbox id="systemAudio" label="Capture system audio" defaultValue={false} />
    <Form.Description text="No camera and no upload. Studio projects are saved under ~/Movies/Cap. Stop only affects recordings tracked by these commands." />
  </Form>;
}

function ExportForm() {
  const { push } = useNavigation();
  return <Form navigationTitle="Export Cap Project" actions={<ActionPanel><Action.SubmitForm title="Export MP4" onSubmit={(values: { paths: string[] }) => perform(async () => {
    if (!values.paths?.[0]) throw new Error("Choose a .cap project directory");
    if (!await confirmAlert({ title: "Export selected project to MP4?", message: "The MP4 will be created beside the .cap project. Existing MP4 files are preserved.", primaryAction: { title: "Export MP4" } })) return;
    push(<Output title="Cap Export" load={() => backend("cap", "export", { path: values.paths[0] })} />);
  })} /></ActionPanel>}><Form.FilePicker id="paths" title="Cap Project" allowMultipleSelection={false} canChooseDirectories canChooseFiles /></Form>;
}

export function Capture() {
  return <List navigationTitle="Capture and Record">
    <List.Section title="Shottr">
      {[["ssa", "Capture Area"], ["ssrg", "Capture Window"], ["sss", "Scrolling Screenshot"], ["ssds", "Delayed Screenshot"], ["sso", "OCR"], ["ssc", "Edit Clipboard Image"]].map(([command, title]) => <List.Item key={command} title={title} icon={Icon.Camera} actions={<ActionPanel><Link title={title} url={`raycast://extensions/fernando_barrios/shottr/${command}`} /></ActionPanel>} />)}
    </List.Section>
    <List.Section title="Cap — Local Recording">
      <List.Item title="Open Cap" icon={Icon.Video} actions={<ActionPanel><Action.Open title="Open Cap" target="/Applications/Cap.app" /></ActionPanel>} />
      <List.Item title="Start Recording" subtitle="Choose target and audio explicitly" actions={<ActionPanel><Action.Push title="Configure Recording" target={<RecordingForm />} /></ActionPanel>} />
      <List.Item title="Recording Status" actions={<ActionPanel><Command title="Show Status" command="cap" action="status" /></ActionPanel>} />
      <List.Item title="Stop Our Recording" actions={<ActionPanel><Command title="Stop Tracked Recording" command="cap" action="stop" confirm /></ActionPanel>} />
      <List.Item title="Clear Stale Recording Tracking" subtitle="Only when Cap reports no active CLI recordings" actions={<ActionPanel><Command title="Clear Stale Tracking" command="cap" action="forget" confirm /></ActionPanel>} />
      {["screens", "windows", "mics"].map(kind => <List.Item key={kind} title={`List ${kind === "mics" ? "Microphones" : kind[0].toUpperCase() + kind.slice(1)}`} actions={<ActionPanel><Command title="List Targets" command="cap" action="targets" payload={{ kind }} /></ActionPanel>} />)}
      <List.Item title="Open Recordings Folder" actions={<ActionPanel><Command title="Open Folder" command="cap" action="folder" /></ActionPanel>} />
      <List.Item title="Export Cap Project to MP4" actions={<ActionPanel><Action.Push title="Choose Project" target={<ExportForm />} /></ActionPanel>} />
    </List.Section>
    <List.Section title="Dropover">
      <List.Item title="Add Finder Selection to Dropover" actions={<ActionPanel><Link title="Add Selection" url="raycast://extensions/jag-k/dropover/index" /></ActionPanel>} />
      <List.Item title="Add Clipboard to Dropover" actions={<ActionPanel><Link title="Add Clipboard" url="raycast://extensions/jag-k/dropover/add-from-clipboard" /></ActionPanel>} />
    </List.Section>
  </List>;
}

export function Dotfiles() {
  return <List navigationTitle="Dotfiles and Help">
    <List.Section title="Read-only Checks">
      {[["status", "Configuration Status"], ["diff", "Preview Configuration Diff"], ["doctor", "Setup Doctor"], ["missing", "Check Declared Packages"]].map(([action, title]) => <List.Item key={action} title={title} icon={Icon.Terminal} actions={<ActionPanel><Command title={title} command="dotfiles" action={action} /></ActionPanel>} />)}
    </List.Section>
    <List.Section title="Configuration">
      {[["Dotfiles", root], ["Brewfile", join(root, "Brewfile")], ["OmniWM Settings", join(homedir(), ".config/omniwm/settings.toml")], ["Ghostty Config", join(homedir(), "Library/Application Support/com.mitchellh.ghostty/config.ghostty")], ["VS Code Settings", join(homedir(), "Library/Application Support/Code/User/settings.json")]].map(([title, path]) => <List.Item key={title} title={title} icon={Icon.Gear} actions={<ActionPanel><Action.Open title="Open in VS Code" target={path} application="com.microsoft.VSCode" /><Action.CopyToClipboard title="Copy Path" content={path} /></ActionPanel>} />)}
    </List.Section>
    <List.Section title="Documentation">
      {[["Documentation Index", "index.md"], ["Raycast Shortcuts and Restore", "raycast.md"], ["OmniWM Shortcuts", "omniwm.md"], ["Ghostty Shortcuts", "ghostty.md"], ["Shell Daily Commands", "shell/daily.md"], ["Yazi Cheat Sheet", "shell/yazi.md"], ["Git Guide", "shell/git.md"], ["tmux Guide", "shell/tmux.md"]].map(([title, file]) => <List.Item key={file} title={title} icon={Icon.Book} actions={<ActionPanel><Action.Open title="Open Guide" target={join(root, "docs", file)} application="com.microsoft.VSCode" /></ActionPanel>} />)}
    </List.Section>
  </List>;
}

export function Hub() {
  const pages = [["Projects", "VS Code, Ghostty, GitHub and work/tmux", Projects], ["Network", "Copy IP, DNS, hostname and inspect ports", Network], ["Developer Tools", "JSON, YAML, encoding, dates and text", Developer], ["Capture and Record", "Shottr, Cap and Dropover", Capture], ["Keep Awake", "Amphetamine sessions", Awake], ["Dotfiles and Help", "Status, diff, doctor, configs and guides", Dotfiles]] as const;
  const apps = ["Slack", "Discord", "Telegram", "Signal", "Ghostty", "Helium", "Visual Studio Code", "Shottr", "Dropover", "Amphetamine", "Cap"];
  return <List navigationTitle="Mac Setup" searchBarPlaceholder="Find a tool, setting or workflow…">
    <List.Section title="Your Tools">{pages.map(([title, subtitle, Page]) => <List.Item key={title} title={title} subtitle={subtitle} icon={Icon.AppWindow} actions={<ActionPanel><Action.Push title={`Open ${title}`} target={<Page />} /></ActionPanel>} />)}</List.Section>
    <List.Section title="Raycast Essentials">{[["Clipboard History", "clipboard-history/clipboard-history"], ["File Search", "file-search/search-files"], ["Snippets", "snippets/search-snippets"], ["Quicklinks", "quicklinks/search-quicklinks"], ["Emoji and Symbols", "emoji-symbols/search-emoji-symbols"], ["My Schedule", "calendar/my-schedule"]].map(([title, path]) => <List.Item key={title} title={title} icon={Icon.MagnifyingGlass} actions={<ActionPanel><Link title={`Open ${title}`} url={`raycast://extensions/raycast/${path}`} /></ActionPanel>} />)}</List.Section>
    <List.Section title="Daily Apps">{apps.map(app => <List.Item key={app} title={app} icon={Icon.AppWindow} actions={<ActionPanel><Action.Open title={`Open ${app}`} target={`/Applications/${app}.app`} /></ActionPanel>} />)}</List.Section>
    <List.Section title="System">
      {[["lock", "Lock Screen"], ["display-sleep", "Sleep Displays"], ["dark-mode", "Toggle Dark Appearance"], ["trash", "Open Trash"]].map(([action, title]) => <List.Item key={action} title={title} icon={Icon.Gear} actions={<ActionPanel><Command title={title} command="system" action={action} confirm={action === "lock" || action === "display-sleep"} /></ActionPanel>} />)}
      {[["Sound Settings", "com.apple.Sound-Settings.extension"], ["Bluetooth Settings", "com.apple.BluetoothSettings"], ["Wi-Fi Settings", "com.apple.wifi-settings-extension"]].map(([title, pane]) => <List.Item key={title} title={title} icon={Icon.Gear} actions={<ActionPanel><Link title={title} url={`x-apple.systempreferences:${pane}`} /></ActionPanel>} />)}
    </List.Section>
  </List>;
}
