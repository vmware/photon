Summary:        A C++11 library for performing operations on two-dimensional vector geometries
Name:           geos
Version:        3.10.2
Release:        1%{?dist}
License:        LGPLv2
URL:            https://trac.osgeo.org/geos
Group:          System Environment/Development
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://download.osgeo.org/geos/%{name}-%{version}.tar.bz2
%define sha512  %{name}=390381711ccf56b862c2736cf6329200822f121de1c49df52b8b85cabea8c7787b199df2196acacc2e5c677ff3ebe042d93d70e89deadbc19d754499edb65126
BuildRequires:  cmake

%description
GEOS (Geometry Engine - Open Source) is a C++ port of the JTS Topology Suite (JTS).
It aims to contain the complete functionality of JTS in C++.

%package	devel
Summary:	Header and development files
Requires:	%{name} = %{version}-%{release}

%description	devel
It contains the libraries and header files

%prep
%autosetup
mkdir build

%build
pushd build
        %cmake ..
        make %{?_smp_mflags}
popd

%install
pushd build
        make DESTDIR=%{buildroot} install
popd

%check
make %{?_smp_mflags} check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc AUTHORS NEWS README.md COPYING
%{_bindir}/geos-config
%{_bindir}/geosop
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/geos
%{_includedir}/geos_c.h
%{_libdir}/*.so
%{_libdir}/cmake/GEOS
%{_libdir}/pkgconfig/geos.pc

%changelog
*   Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 3.10.2-1
-   Automatic Version Bump
*   Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 3.9.1-1
-   Automatic Version Bump
*   Wed Jul 22 2020 Gerrit Photon <photon-checkins@vmware.com> 3.8.1-1
-   Automatic Version Bump
*   Mon Mar 09 2020 Ankit Jain <ankitja@vmware.com> 3.8.0-1
-   Initial build.  First version.
