Summary:       unit testing framework for C
Name:          cmocka
Version:       1.1.2
Release:       3%{?dist}
Group:         Development/Libraries
Vendor:        VMware, Inc.
License:       Apache 2.0
URL:           https://cmocka.org
Distribution:  Photon

Source0:       https://cmocka.org/files/1.1/%{name}-%{version}.tar.xz
%define sha512 %{name}=84435c97a4002c111672f8e18a9270a61de18343de19587ba59436617e57997050a63aac2242a79ec892474e824ca382f78af3e74dc1919cc50e04fd88d5e8f4

BuildRequires: cmake

%description
an elegant unit testing framework for C with support for mock objects. It only requires the standard C library, works on a range of computing platforms (including embedded) and with different compilers.

%package devel
Summary:    Develeopment headers and libraries for %{name}.
Requires:   %{name} = %{version}-%{release}

%description     devel
Develeopment headers and libraries for %{name}.

%prep
%autosetup -p1

%build
mkdir build && cd build
cmake \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    ..

%make_build

%install
cd build
%make_install %{?_smp_mflags}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_libdir}/libcmocka.*

%files devel
%defattr(-,root,root)
%{_libdir}/cmake
%{_libdir}/pkgconfig/cmocka.pc
%{_includedir}/*

%changelog
* Mon Aug 01 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.1.2-3
- Add devel sub package
* Mon Jan 24 2022 Ankit Jain <ankitja@vmware.com> 1.1.2-2
- Version Bump to build with new version of cmake
* Fri Sep 07 2018 Ajay Kaher <akaher@vmware.com> 1.1.2-1
- Upgraded to version 1.1.2
* Fri Jun 29 2018 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.1.1-1
- Initial
