Summary:	Man pages
Name:		man-pages
Version:	5.11
Release:	1%{?dist}
License:	GPLv2+ and BSD
URL:		http://www.kernel.org/doc/man-pages
Group:		System Environment/Base
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	http://www.kernel.org/pub/linux/docs/man-pages/%{name}-%{version}.tar.gz
%define sha1    man-pages=3547c3fd8f2dedefd9fbf6021eae8ec990bb351a
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
# /usr/share/man/man2/move_pages.2 conflict with libnuma-devel-2.0.13-1.ph3.x86_64
rm -vf %{buildroot}%{_mandir}/man2/move_pages.2

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
*   Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 5.11-1
-   Automatic Version Bump
*   Wed Oct 21 2020 Sharan Turlapati <sturlapati@vmware.com> 5.08-3
-   Remove conflict with libnuma-devel
*   Fri Sep 25 2020 Michelle Wang <michellew@vmware.com> 5.08-2
-   Remove conflict with libnuma-devel
*   Tue Sep 01 2020 Gerrit Photon <photon-checkins@vmware.com> 5.08-1
-   Automatic Version Bump
*   Thu Jul 09 2020 Gerrit Photon <photon-checkins@vmware.com> 5.05-1
-   Automatic Version Bump
*   Thu Sep 06 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.16-1
-   Update to version 4.16
*   Fri Mar 31 2017 Michelle Wang <michellew@vmware.com> 4.10-1
-   Update pacakge version
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.04-2
-   GA - Bump release of all rpms
*   Thu Feb 25 2016 Anish Swaminathan <anishs@vmware.com>  4.04-1
-   Upgrade to 4.04
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 3.59-1
-   Initial build. First version
