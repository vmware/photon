Summary:        Ruby
Name:           ruby
Version:        2.5.8
Release:        9%{?dist}
License:        BSDL
URL:            https://www.ruby-lang.org/en/
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://cache.ruby-lang.org/pub/ruby/2.5/%{name}-%{version}.tar.bz2
%define sha512  %{name}=037a5a0510d50b4da85f081d934b07bd6e1c9b5a1ab9b069b3d6eb131ee811351cf02b61988dda7d7aa248aec91612a58d00929d342f0b19ddd7302712caec58

Patch0:         CVE-2020-25613.patch
Patch1:         ruby-CVE-2021-31799.patch
Patch2:         CVE-2022-28739.patch
Patch3:         CVE-2021-41817.patch
Patch4:         CVE-2021-41819.patch
Patch5:         CVE-2023-28756.patch
Patch6:         CVE-2021-33621.patch
Patch7:         CVE-2024-27281.patch
Patch8:         CVE-2024-27282.patch
Patch9:         CVE-2024-49761.patch

BuildRequires:  openssl-devel
BuildRequires:  ca-certificates
BuildRequires:  readline-devel
BuildRequires:  readline
BuildRequires:  tzdata

Requires:       ca-certificates
Requires:       openssl
Requires:       gmp

%description
The Ruby package contains the Ruby development environment.
This is useful for object-oriented scripting.

%prep
%autosetup -p1

%build
%configure \
        --enable-shared \
        --docdir=%{_docdir}/%{name}-%{version} \
        --with-compress-debug-sections=no
%make_build COPY="cp -p"

%install
[ %{buildroot} != "/" ] && rm -rf %{buildroot}/*
%make_install

%check
chmod g+w . -R
useradd test -G root -m
sudo -u test  make check TESTS="-v"

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/*
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.so.*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/ruby/*
%{_datadir}/ri/*
%{_docdir}/%{name}-%{version}
%{_mandir}/man1/*

%changelog
* Tue Jan 28 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.5.8-9
- Fix CVE-2024-49761
* Mon Apr 29 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.5.8-8
- Fix CVE-2024-27282
* Wed Mar 27 2024 Mukul Sikka <mukul.sikka@broadcom.com> 2.5.8-7
- Fix CVE-2024-27281
* Tue Feb 27 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.5.8-6
- Fix CVE-2021-41817, CVE-2021-41819, CVE-2023-28756 and CVE-2021-33621
* Wed Jul 05 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 2.5.8-5
- Version bump to build with updated tzdata
* Fri Sep 02 2022 HarinadhD <hdommaraju@vmware.com> 2.5.8-4
- Fix CVE-2022-28739
* Tue Jan 18 2022 HarinadhD <hdommaraju@vmware.com> 2.5.8-3
- Fix CVE-2021-31799
* Mon Nov 02 2020 Sujay G <gsujay@vmware.com> 2.5.8-2
- Fix CVE-2020-25613
* Mon May 11 2020 Sujay G <gsujay@vmware.com> 2.5.8-1
- Bump version to 2.5.8 to fix CVE-2020-10933
* Fri Dec 13 2019 Sujay G <gsujay@vmware.com> 2.5.7-1
- Bump ruby version to 2.5.7, to fix CVE-2019-15845, CVE-2019-16201, CVE-2019-16255
* Mon Sep 09 2019 Sujay G <gsujay@vmware.com> 2.5.4-1
- Bump version to 2.5.4
- Utilising latest tests from 2.5.4 fixes make check issues.
* Thu Jun 13 2019 Sujay G <gsujay@vmware.com> 2.5.3-2
- Fixed ruby build issue, due to elfutils upgrade.
* Tue Jan 01 2019 Sujay G <gsujay@vmware.com> 2.5.3-1
- Update to version 2.5.3, to fix CVE-2018-16395 & CVE-2018-16396
* Tue Sep 11 2018 srinidhira0 <srinidhir@vmware.com> 2.5.1-1
- Update to version 2.5.1
* Fri Jan 12 2018 Xiaolin Li <xiaolinl@vmware.com> 2.4.3-2
- Fix CVE-2017-17790
* Wed Jan 03 2018 Xiaolin Li <xiaolinl@vmware.com> 2.4.3-1
- Update to version 2.4.3, fix CVE-2017-17405
* Fri Sep 29 2017 Xiaolin Li <xiaolinl@vmware.com> 2.4.2-1
- Update to version 2.4.2
* Fri Sep 15 2017 Xiaolin Li <xiaolinl@vmware.com> 2.4.1-5
- [security] CVE-2017-14064
* Tue Sep 05 2017 Chang Lee <changlee@vmware.com> 2.4.1-4
- Built with copy preserve mode and fixed %check
* Mon Jul 24 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.4.1-3
- [security] CVE-2017-9228
* Tue Jun 13 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.4.1-2
- [security] CVE-2017-9224,CVE-2017-9225
- [security] CVE-2017-9227,CVE-2017-9229
* Thu Apr 13 2017 Siju Maliakkal <smaliakkal@vmware.com> 2.4.1-1
- Update to latest 2.4.1
* Wed Jan 18 2017 Anish Swaminathan <anishs@vmware.com> 2.4.0-1
- Update to 2.4.0 - Fixes CVE-2016-2339
* Mon Oct 10 2016 ChangLee <changlee@vmware.com> 2.3.0-4
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.3.0-3
- GA - Bump release of all rpms
* Wed Mar 09 2016 Divya Thaluru <dthaluru@vmware.com> 2.3.0-2
- Adding readline support
* Wed Jan 20 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.3.0-1
- Updated to 2.3.0-1
* Tue Apr 28 2015 Fabio Rapposelli <fabio@vmware.com> 2.2.1-2
- Added SSL support
* Mon Apr 6 2015 Mahmoud Bassiouny <mbassiouny@vmware.com> 2.2.1-1
- Version upgrade to 2.2.1
* Fri Oct 10 2014 Divya Thaluru <dthaluru@vmware.com> 2.1.3-1
- Initial build.  First version
