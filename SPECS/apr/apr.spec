%global aprver  1
%global __brp_remove_la_files %{nil}

Summary:        The Apache Portable Runtime
Name:           apr
Version:        1.7.4
Release:        3%{?dist}
License:        Apache License 2.0
URL:            https://apr.apache.org
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://archive.apache.org/dist/%{name}/%{name}-%{version}.tar.gz
%define sha512 %{name}=a8c90062eb78b6a33efc968959d1aadc1a73a4d40dbdb7d2745be54471de6d4c28dc154c85e9c5b9a172ac81735b69636d22b3b85d0b7d7c7f7e2670609da3cc

%if 0%{?with_check}
Patch0: apr-skip-getservbyname-test.patch
%endif

Requires:       util-linux-libs

%description
The Apache Portable Runtime.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}
Requires:       util-linux-devel
Requires:       libxcrypt-devel

%description    devel
It contains the libraries and header files to create applications.

%prep
%autosetup -p1

%build
%configure \
        --with-installbuilddir=%{_libdir}/%{name}/build-%{aprver} \
        --with-devrandom=/dev/urandom \
        CC=gcc CXX=g++

%make_build

%install
%make_install %{?_smp_mflags}

%check
%make_build check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/%{name}/*
%{_libdir}/%{name}.exp
%{_libdir}/libapr*.so.*
%exclude %dir %{_libdir}/debug
%{_bindir}/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/pkgconfig

%changelog
* Fri Apr 11 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.7.4-3
- Fix devel package requires
* Mon Apr 01 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.7.4-2
- Bump version as a part of util-linux upgrade
* Wed Mar 06 2024 Ashwin Dayanand Kamat <ashwin.kamat@broadcom.com> 1.7.4-1
- Upgrade apr package to v1.7.4
* Fri Aug 25 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.7.0-5
- Fix devel package requires
* Sun Aug 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.7.0-4
- Don't remove .la files, needed during subversion build
* Mon Feb 28 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.7.0-3
- Fix binary path
* Tue Feb 16 2021 Ankit Jain <ankitja@vmware.com> 1.7.0-2
- Fix make check
* Mon Jul 13 2020 Gerrit Photon <photon-checkins@vmware.com> 1.7.0-1
- Automatic Version Bump
* Tue Sep 18 2018 Ankit Jain <ankitja@vmware.com> 1.6.5-1
- Updated to version 1.6.5
* Fri Dec 08 2017 Xiaolin Li <xiaolinl@vmware.com> 1.5.2-7
- Fix CVE-2017-12613
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.5.2-6
- GA - Bump release of all rpms
* Mon Sep 21 2015 Harish Udaiya Kumar<hudaiyakumar@vmware.com> 1.5.2-5
- Repacked to move the include files in devel package.
* Wed Jul 15 2015 Sarah Choi <sarahc@vmware.com> 1.5.2-4
- Use aprver(=1) instead of version for mesos
* Mon Jul 13 2015 Alexey Makhalov <amakhalov@vmware.com> 1.5.2-3
- Exclude /usr/lib/debug
* Wed Jul 01 2015 Touseef Liaqat <tliaqat@vmware.com> 1.5.2-2
- Fix tags and paths.
* Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 1.5.2-1
- Initial build. First version
