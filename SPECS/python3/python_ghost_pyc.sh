#!/bin/bash

# Script to generate ghost file list for Python byte-compiled files
# This script is called during RPM build to create a list of .pyc files
# and __pycache__ directories to be marked as ghost.
#
# Usage:
#   python_ghost_pyc.sh [output_file] [filter_path]
#
# Arguments:
#   output_file - Where to write the ghost file list (default: ghost_pyc_files.list)
#   filter_path - Optional path to filter (for package-specific lists)
#
# Examples:
#   python_ghost_pyc.sh
#   python_ghost_pyc.sh ghost_foo.list /usr/lib/python*/site-packages/foo
#   python_ghost_pyc.sh ghost_bar.list /usr/lib/python*/site-packages/bar

set -e

if [ -z "$RPM_BUILD_ROOT" ]; then
  echo "ERROR: RPM_BUILD_ROOT not set" >&2
  exit 1
fi

# Output file for ghost entries
GHOST_FILE="${1:-ghost_pyc_files.list}"

# Optional filter path (for package-specific lists)
FILTER_PATH="${2:-}"

# Search path
if [ -n "$FILTER_PATH" ]; then
  # Use filter path - expand wildcards
  SEARCH_PATHS=()
  for pattern in $FILTER_PATH; do
    # If it's a relative path, prefix with RPM_BUILD_ROOT
    if [[ ! $pattern = /* ]]; then
      pattern="$RPM_BUILD_ROOT/$pattern"
    fi
    # Expand the pattern and add matching paths
    for path in $pattern; do
      if [ -e "$path" ]; then
        SEARCH_PATHS+=("$path")
      fi
    done
  done

  if [ ${#SEARCH_PATHS[@]} -eq 0 ]; then
    echo "Warning: No paths found matching filter: $FILTER_PATH"
    touch "$GHOST_FILE"
    exit 0
  fi
else
  # Search entire RPM_BUILD_ROOT
  SEARCH_PATHS=("$RPM_BUILD_ROOT")
fi

# Find all __pycache__ directories and .pyc files
{
  # First, list all __pycache__ directories as %dir
  for search_path in "${SEARCH_PATHS[@]}"; do
    find "$search_path" -type d -name '__pycache__' 2> /dev/null || true
  done | while read -r dir; do
    # Remove RPM_BUILD_ROOT prefix
    rel_path="${dir#$RPM_BUILD_ROOT}"
    echo "%ghost %dir $rel_path"
  done

# Then, list all .pyc and .pyo files as %ghost
for search_path in "${SEARCH_PATHS[@]}"; do
  find "$search_path" -type f \( -name '*.pyc' -o -name '*.pyo' \) 2> /dev/null || true
done | while read -r file; do
    # Remove RPM_BUILD_ROOT prefix
    rel_path="${file#$RPM_BUILD_ROOT}"
    echo "%ghost $rel_path"
    #base="${rel_path%.pyc}"
    #echo "%ghost ${base}.opt-1.pyc"
    #echo "%ghost ${base}.opt-2.pyc"
  done
} > "$GHOST_FILE"

# Sort the file for consistency and remove duplicates
sort -u "$GHOST_FILE" -o "$GHOST_FILE"

echo "Generated ghost file list: $GHOST_FILE"
if [ -n "$FILTER_PATH" ]; then
  echo "Filter path: $FILTER_PATH"
fi

total=$(grep -c '^%ghost ' "$GHOST_FILE" 2>/dev/null || echo 0)
dirs=$(grep -c '^%ghost %dir ' "$GHOST_FILE" 2>/dev/null || echo 0)
files=$((total - dirs))

echo "Found $dirs __pycache__ directories"
echo "Found $files byte-compiled files (.pyc/.pyo)"
