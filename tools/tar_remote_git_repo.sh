#!/bin/bash

if [[ $# != 2 ]]; then
  echo "${0} <remote-repo> <tag>"
  exit 1
fi

TAR_LOCAL_GIT_REPO="$(dirname "$0")/tar_local_git_repo.sh"

set -xe

REPO="$1"
TAG="$2"

DIR="$(basename "$REPO")"
DIR="${DIR%.*}"
TMP="$(mktemp -d "/tmp/git-repo-XXXX")"
trap "{ rm -rf "$TMP"; }" EXIT 

mkdir -p "$TMP/$DIR"
pushd "$TMP/$DIR"
git clone "$REPO" .
popd

"$TAR_LOCAL_GIT_REPO" "$TMP/$DIR" "$TAG" 
