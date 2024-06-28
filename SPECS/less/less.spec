Summary:    Text file viewer
Name:       less
Version:    608
Release:    3%{?dist}
License:    GPLv3+
URL:        http://www.greenwoodsoftware.com/less
Group:      Applications/File
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: http://www.greenwoodsoftware.com/less/%{name}-%{version}.tar.gz
%define sha512 %{name}=7945b7f88921832ebb1b45fba8cbb449ee0133342796b654a52c146dfff3d84db18724ee84e53349eeea6017a0ebe2d8eb5366210275981dde7bb7190118fa66

Patch0: CVE-2022-46663.patch

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
* Fri Jun 09 2023 Nitesh Kumar <kunitesh@vmware.com> 608-3
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
