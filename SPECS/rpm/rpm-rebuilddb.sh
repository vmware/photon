#!/bin/bash

# Script to rebuild rpm backend db

# this serves as a key for systemd service
if [ -x /usr/bin/systemctl ]; then
  touch /var/lib/rpm/.rebuilddb
fi

# log file name
log_fn="/var/log/rpm-rebuilddb.log"

# redirect stderr & stdout to log file
exec > "${log_fn}" 2>&1

# Check if db operation is in progress
# Timesout after 900 seconds
check_if_db_operation_in_progress()
{
  local retry=900

  while [ "${retry}" -gt 0 ]; do
    if [ "$(pgrep "tdnf")" ] || [ "$(pgrep "rpm")" ]; then
      echo -e "\nWARNING: tdnf/rpm is still running ..."
      retry=$((retry-1))
      sleep 1
    else
      echo -e "\nINFO: tdnf/rpm are not running, proceed to next step ..."
      return 0
    fi
  done

  echo -e "\nERROR: tdnf/rpm is running from 15 minutes, retries exceeded ..."
  return 1
}

# Sometimes rebuilddb succeeds but rpm options won't work
# this is a simple sanity check
check_for_sanity()
{
  if command -v rpm &> /dev/null; then
    [ "$(rpm -q rpm)" ] && return 0 || return 1
  elif command -v tdnf &> /dev/null; then
    [ "$(tdnf list installed tdnf)" ] && return 0 || return 1
  fi

  return 0
}

# Rebuild rpm db --> This should finish quick
# Steps:
# 1. Take backup of existing db
# 2. Try rebuilding db
# 3. If ok, do a sanity check and remove backup
#    Else - remove the newly created /var/lib/rpmrebuilddb.* and retry
#
# If sanity check fails, revert backup data
# Stops after 10 attempts(~2 seconds)
try_rpm_rebuilddb()
{
  local retry=10
  local backup_dir=""
  local rpmdb_dir="/var/lib/rpm"

  # need 6 Xs, toybox mktemp doesn't work with 4 Xs
  backup_dir="$(mktemp -d -p /var/lib/ .rpmdbXXXXXX)"
  if [ "$?" -ne 0 ]; then
    echo -e "\nERROR: failed to create backup directory ..."
    return 1
  fi

  # remove temporary lock files
  rm -f "${rpmdb_dir}"/__db*

  if ! cp -arv "${rpmdb_dir}"/* "${backup_dir}"; then
    rm -rf "${backup_dir}"
    echo -e "\nERROR: failed to copy contents to backup directory ..."
    return 1
  fi

  echo -e "\nINFO: took backup of rpmdb at ${backup_dir} ..."

  while [ "${retry}" -gt 0 ]; do

    while [ "$(pgrep "tdnf")" ] || [ "$(pgrep "rpm")" ]; do
      sleep 0.1
      continue
    done

    if rpmdb --rebuilddb; then
      if check_for_sanity; then
        rm -rfv "${backup_dir}" "${rpmdb_dir}"/.rebuilddb
        echo -e "\nINFO: rpmdb --rebuild success ..."
        return 0
      fi

      local err=0
      echo -e "\n--- ERROR: SOMETHING WENT TOTALLY WRONG --"
      echo "Trying to restore RPMDB from backup directory ..."

      if ! rm -fv "${rpmdb_dir}"/*; then
        err=1
        echo -e "\nERROR: failed to empty ${rpmdb_dir} ..."
      fi

      if ! cp -arv "${backup_dir}"/* "${rpmdb_dir}"; then
        err=1
        echo -e "\nERROR: failed copy contents from ${backup_dir} to ${rpmdb_dir} ..."
      else
        rm -rfv "${backup_dir}"
      fi

      if [ "${err}" -eq 0 ]; then
        echo -e "\nINFO: Revert from backup directory success ..."
      fi
      return 1
    fi

    rm -rfv /var/lib/rpmrebuilddb.*

    echo -e "\nERROR: failed to rebuild rpmdb, retrying ..."
    retry=$((retry-1))

  done

  return 1
}

check_if_db_operation_in_progress && try_rpm_rebuilddb
