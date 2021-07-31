#!/usr/bin/env bash

if [ -z "$(git diff-index --name-only $1 HEAD --)" ]; then
  SPECS=($(git diff --name-only $1 @~ | grep -e "SPECS/.*.spec$"))
else
  SPECS=($(git diff --name-only $1 | grep -e "SPECS/.*.spec$"))
fi

if [ ${#SPECS[@]} -eq 0 ]; then
  echo "No spec files to check at the moment"
  exit 0
fi

python3 support/check_spec.py ${SPECS[@]}
