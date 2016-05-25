%{!?python_sitelib: %define python_sitelib %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           pygobject
Version:        3.10.2
Release:	2%{?dist}
Summary:        Python Bindings for GObject
Group:          Development/Languages
License:        LGPLv2+
Vendor:		VMware, Inc.
Distribution:	Photon
URL:            ftp://ftp.gnome.org
Source0:        ftp://ftp.gnome.org/pub/GNOME/sources/pygobject/3.10/pygobject-3.10.2.tar.xz
%define sha1 pygobject=693cc1cb692a8f21ff27d28eaa780f5e67cafb1a
Requires:	python2
Requires:	gobject-introspection
Requires:	glib-devel
Provides:	pygobject
BuildRequires: 	python2-devel
BuildRequires: 	python2-libs
BuildRequires: 	gobject-introspection-devel
BuildRequires: 	glib-devel

%description
Python bindings for GLib and GObject.

%prep
%setup -q -n pygobject-%{version}

%build
./configure --prefix=/usr --disable-cairo --without-cairo
make

%install
make install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/*.so.*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/python*/*
%{_includedir}/*

%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com>         3.10.2-2
-	GA - Bump release of all rpms
*	Sat Jan 24 2015 Touseef Liaqat <tliaqat@vmware.com> 7.19.5.1
-	Initial build.	First version
