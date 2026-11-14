#!/usr/bin/env python3
"""Apply declared macOS preferences; preview unless --write is given."""
import datetime
import json
from pathlib import Path
import shlex
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def load(name):
    return json.loads((ROOT / name).read_text())

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



if __name__ == "__main__":
    if any(arg not in ["--write"] for arg in sys.argv[1:]):
        sys.exit("Usage: macos-defaults.py [--write]")
    macos("--write" in sys.argv[1:])
