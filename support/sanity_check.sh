#!/bin/bash

# Sanify check for all json files.
echo "Sanity check for all json files..."
for i in `find . -name "*.json" -type f -not -path "*stage*"`; do echo $i; json_pp -t null < $i || break -1 ; done

echo "Checking all python code is compilable..."
for i in `find . -name "*.py" -type f -not -path "*stage*"`; do echo $i; python -m py_compile $i || break -1 ; done
