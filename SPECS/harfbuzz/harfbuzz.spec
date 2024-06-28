Summary:        opentype text shaping engine
Name:           harfbuzz
Version:        7.0.1
Release:        2%{?dist}
License:        MIT
URL:            https://github.com/harfbuzz/harfbuzz
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/harfbuzz/harfbuzz/releases/download/%{version}/%{name}-%{version}.tar.xz
%define sha512  %{name}=2f2fe4604c062549bf5975cde4022bb137fc04f05ef99fcb566411408cfd136371eae2139b943f70bd17eb758690cbd5183acd552bc901d13c634da11eea404c

BuildRequires:  glib-devel
BuildRequires:  freetype2-devel
BuildRequires:  gobject-introspection-devel

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
%configure --with-gobject --enable-introspection
%make_build

%install
%make_install %{?_smp_mflags}

%if 0%{?with_check}
%check
make %{?_smp_mflags} check
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
%doc %{_datadir}/gtk-doc
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/cmake/harfbuzz/harfbuzz-config.cmake
%{_datadir}/gir-1.0/HarfBuzz-0.0.gir

%changelog
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
