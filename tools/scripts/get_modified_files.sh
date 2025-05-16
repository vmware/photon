#!/bin/bash

repoDir="$1"
if [ ! -d "${repoDir}" ]; then
  echo "ERROR: Repo directory '${repoDir}' does not exist ..." >&2
  exit 1
fi

pushd ${repoDir} 1>/dev/null

# We don't expect branch names to be something other than
# standard Photon branches.
branch=$(git branch --show-current)

files=($( {
  git diff --name-only origin/${branch}..HEAD
  git diff --name-only
  git diff --name-only --cached
} | sort -u ))

popd 1>/dev/null

[ ${#files[@]} -eq 0 ] && exit 0

# prepend path
prefix="$(realpath ${repoDir})"

printf "%s\n" "${files[@]}" | sed "s|^|$prefix/|"
