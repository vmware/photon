if [ $1 -eq 0 ]; then
  if [ -f "/root/.bash_logout" ]; then
    rm -f /root/.bash_logout
  fi
  if [ ! -x /bin/sh ]; then
    grep -v '^/bin/sh$'  %{_sysconfdir}/shells | \
        grep -v '^/bin/sh$' > %{_sysconfdir}/shells.rpm && \
        mv %{_sysconfdir}/shells.rpm %{_sysconfdir}/shells
  fi
  if [ ! -x /bin/bash ]; then
    grep -v '^/bin/bash$'  %{_sysconfdir}/shells | \
        grep -v '^/bin/bash$' > %{_sysconfdir}/shells.rpm && \
        mv %{_sysconfdir}/shells.rpm %{_sysconfdir}/shells
  fi
  if [ ! -x %{_bindir}/sh ]; then
    grep -v '^%{_bindir}/sh$'  %{_sysconfdir}/shells | \
        grep -v '^%{_bindir}/sh$' > %{_sysconfdir}/shells.rpm && \
        mv %{_sysconfdir}/shells.rpm %{_sysconfdir}/shells
  fi
  if [ ! -x %{_bindir}/bash ]; then
    grep -v '^%{_bindir}/bash$'  %{_sysconfdir}/shells | \
        grep -v '^%{_bindir}/bash$' > %{_sysconfdir}/shells.rpm && \
        mv %{_sysconfdir}/shells.rpm %{_sysconfdir}/shells
  fi
fi
