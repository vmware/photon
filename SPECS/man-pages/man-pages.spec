Summary:	Man pages
Name:		man-pages
Version:	4.10
Release:	1%{?dist}
License:	GPLv2+ and BSD
URL:		http://www.kernel.org/doc/man-pages
Group:		System Environment/Base
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	http://www.kernel.org/pub/linux/docs/man-pages/%{name}-%{version}.tar.gz
%define sha1 man-pages=8538ebbf1723ddd4709a9e1670f023463a2be56c
BuildArch:	noarch

%description
The Man-pages package contains over 1,900 man pages.

%prep
%setup -q
%build

%install
make DESTDIR=%{buildroot} install
#	The following man pages conflict with other packages
rm -vf %{buildroot}%{_mandir}/man3/getspnam.3
rm -vf %{buildroot}%{_mandir}/man5/passwd.5

%files

%defattr(-,root,root)
%{_mandir}/man1/*
%{_mandir}/man2/*
%{_mandir}/man3/*
%{_mandir}/man4/*
%{_mandir}/man5/*
%{_mandir}/man6/*
%{_mandir}/man7/*
%{_mandir}/man8/*

%changelog
*       Fri Mar 31 2017 Michelle Wang <michellew@vmware.com> 4.10-1
-       Update pacakge version
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.04-2
-	GA - Bump release of all rpms
* 	Thu Feb 25 2016 Anish Swaminathan <anishs@vmware.com>  4.04-1
- 	Upgrade to 4.04
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 3.59-1
-	Initial build. First version


