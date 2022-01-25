Summary:       unit testing framework for C
Name:          cmocka
Version:       1.1.2
Release:       2%{?dist}
Group:         Development/Libraries
Vendor:        VMware, Inc.
License:       Apache 2.0
URL:           https://cmocka.org/
Source0:       https://cmocka.org/files/1.1/%{name}-%{version}.tar.xz
%define sha1 cmocka=e2f8a9ad07460d256b1ef5923289f0e8377241e2
Distribution:  Photon
BuildRequires: cmake

%description
an elegant unit testing framework for C with support for mock objects. It only requires the standard C library, works on a range of computing platforms (including embedded) and with different compilers.

%prep
%autosetup -p1

%build
mkdir build
cd build
cmake \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    ..
make %{?_smp_mflags}

%install
cd build
make %{?_smp_mflags} DESTDIR=%{buildroot} install

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
*  Mon Jan 24 2022 Ankit Jain <ankitja@vmware.com> 1.1.2-2
-  Version Bump to build with new version of cmake
*  Fri Sep 07 2018 Ajay Kaher <akaher@vmware.com> 1.1.2-1
-  Upgraded to version 1.1.2
*  Fri Jun 29 2018 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.1.1-1
-  Initial
