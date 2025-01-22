Summary:        library for handling OpenGL function pointer management.
Name:           libepoxy
Version:        1.5.10
Release:        3%{?dist}
License:        MIT
URL:            https://github.com/anholt/libepoxy
Group:          System Environment/Libraries
Vendor:         VMware, Inc.

Distribution:   Photon

Source0: https://github.com/anholt/libepoxy/releases/download/%{version}/%{name}-%{version}.tar.gz
%define sha512 %{name}=6786f31c6e2865e68a90eb912900a86bf56fd3df4d78a477356886ac3b6ef52ac887b9c7a77aa027525f868ae9e88b12e5927ba56069c2e115acd631fca3abee

BuildRequires:  meson >= 0.50
BuildRequires:  libglvnd-devel
BuildRequires:  libX11-devel
BuildRequires:  libglvnd-egl
BuildRequires:  libglvnd-glx
BuildRequires:  libglvnd-gles
BuildRequires:  libglvnd
BuildRequires:  libX11

Requires:       libX11
Requires:       libglvnd
Requires:       libglvnd-egl
Requires:       libglvnd-glx
Requires:       libglvnd-gles

%description
libepoxy is a library for handling OpenGL function pointer management.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}
Requires:       libglvnd-devel

%description    devel
It contains the libraries and header files to create applications

%prep
%autosetup -p1

%build
%meson \
      -Degl=yes \
      -Dglx=yes \
      -Dtests=true \
      %{nil}

%meson_build

%install
%meson_install

%ldconfig_scriptlets

%check
%meson_test

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/

%changelog
* Wed Jan 22 2025 Tapas Kundu <tapas.kundu@broadcom.com> 1.5.10-3
- Bump version as a part of meson upgrade
* Wed Jun 14 2023 Shivani Agarwal <shivania2@vmware.com> 1.5.10-2
- Bump version as a part of libX11 upgrade
* Tue Aug 23 2022 Shivani Agarwal <shivania2@vmware.com> 1.5.10-1
- Version update
* Wed Aug 04 2021 Alexey Makhalov <amakhalov@vmware.com> 1.5.8-1
- Version update
* Thu Jun 13 2019 Alexey Makhalov <amakhalov@vmware.com> 1.4.0-1
- Version update
* Tue May 19 2015 Alexey Makhalov <amakhalov@vmware.com> 1.2-1
- Initial version
