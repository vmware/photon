%global build_if %{photon_subrelease} >= 91

Summary:        Minimalistic C client library for Redis
Name:           hiredis
Version:        1.1.0
Release:        7%{?dist}
Group:          Productivity/Databases/Clients
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/redis/hiredis

Source0: https://github.com/redis/hiredis/archive/v%{version}/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires: make
# Optional: only needed if %check is enabled (make check requires a running redis/valkey server)
%if 0%{?with_check}
BuildRequires: valkey
%endif

%description
Hiredis is a minimalistic C client library for Redis and Valkey databases.

%package devel
Summary:    Development files for %{name}
Group:      Development/Libraries/C++
Requires:   %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains the header files and
libraries for developing with Redis and Valkey databases.

%prep
%autosetup -p1

%build
%make_build PREFIX=%{_prefix}

%install
%make_install PREFIX=%{_prefix}
# Do not ship static library
rm -f %{buildroot}%{_libdir}/libhiredis.a

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
%{_libdir}/libhiredis.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Tue May 12 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 1.1.0-7
- Move to subrelease >=91
* Thu Mar 05 2026 Mukul Sikka <mukul.sikka@broadcom.com> 1.1.0-6
- hiredis builds standalone (valkey only needed for optional make check)
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
* Wed Jul 27 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.0.2-2
- Bump version as a part of redis upgrade
* Mon Apr 04 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.0.2-1
- hiredis initial build
