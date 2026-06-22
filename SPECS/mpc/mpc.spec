%global build_if %{photon_subrelease} >= 91

Summary:        Library for the arithmetic of complex numbers
Name:           mpc
Version:        1.4.1
Release:        3%{?dist}
URL:            http://www.multiprecision.org
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://www.multiprecision.org/mpc/download/%{name}-%{version}.tar.xz

Source1: license.txt
%include %{SOURCE1}

BuildRequires: gmp-devel
BuildRequires: mpfr-devel

Requires:       gmp
Requires:       mpfr

%description
The MPC package contains a library for the arithmetic of complex
numbers with arbitrarily high precision and correct rounding of
the result.

%package devel
Summary:   Development headers for %{name}
Requires:  %{name} = %{version}-%{release}
Requires:  gmp-devel
Requires:  mpfr-devel
Requires:  pkg-config

%description devel
%{summary}

%prep
%autosetup -p1

%build
%configure \
  --disable-silent-rules \
  --disable-static

%make_build

%install
%make_install %{?_smp_mflags}

find %{buildroot}%{_libdir} -name '*.la' -delete
rm -r %{buildroot}%{_infodir}

%if 0%{?with_check}
%check
%make_build check
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Fri Jun 19 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.4.1-3
- Keep devel package files in devel package only
* Tue Jun 16 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.4.1-2
- Remove mpfr-devel, mpc-devel dependency
- Introduce a place holder devel package
* Wed Jun 03 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 1.4.1-1
- Upgrade to 1.4.1
* Tue Jun 17 2025 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 1.3.1-4
- Release bump for aarch64 SRP compliance
* Wed Dec 11 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 1.3.1-3
- Release bump for SRP compliance
* Tue Sep 24 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.3.1-2
- Bump version to generate SRP provenance file
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
