Summary:	Program shows full path of (shell) commands
Name:		which
Version:	2.21
Release:	6%{?dist}
License:	GPLv3+
URL:		http://savannah.gnu.org/projects/which
Group:		Development/Tools
Vendor:		VMware, Inc.
Distribution: Photon

Source0:	http://ftp.gnu.org/gnu/which/%{name}-%{version}.tar.gz
%define sha1 %{name}=6b6bec3d2b3d4661c164feb81b9b1d22d1359ded

Conflicts:      toybox < 0.7.3-7

%description
Program for showing the full the path of (shell) commands.

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install
rm -rf %{buildroot}%{_infodir}

%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1/*

%changelog
* Mon Sep 13 2021 Shreenidhi Shedi <sshedi@vmware.com> 2.21-6
- Conflict only with toybox < 0.7.3-7
* Thu Oct 19 2017 Alexey Makhalov <amakhalov@vmware.com> 2.21-5
- Remove infodir
- Use standard configure/build macros
* Mon Oct 02 2017 Alexey Makhalov <amakhalov@vmware.com> 2.21-4
- Added conflicts toybox
* Mon Oct 10 2016 ChangLee <changlee@vmware.com> 2.21-3
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.21-2
- GA - Bump release of all rpms
* Wed Jan 20 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.21-1
- Update to 2.21-1.
* Tue Oct 21 2014 Divya Thaluru <dthaluru@vmware.com> 2.20-1
- Initial build. First version
