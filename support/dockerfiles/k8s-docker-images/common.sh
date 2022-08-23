#!/bin/bash

COMM_DBG=0

cleanup_repo()
{
  echo "Terminating tdnf repo server with pid: " ${PY_WS_PID}
  kill ${PY_WS_PID}
}

start_repo_server()
{
  if [ ! -d "${STAGE_DIR}" ]; then
    echo "ERROR: STAGE_DIR is invalid" 1>&2
    exit 1
  fi

  mkdir -p tmp
  ln -sfv ${STAGE_DIR}/RPMS tmp/RPMS

  local PORT=62965

  local IFACE_NAME=
  IFACE_NAME="$(ip route list | awk '/^default/ {print $5}')"

  local IFACE_IP=
  IFACE_IP=$(ip -4 addr show "${IFACE_NAME}" scope global | grep 'inet ' | awk '{print $2}' | cut -f1 -d'/')

  cat stage-rpms.repo | sed 's/IFACE_IP:PORT/'"${IFACE_IP}:${PORT}"'/g' > tmp/stage-rpms.repo
  if ! iptables -C INPUT -p tcp --dport ${PORT} -j ACCEPT &> /dev/null; then
    iptables -A INPUT -p tcp --dport ${PORT} -j ACCEPT
  fi

  if [ $COMM_DBG -eq 0 ]; then
    python3 -m http.server --bind ${IFACE_IP} ${PORT} 1>/dev/null &
  else
    python3 -m http.server --bind ${IFACE_IP} ${PORT} &
  fi

  PY_WS_PID=$!
  if [ -z "${PY_WS_PID}" ]; then
    echo "Failed to start repo server" 1>&2
    exit 1
  fi

  trap cleanup_repo EXIT

  echo "tdnf repo server started with pid: " ${PY_WS_PID}
  local CTR=30
  while true; do
    set +e
    netstat -an | grep tcp | grep 62965 | grep LISTEN
    if [ $? -eq 0 ]; then
      set -e
      echo "tdnf repo server running with pid: " ${PY_WS_PID}
      break
    fi
    set -e
    echo "Waiting for $CTR seconds for tdnf repo server to start..."
    sleep 1
    let CTR=$CTR-1
    if [ $CTR -eq 0 ]; then
      echo "Failed to start tdnf repo server. Stopping PID: " ${PY_WS_PID} 1>&2
      kill ${PY_WS_PID}
      exit 1
    fi
  done
}

get_spec_ver()
{
  local spec_fn="$1"
  rpmspec -q --qf "%{version}\n" "${spec_fn}" | head -n1
}

get_spec_rel()
{
  local spec_fn="$1"
  rpmspec -q --qf "%{release}\n" "${spec_fn}" | head -n1
}
