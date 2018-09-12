Summary:	Google's C++ gtest framework
Name:		gtest
Version:	1.8.1
Release:	1%{?dist}
License:	ASL 2.0
URL:		https://github.com/google/googletest
Source0:	https://github.com/google/googletest/archive/googletest-%{version}.tar.gz
%define sha1 googletest=152b849610d91a9dfa1401293f43230c2e0c33f8
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
install -p -m 644 -t %{buildroot}/usr/lib64 googlemock/gtest/libgtest.a
install -p -m 644 -t %{buildroot}/usr/lib64 googlemock/gtest/libgtest_main.a
install -vdm 755 %{buildroot}/usr/src/gtest/src/
cp googletest/src/* %{buildroot}/usr/src/gtest/src/
find %{buildroot} -name '*.la' -delete

%files
%defattr(-,root,root)
%{_lib64dir}/libgtest.so
%{_lib64dir}/libgtest_main.so
%{_lib64dir}/libgmock.so
%{_lib64dir}/libgmock_main.so

%files devel
%defattr(-,root,root)
%{_includedir}/gtest/*
/usr/src/gtest/
%{_lib64dir}/cmake/GTest/*.cmake
%{_lib64dir}/pkgconfig/*.pc

%files static
%defattr(-,root,root)
%{_lib64dir}/libgtest.a
%{_lib64dir}/libgtest_main.a

%changelog
*    Wed Sep 12 2018 Anish Swaminathan <anishs@vmware.com> 1.8.1-1
-    Update version to 1.8.1
*    Thu May 04 2017 Anish Swaminathan <anishs@vmware.com> 1.8.0-2
-    Add gtest sources in devel package
*    Mon Apr 10 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.8.0-1
-    Initial version of libgtest package for Photon.
