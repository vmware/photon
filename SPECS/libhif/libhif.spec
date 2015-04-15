# Copied from inside of libhif.<version>.tar.gz

Summary:   	Simple package manager built on top of hawkey and librepo
Name:      	libhif
Version:   	0.1.7
Release:   	1
License:   	LGPLv2+
URL:       	https://github.com/hughsie/libhif
Source0:   	http://people.freedesktop.org/~hughsient/releases/libhif-%{version}.tar.gz
Vendor:		VMware, Inc.
Distribution:	Photon

Requires: 	librepo
Requires: 	libsolv
Requires: 	gobject-introspection
Requires: 	hawkey
Requires: 	glib >= 2.16.1

BuildRequires: 	glib-devel >= 2.16.1
BuildRequires: 	libtool
BuildRequires: 	gtk-doc
BuildRequires: 	gobject-introspection-devel
BuildRequires: 	hawkey-devel >= 0.4.6
BuildRequires: 	rpm-devel >= 4.11.0
BuildRequires: 	librepo
BuildRequires: 	libsolv
BuildRequires: 	popt-devel
BuildRequires: 	python2-libs
BuildRequires:	python2
BuildRequires: 	gobject-introspection-python

%description
This library provides a simple interface to hawkey and librepo and is currently
used by PackageKit and rpm-ostree.

%package devel
Summary: GLib Libraries and headers for libhif
Requires: libhif

%description devel
GLib headers and libraries for libhif.

%prep
%setup -q -n libhif-%{version}

%build

./autogen.sh \
    LDFLAGS='-L/usr/lib -lrpm -lrepo' \
        --enable-gtk-doc \
        --disable-static \
        --disable-silent-rules \
        --disable-dependency-tracking \

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
cp -rf $RPM_BUILD_ROOT/usr/local/* $RPM_BUILD_ROOT/usr/
rm -rf $RPM_BUILD_ROOT/usr/local/*
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

