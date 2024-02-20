%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Libxml2
Name:           libxml2
Version:        2.9.11
Release:        12%{?dist}
License:        MIT
URL:            http://xmlsoft.org/
Group:          System Environment/General Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        ftp://xmlsoft.org/libxml2/%{name}-%{version}.tar.gz
%define sha512  libxml2=d9c71d75d1cd0708f56fef47802ce53d6c64c4580469458edb2fc12b699319235bcff62bc1be1f0a01f4077726e37ad2cf5e4dee4bca36a9d5d3b21d12253ba5

Patch0:         0001-Work-around-lxml-API.patch
Patch1:         libxml2-CVE-2022-23308.patch
Patch2:         libxml2-CVE-2022-29824.patch
Patch3:         libxml2-CVE-2022-2309-fix1.patch
Patch4:         libxml2-CVE-2022-2309-fix2.patch
Patch5:         libxml2-CVE-2022-40303.patch
Patch6:         libxml2-CVE-2022-40304.patch
Patch7:         libxml2-CVE-2023-29469.patch
Patch8:         libxml2-CVE-2023-28484-1.patch
Patch9:         libxml2-CVE-2023-28484-2.patch
Patch10:        0001-malloc-fail-Fix-memory-leak-in-xmlStaticCopyNodeList.patch
Patch11:        libxml2-CVE-2023-45322.patch
Patch12:        libxml2-CVE-2024-25062.patch

BuildRequires:  python2-devel
BuildRequires:  python2-libs
BuildRequires:  python3-devel
Provides:       pkgconfig(libxml-2.0)

%description
The libxml2 package contains libraries and utilities used for parsing XML files.

%package python
Summary:        The libxml2 python module
Group:          Development/Languages/Python
Requires:       %{name} = %{version}
Requires:       python2
Requires:       python2-libs

%description    python
The libxml2 python module

%package -n     python3-libxml2
Summary:        Python 3 bindings for libxml2.
Group:          Development/Libraries
Requires:       %{name} = %{version}
Requires:       python3

%description -n python3-libxml2
Python3 libxml2.

%package devel
Summary:    Libraries and header files for libxml
Requires:   %{name} = %{version}

%description devel
Static libraries and header files for the support library for libxml

%prep
%autosetup -p1

%build
%configure --disable-static --with-history --with-python=%{_bindir}/python2
make %{?_smp_mflags}

%install
[ %{buildroot} != "/" ] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install %{?_smp_mflags}
find %{buildroot}/%{_libdir} -name '*.la' -delete
make clean %{?_smp_mflags}

%configure --disable-static --with-history --with-python=%{_bindir}/python3
make %{?_smp_mflags}
make DESTDIR=%{buildroot} install %{?_smp_mflags}

