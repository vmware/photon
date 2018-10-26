#!/bin/bash

PROJECT_ROOT=$(pwd)

cd $PROJECT_ROOT && \
    make clean
rm -rf $PROJECT_ROOT/staging
