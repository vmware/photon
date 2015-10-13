%{!?python_sitelib: %define python_sitelib %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:       	gobject-introspection
Summary:    	Introspection system for GObject-based libraries
Version:    	1.43.3
Release:    	4%{?dist}
Group:      	Development/Libraries
License:    	GPLv2+, LGPLv2+, MIT
URL:        	http://live.gnome.org/GObjectIntrospection
Source0:    	%{name}-%{version}.tar.xz
%define sha1 gobject-introspection=eb4db77dfb7bf26e25dbfc8d03eb38be7adfb7cc
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires:  gettext
BuildRequires:  intltool
BuildRequires:  flex
BuildRequires:  bison
BuildRequires:  glib-devel
BuildRequires:  libffi
BuildRequires:	go
Requires:	libffi
Requires:	glib
%description
GObject Introspection can scan C header and source files in order to
generate introspection "typelib" files.  It also provides an API to examine
typelib files, useful for creating language bindings among other
things.

%package python
Summary:    Python package for handling GObject introspection data
Group:      Development/Languages
Requires:   gobject-introspection
BuildRequires:	python2-devel
BuildRequires:	python2-libs
Requires:	python2
%description python
This package contains a Python package for handling the introspection
data from Python.

%package devel
Summary:    Libraries and headers for gobject-introspection
Group:      Development/Libraries
Requires:   gobject-introspection
Requires:   glib-devel
Requires:   python2
Requires:   python2-devel
Requires:   python2-libs

%description devel
Libraries and headers for gobject-introspection.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT/*

make install DESTDIR=$RPM_BUILD_ROOT

# Move the python modules to the correct location
mkdir -p $RPM_BUILD_ROOT/%{python_sitelib}
mv $RPM_BUILD_ROOT/%{_libdir}/gobject-introspection/giscanner $RPM_BUILD_ROOT/%{python_sitelib}

rm -rf $RPM_BUILD_ROOT/%{_datarootdir}/gtk-doc/html
find %{buildroot}%{_libdir} -name '*.la' -delete

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/lib*.so.*
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/*.typelib

%files python
%defattr(-,root,root,-)
%{python_sitelib}/giscanner

%files devel
%defattr(-,root,root,-)
%{_libdir}/lib*.so
%{_libdir}/lib*.a
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_bindir}/g-ir-*
%{_datadir}/gir-1.0
%{_datadir}/aclocal/introspection.m4
%{_datadir}/gobject-introspection-1.0
%doc %{_mandir}/man1/*.gz

%changelog
*   Mon Oct 12 2015 Xiaolin Li <xiaolinl@vmware.com> 1.43.3-4
-   Moving static lib files to devel package.
*   Fri Oct 9 2015 Xiaolin Li <xiaolinl@vmware.com> 1.43.3-3
-   Removing la files from packages.
*	Mon Jul 6 2015 Alexey Makhalov <amakhalov@vmware.com> 1.43.3-2
-	Added more requirements for devel subpackage.
