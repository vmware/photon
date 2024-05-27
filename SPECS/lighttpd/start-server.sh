#!/bin/bash

# Lighttpd custom startup script,
CUSTOM_STARTUP_SCRIPT="/usr/libexec/lighttpd/custom/start.sh"

start_server() {

  if [ -s $CUSTOM_STARTUP_SCRIPT ]; then
    # Start lighttpd server with custom configuration
    /bin/bash $CUSTOM_STARTUP_SCRIPT
    exit $?
  fi

  # Start lighttpd with default configuration
  /usr/sbin/lighttpd -f /etc/lighttpd/lighttpd.conf
  exit $?

}

start_server
