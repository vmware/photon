#!/bin/bash

SRC_ROOT="$1"

if [ ! -d "${SRC_ROOT}" ]; then
  echo "ERROR: ${SRC_ROOT} doesn't exist ..." 1>&2
  exit 1
fi

if [ ! -d "${SRC_ROOT}/.git" ]; then
  echo "${SRC_ROOT}/.git doesn't exist, not a git repo" 1>&2
  exit 0
fi

git_hooks_path="${SRC_ROOT}/.git/hooks"
hook_scripts_path="${SRC_ROOT}/tools/scripts"

for fn in "commit-msg" "pre-push"; do
  if [ ! -f "${git_hooks_path}/${fn}" ]; then
    echo "${git_hooks_path}/${fn} doesn't exist, creating now ..."
    if ! ln -srv "${hook_scripts_path}/${fn}" "${git_hooks_path}/${fn}"; then
      echo "ERROR: failed to create git hook with ${hook_scripts_path}/${fn}"
      exit 1
    fi
  fi
done

exit 0
