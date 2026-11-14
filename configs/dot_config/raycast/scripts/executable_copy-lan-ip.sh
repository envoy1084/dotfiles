#!/bin/sh
# @raycast.schemaVersion 1
# @raycast.title Copy LAN IP
# @raycast.mode silent
# @raycast.packageName Mac Setup
# @raycast.description Copy IPv4 from the active default-route interface.
# @raycast.icon 🌐
exec /usr/bin/python3 "$HOME/.config/raycast/mac-tools.py" network ipv4 --copy
