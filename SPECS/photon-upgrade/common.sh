declare -a core_packages=(
  rpm
)

function prepare_for_upgrade() {
  # Refer https://bugzilla.redhat.com/show_bug.cgi?id=1936422
  if [ -L "/usr/share/squid/errors/es-mx" ]; then
    ${RM} -f "/usr/share/squid/errors/es-mx"
  fi

  # rpm installation fails with cpio error destination /var/log/audit already exists
  if [ -L "/var/log/audit" ]; then
    ${RM} -f "/var/log/audit"
  fi

  # remove toybox from vm & install coreutils
  # toybox is intended for container images only to keep image size small
  if ${RPM} -q --quiet toybox; then
    ${TDNF} erase -y toybox
  fi

  # Now install coreutils
  if ${RPM} -q --quiet coreutils; then
    ${TDNF} reinstall -y coreutils
  else
    ${TDNF} install -y coreutils
  fi
}

function create_core_pkgs_list() {
  if ${RPM} -q --quiet systemd; then
    core_packages+=(systemd systemd-udev)
  fi
}

function update_core_packages()
{
  local rc=0
  create_core_pkgs_list

  if ! ${TDNF} $ASSUME_YES_OPT install ${core_packages[@]}; then
    rc=$?
    abort $rc "Error upgrading rpm package to use the new location."
  fi
}
