#!/bin/bash

#
# Main
#

PROJECT_ROOT=$(pwd)

DOCKER_ROOT=$PROJECT_ROOT/BUILD/docker
DOCKER_SRC_ROOT=$PROJECT_ROOT/support/cross/docker/toolchain/photon-xc-$1

mkdir -p $DOCKER_ROOT

rm -rf $DOCKER_ROOT/*

case $1 in
    i686)
        cp -r $PROJECT_ROOT/RPMS/x86_64/cross-i686-tools-*.rpm $DOCKER_ROOT/
        cp $DOCKER_SRC_ROOT/texinfo-6.5-2.ph3.x86_64.rpm $DOCKER_ROOT/
        ;;
    arm)
        cp -r $PROJECT_ROOT/RPMS/x86_64/cross-arm-tools-*.rpm $DOCKER_ROOT/
        ;;
    aarch64)
        cp -r $PROJECT_ROOT/RPMS/x86_64/cross-aarch64-tools-*.rpm $DOCKER_ROOT/
        ;;
    *)
        echo "Error: Unsupported architecture - $1"
        exit 1
        ;;
esac

cp -r $DOCKER_SRC_ROOT/Dockerfile $DOCKER_ROOT/
cp -r $DOCKER_SRC_ROOT/run-photon-xc.sh $DOCKER_ROOT/
