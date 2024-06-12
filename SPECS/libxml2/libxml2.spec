Summary:        Libxml2
Name:           libxml2
Version:        2.9.12
Release:        14%{?dist}
License:        MIT
URL:            http://xmlsoft.org
Group:          System Environment/General Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://download.gnome.org/sources/libxml2/2.9/%{name}-%{version}.tar.gz
%define sha512 %{name}=df1c6486e80f0fcf3c506f3599bcfb94b620c00d0b5d26831bc983daa78d58ec58b5057b1ec7c1a26c694f40199c6234ee2a6dcabf65abfa10c447cb5705abbd

Patch0:  0001-Work-around-lxml-API.patch
Patch1:  libxml2-CVE-2022-23308.patch
Patch2:  libxml2-CVE-2022-29824.patch
Patch3:  libxml2-CVE-2022-2309-fix1.patch
Patch4:  libxml2-CVE-2022-2309-fix2.patch
Patch5:  libxml2-CVE-2022-40303.patch
Patch6:  libxml2-CVE-2022-40304.patch
Patch7:  libxml2-CVE-2023-29469.patch
Patch8:  libxml2-CVE-2023-28484-1.patch
Patch9:  libxml2-CVE-2023-28484-2.patch
Patch10: libxml2-CVE-2023-39615-1.patch
Patch11: libxml2-CVE-2023-39615-2.patch
Patch12: 0001-malloc-fail-Fix-memory-leak-in-xmlStaticCopyNodeList.patch
Patch13: libxml2-CVE-2023-45322.patch
Patch14: libxml2-CVE-2024-25062.patch
Patch15: libxml2-CVE-2024-34459.patch

BuildRequires: python3-devel
BuildRequires: zlib-devel
BuildRequires: pkg-config
BuildRequires: readline-devel
BuildRequires: ncurses-devel

Requires: readline
Requires: ncurses-libs
Requires: zlib

Provides: pkgconfig(libxml-2.0)

%description
The libxml2 package contains libraries and utilities used for parsing XML files.

%package -n     python3-%{name}
Summary:        Python 3 bindings for libxml2.
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       python3

%description -n python3-%{name}
Python3 libxml2.

%package devel
Summary:    Libraries and header files for libxml
Requires:   %{name} = %{version}-%{release}

%description devel
Static libraries and header files for the support library for libxml

%prep
%autosetup -p1

%build
%configure \
    --disable-static \
    --with-history \
    --with-python=%{python3}

%make_build

%install
%make_install
find %{buildroot}%{_libdir} -name '*.la' -delete

%if 0%{?with_check}
%check
%make_build runtests
%endif

%ldconfig_scriptlets

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_libdir}/xml2Conf.sh
%{_bindir}/*

%files -n python3-%{name}
%defattr(-,root,root)
%{python3_sitelib}/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_mandir}/man3/*
%{_libdir}/pkgconfig/libxml-2.0.pc
%{_libdir}/cmake/%{name}/%{name}-config.cmake
%{_docdir}/*
%{_datadir}/gtk-doc/*
%{_mandir}/man1/*
%{_datadir}/aclocal/*

%changelog
* Tue Jun 11 2024 Ashwin Dayanand Kamat <ashwin.kamat@broadcom.com> 2.9.12-14
- Fix for CVE-2024-34459
* Mon Feb 19 2024 Ashwin Dayanand Kamat <ashwin.kamat@broadcom.com> 2.9.12-13
- Fix for CVE-2024-25062
* Fri Oct 13 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2.9.12-12
- Fix for CVE-2023-45322
* Fri Sep 08 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2.9.12-11
- Fix for CVE-2023-39615
* Thu May 04 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.9.12-10
- Fix library file packaging
* Thu Apr 27 2023 Ankit Jain <ankitja@vmware.com> 2.9.12-9
- fixes requires
* Wed Apr 19 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2.9.12-8
- Fix for CVE-2023-29469/CVE-2023-28484
* Fri Dec 02 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2.9.12-7
- Fix for CVE-2022-40304
* Wed Nov 30 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2.9.12-6
- Fix for CVE-2022-40303
* Tue Aug 09 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2.9.12-5
- Fix for CVE-2022-2309
* Tue May 24 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2.9.12-4
- Fix for CVE-2022-29824
* Thu Mar 10 2022 Nitesh Kumar <kunitesh@vmware.com> 2.9.12-3
- Fix CVE-2022-23308
* Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 2.9.12-2
- Bump up to compile with python 3.10
* Fri Oct 29 2021 Nitesh Kumar <kunitesh@vmware.com> 2.9.12-1
- Version Upgrade to 2.9.12 also optmizing the packages.
* Sat Jun 19 2021 Ankit Jain <ankitja@vmware.com> 2.9.11-2
- fix for lxml API issue
* Mon May 31 2021 Sujay G <gsujay@vmware.com> 2.9.11-1
- Bump version to 2.9.11 to fix CVE-2021-3517, CVE-2021-3518, CVE-2021-3537
- Removed previous CVE patches that are un-necessary
* Tue Dec 15 2020 Shreenidhi Shedi <sshedi@vmware.com> 2.9.10-6
- Fix build with new rpm
* Sat Nov 07 2020 Prashant S Chauhan <psinghchauha@vmware.com> 2.9.10-5
- Fix CVE-2019-20388(memory leak issue)
* Tue Oct 13 2020 Tapas Kundu <tkundu@vmware.com> 2.9.10-4
- Fix build with python 3.9
* Tue Sep 15 2020 Prashant S Chauhan <psinghchauha@vmware.com> 2.9.10-3
- Fix for CVE-2020-24977(Fix Buffer Overflow vulnerability)
* Sat Jun 20 2020 Tapas Kundu <tkundu@vmware.com> 2.9.10-2
- Mass removal python2
* Fri Jan 31 2020 Shreyas B <shreyasb@vmware.com> 2.9.10-1
- Updgrade to v2.9.10 to address CVE-2019-19956(memory leak issue).
- Fix CVE-2020-7595(end-of-file issue).
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
