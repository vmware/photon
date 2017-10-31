#!/bin/sh 
## EMQ docker image start script

## Shell setting
if [[ ! -z "$DEBUG" ]]; then
    set -ex
fi

## Local IP address setting

LOCAL_IP=$(hostname -i |grep -E -oh '((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])'|head -n 1)

## EMQ Base settings and plugins setting
# Base settings in /opt/emqttd/etc/emq.conf
# Plugin settings in /opt/emqttd/etc/plugins

_EMQ_HOME="/opt/emqtt"

if [[ -z "$PLATFORM_ETC_DIR" ]]; then
    export PLATFORM_ETC_DIR="$_EMQ_HOME/etc"
fi

if [[ -z "$PLATFORM_LOG_DIR" ]]; then
    export PLATFORM_LOG_DIR="$_EMQ_HOME/log"
fi

if [[ -z "$EMQ_NAME" ]]; then
    export EMQ_NAME="$(hostname)"
fi

if [[ -z "$EMQ_HOST" ]]; then
    export EMQ_HOST="$LOCAL_IP"
fi

if [[ -z "$EMQ_WAIT_TIME" ]]; then
    export EMQ_WAIT_TIME=5
fi

if [[ -z "$EMQ_NODE__NAME" ]]; then
    export EMQ_NODE__NAME="$EMQ_NAME@$EMQ_HOST"
fi

# Set hosts to prevent cluster mode failed

if [[ ! -z "$LOCAL_IP" && ! -z "$EMQ_HOST" ]]; then
    echo "$LOCAL_IP        $EMQ_HOST" >> /etc/hosts
fi

# unset EMQ_NAME
# unset EMQ_HOST

if [[ -z "$EMQ_NODE__PROCESS_LIMIT" ]]; then
    export EMQ_NODE__PROCESS_LIMIT=2097152
fi

if [[ -z "$EMQ_NODE__MAX_PORTS" ]]; then
    export EMQ_NODE__MAX_PORTS=1048576
fi

if [[ -z "$EMQ_NODE__MAX_ETS_TABLES" ]]; then
    export EMQ_NODE__MAX_ETS_TABLES=2097152
fi

if [[ -z "$EMQ_LOG__CONSOLE" ]]; then
    export EMQ_LOG__CONSOLE="console"
fi

if [[ -z "$EMQ_LISTENER__TCP__EXTERNAL__ACCEPTORS" ]]; then
    export EMQ_LISTENER__TCP__EXTERNAL__ACCEPTORS=64
fi

if [[ -z "$EMQ_LISTENER__TCP__EXTERNAL__MAX_CLIENTS" ]]; then
    export EMQ_LISTENER__TCP__EXTERNAL__MAX_CLIENTS=1000000
fi

if [[ -z "$EMQ_LISTENER__SSL__EXTERNAL__ACCEPTORS" ]]; then
    export EMQ_LISTENER__SSL__EXTERNAL__ACCEPTORS=32
fi

if [[ -z "$EMQ_LISTENER__SSL__EXTERNAL__MAX_CLIENTS" ]]; then
    export EMQ_LISTENER__SSL__EXTERNAL__MAX_CLIENTS=500000
fi

if [[ -z "$EMQ_LISTENER__WS__EXTERNAL__ACCEPTORS" ]]; then
    export EMQ_LISTENER__WS__EXTERNAL__ACCEPTORS=16
fi

if [[ -z "$EMQ_LISTENER__WS__EXTERNAL__MAX_CLIENTS" ]]; then
    export EMQ_LISTENER__WS__EXTERNAL__MAX_CLIENTS=250000
fi

