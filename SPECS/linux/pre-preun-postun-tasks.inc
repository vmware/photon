%define do_libmodules_housekeeping \
  find /lib/modules -mindepth 1 -maxdepth 1 -xtype l -delete \
  find /lib/modules -mindepth 1 -maxdepth 1 -type d -empty -delete \
  if [ $(uname -r) == %{uname_r} ] && [ -L "/lib/modules/$(uname -r)" ]; then \
    rm -f /lib/modules/$(uname -r) \
  fi \
%{nil}

%pre
%do_libmodules_housekeeping
if [ $(uname -r) == %{uname_r} ]; then
  rm -rf /tmp/.$(uname -r)
fi

%preun
%do_libmodules_housekeeping
if [ $(uname -r) == %{uname_r} ] && [ ! -d "/tmp/.$(uname -r)" ]; then
  cp -r /lib/modules/$(uname -r) /tmp/.$(uname -r)
fi

%postun
if [ ! -e /boot/photon.cfg ]; then
  list="$(basename "$(ls -1 -tu /boot/linux-*.cfg 2>/dev/null | head -n1)")"
  test -n "$list" && ln -sf "$list" /boot/photon.cfg
fi

if [ $(uname -r) == %{uname_r} ] && [ -d "/tmp/.$(uname -r)" ]; then
  %do_libmodules_housekeeping

  if [ ! -d "/lib/modules/$(uname -r)" ]; then
    ln -sfn /tmp/.$(uname -r) /lib/modules/$(uname -r)
  else
    rm -rf /tmp/.$(uname -r)
  fi
fi
