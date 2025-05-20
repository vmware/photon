Summary:          An enhanced version of csh, the C shell
Name:             tcsh
Version:          6.24.06
Release:          5%{?dist}
URL:              http://www.tcsh.org
Group:            System Environment/Shells
Vendor:           VMware, Inc.
Distribution:     Photon

Source0: http://ftp.funet.fi/pub/mirrors/ftp.astron.com/pub/tcsh/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

Provides: /bin/csh
Provides: /bin/%{name}
Provides: csh = %{version}-%{release}

BuildRequires: ncurses-devel

Requires:         ncurses
Requires(post):   /bin/grep
Requires(postun): /bin/grep
Requires(postun): coreutils >= 9.1-10

%description
Tcsh is an enhanced but completely compatible version of csh, the C
shell.  Tcsh is a command language interpreter which can be used both
as an interactive login shell and as a shell script command processor.
Tcsh includes a command line editor, programmable word completion,
spelling correction, a history mechanism, job control and a C language
like syntax.

%prep
%autosetup -p1

%build
%configure
%make_build

%install
mkdir -p %{buildroot}%{_mandir}/man1 %{buildroot}%{_bindir}
install -p -m 755 %{name} %{buildroot}%{_bindir}/%{name}
install -p -m 644 %{name}.man %{buildroot}%{_mandir}/man1/%{name}.1
ln -sf %{name} %{buildroot}%{_bindir}/csh
ln -sf %{name}.1 %{buildroot}%{_mandir}/man1/csh.1

while read lang language; do
  dest=%{buildroot}%{_datadir}/locale/$lang/LC_MESSAGES
  if test -f nls/$language.cat ; then
    mkdir -p $dest
    install -p -m 644 nls/$language.cat $dest/%{name}
    echo "%lang($lang) %{_datadir}/locale/$lang/LC_MESSAGES/%{name}"
  fi
done > %{name}.lang << _EOF
de german
el greek
en C
es spanish
et et
fi finnish
fr french
it italian
ja ja
pl pl
ru russian
uk ukrainian
_EOF

%if 0%{?with_check}
%check
# tcsh expect nonroot user to run a tests
chmod g+w . -R
useradd test -G root -m
sudo -u test make check && userdel test -r -f
%endif

%clean
rm -rf %{buildroot}

%post
if [ $1 -eq 1 ] ; then
  if [ ! -f %{_sysconfdir}/shells ]; then
    echo "%{_bindir}/%{name}" >> %{_sysconfdir}/shells
    echo "%{_bindir}/csh" >> %{_sysconfdir}/shells
    echo "/bin/%{name}" >> %{_sysconfdir}/shells
    echo "/bin/csh" >> %{_sysconfdir}/shells
  else
    grep -q '^%{_bindir}/%{name}$' %{_sysconfdir}/shells || \
    echo "%{_bindir}/%{name}" >> %{_sysconfdir}/shells
    grep -q '^%{_bindir}/csh$' %{_sysconfdir}/shells || \
    echo "%{_bindir}/csh" >> %{_sysconfdir}/shells
    grep -q '^/bin/%{name}$' %{_sysconfdir}/shells || \
    echo "/bin/%{name}" >> %{_sysconfdir}/shells
    grep -q '^/bin/csh$' %{_sysconfdir}/shells || \
    echo "/bin/csh" >> %{_sysconfdir}/shells
  fi
fi

%postun
if [ $1 -eq 0 ] ; then
  if [ ! -x %{_bindir}/%{name} ]; then
    grep -v '^%{_bindir}/%{name}$'  %{_sysconfdir}/shells | \
    grep -v '^%{_bindir}/csh$' > %{_sysconfdir}/shells.rpm && \
    mv %{_sysconfdir}/shells.rpm %{_sysconfdir}/shells
  fi
  if [ ! -x /bin/%{name} ]; then
    grep -v '^/bin/%{name}$'  %{_sysconfdir}/shells | \
    grep -v '^/bin/csh$' > %{_sysconfdir}/shells.rpm && \
    mv %{_sysconfdir}/shells.rpm %{_sysconfdir}/shells
  fi
fi

%files -f %{name}.lang
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_bindir}/csh
%{_mandir}/man1/*.1*

%changelog
* Fri May 09 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 6.24.06-5
- Require coreutils only
* Thu Dec 12 2024 Dweep Advani <dweep.advani@broadcom.com> 6.24.06-4
- Release bump for SRP compliance
* Thu Jun 01 2023 Nitesh Kumar <kunitesh@vmware.com> 6.24.06-3
- Bump version as a part of ncurses upgrade to v6.4
* Sat Jan 28 2023 Shreenidhi Shedi <sshedi@vmware.com> 6.24.06-2
- Fix requires
* Wed Dec 14 2022 Gerrit Photon <photon-checkins@vmware.com> 6.24.06-1
- Automatic Version Bump
* Mon Jul 11 2022 Gerrit Photon <photon-checkins@vmware.com> 6.24.01-1
- Automatic Version Bump
* Tue Apr 19 2022 Gerrit Photon <photon-checkins@vmware.com> 6.24.00-1
- Automatic Version Bump
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 6.22.04-1
- Automatic Version Bump
* Fri Jan 15 2021 Alexey Makhalov <amakhalov@vmware.com> 6.22.02-2
- GCC-10 support.
* Mon Jul 27 2020 Gerrit Photon <photon-checkins@vmware.com> 6.22.02-1
- Automatic Version Bump
* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 6.20.00-4
- Requires coreutils or toybox and /bin/grep
* Tue Jun 6 2017 Alexey Makhalov <amakhalov@vmware.com> 6.20.00-3
- Fix make check issues.
* Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 6.20.00-2
- Ensure non empty debuginfo
* Tue Mar 28 2017 Xiaolin Li <xiaolinl@vmware.com> 6.20.00-1
- Updated to version 6.20.00
* Tue Feb 07 2017 Divya Thaluru <dthaluru@vmware.com> 6.19.00-6
- Added /bin/csh and /bin/tsch entries in /etc/shells
* Wed Dec 14 2016 Alexey Makhalov <amakhalov@vmware.com> 6.19.00-5
- tcsh.glibc-2.24.patch
* Wed May 25 2016 Anish Swaminathan <anishs@vmware.com> 6.19.00-4
- Fix calloc for gcc 5 optimization
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 6.19.00-3
- GA - Bump release of all rpms
* Wed May 4 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 6.19.00-2
- Fix for upgrade issues
* Thu Jan 21 2016 Anish Swaminathan <anishs@vmware.com> 6.19.00-1
- Upgrade version
* Wed Apr 1 2015 Divya Thaluru <dthaluru@vmware.com> 6.18.01-1
- Initial build. First version
