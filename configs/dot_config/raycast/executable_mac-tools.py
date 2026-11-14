#!/usr/bin/python3
"""Local Raycast helpers. JSON in/out; no shell evaluation or interactive rc loading."""
import argparse
import base64
from datetime import datetime, timezone
import ipaddress
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys
import urllib.parse
import uuid

HOME = Path.home()
CONFIG = HOME / ".config/raycast"
STATE = HOME / "Library/Application Support/dotfiles/raycast"
CAP = "/Applications/Cap.app/Contents/MacOS/cap-cli"
os.environ["PATH"] = ":".join([str(HOME / ".local/share/mise/shims"), "/opt/homebrew/bin", "/usr/local/bin", "/usr/bin", "/bin", "/usr/sbin", "/sbin"])


def run(argv, stdin=None, timeout=30, check=True):
    result = subprocess.run([str(a) for a in argv], input=stdin, text=True,
                            capture_output=True, timeout=timeout)
    if check and result.returncode:
        raise ValueError((result.stderr or result.stdout or "Command failed").strip()[:2000])
    return result.stdout.strip()


def settings():
    return json.loads((CONFIG / "settings.json").read_text())


def root():
    return Path(settings()["dotfiles_root"]).expanduser()


def network():
    route = run(["/sbin/route", "-n", "get", "default"], check=False)
    interface = re.search(r"interface:\s*(\S+)", route)
    gateway = re.search(r"gateway:\s*(\S+)", route)
    interface = interface.group(1) if interface else ""
    ipv4 = run(["/usr/sbin/ipconfig", "getifaddr", interface], check=False) if interface else ""
    # Tunnel interfaces may not be understood by ipconfig. Read that interface's inet address.
    if interface and not ipv4:
        config = run(["/sbin/ifconfig", interface], check=False)
        match = re.search(r"\binet\s+(\d+\.\d+\.\d+\.\d+)", config)
        ipv4 = match.group(1) if match else ""
    dns = run(["/usr/sbin/scutil", "--dns"], check=False)
    servers = list(dict.fromkeys(re.findall(r"nameserver\[\d+\]\s*:\s*(\S+)", dns)))
    return {"interface": interface or "Disconnected", "ipv4": ipv4 or "Unavailable",
            "router": gateway.group(1) if gateway else "Unavailable",
            "dns": ", ".join(servers) or "Unavailable",
            "hostname": run(["/bin/hostname"])}


def transform(kind, text):
    if kind in ("json-format", "json-minify", "json-validate"):
        parsed = json.loads(text)
        if kind == "json-validate":
            return "Valid JSON"
        return json.dumps(parsed, ensure_ascii=False, indent=2 if kind == "json-format" else None,
                          separators=None if kind == "json-format" else (",", ":"))
    if kind == "json-yaml":
        json.loads(text)
        return run(["yq", "-P", "-p=json", "."], text)
    if kind == "yaml-json":
        return run(["yq", "-o=json", "."], text)
    if kind == "base64-encode":
        return base64.b64encode(text.encode()).decode()
    if kind == "base64-decode":
        return base64.b64decode("".join(text.split()), validate=True).decode()
    if kind == "url-encode":
        return urllib.parse.quote(text, safe="")
    if kind == "url-decode":
        return urllib.parse.unquote(text)
    if kind == "jwt-decode":
        parts = text.strip().split(".")
        if len(parts) != 3:
            raise ValueError("Expected a three-part JWT. This command does not verify signatures.")
        decoded = [json.loads(base64.urlsafe_b64decode(p + "=" * (-len(p) % 4))) for p in parts[:2]]
        return json.dumps({"warning": "UNVERIFIED: signature, issuer, audience and expiry not validated",
                           "header": decoded[0], "payload": decoded[1]}, indent=2, ensure_ascii=False)
    if kind == "uuid":
        return str(uuid.uuid4())
    if kind in ("unix-seconds", "unix-milliseconds"):
        stamp = float(text.strip()) / (1000 if kind.endswith("milliseconds") else 1)
        return datetime.fromtimestamp(stamp, timezone.utc).isoformat()
    if kind in ("date-seconds", "date-milliseconds"):
        date = datetime.fromisoformat(text.strip().replace("Z", "+00:00"))
        if date.tzinfo is None:
            raise ValueError("Include a timezone, for example 2026-11-14T12:00:00+05:30.")
        return str(int(date.timestamp() * (1000 if kind.endswith("milliseconds") else 1)))
    if kind == "upper":
        return text.upper()
    if kind == "lower":
        return text.lower()
    words = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", text)
    words = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1 \2", words)
    words = re.findall(r"[^\W_]+", words.lower())
    if kind in ("kebab", "slug"):
        return "-".join(words)
    if kind == "snake":
        return "_".join(words)
    if kind == "camel":
        return "" if not words else words[0] + "".join(w.title() for w in words[1:])
    raise ValueError("Unknown transformation")


