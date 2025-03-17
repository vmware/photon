Summary:          Z shell
Name:             zsh
Version:          5.9
Release:          4%{?dist}
URL:              http://zsh.org
Group:            System Environment/Shells
Vendor:           VMware, Inc.
Distribution:     Photon

Source0: http://www.zsh.org/pub/%{name}-%{version}.tar.xz

Source1: zprofile.rhs
Source2: zshrc

Source3: license.txt
%include %{SOURCE3}

BuildRequires:    (coreutils or coreutils-selinux)
BuildRequires:    tar
BuildRequires:    patch
BuildRequires:    diffutils
BuildRequires:    make
BuildRequires:    gcc
BuildRequires:    binutils
BuildRequires:    linux-api-headers
BuildRequires:    sed
BuildRequires:    ncurses-devel
BuildRequires:    libcap-devel
BuildRequires:    texinfo
BuildRequires:    gawk
BuildRequires:    elfutils

Requires(post):   /bin/grep
Requires(postun): /bin/grep
Requires:       (coreutils or coreutils-selinux)

Provides:         /bin/%{name}

%description
The %{name} shell is a command interpreter usable as an interactive login
shell and as a shell script command processor.  Zsh resembles the ksh
shell (the Korn shell), but includes many enhancements.  Zsh supports
command line editing, built-in spelling correction, programmable
command completion, shell functions (with autoloading), a history
mechanism, and more.

%prep
%autosetup -p1

%build
# make loading of module's dependencies work again (#1277996)
export LIBLDFLAGS='-z lazy'

%configure \
    --enable-etcdir=%{_sysconfdir} \
    --with-tcsetpgrp \
    --enable-maildir-support

%make_build all html

%install
%make_install %{?_smp_mflags} install.info \
  fndir=%{_datadir}/%{name}/%{version}/functions \
  sitefndir=%{_datadir}/%{name}/site-functions \
  scriptdir=%{_datadir}/%{name}/%{version}/scripts \
  sitescriptdir=%{_datadir}/%{name}/scripts \
  runhelpdir=%{_datadir}/%{name}/%{version}/help

rm -f %{buildroot}%{_bindir}/%{name}-%{version} \
      %{buildroot}%{_infodir}/dir

mkdir -p %{buildroot}%{_sysconfdir}/skel

for i in %{SOURCE1}; do
  install -m 644 $i %{buildroot}%{_sysconfdir}/"$(basename $i .rhs)"
done

install -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/skel/.zshrc

for i in checkmail harden run-help zcalc zkbd \
         test-repo-git-rebase-{apply,merge} _path_files; do
  sed -i -e 's!/usr/local/bin/zsh!%{_bindir}/zsh!' \
      %{buildroot}%{_datadir}/%{name}/%{version}/functions/$i
  chmod +x %{buildroot}%{_datadir}/%{name}/%{version}/functions/$i
done

sed -i "s!%{buildroot}%{_datadir}/%{name}/%{version}/help!%{_datadir}/%{name}/%{version}/help!" \
    %{buildroot}%{_datadir}/%{name}/%{version}/functions/{run-help,_run-help}

%clean
rm -rf %{buildroot}

%if 0%{?with_check}
%check
make check %{_smp_mflags}
%endif

%post
if [ "$1" = 1 ]; then
  if [ ! -f %{_sysconfdir}/shells ] ; then
    echo "%{_bindir}/%{name}" > %{_sysconfdir}/shells
    echo "/bin/%{name}" >> %{_sysconfdir}/shells
  else
    grep -q "^%{_bindir}/%{name}$" %{_sysconfdir}/shells || echo "%{_bindir}/%{name}" >> %{_sysconfdir}/shells
    grep -q "^/bin/%{name}$" %{_sysconfdir}/shells || echo "/bin/%{name}" >> %{_sysconfdir}/shells
  fi
fi

%preun

%postun
if [ "$1" = 0 ] && [ -f %{_sysconfdir}/shells ] ; then
  sed -i '\!^%{_bindir}/%{name}$!d' %{_sysconfdir}/shells
  sed -i '\!^/bin/%{name}$!d' %{_sysconfdir}/shells
fi

%files
%defattr(-,root,root)
%attr(755,root,root) %{_bindir}/%{name}
%{_mandir}/*
%{_infodir}/*
%{_libdir}/%{name}/*
%{_datadir}/%{name}/*
%config(noreplace) %{_sysconfdir}/skel/.z*
%config(noreplace) %{_sysconfdir}/z*

%changelog
* Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 5.9-4
- Release bump for SRP compliance
* Wed Jan 25 2023 Shreenidhi Shedi <sshedi@vmware.com> 5.9-3
- Fix requires
- Remove html sub package
* Fri Jan 06 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.9-2
- Bump up due to change in elfutils
* Thu Sep 29 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.9-1
- Upgrade to v5.9
* Tue Apr 19 2022 Gerrit Photon <photon-checkins@vmware.com> 5.8.1-1
- Automatic Version Bump
* Wed Oct 07 2020 Ajay Kaher <akaher@vmware.com> 5.8-2
- Fix ncurses compilation failure
* Mon May 11 2020 Susant Sahani <ssahani@vmware.com> 5.8.1
- Upgrading to 5.8
* Thu Sep 13 2018 Siju Maliakkal <smaliakkal@vmware.com> 5.6.1-1
- Upgrading to latest
* Mon Mar 19 2018 Xiaolin Li <xiaolinl@vmware.com> 5.3.1-5
- Fix CVE-2018-7548
* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 5.3.1-4
- Requires coreutils or toybox and /bin/grep
* Fri Sep 15 2017 Bo Gan <ganb@vmware.com> 5.3.1-3
- Clean up check
* Wed Aug 02 2017 Chang Lee <changlee@vmware.com> 5.3.1-2
- Skip a test case that is not supported from photon OS chroot
* Wed Apr 05 2017 Xiaolin Li <xiaolinl@vmware.com> 5.3.1-1
- Updated to version 5.3.1.
* Sun Jul 24 2016 Ivan Porto Carrero <icarrero@vmware.com> - 5.2-1
- Initial zsh for photon os
