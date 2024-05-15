Summary:        Text file viewer
Name:           less
Version:        530
Release:        3%{?dist}
License:        GPLv3+
URL:            http://www.greenwoodsoftware.com/less
Group:          Applications/File
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://www.greenwoodsoftware.com/less/%{name}-%{version}.tar.gz
%define sha512 %{name}=8d83a18b5648c4fe85921a563aa2c40bcf495aeb611098c83cd167b1e2f706649846cdf457c8506ae2683ab362ad970a0b261747349673020894bccdb9acbc10

BuildRequires:  ncurses-devel

Requires:       ncurses
Patch0:         CVE-2024-32487.patch

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
* Tue May 14 2024 Mukul Sikka <msikka@vmware.com> 530-3
- Fix for CVE-2024-32487
* Mon Jul 20 2020 Sharan Turlapati <sturlapati@vmware.com> 530-2
- Replacing ./configure with %configure
* Mon Sep 17 2018 Ankit Jain <ankitja@vmware.com> 530-1
- Upgrade version to 530
* Mon Apr 03 2017 Divya Thaluru <dthaluru@vmware.com> 487-1
- Upgrade version to 487
* Tue Oct 18 2016 Anish Swaminathan <anishs@vmware.com>  481-1
- Upgrade version to 481
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 458-2
- GA - Bump release of all rpms
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 458-1
- Initial build. First version
