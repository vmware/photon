#!/bin/bash

if [[ $# != 2 ]]; then
  echo "${0} <repo> <tag>"
  exit 1
fi

set -x
set -e

REPO="$1"
TAG="$2"
DIR="$(basename "$REPO")"
DIR="${DIR%.*}"
TMP="$(mktemp -d "/tmp/git-repo-XXXX")"
trap "{ rm -rf "$TMP"; }" EXIT 

mkdir -p "$TMP/$DIR"
pushd "$TMP"
#phase 1: clone the repo
git clone "$REPO" "${DIR}-orig"
#phase 2: clone again with the tag/commit only
cd "$DIR"
git init --template=/dev/null
git remote add origin "../${DIR}-orig"
git fetch origin "$TAG" --depth=1
git checkout FETCH_HEAD
git gc --aggressive --prune=now
COMMIT="$(git rev-parse --short HEAD)"
cd ..
du -xhd1
popd

tar -czf "$DIR-$COMMIT.tar.gz" -C "$TMP" "$DIR"
