source ${PHOTON_UPGRADE_UTILS_DIR}/constants.sh

function echo() {
  builtin echo -e "$(date '+%FT%T%z') $*"
}

function echoerr() {
  echo "$*" 1>&2
}

function write_to_syslog() {
  $LOGGER -t photon-upgrade -- "$@"
}

# To be called on irrecoverable error. It provides a user with actionable items
# to help debugging. When in the precheck mode, abort() simply returns the
# the provided exit code so that all the prechecks can complete
function abort() {
  local rc=$1
  shift

  if is_precheck_running; then
    echoerr $*
    return $rc
  fi

  echoerr "$*\nOriginal list of RPMs and RPM DB are stored in $TMP_BACKUP_LOC,"\
          " please provide contents of that folder along with system journal "\
          " logs for analysis; these logs can be captured using command-\n"\
          "# /usr/bin/journalctl -xa > $TMP_BACKUP_LOC/journal.log\n" \
          "Cannot continue. Aborting."
  write_to_syslog "photon-upgrade aborted with exit code $rc."
  exit $rc
}

function write_to_syslog() {
  $LOGGER -t photon-upgrade -- "$@"
}

# Usage: find_incorrect_units
# discover any regular systemd unit files in multi-user.target.wants under /etc,
# interfering with enabled services and report the same to the caller.
# restore_units()
# Returns: $ERETRY_EAGAIN when such files are found
function find_incorrect_units() {
  local src=/etc/systemd/system/multi-user.target.wants
  local -a wes_arr=()  # List of unexpected systemd-units in multi-user.target

  # Search in multi-user.target.wants for valid unit file names which happen
  # to be those regular files which interfere in unit enable/disable operations
  wes_arr+=(
    $(
      $FIND $src ! -type l \
        \( \
           -name '*.service' -o -name '*.socket' \
           -o -name '*.device' -o -name '*.mount' -o -name '*.automount' \
           -o -name '*.swap' -o -name '*.target' -o -name '*.path' \
           -o -name '*.timer' -o -name '*.slice' -o -name '*.scope' \
        \)
    )
  )
  [ ${#wes_arr[@]} -eq 0 ] && return 0
  abort $ERETRY_EAGAIN echoerr "Error: Found incorrect filetypes for following systemd unit files"\
       "which need to be reviewed by the administrator as these files may "\
       "interfere in the OS upgrade - ${wes_arr[@]}."
}

# Usage: find_files_for_review
# discover any user created files in multi-user.target.wants under /etc, which
# are not valid systemd unit files
# Returns: $ERETRY_EAGAIN when such files are found
function find_files_for_review() {
  local src=/etc/systemd/system/multi-user.target.wants
  local -a files_arr=()  # List of unexpected pollutant files in multi-user.target

  # Search in multi-user.target.wants for objects which are not systemd units
  files_arr+=(
    $(
      $FIND $src -mindepth 1 ! \
        \( \
           -name '*.service' -o -name '*.socket' \
           -o -name '*.device' -o -name '*.mount' -o -name '*.automount' \
           -o -name '*.swap' -o -name '*.target' -o -name '*.path' \
           -o -name '*.timer' -o -name '*.slice' -o -name '*.scope' \
        \)
    )
  )
  [ ${#files_arr[@]} -eq 0 ] && return 0
  echo "Warning: Found following unexpected user created files in $src." \
       "This location is used by systemd and hence it is best to review these" \
       "and preferably remove them. These files will not interfere in the" \
       "OS upgrade though - ${files_arr[@]}."
  return $ERETRY_EAGAIN
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

# Usage: install_pkgs p1 p2 p3 ...
# installs named packages using tdnf
function install_pkgs() {
  [ $# -eq 0 ] && return 0
  ${TDNF} $REPOS_OPT $ASSUME_YES_OPT install $*
  return $?
}


# Usage: erase_pkgs p1 p2 p3 ...
# Erases named packages using tdnf invoked with all disabled repos
function erase_pkgs() {
  local -a i_arr=()  # installed pkgs array
  [ $# -eq 0 ] && return 0
  i_arr=( $(find_installed_packages $*) )
  [ ${#i_arr[@]} -eq 0 ] && return 0
  ${TDNF} --disablerepo=* $ASSUME_YES_OPT erase ${i_arr[@]}
  return $?
}

# Usage: backup_configs backup_location p1 p2 p3 ...
# Backs up configurations, if any, of package names provided as arguments into
# the temporary backup location provided as the first argument. The backed up
# configurations will be restored by restore_configs().
function backup_configs() {
  local backup_root_dir
  local p
  local f
  local src_dir
  local tgt_dir
  local rc
  local mode
  local user
  local group
  local -a f_arr=()

  [ $# -le 1 ] && return 0
  backup_root_dir="$1"
  shift
  echo "Backing up configurations in $backup_root_dir."
  [ $# -eq 0 ] && echo "No package configurations needed to be backed up."
  for p in $*; do
    rc=0
    # while verifying package file, check for differences in size (S........)
    # or checksum (..5......). Refer RPM src: rpmVerifyString() in lib/verify.c
    f_arr=(
      $(
        ${RPM} -V $p | ${SED} -nE 's#^((S..)|(..5)).{6}\s+[c]?\s+(/.*)$#\4#p'
      )
    )
    [ ${#f_arr[@]} -gt 0 ] && echo "Backing up configuration of $p."
    for f in ${f_arr[@]}; do
      if [ -d "$f" ]; then
        src_dir="$f"
        tgt_dir="$backup_root_dir/$f"
      else
        src_dir="$($DIRNAME $f)"
        tgt_dir="$backup_root_dir/$src_dir"
      fi
      if [ -e "$tgt_dir" ]; then
        rc=0
      else
        mkdir -p "$tgt_dir"
        rc=$?
        if [ $rc -eq 0 ]; then
          builtin read mode user group <<< $($STAT -c "%a %U %G" $src_dir)
          $CHMOD $mode "$tgt_dir" && $CHOWN "$user:$group" "$tgt_dir" || \
            echoerr "Warning: failed setting mode to $mode or ownership to $user:$group for $tgt_dir/"
        fi
      fi
      if [ $rc -ne 0 ]; then
        echoerr "Error creating $tgt_dir for backing up configuration of $p."
        break
      fi
      if [ ! -d "$f" ]; then
        ${CP} -a "$f" "$tgt_dir"
        rc=$?
        if [ $rc -ne 0 ]; then
          echoerr "Error backing up $f of package $p to $tgt_dir."
          break
        fi
      fi
    done
    [ $rc -ne 0 ] && break
  done
  if [ $rc -ne 0 ]; then
    abort $rc "Please check if /tmp filesystem is full?" \
              "Please freeup space in /tmp and retry."
  fi
  [ $# -gt 0 ] && echo "Package configuration backup completed."
  return 0
}

# Usage: restore_configs backup_location
# Restores the configurations, if any, from the backup location provided as
# argument into the original location, backup of which were created by
# backup_configs() earlier.
function restore_configs() {
  local backup_root_dir
  local bkup_obj
  local orig_obj
  local orig_dir
  local f
  local len
  local p
  local -a dir_arr=()
  local d

  backup_root_dir="$1"
  len=${#backup_root_dir}
  for d in etc opt; do
    if [ -d "$backup_root_dir/$d" ]; then
      dir_arr+=("$backup_root_dir/$d")
    fi
  done
  if [ ${#dir_arr[@]} -gt 0 ]; then
    echo "Restoring configurations of packages."
    while read bkup_obj; do
      orig_obj="${bkup_obj:$len}"
      orig_dir="$($DIRNAME $orig_obj)"
      if [ -d "$orig_dir" ]; then
        if [ ! -d "$orig_obj" ]; then
          ${CP} -a "$bkup_obj" "$orig_obj" || \
            echoerr "Warning: failed restoring $bkup_obj to $orig_obj"
        fi
      fi
    done <<< $($FIND ${dir_arr[@]} ! -type d)
    echo "Configurations of packages were restored."
  fi

  for orig_dir in ${!conf_path_map[@]}; do
    bkup_obj="$backup_root_dir/$orig_dir"
    if [ -d "$bkup_obj" ]; then
      for p in ${conf_path_map[$orig_dir]}; do
        if [ -d "$p" ]; then
          echo "Restoring configurations for $p."
          ${CP} -a $bkup_obj/* $p/ || \
            echoerr "Warning: failed restoring $bkup_obj/* to $p/"
          break
        fi
      done
    fi
  done
}
