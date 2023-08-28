Summary:    The package automatically configure source code
Name:       autoconf
Version:    2.69
Release:    10%{?dist}
License:    GPLv2
URL:        http://www.gnu.org/software/autoconf
Group:      System Environment/Base
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: http://ftp.gnu.org/gnu/autoconf/%{name}-%{version}.tar.xz
%define sha512 %{name}=995d3e5a8eb1eb37e2b7fae53c6ec7a9b4df997286b7d643344818f94636756b1bf5ff5ea9155e755cb9461149a853dfbf2886fc6bd7132e5afa9c168e306e9b

%if 0%{?with_check}
Patch0: autoconf-make-check.patch
Patch1: make-check-failure.patch
Patch2: make-check-failure1.patch
%endif

BuildRequires: m4

Requires: perl
Requires: m4

BuildArch: noarch

%description
The package contains programs for producing shell scripts that can
automatically configure source code.

%prep
%autosetup -p1

%build
%configure \
    --disable-silent-rules

%make_build

%install
%make_install %{?_smp_mflags}
rm -rf %{buildroot}%{_infodir}

%check
%make_build check TESTSUITEFLAGS="1-500"

%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/*/*
%{_datadir}/autoconf/*

%changelog
* Wed Mar 24 2021 Anish Swaminathan <anishs@vmware.com> 2.69-10
- Fix check macro invocation
* Sun Nov 15 2020 Prashant Singh Chauhan <psinghchauha@vmware.com> 2.69-9
- Fix for make check failure port test to bash 5.0
* Wed Sep 11 2019 Prashant Singh Chauhan <psinghchauha@vmware.com> 2.69-8
- Fix for make check failure
* Wed Oct 17 2018 Dweep Advani <dadvani@vmware.com> 2.69-7
- Build section is changed to used %configure
* Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.69-6
- Fix arch
* Tue Dec 6 2016 Dheeraj Shetty <dheerajs@vmware.com> 2.69-5
- Fixed Bug 1718089 make check failure
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.69-4
- GA - Bump release of all rpms
* Fri Jun 5 2015 Divya Thaluru <dthaluru@vmware.com> 2.69-3
- Adding m4 package to build and run time required package
* Wed Jun 3 2015 Divya Thaluru <dthaluru@vmware.com> 2.69-2
- Adding perl packages to required packages
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.69-1
- Initial build.  First version
