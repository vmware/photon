Summary:    Library for the arithmetic of complex numbers
Name:       mpc
Version:    1.3.1
Release:    2%{?dist}
URL:        http://www.multiprecision.org
Group:      Applications/System
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: http://www.multiprecision.org/mpc/download/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires: gmp-devel
BuildRequires: mpfr-devel

Requires: gmp
Requires: mpfr

%description
The MPC package contains a library for the arithmetic of complex
numbers with arbitrarily high precision and correct rounding of
the result.

%package devel
Summary: Headers and shared development libraries for MPC
Requires: %{name} = %{version}-%{release}
Requires: gmp-devel
Requires: mpfr-devel

%description devel
Header files and shared library symlinks for the MPC library.

%prep
%autosetup -p1

%build
%configure \
    --disable-silent-rules  \
    --disable-static

%install
%make_install %{?_smp_mflags}
rm -rf %{buildroot}%{_infodir}

%check
%make_build check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so

%changelog
* Sun Oct 08 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.3.1-2
- Fix requires
- Introduce devel package
* Tue Dec 13 2022 Gerrit Photon <photon-checkins@vmware.com> 1.3.1-1
- Automatic Version Bump
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 1.2.1-1
- Automatic Version Bump
* Wed Sep 04 2019 Alexey Makhalov <amakhalov@vmware.com> 1.1.0-2
- Bump up release number to get generic mtune option from gmp.h
* Mon Sep 10 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 1.1.0-1
- Update to version 1.1.0
* Mon Oct 03 2016 ChangLee <changLee@vmware.com> 1.0.3-3
- Modified check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.3-2
- GA - Bump release of all rpms
* Tue Jan 12 2016 Anish Swaminathan <anishs@vmware.com>  1.0.3-1
- Update version.
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 1.0.2-1
- Initial build. First version
