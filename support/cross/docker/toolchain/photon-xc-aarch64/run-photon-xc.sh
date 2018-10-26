#!/bin/bash

function clean_up {

    # Perform program exit housekeeping
    echo "shutdown signal handled"

    exit $1
}

while :
do
    sleep 5 &
    wait
done
