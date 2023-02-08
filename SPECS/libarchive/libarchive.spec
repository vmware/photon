Summary:         Multi-format archive and compression library
Name:            libarchive
Version:         3.3.3
Release:         9%{?dist}
License:         BSD 2-Clause License
URL:             http://www.libarchive.org
Group:           System Environment/Development
Vendor:          VMware, Inc.
Distribution:    Photon

Source0:         http://www.libarchive.org/downloads/%{name}-%{version}.tar.gz
%define sha512   %{name}=9d12b47d6976efa9f98e62c25d8b85fd745d4e9ca7b7e6d36bfe095dfe5c4db017d4e785d110f3758f5938dad6f1a1b009267fd7e82cb7212e93e1aea237bab7

Patch0:          libarchive-CVE-2018-1000877.patch
Patch1:          libarchive-CVE-2018-1000878.patch
Patch2:          libarchive-CVE-2018-1000879.patch
Patch3:          libarchive-CVE-2018-1000880.patch
Patch4:          libarchive-CVE-2019-1000019.patch
Patch5:          libarchive-CVE-2019-1000020.patch
Patch6:          libarchive-CVE-2019-18408.patch
Patch7:          libarchive-CVE-2019-19221.patch
Patch8:          libarchive-CVE-2020-21674.patch
Patch9:          libarchive-CVE-2021-23177.patch
# Fix for CVE-2021-31566
Patch10:         0001-archive_write_disk_posix-open-a-fd-when-processing-f.patch
Patch11:         0002-archive_write_disk_posix-changes.patch
Patch12:         0003-Do-not-follow-symlinks-when-processing-the-fixup-lis.patch
Patch13:         libarchive-CVE-2022-36227.patch

BuildRequires:  automake
BuildRequires:  xz-libs
BuildRequires:  xz-devel

Requires:       xz-libs

%description
Multi-format archive and compression library

%package	devel
Summary:	Header and development files
Requires:	%{name} = %{version}-%{release}
%description	devel
It contains the libraries and header files to create applications

%prep
%autosetup -p1

%build
autoreconf -ifv
%configure --disable-static
%make_build

%install
%make_install

%check
%if 0%{?with_check}
make %{?_smp_mflags} check
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so.*
%exclude %dir %{_libdir}/debug

%files devel
%defattr(-,root,root)
%{_includedir}
%{_mandir}
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Wed Feb 08 2023 Harinadh D <hdommaraju@vmware.com> 3.3.3-9
- fix for CVE-2022-36277
* Tue Aug 30 2022 Ankit Jain <ankitja@vmware.com> 3.3.3-8
- Fix for CVE-2021-23177, CVE-2021-31566
* Fri Mar 25 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.3.3-7
- Exclude debug symbols properly
* Mon Nov 02 2020 Ankit Jain <ankitja@vmware.com> 3.3.3-6
- Fix for CVE-2020-21674
* Tue Feb 04 2020 Ankit Jain <ankitja@vmware.com> 3.3.3-5
- Fix for CVE-2019-19221
* Fri Nov 08 2019 Ankit Jain <ankitja@vmware.com> 3.3.3-4
- Fix for CVE-2019-18408
* Tue May 21 2019 Ankit Jain <ankitja@vmware.com> 3.3.3-3
- Fix for CVE-2018-1000879,CVE-2018-1000880,CVE-2019-1000019
- CVE-2019-1000020
* Mon Mar 04 2019 Ankit Jain <ankitja@vmware.com> 3.3.3-2
- Fix for CVE-2018-1000877 and CVE-2018-1000878
* Thu Sep 13 2018 Siju Maliakkal <smaliakkal@vmware.com> 3.3.3-1
- Updated to latest version
* Fri Sep 15 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.3.1-2
- Add xz-libs and xz-devel to BuildRequires and Requires
* Mon Apr 03 2017 Divya Thaluru <dthaluru@vmware.com> 3.3.1-1
- Upgrade version to 3.3.1
* Tue Sep 27 2016 Alexey Makhalov <amakhalov@vmware.com> 3.2.1-1
- Update version to 3.2.1
* Thu Sep 22 2016 Anish Swaminathan <anishs@vmware.com> 3.1.2-7
- Adding patch for security fix CVE-2016-6250
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.1.2-6
- GA - Bump release of all rpms
* Mon Oct 12 2015 Xiaolin Li <xiaolinl@vmware.com> 3.1.2-5
- Moving static lib files to devel package.
* Fri Oct 9 2015 Xiaolin Li <xiaolinl@vmware.com> 3.1.2-4
- Removing la files from packages.
* Fri Aug 14 2015 Alexey Makhalov <amakhalov@vmware.com> 3.1.2-3
- Adding patches for security fixes CVE-2013-2011 and CVE-2015-2304.
* Wed Jul 8 2015 Alexey Makhalov <amakhalov@vmware.com> 3.1.2-2
- Added devel package, dist tag. Use macroses part.
* Fri Jun 5 2015 Touseef Liaqat <tliaqat@vmware.com> 3.1.2-1
- Initial build.  First version
