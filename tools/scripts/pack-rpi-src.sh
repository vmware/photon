#!/bin/bash

BRANCH=rpi-5.9.y
BASE=v5.9-rc5
V=5.9.0

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
git clone -b "$BASE" --depth=1 https://github.com/torvalds/linux .
git remote add rpi https://github.com/raspberrypi/linux.git
git fetch rpi "$BRANCH"
git checkout FETCH_HEAD

ARGS=( git log --format=format:"%at" "$BASE.." )
echo "Timestamping (${ARGS[@]}) ..."
DATE_TS="$( "${ARGS[@]}" | sort -n | tail -n 1)"
DATE="$(TZ= date +%Y.%m.%d -d "@$DATE_TS")"
echo "Version is $V.$DATE"

ARGS=( git archive --format=tar --prefix=rpi-linux-$V.$DATE/ HEAD )
echo "packaging (${ARGS[@]}) ..."
"${ARGS[@]}" >&3
