%global build_if %{photon_subrelease} >= 91

Summary:        Ruby
Name:           ruby
Version:        4.0.1
Release:        2%{?dist}
URL:            https://www.ruby-lang.org/en
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://cache.ruby-lang.org/pub/ruby/3.4/%{name}-%{version}.tar.gz

Source1:        macros.ruby

Source3: license.txt
%include %{SOURCE3}

BuildRequires:  openssl-devel
BuildRequires:  ca-certificates
BuildRequires:  readline-devel
BuildRequires:  readline
BuildRequires:  tzdata
BuildRequires:  libffi-devel
BuildRequires:  libyaml-devel

Requires:       ca-certificates
Requires:       openssl
Requires:       gmp
Requires:       libffi
Requires:       libyaml

# CVE-2025-0306 requires "rsa: add implicit rejection in PKCS#1 v1.5 patch in openssl".
# This patch is present in openssl from 3.0.13-2 version
Requires:       openssl >= 3.0.13-2

Obsoletes:      rubygem-base64
Obsoletes:      rubygem-drb
Obsoletes:      rubygem-ruby2-keywords

Provides:      rubygem-base64 = 0.2.0
Provides:      rubygem-drb = 2.2.1
Provides:      rubygem-ruby2-keywords = 0.0.5

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
%if 0%{?with_check} == 0
rm -r test
%endif

%build
%configure \
  --enable-shared \
  --docdir=%{_docdir}/%{name}-%{version} \
  --with-compress-debug-sections=no
%make_build COPY="cp -p"

%install
%make_install %{?_smp_mflags}
# Move macros file into proper place and replace the %%{name} macro, since it
# would be wrongly evaluated during build of other packages.
mkdir -p %{buildroot}%{_rpmmacrodir}
install -m 644 %{SOURCE1} %{buildroot}%{_rpmmacrodir}/macros.ruby
sed -i "s/%%{name}/%{name}/" %{buildroot}%{_rpmmacrodir}/macros.ruby

%if 0%{?with_check}
%check
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
%{_libdir}/*.so.*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/ruby/*
%{_datadir}/ri/*
%{_docdir}/%{name}-%{version}
%{_mandir}/man1/*

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_rpmmacrodir}/macros.ruby

%changelog
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 4.0.1-2
- Extended to build for subrelease 91 and above
* Thu Feb 26 2026 Shivani Agarwal <shivani.agarwal@broadcom.com> 4.0.1-1
- Upgrade to ruby 4.0.1
* Thu Feb 19 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.4.7-3
- Fix provides with proper version info
* Thu Oct 30 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 3.4.7-2
- Fix CVE-2025-58767 Upgrade rexml to rexml-3.4.4 from rexml-3.4.0
* Wed Oct 22 2025 Harinadh Dommaraju <Harinadh.Dommaraju@broadcom.com> 3.4.7-1
- Upgrade to ruby 3.4.7, Fixes CVE-2025-43857
* Wed Oct 15 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 3.4.3-1
- Upgrade to ruby 3.4.3
* Mon Sep 22 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.1.4-12
- Chore cleanups
* Fri Jul 25 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 3.1.4-11
- Remove unintended license for SRP compliance
* Wed Mar 19 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 3.1.4-10
- Fix CVE-2025-27219, CVE-2025-27220 and CVE-2025-27221
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
