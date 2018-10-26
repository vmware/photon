#!/bin/bash

PROJECT_ROOT=$(pwd)

case "$1" in
    i686)
        cd $PROJECT_ROOT/support/cross/docker && make package-i686
        ;;
    aarch64)
        cd $PROJECT_ROOT/support/cross/docker && make package-aarch64
        ;;
    arm)
        cd $PROJECT_ROOT/support/cross/docker && make package-arm
        ;;
    *)
        echo "Error: Unsupported architecture - $1"
        exit 1
        ;;
esac
