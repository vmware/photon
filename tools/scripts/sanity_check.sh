#!/bin/bash

NCPUS=$(nproc)
SCRIPTS_DIR="$(dirname ${0})"

echo "Sanity check for all json files ..."
find . ! \( -path './stage' -prune \)  -name '*\.json' -type f | \
  xargs -r -P${NCPUS} -n32 python3 ${SCRIPTS_DIR}/validate_json.py

echo "Checking all python code is compilable ..."
find . ! \( -path './stage' -prune \)  -name '*\.py' -type f | \
  xargs -r -P${NCPUS} -n32 python3 -m py_compile

# delete all __pycache__ dirs created after running py_compile
find . ! \( -path './stage' -prune \) -type d -name "__pycache__" | xargs rm -rf
