source ${PHOTON_UPGRADE_UTILS_DIR}/constants.sh

function echo() {
  builtin echo -e "$(date '+%FT%T%z') $*"
}

function echoerr() {
  echo "$*" 1>&2
}

# To be called on irrecoverable error. It provides a user with actionable items
# to help debugging
function abort() {
  local rc=$1
  shift

  echoerr "$*\nOriginal list of RPMs and RPM DB are stored in $TMP_BACKUP_LOC,"\
          " please provide contents of that folder along with system journal "\
          " logs for analysis; these logs can be captured using command-\n"\
          "# /usr/bin/journalctl -xa > $TMP_BACKUP_LOC/journal.log\n" \
          "Cannot continue. Aborting."
  exit $rc
}

# discover any regular file in /etc/systemd/system/multi-user.target.wants,
# whcih is meant for enabled services. If found, terminate the upgrade process
function find_wrongly_enabled_services() {
  local f
  local p=/etc/systemd/system/multi-user.target.wants
  local wes=''  # holds space separated Wrongly Enabled Services list

  pushd $p
  for f in *; do
    if [ ! -L $f ]; then
      wes="${wes}${p}/${f} "
    fi
  done
  popd
  if [ -n "$wes" ]; then
    echoerr "Incorrect service configuratiion of following regular file(s) was found - " \
        "'$wes'.\nThese files must be removed for the upgrade to continue.\n" \
        "Those files may be removed and corresponding 'systemctl enable' command " \
        "may be, subsequently, used for enabling those systemd units."
    exit $ERETRY_EINVAL
  fi
}

# displays the space separated list of systemd managed services which have
# provided state
# e.g. get_services_by_state(enabled) - will return space separated list of
# enabled services
function get_services_by_state() {
  local state=$1

  ${SYSTEMCTL} list-unit-files \
    --state=$state --no-legend --plain --no-pager | \
    awk '{print $1}'
  return $?
}

function rebuilddb() {
  local rc=0

  echo "Rebuilding RPMDB."
  ${RPM} --rebuilddb
  rc=$?
  if [ $rc -ne 0 ]; then
    abort $rc "Failed rebuilding installed package database."
  fi
  echo "successfully rebuilt RPMDB."
}

# Finds packages which are installed from the provided package names in args
function find_installed_packages() {
  $RPM -q --queryformat="%{NAME}\n" $* | $GREP -v 'is not installed'
}
