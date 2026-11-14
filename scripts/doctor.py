#!/usr/bin/env python3
"""Read-only configuration and foundation checks; never installs or applies."""
import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def run(argv):
    return subprocess.run(argv, cwd=str(ROOT), capture_output=True, text=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config-only", action="store_true")
    args = parser.parse_args()
    failures = []

    def report(ok, message):
        print(("OK   " if ok else "FIX  ") + message)
        if not ok:
            failures.append(message)

    report(bool(shutil.which("chezmoi")), "chezmoi available")
    if failures:
        return 1
    dump = run(["chezmoi", "--source", str(ROOT), "dump", "--format=json"])
    report(dump.returncode == 0, "configuration renders")
    if dump.returncode:
        print(dump.stderr.strip())
        return 1
    state = json.loads(dump.stdout)
    forbidden = re.compile(r"(^|/)(id_(rsa|ed25519|ecdsa|dsa)(\.pub)?|auth\.json|credentials\.json|\.env)$|\.(sqlite|db)$")
    key_marker = re.compile(r"-----BEGIN (?:OPENSSH |RSA |EC |DSA |ENCRYPTED )?PRIVATE KEY-----")
    files = [(p, e) for p, e in state.items() if e["type"] == "file"]
    report(not any(forbidden.search(p) or key_marker.search(e.get("contents", "")) for p, e in files), "managed targets exclude keys, auth files, and databases")
    syntax = run(["/bin/zsh", "-n", str(ROOT / "configs/dot_zprofile")])
    report(syntax.returncode == 0, "shell profile syntax valid")
    print("INFO {} managed config files".format(len(files)))
    if args.config_only:
        return bool(failures)

    for command in ["brew", "gh", "git"]:
        report(bool(shutil.which(command)), command + " available")
    if shutil.which("brew"):
        formulae = set(run(["brew", "list", "--formula"]).stdout.splitlines())
        casks = set(run(["brew", "list", "--cask"]).stdout.splitlines())
        wanted = re.findall(r'^(brew|cask) "([^"]+)"', (ROOT / "Brewfile").read_text(), re.M)
        missing = [name for kind, name in wanted if name not in (formulae if kind == "brew" else casks)]
        report(not missing, "Brewfile packages installed" + (": " + ", ".join(missing) if missing else ""))
    status = run(["chezmoi", "--source", str(ROOT), "status"])
    report(status.returncode == 0 and not status.stdout.strip(), "live configuration matches source")
    if status.stdout.strip():
        print(status.stdout.strip())
    config = run(["chezmoi", "dump-config", "--format=json"])
    try:
        configured_source = json.loads(config.stdout)["sourceDir"]
        report(Path(configured_source).resolve() in [ROOT.resolve(), (ROOT / "configs").resolve()], "plain chezmoi commands use this repo")
    except (ValueError, KeyError):
        report(False, "initialize chezmoi with ./setup init --write")
    if shutil.which("gh"):
        if run(["gh", "auth", "status"]).returncode == 0:
            print("OK   GitHub CLI authenticated")
        else:
            print("INFO GitHub CLI sign-in deferred; run gh auth login when setting up the remote.")
    for field in ["user.name", "user.email"]:
        report(bool(run(["git", "config", "--get", field]).stdout.strip()), "Git " + field + " configured")
    if run(["git", "remote", "get-url", "origin"]).stdout.strip():
        print("OK   origin remote configured")
    else:
        print("INFO Remote repository deferred by the user; local Git history is available.")
    report(run(["git", "rev-parse", "--verify", "HEAD"]).returncode == 0, "Git history exists")
    if run(["git", "status", "--porcelain"]).stdout.strip():
        print("INFO Uncommitted dotfiles changes; review and commit when ready.")
    print("INFO App exports, permissions, and sign-ins: README.md (Manual restore notes)")
    return bool(failures)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print("FIX  " + str(error), file=sys.stderr)
        sys.exit(1)
