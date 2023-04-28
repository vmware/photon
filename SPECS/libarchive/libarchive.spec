Summary:        Multi-format archive and compression library
Name:           libarchive
Version:        3.6.1
Release:        5%{?dist}
License:        BSD 2-Clause License
URL:            http://www.libarchive.org
Group:          System Environment/Development
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://www.libarchive.org/downloads/%{name}-%{version}.tar.gz
%define sha512  %{name}=58f7ac0c52116f73326a07dec10ff232be33b318862078785dc39f1fb2f8773b5194eabfa14764bb51ce6a5a1aa8820526e7f4c76087a6f4fcbe7789a22275b4

BuildRequires:  xz-libs
BuildRequires:  xz-devel
BuildRequires:  zstd-devel
BuildRequires:  openssl-devel

Requires:       xz-libs
Requires:       zstd
Requires:       openssl >= 1.1.1

%description
Multi-format archive and compression library

%package    devel
Summary:    Header and development files
Requires:   %{name} = %{version}-%{release}

%description    devel
It contains the libraries and header files to create applications

%prep
%autosetup -p1

%build
export CFLAGS="%{optflags}"
%configure --disable-static
%make_build

%install
%make_install %{?_smp_mflags}
find %{buildroot}%{_libdir} -name '*.la' -delete

%if 0%{?with_check}
%check
make %{?_smp_mflags} check
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_bindir}
%exclude %dir %{_libdir}/debug
%files devel
%defattr(-,root,root)
%{_includedir}
%{_mandir}
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.6.1-5
- Bump version as a part of zstd upgrade
* Fri Dec 23 2022 Oliver Kurth <okurth@vmware.com> 3.6.1-4
- bump version as a part of xz upgrade
* Tue Oct 04 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.6.1-3
- Bump version as a part of zstd upgrade
* Sun May 29 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.6.1-2
- Fix binary path
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 3.6.1-1
- Automatic Version Bump
* Wed Aug 04 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 3.5.1-2
- Bump up release for openssl
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 3.5.1-1
- Automatic Version Bump
* Tue Sep 22 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 3.4.3-3
- Make libarchive compatible for openssl-1.1.1
* Tue Sep 08 2020 Ankit Jain <ankitja@vmware.com> 3.4.3-2
- With system zstd compression and decompression
* Tue Jun 30 2020 Gerrit Photon <photon-checkins@vmware.com> 3.4.3-1
- Automatic Version Bump
* Mon Mar 09 2020 Ankit Jain <ankitja@vmware.com> 3.4.2-1
- Updated to Version 3.4.2
* Wed Feb 05 2020 Ankit Jain <ankitja@vmware.com> 3.3.3-3
- Fix for CVE-2019-19221
* Fri Nov 08 2019 Ankit Jain <ankitja@vmware.com> 3.3.3-2
- Fix for CVE-2019-18408,CVE-2018-1000879,CVE-2018-1000880
- CVE-2019-1000019,CVE-2019-1000020,CVE-2018-1000877, CVE-2018-1000878
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
