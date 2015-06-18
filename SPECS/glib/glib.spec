Summary:	Low-level libraries useful for providing data structure handling for C.
Name:		glib
Version:	2.42.0
Release:	3%{?dist}
License:	LGPLv2+
URL:		http://ftp.gnome.org/pub/gnome/sources/glib/2.42/glib-2.42.0.tar.xz
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://ftp.gnome.org/pub/gnome/sources/glib/2.42/%{name}-%{version}.tar.xz
BuildRequires:	pcre-devel
BuildRequires:	libffi
BuildRequires:	pkg-config
BuildRequires:	cmake
Requires:	pcre
Requires:	libffi
Provides:	pkgconfig(glib-2.0)
Provides:	pkgconfig(gmodule-2.0)
Provides:	pkgconfig(gmodule-no-export-2.0)
Provides:	pkgconfig(gobject-2.0)
Provides:	pkgconfig(gio-2.0)
Provides:	pkgconfig(gio-unix-2.0)
Provides:	pkgconfig(gthread-2.0)
%description
The GLib package contains a low-level libraries useful for providing data structure handling for C, portability wrappers and interfaces for such runtime functionality as an event loop, threads, dynamic loading and an object system. Development libs and headers are in glib-devel.

%package devel
Summary:	Header files for the glib library
Group:		Development/Libraries
Requires:	glib glib-schemas
Provides:	glib-devel
Provides:	glib-devel(x86-64)
BuildRequires:	python2 >= 2.7
BuildRequires:	python2-libs >= 2.7
Requires:	pcre-devel
Requires:	python2

%description devel
Static libraries and header files for the support library for the glib library

%package schemas
Summary:	gsettings schemas compiling tool
Group:		Development/Libraries
Requires:	glib

%description schemas
Gsettings schemas compiling tool

%prep
%setup -q
%build
./configure --prefix=/usr --with-pcre=system 
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files 
%defattr(-,root,root)
%{_libdir}/libglib-*.so.*
%{_libdir}/libgthread-*.so.*
%{_libdir}/libgmodule-*.so.*
%{_libdir}/libgio-*.so.*
%{_libdir}/libgobject-*.so.*

%files devel
%defattr(-, root, root)
%{_bindir}/*
%{_libdir}/*.so
%{_libdir}/*.la
%{_libdir}/pkgconfig/*
%{_libdir}/gio/*
%{_libdir}/glib-*/*
%{_includedir}/*
%{_datadir}/*
%exclude %{_bindir}/glib-compile-schemas
%exclude %{_bindir}/gsettings
%exclude %{_datadir}/glib-2.0/schemas/*

%files schemas
%defattr(-, root, root)
%{_bindir}/glib-compile-schemas
%{_bindir}/gsettings
%{_datadir}/glib-2.0/schemas/*

%changelog
*	Fri Jun 12 2015 Alexey Makhalov <amakhalov@vmware.com> 2.42.0-3
-	Added glib-schemas package
*	Thu Jun 11 2015 Alexey Makhalov <amakhalov@vmware.com> 2.42.0-2
-	Added more 'Provides: pkgconfig(...)' for base package
*	Thu Nov 06 2014 Sharath George <sharathg@vmware.com> 2.42.0-1
	Initial version
