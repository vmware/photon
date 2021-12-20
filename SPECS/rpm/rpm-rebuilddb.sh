#!/bin/bash

# Script to rebuild rpm backend db

#set -x

# log file name
log_fn="/var/log/rpm-rebuilddb.log"

# redirect stderr & stdout to log file
exec > "${log_fn}" 2>&1

# this serves as a key for systemd service
if [ -x /usr/bin/systemctl ]; then
  touch /var/lib/rpm/.rebuilddb
fi

rpm_lock_fn="/var/lib/rpm/.rpm.lock"
lock_bin="/usr/lib/rpm/lock"
lock_flag="/var/run/.lkflg"

# Check if db operation is in progress
# Timesout after 900 seconds
check_if_db_operation_in_progress()
{
  local retry=900

  while [ "${retry}" -gt 0 ]; do
    if pgrep -x "tdnf|rpm|rpmdb" &> /dev/null; then
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
sanity_check()
{
  if command -v rpm &> /dev/null; then
    if rpm -q rpm &> /dev/null; then
      return 0
    fi
  fi

  if command -v tdnf &> /dev/null; then
    if tdnf list installed tdnf --disablerepo=* &> /dev/null; then
      return 0
    fi
  fi

  # should not reach here
  return 1
}

lpid=""

unlock()
{
  rm -f "${lock_flag}"
  kill -9 "${lpid}"
}

get_lock()
{
  local retry=100

  # remove "$lock_flag" file to ensure that there is no leftover
  rm -f "${lock_flag}"

  "${lock_bin}" "${rpm_lock_fn}" &
  lpid="$!"

  # 20 second max delay
  while [ "${retry}" -gt 0 ]; do
    if [ -f "${lock_flag}" ]; then
      return 0
    fi
    sleep 0.2
    retry=$((retry-1))
  done

  echo -e "\nERROR: failed to get lock ..."
  exit 1
}

# Rebuild rpm db --> This should finish quick
# Steps:
# 1. Take backup of existing db
# 2. Try rebuilding db
# 3. If ok, do a sanity check and remove backup
#    Else - remove the newly created /var/lib/rpmrebuilddb.* and retry
#
# If sanity check fails, revert backup data
# Stops after 10 attempts
try_rpm_rebuilddb()
{
  local retry=10
  local backup_dir=""
  local rpmdb_dir="/var/lib/rpm"

  # need 6 Xs, toybox mktemp doesn't work with 4 Xs
  backup_dir="$(mktemp -d -p /var/lib .rpmdbXXXXXX)"
  if [ "$?" -ne 0 ]; then
    echo -e "\nERROR: failed to create backup directory ..."
    return 1
  fi

  # During taking backup & restoring backup operations
  # we need a lock, otherwise this might create contention.
  #
  # During this copy & restore operation, rpm transaction might run parallely
  # and we might end up in an unlikely situation
  if get_lock; then
    # remove temporary lock files
    rm -f "${rpmdb_dir}"/__db*

    if ! cp -ar "${rpmdb_dir}"/* "${backup_dir}"; then
      unlock
      rm -rf "${backup_dir}"
      echo -e "\nERROR: failed to copy contents to backup directory ..."
      return 1
    fi
    unlock
  fi

  echo -e "\nINFO: took backup of rpmdb at ${backup_dir} ..."

  while [ "${retry}" -gt 0 ]; do
    while true; do
      if ! pgrep -x "tdnf|rpm|rpmdb" &> /dev/null; then
        break
      fi
      sleep 0.1
    done

    if rpmdb --rebuilddb; then
      if get_lock; then
        if sanity_check; then
          unlock

          rm -rf "${backup_dir}" "${rpmdb_dir}"/.rebuilddb
          echo -e "\nINFO: rpmdb --rebuild success ..."
          return 0
        fi

        local err=0
        echo -e "\n--- ERROR: SOMETHING WENT TOTALLY WRONG --"
        echo "Trying to restore RPMDB from backup directory ..."

        rm -rf "${rpmdb_dir}"/*

        if ! cp -ar "${backup_dir}"/* "${rpmdb_dir}"; then
          err=1
          echo -e "\nERROR: failed copy contents from ${backup_dir} to ${rpmdb_dir} ..."
        else
          rm -rf "${backup_dir}"
        fi

        if [ "${err}" -eq 0 ]; then
          echo -e "\nINFO: Revert from backup directory success ..."
        fi

        unlock
        return 1
      fi
    fi

    rm -rf /var/lib/rpmrebuilddb.*

    echo -e "\nERROR: failed to rebuild rpmdb, retrying ..."
    retry=$((retry-1))

  done

  return 1
}

check_if_db_operation_in_progress && try_rpm_rebuilddb
