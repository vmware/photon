#!/bin/bash

BRANCH=stable
TAG=1.20200902
VER=1.2020.09.02

set -e

exec 3>&1
exec 1>&2

DIR="$(mktemp -d)"
pushd "$DIR"

atexit() {
  popd
  rm -rf "$DIR"
}

trap -- atexit EXIT

echo "cloning to $DIR ..."
git clone -b "$TAG" --depth=1 https://github.com/raspberrypi/firmware .

ARGS=( git archive --format=tar --prefix=raspberrypi-firmware-$VER/ HEAD boot )
echo "packaging (${ARGS[@]}) ..."
"${ARGS[@]}" >&3
