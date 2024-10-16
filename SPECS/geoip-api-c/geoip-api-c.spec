Summary:        Library to find geographical and network information of an IP address
Name:           geoip-api-c
Version:        1.6.12
Release:        4%{?dist}
License:        LGPLv2+
URL:            https://github.com/maxmind/geoip-api-c
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/maxmind/geoip-api-c/releases/download/v%{version}/GeoIP-%{version}.tar.gz
%define sha512 GeoIP=a1c8120692a7ba6de5836550917f86f4797dd236a8b7d71b6f92b5389e4b071d89e57036654f5de1d4b762730a2a5c331c31414eab0c889c9befaa097941fee7

BuildRequires:  coreutils >= 9.1-7
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  zlib-devel
BuildRequires:  sed

Requires: bash
Requires: glibc

%description
The GeoIP Legacy C library enables the user to find geographical and network information of an IP address using Geolite Legacy country or city databases.

%package devel
Summary:    Development headers and libraries for GeoIP
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Provides:   geoip-devel = %{version}-%{release}

%description devel
Development headers and static libraries for building GeoIP applications.

%prep
%autosetup -p1 -n GeoIP-%{version}

%build
%configure \
    --disable-static \
    --disable-dependency-tracking

%make_build

%install
%make_install %{?_smp_mflags}

%if 0%{?with_check}
%check
make %{?_smp_mflags} -k check
%endif

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/geoiplookup
%{_bindir}/geoiplookup6
%{_libdir}/libGeoIP.so.1*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root)
%{_includedir}/GeoIP*.h
%{_libdir}/libGeoIP.so
%{_libdir}/pkgconfig/geoip.pc

%changelog
* Wed Oct 16 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.6.12-4
- Require coreutils only
* Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.6.12-3
- Bump version as a part of zlib upgrade
* Sun Feb 12 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.6.12-2
- Fix build requires
* Fri Sep 14 2018 Keerthana K <keerthanak@vmware.com> 1.6.12-1
- Update to version 1.6.12
* Wed Apr 05 2017 Danut Moraru <dmoraru@vmware.com> 1.6.10-1
- Upgrade geoip-api-c to 1.6.10
* Wed Jul 27 2016 Anish Swaminathan <anishs@vmware.com> 1.6.9-1
- Initial build.  First version
