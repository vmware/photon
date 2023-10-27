Summary:        library for laying out and rendering of text.
Name:           pango
Version:        1.41.1
Release:        5%{?dist}
License:        LGPLv2 or MPLv1.1
URL:            http://pango.org
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://download.gnome.org/sources/pango/1.40/%{name}-%{version}.tar.xz
%define sha512 %{name}=bd88db59042b618d64fabcae616f59cc600554c6e9734d0f92d6fdf70cc1db8efa9909919477e0635be100491a7a8128deb4ae5c8165081eea3352f134ce963e

BuildRequires:  libX11-devel
BuildRequires:  libXext-devel
BuildRequires:  fribidi-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  glib-devel >= 2.68.4
BuildRequires:  cairo-devel
BuildRequires:  libpng-devel
BuildRequires:  fontconfig-devel
BuildRequires:  harfbuzz-devel

Requires:       glib >= 2.68.4
Requires:       cairo
Requires:       libpng
Requires:       fontconfig
Requires:       harfbuzz
Requires:       fribidi

%description
Pango is a library for laying out and rendering of text, with an emphasis on internationalization.
Pango can be used anywhere that text layout is needed, though most of the work on Pango so far has been done in the context of the GTK+ widget toolkit.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}
Requires:       glib-devel >= 2.68.4
Requires:       cairo-devel
Requires:       libpng-devel
Requires:       fontconfig-devel
Requires:       harfbuzz-devel
Requires:       fribidi-devel

%description    devel
It contains the libraries and header files to create applications

%prep
%autosetup -p1

%build
%configure --enable-introspection
%make_build

%install
%make_install %{?_smp_mflags}

%check
#These tests are known to fail. Hence sending exit 0
make %{?_smp_mflags} check

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so*
%{_datadir}/gir-1.0/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/girepository-1.0/
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gtk-doc/*
%{_datadir}/man/*

%changelog
* Sat Oct 07 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 1.41.1-5
- Bump version as part of glib upgrade
* Wed Jun 14 2023 Shivani Agarwal <shivania2@vmware.com> 1.41.1-4
- Bump version as a part of libX11 upgrade
* Wed Apr 19 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.41.1-3
- Bump version as a part of freetype2 upgrade
* Tue Feb 21 2023 Shivani Agarwal <shivania2@vmware.com> 1.41.1-2
- upgrade to build with new harfbuzz
* Thu Sep 08 2022 Shivani Agarwal <shivania2@vmware.com> 1.41.1-1
- Upgrade Version
* Thu Dec 16 2021 Alexey Makhalov <amakhalov@vmware.com> 1.40.4-2
- Fix pango -> fontconfig -> freetype2 dependency
- Clean up Requires and BuildRequires
* Tue Apr 04 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.40.4-1
- Initial version
