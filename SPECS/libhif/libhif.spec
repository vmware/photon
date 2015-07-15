# Copied from inside of libhif.<version>.tar.gz
%define libhif_version %{name}-%{name}_0_2_0

Summary:   	Simple package manager built on top of hawkey and librepo
Name:		libhif
Version:   	0.2.0
Release:   	1%{?dist}
License:   	LGPLv2+
URL:       	https://github.com/hughsie/libhif
Source0:   	http://people.freedesktop.org/~hughsient/releases/%{name}-%{version}.tar.gz
%define sha1 libhif=7de667ee0a26f448c5a0c9f56dc5c304d7c282aa
Vendor:		VMware, Inc.
Distribution:	Photon

BuildRequires: 	glib-devel >= 2.16.1
BuildRequires: 	libtool
BuildRequires: 	gtk-doc
BuildRequires: 	gobject-introspection-devel
BuildRequires: 	hawkey-devel >= 0.4.6
BuildRequires: 	rpm-devel >= 4.11.0
BuildRequires: 	librepo-devel >= 1.7.11
BuildRequires: 	libsolv
BuildRequires: 	popt-devel
BuildRequires: 	python2-libs
BuildRequires:	python2
BuildRequires: 	gobject-introspection-python
BuildRequires:	openssl-devel

Requires:       openssl
Requires:       librepo-devel
Requires: 	libsolv
Requires: 	gobject-introspection
Requires: 	hawkey-devel
Requires: 	rpm-devel
Requires: 	glib >= 2.16.1

%description
This library provides a simple interface to hawkey and librepo and is currently
used by PackageKit and rpm-ostree.

%package devel
Summary: GLib Libraries and headers for libhif
Requires: libhif
Provides: pkgconfig(libhif)

%description devel
GLib headers and libraries for libhif.

%prep
%setup -q -n %{libhif_version}

%build

./autogen.sh --prefix=/usr \
    LDFLAGS='-L/usr/lib -lrpm -lrepo' \
        --enable-gtk-doc \
        --disable-static \
        --disable-silent-rules \
        --disable-dependency-tracking \

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/libhif*.la

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc README.md AUTHORS NEWS COPYING
%{_libdir}/libhif.so.1*
%{_libdir}/girepository-1.0/*.typelib

%files devel
%{_libdir}/libhif.so
%{_libdir}/pkgconfig/libhif.pc
%dir %{_includedir}/libhif
%{_includedir}/libhif/*.h
%{_datadir}/gtk-doc
%{_datadir}/gir-1.0/*.gir

%changelog
*       Wed Jun 17 2015 Anish Swaminathan <anishs@vmware.com> 0.2.0-1
-       Updated version