def applescript(script, *args):
    return run(["/usr/bin/osascript", "-", *args], script)


def awake(action, replace=False):
    active = applescript('tell application "Amphetamine" to return session is active') == "true"
    if action == "status":
        remaining = applescript('tell application "Amphetamine" to return session time remaining') if active else "0"
        return {"active": active, "remaining": remaining}
    if action == "end":
        applescript('tell application "Amphetamine" to end session')
        return {"message": "End requested. Amphetamine triggers may start another session."}
    minutes = int(action)
    if minutes not in (30, 60):
        raise ValueError("Choose 30 or 60 minutes")
    if active and not replace:
        raise ValueError("An Amphetamine session is active. Choose Replace explicitly to start a new one.")
    applescript('tell application "Amphetamine" to start new session with options '
                '{duration:' + str(minutes) + ', interval:minutes, displaySleepAllowed:true}')
    return {"message": "Awake for %s minutes; display may sleep." % minutes}


def project_list():
    directory = Path(settings()["projects_dir"]).expanduser()
    paths = [root()] + (sorted(p for p in directory.iterdir() if p.is_dir() and not p.name.startswith(".")) if directory.exists() else [])
    return [{"name": p.name, "path": str(p)} for p in dict.fromkeys(paths)]


def project_action(action, path):
    project = Path(path).expanduser().resolve()
    if not project.is_dir():
        raise ValueError("Project directory does not exist")
    if action == "code":
        run(["/usr/bin/open", "-a", "Visual Studio Code", project])
    elif action in ("terminal", "work"):
        command = ""
        if action == "work":
            command = "/bin/zsh -ic " + shlex.quote("work " + shlex.quote(str(project)))
        # Arguments are passed as data; the fixed AppleScript never interpolates project names.
        applescript('''on run argv
tell application "Ghostty"
set cfg to new surface configuration
set initial working directory of cfg to item 1 of argv
if item 2 of argv is not "" then set command of cfg to item 2 of argv
new window with configuration cfg
activate
end tell
end run''', str(project), command)
    elif action == "github":
        remote = run(["git", "-C", project, "remote", "get-url", "origin"])
        if remote.startswith("git@github.com:"):
            url = "https://github.com/" + remote.split(":", 1)[1]
        elif remote.startswith("https://github.com/") or remote.startswith("ssh://git@github.com/"):
            url = "https://github.com/" + urllib.parse.urlparse(remote).path.lstrip("/")
        else:
            raise ValueError("Origin is not a recognized GitHub URL")
        if url.endswith(".git"):
            url = url[:-4]
        run(["/usr/bin/open", "-a", "Helium", url])
    else:
        raise ValueError("Unknown project action")
    return {"message": "Opened " + project.name}


