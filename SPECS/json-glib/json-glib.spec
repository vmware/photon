Summary:        Library providing serialization and deserialization support for the JSON format
Name:           json-glib
Version:        1.6.0
Release:        1%{?dist}
License:        LGPLv2+
Group:          Development/Libraries
Source0:        http://ftp.gnome.org/pub/GNOME/sources/json-glib/1.4/%{name}-%{version}.tar.xz
%define sha1    %{name}=7f0d55cc5b9644b2aaeb9995e85427ce545b15c2
URL:            http://live.gnome.org/JsonGlib
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  python3-gobject-introspection
BuildRequires:  gobject-introspection-devel
BuildRequires:  glib-devel
BuildRequires:  libtool
BuildRequires:  which
BuildRequires:	meson
BuildRequires:	python3
BuildRequires:	python3-libs
BuildRequires:  gtk-doc
Requires:	glib
Provides:	pkgconfig(json-glib-1.4)

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
%setup -q -n %{name}-%{version}

%build
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
meson build --prefix=/usr
ninja -C build

%install
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
DESTDIR=%{buildroot} ninja -C build install

%find_lang json-glib-1.0

%check
sed -i 's/mesontest/meson test/g' Makefile
make  %{?_smp_mflags} check

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f json-glib-1.0.lang
#%defattr(-, root, root)
%doc NEWS
%attr(755,root,root) %{_bindir}/json-glib-format
%attr(755,root,root) %{_bindir}/json-glib-validate
%ghost %{_libdir}/libjson-glib-1.0.so.?
%attr(755,root,root) %{_libdir}/libjson-glib-1.0.so.*.*.*

%files devel
#%defattr(-, root, root)
%{_libdir}/libjson-glib-1.0.so
%{_includedir}/json-glib-1.0
%{_libdir}/pkgconfig/json-glib-1.0.pc
%{_datadir}/gir-1.0/Json-1.0.gir
%{_libdir}/girepository-1.0/Json-1.0.typelib
%{_libexecdir}/installed-tests/*
%{_datadir}/installed-tests/*
%{_datadir}/gtk-doc/html/json-glib/*

%changelog
*   Fri Sep 25 2020 Gerrit Photon <photon-checkins@vmware.com> 1.6.0-1
-   Automatic Version Bump
*   Sun Aug 16 2020 Susant Sahani <ssahani@vmware.com> 1.4.4-3
-   Use meson and ninja build system
*   Mon Jun 22 2020 Tapas Kundu <tkundu@vmware.com> 1.4.4-2
-   Build with python3
-   Mass removal python2
*   Fri Sep 21 2018 Ankit Jain <ankitja@vmware.com> 1.4.4-1
-   Updated package to version 1.4.4
*   Mon Apr 03 2017 Divya Thaluru <dthaluru@vmware.com> 1.2.8-1
-   Updated package to version 1.2.8
*   Thu Oct 06 2016 ChangLee <changlee@vmware.com> 1.0.4-3
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.4-2
-   GA - Bump release of all rpms
*   Thu Feb 25 2016 Anish Swaminathan <anishs@vmware.com>  1.0.4-1
-   Upgrade to 1.0.4
*   Mon Jul 6 2015 Alexey Makhalov <amakhalov@vmware.com> 1.0.2-3
-   Added more requirements for devel subpackage.
*   Fri Jun 26 2015 Alexey Makhalov <amakhalov@vmware.com> 1.0.2-2
-   Added Provides:	pkgconfig(json-glib-1.0)
