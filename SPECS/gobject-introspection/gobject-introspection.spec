Name:           gobject-introspection
Summary:        Introspection system for GObject-based libraries
Version:        1.66.0
Release:        19%{?dist}
Group:          Development/Libraries
License:        GPLv2+, LGPLv2+, MIT
URL:            http://live.gnome.org/GObjectIntrospection
Source0:        http://ftp.gnome.org/pub/GNOME/sources/gobject-introspection/1.52/%{name}-%{version}.tar.xz
%define sha512  gobject-introspection=ff69514cc6b1dfbeafb488c1a3c1328cb222d4ab8c644e7f84c62cde8529b6e2dcf21c3a903684a837c5841f6ccf47eb179881eb1cba08cdc0ec7a352fafeee0
Vendor:         VMware, Inc.
Distribution:   Photon
Patch0:         avoid_doctemplates_hack.patch

BuildRequires:  gettext
BuildRequires:  intltool
BuildRequires:  flex
BuildRequires:  bison
BuildRequires:  which
BuildRequires:  glib-devel >= 2.58.0
BuildRequires:  libffi-devel
BuildRequires:  go
BuildRequires:  autoconf-archive
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-xml
BuildRequires:  meson

Requires:       libffi
Requires:       glib >= 2.58.0

%description
GObject Introspection can scan C header and source files in order to
generate introspection "typelib" files.  It also provides an API to examine
typelib files, useful for creating language bindings among other
things.

%package -n     python3-gobject-introspection
Summary:        Python3 package for handling GObject introspection data
Group:          Development/Languages
Requires:       %{name} = %{version}-%{release}
Requires:       python3-xml
Requires:       python3-libs
Requires:       python3
%description -n python3-gobject-introspection
This package contains a Python package for handling the introspection
data from Python.

%package devel
Summary:        Libraries and headers for gobject-introspection
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       python3-gobject-introspection = %{version}-%{release}
Requires:       libffi-devel
Requires:       glib-devel

%description devel
Libraries and headers for gobject-introspection.

%prep
%autosetup -p1

%build
meson --prefix=/usr --libdir=lib -Dpython=%{__python3} build
ninja -C build

%install
DESTDIR=%{buildroot} ninja -C build install
# Move the python3 modules to the correct location
mkdir -p %{buildroot}/%{python3_sitelib}
mv %{buildroot}%{_libdir}/gobject-introspection/giscanner %{buildroot}/%{python3_sitelib}
rm -rf %{buildroot}/%{_datarootdir}/gtk-doc/html
find %{buildroot}%{_libdir} -name '*.la' -delete

%check
meson test

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/lib*.so.*
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/*.typelib

%files -n python3-gobject-introspection
%defattr(-,root,root,-)
%{python3_sitelib}/giscanner

%files devel
%defattr(-,root,root,-)
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_bindir}/g-ir-*
%{_datadir}/gir-1.0
%{_datadir}/aclocal/introspection.m4
%{_datadir}/gobject-introspection-1.0
%doc %{_mandir}/man1/*.gz

%changelog
* Thu Mar 16 2023 Piyush Gupta <gpiyush@vmware.com> 1.66.0-19
- Bump up version to compile with new go
* Tue Jan 17 2023 Shivani Agarwal <shivania2@vmware.com> 1.66.0-18
- Add patch to build with new meson
* Tue Dec 20 2022 Piyush Gupta <gpiyush@vmware.com> 1.66.0-17
- Bump up version to compile with new go
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 1.66.0-16
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 1.66.0-15
- Bump up version to compile with new go
* Thu Sep 15 2022 Piyush Gupta <gpiyush@vmware.com> 1.66.0-14
- Bump up version to compile with new go
* Fri Aug 19 2022 Piyush Gupta <gpiyush@vmware.com> 1.66.0-13
- Bump up version to compile with new go
* Tue Jul 12 2022 Piyush Gupta <gpiyush@vmware.com> 1.66.0-12
- Bump up version to compile with new go
* Sat May 07 2022 Piyush Gupta <gpiyush@vmware.com> 1.66.0-11
- Bump up version to compile with new go
* Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 1.66.0-10
- Bump up version to compile with new go
* Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 1.66.0-9
- Bump up version to compile with new go
* Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 1.66.0-8
- Bump up to compile with python 3.10
* Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 1.66.0-7
- Bump up version to compile with new go
* Tue Oct 05 2021 Piyush Gupta <gpiyush@vmware.com> 1.66.0-6
- Bump up version to compile with new go
* Fri Jun 11 2021 Piyush Gupta <gpiyush@vmware.com> 1.66.0-5
- Bump up version to compile with new go
* Thu Mar 25 2021 Piyush Gupta<gpiyush@vmware.com> 1.66.0-4
- Bump up version to compile with new go
* Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 1.66.0-3
- Bump up version to compile with new go
* Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 1.66.0-2
- Bump up version to compile with new go
* Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 1.66.0-1
- Automatic Version Bump
* Sun Aug 30 2020 Gerrit Photon <photon-checkins@vmware.com> 1.64.1-1
- Automatic Version Bump
* Thu Aug 13 2020 Ankit Jain <ankitja@vmware.com> 1.58.0-4
- Requires python3-libs
* Mon Jun 22 2020 Tapas Kundu <tkundu@vmware.com> 1.58.0-3
- Mass removal python2
* Mon Dec 10 2018 Alexey Makhalov <amakhalov@vmware.com> 1.58.0-2
- -devel requires -python.
* Thu Sep 06 2018 Anish Swaminathan <anishs@vmware.com> 1.58.0-1
- Update version to 1.58.0
* Tue Jan 02 2018 Alexey Makhalov <amakhalov@vmware.com> 1.52.1-5
- Add autoreconf to support automake-1.15.1
* Mon Aug 28 2017 Kumar Kaushik <kaushikk@vmware.com> 1.52.1-4
- Disabling make check for Regress-1.0.gir test, bug#1635886
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 1.52.1-3
- Add python3-xml to python3 sub package Buildrequires.
* Tue May 23 2017 Xiaolin Li <xiaolinl@vmware.com> 1.52.1-2
- Added python3 subpackage.
* Wed Apr 12 2017 Danut Moraru <dmoraru@vmware.com> 1.52.1-1
- Updated to version 1.52.1
* Thu Oct 06 2016 ChangLee <changlee@vmware.com> 1.46.0-3
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.46.0-2
- GA - Bump release of all rpms
* Thu Feb 25 2016 Kumar Kaushik <kaushikk@vmware.com> 1.46.0-1
- Updated version.
* Mon Oct 12 2015 Xiaolin Li <xiaolinl@vmware.com> 1.43.3-4
- Moving static lib files to devel package.
* Fri Oct 9 2015 Xiaolin Li <xiaolinl@vmware.com> 1.43.3-3
- Removing la files from packages.
* Mon Jul 6 2015 Alexey Makhalov <amakhalov@vmware.com> 1.43.3-2
- Added more requirements for devel subpackage.
