Summary:	Google's C++ gtest framework
Name:		gtest
Version:	1.11.0
Release:	1%{?dist}
License:	ASL 2.0
URL:		https://github.com/google/googletest
Source0:	https://github.com/google/googletest/archive/googletest-%{version}.tar.gz
%define sha512  googletest=6fcc7827e4c4d95e3ae643dd65e6c4fc0e3d04e1778b84f6e06e390410fe3d18026c131d828d949d2f20dde6327d30ecee24dcd3ef919e21c91e010d149f3a28
Group:		Development/Tools
Vendor:		VMware, Inc.
Distribution: 	Photon
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  gcc

%description
Google's C++ test framework that combines the GoogleTest and GoogleMock projects.
This package provides gtest shared libraries.

%package        devel
Summary:        libgtest headers
Group:          Development/Tools

%description    devel
This contains libgtest header files.

%package        static
Summary:        libgtest static lib
Group:          Development/Tools

%description    static
This contains libgtest static library.

%package -n     gmock
Summary:        Google's C++ gmock framework
Group:          Development/Tools

%description -n gmock
Google's C++ test framework that combines the GoogleTest and GoogleMock projects.
This package provides gmock shared libraries.

%package -n     gmock-devel
Summary:        libgmock headers
Group:          Development/Tools

%description -n gmock-devel
This contains libgmock header files.

%package -n     gmock-static
Summary:        libgtest static lib
Group:          Development/Tools

%description -n gmock-static
This contains libgmock static library.

%prep
%autosetup -n googletest-release-%{version}

%build
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -DBUILD_SHARED_LIBS=OFF .
make %{_smp_mflags}
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -DBUILD_SHARED_LIBS=ON .
make %{_smp_mflags}

%install
make DESTDIR=%{buildroot} %{_smp_mflags} install
install -p -m 644 -t %{buildroot}/usr/lib64 lib/libgmock.a
install -p -m 644 -t %{buildroot}/usr/lib64 lib/libgmock_main.a
install -p -m 644 -t %{buildroot}/usr/lib64 lib/libgtest.a
install -p -m 644 -t %{buildroot}/usr/lib64 lib/libgtest_main.a
install -vdm 755 %{buildroot}/usr/src/gtest/src/
install -vdm 755 %{buildroot}/usr/src/gmock/src/
cp googletest/src/* %{buildroot}/usr/src/gtest/src/
cp googlemock/src/* %{buildroot}/usr/src/gmock/src/
find %{buildroot} -name '*.la' -delete

%files
%defattr(-,root,root)
%{_lib64dir}/libgtest.so
%{_lib64dir}/libgtest_main.so

%files -n gmock
%{_lib64dir}/libgmock.so
%{_lib64dir}/libgmock_main.so

%files devel
%defattr(-,root,root)
%{_includedir}/gtest/*
/usr/src/gtest/
%{_lib64dir}/cmake/GTest/*.cmake
%{_lib64dir}/pkgconfig/*.pc
%{_lib64dir}/libgmock.so.*
%{_lib64dir}/libgmock_main.so.*
%{_lib64dir}/libgtest.so.*
%{_lib64dir}/libgtest_main.so.*

%files -n gmock-devel
%{_includedir}/gmock/*
/usr/src/gmock/

%files -n gmock-static
%defattr(-,root,root)
%{_lib64dir}/libgmock.a
%{_lib64dir}/libgmock_main.a

%files static
%defattr(-,root,root)
%{_lib64dir}/libgtest.a
%{_lib64dir}/libgtest_main.a

%changelog
*    Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 1.11.0-1
-    Automatic Version Bump
*    Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.10.0-1
-    Automatic Version Bump
*    Sun Sep 23 2018 Sharath George <anishs@vmware.com> 1.8.1-2
-    Add gmock subpackage
*    Wed Sep 12 2018 Anish Swaminathan <anishs@vmware.com> 1.8.1-1
-    Update version to 1.8.1
*    Thu May 04 2017 Anish Swaminathan <anishs@vmware.com> 1.8.0-2
-    Add gtest sources in devel package
*    Mon Apr 10 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.8.0-1
-    Initial version of libgtest package for Photon.
