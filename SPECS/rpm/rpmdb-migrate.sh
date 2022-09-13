#!/bin/bash

# Script to migrate rpmdb from /var/lib/rpm to new rpmdb path at /usr
#set -x

# log file name
log_fn="/var/log/rpmdb-migrate.log"

# redirect stderr & stdout to log file
exec > "${log_fn}" 2>&1

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

main()
{
  local dbpath_old="/var/lib/rpm"

  if [ ! -f "${dbpath_old}/.migratedb" ]; then
    echo "${dbpath_old}/.migratedb not preset, exit"
    exit 0
  fi

  local dbpath_new="$(rpmdb -E '%_dbpath' 2>/dev/null)"

  if [ "${dbpath_new}" = "${dbpath_old}" ]; then
    echo "RpmDB path is still at ${dbpath_new}, exit"
    exit 0
  fi

  if [ -L "${dbpath_old}" ]; then
    echo "RpmDB has been migrated, exit"
    rm -f "${dbpath_old}/.migratedb"
    exit 0
  fi

  if ! rpmdb --rebuilddb; then
    echo "ERROR: Failed to rebuild RpmDB" 1>&2
    exit 1
  fi

  if ! sanity_check; then
    echo "ERROR: sanity check failed" 1>&2
    exit 1
  fi

  rm -rfv "${dbpath_old}"
  ln -sfr "${dbpath_new}" "${dbpath_old}"
}

main
