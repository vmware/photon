#!/bin/bash

# Set up log directories
LOG_DIR=/var/log/telegraf
mkdir -p -m 755 $LOG_DIR
chown -R -L telegraf:telegraf $LOG_DIR

STATE_DIR=/var/lib/telegraf
test -d "$STATE_DIR" || {
  mkdir -p "$STATE_DIR"
  chmod 770 "$STATE_DIR"
  chown root:telegraf "$STATE_DIR"
}

STATE_FILE="$STATE_DIR/statefile"
test -f "$STATE_FILE" || {
  touch "$STATE_FILE"
  echo {} > "$STATE_FILE"
  chown root:telegraf "$STATE_FILE"
  chmod 660 "$STATE_FILE"
}

chown -R telegraf:telegraf /etc/telegraf

[[ -d /run/systemd/system ]] && systemctl daemon-reload
