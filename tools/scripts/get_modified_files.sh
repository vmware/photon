#!/bin/bash

# get @~ file list if there are no files in git diff or HEAD is ahead
if [ -z "$(git diff --name-only HEAD --)" ]; then
  git diff --name-only @~
elif [ -n "$(git status 2>&1 | grep -iw 'ahead of')" ]; then
  ahead_by="$(git status | sed -n -e 's/^.*ahead.* by //p' |  cut -d' ' -f1)"
  git diff --name-only @~${ahead_by} @
else
  git diff --name-only
fi
