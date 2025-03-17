Summary:        Thin layer of types for graphic libraries.
Name:           graphene
Version:        1.10.8
Release:        3%{?dist}
URL:            https://github.com/ebassi/graphene
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/ebassi/graphene/archive/refs/tags//%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  meson >= 0.50
BuildRequires:  ninja-build
BuildRequires:  gobject-introspection-devel

Requires: gobject-introspection

%description
Graphene provides a small set of mathematical types needed to implement graphic
libraries that deal with 2D and 3D transformations and projections.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -p1

%build
%meson \
      -Dtests=true \
      -Dinstalled_tests=false \
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
%{_libdir}/girepository-1.0/
%{_libdir}/libgraphene-1.0.so.0*

%files devel
%defattr(-,root,root)
%{_includedir}/graphene-1.0/
%dir %{_libdir}/graphene-1.0
%{_libdir}/graphene-1.0/include/
%{_libdir}/libgraphene-1.0.so
%{_libdir}/pkgconfig/graphene-1.0.pc
%{_libdir}/pkgconfig/graphene-gobject-1.0.pc
%{_libexecdir}/installed-tests/*
%{_datadir}/gir-1.0/

%changelog
* Wed Jan 22 2025 Tapas Kundu <tapas.kundu@broadcom.com> 1.10.8-3
- Bump version as a part of meson upgrade
* Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 1.10.8-2
- Release bump for SRP compliance
* Mon Sep 5 2022 Shivani Agarwal <shivania2@vmware.com> 1.10.8-1
- Initial version
