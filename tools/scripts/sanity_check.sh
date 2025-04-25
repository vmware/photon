#!/bin/bash

if [ $# -ne 1 ]; then
  echo "ERROR: Usage: $0 <scan-dir>" >&2
  exit 1
fi

SCAN_DIR="${1}"

[ ! -d "${SCAN_DIR}" ] && exit 1
cd ${SCAN_DIR}

NCPUS=$(nproc)
SCRIPTS_DIR="$(dirname ${0})"

echo "Sanity check for all json files in dir '${SCAN_DIR}' ..."
find . ! \( -path './stage' -prune \) -name '*\.json' -type f | \
  xargs -r -P${NCPUS} -n32 python3 ${SCRIPTS_DIR}/validate_json.py

echo "Checking all python code is compilable in dir '${SCAN_DIR}' ..."
find . ! \( -path './stage' -prune \) -name '*\.py' -type f | \
  xargs -r -P${NCPUS} -n32 python3 -m py_compile

# delete all __pycache__ dirs created after running py_compile
find . ! \( -path './stage' -prune \) -type d -name "__pycache__" | xargs rm -rf
