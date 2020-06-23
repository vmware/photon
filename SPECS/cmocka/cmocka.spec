Summary:       unit testing framework for C
Name:          cmocka
Version:       1.1.5
Release:       1%{?dist}
Group:         Development/Libraries
Vendor:        VMware, Inc.
License:       Apache 2.0
URL:           https://cmocka.org/
Source0:       https://cmocka.org/files/1.1/%{name}-%{version}.tar.xz
%define sha1 cmocka=2c0892423f6653062f45566172b85a4621a74ddb
Distribution:  Photon
BuildRequires: cmake

%description
an elegant unit testing framework for C with support for mock objects. It only requires the standard C library, works on a range of computing platforms (including embedded) and with different compilers.

%prep
%setup

%build
mkdir build
cd build
cmake \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    ..
make

%install
cd build
make DESTDIR=%{buildroot} install

%post

    /sbin/ldconfig

    # First argument is 1 => New Installation
    # First argument is 2 => Upgrade

%clean
rm -rf %{buildroot}/*

%files
%exclude %{_libdir}/cmake
%{_libdir}/libcmocka.*
%{_libdir}/pkgconfig/cmocka.pc
%{_includedir}/*

%changelog
*  Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.1.5-1
-  Automatic Version Bump
*  Fri Sep 07 2018 Ajay Kaher <akaher@vmware.com> 1.1.2-1
-  Upgraded to version 1.1.2
*  Fri Jun 29 2018 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.1.1-1
-  Initial
