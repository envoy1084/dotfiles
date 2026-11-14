#!/usr/bin/env python3
"""Build/install the local extension or inspect Raycast's portable setup."""
import argparse
import ast
import json
import os
import queue
import signal
import threading
import time
from pathlib import Path
import subprocess
import sys

CONFIG = Path.home() / ".config/raycast"


def check():
    errors = []
    for name in ["settings.json", "extensions.json", "quicklinks.json", "snippets.json", "mac-setup/package.json"]:
        try:
            json.loads((CONFIG / name).read_text())
        except (OSError, ValueError) as error:
            errors.append(str(error))
    try:
        ast.parse((CONFIG / "mac-tools.py").read_text())
    except (OSError, SyntaxError) as error:
        errors.append(str(error))
    installed = set()
    for path in (CONFIG / "extensions").glob("*/package.json"):
        try:
            installed.add(json.loads(path.read_text())["name"])
        except (OSError, ValueError, KeyError):
            continue
    wanted = {item["slug"] for item in json.loads((CONFIG / "extensions.json").read_text())} | {"mac-setup"}
    missing = sorted(wanted - installed)
    print(("FIX  " if errors else "OK   ") + "Raycast portable files" + (": " + "; ".join(errors) if errors else ""))
    print(("INFO " if missing else "OK   ") + "Raycast extensions" + (" awaiting supported installation: " + ", ".join(missing) if missing else " installed"))
    print("INFO Verify Raycast permissions, native settings and sign-ins in-app; see docs/raycast.md.")
    return bool(errors)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        return check()
    if not args.write:
        print("Preview: install locked dependencies; typecheck; import using ray develop; stop the build watcher.")
        print("Native imports: ~/.config/raycast/{quicklinks,snippets}.json. App settings/Store extensions: docs/raycast.md.")
        return 0
    extension = CONFIG / "mac-setup"
    for command in [["mise", "exec", "--", "pnpm", "install", "--frozen-lockfile"],
                    ["mise", "exec", "--", "pnpm", "run", "typecheck"]]:
        subprocess.run(command, cwd=extension, check=True)
    process = subprocess.Popen(["mise", "exec", "--", "pnpm", "exec", "ray", "develop"], cwd=extension,
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, start_new_session=True)
    try:
        lines = queue.Queue()
        def read_output():
            for line in process.stdout:
                lines.put(line)
        reader = threading.Thread(target=read_output, daemon=True)
        reader.start()
        deadline = time.monotonic() + 45
        built = False
        while time.monotonic() < deadline:
            try:
                line = lines.get(timeout=1)
            except queue.Empty:
                if process.poll() is not None:
                    break
                continue
            print(line, end="", flush=True)
            if "built extension successfully" in line:
                built = True
                time.sleep(2)
                break
        if not built:
            raise ValueError("Development import did not finish; run pnpm dev from the local extension directory to inspect it.")
    finally:
        pid_file = CONFIG / "extensions/mac-setup/cli.pid"
        owned_pid = None
        try:
            value = pid_file.read_text().strip()
            if os.getpgid(int(value)) == process.pid:
                owned_pid = value
        except (OSError, ValueError):
            pass
        if process.poll() is None:
            os.killpg(process.pid, signal.SIGTERM)
            process.wait(timeout=10)
        if owned_pid and pid_file.exists() and pid_file.read_text().strip() == owned_pid:
            pid_file.unlink()
    print("Local extension built/imported; watcher stopped. Native settings/imports and authorizations are separate steps.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print("FIX  " + str(error), file=sys.stderr)
        sys.exit(1)
