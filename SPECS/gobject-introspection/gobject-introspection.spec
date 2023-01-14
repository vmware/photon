Name:           gobject-introspection
Summary:        Introspection system for GObject-based libraries
Version:        1.74.0
Release:        5%{?dist}
Group:          Development/Libraries
License:        GPLv2+, LGPLv2+, MIT
URL:            http://live.gnome.org/GObjectIntrospection
Distribution:   Photon
Vendor:         VMware, Inc.

Source0: https://gitlab.gnome.org/GNOME/gobject-introspection/-/archive/%{version}/%{name}-%{version}.tar.xz
%define sha512 %{name}=decff5dda0ec5ec0afda4d6bcd3bdadcbf34289002c0d9c0c77ecf8c5d3f15d196b24d8035041545031006acbdfe76af47c42da061c40e200c87f2c74cd301f0

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
BuildRequires:  python3-xml
BuildRequires:  meson
BuildRequires:  cmake

Requires:       libffi
Requires:       glib >= 2.58.0

%description
GObject Introspection can scan C header and source files in order to
generate introspection "typelib" files.  It also provides an API to examine
typelib files, useful for creating language bindings among other
things.

%package -n     python3-%{name}
Summary:        Python3 package for handling GObject introspection data
Group:          Development/Languages
Requires:       %{name} = %{version}-%{release}
Requires:       python3-xml
Requires:       python3

%description -n python3-%{name}
This package contains a Python package for handling the introspection
data from Python.

%package        devel
Summary:        Libraries and headers for gobject-introspection
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       python3-%{name} = %{version}-%{release}
Requires:       libffi-devel
Requires:       glib-devel

%description devel
Libraries and headers for gobject-introspection.

%prep
%autosetup -p1

%build
%{meson} \
    -Dpython=%{python3} \
    -Dcairo=disabled \
    -Ddoctool=disabled

%{meson_build}

%install
%{meson_install}
# Move the python3 modules to the correct location
mkdir -p %{buildroot}%{python3_sitelib}
mv %{buildroot}%{_libdir}/%{name}/giscanner %{buildroot}%{python3_sitelib}
rm -rf %{buildroot}%{_datarootdir}/gtk-doc/html

%check
%if 0%{?with_check}
%{meson_test}
%endif

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/lib*.so.*
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/*.typelib

%files -n python3-%{name}
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
%{_datadir}/%{name}-1.0
%doc %{_mandir}/man1/*.gz

%changelog
* Sat Jan 14 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.74.0-5
- Bump version as a part of gettext upgrade
* Tue Dec 06 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.74.0-4
- Update release to compile with python 3.11
* Mon Nov 21 2022 Piyush Gupta <gpiyush@vmware.com> 1.74.0-3
- Bump up version to compile with new go
* Sun Nov 13 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.74.0-2
- Bump version as a part of autoconf-archive upgrade
* Tue Nov 01 2022 Susant Sahani <ssahani@vmware.com> 1.74.0-1
- Bump up version
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 1.68.0-5
- Bump up version to compile with new go
* Fri Jun 17 2022 Piyush Gupta <gpiyush@vmware.com> 1.68.0-4
- Bump up version to compile with new go
* Tue May 10 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.68.0-3
- Bump version as a part of libffi upgrade
* Fri Jun 11 2021 Piyush Gupta<gpiyush@vmware.com> 1.68.0-2
- Bump up version to compile with new go
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 1.68.0-1
- Automatic Version Bump
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
