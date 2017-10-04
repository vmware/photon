#!/bin/bash

if [[ $# != 2 ]]; then
  echo "${0} <local_repo> <tag>"
  exit 1
fi

set -xe

LOCAL_REPO="$1"
TAG="$2"

PKGNAME="$(basename "$LOCAL_REPO")"

TMP="$(mktemp -d "/tmp/git-repo-XXXX")"
trap "{ rm -rf "$TMP"; }" EXIT 

pushd "$TMP"
#fetch with the tag/commit only
git init --template=/dev/null
git remote add origin "${LOCAL_REPO}"
git fetch origin "$TAG" --depth=1
git checkout FETCH_HEAD
git gc --aggressive --prune=now
git remote remove origin
COMMIT="$(git rev-parse --short HEAD)"
du -xhd1
popd

tar -czf "$PKGNAME-$COMMIT.tar.gz" -C "$TMP" .
