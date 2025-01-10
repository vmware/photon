#!/bin/bash

# This is the main script which invokes template creation scripts
# for now, there is only one script but this can grow.
# this is invoked by build.py

script_dir="$(dirname ${BASH_SOURCE[0]})"

cd $script_dir

echo "Generate generic kernel dep specs ..."
if ! python3 ./create-kernel-deps-specs-from-template.py "$@"; then
  echo "ERROR: failed to generate kernel dep specs ..." 1>&2
  exit 1
fi
