#!/bin/bash
SCRIPTS_DIR="$(dirname ${0})"

# Sanify check for all json files.
echo "Sanity check for all json files..."
while read f; do
	if ! json_pp -t null < "${f}" >& /dev/null; then
		echo "Please check:${f} for syntax errors"
		exit 1
	fi
done < <(find "${SCRIPTS_DIR}/../" \( -name '*stage*' \) -prune -o -name "*.json" -type f | grep -v "/stage")

echo "Checking all python code is compilable..."
while read f; do
	if ! python3 -m py_compile "${f}"; then
		echo "Please check:${f} for complitation errors"
		exit 1
	fi
done < <(find "${SCRIPTS_DIR}/../" \( -name '*stage*' \) -prune -o -name "*.py" -type f | grep -v "/stage")
