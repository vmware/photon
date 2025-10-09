#!/bin/bash
# Shell execution template for spec2git prep section execution
# This script handles state restoration between command blocks
set -e

STATE_FILE="__STATE_FILE_PLACEHOLDER__"

# Set RPM environment variables that rpmspec injects
__RPM_ENV_VARS_PLACEHOLDER__

# Restore state from previous execution if state file exists
if [ -f "$STATE_FILE" ]; then
  # Restore directory stack
  # dirs -p outputs: top of stack first, bottom last
  # We need to: cd to bottom, then pushd each directory from bottom-1 to top
  in_dirstack=0
  declare -a dirstack_dirs
  while IFS= read -r line; do
    if [[ "$line" == '# DIRSTACK_START' ]]; then
      in_dirstack=1
    elif [[ "$line" == '# DIRSTACK_END' ]]; then
      break
    elif [[ $in_dirstack -eq 1 ]]; then
      dirstack_dirs+=("$line")
    fi
  done < "$STATE_FILE"

  # If we have a directory stack, restore it
  if [ ${#dirstack_dirs[@]} -gt 0 ]; then
    # cd to the bottom of the stack (last entry)
    bottom_idx=$((${#dirstack_dirs[@]}-1))
    # Use eval to expand tilde in path
    eval cd "${dirstack_dirs[$bottom_idx]}"
    # Now pushd each directory from bottom-1 down to 0 (which becomes top)
    for ((i=$bottom_idx-1; i>=0; i--)); do
      eval pushd "${dirstack_dirs[i]}" > /dev/null
    done
  else
    # No directory stack, just restore the cd command
    saved_dir=$(grep '^cd ' "$STATE_FILE" | head -1)
    if [ -n "$saved_dir" ]; then
      eval "$saved_dir"
    fi
  fi

  # Now source only the export statements for environment variables
  eval "$(grep '^export ' "$STATE_FILE" || true)"
  eval "$(grep '^declare -x ' "$STATE_FILE" || true)"
fi

# User commands will be inserted here
__COMMANDS_PLACEHOLDER__

# Save state if state file is configured
if [ -n "$STATE_FILE" ]; then
  # Export all variables, current directory, and directory stack
  export -p > "$STATE_FILE"
  echo "cd \"$(pwd)\"" >> "$STATE_FILE"
  # Save directory stack - use a delimiter that won't appear in paths
  echo "# DIRSTACK_START" >> "$STATE_FILE"
  dirs -p >> "$STATE_FILE"
  echo "# DIRSTACK_END" >> "$STATE_FILE"
fi

