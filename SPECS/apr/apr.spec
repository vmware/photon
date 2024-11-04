%define aprver 1
%global __brp_remove_la_files %{nil}

Summary:        The Apache Portable Runtime
Name:           apr
Version:        1.7.2
Release:        3%{?dist}
License:        Apache License 2.0
URL:            https://apr.apache.org/
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://archive.apache.org/dist/%{name}/%{name}-%{version}.tar.gz
%define sha512 %{name}=3fc607af4b8d7e92dc22e35099ebedec5b6ad7c9457ef971bcbdd715d8b1100a76215f75cedf1fc216ac55ae4919c6ea38fb0517025f153c53ec426f0a34f7c2

%if 0%{?with_check}
Patch0:         apr-skip-getservbyname-test.patch
%endif

Patch1:         CVE-2023-49582.patch

Requires:       util-linux-libs

%description
The Apache Portable Runtime.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}
Requires:       util-linux-devel

%description    devel
It contains the libraries and header files to create applications.

%prep
%autosetup -p1

%build
%configure \
        --with-installbuilddir=%{_libdir}/apr/build-%{aprver} \
        --with-devrandom=/dev/urandom \
        CC=gcc CXX=g++

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}

%check
%make_build check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/%{name}/*
%{_libdir}/%{name}.exp
%{_libdir}/libapr*.so.*
%exclude %dir %{_libdir}/debug
%{_bindir}/*

%files  devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.la
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/pkgconfig

%changelog
* Mon Nov 04 2024 Kuntal Nayak <kuntal.nayak@broadcom.com> 1.7.2-3
- Fix CVE-2023-49582
* Mon Dec 18 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.7.2-2
- Fix devel package requires
* Thu Feb 09 2023 Ankit Jain <ankitja@vmware.com> 1.7.2-1
- Fix CVE-2022-24963
* Sun Oct 02 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.7.0-5
- Don't remove .la files, needed during subversion build
* Tue Mar 01 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.7.0-4
- Exclude debug symbols properly
* Thu Oct 28 2021 Ankit Jain <ankitja@vmware.com> 1.7.0-3
- Fix CVE-2021-35940
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
