# this file is encoded in UTF-8  -*- coding: utf-8 -*-

Summary: Z shell
Name: zsh
Version: 5.2
Release: 1%{?dist}
License: MIT
URL: http://zsh.sourceforge.net/
Group: System Environment/Shells
Vendor:		VMware, Inc.
Distribution: Photon
Source0: http://www.zsh.org/pub/%{name}-%{version}.tar.xz
Source1: zprofile.rhs
Source2: zshrc

# Fix to a minor VCS_INFO bug from http://www.zsh.org/mla/users/2016/msg00008.html
Patch0: zsh-5.2-vcs_info.patch

# prevent zsh from crashing when printing the "out of memory" message (#1300958)
Patch1: zsh-5.2-oom-fatal-error.patch

BuildRequires: coreutils
BuildRequires: tar
BuildRequires: patch
BuildRequires: diffutils
BuildRequires: make
BuildRequires: gcc
BuildRequires: binutils
BuildRequires: linux-api-headers
BuildRequires: sed
BuildRequires: ncurses-devel
BuildRequires: libcap-devel
BuildRequires: texinfo
BuildRequires: gawk
BuildRequires: elfutils
Requires(post): grep
Requires(postun): coreutils grep

Provides: /bin/zsh

%description
The zsh shell is a command interpreter usable as an interactive login
shell and as a shell script command processor.  Zsh resembles the ksh
shell (the Korn shell), but includes many enhancements.  Zsh supports
command line editing, built-in spelling correction, programmable
command completion, shell functions (with autoloading), a history
mechanism, and more.

%package html
Summary: Zsh shell manual in html format
Group: System Environment/Shells

%description html
The zsh shell is a command interpreter usable as an interactive login
shell and as a shell script command processor.  Zsh resembles the ksh
shell (the Korn shell), but includes many enhancements.  Zsh supports
command line editing, built-in spelling correction, programmable
command completion, shell functions (with autoloading), a history
mechanism, and more.

This package contains the Zsh manual in html format.

%prep

%setup -q
%patch0 -p1
%patch1 -p1

%build
# make loading of module's dependencies work again (#1277996)
export LIBLDFLAGS='-z lazy'

%configure --enable-etcdir=%{_sysconfdir} --with-tcsetpgrp --enable-maildir-support

make all html

%check
# Run the testsuite
make check

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall install.info \
  fndir=$RPM_BUILD_ROOT%{_datadir}/%{name}/%{version}/functions \
  sitefndir=$RPM_BUILD_ROOT%{_datadir}/%{name}/site-functions \
  scriptdir=$RPM_BUILD_ROOT%{_datadir}/%{name}/%{version}/scripts \
  sitescriptdir=$RPM_BUILD_ROOT%{_datadir}/%{name}/scripts \
  runhelpdir=$RPM_BUILD_ROOT%{_datadir}/%{name}/%{version}/help

rm -f ${RPM_BUILD_ROOT}%{_bindir}/zsh-%{version}
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}
for i in %{SOURCE1}; do
    install -m 644 $i $RPM_BUILD_ROOT%{_sysconfdir}/"$(basename $i .rhs)"
done

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/skel
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/skel/.zshrc

# This is just here to shut up rpmlint, and is very annoying.
# Note that we can't chmod everything as then rpmlint will complain about
# those without a she-bang line.
for i in checkmail harden run-help zcalc zkbd; do
    sed -i -e 's!/usr/local/bin/zsh!%{_bindir}/zsh!' \
    $RPM_BUILD_ROOT%{_datadir}/zsh/%{version}/functions/$i
    chmod +x $RPM_BUILD_ROOT%{_datadir}/zsh/%{version}/functions/$i
done

sed -i "s!$RPM_BUILD_ROOT%{_datadir}/%{name}/%{version}/help!%{_datadir}/%{name}/%{version}/help!" \
    $RPM_BUILD_ROOT%{_datadir}/zsh/%{version}/functions/{run-help,_run-help}


%clean
rm -rf $RPM_BUILD_ROOT

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
%doc README LICENCE Etc/BUGS Etc/CONTRIBUTORS Etc/FAQ FEATURES MACHINES
%doc NEWS Etc/zsh-development-guide Etc/completion-style-guide
%attr(755,root,root) %{_bindir}/zsh
%{_mandir}/*/*
%{_infodir}/*
%{_datadir}/zsh
%{_libdir}/zsh
%config(noreplace) %{_sysconfdir}/skel/.z*
%config(noreplace) %{_sysconfdir}/z*

%files html
%defattr(-,root,root)
%doc Doc/*.html

%changelog
* Sun Jul 24 2016 Ivan Porto Carrero <icarrero@vmware.com> - 5.2-1
- Initial zsh for photon os
