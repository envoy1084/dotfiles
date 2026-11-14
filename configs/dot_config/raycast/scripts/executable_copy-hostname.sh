#!/bin/sh
# @raycast.schemaVersion 1
# @raycast.title Copy Hostname
# @raycast.mode silent
# @raycast.packageName Mac Setup
# @raycast.description Copy this Mac's hostname.
# @raycast.icon 💻
exec /usr/bin/python3 "$HOME/.config/raycast/mac-tools.py" network hostname --copy
