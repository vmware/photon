Summary:	Google's C++ gmock framework
Name:		gmock
Version:	1.8.0
Release:	1%{?dist}
License:	ASL 2.0
URL:		https://github.com/google/googletest
Source0:	https://github.com/google/googletest/archive/googletest-%{version}.tar.gz
%define sha1 googletest=e7e646a6204638fe8e87e165292b8dd9cd4c36ed
Group:		Development/Tools
Vendor:		VMware, Inc.
Distribution: 	Photon
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  libgcc
BuildRequires:  libtool
BuildRequires:  linux-devel
BuildRequires:  libxml2
BuildRequires:  libxml2-devel
BuildRequires:  python2
BuildRequires:  python2-devel
BuildRequires:  python-xml
Requires:       libxml2
Requires:       python2
Requires:       cmake
Requires:       make

%description
Google's C++ test framework that combines the GoogleTest and GoogleMock projects. This package provides gmock shared libraries.

%package devel
Summary:        libgmock headers and static lib
Group:          Development/Tools
%description devel
This contains libgmock static lib and header files.

%prep
%setup -n googletest-release-%{version}

%build
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -DBUILD_SHARED_LIBS=OFF .
make
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -DBUILD_SHARED_LIBS=ON .
make

%install
make DESTDIR=%{buildroot} install
rm -rf %{buildroot}/%{_includedir}/gtest
rm -f %{buildroot}/%{_libdir}/libgtest*
install -p -m 644 -t %{buildroot}/usr/lib googlemock/libgmock.a
install -p -m 644 -t %{buildroot}/usr/lib googlemock/libgmock_main.a
find %{buildroot} -name '*.la' -delete

%files
%defattr(-,root,root)
%{_libdir}/libgmock.so
%{_libdir}/libgmock_main.so

%files devel
%defattr(-,root,root)
%{_includedir}/gmock/*
%{_libdir}/libgmock.a
%{_libdir}/libgmock_main.a

%changelog
*    Mon Apr 10 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.8.0-1
-    Initial version of libgmock package for Photon.
