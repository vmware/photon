if [ $1 -eq 1 ]; then
  if [ ! -f "/root/.bash_logout" ]; then
    cp %{_sysconfdir}/skel/.bash_logout /root/.bash_logout
  fi

  if [ ! -f %{_sysconfdir}/shells ]; then
    echo "/bin/sh" >> %{_sysconfdir}/shells
    echo "/bin/bash" >> %{_sysconfdir}/shells
    echo "%{_bindir}/sh" >> %{_sysconfdir}/shells
    echo "%{_bindir}/bash" >> %{_sysconfdir}/shells
  else
    grep -q '^/bin/sh$' %{_sysconfdir}/shells || \
        echo "/bin/sh" >> %{_sysconfdir}/shells
    grep -q '^/bin/bash$' %{_sysconfdir}/shells || \
        echo "/bin/bash" >> %{_sysconfdir}/shells
    grep -q '^%{_bindir}/sh$' %{_sysconfdir}/shells || \
        echo "%{_bindir}/sh" >> %{_sysconfdir}/shells
    grep -q '^%{_bindir}/bash$' %{_sysconfdir}/shells || \
        echo "%{_bindir}/bash" >> %{_sysconfdir}/shells
  fi
fi
