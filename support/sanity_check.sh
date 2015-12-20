#!/bin/bash

SCRIPTS_DIR="$(dirname ${0})"

# Sanify check for all json files.
echo "Sanity check for all json files..."
while read f; do
	echo "Checking:${f}"
	if ! json_pp -t null < "${f}" >& /dev/null; then
		echo "Please check:${f} for syntax errors"
		exit 1
	fi
done < <(find "${SCRIPTS_DIR}/../" -name "*.json" -type f -not -path "*stage*")

echo "Checking all python code is compilable..."
while read f; do
	echo "Checking:${f}"
	if ! python -m py_compile "${f}"; then
		echo "Please check:${f} for complitation errors"
		exit 1
	fi
done < <(find "${SCRIPTS_DIR}/../" -name "*.py" -type f -not -path "*stage*")
