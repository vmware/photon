Summary:         Multithreaded IO generation tool
Name:            fio
Version:         3.33
Release:         3%{?dist}
License:         GPLv2
Group:           Applications/System
Vendor:          VMware, Inc.
Distribution:    Photon
URL:             http://git.kernel.dk/?p=fio.git;a=summary
Source0:         https://git.kernel.org/pub/scm/linux/kernel/git/axboe/fio.git/snapshot/%{name}-%{version}.tar.gz
%define sha512   %{name}=d75b0d4ad7bc7c3885d0a41065a80b82b5b3f0eb41e10e02cba9d527eba1ae6573548345f795954ffc6a45375161191a741290cbaf4fda05ab601b49a6aceb32
BuildRequires:   gcc
BuildRequires:   gnupg
BuildRequires:   zlib-devel
BuildRequires:   python3-devel
BuildRequires:   curl-devel
BuildRequires:   openssl-devel
BuildRequires:   make
BuildRequires:   libaio-devel
Requires:        libaio
Requires:        zlib
Recommends:      %{name}-engine-libaio
Recommends:      %{name}-engine-http

%description
Fio spawns a number of threads or processes doing a particular type of I/O
action as specified by the user. fio takes a number of global parameters, each
inherited by the thread unless otherwise parameters given to them overriding
that setting is given. The typical use of fio is to write a job file matching
the I/O load one wants to simulate.

%package engine-libaio
Summary:        Linux libaio engine for %{name}.
Requires:       %{name} = %{version}-%{release}
Requires:       libaio

%description engine-libaio
Linux libaio engine for %{name}.

%package docs
Summary: Files needed for development using %{name} protocol
Requires: %{name} = %{version}-%{release}

%description docs
Package %{name}-docs provide man pages and other docs related to fio.

%package engine-http
Summary:        HTTP engine for %{name}.
Requires:       %{name} = %{version}-%{release}
Requires:       curl-libs
Requires:       openssl

%description engine-http
HTTP engine for %{name}.

%prep
%autosetup -p1
sed -e 's,/usr/local/lib/,%{_libdir}/,g' -i os/os-linux.h

%build
sh ./configure --disable-optimizations --dynamic-libengines
%make_build

%install
%make_install prefix=%{_prefix} mandir=%{_mandir}

%files
%defattr(-,root,root)
%doc MORAL-LICENSE GFIO-TODO SERVER-TODO STEADYSTATE-TODO
%license COPYING
%dir %{_datadir}/%{name}
%{_bindir}/*
%{_datadir}/%{name}/*

%files engine-http
%{_libdir}/fio/fio-http.so

%files engine-libaio
%{_libdir}/fio/fio-libaio.so

%files docs
%defattr(-,root,root)
%doc README.rst REPORTING-BUGS HOWTO.rst examples
%{_mandir}/man1/*

%changelog
* Sun Nov 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.33-3
- Bump version as a part of openssl upgrade
* Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.33-2
- Bump version as a part of zlib upgrade
* Tue Dec 13 2022 Gerrit Photon <photon-checkins@vmware.com> 3.33-1
- Automatic Version Bump
* Mon Jun 06 2022 Piyush Gupta <gpiyush@vmware.com> 3.30-1
- Initial packaging for Photon OS.
