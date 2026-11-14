#!/bin/sh
# @raycast.schemaVersion 1
# @raycast.title Copy Public IP
# @raycast.mode silent
# @raycast.packageName Mac Setup
# @raycast.description Request your public IP from api.ipify.org and copy it.
# @raycast.icon 🌐
exec /usr/bin/python3 "$HOME/.config/raycast/mac-tools.py" public-ip --copy
