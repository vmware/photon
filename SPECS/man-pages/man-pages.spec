Summary:	Man pages
Name:		man-pages
Version:	3.59
Release:	1%{?dist}
License:	GPLv2+ and BSD
URL:		http://www.kernel.org/doc/man-pages
Group:		System Environment/Base
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	http://www.kernel.org/pub/linux/docs/man-pages/%{name}-%{version}.tar.xz
%define sha1 man-pages=76eae3fb069a6df2195081408e7ea2784722385b
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
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 3.59-1
-	Initial build. First version


