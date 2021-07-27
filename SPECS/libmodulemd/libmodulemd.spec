%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib    ;print(get_python_lib())")}

Summary:        Module manipulating metadata files
Name:           libmodulemd
Version:        2.4.0
Release:        3%{?dist}
License:        MIT
URL:            https://github.com/fedora-modularity/libmodulemd
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/fedora-modularity/libmodulemd/archive/%{name}-%{version}.tar.gz
%define sha1    %{name}-%{version}=b832bdd33e80901f2fa7946ebafdec3ee8e4853f
BuildRequires:  meson
BuildRequires:  clang-devel
BuildRequires:  gcc
BuildRequires:  glib
BuildRequires:  valgrind
BuildRequires:  gobject-introspection-devel
BuildRequires:  python3-pygobject
BuildRequires:  python3-pycodestyle
BuildRequires:  python3-autopep8
BuildRequires:  gtk-doc
BuildRequires:  libyaml-devel
Requires:       libyaml
Requires:       clang

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
meson -Dprefix=%{_prefix} -Ddeveloper_build=false -Dbuild_api_v1=true -Dbuild_api_v2=false \
       -Dwith_py3_overrides=true -Dwith_py2_overrides=false api1
cd api1
ninja

%install
cd api1
DESTDIR=%{buildroot}/ ninja install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc README.md
%{_bindir}/modulemd-validator-v1
%{_libdir}/girepository-1.0/Modulemd-1.0.typelib
%{_libdir}/libmodulemd.so.*
%{_datadir}/gir-1.0/Modulemd-1.0.gir
%{_datadir}/gtk-doc/html/modulemd-1.0/*
%{python3_sitelib}/*

%files  devel
%{_libdir}/libmodulemd.so
%{_libdir}/pkgconfig/modulemd.pc
%{_includedir}/modulemd/*

%changelog
*   Tue Jul 27 2021 Tapas Kundu <tkundu@vmware.com> 2.4.0-3
-   Rebuild with updated clang
*   Thu Oct 24 2019 Ankit Jain <ankitja@vmware.com> 2.4.0-2
-   Added for ARM Build
*   Wed May 15 2019 Ankit Jain <ankitja@vmware.com> 2.4.0-1
-   Initial build. First version
