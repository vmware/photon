Summary:    Text file viewer
Name:       less
Version:    654
Release:    2%{?dist}
URL:        http://www.greenwoodsoftware.com/less
Group:      Applications/File
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: http://www.greenwoodsoftware.com/less/%{name}-%{version}.tar.gz
%define sha512 %{name}=b8fa6688fb2aac4b015dbc000429db45f94c7484f388d1af60ff8fee7f72fec35614e0a3f6eb811583cd899f647b2e01fe47533ab6a7633dac04c155dd415678

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ncurses-devel

Requires: ncurses-libs

%description
The Less package contains a text file viewer

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install %{?_smp_mflags}

%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/*/*

%changelog
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 654-2
- Release bump for SRP compliance
* Tue May 14 2024 Mukul Sikka <msikka@vmware.com> 654-1
- Upgrade version to 654
* Thu Jun 01 2023 Nitesh Kumar <kunitesh@vmware.com> 608-3
- Bump version as a part of ncurses upgrade to v6.4
* Fri Feb 10 2023 Shreenidhi Shedi <sshedi@vmware.com> 608-2
- Fix CVE-2022-46663
* Wed Nov 16 2022 Shreenidhi Shedi <sshedi@vmware.com> 608-1
- Upgrade to v608
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 590-1
- Automatic Version Bump
* Sun Apr 18 2021 Gerrit Photon <photon-checkins@vmware.com> 581-1
- Automatic Version Bump
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 563-1
- Automatic Version Bump
* Fri Jul 17 2020 Sharan Turlapati <sturlapati@vmware.com> 551-2
- Replace ./configure with %configure
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 551-1
- Automatic Version Bump
* Mon Sep 17 2018 Ankit Jain <ankitja@vmware.com> 530-1
- Upgrade version to 530
* Mon Apr 03 2017 Divya Thaluru <dthaluru@vmware.com> 487-1
- Upgrade version to 487
* Tue Oct 18 2016 Anish Swaminathan <anishs@vmware.com>  481-1
- Upgrade version to 481
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 458-2
- GA - Bump release of all rpms
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 458-1
- Initial build. First version.
