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
    erase_pkgs toybox
  fi

  # Now install coreutils
  if ${RPM} -q --quiet coreutils; then
    ${TDNF} $ASSUME_YES_OPT $REPOS_OPT reinstall coreutils
  else
    install_pkgs coreutils
  fi
}
