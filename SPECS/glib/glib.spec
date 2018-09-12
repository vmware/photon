Summary:	Low-level libraries useful for providing data structure handling for C.
Name:		glib
Version:	2.58.0
Release:	1%{?dist}
License:	LGPLv2+
URL:		https://developer.gnome.org/glib/
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://ftp.gnome.org/pub/gnome/sources/glib/2.58/%{name}-%{version}.tar.xz
%define sha1 glib=c00e433c56e0ba3541abc5222aeca4136de10fb8
BuildRequires:	pcre-devel
BuildRequires:	libffi-devel
BuildRequires:	pkg-config
BuildRequires:	cmake
BuildRequires:	which
BuildRequires:	python-xml
Requires:	pcre-libs
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
Requires:	glib = %{version}-%{release}
BuildRequires:	python2 >= 2.7
BuildRequires:	python2-libs >= 2.7
Requires:	pcre-devel
Requires:	python2
Requires:	libffi-devel

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
./autogen.sh
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
*   Tue Sep 11 2018 Anish Swaminathan <anishs@vmware.com> 2.58.0-1
-   Update version to 2.58.0
*   Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> 2.52.1-2
-   Requires pcre-libs, BuildRequires libffi-devel.
*   Wed Apr 12 2017 Danut Moraru <dmoraru@vmware.com> 2.52.1-1
-   Updated to version 2.52.1-1
*   Thu Oct 06 2016 ChangLee <changlee@vmware.com> 2.48.2-2
-   Modified %check
*   Tue Sep 06 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.48.2-1
-   Updated to version 2.48.2-1
*   Thu Aug 11 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.47.6-3
-   Update glib require for devel to use the same version and release
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.47.6-2
-   GA - Bump release of all rpms
*   Thu Apr 14 2016	Harish Udaiya Kumar<hudaiyakumar@vmware.com> 2.47.6-1
    Updated to version 2.47.6
*   Thu Jan 14 2016 Xiaolin Li <xiaolinl@vmware.com> 2.46.2-1
-   Updated to version 2.46.2
*   Fri Jun 12 2015 Alexey Makhalov <amakhalov@vmware.com> 2.42.0-3
-   Added glib-schemas package
*   Thu Jun 11 2015 Alexey Makhalov <amakhalov@vmware.com> 2.42.0-2
-   Added more 'Provides: pkgconfig(...)' for base package
*   Thu Nov 06 2014 Sharath George <sharathg@vmware.com> 2.42.0-1
-   Initial version
