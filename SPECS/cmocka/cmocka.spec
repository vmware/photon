Summary:       unit testing framework for C
Name:          cmocka
Version:       1.1.5
Release:       4%{?dist}
Group:         Development/Libraries
Vendor:        VMware, Inc.
URL:           https://cmocka.org
Distribution:  Photon

Source0:       https://cmocka.org/files/1.1/%{name}-%{version}.tar.xz

Source1: license.txt
%include %{SOURCE1}

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
%cmake \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
    -DCMAKE_BUILD_TYPE=Debug \
    -DWITH_CMOCKERY_SUPPORT=ON \
    -DUNIT_TESTING=ON

%cmake_build

%install
%cmake_install

%if 0%{?with_check}
%check
%ctest
%endif

%postun
/sbin/ldconfig

%post
/sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%{_libdir}/libcmocka.*

%files devel
%{_libdir}/cmake
%{_libdir}/pkgconfig/cmocka.pc
%{_includedir}/*

%changelog
* Thu Dec 12 2024 HarinadhD <harinadh.dommaraju@broadcom.com> 1.1.5-4
- Release bump for SRP compliance
* Mon Jun 20 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.1.5-3
- Introduce devel sub package
- Use cmake macros for build
* Thu Jun 25 2020 Ajay Kaher <akaher@vmware.com> 1.1.5-2
- Corrected include file path
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.1.5-1
- Automatic Version Bump
* Fri Sep 07 2018 Ajay Kaher <akaher@vmware.com> 1.1.2-1
- Upgraded to version 1.1.2
* Fri Jun 29 2018 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.1.1-1
- Initial
