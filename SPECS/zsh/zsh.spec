# this file is encoded in UTF-8  -*- coding: utf-8 -*-

Summary:      Z shell
Name:         zsh
Version:      5.3.1
Release:      2%{?dist}
License:      MIT
URL:          http://zsh.sourceforge.net/
Group:        System Environment/Shells
Vendor:       VMware, Inc.
Distribution: Photon
Source0:      http://www.zsh.org/pub/%{name}-%{version}.tar.xz
%define sha1  zsh=ec2a98c080f213c1c6c465c0c64662b5eae6818f
Source1:      zprofile.rhs
Source2:      zshrc

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

%build
# make loading of module's dependencies work again (#1277996)
export LIBLDFLAGS='-z lazy'

%configure --enable-etcdir=%{_sysconfdir} --with-tcsetpgrp --enable-maildir-support

make all html

%check
#Ubuntu dev machine can have different test failures like Y01completion.ztst, Y02compmatch.ztst, and Y03arguments.ztst
if `uname -a | grep photon`;then
    mount -t devpts -o gid=4,mode=620 none /dev/pts
    #Skip the C02cond.ztst that failed in Phootn OS chroot.
    rm -f Test/C02cond.ztst
    make check
else
    echo '*** The chroot file system from other OSes does not support all zsh test cases ***'
fi
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
*   Wed Aug 02 2017 Chang Lee <changlee@vmware.com> 5.3.1-2
-   Skip a test case that is not supported from photon OS chroot
*   Wed Apr 05 2017 Xiaolin Li <xiaolinl@vmware.com> 5.3.1-1
-   Updated to version 5.3.1.
*   Sun Jul 24 2016 Ivan Porto Carrero <icarrero@vmware.com> - 5.2-1
-   Initial zsh for photon os