def cap(action, payload):
    if not Path(CAP).is_file():
        raise ValueError("Cap is not installed")
    if action == "targets":
        kind = payload.get("kind", "screens")
        if kind not in ("screens", "windows", "mics"):
            raise ValueError("Unknown target type")
        return run([CAP, "targets", kind, "--json"])
    if action == "status":
        return run([CAP, "record", "status", "--json"])
    if action == "forget":
        active = json.loads(run([CAP, "record", "status", "--json"]))
        if active != []:
            raise ValueError("Cap reports active recordings. Stop the intended recording before clearing stale tracking.")
        tracking = STATE / "recording.json"
        if tracking.exists():
            tracking.unlink()
        return "Cleared stale Raycast recording metadata. No recording or media was deleted."
    recording_dir = HOME / "Movies/Cap"
    if action == "folder":
        recording_dir.mkdir(parents=True, exist_ok=True)
        run(["/usr/bin/open", recording_dir])
        return "Opened recordings folder"
    if action == "start":
        kind, target = payload.get("kind"), str(payload.get("target", "")).strip()
        if kind not in ("screen", "window") or not target:
            raise ValueError("Select screen/window and enter its ID from List Targets")
        STATE.mkdir(parents=True, exist_ok=True, mode=0o700)
        tracking = STATE / "recording.json"
        if tracking.exists():
            raise ValueError("A Raycast recording is already tracked. Check status and stop it first.")
        recording_dir.mkdir(parents=True, exist_ok=True)
        path = recording_dir / (datetime.now().strftime("%Y-%m-%d_%H-%M-%S_") + uuid.uuid4().hex[:6] + ".cap")
        argv = [CAP, "record", "start", "--" + kind, target, "--mode", "studio", "--detach", "--json", "--path", path]
        if payload.get("mic"):
            argv += ["--mic", payload["mic"]]
        if payload.get("systemAudio"):
            argv += ["--system-audio"]
        output = run(argv, timeout=60)
        events = []
        for line in output.splitlines():
            try:
                events.append(json.loads(line))
            except ValueError:
                continue
        recording_id = None
        for event in events:
            if isinstance(event, dict):
                recording_id = event.get("recordingId") or event.get("recording_id") or event.get("id") or recording_id
        # A detached CLI recording without an ID cannot safely be stopped by an unrelated process.
        tracking.write_text(json.dumps({"id": recording_id, "path": str(path), "start_output": output}, indent=2))
        tracking.chmod(0o600)
        return output
    if action == "stop":
        tracking = STATE / "recording.json"
        if not tracking.exists():
            raise ValueError("No recording started by these commands is tracked")
        data = json.loads(tracking.read_text())
        if not data.get("id"):
            raise ValueError("Cap did not return a recognized recording ID. Stop in Cap; inspect the local tracking file.")
        output = run([CAP, "record", "stop", "--id", str(data["id"]), "--json"], timeout=90)
        tracking.unlink()
        return output
    if action == "export":
        path = Path(payload.get("path", "")).expanduser().resolve()
        if not path.is_dir() or path.suffix != ".cap":
            raise ValueError("Select an existing .cap project directory")
        destination = path.with_suffix(".mp4")
        if destination.exists():
            raise ValueError("MP4 already exists; rename it before exporting")
        return run([CAP, "export", path, "--format", "mp4", "--output", destination, "--json"], timeout=600)
    raise ValueError("Unknown Cap action")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["network", "public-ip", "ports", "quality", "transform", "projects", "project", "awake", "cap", "dotfiles", "finder-paths", "diff", "system"])
    parser.add_argument("action", nargs="?", default="")
    parser.add_argument("--copy", action="store_true", help="Copy result to clipboard explicitly")
    parser.add_argument("--plain", action="store_true", help="Print a text result for shell integration")
    parser.add_argument("--replace", action="store_true", help="Replace an existing Amphetamine session")
    args = parser.parse_args()
    payload = json.loads(sys.stdin.read() or "{}") if not sys.stdin.isatty() and args.command in ("transform", "project", "cap", "diff") else {}
    if args.command == "system":
        if args.action == "display-sleep":
            run(["/usr/bin/pmset", "displaysleepnow"])
        elif args.action == "lock":
            applescript('tell application "System Events" to keystroke "q" using {control down, command down}')
        elif args.action == "dark-mode":
            applescript('tell application "System Events" to tell appearance preferences to set dark mode to not dark mode')
        elif args.action == "trash":
            run(["/usr/bin/open", str(HOME / ".Trash")])
        else:
            raise ValueError("Unknown system action")
        data = "Done"
    elif args.command == "network":
        data = network()
        if args.action:
            data = data[args.action]
            if args.action == "ipv4" and data == "Unavailable":
                raise ValueError("No IPv4 address on the active interface")
    elif args.command == "public-ip":
        data = run(["/usr/bin/curl", "--fail", "--silent", "--show-error", "--max-time", "10", "https://api.ipify.org"])
        ipaddress.ip_address(data)
    elif args.command == "ports":
        data = run(["/usr/sbin/lsof", "-nP", "-iTCP", "-sTCP:LISTEN"], check=False) or "No visible listening TCP ports"
    elif args.command == "quality":
        data = run(["/usr/bin/networkQuality"], timeout=180)
    elif args.command == "transform":
        data = transform(args.action, payload.get("text", ""))
    elif args.command == "projects":
        data = project_list()
    elif args.command == "project":
        data = project_action(args.action, payload["path"])
    elif args.command == "awake":
        data = awake(args.action or "status", args.replace)
    elif args.command == "cap":
        data = cap(args.action, payload)
    elif args.command == "finder-paths":
        data = applescript('''tell application "Finder"
set paths to {}
repeat with f in selection
set end of paths to POSIX path of (f as alias)
end repeat
set AppleScript's text item delimiters to linefeed
return paths as text
end tell''')
        if not data:
            raise ValueError("Select one or more files in Finder first")
    elif args.command == "diff":
        STATE.mkdir(parents=True, exist_ok=True, mode=0o700)
        # Fixed files are overwritten only on explicit Diff; never tracked by Git.
        paths = [STATE / "diff-left.txt", STATE / "diff-right.txt"]
        for path, value in zip(paths, [payload.get("left", ""), payload.get("right", "")]):
            path.write_text(value); path.chmod(0o600)
        run(["code", "--diff", *paths])
        data = "Opened local comparison. Files remain outside Git until the next comparison or manual removal."
    elif args.command == "dotfiles":
        if args.action == "missing":
            result = subprocess.run(["brew", "bundle", "check", "--file=" + str(root() / "Brewfile"), "--verbose"], capture_output=True, text=True)
            data = (result.stdout + result.stderr).strip()
            if result.returncode not in (0, 1):
                raise ValueError(data)
        elif args.action in ("doctor", "status", "diff"):
            command = [root() / "doctor"] if args.action == "doctor" else [root() / "setup", args.action]
            result = subprocess.run(command, cwd=root(), capture_output=True, text=True, timeout=180)
            data = {"exit_code": result.returncode, "output": result.stdout + result.stderr}
        else:
            raise ValueError("Choose doctor, status, diff or missing")
    else:
        raise ValueError("Unknown command")
    if args.copy:
        value = data if isinstance(data, str) else json.dumps(data, indent=2)
        run(["/usr/bin/pbcopy"], value)
    if args.plain:
        if isinstance(data, str):
            print(data)
        elif isinstance(data, dict) and "output" in data:
            print(data["output"])
        else:
            print(json.dumps(data, indent=2))
        if isinstance(data, dict) and "exit_code" in data:
            sys.exit(data["exit_code"])
    else:
        print(json.dumps({"ok": True, "data": data}, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as error:
        print(json.dumps({"ok": False, "error": str(error)}, ensure_ascii=False))
        sys.exit(1)
