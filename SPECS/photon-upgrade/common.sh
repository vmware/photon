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

# Take care of pre upgrade config changes
function fix_pre_upgrade_config() {
  local s=''
  local python_link=/usr/bin/python

  # fix pam
  echo "Fixing PAM config to avoid authentication failures after upgrading."
  ${SED} -i -E 's/^(\s*\w+\s+\w+\s+pam_tally2?\.so).*$/\1/' /etc/pam.d/*
  echo "Fixing unsupported FipsMode config in ssh*_config for avoiding post upgrade ssh issues."
  ${SED} -i -E 's/^(\s*FipsMode\s+yes\s*)$/#\1/' /etc/ssh/sshd_config /etc/ssh/ssh_config

  # either of sshd or sshd.socket may be active
  for s in sshd sshd.socket; do
    if ${SYSTEMCTL} is-active -q ${s}; then
      ${SYSTEMCTL} restart ${s}
      break
    fi
  done
}
