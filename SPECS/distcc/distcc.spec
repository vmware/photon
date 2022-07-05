Name:         distcc
Version:      3.4
Release:      1%{?dist}
Summary:      Distributed C/C++ compilation
License:      GPLv2+
URL:          https://github.com/distcc/distcc
Group:        Applications/File
Vendor:       VMware, Inc.
Distribution: Photon
Source0:      https://github.com/distcc/distcc/archive/v%{version}/%{name}-%{version}.tar.gz
%define sha512  %{name}=de09329fdfa25e08a9b9529190ddaa9ceccb34c8655692edb86f367a8db4a71b750c6e928cb8e5a670f51fbbc02fd1c8524f72e01b3ebaacc1106dc676d18eef
Source1:      hosts.sample
Source2:      distccd.service

BuildRequires: automake
BuildRequires: autoconf
BuildRequires: which
BuildRequires: popt-devel
BuildRequires: python3-devel
BuildRequires: krb5-devel
BuildRequires: binutils-devel
BuildRequires: systemd-rpm-macros
BuildRequires: make

Requires: krb5
Requires: popt
Requires: python3

%description
distcc is a program to distribute builds of C, C++, Objective C or Objective
C++ code across several machines on a network. distcc should always generate
the same results as a local build, is simple to install and use, and is
usually much faster than a local compile.

%package server
Summary: Server for distributed C/C++ compilation

Requires: %{name} = %{version}-%{release}
Requires: krb5
Requires: popt
Requires: systemd

%description server
This package contains the compilation server needed to use %{name}.

%prep
%autosetup -p1

%build
sh ./autogen.sh
%{configure} --with-auth
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}

install -Dm 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/%{name}/hosts
install -Dm 0644 contrib/redhat/sysconfig %{buildroot}%{_sysconfdir}/sysconfig/distccd
install -Dm 0644 %{SOURCE2} %{buildroot}%{_unitdir}/distccd.service
mkdir -p %{buildroot}/usr/lib/%{name} %{buildroot}/usr/lib/gcc-cross
rm -rf %{buildroot}%{_docdir}/*

%post server
%systemd_post distccd.service
%{_sbindir}/update-distcc-symlinks > /dev/null 2>&1

%preun server
%systemd_preun distccd.service

%postun server
%systemd_postun_with_restart distccd.service

%files
%defattr(-,root,root)
%license COPYING
%doc AUTHORS doc/* NEWS README.pump TODO
%doc INSTALL README survey.txt
%{_bindir}/distcc
%{_bindir}/distccmon-text
%{_bindir}/lsdistcc
%{_bindir}/pump
%{_mandir}/man1/distcc.*
%{_mandir}/man1/distccmon*
%{_mandir}/man1/pump*
%{_mandir}/man1/include_server*
%{_mandir}/man1/lsdistcc*
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/hosts
%{python3_sitearch}/include_server*

%files server
%defattr(-,root,root)
%license COPYING
%doc README
%{_bindir}/distccd
%{_unitdir}/*
%{_sysconfdir}/default/distcc
%{_sysconfdir}/distcc/*allow*
%{_mandir}/man1/distccd*
%config(noreplace) %{_sysconfdir}/sysconfig/distccd
%{_sbindir}/update-distcc-symlinks
%dir /usr/lib/%{name}
%dir /usr/lib/gcc-cross

%changelog
* Tue Apr 12 2022 Oliver Kurth <okurth@vmware.com> 3.4-1
- initial build for Photon
