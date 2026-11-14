#!/bin/sh
# @raycast.schemaVersion 1
# @raycast.title Setup Doctor
# @raycast.mode fullOutput
# @raycast.packageName Mac Setup
# @raycast.description Read-only dotfiles health and configuration drift checks.
# @raycast.icon 🩺
exec /usr/bin/python3 "$HOME/.config/raycast/mac-tools.py" dotfiles doctor --plain
