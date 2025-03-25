Summary:        Libxslt
Name:           libxslt
Version:        1.1.34
Release:        8%{?dist}
License:        MIT
URL:            http://http://xmlsoft.org/libxslt
Group:          System Environment/General Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://xmlsoft.org/sources/%{name}-%{version}.tar.gz
%define sha512 %{name}=1516a11ad608b04740674060d2c5d733b88889de5e413b9a4e8bf8d1a90d712149df6d2b1345b615f529d7c7d3fa6dae12e544da828b39c7d415e54c0ee0776b

Patch0: patch-to-fix-samba-build.patch
Patch1: CVE-2021-30560.patch
Patch2: CVE-2024-55549.patch
Patch3: CVE-2025-24855.patch

Requires:       libxml2
Requires:       libgcrypt

BuildRequires:  libxml2-devel
BuildRequires:  libgcrypt-devel

%description
The libxslt package contains XSLT libraries used for extending libxml2 libraries to support XSLT files.

%package devel
Summary:        Development Libraries for libxslt
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       libgpg-error-devel
Requires:       libxml2-devel

%description devel
Header files for doing development with libxslt.

%prep
%autosetup -p1

%build
autoreconf -vif
%configure \
    $(test %{_host} != %{_build} && echo "--with-sysroot=/target-%{_arch}") \
    --disable-static \
    --without-python

%make_build

%install
%make_install %{?_smp_mflags}
find %{buildroot}%{_libdir} -name '*.la' -delete

%{_fixperms} %{buildroot}/*

%if 0%{?with_check}
%check
%make_build tests
%endif

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_libdir}/*.sh
%{_libdir}/%{name}-plugins
%{_bindir}/*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so
%{_includedir}/*
%{_docdir}/*
%{_datadir}/aclocal/*
%{_mandir}/man3/*

%changelog
* Tue Mar 25 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.1.34-8
- Fix CVE-2024-55549, CVE-2025-24855
* Thu May 04 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.1.34-7
- Fix requires
* Tue Jun 14 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.1.34-6
- Bump up the release to fix CVE-2022-29824
* Tue May 24 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.1.34-5
- Apply patch for CVE-2021-30560
* Thu Nov 18 2021 Nitesh Kumar <kunitesh@vmware.com> 1.1.34-4
- Release bump up to use libxml2 2.9.12-1.
* Fri Feb 19 2021 Shreyas B. <shreyasb@vmware.com> 1.1.34-3
- Increase the maximum number of nested template calls for xml.
* Fri Dec 18 2020 Shreenidhi Shedi <sshedi@vmware.com> 1.1.34-2
- Fix build with new rpm
* Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 1.1.34-1
- Automatic Version Bump
* Tue Dec 17 2019 Shreyas B. <shreyasb@vmware.com> 1.1.32-3
- Apply patch for CVE-2019-5815: READ heap-buffer-overflow in libxslt.
- Apply patch for CVE-2019-18197
- Apply patch for CVE-2019-13118
- Apply patch for CVE-2019-13117
- Apply patch for CVE-2019-11068
* Thu Nov 15 2018 Alexey Makhalov <amakhalov@vmware.com> 1.1.32-2
- Cross compilation support
* Wed Sep 12 2018 Keerthana K <keerthanak@vmware.com> 1.1.32-1
- Update to version 1.1.32.
* Tue Jul 11 2017 Divya Thaluru <dthaluru@vmware.com> 1.1.29-4
- Applied patches for CVE-2015-9019 and CVE-2017-5029.
* Tue May 23 2017 Kumar Kaushik <kaushikk@vmware.com> 1.1.29-3
- Build does not requires python.
* Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 1.1.29-2
- Moved man3 to devel subpackage.
* Fri Oct 21 2016 Vinay Kulkarni <kulkarniv@vmware.com> 1.1.29-1
- Fix CVEs 2016-1683, 2016-1684, 2015-7995 with version 1.1.29
* Mon Oct 03 2016 Chang Lee <changlee@vmware.com> 1.1.28-4
- Modified check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.1.28-3
- GA - Bump release of all rpms
* Tue Jan 19 2016 Xiaolin Li <xiaolinl@vmware.com> 1.1.28-2
- Add a dev subpackage.
* Mon Oct 13 2014 Divya Thaluru <dthaluru@vmware.com> 1.1.28-1
- Initial build.  First version
