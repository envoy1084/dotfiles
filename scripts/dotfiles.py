#!/usr/bin/env python3
"""Manage an explicit list of desktop dotfiles, with previews and backups."""
import argparse
import datetime
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SECRET = re.compile(r"-----BEGIN (?:OPENSSH |RSA |EC |DSA |ENCRYPTED )?PRIVATE KEY-----|(?im:^\s*(?:export\s+)?[\w.-]*(?:token|secret|password|api[_-]?key)[\w.-]*\s*[:=]\s*\S+)")


def load(name):
    return json.loads((ROOT / name).read_text())


def under(root, relative):
    path = Path(relative)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError("Manifest paths must be relative and cannot contain '..'")
    return root / path


def safe_content(path):
    content = path.read_bytes()
    if SECRET.search(content.decode("utf-8")):
        raise ValueError("Possible secret in {}: keep it in a local untracked file".format(path))
    return content


def atomic_write(path, content, mode):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".dotfiles-", dir=str(path.parent))
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(content)
        os.chmod(temporary, mode)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def entries(home):
    for entry in load("manifest.json")["files"]:
        yield entry, under(ROOT, entry["source"]), under(home, entry["target"])


def check(home):
    items = list(entries(home))
    if len({e[0]["target"] for e in items}) != len(items):
        raise ValueError("Duplicate target paths in manifest")
    for entry, source, target in items:
        if source.is_symlink():
            raise ValueError("Managed sources must be regular files: {}".format(source))
        safe_content(source)
        int(entry["mode"], 8)
    for filename in ["macos-defaults.json", "state/observed.json"]:
        load(filename)
    subprocess.run(["/bin/zsh", "-n", str(ROOT / "configs/zsh/zprofile")], check=True)
    print("Checked {} managed files, manifests, and shell syntax.".format(len(items)))


def status(home):
    for entry, source, target in entries(home):
        state = "missing"
        if target.is_file():
            state = "same" if source.read_bytes() == target.read_bytes() else "different"
        elif target.exists() or target.is_symlink():
            state = "not a regular file"
        print("{:18} ~/{}".format(state, entry["target"]))


def sync(home, capture, write):
    check(home)
    stamp = datetime.datetime.now().astimezone().strftime("%Y-%m-%d_%H-%M-%S-%f")
    backup_root = home / "Library/Application Support/dotfiles/backups" / stamp
    changes = []
    # Validate every source first, so a rejected file does not leave a half-run.
    for entry, repository_file, live_file in entries(home):
        source, target = (live_file, repository_file) if capture else (repository_file, live_file)
        if not source.is_file():
            raise ValueError("Missing source: {}".format(source))
        if target.is_dir():
            raise ValueError("Target is a directory: {}".format(target))
        content = safe_content(source)
        if capture and entry["source"] == "configs/zsh/zprofile":
            content = content.replace(str(home).encode(), b"$HOME")
        same = target.is_file() and target.read_bytes() == content
        mode = 0o644 if capture else int(entry["mode"], 8)
        mode_differs = target.is_file() and (target.stat().st_mode & 0o777) != mode
        if same and (capture or not mode_differs):
            continue
        changes.append((entry, source, target, content, mode))
    for entry, source, target, content, mode in changes:
        print("{} {} -> {}".format("COPY" if write else "WOULD COPY", source, target))
        if not write:
            continue
        if target.is_file():
            backup = backup_root / ("repository" if capture else "home") / (entry["source"] if capture else entry["target"])
            backup.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
            shutil.copy2(target, backup)
            os.chmod(backup, 0o600)
        if not capture and entry["target"].startswith(".ssh/"):
            (home / ".ssh").mkdir(mode=0o700, exist_ok=True)
            os.chmod(home / ".ssh", 0o700)
        atomic_write(target, content, mode)
    print("{} change(s). {}".format(len(changes), "Applied." if write else "Preview only; add --write to apply."))
    if write and backup_root.exists():
        print("Previous files: {}".format(backup_root))


def packages(write):
    brew = shutil.which("brew")
    if not brew:
        raise ValueError("Install Homebrew first using https://brew.sh, then run this command again.")
    argv = [brew, "bundle", "install", "--no-upgrade", "--file=" + str(ROOT / "Brewfile")]
    print(("RUN " if write else "WOULD RUN ") + shlex.join(argv), flush=True)
    if write:
        subprocess.run(argv, check=True)
    else:
        print("Preview only; add --write to install. Nothing will be uninstalled.")


def macos(write):
    commands = []
    for setting in load("macos-defaults.json")["settings"]:
        kind = setting["type"]
        value = setting["value"]
        if kind not in ["bool", "int", "float", "string"]:
            raise ValueError("Unsupported defaults type: " + kind)
        encoded = str(value).lower() if kind == "bool" else str(value)
        commands.append(["/usr/bin/defaults", "write", setting["domain"], setting["key"], "-" + kind, encoded])
    if write:
        backup = Path.home() / "Library/Application Support/dotfiles/backups" / datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f") / "macos"
        backup.mkdir(parents=True, mode=0o700)
        previous = []
        for setting in load("macos-defaults.json")["settings"]:
            read = subprocess.run(["/usr/bin/defaults", "read", setting["domain"], setting["key"]], capture_output=True, text=True)
            previous.append({"domain": setting["domain"], "key": setting["key"], "was_set": read.returncode == 0, "previous_value": read.stdout.strip() if read.returncode == 0 else None})
        (backup / "previous-values.json").write_text(json.dumps(previous, indent=2) + "\n")
        print("Previous preference values: {}".format(backup))
    for argv in commands:
        print(("RUN " if write else "WOULD RUN ") + shlex.join(argv), flush=True)
        if write:
            subprocess.run(argv, check=True)
    print("Changes may require restarting Dock or logging in again." if write else "Preview only; add --write to apply these preferences.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", nargs="?", default="status", choices=["status", "check", "apply", "capture", "packages", "macos"])
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true", help="Apply changes; default is a preview")
    mode.add_argument("--dry-run", action="store_true", help="Explicitly request the default preview")
    parser.add_argument("--home", type=Path, default=Path.home(), help="Alternate home directory for file previews/restores")
    args = parser.parse_args()
    home = args.home.expanduser().absolute()
    if args.command in ["packages", "macos"] and home != Path.home():
        raise ValueError("--home is only supported for file commands")
    if args.command == "check":
        check(home)
    elif args.command == "status":
        status(home)
    elif args.command in ["apply", "capture"]:
        sync(home, args.command == "capture", args.write)
    elif args.command == "packages":
        packages(args.write)
    elif args.command == "macos":
        macos(args.write)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print("Error: {}".format(error), file=sys.stderr)
        sys.exit(1)
