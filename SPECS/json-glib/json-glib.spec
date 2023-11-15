Summary:        Library providing serialization and deserialization support for the JSON format
Name:           json-glib
Version:        1.4.4
Release:        3%{?dist}
License:        LGPLv2+
Group:          Development/Libraries
URL:            http://live.gnome.org/JsonGlib
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://ftp.gnome.org/pub/GNOME/sources/json-glib/1.4/%{name}-%{version}.tar.xz
%define sha512 %{name}=cf56a99dce3938b5c0075810f105719836fac65392da33a49b26ebf33aee1fab89ca9fac58059a2008d688ecc75a3e524de60621a5b027d566963541f38b971f

Patch0: use-meson-test-in-place-of-mesontest.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gobject-introspection-python
BuildRequires:  gobject-introspection-devel
BuildRequires:  glib-devel >= 2.58.3
BuildRequires:  libtool
BuildRequires:  which
BuildRequires:  meson
BuildRequires:  python3-devel
BuildRequires:  gtk-doc

Requires:   glib >= 2.58.3

Provides:   pkgconfig(json-glib-1.4)

%description
JSON-GLib is a library providing serialization and deserialization
support for the JavaScript Object Notation (JSON) format described by
RFC 4627.

%package devel
Summary:    Header files for the json-glib library
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Requires:   glib-devel
Requires:   gobject-introspection-devel

%description devel
Header files for the json-glib library.

%prep
%autosetup -p1 -n %{name}-%{version}

%build
%configure --enable-gtk-doc

%make_build

%install
%make_install %{?_smp_mflags}

%find_lang json-glib-1.0

%check
make %{?_smp_mflags} check

%clean
rm -rf %{buildroot}

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f json-glib-1.0.lang
%defattr(-, root, root)
%doc NEWS
%attr(755,root,root) %{_bindir}/json-glib-format
%attr(755,root,root) %{_bindir}/json-glib-validate

%ghost %{_libdir}/libjson-glib-1.0.so.?
%attr(755,root,root) %{_libdir}/libjson-glib-1.0.so.*.*.*

%files devel
%defattr(-, root, root)
%{_libdir}/libjson-glib-1.0.so
%{_includedir}/json-glib-1.0
%{_libdir}/pkgconfig/json-glib-1.0.pc
%{_datadir}/gir-1.0/Json-1.0.gir
%{_datadir}/gtk-doc
%{_libdir}/girepository-1.0/Json-1.0.typelib
%{_libexecdir}/installed-tests/*
%{_datadir}/installed-tests/*

%changelog
* Wed Nov 15 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 1.4.4-3
- Version bump due to glib change
* Tue Aug 09 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.4.4-2
- Fix meson test usages
* Fri Sep 21 2018 Ankit Jain <ankitja@vmware.com> 1.4.4-1
- Updated package to version 1.4.4
* Mon Apr 03 2017 Divya Thaluru <dthaluru@vmware.com> 1.2.8-1
- Updated package to version 1.2.8
* Thu Oct 06 2016 ChangLee <changlee@vmware.com> 1.0.4-3
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.4-2
- GA - Bump release of all rpms
* Thu Feb 25 2016 Anish Swaminathan <anishs@vmware.com>  1.0.4-1
- Upgrade to 1.0.4
* Mon Jul 6 2015 Alexey Makhalov <amakhalov@vmware.com> 1.0.2-3
- Added more requirements for devel subpackage.
* Fri Jun 26 2015 Alexey Makhalov <amakhalov@vmware.com> 1.0.2-2
- Added Provides:   pkgconfig(json-glib-1.0)
