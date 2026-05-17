%global build_if %{photon_subrelease} >= 91

%define disable_introspection 0

Summary:        Library providing serialization and deserialization support for the JSON format
Name:           json-glib
Version:        1.10.8
Release:        3%{?dist}
Group:          Development/Libraries
URL:            http://live.gnome.org/JsonGlib
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://download.gnome.org/sources/json-glib/1.10/%{name}-%{version}.tar.xz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  python3-gobject-introspection
BuildRequires:  gobject-introspection-devel
BuildRequires:  glib-devel
BuildRequires:  libtool
BuildRequires:  which
BuildRequires:  meson
BuildRequires:  cmake
BuildRequires:  python3
BuildRequires:  gtk-doc

Requires:       glib

Provides:       pkgconfig(json-glib-1.4)

%description
JSON-GLib is a library providing serialization and deserialization
support for the JavaScript Object Notation (JSON) format described by
RFC 4627.

%package        devel
Summary:        Header files for the json-glib library
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       glib-devel
Requires:       gobject-introspection-devel

%description    devel
Header files for the json-glib library.

%prep
%autosetup -p1 -n %{name}-%{version}

%build
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

CONFIGURE_OPTS=(-Dgtk_doc=disabled)
%if 0%{?disable_introspection}
CONFIGURE_OPTS+=(-Dintrospection=disabled)
%else
CONFIGURE_OPTS+=(-Dintrospection=enabled)
%endif

%meson "${CONFIGURE_OPTS[@]}"

%meson_build

%install
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
%meson_install

%find_lang json-glib-1.0

%check
sed -i 's/mesontest/meson test/g' Makefile
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

%if 0%{?disable_introspection} == 0
%{_datadir}/gir-1.0/Json-1.0.gir
%{_libdir}/girepository-1.0/Json-1.0.typelib
%endif

%{_libexecdir}/installed-tests/*
%{_datadir}/installed-tests/*

%changelog
* Tue May 19 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 1.10.8-3
- Enable for 91 subrlease
* Sat May 16 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.10.8-2
- Bump to keep version higher than 91
* Fri Apr 10 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.10.8-1
- Upgrade to v1.10.8
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.6.6-6
- Bump version as a part of python3.14 upgrade
* Fri Aug 08 2025 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 1.6.6-5
- Remove not required docuementation
* Wed Jan 22 2025 Tapas Kundu <tapas.kundu@broadcom.com> 1.6.6-4
- Bump version as a part of meson upgrade
* Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 1.6.6-3
- Release bump for SRP compliance
* Tue Dec 06 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.6.6-2
- Update release to compile with python 3.11
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 1.6.6-1
- Automatic Version Bump
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 1.6.2-1
- Automatic Version Bump
* Fri Sep 25 2020 Gerrit Photon <photon-checkins@vmware.com> 1.6.0-1
- Automatic Version Bump
* Sun Aug 16 2020 Susant Sahani <ssahani@vmware.com> 1.4.4-3
- Use meson and ninja build system
* Mon Jun 22 2020 Tapas Kundu <tkundu@vmware.com> 1.4.4-2
- Build with python3
- Mass removal python2
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
- Added Provides:pkgconfig(json-glib-1.0)
