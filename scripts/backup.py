#!/usr/bin/env python3
"""Back up changed managed files outside Git before chezmoi applies them."""
import datetime
import json
import os
from pathlib import Path
import shutil
import subprocess

root = Path(__file__).resolve().parents[1]
home = Path.home()
result = subprocess.run(["chezmoi", "--source", str(root), "dump", "--format=json"], capture_output=True, text=True, check=True)
state = json.loads(result.stdout)
backup = home / "Library/Application Support/dotfiles/backups" / datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
count = 0
for relative, entry in state.items():
    if entry["type"] != "file":
        continue
    path = home / relative
    if not path.is_file():
        continue
    if path.read_bytes() == entry["contents"].encode() and path.stat().st_mode & 0o777 == entry["perm"]:
        continue
    destination = backup / relative
    destination.parent.mkdir(parents=True, mode=0o700, exist_ok=True)
    shutil.copy2(path, destination)
    os.chmod(destination, 0o600)
    count += 1
if count:
    print("Backed up {} managed file(s) to {}".format(count, backup))
else:
    print("No existing managed files need a backup.")
