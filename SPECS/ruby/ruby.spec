%define rexml_version    3.3.9

Summary:        Ruby
Name:           ruby
Version:        3.1.4
Release:        9%{?dist}
URL:            https://www.ruby-lang.org/en
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://cache.ruby-lang.org/pub/ruby/3.1/%{name}-%{version}.tar.gz
%define sha512 %{name}=41cf1561dd7eb249bb2c2f5ea958884880648cc1d11da9315f14158a2d0ff94b2c5c7d75291a67e57e1813d2ec7b618e5372a9f18ee93be6ed306f47b0d3199a

Patch1:         CVE-2024-27281.patch
Patch2:         CVE-2024-27280.patch
Patch3:         CVE-2023-36617-1.patch
Patch4:         CVE-2023-36617-2.patch
Patch5:         CVE-2024-27282.patch
Patch6:         0001-Modify-code-to-upgrade-rexml-3.2.5-to-rexml-3.3.9.patch

Source1:        macros.ruby

Source2:        rexml-%{rexml_version}.tar.gz
%define sha512  rexml-%{rexml_version}.tar.gz=cc38609e5321f157b0a9ea793386017c8d4f743aabd66fc31a8f450f68c57e89825ec1d549efc4e2459ae952e57bbc87d47f9a0affa457639b89b9374e0bb137

Source3: license.txt
%include %{SOURCE3}

BuildRequires:  openssl-devel
BuildRequires:  ca-certificates
BuildRequires:  readline-devel
BuildRequires:  readline
BuildRequires:  tzdata

Requires:       ca-certificates
Requires:       openssl
Requires:       gmp

# CVE-2025-0306 requires "rsa: add implicit rejection in PKCS#1 v1.5 patch in openssl".
# This patch is present in openssl from 3.0.13-2 version
Requires:       openssl >= 3.0.13-2

Obsoletes:      rubygem-base64
Obsoletes:      rubygem-connection_pool
Obsoletes:      rubygem-drb
Obsoletes:      rubygem-ruby2-keywords

Provides:      rubygem-base64
Provides:      rubygem-connection_pool
Provides:      rubygem-drb
Provides:      rubygem-ruby2-keywords

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
rm -rf .bundle/gems/rexml-3.2.5
tar -xvpf %{SOURCE2} -C .bundle/gems

rm gems/rexml-3.2.5.gem
cp -p .bundle/gems/rexml-%{rexml_version}/rexml-%{rexml_version}.gem gems/

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

%files devel
%defattr(-,root,root)
%{_rpmmacrodir}/macros.ruby

%changelog
* Tue Feb 04 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.1.4-9
- Fix requireed openssl version
* Mon Feb 03 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 3.1.4-8
- Fix CVE-2025-0306
* Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 3.1.4-7
- Release bump for SRP compliance
* Tue Dec 10 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 3.1.4-6
- Fix CVE-2024-49761 Upgrade rexml to rexml-3.3.9 from rexml-3.2.5
* Mon Oct 21 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 3.1.4-5
- Fix CVE-2024-49416 and, CVE-2024-41123 Upgrade rexml to rexml-3.3.3 from rexml-3.2.5
* Thu Jun 27 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 3.1.4-4
- Fix Syntax error in macros.ruby file
* Mon Apr 29 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 3.1.4-3
- Add Macro definition macros.ruby file
* Mon Apr 29 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 3.1.4-2
- Fix CVE-2024-27282
* Mon Apr 15 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 3.1.4-1
- Upgrade to 3.1.4 to Fix CVE-2024-27280, CVE-2023-36617, CVE-2023-28755
* Tue Mar 26 2024 Mukul Sikka <mukul.sikka@broadcom.com> 3.1.2-6
- Fix CVE-2024-27281
* Wed Feb 07 2024 Mukul Sikka <mukul.sikka@broadcom.com> 3.1.2-5
- Fix CVE-2021-33621
* Tue Jan 30 2024 Shivani Agarwal <shivania2@vmware.com> 3.1.2-4
- Add provides for package rubygem-base64, rubygem-drb, rubygem-connection_pool, rubygem-ruby2-keywords
* Mon Jan 22 2024 Shivani Agarwal <shivania2@vmware.com> 3.1.2-3
- Add obsolete package
* Tue Dec 20 2022 Guruswamy Basavaiah <bguruswamy@vmware.com> 3.1.2-2
- Bump release as a part of readline upgrade
* Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 3.1.2-1
- Automatic Version Bump
* Sat Feb 12 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.7.1-4
- Drop libdb support
* Fri Jun 04 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.7.1-3
- openssl 3.0.0 support
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
