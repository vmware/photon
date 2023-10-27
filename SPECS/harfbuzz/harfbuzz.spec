Summary:        opentype text shaping engine
Name:           harfbuzz
Version:        7.0.1
Release:        3%{?dist}
License:        MIT
URL:            https://github.com/harfbuzz/harfbuzz
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/harfbuzz/harfbuzz/releases/download/%{version}/%{name}-%{version}.tar.xz
%define sha512  harfbuzz=2f2fe4604c062549bf5975cde4022bb137fc04f05ef99fcb566411408cfd136371eae2139b943f70bd17eb758690cbd5183acd552bc901d13c634da11eea404c
BuildRequires:  glib-devel >= 2.68.4
BuildRequires:  freetype2
BuildRequires:  freetype2-devel
Requires:       glib >= 2.68.4

%description
HarfBuzz is an implementation of the OpenType Layout engine.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}
Requires:       glib-devel >= 2.68.4
%description    devel
It contains the libraries and header files to create applications

%prep
%autosetup
%build
%configure
%make_build

%install
%make_install %{?_smp_mflags}

%check
make %{?_smp_mflags} -k check

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so*
%{_bindir}/*

%files devel
%defattr(-,root,root)
%doc %{_datadir}/gtk-doc
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/cmake/harfbuzz/harfbuzz-config.cmake

%changelog
* Sat Oct 07 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 7.0.1-3
- Bump version as part of glib upgrade
* Wed Apr 19 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 7.0.1-2
- Bump version as a part of freetype2 upgrade
* Tue Feb 21 2023 Shivani Agarwal <shivania2@vmware.com> 7.0.1-1
- Update version 7.0.1 to fix CVE-2023-25193
* Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 2.6.7-1
- Automatic Version Bump
* Wed Sep 12 2018 Anish Swaminathan <anishs@vmware.com> 1.9.0-1
- Update to version 1.9.0
* Thu Dec 07 2017 Alexey Makhalov <amakhalov@vmware.com> 1.4.5-2
- Add glib requirement
* Wed Apr 05 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.4.5-1
- Initial version
