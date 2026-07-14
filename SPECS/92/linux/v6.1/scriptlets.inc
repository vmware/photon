%define running_kernel_ver          $(uname -r)
%define modules_backup_loc          /tmp/.%{running_kernel_ver}
%define running_kernel_modules_dir  /lib/modules/%{running_kernel_ver}

# delete dead symlinks and empty dirs at top level only
# if running kernel is re-installed, remove the symlink
%define do_libmodules_housekeeping \
if [ -d "%{running_kernel_modules_dir}" ]; then \
  find /lib/modules -mindepth 1 -maxdepth 1 -xtype l -delete \
  find /lib/modules -mindepth 1 -maxdepth 1 -type d -empty -delete \
  if [ "%{running_kernel_ver}" = "%{uname_r}" ] && [ -L "%{running_kernel_modules_dir}" ]; then \
    rm -f %{running_kernel_modules_dir} \
  fi \
fi \
%{nil}

%pre
%do_libmodules_housekeeping
if [ "%{running_kernel_ver}" = "%{uname_r}" ]; then
  rm -rf %{modules_backup_loc}
fi

%postun
if [ ! -e /boot/photon.cfg ]; then
  list="$(basename "$(ls -1 -tu /boot/linux-*.cfg 2>/dev/null | head -n1)")"
  test -n "$list" && ln -sf "$list" /boot/photon.cfg
fi

if [ ! -s /boot/linux-%{uname_r}.cfg ]; then
  rm -f %{_sharedstatedir}/rpm-state/initramfs/pending/%{uname_r} \
        /boot/initrd.img-%{uname_r}
  echo "initrd of kernel %{uname_r} removed" >&2
fi

if [ -d "%{modules_backup_loc}" ]; then
  if [ ! -s /boot/linux-%{running_kernel_ver}.cfg ]; then

    %do_libmodules_housekeeping

    # if running kernel's modules dir doesn't exist
    # create a symlink which points to backup dir
    if [ ! -d "%{running_kernel_modules_dir}" ]; then
      ln -sfn "%{modules_backup_loc}" "%{running_kernel_modules_dir}"
    fi
  else
    rm -rf "%{modules_backup_loc}"
  fi
fi

%filetriggerun -- /lib/modules/
%do_libmodules_housekeeping
if [ "%{running_kernel_ver}" = "%{uname_r}" ] && [ ! -d "%{modules_backup_loc}" ]; then
  cp -pr "%{running_kernel_modules_dir}" "%{modules_backup_loc}"
fi
