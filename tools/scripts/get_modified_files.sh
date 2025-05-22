#!/bin/bash

repoDir="$1"
if [ ! -d "${repoDir}" ]; then
  echo "ERROR: Repo directory '${repoDir}' does not exist ..." >&2
  exit 1
fi

# get @~ file list if there are no files in git diff or HEAD is ahead
if [ -z "$(git -C ${repoDir} diff --name-only HEAD --)" ]; then
  files=($(git -C ${repoDir} diff --name-only @~))
elif [ -n "$(git -C ${repoDir} status 2>&1 | grep -iw 'ahead of')" ]; then
  ahead_by="$(git -C ${repoDir} status | sed -n -e 's/^.*ahead.* by //p' |  cut -d' ' -f1)"
  files=($(git -C ${repoDir} diff --name-only @~${ahead_by} @))
else
  files=($(git -C ${repoDir} diff --name-only))
fi

# prepend path
prefix="$(realpath ${repoDir})"

printf "%s\n" "${files[@]}" | sed "s|^|$prefix/|"
