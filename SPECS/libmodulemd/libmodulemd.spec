%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib    ;print(get_python_lib())")}

Summary:        Module manipulating metadata files
Name:           libmodulemd
Version:        2.9.4
Release:        1%{?dist}
License:        MIT
URL:            https://github.com/fedora-modularity/libmodulemd
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/fedora-modularity/libmodulemd/archive/%{name}-%{version}.tar.gz
%define sha1    %{name}-%{version}=b2070336eddf5ce26250c90e824ae5c4bdf4733e
BuildRequires:  meson
BuildRequires:  clang-devel
BuildRequires:  gcc
BuildRequires:  glib-devel
BuildRequires:  glib-doc
BuildRequires:  valgrind
BuildRequires:  gobject-introspection-devel
BuildRequires:  python3-pygobject
BuildRequires:  python3-pycodestyle
BuildRequires:  python3-autopep8
BuildRequires:  gtk-doc
BuildRequires:  libyaml-devel
BuildRequires:  file-devel
Requires:       libyaml

%description
C Library for manipulating module metadata files

%package        devel
Summary:        Header and development files for libmodulemd
Requires:       libyaml-devel
Requires:       %{name} = %{version}-%{release}
%description    devel
It contains the libraries and header files.

%prep
%setup -q -n %{name}-%{name}-%{version}

%build
meson -Dprefix=%{_prefix} -Ddeveloper_build=false -Dwith_py2=false \
      -Dwith_manpages=disabled api1
cd api1
ninja

%install
cd api1
DESTDIR=%{buildroot}/ ninja install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc README.md
%{_bindir}/modulemd-validator
%{_libdir}/girepository-1.0/Modulemd-2.0.typelib
%{_libdir}/libmodulemd.so.*
%{_datadir}/gir-1.0/Modulemd-2.0.gir
%{_datadir}/gtk-doc/html/modulemd-2.0/*
%{python3_sitelib}/*

%files  devel
%{_libdir}/libmodulemd.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/modulemd-2.0/*.h

%changelog
*   Thu Aug 13 2020 Ankit Jain <ankitja@vmware.com> 2.9.4-1
-   Updated to 2.9.4
*   Thu Oct 24 2019 Ankit Jain <ankitja@vmware.com> 2.4.0-2
-   Added for ARM Build
*   Wed May 15 2019 Ankit Jain <ankitja@vmware.com> 2.4.0-1
-   Initial build. First version
