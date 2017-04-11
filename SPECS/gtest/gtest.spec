Summary:	Google's C++ gtest framework
Name:		gtest
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

%description
Google's C++ test framework that combines the GoogleTest and GoogleMock projects. This package provides gtest shared libraries.

%package devel
Summary:        libgtest headers
Group:          Development/Tools
%description devel
This contains libgtest header files.

%package static
Summary:        libgtest static lib
Group:          Development/Tools
%description static
This contains libgtest static library.

%prep
%setup -n googletest-release-%{version}

%build
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -DBUILD_SHARED_LIBS=OFF .
make
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -DBUILD_SHARED_LIBS=ON .
make

%install
make DESTDIR=%{buildroot} install
rm -rf %{buildroot}/%{_includedir}/gmock
rm -f %{buildroot}/%{_libdir}/libgmock*
install -p -m 644 -t %{buildroot}/usr/lib googlemock/gtest/libgtest.a
install -p -m 644 -t %{buildroot}/usr/lib googlemock/gtest/libgtest_main.a
find %{buildroot} -name '*.la' -delete

%files
%defattr(-,root,root)
%{_libdir}/libgtest.so
%{_libdir}/libgtest_main.so

%files devel
%defattr(-,root,root)
%{_includedir}/gtest/*

%files static
%defattr(-,root,root)
%{_libdir}/libgtest.a
%{_libdir}/libgtest_main.a

%changelog
*    Mon Apr 10 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.8.0-1
-    Initial version of libgtest package for Photon.
