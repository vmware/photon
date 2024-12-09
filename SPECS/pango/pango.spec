Summary:        library for laying out and rendering of text.
Name:           pango
Version:        1.50.11
Release:        6%{?dist}
URL:            http://pango.org
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://gitlab.gnome.org/GNOME/pango/-/archive/%{version}/%{name}-%{version}.tar.gz
%define sha512 %{name}=695b6d11dcb72918f699ea6441d67f4f9a9fa930131c6079b0aa689ee6910903a79cd308c5054fd3ccdd8efd390b3b56f1d0cbf27eaef7247315db2fe9710b7a

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  glib-devel
BuildRequires:  cairo-devel
BuildRequires:  fontconfig-devel
BuildRequires:  harfbuzz-devel
BuildRequires:  freetype2-devel
BuildRequires:  meson
BuildRequires:  pkg-config
BuildRequires:  fribidi-devel
BuildRequires:  cmake
BuildRequires:  libX11-devel
BuildRequires:  libXext-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  libpng-devel

Requires:       freetype2
Requires:       fontconfig
Requires:       fribidi
Requires:       glib
Requires:       harfbuzz
Requires:       libpng

%description
Pango is a library for laying out and rendering of text, with an emphasis on internationalization.
Pango can be used anywhere that text layout is needed, though most of the work on Pango so far has been done in the context of the GTK+ widget toolkit.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}
Requires:       harfbuzz-devel
Requires:       glib-devel
Requires:       cairo-devel
Requires:       libpng-devel
Requires:       fontconfig-devel
Requires:       fribidi-devel

%description    devel
It contains the libraries and header files to create applications

%prep
%autosetup -p1

%build
%meson \
    -Dlibthai=disabled \
    -Dxft=disabled \
    -Dintrospection=enabled

%meson_build

%install
%meson_install

%if 0%{?with_check}
%check
%meson_test
%endif

%ldconfig_scriptlets

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so.*
%{_datadir}/gir-1.0/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/girepository-1.0/
%{_libdir}/pkgconfig/*.pc

%changelog
* Wed Dec 11 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.50.11-6
- Release bump for SRP compliance
* Wed Jun 14 2023 Shivani Agarwal <shivania2@vmware.com> 1.50.11-5
- Bump version as a part of libX11 upgrade
* Wed Apr 19 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.50.11-4
- Bump version as a part of freetype2 upgrade
* Tue Dec 13 2022 Guruswamy Basavaiah <bguruswamy@vmware.com> 1.50.11-3
- Bump release as a part of libpng upgrade
* Wed Nov 30 2022 Shivani Agarwal <shivania2@vmware.com> 1.50.11-2
- Enabled introspection
* Sun Nov 13 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.50.11-1
- Upgrade to v1.50.11
* Tue Apr 04 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.40.4-1
- Initial version
