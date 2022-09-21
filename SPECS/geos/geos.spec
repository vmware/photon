Summary:    A C++11 library for performing operations on two-dimensional vector geometries
Name:       geos
Version:    3.8.1
Release:    1%{?dist}
License:    LGPLv2
URL:        https://trac.osgeo.org/geos
Group:      System Environment/Development
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: http://download.osgeo.org/geos/%{name}-%{version}.tar.bz2
%define sha512 %{name}=1d8d8b3ece70eb388ea128f4135c7455899f01828223b23890ad3a2401e27104efce03987676794273a9b9d4907c0add2be381ff14b8420aaa9a858cc5941056

BuildRequires: cmake

%description
GEOS (Geometry Engine - Open Source) is a C++ port of the JTS Topology Suite (JTS).
It aims to contain the complete functionality of JTS in C++.

%package    devel
Summary:    Header and development files
Requires:   %{name} = %{version}-%{release}
%description    devel
It contains the libraries and header files

%prep
%autosetup -p1

%build
%cmake \
    -DDEFAULT_BUILD_TYPE=Debug \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir}

%cmake_build

%install
%cmake_install

%if 0%{?with_check}
%check
make %{?_smp_mflags} check
%endif

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc AUTHORS NEWS README.md COPYING
%{_bindir}/geos-config
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/geos
%{_includedir}/geos_c.h
%{_libdir}/*.so
%{_libdir}/cmake/GEOS

%changelog
* Wed Jul 22 2020 Gerrit Photon <photon-checkins@vmware.com> 3.8.1-1
- Automatic Version Bump
* Mon Mar 09 2020 Ankit Jain <ankitja@vmware.com> 3.8.0-1
- Initial build.  First version
