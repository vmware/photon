Summary:        Module manipulating metadata files
Name:           libmodulemd
Version:        2.14.0
Release:        5%{?dist}
URL:            https://github.com/fedora-modularity/libmodulemd
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/fedora-modularity/libmodulemd/archive/%{name}-%{version}.tar.gz
%define sha512 %{name}-%{version}=8c48995aa6a9c6370a07a6887c7237614c502e335173dcba004037ffa41c8fbca8bdf36dfd59ba7d1d125dff6c8722ddc924e14173e3995e147c01a39c6f0ed1

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  meson
BuildRequires:  clang-devel
BuildRequires:  gcc
BuildRequires:  glib-devel
BuildRequires:  valgrind
BuildRequires:  python3-devel
BuildRequires:  python3-gobject-introspection
BuildRequires:  gobject-introspection-devel
BuildRequires:  python3-pygobject
BuildRequires:  python3-pycodestyle
BuildRequires:  python3-autopep8
BuildRequires:  gtk-doc
BuildRequires:  libyaml-devel
BuildRequires:  file-devel

Requires:       libyaml
Requires:       file-libs
Requires:       python3
Requires:       rpm-libs
Requires:       glib

%description
C Library for manipulating module metadata files

%package        devel
Summary:        Header and development files for libmodulemd
Requires:       libyaml-devel
Requires:       %{name} = %{version}-%{release}
Requires:       glib-devel

%description    devel
It contains the libraries and header files.

%prep
%autosetup -p1 -n %{name}-%{name}-%{version}

%build
%meson \
    -Dwith_py2=false \
    -Dwith_manpages=disabled \
    -Dwith_docs=false

%meson_build

%install
%meson_install

%ldconfig_scriptlets

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%doc README.md
%{_bindir}/modulemd-validator
%{_libdir}/girepository-1.0/Modulemd-2.0.typelib
%{_libdir}/libmodulemd.so.*
%{_datadir}/gir-1.0/Modulemd-2.0.gir
%{python3_sitelib}/*

%files devel
%defattr(-,root,root)
%{_libdir}/libmodulemd.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/modulemd-2.0/*.h

%changelog
* Wed Dec 11 2024 Mukul Sikka <mukul.sikka@broadcom.com> 2.14.0-5
- Release bump for SRP compliance
* Tue Nov 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.14.0-4
- Bump version as a part of rpm upgrade
* Tue Jan 03 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.14.0-3
- Bump version as a part of rpm upgrade
* Tue Dec 06 2022 Prashant S Chauhan <psinghchauha@vmware.com> 2.14.0-2
- Update release to compile with python 3.11
* Fri Oct 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.14.0-1
- Upgrade to v2.14.0
* Wed Sep 28 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.13.0-2
- Bump version as a part of clang upgrade
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
