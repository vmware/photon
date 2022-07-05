Summary:	Text file viewer
Name:		less
Version:	590
Release:	1%{?dist}
License:	GPLv3+
URL:		http://www.greenwoodsoftware.com/less
Group:		Applications/File
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://www.greenwoodsoftware.com/less/%{name}-%{version}.tar.gz
%define sha512  %{name}=426fa5840fd43c17bd5a452ad35ad24f2d6684623c6914403fd0059af62266bf2138e6828c7d73a1cef26a736c0d2b8ed4ab180eea8297281dae79a4228eb903
BuildRequires:	ncurses-devel
Requires:	ncurses

%description
The Less package contains a text file viewer

%prep
%autosetup

%build
%configure
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} %{?_smp_mflags} install

%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/*/*

%changelog
*   Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 590-1
-   Automatic Version Bump
*   Sun Apr 18 2021 Gerrit Photon <photon-checkins@vmware.com> 581-1
-   Automatic Version Bump
*   Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 563-1
-   Automatic Version Bump
*   Fri Jul 17 2020 Sharan Turlapati <sturlapati@vmware.com> 551-2
-   Replace ./configure with %configure
*   Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 551-1
-   Automatic Version Bump
*   Mon Sep 17 2018 Ankit Jain <ankitja@vmware.com> 530-1
-   Upgrade version to 530
*   Mon Apr 03 2017 Divya Thaluru <dthaluru@vmware.com> 487-1
-   Upgrade version to 487
*   Tue Oct 18 2016 Anish Swaminathan <anishs@vmware.com>  481-1
-   Upgrade version to 481
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 458-2
-   GA - Bump release of all rpms
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 458-1
-   Initial build. First version.
