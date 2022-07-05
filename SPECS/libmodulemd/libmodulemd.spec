Summary:        Module manipulating metadata files
Name:           libmodulemd
Version:        2.13.0
Release:        1%{?dist}
License:        MIT
URL:            https://github.com/fedora-modularity/libmodulemd
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/fedora-modularity/libmodulemd/archive/%{name}-%{version}.tar.xz
%define sha1    %{name}-%{version}=e83886f374922ecf6fa728c6c588d697d0748b99

BuildRequires:  meson
BuildRequires:  clang-devel
BuildRequires:  gcc
BuildRequires:  glib-devel
BuildRequires:  valgrind
BuildRequires:  python3-devel
BuildRequires:  python3
BuildRequires:  python3-gobject-introspection
BuildRequires:  gobject-introspection-devel
BuildRequires:  python3-pygobject
BuildRequires:  python3-pycodestyle
BuildRequires:  python3-autopep8
BuildRequires:  python3-macros
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
%autosetup -p1 -n modulemd-%{version}

%build
%meson -Dwith_py2=false \
      -Dwith_manpages=disabled \
      -Dwith_docs=false

%meson_build

%install
%meson_install

%ldconfig_scriptlets

%files
%doc README.md
%{_bindir}/modulemd-validator
%{_libdir}/girepository-1.0/Modulemd-2.0.typelib
%{_libdir}/libmodulemd.so.*
%{_datadir}/gir-1.0/Modulemd-2.0.gir
%{python3_sitelib}/*

%files  devel
%{_libdir}/libmodulemd.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/modulemd-2.0/*.h

%changelog
* Mon Aug 02 2021 Susant Sahani <ssahani@vmware.com> 2.13.0-1
- Use autosetup, ldconfig scriptlets, switch to meson
- and version bump
* Sat Dec 12 2020 Shreenidhi Shedi <sshedi@vmware.com> 2.11.0-1
- Upgrade to v2.11.0
* Thu Aug 13 2020 Ankit Jain <ankitja@vmware.com> 2.9.4-1
- Updated to 2.9.4
* Thu Oct 24 2019 Ankit Jain <ankitja@vmware.com> 2.4.0-2
- Added for ARM Build
* Wed May 15 2019 Ankit Jain <ankitja@vmware.com> 2.4.0-1
- Initial build. First version
