Summary:        Module manipulating metadata files
Name:           libmodulemd
Version:        2.4.0
Release:        5%{?dist}
License:        MIT
URL:            https://github.com/fedora-modularity/libmodulemd
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/fedora-modularity/libmodulemd/archive/%{name}-%{version}.tar.gz
%define sha512 %{name}-%{version}=0dc6dec1c679caf5b233e47f92ccef790aa3739d696bb6042153284612f7ea6c9e7c0c6cc6659f081c339f7a28c62f14ae85bf88d245fe74bcdcf1eac5e5e358

BuildRequires:  meson
BuildRequires:  clang-devel
BuildRequires:  gcc
BuildRequires:  glib-devel >= 2.58.3
BuildRequires:  valgrind
BuildRequires:  gobject-introspection-devel
BuildRequires:  python3-pygobject
BuildRequires:  python3-pycodestyle
BuildRequires:  python3-autopep8
BuildRequires:  gtk-doc
BuildRequires:  libyaml-devel

Requires:       libyaml
Requires:       glib >= 2.58.3

%description
C Library for manipulating module metadata files

%package        devel
Summary:        Header and development files for libmodulemd
Requires:       libyaml-devel
Requires:       glib-devel >= 2.58.3
Requires:       %{name} = %{version}-%{release}
%description    devel
It contains the libraries and header files.

%prep
%autosetup -p1 -n %{name}-%{name}-%{version}

%build
meson -Dprefix=%{_prefix} \
    -Ddeveloper_build=false \
    -Dbuild_api_v1=true \
    -Dbuild_api_v2=false \
    -Dwith_py3_overrides=true \
    -Dwith_py2_overrides=false api1

cd api1
ninja

%install
cd api1
DESTDIR=%{buildroot}/ ninja install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc README.md
%{_bindir}/modulemd-validator-v1
%{_libdir}/girepository-1.0/Modulemd-1.0.typelib
%{_libdir}/libmodulemd.so.*
%{_datadir}/gir-1.0/Modulemd-1.0.gir
%{_datadir}/gtk-doc/html/modulemd-1.0/*
%{python3_sitelib}/*

%files  devel
%defattr(-,root,root)
%{_libdir}/libmodulemd.so
%{_libdir}/pkgconfig/modulemd.pc
%{_includedir}/modulemd/*

%changelog
* Wed Nov 15 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 2.4.0-5
- Version bump due to glib change
* Wed Jul 20 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.4.0-4
- Remove clang from Requires
* Tue Jul 27 2021 Tapas Kundu <tkundu@vmware.com> 2.4.0-3
- Rebuild with updated clang
* Thu Oct 24 2019 Ankit Jain <ankitja@vmware.com> 2.4.0-2
- Added for ARM Build
* Wed May 15 2019 Ankit Jain <ankitja@vmware.com> 2.4.0-1
- Initial build. First version
