%global aprver  1

Summary:        The Apache Portable Runtime
Name:           apr
Version:        1.7.0
Release:        3%{?dist}
License:        Apache License 2.0
URL:            https://apr.apache.org
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://archive.apache.org/dist/%{name}/%{name}-%{version}.tar.gz
%define sha512  %{name}=daa140c83c7e2c45c3980d9dc81d34fa662bebd050653562c39572d0ddf2eaedb71767c518a59d77f59db9b32e00221ef48b9f72ec3666c4521dd511969f3706

%if 0%{?with_check}
Patch0:         apr-skip-getservbyname-test.patch
%endif

%description
The Apache Portable Runtime.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}
%description    devel
It contains the libraries and header files to create applications.

%prep
%autosetup -p1

%build
%configure \
        --with-installbuilddir=%{_libdir}/apr/build-%{aprver} \
        --with-devrandom=/dev/urandom \
        CC=gcc CXX=g++

%make_build

%install
%make_install %{?_smp_mflags}

%if 0%{?with_check}
%check
make %{?_smp_mflags} check
%endif

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/%{name}/*
%{_libdir}/%{name}.exp
%{_libdir}/libapr*.so*
%exclude %dir %{_libdir}/debug
%exclude %{_libdir}/*.la
%exclude %{_libdir}/*.a
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig
%{_bindir}/*

%files  devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.la
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/pkgconfig

%changelog
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
