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
    forbidden = re.compile(r"(^|/)(id_(rsa|ed25519|ecdsa|dsa)(\.pub)?|auth\.json|credentials\.json|\.env)$|\.(sqlite|db)$|(^|/)\.zsh_(history|sessions)(/|$)|(^|/)\.zcompdump[^/]*$")
    key_marker = re.compile(r"-----BEGIN (?:OPENSSH |RSA |EC |DSA |ENCRYPTED )?PRIVATE KEY-----")
    files = [(p, e) for p, e in state.items() if e["type"] == "file"]
    report(not any(forbidden.search(p) or key_marker.search(e.get("contents", "")) for p, e in files), "managed targets exclude keys, auth files, and databases")
    # Validate rendered helpers too, including files built from templates.
    shell_files = [(p, e) for p, e in files if Path(p).name in (".zprofile", ".zshrc") or p.endswith(".zsh")]
    syntax = [subprocess.run(["/bin/zsh", "-n"], input=e.get("contents", ""),
                             capture_output=True, text=True) for _, e in shell_files]
    report(all(result.returncode == 0 for result in syntax), "shell configuration syntax valid")
    for result in syntax:
        if result.returncode:
            print(result.stderr.strip())
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
    store_apps = re.findall(r'^mas "([^"]+)",\s*id:\s*(\d+)', (ROOT / "Brewfile").read_text(), re.M)
    if store_apps:
        report(bool(shutil.which("mas")), "Mac App Store CLI available")
        if shutil.which("mas"):
            store = run(["mas", "list"])
            installed_ids = set(re.findall(r"^\s*(\d+)\s", store.stdout, re.M))
            missing = [name for name, app_id in store_apps if app_id not in installed_ids]
            report(store.returncode == 0 and not missing,
                   "Brewfile App Store apps installed" + (": " + ", ".join(missing) if missing else ""))
            if store.returncode:
                print(store.stderr.strip())
    if (ROOT / "configs/dot_config/mise/config.toml").exists():
        report(bool(shutil.which("mise")), "mise available")
        if shutil.which("mise"):
            installed = run(["mise", "--cd", str(Path.home()), "ls", "--current", "--json"])
            try:
                tools = json.loads(installed.stdout)
                missing = [name for name, versions in tools.items()
                           if any(not entry.get("installed") for entry in versions)]
                report(installed.returncode == 0 and bool(tools) and not missing,
                       "mise default tools installed" + (": " + ", ".join(missing) if missing else ""))
            except (ValueError, TypeError):
                report(False, "mise default tools can be inspected")
            # A login shell has shims without loading interactive prompt plugins.
            login = run(["/bin/zsh", "-lc", "mise doctor"])
            report(login.returncode == 0, "mise runtime access in login/agent shells")
            if login.returncode:
                print(login.stdout.strip())
                print(login.stderr.strip())
    manifest = ROOT / "configs/dot_config/vscode/extensions.txt"
    if manifest.exists():
        report(bool(shutil.which("code")), "VS Code CLI available")
        if shutil.which("code"):
            installed = run(["code", "--list-extensions"])
            present = {line.strip().lower() for line in installed.stdout.splitlines()}
            wanted = {line.strip().split("@", 1)[0].lower() for line in manifest.read_text().splitlines()
                      if line.strip() and not line.lstrip().startswith("#")}
            missing = sorted(wanted - present)
            report(installed.returncode == 0 and not missing,
                   "VS Code extensions installed" + (": " + ", ".join(missing) if missing else ""))
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
