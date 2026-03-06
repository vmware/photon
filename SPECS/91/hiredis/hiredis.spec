%global build_if %{photon_subrelease} <= 91

Summary:        Minimalistic C client library for Redis
Name:           hiredis
Version:        1.1.0
Release:        5.1%{?dist}
Group:          Productivity/Databases/Clients
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/redis/hiredis

Source0: https://github.com/redis/hiredis/archive/v%{version}/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

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
* Fri Mar 06 2026 Mukul Sikka <mukul.sikka@broadcom.com> 1.1.0-5.1
- Backup to SPECS/91
* Thu Oct 16 2025 Harinadh Dommaraju <Harinadh.Dommaraju@broadcom.com> 1.1.0-5
- Version bump up to consume redis v7.2.11
* Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 1.1.0-4
- Release bump for SRP compliance
* Thu Jan 18 2024 Nitesh Kumar <nitesh-nk.kumar@broadcom.com> 1.1.0-3
- Version bump up to consume redis v7.2.4
* Mon Sep 11 2023 Nitesh Kumar <kunitesh@vmware.com> 1.1.0-2
- Bump up version to consume redis v7.0.13
* Tue Dec 13 2022 Gerrit Photon <photon-checkins@vmware.com> 1.1.0-1
- Automatic Version Bump
