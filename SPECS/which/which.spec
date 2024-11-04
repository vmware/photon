Summary:    Program shows full path of (shell) commands
Name:       which
Version:    2.21
Release:    7%{?dist}
URL:        http://savannah.gnu.org/projects/which
Group:      Development/Tools
Vendor:     VMware, Inc.
Distribution: Photon

Source0: http://ftp.gnu.org/gnu/which/%{name}-%{version}.tar.gz
%define sha512 %{name}=d2f04a5c5291f2d7d1226982da7cf999d36cfe24d3f7bda145508efcfb359511251d3c68b860c0ddcedd66b15a0587b648a35ab6d1f173707565305c506dfc61

Source1: license.txt
%include %{SOURCE1}

Conflicts:      toybox < 0.8.2-2

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
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.21-7
- Release bump for SRP compliance
* Thu Apr 16 2020 Alexey Makhalov <amakhalov@vmware.com> 2.21-6
- Do not conflict with toybox >= 0.8.2-2
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
