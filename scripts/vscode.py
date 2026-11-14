#!/usr/bin/env python3
"""Preview/restore missing VS Code extensions, or capture current preferences."""
import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
HOME = Path.home()
MANIFEST = HOME / ".config/vscode/extensions.txt"
SOURCE_MANIFEST = ROOT / "configs/dot_config/vscode/extensions.txt"
USER = HOME / "Library/Application Support/Code/User"


def extensions(versions=False):
    args = ["code", "--list-extensions"]
    if versions:
        args.append("--show-versions")
    result = subprocess.run(args, capture_output=True, text=True, check=True)
    return sorted(line.strip() for line in result.stdout.splitlines() if line.strip())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--capture", action="store_true")
    args = parser.parse_args()
    if not shutil.which("code"):
        raise RuntimeError("VS Code CLI is unavailable; restore the visual-studio-code cask first.")

    if args.capture:
        selected = extensions(versions=True)
        targets = [USER / name for name in ("settings.json", "keybindings.json", "tasks.json")]
        targets = [p for p in targets if p.is_file()]
        if (USER / "snippets").is_dir():
            targets.append(USER / "snippets")
        state = json.loads(subprocess.check_output(
            ["chezmoi", "--source", str(ROOT), "dump", "--format=json"], text=True))
        prefix = "Library/Application Support/Code/User/"
        removed = []
        for relative, entry in state.items():
            if entry["type"] != "file" or not relative.startswith(prefix):
                continue
            name = relative[len(prefix):]
            if name not in ("settings.json", "keybindings.json", "tasks.json") and not name.startswith("snippets/"):
                continue
            if not (HOME / relative).exists():
                removed.append(HOME / relative)
        for target in targets:
            print("Capture " + str(target))
        for target in removed:
            print("Stop managing removed preference " + str(target))
        print("Capture {} extension versions".format(len(selected)))
        if args.write:
            MANIFEST.parent.mkdir(parents=True, exist_ok=True)
            MANIFEST.write_text("\n".join(selected) + "\n")
            subprocess.run(["chezmoi", "--source", str(ROOT), "add", "--secrets=error",
                            *map(str, targets), str(MANIFEST)], check=True)
            if removed:
                subprocess.run(["chezmoi", "--source", str(ROOT), "forget", "--force", *map(str, removed)], check=True)
        return 0

    manifest = MANIFEST if MANIFEST.exists() else SOURCE_MANIFEST
    desired = [line.strip() for line in manifest.read_text().splitlines()
               if line.strip() and not line.lstrip().startswith("#")]
    if not all(re.fullmatch(r"[\w-]+\.[\w-]+@[^\s]+", item) for item in desired):
        raise RuntimeError("Invalid extension manifest; expected publisher.name@version.")
    installed = {item.lower() for item in extensions()}
    missing = [item for item in desired if item.split("@", 1)[0].lower() not in installed]
    for item in missing:
        print(("Installing " if args.write else "Would install ") + item, flush=True)
        if args.write:
            subprocess.run(["code", "--install-extension", item], check=True)
    print("{} recorded extensions; {} missing{}".format(
        len(desired), len(missing), " before restore" if args.write else ""))
    # Existing versions and unlisted extensions are preserved; capture records updates.
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, RuntimeError, subprocess.CalledProcessError) as error:
        print("FIX  " + str(error), file=sys.stderr)
        sys.exit(1)