# Catch all EMQ_ prefix environment variable and match it in configure file
CONFIG=/opt/emqttd/etc/emq.conf
CONFIG_PLUGINS=/opt/emqttd/etc/plugins
for VAR in $(env)
do
    # Config normal keys such like node.name = emqttd@127.0.0.1
    if [[ ! -z "$(echo $VAR | grep -E '^EMQ_')" ]]; then
        VAR_NAME=$(echo "$VAR" | sed -r "s/EMQ_(.*)=.*/\1/g" | tr '[:upper:]' '[:lower:]' | sed -r "s/__/\./g")
        VAR_FULL_NAME=$(echo "$VAR" | sed -r "s/(.*)=.*/\1/g")
        # Config in emq.conf
        if [[ ! -z "$(cat $CONFIG |grep -E "^(^|^#*|^#*\s*)$VAR_NAME")" ]]; then
            echo "$VAR_NAME=$(eval echo \$$VAR_FULL_NAME)"
            sed -r -i "s/(^#*\s*)($VAR_NAME)\s*=\s*(.*)/\2 = $(eval echo \$$VAR_FULL_NAME)/g" $CONFIG
        fi
        # Config in plugins/*
        if [[ ! -z "$(cat $CONFIG_PLUGINS/* |grep -E "^(^|^#*|^#*\s*)$VAR_NAME")" ]]; then
            echo "$VAR_NAME=$(eval echo \$$VAR_FULL_NAME)"
            sed -r -i "s/(^#*\s*)($VAR_NAME)\s*=\s*(.*)/\2 = $(eval echo \$$VAR_FULL_NAME)/g" $(ls $CONFIG_PLUGINS/*)
        fi        
    fi
    # Config template such like {{ platform_etc_dir }}
    if [[ ! -z "$(echo $VAR | grep -E '^PLATFORM_')" ]]; then
        VAR_NAME=$(echo "$VAR" | sed -r "s/(.*)=.*/\1/g"| tr '[:upper:]' '[:lower:]')
        VAR_FULL_NAME=$(echo "$VAR" | sed -r "s/(.*)=.*/\1/g")
        sed -r -i "s@\{\{\s*$VAR_NAME\s*\}\}@$(eval echo \$$VAR_FULL_NAME)@g" $CONFIG
    fi
done

## EMQ Plugin load settings
# Plugins loaded by default

if [[ ! -z "$EMQ_LOADED_PLUGINS" ]]; then
    echo "EMQ_LOADED_PLUGINS=$EMQ_LOADED_PLUGINS"
    # First, remove special char at header
    # Next, replace special char to ".\n" to fit emq loaded_plugins format
    echo $(echo "$EMQ_LOADED_PLUGINS."|sed -e "s/^[^A-Za-z0-9_]\{1,\}//g"|sed -e "s/[^A-Za-z0-9_]\{1,\}/\. /g")|tr ' ' '\n' > /opt/emqttd/data/loaded_plugins
fi

## EMQ Main script

# Start and run emqttd, and when emqttd crashed, this container will stop

/opt/emqttd/bin/emqttd foreground &

# wait and ensure emqttd status is running
WAIT_TIME=0
while [[ -z "$(/opt/emqttd/bin/emqttd_ctl status |grep 'is running'|awk '{print $1}')" ]]
do
    sleep 1
    echo "['$(date -u +"%Y-%m-%dT%H:%M:%SZ")']:waiting emqttd"
    WAIT_TIME=$((WAIT_TIME+1))
    if [[ $WAIT_TIME -gt $EMQ_WAIT_TIME ]]; then
        echo "['$(date -u +"%Y-%m-%dT%H:%M:%SZ")']:timeout error"
        exit 1
    fi
done

echo "['$(date -u +"%Y-%m-%dT%H:%M:%SZ")']:emqttd start"

# Run cluster script

if [[ -x "./cluster.sh" ]]; then
    ./cluster.sh &
fi

# Join an exist cluster

if [[ ! -z "$EMQ_JOIN_CLUSTER" ]]; then
    echo "['$(date -u +"%Y-%m-%dT%H:%M:%SZ")']:emqttd try join $EMQ_JOIN_CLUSTER"
    /opt/emqttd/bin/emqttd_ctl cluster join $EMQ_JOIN_CLUSTER &
fi

# Change admin password

if [[ ! -z "$EMQ_ADMIN_PASSWORD" ]]; then
    echo "['$(date -u +"%Y-%m-%dT%H:%M:%SZ")']:admin password changed to $EMQ_ADMIN_PASSWORD"
    /opt/emqttd/bin/emqttd_ctl admins passwd admin $EMQ_ADMIN_PASSWORD &
fi

# monitor emqttd is running, or the docker must stop to let docker PaaS know
# warning: never use infinite loops such as `` while true; do sleep 1000; done`` here
#          you must let user know emqtt crashed and stop this container,
#          and docker dispatching system can known and restart this container.
IDLE_TIME=0
while [[ $IDLE_TIME -lt 5 ]]
do  
    IDLE_TIME=$((IDLE_TIME+1))
    if [[ ! -z "$(/opt/emqttd/bin/emqttd_ctl status |grep 'is running'|awk '{print $1}')" ]]; then
        IDLE_TIME=0
    else
        echo "['$(date -u +"%Y-%m-%dT%H:%M:%SZ")']:emqttd not running, waiting for recovery in $((25-IDLE_TIME*5)) seconds"
    fi
    sleep 5
done
# If running to here (the result 5 times not is running, thus in 25s emq is not running), exit docker image
# Then the high level PaaS, e.g. docker swarm mode, will know and alert, rebanlance this service

# tail $(ls /opt/emqttd/log/*)

echo "['$(date -u +"%Y-%m-%dT%H:%M:%SZ")']:emqttd exit abnormally"
exit 1
