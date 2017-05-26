Summary:	Google's C++ gmock framework
Name:		gmock
Version:	1.8.0
Release:	2%{?dist}
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

%description
Google's C++ test framework that combines the GoogleTest and GoogleMock projects. This package provides gmock shared libraries.

%package devel
Summary:        libgmock headers
Group:          Development/Tools
%description devel
This contains libgmock header files.

%package static
Summary:        libgmock static lib
Group:          Development/Tools
%description static
This contains libgmock static library.

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
install -vdm 755 %{buildroot}/usr/src/gmock/src/
cp googlemock/src/* %{buildroot}/usr/src/gmock/src/
find %{buildroot} -name '*.la' -delete

%files
%defattr(-,root,root)
%{_libdir}/libgmock.so
%{_libdir}/libgmock_main.so

%files devel
%defattr(-,root,root)
%{_includedir}/gmock/*
/usr/src/gmock/

%files static
%defattr(-,root,root)
%{_libdir}/libgmock.a
%{_libdir}/libgmock_main.a

%changelog
*    Thu May 04 2017 Anish Swaminathan <anishs@vmware.com> 1.8.0-2
-    Add gmock sources in devel package
*    Mon Apr 10 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.8.0-1
-    Initial version of libgmock package for Photon.
