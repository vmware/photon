%define rexml_version    3.3.9

Summary:        Ruby
Name:           ruby
Version:        2.7.4
Release:        17%{?dist}
License:        BSDL
URL:            https://www.ruby-lang.org/en
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://cache.ruby-lang.org/pub/ruby/2.7/%{name}-%{version}.tar.bz2
%define sha512  ruby=f144c32c9cb0006dfcfa7d297f83f88b881f68c94f0130346c74dfd8758583a68d22accfd0fc9f31db304ab5ff0bc135bfb2868145c0dec1ee6cec5ac6c3725d

Patch0:         0001-openssl-3.0.0-compatibility.patch
Patch1:         ruby-CVE-2022-28739.patch
Patch2:         ruby-CVE-2021-28965.patch
Patch3:         ruby-CVE-2021-41819.patch
Patch4:         CVE-2021-33621.patch
Patch5:         CVE-2021-41819.patch
Patch6:         CVE-2023-28756.patch
Patch7:         CVE-2021-41817.patch
Patch8:         CVE-2024-27281.patch
Patch9:         CVE-2021-41816.patch
Patch10:        CVE-2023-36617-1.patch
Patch11:        CVE-2023-36617-2.patch
Patch12:        CVE-2023-28755.patch
Patch13:        CVE-2024-27282.patch
Patch14:        CVE-2021-43809.patch
Patch15:        CVE-2025-27219.patch
Patch16:        CVE-2025-27220.patch
Patch17:        CVE-2025-27221-1.patch
Patch18:        CVE-2025-27221-2.patch

Source1: macros.ruby

Source2:        rexml-%{rexml_version}.tar.gz
%define sha512  rexml-%{rexml_version}.tar.gz=cc38609e5321f157b0a9ea793386017c8d4f743aabd66fc31a8f450f68c57e89825ec1d549efc4e2459ae952e57bbc87d47f9a0affa457639b89b9374e0bb137

BuildRequires:  openssl-devel
BuildRequires:  ca-certificates
BuildRequires:  readline-devel
BuildRequires:  readline
BuildRequires:  tzdata

Requires:       ca-certificates
Requires:       openssl
Requires:       gmp

# CVE-2025-0306 requires "rsa: add implicit rejection in PKCS#1 v1.5 patch in openssl".
# This patch is present in openssl from 3.0.13-3 version
Requires:       openssl >= 3.0.13-3

%description
The Ruby package contains the Ruby development environment.
This is useful for object-oriented scripting.

%package devel
Summary:    Development Libraries for ruby
Group:      Development/Libraries
Requires:   findutils
Requires:   libselinux-devel
Requires:   (coreutils or coreutils-selinux)
Requires:   %{name} = %{version}-%{release}

%description devel
Header files for doing development with ruby.

%prep
%autosetup -p1

%build
# Modification to upgrade rexml-3.2.5 to rexml-3.3.9
tar -xvpf %{SOURCE2}
cp -a rexml-%{rexml_version}/lib/rexml/* lib/rexml/
cp -a rexml-%{rexml_version}/test/* test/rexml

# below loop fixes the files in libexec to point correct ruby
# Only verfied and to be used with ruby version 2.7.1
# Any future versions needs to be verified
for f in `grep -ril "\/usr\/local\/bin\/ruby" ./libexec/`; do
  sed -i "s|/usr/local/bin/ruby|/usr/bin/ruby|g" $f
  head -1 $f
done

%configure \
  --enable-shared \
  --docdir=%{_docdir}/%{name}-%{version} \
  --with-compress-debug-sections=no

make %{?_smp_mflags} COPY="cp -p"

%install
[ %{buildroot} != "/" ] && rm -rf %{buildroot}/*
%make_install %{?_smp_mflags}
# Move macros file into proper place and replace the %%{name} macro, since it
# would be wrongly evaluated during build of other packages.
mkdir -p %{buildroot}%{_rpmmacrodir}
install -m 644 %{SOURCE1} %{buildroot}%{_rpmmacrodir}/macros.ruby
sed -i "s/%%{name}/%{name}/" %{buildroot}%{_rpmmacrodir}/macros.ruby

%check
%if 0%{?with_check}
chmod g+w . -R
useradd test -G root -m
sudo -u test make check TESTS="-v" %{?_smp_mflags}
%endif

%post -p /sbin/ldconfig
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
%{_mandir}/man5/*

%files devel
%defattr(-,root,root)
%{_rpmmacrodir}/macros.ruby

%changelog
* Wed Mar 19 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.7.4-17
- Fix CVE-2025-27219, CVE-2025-27220 and CVE-2025-27221
* Tue Feb 04 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.7.4-16
- Fix required openssl version
* Mon Feb 03 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.7.4-15
- Fix CVE-2025-0306
* Tue Dec 10 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.7.4-14
- Fix CVE-2024-49761 Upgrade rexml to rexml-3.3.9 from rexml-3.2.5
* Tue Aug 13 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.7.4-13
- Fix CVE-2021-43809
* Thu Jun 27 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.7.4-12
- Fix Syntax error in macros.ruby file
* Mon Apr 29 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.7.4-11
- Add Macro definition macros.ruby file
* Mon Apr 29 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.7.4-10
- Fix CVE-2024-27282
* Mon Apr 15 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.7.4-9
- Fix CVE-2023-36617, CVE-2023-28755
* Fri Apr 12 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.7.4-8
- Fix CVE-2021-41816
* Wed Mar 27 2024 Mukul Sikka <mukul.sikka@broadcom.com> 2.7.4-7
- Fix CVE-2024-27281
* Wed Feb 07 2024 Mukul Sikka <mukul.sikka@broadcom.com> 2.7.4-6
- Fix CVE-2021-33621, CVE-2021-41817, CVE-2021-41819, CVE-2023-28756
* Thu Dec 15 2022 Shivani Agarwal <shivania2@vmware.com> 2.7.4-5
- Fix CVE-2021-28965, CVE-2021-41819
* Sat Jun 11 2022 Harinadh D <hdommaraju@vmware.com> 2.7.4-4
- fix CVE-2022-28739
* Sat Feb 12 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.7.4-3
- Drop libdb support
* Mon Sep 06 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.7.4-2
- openssl 3.0.0 support
* Mon Aug 30 2021 Sujay G <gsujay@vmware.com> 2.7.4-1
- Bump version to 2.7.4 to fix CVE-2021-31810
* Wed Aug 18 2021 Sujay G <gsujay@vmware.com> 2.7.3-2
- Fix CVE-2021-32066
* Wed Apr 07 2021 Sujay G <gsujay@vmware.com> 2.7.3-1
- Bump version to 2.7.3 to fix CVE-2013-1655
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.7.1-2
- openssl 1.1.1
* Tue Sep 01 2020 Sujay G <gsujay@vmware.com> 2.7.1-1
- Bump version to 2.7.1
* Fri Jul 17 2020 Ankit Jain <ankitja@vmware.com> 2.5.8-2
- Added --with-compress-debug-sections=no to fix build issue
* Wed May 13 2020 Sujay G <gsujay@vmware.com> 2.5.8-1
- Bump version to 2.5.8
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