%check
make %{?_smp_mflags} check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_libdir}/libxml*
%{_libdir}/xml2Conf.sh
%{_bindir}/*

%files python
%defattr(-,root,root)
%{python2_sitelib}/*

%files -n python3-libxml2
%defattr(-,root,root)
%{python3_sitelib}/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_mandir}/man3/*
%{_libdir}/pkgconfig/libxml-2.0.pc
%{_libdir}/cmake/libxml2/libxml2-config.cmake
%{_docdir}/*
%{_datadir}/gtk-doc/*
%{_mandir}/man1/*
%{_datadir}/aclocal/*

%changelog
* Mon Feb 19 2024 Ashwin Dayanand Kamat <ashwin.kamat@broadcom.com> 2.9.11-12
- Fix for CVE-2024-25062
* Fri Oct 13 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2.9.11-11
- Fix for CVE-2023-45322
* Wed Apr 19 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2.9.11-10
- Fix for CVE-2023-29469/CVE-2023-28484
* Wed Nov 30 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2.9.11-9
- Fix for CVE-2022-40303
* Tue Aug 09 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2.9.11-8
- Fix for CVE-2022-2309
* Mon May 23 2022 Nitesh Kumar <kunitesh@vmware.com> 2.9.11-7
- Fix CVE-2022-29824
* Thu Mar 10 2022 Nitesh Kumar <kunitesh@vmware.com> 2.9.11-6
- Fix CVE-2022-23308
* Wed Dec 01 2021 Shreenidhi Shedi <sshedi@vmware.com> 2.9.11-5
- Remove ldconfig_scriptlets
* Fri Oct 29 2021 Nitesh Kumar <kunitesh@vmware.com> 2.9.11-4
- Moving document, man pages and bins to sub package.
* Wed Oct 06 2021 Tapas Kundu <tkundu@vmware.com> 2.9.11-3
- Fix build with updated python symlink changes
* Sat Jun 19 2021 Ankit Jain <ankitja@vmware.com> 2.9.11-2
- fix for lxml API issue
* Mon May 31 2021 Sujay G <gsujay@vmware.com> 2.9.11-1
- Bump version to 2.9.11 to fix CVE-2021-3517, CVE-2021-3518, CVE-2021-3537.
- Remove other unnecessary patch files.
* Tue Sep 15 2020 Prashant S Chauhan <psinghchauha@vmware.com> 2.9.10-3
- Fix for CVE-2020-24977(Fix Buffer Overflow vulnerability)
* Wed Feb 05 2020 Shreyas B <shreyasb@vmware.com> 2.9.10-2
- Fix for CVE-2019-20388(Fix memory leak in xmlSchemaValidateStream).
* Thu Jan 30 2020 Shreyas B <shreyasb@vmware.com> 2.9.10-1
- Updgrade to v2.9.10 to address CVE-2019-19956(memory leak issue).
- Fix CVE-2020-7595(end-of-file issue).
* Sun Jul 07 2019 Sujay G <gsujay@vmware.com> 2.9.9-1
- Bump version to 2.9.9
* Fri Dec 07 2018 Dweep Advani <dadvani@vmware.com> 2.9.8-2
- Fix CVE-2018-14404 and improve build and install sections
* Tue Sep 11 2018 Keerthana K <keerthanak@vmware.com> 2.9.8-1
- Update to version 2.9.8
* Mon Feb 12 2018 Xiaolin Li <xiaolinl@vmware.com> 2.9.7-1
- Update to version 2.9.7
* Wed Oct 18 2017 Xiaolin Li <xiaolinl@vmware.com> 2.9.6-1
- Update to version 2.9.6
* Mon Oct 2 2017 Anish Swaminathan <anishs@vmware.com> 2.9.4-12
- Remove call to _PyVerify_fd
* Wed Aug 09 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.9.4-11
- Apply patch for CVE-2017-8872
* Mon Aug 07 2017 Danut Moraru <dmoraru@vmware.com> 2.9.4-10
- Change expected parsing error for test for upstream bug 781205 introduced by CVE-2017-9049
* Mon Jul 10 2017 Divya Thaluru <dthaluru@vmware.com> 2.9.4-9
- Apply patch for CVE-2017-9047, CVE-2017-9048, CVE-2017-9049 and CVE-2017-9050
* Thu May 18 2017 Xiaolin Li <xiaolinl@vmware.com> 2.9.4-8
- Move python2 requires to python subpackage.
* Wed Apr 26 2017 Siju Maliakkal <smaliakkal@vmware.com> 2.9.4-7
- Modified python3 version in configure
* Thu Apr 13 2017 Xiaolin Li <xiaolinl@vmware.com> 2.9.4-6
- Added python3-libxml2 package.
* Tue Jan 3 2017 Alexey Makhalov <amakhalov@vmware.com> 2.9.4-5
- Fix for CVE-2016-9318
* Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 2.9.4-4
- Moved man3 to devel subpackage.
* Thu Oct 20 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.9.4-3
- Apply patch for CVE-2016-5131
* Mon Oct 03 2016 Chang Lee <changlee@vmware.com> 2.9.4-2
- Modified check
* Wed Jun 01 2016 Anish Swaminathan <anishs@vmware.com> 2.9.4-1
- Upgrade to 2.9.4
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.9.3-2
- GA - Bump release of all rpms
* Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.9.3-1
- Upgraded to version 2.9.3
* Thu Jan 28 2016 Xiaolin Li <xiaolinl@vmware.com> 2.9.2-1
- Downgrade to version 2.9.2
- libxml 2.9.3 has been found to have major functional issues.
- Until these are resolved, please roadmap updating to 2.9.2.
* Wed Dec 2 2015 Xiaolin Li <xiaolinl@vmware.com> 2.9.3-1
- Update to version 2.9.3
* Thu Jul 2 2015 Mahmoud Bassiouny <mbassiouny@vmware.com> 2.9.1-3
- Seperate the python module from the main library
* Thu Jun 11 2015 Alexey Makhalov <amakhalov@vmware.com> 2.9.1-2
- Moved 'Provides: pkgconfig(...)' into base package
* Mon Oct 13 2014 Divya Thaluru <dthaluru@vmware.com> 2.9.1-1
- Initial build.  First version
