Summary:	Text file viewer
Name:		less
Version:	487
Release:	2%{?dist}
License:	GPLv3+
URL:		http://www.greenwoodsoftware.com/less
Group:		Applications/File
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://www.greenwoodsoftware.com/less/%{name}-%{version}.tar.gz
%define sha1 less=8a5c4be2a51f11543793defec7ccb77c525f007e
BuildRequires:	ncurses-devel
Requires:	ncurses
%description
The Less package contains a text file viewer
%prep
%setup -q
%build
%configure
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/*/*
%changelog
*   Mon Jul 20 2020 Sharan Turlapati <sturlapati@vmware.com> 487-2
-   Replace ./configure with %configure
*   Mon Apr 03 2017 Divya Thaluru <dthaluru@vmware.com> 487-1
-   Upgrade version to 487
*   Tue Oct 18 2016 Anish Swaminathan <anishs@vmware.com>  481-1
-   Upgrade version to 481
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 458-2
-   GA - Bump release of all rpms
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 458-1
-   Initial build. First version
