#!/bin/bash

PROJECT_ROOT=$(pwd)

cd $PROJECT_ROOT/support/cross/docker && \
    make clean
rm -rf $PROJECT_ROOT/stage/cross
