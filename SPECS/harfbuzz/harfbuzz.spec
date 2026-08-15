%global build_if %{photon_subrelease} >= 91

Summary:        opentype text shaping engine
Name:           harfbuzz
Version:        14.2.1
Release:        2%{?dist}
URL:            https://github.com/harfbuzz/harfbuzz
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/harfbuzz/harfbuzz/releases/download/%{version}/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  glib-devel
BuildRequires:  freetype2-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  python3-setuptools
BuildRequires:  meson

Requires:       glib
Requires:       freetype2

%description
HarfBuzz is an implementation of the OpenType Layout engine.

%package    devel
Summary:    Header and development files
Requires:   %{name} = %{version}-%{release}
Requires:   glib-devel

%description    devel
It contains the libraries and header files to create applications

%prep
%autosetup -p1

%build
%meson \
    -Dgobject=enabled \
    -Dintrospection=enabled \
    -Dcairo=disabled \
    -Dchafa=disabled \
    -Dpng=disabled \
    -Dicu=disabled \
    -Ddocs=disabled \
    -Dgpu_demo=disabled
%meson_build

%install
%meson_install

%if 0%{?with_check}
%check
%meson_test
%endif

%clean
rm -rf %{buildroot}/*

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_bindir}/*
%{_libdir}/girepository-1.0/*

%files devel
%defattr(-,root,root)
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/cmake/harfbuzz/harfbuzz-config.cmake
%{_datadir}/gir-1.0/HarfBuzz-0.0.gir

%changelog
* Sat Aug 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 14.2.1-2
- Extend to build for 91 and above
* Mon Jul 20 2026 Shivani Agarwal <shivani.agarwal@broadcom.com> 14.2.1-1
- Upgrade version 14.2.1 to fix CVE-2026-22693
* Sat Jun 27 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 7.0.1-6
- Fix aarch64 build
* Tue May 19 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 7.0.1-5
- Enable for 91 subrlease
* Tue Jan 13 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 7.0.1-4
- Add python3-setuptools in BuildRequires for python3.14
* Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 7.0.1-3
- Release bump for SRP compliance
* Wed Apr 19 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 7.0.1-2
- Bump version as a part of freetype2 upgrade
* Tue Feb 21 2023 Shivani Agarwal <shivania2@vmware.com> 7.0.1-1
- Update version 7.0.1
* Wed Nov 23 2022 Shivani Agarwal <shivania2@vmware.com> 2.6.7-3
- Enabled introspection
* Sun Nov 13 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.6.7-2
- Spec fixes
* Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 2.6.7-1
- Automatic Version Bump
* Wed Sep 12 2018 Anish Swaminathan <anishs@vmware.com> 1.9.0-1
- Update to version 1.9.0
* Thu Dec 07 2017 Alexey Makhalov <amakhalov@vmware.com> 1.4.5-2
- Add glib requirement
* Wed Apr 05 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.4.5-1
- Initial version
