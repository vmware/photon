%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           gobject-introspection
Summary:        Introspection system for GObject-based libraries
Version:        1.52.1
Release:        2%{?dist}
Group:          Development/Libraries
License:        GPLv2+, LGPLv2+, MIT
URL:            http://live.gnome.org/GObjectIntrospection
Source0:        http://ftp.gnome.org/pub/GNOME/sources/gobject-introspection/1.52/%{name}-%{version}.tar.xz
%define sha1 gobject-introspection=2a0c86bd23d27df0588b79404cfc5619ed6171e8
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  gettext
BuildRequires:  intltool
BuildRequires:  flex
BuildRequires:  bison
BuildRequires:  which
BuildRequires:  glib-devel
BuildRequires:  libffi-devel
BuildRequires:  go
Requires:       libffi
Requires:       glib >= 2.52.1
%description
GObject Introspection can scan C header and source files in order to
generate introspection "typelib" files.  It also provides an API to examine
typelib files, useful for creating language bindings among other
things.

%package        python
Summary:        Python package for handling GObject introspection data
Group:          Development/Languages
Requires:       %{name} = %{version}-%{release}
BuildRequires:  python2-devel
BuildRequires:  python2-libs
BuildRequires:  python-xml
Requires:       python2
%description    python
This package contains a Python package for handling the introspection
data from Python.

%package -n     python3-gobject-introspection
Summary:        Python3 package for handling GObject introspection data
Group:          Development/Languages
Requires:       %{name} = %{version}-%{release}
BuildRequires:  python3-devel
BuildRequires:  python3-libs
Requires:       python3
%description -n python3-gobject-introspection
This package contains a Python package for handling the introspection
data from Python.

%package devel
Summary:        Libraries and headers for gobject-introspection
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       libffi-devel
Requires:       glib-devel
Requires:       python2
Requires:       python2-devel
Requires:       python2-libs
Requires:       python-xml

%description devel
Libraries and headers for gobject-introspection.

%prep
%setup -q
rm -rf ../p3dir
cp -a . ../p3dir

%build
%configure --with-python=/usr/bin/python2
make %{?_smp_mflags}

pushd ../p3dir
%configure --with-python=/usr/bin/python3
make %{?_smp_mflags}
popd

%install
rm -rf %{buildroot}/*

make install DESTDIR=%{buildroot}

# Move the python modules to the correct location
mkdir -p %{buildroot}/%{python2_sitelib}
mv %{buildroot}/%{_libdir}/gobject-introspection/giscanner %{buildroot}/%{python2_sitelib}

pushd ../p3dir
make install DESTDIR=%{buildroot}
# Move the python3 modules to the correct location
mkdir -p %{buildroot}/%{python3_sitelib}
mv %{buildroot}/%{_libdir}/gobject-introspection/giscanner %{buildroot}/%{python3_sitelib}
popd
rm -rf $RPM_BUILD_ROOT/%{_datarootdir}/gtk-doc/html
find %{buildroot}%{_libdir} -name '*.la' -delete


%check
make  %{?_smp_mflags} check

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
%{python2_sitelib}/giscanner

%files -n python3-gobject-introspection
%defattr(-,root,root,-)
%{python3_sitelib}/giscanner

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
*   Tue May 23 2017 Xiaolin Li <xiaolinl@vmware.com> 1.52.1-2
-   Added python3 subpackage.
*   Wed Apr 12 2017 Danut Moraru <dmoraru@vmware.com> 1.52.1-1
-   Updated to version 1.52.1
*   Thu Oct 06 2016 ChangLee <changlee@vmware.com> 1.46.0-3
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.46.0-2
-   GA - Bump release of all rpms
*   Thu Feb 25 2016 Kumar Kaushik <kaushikk@vmware.com> 1.46.0-1
-   Updated version.
*   Mon Oct 12 2015 Xiaolin Li <xiaolinl@vmware.com> 1.43.3-4
-   Moving static lib files to devel package.
*   Fri Oct 9 2015 Xiaolin Li <xiaolinl@vmware.com> 1.43.3-3
-   Removing la files from packages.
*   Mon Jul 6 2015 Alexey Makhalov <amakhalov@vmware.com> 1.43.3-2
-   Added more requirements for devel subpackage.
