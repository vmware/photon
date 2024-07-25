Summary:        Minimalistic C client library for Redis
Name:           hiredis
Version:        1.1.0
Release:        2%{?dist}
License:        BSD-3-Clause
Group:          Productivity/Databases/Clients
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/redis/hiredis

Source0: https://github.com/redis/hiredis/archive/v%{version}/%{name}-%{version}.tar.gz
%define sha512 %{name}=9dad012c144ed24de6aa413a3a10d19a9d0d9ece18dbc388406cd86c5b98cb66c76c586cb559c601ed13a75051d8921dc2882534cc3605513fde47d57276c3bb

BuildRequires: make
BuildRequires: redis

%description
Hiredis is a minimalistic C client library for the Redis database.

%package devel
Summary:    Development files for %{name}
Group:      Development/Libraries/C++
Requires:   %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains the header files and
libraries for Redis database.

%prep
%autosetup -p1

%build
%make_build PREFIX=%{_prefix}

%install
%make_install PREFIX=%{_prefix}

%if 0%{?with_check}
%check
make check %{?_smp_mflags}
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc COPYING
%{_libdir}/libhiredis.so.*

%files devel
%doc CHANGELOG.md README.md
%{_includedir}/%{name}/
%{_libdir}/libhiredis.a
%{_libdir}/libhiredis.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Mon Sep 11 2023 Nitesh Kumar <kunitesh@vmware.com> 1.1.0-2
- Bump up version to consume redis v7.0.13
* Tue Dec 13 2022 Gerrit Photon <photon-checkins@vmware.com> 1.1.0-1
- Automatic Version Bump
* Wed Jul 27 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.0.2-2
- Bump version as a part of redis upgrade
* Mon Apr 04 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.0.2-1
- hiredis initial build
