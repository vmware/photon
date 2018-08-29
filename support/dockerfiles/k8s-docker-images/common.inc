
setup_repo()
{
    mkdir -p tmp
    ln -fs ${STAGE_DIR}/RPMS tmp/RPMS
    ETH0_IP=`ip -4 addr show eth0 scope global | grep 'inet ' | awk '{print $2}' | cut -f1  -d'/'`
    cat stage-rpms.repo | sed 's/ETH0_IP/'"${ETH0_IP}"'/g' > tmp/stage-rpms.repo
    if ! iptables -C INPUT -p tcp --dport 62965 -j ACCEPT &> /dev/null; then
        iptables -A INPUT -p tcp --dport 62965 -j ACCEPT
    fi
    python3 -m http.server --bind ${ETH0_IP} 62965 &
    PY_WS_PID=$!
    if [ -z "${PY_WS_PID}" ]; then
        echo "Failed to start repo server"
        exit 1
    fi
    echo "tdnf repo server started with pid: " ${PY_WS_PID}
    CTR=30
    while true
    do
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
            echo "Failed to start tdnf repo server. Stopping PID: " ${PY_WS_PID}
            kill ${PY_WS_PID}
            exit 1
        fi
    done
}

function cleanup_repo {
  echo "Terminating tdnf repo server with pid: " ${PY_WS_PID}
  kill ${PY_WS_PID}
}
trap cleanup_repo EXIT
