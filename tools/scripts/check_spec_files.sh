#!/bin/bash

# get @~ file list if there are no files in git diff or HEAD is ahead
if [ -z "$(git diff --name-only HEAD --)" ]; then
  SPECS=($(git diff --name-only @~ | grep -e "SPECS/.*.spec$"))
elif [ -n "$(git status 2>&1 | grep -iw 'ahead of')" ]; then
  ahead_by="$(git status | sed -n -e 's/^.*ahead.* by //p' |  cut -d' ' -f1)"
  SPECS=($(git diff --name-only @~${ahead_by} @ | grep -e "SPECS/.*.spec$"))
else
  SPECS=($(git diff --name-only | grep -e "SPECS/.*.spec$"))
fi

if [ ${#SPECS[@]} -eq 0 ]; then
  echo "No spec files to check at the moment"
  exit 0
fi

python3 support/spec-checker/check_spec.py ${SPECS[@]}
exit $?
