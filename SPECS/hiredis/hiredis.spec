Summary:        Minimalistic C client library for Redis
Name:           hiredis
Version:        1.0.2
Release:        2%{?dist}
License:        BSD-3-Clause
Group:          Productivity/Databases/Clients
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/redis/hiredis

Source0: https://github.com/redis/hiredis/archive/v%{version}/%{name}-%{version}.tar.gz
%define sha512 %{name}=86497a1c21869bbe535378885eee6dbd594ef96325966511a3513f81e501af0f5ac7fed864f3230372f3ac7a23c05bad477fa5aa90b9747c9fb1408028174f9b

BuildRequires: make
BuildRequires: redis

%description
Hiredis is a minimalistic C client library for the Redis database.

%package devel
Summary: Development files for %{name}
Group: Development/Libraries/C++
Requires: %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains the header files and
libraries for Redis database.

%prep
%autosetup

%build
%make_build PREFIX="%{_prefix}"

%install
%make_install PREFIX="%{_prefix}"

find %{buildroot} -name '*.a' -delete

%check
make check %{?_smp_mflags}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc COPYING
%{_libdir}/libhiredis.so.1.0.0

%files devel
%doc CHANGELOG.md README.md
%{_includedir}/%{name}/
%{_libdir}/libhiredis.so
%{_libdir}/pkgconfig/hiredis.pc

%changelog
* Thu Jan 18 2024 Nitesh Kumar <nitesh-nk.kumar@broadcom.com> 1.0.2-2
- Version bump up to consume redis v7.0.15
* Mon Apr 04 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.0.2-1
- hiredis initial build
