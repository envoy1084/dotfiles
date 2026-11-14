#!/bin/sh
# @raycast.schemaVersion 1
# @raycast.title Show Listening Ports
# @raycast.mode fullOutput
# @raycast.packageName Mac Setup
# @raycast.description Show listening TCP ports; never stops processes.
# @raycast.icon 🔌
exec /usr/sbin/lsof -nP -iTCP -sTCP:LISTEN
