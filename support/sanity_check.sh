#!/bin/bash

# Sanify check for all json files.
echo "Sanity check for all json files..."
while IFS= read -r f; do
	if ! json_pp -t null < "${f}" >& /dev/null; then
		echo "Please check:${f} for syntax errors"
		exit 1
	fi
done < <(find . ! \( -path './stage' -prune \)  -name '*\.json' -type f)

echo "Checking all python code is compilable..."
while IFS= read -r f; do
	if ! python3 -m py_compile "${f}"; then
		echo "Please check:${f} for compilation errors"
		exit 1
	fi
done < <(find . ! \( -path './stage' -prune \)  -name '*\.py' -type f)
