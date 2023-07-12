#!/bin/bash

# Helper script to move rpm db from /var/lib/rpm to /usr/lib/sysimage/rpm
# This script comes to picture when host's rpm has sqlite backend db but
# /var/lib/rpm as dbpath.
# If db path is /usr/lib/sysimage/rpm, nothing will be done

old_rpmdb_path="/var/lib/rpm"
actual_rpmdb_path="$(rpm -E %_dbpath)"

abort()
{
  echo -e "$*" 1>&2
  exit 1
}

# check for old_rpmdb_path directorie's existence before running rpm query
# rpm --quiet -q rpm --dbpath <dir> will create <dir> if it doesn't exist
if ls -ld "${old_rpmdb_path}" &> /dev/null && \
    rpm --quiet -q rpm --dbpath "${old_rpmdb_path}"; then
  if [ "${old_rpmdb_path}" != "${actual_rpmdb_path}" ]; then
    echo "INFO: RpmDB is at ${old_rpmdb_path} and needs to be migrated"
    if ! mkdir -p "${actual_rpmdb_path}"; then
      abort "ERROR: failed to create ${actual_rpmdb_path} dir"
    fi

    if ! mv "${old_rpmdb_path}"/* "${actual_rpmdb_path}"; then
      abort "ERROR: failed to move files from ${old_rpmdb_path} to ${actual_rpmdb_path}"
    fi

    if ! rpmdb --rebuilddb; then
      abort "ERROR: failed to rebuild db"
    fi
  fi
elif rpm --quiet -q rpm --dbpath "${actual_rpmdb_path}"; then
  echo "INFO: RpmDB is at ${actual_rpmdb_path} and healthy"
else
  abort "ERROR: RpmDB is either corrupt or does not exist"
fi

exit 0
