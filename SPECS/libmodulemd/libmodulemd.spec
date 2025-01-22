Summary:        Module manipulating metadata files
Name:           libmodulemd
Version:        2.13.0
Release:        6%{?dist}
License:        MIT
URL:            https://github.com/fedora-modularity/libmodulemd
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/fedora-modularity/libmodulemd/archive/%{name}-%{version}.tar.gz
%define sha512 %{name}-%{version}=212fd2a6797ea003d11d58d47bdb249fd3cb67fe2188c46a90c9b4fc46147817444e5aa068d2eaeb6b19670b1b05a21823e1f29ae611a14bd1ea428001d7d371

BuildRequires:  meson
BuildRequires:  clang-devel
BuildRequires:  gcc
BuildRequires:  glib-devel >= 2.68.4
BuildRequires:  glib-doc
BuildRequires:  valgrind
BuildRequires:  python3-devel
BuildRequires:  python3
BuildRequires:  python3-gobject-introspection
BuildRequires:  gobject-introspection-devel
BuildRequires:  python3-pygobject
BuildRequires:  python3-pycodestyle
BuildRequires:  python3-autopep8
BuildRequires:  gtk-doc
BuildRequires:  libyaml-devel
BuildRequires:  file-devel

Requires:       libyaml
Requires:       rpm-libs
Requires:       glib >= 2.68.4

%description
C Library for manipulating module metadata files

%package        devel
Summary:        Header and development files for libmodulemd
Requires:       libyaml-devel
Requires:       %{name} = %{version}-%{release}
Requires:       glib-devel >= 2.68.4
%description    devel
It contains the libraries and header files.

%prep
%autosetup -p1 -n %{name}-%{name}-%{version}

%build
meson \
    -Dprefix=%{_prefix} \
    -Dwith_py2=false \
    -Dwith_manpages=disabled \
    api1

cd api1
ninja

%install
cd api1
DESTDIR=%{buildroot}/ ninja install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/modulemd-validator
%{_libdir}/girepository-1.0/Modulemd-2.0.typelib
%{_libdir}/libmodulemd.so.*
%{_datadir}/gir-1.0/Modulemd-2.0.gir
%{_datadir}/gtk-doc/html/modulemd-2.0/*
%{python3_sitelib}/*

%files  devel
%defattr(-,root,root)
%{_libdir}/libmodulemd.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/modulemd-2.0/*.h

%changelog
* Wed Jan 22 2025 Tapas Kundu <tapas.kundu@broadcom.com> 2.13.0-6
- Bump version as a part of meson upgrade
* Sat Oct 07 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 2.13.0-5
- Bump version as part of glib upgrade
* Tue Nov 22 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.13.0-4
- Bump version as a part of llvm upgrade
* Mon Oct 31 2022 Piyush Gupta <gpiyush@vmware.com> 2.13.0-3
- Remove unkonw option developer_build.
* Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 2.13.0-2
- Bump up to compile with python 3.10
* Sat Aug 28 2021 Ankit Jain <ankitja@vmware.com> 2.13.0-1
- Updated to 2.13.0
* Sat Dec 12 2020 Shreenidhi Shedi <sshedi@vmware.com> 2.11.0-1
- Upgrade to v2.11.0
* Thu Aug 13 2020 Ankit Jain <ankitja@vmware.com> 2.9.4-1
- Updated to 2.9.4
* Thu Oct 24 2019 Ankit Jain <ankitja@vmware.com> 2.4.0-2
- Added for ARM Build
* Wed May 15 2019 Ankit Jain <ankitja@vmware.com> 2.4.0-1
- Initial build. First version
