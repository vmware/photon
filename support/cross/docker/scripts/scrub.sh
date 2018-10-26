#!/bin/bash

PROJECT_ROOT=$(pwd)

cd $PROJECT_ROOT/support/cross/docker && \
    make scrub
