#!/bin/sh
# @raycast.schemaVersion 1
# @raycast.title Copy Selected Finder Paths
# @raycast.mode silent
# @raycast.packageName Mac Setup
# @raycast.description Copy absolute paths of the current Finder selection.
# @raycast.icon 📁
exec /usr/bin/python3 "$HOME/.config/raycast/mac-tools.py" finder-paths --copy
