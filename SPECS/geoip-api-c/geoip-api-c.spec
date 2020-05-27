Summary:        Library to find geographical and network information of an IP address
Name:           geoip-api-c
Version:        1.6.12
Release:        1%{?dist}
License:        LGPLv2+
URL:            https://github.com/maxmind/geoip-api-c
Source0:        https://github.com/maxmind/geoip-api-c/releases/download/v%{version}/GeoIP-%{version}.tar.gz 
%define sha1 GeoIP=ac1a6809afbb7624aff2f6e12ceb300b12de1715
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  coreutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  zlib-devel
BuildRequires:  sed

%description
The GeoIP Legacy C library enables the user to find geographical and network information of an IP address using Geolite Legacy country or city databases.

%package devel
Summary:	Development headers and libraries for GeoIP
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Provides:	geoip-devel = %{version}-%{release}

%description devel
Development headers and static libraries for building GeoIP applications.

%prep
%setup -q -n GeoIP-%{version}

%build
%configure --disable-static --disable-dependency-tracking
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} INSTALL="install -p" install
rm -f %{buildroot}%{_libdir}/*.la

%check
make %{?_smp_mflags} -k check

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%doc AUTHORS ChangeLog NEWS.md README.md COPYING
%{_bindir}/geoiplookup
%{_bindir}/geoiplookup6
%{_libdir}/libGeoIP.so.1*
%{_mandir}/man1/*

%files devel
%{_includedir}/GeoIP*.h
%{_libdir}/libGeoIP.so
%{_libdir}/pkgconfig/geoip.pc

%changelog
*   Fri Sep 14 2018 Keerthana K <keerthanak@vmware.com> 1.6.12-1
-   Update to version 1.6.12
*   Wed Apr 05 2017 Danut Moraru <dmoraru@vmware.com> 1.6.10-1
-   Upgrade geoip-api-c to 1.6.10
*   Wed Jul 27 2016 Anish Swaminathan <anishs@vmware.com> 1.6.9-1
-   Initial build.  First version

