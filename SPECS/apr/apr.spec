%define aprver 1
%global __brp_remove_la_files %{nil}

Summary:        The Apache Portable Runtime
Name:           apr
Version:        1.6.5
Release:        3%{?dist}
License:        Apache License 2.0
URL:            https://apr.apache.org/
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://archive.apache.org/dist/%{name}/%{name}-%{version}.tar.gz
%define sha512 %{name}=cfdc6e618fa35fb42cf394855795c6835fd361d4b090e71b6e1cf7c631fdb96cbbed54f2d1584099ea8f7e623a4a968bf7d70a947eee06216caff2db72d55ea8

%if 0%{?with_check}
Patch0:         apr-skip-getservbyname-test.patch
%endif

%description
The Apache Portable Runtime.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}

%description    devel
It contains the libraries and header files to create applications

%prep
%autosetup -p1

%build
sh ./configure --prefix=%{_prefix} \
        --includedir=%{_includedir}/%{name}-%{aprver} \
        --with-installbuilddir=%{_libdir}/%{name}/build-%{aprver} \
        --with-devrandom=/dev/urandom \
        CC=gcc CXX=g++

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}

%check
%if 0%{?with_check}
make %{?_smp_mflags} check
%endif

%files
%defattr(-,root,root)
%{_libdir}/%{name}/*
%{_libdir}/%{name}.exp
%{_libdir}/libapr*.so.*
%exclude %dir %{_libdir}/debug
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
* Sun Aug 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.6.5-3
- Don't remove .la files, needed during subversion build
* Tue Sep 24 2019 Ankit Jain <ankitja@vmware.com> 1.6.5-2
- Fix for makecheck, added a patch for the same
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
